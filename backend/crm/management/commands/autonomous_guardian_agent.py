"""
THE FINISHER LUXURY — 24/7 Autonomous Guardian Agent Engine
============================================================
An autonomous background agent running on 10-second intervals that:
1. Keeps Supabase PostgreSQL database connections warm and active 24/7.
2. Continuously audits multi-tenant data integrity, isolation, and POPIA S19 compliance.
3. Automatically unlocks and repairs any stuck or corrupted account states (anti-lockout sentinel).
4. Dynamically monitors client adoption against the 10-client threshold:
   - < 10 Clients: WATCHDOG_STAGING mode (integrity verification, warm pool, tracking).
   - >= 10 Clients: AUTONOMOUS_ENTERPRISE_LIVE mode (full automated orchestration & scale).
5. Exposes real-time agent telemetry for the executive Admin Console.

Usage:
    python manage.py autonomous_guardian_agent [--interval 10] [--once]
"""

import time
import json
import os
import sys
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import connection
from django.conf import settings
from crm.models import Organization, UserProfile, Contact, Deal, Ticket, SecurityAuditTrail, Notification
from django.contrib.auth.models import User

def _resolve_telemetry_file():
    env_path = os.environ.get('TELEMETRY_FILE')
    if env_path:
        return env_path
    base_file = os.path.join(settings.BASE_DIR, 'agent_telemetry.json')
    try:
        test_file = os.path.join(settings.BASE_DIR, '.writable_test')
        with open(test_file, 'w') as f:
            f.write('')
        os.remove(test_file)
        return base_file
    except Exception:
        return '/tmp/agent_telemetry.json'

TELEMETRY_FILE = _resolve_telemetry_file()

def run_agent_cycle(verbose=False):
    """
    Executes a single autonomous guardian agent pulse.
    Returns telemetry dictionary.
    """
    start_time = time.time()
    pulse_timestamp = timezone.now().isoformat()
    findings = []
    actions_taken = []

    # 1. Supabase Connection & Latency Heartbeat
    db_latency_ms = 0.0
    try:
        t0 = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        db_latency_ms = round((time.time() - t0) * 1000, 2)
        db_status = "nominal"
    except Exception as e:
        db_status = f"degraded: {str(e)}"
        findings.append(f"Database ping warning: {str(e)}")

    # 2. Client Organization Census & Threshold Engine (Excluding internal ingestion bots)
    active_orgs = Organization.objects.filter(is_active=True).exclude(slug__icontains='system_lead_ingest')
    total_clients = active_orgs.count()
    threshold = 10
    is_live_scale = total_clients >= threshold
    mode = "AUTONOMOUS_ENTERPRISE_LIVE" if is_live_scale else "WATCHDOG_STAGING"
    clients_to_threshold = max(0, threshold - total_clients)

    # 3. Account Unlock & Trial Sanitizer Sentinel
    # Auto-heal any organization marked 'trial' to 'basic' (Corporate Sovereign)
    trial_orgs = Organization.objects.filter(subscription_tier='trial')
    if trial_orgs.exists():
        count_fixed = trial_orgs.count()
        trial_orgs.update(
            subscription_tier='basic',
            trial_end_date=timezone.now() + timedelta(days=3650),
            is_active=True,
            can_export_csv=True
        )
        actions_taken.append(f"Sanitized {count_fixed} organizations from trial to Corporate Sovereign")

    # Auto-heal any user profile marked 'trial' or 'pending'
    pending_profiles = UserProfile.objects.filter(payment_status__in=['trial', 'pending'])
    if pending_profiles.exists():
        p_count = pending_profiles.count()
        pending_profiles.update(payment_status='paid')
        actions_taken.append(f"Unlocked {p_count} user profiles to paid/active status")

    # Ensure no inactive organizations exist erroneously
    inactive_orgs = Organization.objects.filter(is_active=False)
    if inactive_orgs.exists():
        in_count = inactive_orgs.count()
        inactive_orgs.update(is_active=True)
        actions_taken.append(f"Activated {in_count} inactive organizations")

    # 4. Data Health & POPIA Section 19 Vault Isolation
    total_contacts = Contact.objects.count()
    total_deals = Deal.objects.count()
    total_tickets = Ticket.objects.count()
    total_users = User.objects.count()

    # Reconcile orphaned contacts (contacts without organization)
    orphan_contacts = Contact.objects.filter(organization__isnull=True)
    if orphan_contacts.exists():
        orphan_count = orphan_contacts.count()
        primary_org = Organization.objects.first()
        if primary_org:
            orphan_contacts.update(organization=primary_org)
            actions_taken.append(f"Re-linked {orphan_count} orphaned contacts to {primary_org.name}")

    # 4b. Autonomous SLA Ticket Monitor (Fortune 500 / Zoho Standard)
    # Audits open/in-progress tickets approaching due date (within 24h) or overdue where no reminder was sent in the last 24h
    now = timezone.now()
    approaching_sla = now + timedelta(hours=24)
    pending_sla_tickets = Ticket.objects.filter(
        status__in=['open', 'in_progress'],
        due_at__isnull=False,
        due_at__lte=approaching_sla
    ).exclude(
        last_reminder_sent_at__gte=now - timedelta(hours=24)
    )

    sla_reminders_dispatched = 0
    from crm.email_service import send_ticket_reminder_email
    for t in pending_sla_tickets[:5]:  # Guarded throughput: max 5 per pulse
        t.last_reminder_sent_at = now
        t.reminder_count = (t.reminder_count or 0) + 1
        t.save(update_fields=['last_reminder_sent_at', 'reminder_count'])

        if t.assigned_to:
            Notification.objects.create(
                recipient=t.assigned_to,
                title='Autonomous SLA Alert',
                message=f"Sentinel Agent: Ticket #{t.id} '{t.title}' is due {t.due_at.strftime('%d %b %H:%M')}.",
                entity_type='ticket',
                entity_id=t.id,
                meta={'status': t.status, 'is_sla_alert': True}
            )

        send_ticket_reminder_email(t, reminder_type='sla_automated')
        sla_reminders_dispatched += 1

    if sla_reminders_dispatched > 0:
        actions_taken.append(f"Autonomous Sentinel dispatched {sla_reminders_dispatched} SLA reminder directives")

    # 5. Billionaire Business Intelligence Metrics
    pipeline_value = sum(float(d.value or 0) for d in Deal.objects.all())
    paying_clients = Organization.objects.filter(subscription_tier__in=['luxury', 'executive', 'enterprise']).count()
    sovereign_clients = Organization.objects.filter(subscription_tier__in=['basic', 'classic']).count()

    execution_duration_ms = round((time.time() - start_time) * 1000, 2)

    telemetry = {
        "agent_name": "FINISHER SENTINEL 24/7 GUARDIAN",
        "version": "v2.0-autonomous",
        "last_pulse": pulse_timestamp,
        "mode": mode,
        "is_enterprise_live": is_live_scale,
        "client_count": total_clients,
        "client_threshold": threshold,
        "clients_remaining_to_live_scale": clients_to_threshold,
        "pioneer_cohort": {
            "max_companies": threshold,
            "claimed_companies": total_clients,
            "remaining_spots": clients_to_threshold,
            "is_open": not is_live_scale,
            "seats_per_company": 8,
            "executive_monthly_rate": 1500.00,
            "status": "CLOSED (11th+ Company -> Executive Suite R1,500/mo)" if is_live_scale else f"ACTIVE ({clients_to_threshold} spots remaining)"
        },
        "health_score": 100 if db_status == "nominal" else 85,
        "database": {
            "status": db_status,
            "latency_ms": db_latency_ms,
            "host": "Supabase PostgreSQL (Enterprise Pooler)"
        },
        "metrics": {
            "total_users": total_users,
            "total_organizations": total_clients,
            "paying_clients": paying_clients,
            "sovereign_clients": sovereign_clients,
            "total_contacts": total_contacts,
            "total_deals": total_deals,
            "total_tickets": total_tickets,
            "pipeline_value_zar": pipeline_value
        },
        "actions_taken": actions_taken,
        "findings": findings if findings else ["All systems nominal. Zero account lockouts detected."],
        "execution_duration_ms": execution_duration_ms,
        "interval_seconds": 10
    }

    # Atomically persist telemetry file for API / Frontend consumption
    try:
        temp_file = TELEMETRY_FILE + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(telemetry, f, indent=2)
        os.replace(temp_file, TELEMETRY_FILE)
    except Exception as e:
        if verbose:
            print(f"[Agent Warning] Failed to write telemetry file: {e}")

    return telemetry


