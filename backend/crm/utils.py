"""Utility helpers for THE FINISHER LUXURY backend."""
from typing import Optional
import os

_ENV_TRUSTED = [ip.strip() for ip in os.environ.get('TRUSTED_IPS', '').split(',') if ip.strip()]
TRUSTED_IP_WHITELIST = set(
    _ENV_TRUSTED or [
        '41.198.159.124',  # Owner's trusted network (example)
    ]
)

OWNER_ADMIN_USERNAME = 'adminluxury'

MAX_ACCOUNTS_PER_IP = int(os.environ.get('MAX_ACCOUNTS_PER_IP', '2') or '2')

DISABLE_IP_LIMIT = (os.environ.get('DISABLE_IP_LIMIT', 'true').lower() == 'true')


def get_client_ip(request) -> Optional[str]:
    """Extract the originating client IP address from the incoming request."""
    if request is None:
        return None

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:

        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def is_trusted_ip(ip_address: Optional[str]) -> bool:
    """Return True when the provided IP address belongs to a trusted network.

    If DISABLE_IP_LIMIT is set (default true for testing), always return True to
    allow registrations from any IP.
    """
    if DISABLE_IP_LIMIT:
        return True
    if not ip_address:
        return False
    return ip_address in TRUSTED_IP_WHITELIST


def is_owner_admin_user(user) -> bool:
    """Check if the given Django user object represents the owner admin account."""
    if not user or not getattr(user, 'username', None):
        return False
    return user.username.lower() == OWNER_ADMIN_USERNAME.lower()


def normalize_company_name(company_name: Optional[str]) -> str:
    """Normalize company names for consistent multi-tenant scoping."""
    if not company_name:
        return ''
    return ' '.join(str(company_name).strip().split())
