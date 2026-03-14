"""
MFA (Multi-Factor Authentication) Utilities
Handles OTP generation, sending, and verification for email-based MFA
"""
import logging
import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def generate_mfa_code(length=6):
    """Generate a random 6-digit numeric code"""
    return ''.join(random.choices(string.digits, k=length))


def send_mfa_code_email(user, mfa_code):
    """
    Send MFA code via email to user's email address
    Returns: (success: bool, message: str)
    """
    try:
        first_login = getattr(getattr(user, 'profile', None), 'requires_password_reset', False)
        if first_login:
            subject = "Welcome to THE FINISHER LUXURY - Verify Your First Login"
            intro_line = "Hi"
            body_line = "Welcome to The Finisher Luxury. Please use these digits to verify your first login."
        else:
            subject = "Welcome back - THE FINISHER LUXURY Login Verification"
            intro_line = "Welcome back"
            body_line = "Please use this 6 digit OTP to login:"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; max-width: 500px; margin: 0 auto; border-radius: 8px; padding: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; text-align: center;">Finisher CRM</h2>
                    
                    <p style="color: #555; font-size: 16px;">{intro_line} <strong>{user.first_name or user.username}</strong>,</p>
                    
                    <p style="color: #555; font-size: 14px;">{body_line}</p>
                    
                    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 6px; text-align: center; margin: 20px 0;">
                        <p style="font-size: 36px; font-weight: bold; color: #2c3e50; letter-spacing: 5px; margin: 0;">
                            {mfa_code}
                        </p>
                    </div>
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        ⏱️ This code expires in <strong>5 minutes</strong>
                    </p>
                    
                    <p style="color: #777; font-size: 13px; margin-top: 30px;">
                        If you didn't request this code, please ignore this email. Your account is secure.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="color: #aaa; font-size: 11px; text-align: center;">
                        The Finisher Team<br>
                        <a href="https://www.thefinisher.co.za" style="color: #3498db; text-decoration: none;">Visit our website</a>
                    </p>
                </div>
            </body>
        </html>
        """
        
        plain_message = f"""
        {intro_line} {user.first_name or user.username},
        
        {body_line} {mfa_code}
        
        This code expires in 5 minutes.
        
        If you didn't request this code, please ignore this email.
        
        The Finisher Team
        """
        
        if not user.email:
            raise ValueError('User has no email address')

        # Use Django's send_mail; avoid passing unsupported kwargs like `timeout`
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True, "OTP sent successfully"
    
    except Exception as e:
        logger.exception('Failed to send MFA email to %s', getattr(user, 'email', None))
        return False, f"Failed to send OTP: {str(e)}"


def create_mfa_code(user):
    """
    Create and store MFA code for user
    Returns: (code: str, success: bool, message: str)
    """
    profile = user.profile
    code = generate_mfa_code()

    profile.mfa_code = code
    profile.mfa_code_created_at = timezone.now()
    profile.mfa_code_attempts = 0
    profile.save()

    success, message = send_mfa_code_email(user, code)
    
    return code, success, message


def verify_mfa_code(user, provided_code):
    """
    Verify MFA code for user
    Returns: (success: bool, message: str)
    """
    profile = user.profile

    if not profile.mfa_enabled:
        return True, "MFA is disabled for this account"

    if not profile.mfa_code:
        return False, "No verification code generated. Please request a new one."

    if profile.mfa_code_attempts >= settings.MFA_MAX_ATTEMPTS:
        profile.mfa_code = None
        profile.mfa_code_attempts = 0
        profile.save()
        return False, f"Too many failed attempts. Please request a new code."

    expiry_time = profile.mfa_code_created_at + timedelta(minutes=settings.MFA_CODE_EXPIRY_MINUTES)
    if timezone.now() > expiry_time:
        profile.mfa_code = None
        profile.save()
        return False, "Verification code has expired. Please request a new one."

    if provided_code.strip() != profile.mfa_code:
        profile.mfa_code_attempts += 1
        remaining = settings.MFA_MAX_ATTEMPTS - profile.mfa_code_attempts
        profile.save()
        return False, f"Incorrect code. {remaining} attempts remaining."

    profile.mfa_code = None
    profile.mfa_code_attempts = 0
    profile.mfa_verified_at = timezone.now()
    profile.save()
    
    return True, "Verification successful"


def is_mfa_required(user):
    """
    Check if MFA is required for user.
    MFA is enforced for everyone BELOW CEO level:
      - executive, manager, supervisor, user => MFA required
      - admin/CEO, superuser, staff => MFA skipped
    """
    if user.is_superuser or user.is_staff:
        return False

    profile = user.profile

    if profile.role == 'admin':
        return False

    return profile.mfa_enabled