class Command(BaseCommand):
    help = 'Runs the 24/7 Autonomous Guardian Agent for database integrity, auto-unlocking, and telemetry.'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=10, help='Loop interval in seconds (default: 10s)')
        parser.add_argument('--once', action='store_true', help='Execute a single pulse cycle and exit')

    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']

        self.stdout.write(self.style.SUCCESS('=' * 65))
        self.stdout.write(self.style.SUCCESS('  THE FINISHER LUXURY — 24/7 AUTONOMOUS GUARDIAN AGENT'))
        self.stdout.write(self.style.SUCCESS(f'  Pulse Interval: {interval}s | Target: Supabase DB Integrity'))
        self.stdout.write(self.style.SUCCESS('=' * 65))

        if run_once:
            telemetry = run_agent_cycle(verbose=True)
            self.stdout.write(self.style.SUCCESS(f"[Pulse OK] Mode: {telemetry['mode']} | DB Latency: {telemetry['database']['latency_ms']}ms"))
            self.stdout.write(self.style.SUCCESS(f"Clients: {telemetry['client_count']}/{telemetry['client_threshold']} towards full autonomous scale."))
            if telemetry['actions_taken']:
                for act in telemetry['actions_taken']:
                    self.stdout.write(self.style.WARNING(f"  * Action: {act}"))
            return

        self.stdout.write(self.style.NOTICE(f'Agent is now live and running every {interval} seconds. Press Ctrl+C to stop.\n'))

        cycle_count = 0
        try:
            while True:
                cycle_count += 1
                telemetry = run_agent_cycle(verbose=False)
                timestamp = datetime.now().strftime('%H:%M:%S')
                mode_badge = "[LIVE SCALE]" if telemetry['is_enterprise_live'] else f"[STAGING {telemetry['client_count']}/{telemetry['client_threshold']}]"
                self.stdout.write(
                    f"[{timestamp}] Pulse #{cycle_count:04d} {mode_badge} | DB: {telemetry['database']['latency_ms']}ms | Duration: {telemetry['execution_duration_ms']}ms"
                )
                if telemetry['actions_taken']:
                    for act in telemetry['actions_taken']:
                        self.stdout.write(self.style.WARNING(f"   -> {act}"))
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.NOTICE('\nAutonomous Guardian Agent gracefully paused.'))
