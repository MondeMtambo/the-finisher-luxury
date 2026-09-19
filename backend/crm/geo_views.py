"""
THE FINISHER LUXURY — Network Security Diagnostics Endpoint
Allows the Executive Directorate and users to verify their live IP, Country, and VPN status.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .geo_security import verify_network_security


class NetworkSecurityCheckView(APIView):
    """
    Public Diagnostic Endpoint:
    GET /api/security/network-check/
    Returns live inspection data showing whether access is Allowed or Blocked by the Geo & Anti-VPN Shield.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        report = verify_network_security(request)
        return Response(report)
