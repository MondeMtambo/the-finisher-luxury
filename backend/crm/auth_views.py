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
from .mfa_utils import create_mfa_code, verify_mfa_code, is_mfa_required
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
            user = User.objects.filter(email__iexact=raw_identifier).first()
            if not user:
                raise serializers.ValidationError({'detail': 'No account found with that email.'})
            attrs[self.username_field] = user.username

        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    """
    JWT login endpoint with IP tracking.
    POST /api/auth/login/
    Body: {username, password}
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailOnlyLoginTokenSerializer
    
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

                    skip_mfa = user.is_superuser or user.is_staff or is_owner_admin_user(user)

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

                    if not skip_mfa and is_mfa_required(user):

                        code, success, msg = create_mfa_code(user)


                        email_status = 'sent' if success else 'failed'
                        return Response({
                            'requires_mfa': True,
                            'user_id': user.id,
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

        success, message = verify_mfa_code(user, mfa_code)
        
        if not success:
            return Response({
                'error': 'MFA verification failed',
                'message': message
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        
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
                    from_email='thefinishercrm@gmail.com',
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
