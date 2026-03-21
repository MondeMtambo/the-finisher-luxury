import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

def is_mfa_required(user):
    if not hasattr(user, 'profile'):
        return False
    return getattr(user.profile, 'mfa_enabled', True)

def create_mfa_code(user):
    if not hasattr(user, 'profile'):
        return None, False, "User has no profile"
    
    profile = user.profile
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    profile.mfa_code = code
    profile.mfa_code_created_at = timezone.now()
    profile.mfa_code_attempts = 0
    profile.save()

    try:
        send_mail(
            subject='🔐 Your Login Verification Code - THE FINISHER CRM',
            message=f'''Hello {user.first_name or user.username},

Your 6-digit verification code is: {code}

This code will expire in 10 minutes.

Best regards,
THE FINISHER
MTAMBO HOLDINGS Team''',
            from_email='thefinishercrm@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return code, True, "Email sent"
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send MFA email: {e}")
        return code, False, str(e)

def verify_mfa_code(user, code):
    if not hasattr(user, 'profile'):
        return False, "User profile not found"
        
    profile = user.profile
    
    if not profile.mfa_code or profile.mfa_code_attempts >= 3:
        return False, "Invalid or expired code. Please request a new one."
        
    if profile.mfa_code_created_at and timezone.now() > profile.mfa_code_created_at + timedelta(minutes=10):
        return False, "Code has expired. Please request a new one."
        
    if profile.mfa_code != code:
        profile.mfa_code_attempts += 1
        profile.save()
        return False, "Incorrect verification code."
        
    profile.mfa_code = None
    profile.mfa_code_created_at = None
    profile.mfa_code_attempts = 0
    profile.mfa_verified_at = timezone.now()
    profile.save()
    
    return True, "Verification successful"