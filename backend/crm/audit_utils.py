"""
Enterprise Security Audit Logging Utility for THE FINISHER LUXURY.
POPIA Section 19 & ISO 27001 compliant non-repudiation audit recorder.
"""
import logging
from django.utils import timezone

logger = logging.getLogger('crm.security')


def get_client_ip(request):
    """
    Safely extract client IP address behind reverse proxies (Cloudflare & Render).
    """
    if not request:
        return None
    
    # 1. Cloudflare True-Client-IP
    cf_ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if cf_ip:
        return cf_ip.strip()
    
    # 2. X-Forwarded-For (Render / Load Balancer)
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    
    # 3. Direct Remote Address
    return request.META.get('REMOTE_ADDR')


def get_client_user_agent(request):
    """Extract client User-Agent string."""
    if not request:
        return ''
    return request.META.get('HTTP_USER_AGENT', '')[:500]


def record_audit_event(
    event_type: str,
    description: str,
    user=None,
    username_attempted: str = '',
    request=None,
    severity: str = 'INFO',
    metadata: dict = None,
    organization=None
):
    """
    Record an immutable event into the SecurityAuditTrail.
    Failsafe: Never raises an unhandled exception that disrupts core operations.
    """
    try:
        from .models import SecurityAuditTrail

        # Auto-infer user from request if not explicitly provided
        if not user and request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user

        # Auto-infer organization from user profile if not provided
        if not organization and user and hasattr(user, 'profile'):
            organization = getattr(user.profile, 'organization', None)

        # Auto-infer username if not provided
        if not username_attempted:
            if user:
                username_attempted = user.username
            elif request and hasattr(request, 'data') and isinstance(request.data, dict):
                username_attempted = request.data.get('username', '')

        ip = get_client_ip(request)
        ua = get_client_user_agent(request)

        entry = SecurityAuditTrail.objects.create(
            user=user if user and getattr(user, 'is_authenticated', False) else None,
            username_attempted=username_attempted[:150],
            organization=organization,
            event_type=event_type,
            severity=severity.upper(),
            description=description,
            ip_address=ip,
            user_agent=ua,
            metadata=metadata or {},
            timestamp=timezone.now(),
        )
        return entry
    except Exception as e:
        logger.error(f"[POPIA Audit] Failed to record security event {event_type}: {e}", exc_info=True)
        return None
