"""
THE FINISHER LUXURY — GeoAndVPNShieldMiddleware
Blocks foreign connections (outside South Africa) and commercial VPN tunnels from registering,
submitting access requests, or attacking the backend Supabase database.
"""

from django.http import JsonResponse
from .geo_security import verify_network_security


class GeoAndVPNShieldMiddleware:
    """
    Zero-Trust Security Middleware:
    Inspects incoming requests to public onboarding and auth endpoints.
    Enforces that traffic originates directly within South Africa (ZA) and blocks VPNs.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Critical Protected Paths (Public Onboarding & Registration surfaces)
        protected_prefixes = [
            '/api/auth/register/',
            '/api/public/request-access/',
            '/api/public/verify-access-request/',
            '/api/public/leads/',
        ]

        needs_shield = any(path.startswith(prefix) for prefix in protected_prefixes)

        if needs_shield:
            sec_report = verify_network_security(request)
            if not sec_report.get('allowed', True):
                return JsonResponse({
                    'error': 'Access Denied: Zero-Trust Perimeter Policy Enforced.',
                    'detail': sec_report.get('reason'),
                    'client_ip': sec_report.get('client_ip'),
                    'country': sec_report.get('country'),
                    'is_vpn_or_proxy': sec_report.get('is_vpn_or_proxy'),
                    'status': 'BLOCKED'
                }, status=403)

        return self.get_response(request)
