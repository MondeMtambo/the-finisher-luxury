"""
THE FINISHER LUXURY — Autonomous Agent API Views
================================================
Endpoints to inspect and interact with the 24/7 Sentinel Guardian Agent.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import os
import json
from django.conf import settings
from crm.management.commands.autonomous_guardian_agent import run_agent_cycle, TELEMETRY_FILE

class SentinelAgentStatusView(APIView):
    """
    GET /api/agent/sentinel/status/
    Returns the latest telemetry snapshot of the 24/7 Sentinel Agent.
    If no telemetry file exists yet, triggers an immediate cycle.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if os.path.exists(TELEMETRY_FILE):
            try:
                with open(TELEMETRY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return Response(data, status=status.HTTP_200_OK)
            except Exception:
                pass
        
        # Fallback / initialize on-demand
        data = run_agent_cycle(verbose=False)
        return Response(data, status=status.HTTP_200_OK)


class SentinelAgentTriggerPulseView(APIView):
    """
    POST /api/agent/sentinel/pulse/
    Forces an immediate autonomous pulse and returns fresh telemetry.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only admins/executives may manually force an autonomous pulse
        user = request.user
        is_admin = user.is_superuser or (getattr(user, 'username', '').lower() == 'adminluxury')
        profile = getattr(user, 'profile', None)
        if profile and profile.role in ['admin', 'executive']:
            is_admin = True

        if not is_admin:
            return Response(
                {'error': 'Restricted to Executive Administrators.'},
                status=status.HTTP_403_FORBIDDEN
            )

        telemetry = run_agent_cycle(verbose=False)
        return Response({
            'message': 'Autonomous Guardian Agent pulse completed successfully.',
            'telemetry': telemetry
        }, status=status.HTTP_200_OK)

class SentinelAgentCronView(APIView):
    """
    GET /api/agent/sentinel/cron/
    Automated execution endpoint triggered by Vercel Cron or external uptime monitors.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        cron_secret = os.environ.get('CRON_SECRET', '')
        auth_header = request.headers.get('Authorization', '')
        user_agent = request.headers.get('User-Agent', '')

        if cron_secret and auth_header != f'Bearer {cron_secret}' and 'vercel-cron' not in user_agent:
            return Response(
                {'error': 'Unauthorized cron invocation.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        telemetry = run_agent_cycle(verbose=False)
        return Response({
            'status': 'ok',
            'agent': 'FINISHER SENTINEL 24/7 GUARDIAN',
            'telemetry': telemetry
        }, status=status.HTTP_200_OK)

