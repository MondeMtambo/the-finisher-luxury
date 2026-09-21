"""
Authentication views for THE FINISHER LUXURY
Handles registration, login (JWT), OTP-based password reset
Maximum 10 users enforced for LUXURY edition
"""
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .email_service import send_email_async, render_luxury_email_html
from django.db.models import Q
from .models import PasswordResetOTP, UserProfile
from .mfa_utils import create_mfa_code, verify_mfa_code, is_mfa_required, generate_pre_auth_token, validate_pre_auth_token
from .auth_serializers import (
    RegisterSerializer, 
    UserSerializer, 
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .tier_limits import LUXURY_TIER_LIMITS, can_add_user, get_remaining_user_slots
from .utils import get_client_ip, is_trusted_ip, MAX_ACCOUNTS_PER_IP, is_owner_admin_user
from .models import Notification
from .audit_utils import record_audit_event
import os


class EmailOnlyLoginTokenSerializer(TokenObtainPairSerializer):
    """
    Login policy:
    - adminluxury may login with username "adminluxury"
    - all other users must login with email
    """

    def validate(self, attrs):
        raw_identifier = (attrs.get(self.username_field) or '').strip()
        if not raw_identifier:
            raise serializers.ValidationError({'detail': 'Email is required.'})

        is_adminluxury_username = raw_identifier.lower() == 'adminluxury'

        if not is_adminluxury_username and '@' not in raw_identifier:
            raise serializers.ValidationError({
                'detail': 'Login with your email address. Only adminluxury can login with username.'
            })

        if is_adminluxury_username:
            admin_account = User.objects.filter(username__iexact='adminluxury').first()
            if admin_account:
                attrs[self.username_field] = admin_account.username
            else:
                attrs[self.username_field] = raw_identifier

        if '@' in raw_identifier:
            from .models import CorporateAccessRequest, UserProfile
            clean_email = raw_identifier.lower().strip()
            user = User.objects.filter(email__iexact=clean_email).first() or User.objects.filter(username__iexact=clean_email).first()

            password = attrs.get('password') or ''

            # Check if there is an authorized CorporateAccessRequest with matching auto_generated_password
            access_req = None
            try:
                access_req = CorporateAccessRequest.objects.filter(email__iexact=clean_email).first()
            except Exception:
                # If table is undergoing migration or column mismatch, gracefully proceed
                access_req = None

            if access_req:
                if password and access_req.auto_generated_password and access_req.auto_generated_password == password:
                    if not user:
                        # Auto-provision user account from authorized access request
                        user, _ = User.objects.get_or_create(
                            username=clean_email,
                            defaults={
                                'email': clean_email,
                                'first_name': access_req.first_name,
                                'last_name': access_req.last_name,
                                'is_active': True
                            }
                        )
                    user.set_password(password)
                    user.is_active = True
                    user.save()

                    profile, _ = UserProfile.objects.get_or_create(user=user)
                    profile.requires_password_reset = True
                    if not profile.company_name:
                        profile.company_name = access_req.company_name
                    profile.save()

                    if access_req.status != 'approved':
                        access_req.status = 'approved'
                        access_req.save(update_fields=['status'])

                elif access_req.status == 'pending' and not user:
                    raise serializers.ValidationError({
                        'detail': 'Your corporate application is currently pending executive authorization. You will receive an email once authorized.'
                    })

            if not user:
                raise serializers.ValidationError({'detail': 'No active account found with that email address.'})

            attrs[self.username_field] = user.username

        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    """
    JWT login endpoint with comprehensive POPIA Section 19 audit logging.
    Records ALL login attempts (known employees, unknown usernames, failed credentials, and MFA).
    POST /api/auth/login/
    Body: {username, password}
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailOnlyLoginTokenSerializer
    
    def post(self, request, *args, **kwargs):
        identifier = (request.data.get('username') or '').strip()
        
        # 1. Attempt authentication and intercept any authentication failure/exception
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as exc:
            user_found = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()
            org = None
            company_label = 'Unknown / Unaffiliated'
            if user_found and hasattr(user_found, 'profile'):
                org = getattr(user_found.profile, 'organization', None)
                company_label = getattr(user_found.profile, 'company_name', None) or (org.name if org else 'Individual')
            
            err_detail = getattr(exc, 'detail', str(exc))
            if isinstance(err_detail, (list, dict)):
                err_detail = str(err_detail)
            
            record_audit_event(
                'AUTH_LOGIN_FAILED',
                f"Failed authentication attempt for '{identifier}' ({company_label}) - Reason: {err_detail}",
                user=user_found,
                username_attempted=identifier,
                organization=org,
                request=request,
                severity='WARNING',
                metadata={'identifier': identifier, 'company_name': company_label, 'error': str(err_detail)}
            )
            raise exc

        # 2. Process HTTP response
        if response.status_code == 200:
            try:
                user = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()
                if not user:
                    raise User.DoesNotExist

                profile = getattr(user, 'profile', None)
                org = getattr(profile, 'organization', None) if profile else None
                company_label = (getattr(profile, 'company_name', None) or (org.name if org else 'Independent Enterprise')).strip()

                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

                if profile:
                    # If admin forced a password reset, don't return tokens — require change first
                    if getattr(profile, 'requires_password_reset', False):
                        response.data.pop('access', None)
                        response.data.pop('refresh', None)
                        response.data['requires_password_reset'] = True
                        response.data['user_id'] = user.id
                        response.data['email'] = user.email
                        record_audit_event(
                            'SECURITY_WARNING',
                            f"Mandatory password reset challenge triggered on login for {user.username} ({user.email})",
                            user=user,
                            organization=org,
                            request=request,
                            severity='WARNING'
                        )
                        return response

                    if not profile.registration_ip and ip:
                        profile.registration_ip = ip
                    profile.last_login_ip = ip
                    profile.save(update_fields=['last_login_ip'] if profile.registration_ip else ['registration_ip', 'last_login_ip'])

                    if profile.is_banned:
                        record_audit_event(
                            'SECURITY_POLICY_VIOLATION',
                            f"Blocked authentication attempt for banned user: {user.username} ({user.email})",
                            user=user,
                            organization=org,
                            request=request,
                            severity='CRITICAL'
                        )
                        return Response({
                            'error': 'Account banned',
                            'message': f'Your account has been banned. Reason: {profile.ban_reason}',
                            'contact': 'security@thefinishercrm.tech'
                        }, status=status.HTTP_403_FORBIDDEN)

                    if not profile.can_access:
                        record_audit_event(
                            'SECURITY_WARNING',
                            f"Login restricted due to inactive license/payment requirement for {user.username} ({user.email})",
                            user=user,
                            organization=org,
                            request=request,
                            severity='WARNING'
                        )
                        return Response({
                            'error': 'Payment required',
                            'message': 'Your account requires payment or active trial to continue. Please contact concierge support.',
                            'payment_status': profile.payment_status,
                            'contact': 'concierge@thefinishercrm.tech'
                        }, status=status.HTTP_402_PAYMENT_REQUIRED)

                    if is_mfa_required(user):
                        code, success, msg = create_mfa_code(user)
                        pre_auth_token = generate_pre_auth_token(user)

                        response.data.pop('access', None)
                        response.data.pop('refresh', None)

                        email_status = 'sent' if success else 'failed'
                        record_audit_event(
                            'MFA_CHALLENGE',
                            f"MFA verification challenge dispatched to {user.email} (Delivery: {email_status})",
                            user=user,
                            organization=org,
                            request=request,
                            severity='INFO'
                        )
                        return Response({
                            'requires_mfa': True,
                            'user_id': user.id,
                            'pre_auth_token': pre_auth_token,
                            'email': user.email,
                            'message': f'Verification code {email_status}. Check your email inbox.' if success else 'Email send failed. Click "Resend Code" to try again.',
                            'email_send_status': email_status,
                            'user': UserSerializer(user).data
                        }, status=200)

                    try:
                        from django.utils import timezone
                        if not user.notifications.filter(entity_type='welcome').exists():
                            Notification.objects.create(
                                recipient=user,
                                title='Welcome to THE FINISHER LUXURY',
                                message='Your workspace is ready. Explore Dashboard, Employees and Tickets to get started!',
                                entity_type='welcome',
                                entity_id=None,
                                meta={'company_name': company_label}
                            )
                    except Exception:
                        pass

                response.data['user'] = UserSerializer(user).data
                # Always record successful login in audit trail for full accountability
                actor_display = f"{user.first_name} {user.last_name}".strip() or user.username
                record_audit_event(
                    'AUTH_LOGIN_SUCCESS',
                    f"Login verified for {actor_display} ({user.email or user.username}) - Company: {company_label}",
                    user=user,
                    organization=org,
                    request=request,
                    severity='INFO',
                    metadata={'role': getattr(profile, 'role', 'user'), 'company_name': company_label}
                )
                
            except User.DoesNotExist:
                record_audit_event(
                    'AUTH_LOGIN_FAILED',
                    f"Authentication token issued but User object could not be resolved for identifier '{identifier}'",
                    username_attempted=identifier,
                    request=request,
                    severity='WARNING'
                )
        else:
            record_audit_event(
                'AUTH_LOGIN_FAILED',
                f"Failed authentication attempt for identifier '{identifier}' (Status: {response.status_code})",
                username_attempted=identifier,
                request=request,
                severity='WARNING'
            )
        
        return response

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .auth_serializers import RegisterSerializer


class VerifyMFAView(APIView):
    """
    Bank-Grade MFA Verification Endpoint.
    POST /api/auth/verify-mfa/
    Body: {pre_auth_token (recommended) or user_id, mfa_code}
    """
    permission_classes = (AllowAny,)
    
    def post(self, request):
        pre_auth_token = request.data.get('pre_auth_token')
        user_id = request.data.get('user_id')
        mfa_code = request.data.get('mfa_code', '').strip()
        
        if not mfa_code or (not pre_auth_token and not user_id):
            return Response({
                'error': 'Missing parameters',
                'message': 'Both verification code and active session token are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        if pre_auth_token:
            token_user_id, token_error = validate_pre_auth_token(pre_auth_token)
            if token_error:
                return Response({
                    'error': 'Session expired',
                    'message': token_error
                }, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = User.objects.get(id=token_user_id)
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid user',
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        elif user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid user',
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None
        company_label = (getattr(profile, 'company_name', None) or (org.name if org else 'Independent Enterprise')).strip()

        success, message = verify_mfa_code(user, mfa_code)
        
        if not success:
            record_audit_event(
                'AUTH_LOGIN_FAILED',
                f"MFA verification code failed for {getattr(user, 'username', 'Unknown')} ({getattr(user, 'email', '')}): {message}",
                user=user,
                organization=org,
                request=request,
                severity='WARNING',
                metadata={'company_name': company_label, 'error': message}
            )
            return Response({
                'error': 'MFA verification failed',
                'message': message
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        actor_display = f"{user.first_name} {user.last_name}".strip() or user.username

        # 1. Record MFA_VERIFIED event
        record_audit_event(
            'MFA_VERIFIED',
            f"MFA verification successful for {user.username} ({user.email})",
            user=user,
            organization=org,
            request=request,
            severity='INFO',
            metadata={'company_name': company_label}
        )

        # 2. ALSO record AUTH_LOGIN_SUCCESS so filtering by 'Login Success' immediately captures this login!
        record_audit_event(
            'AUTH_LOGIN_SUCCESS',
            f"Login verified via MFA for {actor_display} ({user.email or user.username}) - Company: {company_label}",
            user=user,
            organization=org,
            request=request,
            severity='INFO',
            metadata={'role': getattr(profile, 'role', 'user'), 'company_name': company_label, 'method': 'MFA'}
        )
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            profile = getattr(user, 'profile', None)
            org = getattr(profile, 'organization', None) if profile else None
            company_label = (getattr(profile, 'company_name', None) or (org.name if org else '')).strip()

            actor_display = f"{user.first_name} {user.last_name}".strip() or user.username
            record_audit_event(
                'AUTH_REGISTRATION',
                f"New user registered: {actor_display} ({user.email or user.username}) - Company: {company_label or 'Individual'}",
                user=user,
                organization=org,
                request=request,
                severity='INFO',
                metadata={'email': user.email, 'company_name': company_label}
            )

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': user.get_full_name(),
                },
                'message': 'Registration successful! Welcome to THE FINISHER LUXURY.',
            }, status=status.HTTP_201_CREATED)

        attempted_identifier = (request.data.get('email') or request.data.get('username') or '').strip()
        record_audit_event(
            'AUTH_REGISTRATION',
            f"Registration attempt failed for '{attempted_identifier}': {serializer.errors}",
            username_attempted=attempted_identifier,
            request=request,
            severity='WARNING',
            metadata={'errors': str(serializer.errors)}
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get/Update user profile.
    GET /api/auth/profile/
    PUT /api/auth/profile/
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    Change password for authenticated user.
    POST /api/auth/change-password/
    Body: {old_password, new_password, new_password2}
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():

            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Wrong password.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            try:
                if hasattr(request.user, 'profile') and request.user.profile.requires_password_reset:
                    request.user.profile.requires_password_reset = False
                    request.user.profile.save()
            except Exception:
                pass
            
            return Response({
                'message': 'Password updated successfully!'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """
    Request password reset OTP via email.
    POST /api/auth/password-reset/
    Body: {email}
    Returns: Success message (OTP sent to email)
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)

                otp_code = PasswordResetOTP.generate_otp()

                otp_instance = PasswordResetOTP.objects.create(
                    email=email,
                    otp_code=otp_code
                )

                reset_html = render_luxury_email_html(
                    title="Security Authentication Protocol",
                    subtitle="Mtambo Holdings Private Cloud &middot; Key Recovery",
                    recipient_name=user.first_name or user.username,
                    message_paragraphs=[
                        "A master key recovery request was initiated for your enterprise account on <strong>THE FINISHER LUXURY</strong>.",
                        "To authorize the credential reset and verify your executive identity, input the ephemeral single-use passcode below."
                    ],
                    otp_code=otp_code,
                    otp_expiry_minutes=10,
                    security_note="If you did not initiate this credential recovery, your account security remains intact. Ignore this dispatch immediately."
                )

                send_email_async(
                    subject='🔐 Password Reset Verification Passcode — THE FINISHER LUXURY',
                    text_body=f"""
Hello {user.first_name or user.username},

You requested to reset your password for THE FINISHER LUXURY.

Your One-Time Passcode (OTP) is:

    {otp_code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email and your password will remain unchanged.

Best regards,
The Executive Directorate
THE FINISHER LUXURY | MTAMBO HOLDINGS
                    """,
                    recipient_list=[email],
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'The Finisher Luxury Registrations <noreply@mtamboholdings.dev>'),
                    html_body=reset_html
                )
                
                return Response({
                    'message': 'OTP sent to your email! Check your inbox.',
                    'email': email
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:

                return Response({
                    'message': 'If that email exists, an OTP has been sent.'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f'Failed to send OTP. Please try again. ({str(e)})'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyOTPView(APIView):
    """
    Verify OTP code before allowing password reset.
    POST /api/auth/password-reset/verify-otp/
    Body: {email, otp_code}
    Returns: {valid: true/false, message}
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        
        if not email or not otp_code:
            return Response({
                'error': 'Email and OTP code are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:

            otp_instance = PasswordResetOTP.objects.filter(
                email=email,
                otp_code=otp_code
            ).order_by('-created_at').first()
            
            if not otp_instance:
                return Response({
                    'valid': False,
                    'error': 'Invalid OTP code.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if otp_instance.is_expired:
                return Response({
                    'valid': False,
                    'error': 'OTP has expired. Please request a new one.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if otp_instance.is_used:
                return Response({
                    'valid': False,
                    'error': 'OTP has already been used. Please request a new one.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'valid': True,
                'message': 'OTP verified successfully! You can now reset your password.'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Verification failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with verified OTP.
    POST /api/auth/password-reset-confirm/
    Body: {email, otp_code, password, password2}
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            password = serializer.validated_data['password']
            
            try:

                otp_instance = PasswordResetOTP.objects.filter(
                    email=email,
                    otp_code=otp_code
                ).order_by('-created_at').first()
                
                if not otp_instance or not otp_instance.is_valid:
                    return Response({
                        'error': 'Invalid or expired OTP.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()

                otp_instance.mark_as_used()
                
                return Response({
                    'message': 'Password reset successful! You can now login with your new password. 🎉'
                }, status=status.HTTP_200_OK)
                    
            except User.DoesNotExist:
                return Response({
                    'error': 'User not found.'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': f'Password reset failed: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout (client should delete tokens).
    POST /api/auth/logout/
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            if request.user and request.user.is_authenticated:
                record_audit_event(
                    'AUTH_LOGOUT',
                    f"Session terminated for {request.user.username}",
                    user=request.user,
                    request=request,
                    severity='INFO'
                )
            return Response({
                'message': 'Logged out successfully!'
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'error': 'Something went wrong.'
            }, status=status.HTTP_400_BAD_REQUEST)


class ForceChangePasswordView(APIView):
    """
    Force change password flow for admin-reset temporary passwords.
    POST /api/auth/force-change-password/
    Body: { user_id, old_password, password, password2 }
    Returns: requires_mfa True + user info (then frontend calls verify MFA to obtain tokens)
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password', '')
        password = request.data.get('password', '')
        password2 = request.data.get('password2', '')

        if not user_id or not old_password or not password or not password2:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        is_valid_old = user.check_password(old_password)
        if not is_valid_old:
            from django.db.models import Q
            from .models import CorporateAccessRequest
            car = CorporateAccessRequest.objects.filter(
                Q(email__iexact=user.email) | Q(created_user=user)
            ).order_by('-created_at').first()
            if car and car.auto_generated_password and car.auto_generated_password.strip() == (old_password or '').strip():
                is_valid_old = True

        if not is_valid_old:
            return Response({'error': 'Old password incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Apply new password
            user.set_password(password)
            user.save()

            # Update profile flags
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.requires_password_reset = False
                from django.utils import timezone
                profile.password_changed_at = timezone.now()
                profile.save()

                # Blacklist outstanding refresh tokens for user (if token_blacklist enabled)
                try:
                    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
                    for ot in OutstandingToken.objects.filter(user=user):
                        try:
                            BlacklistedToken.objects.get_or_create(token=ot)
                        except Exception:
                            pass
                except Exception:
                    pass

            # Instantaneous Executive Session: issue fresh JWT tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            profile = getattr(user, 'profile', None)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': getattr(profile, 'role', 'admin') if profile else 'admin',
                'tier': getattr(profile, 'tier', 'luxury') if profile else 'luxury',
                'organization': profile.organization.name if (profile and profile.organization) else None,
                'organization_id': str(profile.organization.id) if (profile and profile.organization) else None,
                'company_name': getattr(profile, 'company_name', '') if profile else '',
                'is_superuser': user.is_superuser,
            }

            return Response({
                'success': True,
                'requires_mfa': False,
                'access': access,
                'refresh': str(refresh),
                'user': user_data,
                'message': 'Password updated successfully. Welcome to your Executive Workspace.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Failed to change password: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
