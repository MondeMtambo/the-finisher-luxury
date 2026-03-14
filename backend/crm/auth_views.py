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
from django.conf import settings
from .models import PasswordResetOTP, UserProfile
from .mfa_utils import create_mfa_code, verify_mfa_code
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
import os

class LoginView(TokenObtainPairView):
    """
    JWT login endpoint with IP tracking.
    POST /api/auth/login/
    Body: {username, password}
    """
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            identifier = (request.data.get('username') or '').strip()
            try:
                user = User.objects.filter(username__iexact=identifier).first() or User.objects.filter(email__iexact=identifier).first()
                if not user:
                    raise User.DoesNotExist

                if hasattr(user, 'profile'):
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0].strip()
                    else:
                        ip = request.META.get('REMOTE_ADDR')

                    profile = user.profile
                    if not profile.registration_ip and ip:
                        profile.registration_ip = ip
                    profile.last_login_ip = ip
                    profile.save()

                    skip_mfa = user.is_superuser or user.is_staff

                    if user.profile.is_banned:
                        return Response({
                            'error': 'Account banned',
                            'message': f'Your account has been banned. Reason: {user.profile.ban_reason}',
                            'contact': 'support@thefinisher.co.za'
                        }, status=status.HTTP_403_FORBIDDEN)

                    if not user.profile.can_access:
                        return Response({
                            'error': 'Payment required',
                            'message': 'Your account requires payment to continue. Please contact support.',
                            'payment_status': user.profile.payment_status,
                            'contact': 'support@thefinisher.co.za'
                        }, status=status.HTTP_402_PAYMENT_REQUIRED)

                    if not skip_mfa:

                        code, success, msg = create_mfa_code(user)


                        email_status = 'sent' if success else 'failed'
                        mfa_prompt = (
                            'Hi. Welcome to The Finisher Luxury. Please use the 6-digit code sent to your email to verify your account.'
                            if profile.requires_password_reset else
                            'Welcome back. Please use these digits to verify your login.'
                        )
                        return Response({
                            'requires_mfa': True,
                            'user_id': user.id,
                            'email': user.email,
                            'message': mfa_prompt if success else 'Email send failed. Click "Resend Code" to try again.',
                            'email_send_status': email_status,
                            'requires_password_reset': profile.requires_password_reset,
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
                                meta={'company_name': getattr(user.profile, 'company_name', '')}
                            )
                    except Exception:
                        pass

                    response.data['user'] = UserSerializer(user).data
                
            except User.DoesNotExist:
                pass
        
        return response

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .auth_serializers import RegisterSerializer


class VerifyMFAView(APIView):
    """
    MFA verification endpoint
    POST /api/auth/verify-mfa/
    Body: {user_id, mfa_code}
    """
    permission_classes = (AllowAny,)
    
    def post(self, request):
        user_id = request.data.get('user_id')
        mfa_code = request.data.get('mfa_code', '').strip()
        
        if not user_id or not mfa_code:
            return Response({
                'error': 'Missing parameters',
                'message': 'Both user_id and mfa_code are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid user',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        profile = getattr(user, 'profile', None)
        was_first_login = bool(profile and profile.requires_password_reset and not profile.mfa_verified_at)

        success, message = verify_mfa_code(user, mfa_code)
        
        if not success:
            return Response({
                'error': 'MFA verification failed',
                'message': message
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        if was_first_login and profile and profile.onboarded_by and profile.onboarded_by != user:
            try:
                Notification.objects.create(
                    recipient=profile.onboarded_by,
                    title='Employee Verified First Login',
                    message=f"{user.get_full_name().strip() or user.username} verified first login OTP successfully.",
                    entity_type='onboarding',
                    entity_id=user.id,
                    meta={'event': 'first_login_otp_verified', 'employee_email': user.email}
                )
            except Exception:
                pass
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'message': 'OTP verified. Please change your temporary password now.' if profile and profile.requires_password_reset else 'Login successful'
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
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

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # Update basic User fields
        for field in ('first_name', 'last_name'):
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        # Update profile fields
        profile = getattr(user, 'profile', None)
        if profile:
            profile_fields = ('company_name', 'phone', 'job_title', 'department')
            for field in profile_fields:
                if field in request.data:
                    setattr(profile, field, request.data[field])
            profile.save()
        return Response(UserSerializer(user).data)


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

            profile = getattr(request.user, 'profile', None)
            was_reset_required = bool(profile and profile.requires_password_reset)

            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            try:
                if hasattr(request.user, 'profile') and request.user.profile.requires_password_reset:
                    request.user.profile.requires_password_reset = False
                    request.user.profile.save()

                if was_reset_required and profile and profile.onboarded_by and profile.onboarded_by != request.user:
                    Notification.objects.create(
                        recipient=profile.onboarded_by,
                        title='Employee Completed First Password Change',
                        message=f"{request.user.get_full_name().strip() or request.user.username} changed temporary password and completed initial access.",
                        entity_type='onboarding',
                        entity_id=request.user.id,
                        meta={'event': 'first_password_changed', 'employee_email': request.user.email}
                    )
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

                send_mail(
                    subject='🔐 Password Reset OTP - THE FINISHER CRM',
                    message=f"""
Hello {user.first_name or user.username},

You requested to reset your password for THE FINISHER CRM.

Your One-Time Password (OTP) is:

    {otp_code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email and your password will remain unchanged.

Best regards,
� THE FINISHER
MTAMBO HOLDINGS Team
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
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


class RequestAccessView(APIView):
    """
    Public endpoint to request access/demo. Sends email to system admin.
    POST /api/auth/request-access/
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        email = data.get('email', '')
        company = data.get('company_name', '')
        phone = data.get('phone', '')
        role = data.get('job_title', '')
        tier = data.get('tier', 'unknown')
        use_case = data.get('intended_use_case', '')

        subject = f"🚀 New Application: {company} ({tier.upper()})"
        message = f"""
A new CEO/Company has applied for access to THE FINISHER!

Applicant Details:
------------------
Name: {name}
Email: {email}
Phone: {phone}
Role: {role}
Company: {company}

Preferences:
------------
Requested Tier: {tier.upper()}
Intended Use Case: {use_case}

Please reach out to them to verify details, take payment, and onboard them via the Admin Console.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Send directly to the admin
                fail_silently=False,
            )
            return Response({'message': 'Application received successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Could not process application at this time.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """
    Logout (client should delete tokens).
    POST /api/auth/logout/
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:


            return Response({
                'message': 'Logged out successfully!'
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'error': 'Something went wrong.'
            }, status=status.HTTP_400_BAD_REQUEST)
