import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from crm.models import Organization, UserProfile, Notification
from crm.audit_utils import record_audit_event
from crm.email_service import send_email_async, render_luxury_email_html

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automate 7-day VIP trial transitions, 3-day grace period alerts, and vault locks with 100% data preservation.'

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(self.style.NOTICE(f"[{now.isoformat()}] Processing 7-day trial and 3-day grace period lifecycle..."))

        active_orgs = Organization.objects.filter(is_active=True)
        grace_notified_count = 0
        locked_count = 0

        for org in active_orgs:
            # Check if paid
            sub = getattr(org, 'subscription', None)
            if sub and sub.status == 'active':
                continue

            # Check if in 3-day grace period (Days 8-10)
            if org.is_in_grace_period:
                days_left = org.days_remaining_in_grace
                admins = UserProfile.objects.filter(organization=org, role='admin').select_related('user')
                for admin in admins:
                    if not admin.user:
                        continue

                    # Idempotent notification: max 1 notification per day of grace
                    notif_tag = f"grace_day_{days_left}_{now.date().isoformat()}"
                    if not Notification.objects.filter(recipient=admin.user, meta__tag=notif_tag).exists():
                        Notification.objects.create(
                            recipient=admin.user,
                            title="VIP Trial Ended — 3-Day Grace Period Active",
                            message=f"Your 7-day VIP allocation has ended. You have {days_left} day(s) remaining in your grace period. Settle your plan to avoid workspace quarantine.",
                            entity_type="billing",
                            meta={'tag': notif_tag, 'days_remaining': days_left}
                        )

                        if admin.user.email:
                            email_html = render_luxury_email_html(
                                title="3-Day Settlement Grace Period Active",
                                subtitle=f"{org.name} &middot; VIP Allocation Expiring",
                                recipient_name=admin.user.first_name or admin.user.username,
                                message_paragraphs=[
                                    f"Your 7-day VIP All-Access allocation on <strong>THE FINISHER LUXURY</strong> has ended.",
                                    f"Your private workspace has entered a <strong>3-Day Settlement Grace Period ({days_left} day(s) remaining)</strong>.",
                                    "Your database records, deals, contacts, and employee permissions remain cryptographically preserved. Settle your monthly allocation now to maintain continuous uninterrupted service."
                                ],
                                cta_text="Secure Workspace Allocation",
                                cta_url="https://www.thefinishercrm.tech/#/upgrade",
                                security_note="Mtambo Holdings Financial Directorate (mtamboholdings@outlook.com). In compliance with POPIA Section 19, zero data will be destroyed."
                            )
                            send_email_async(
                                subject=f"Action Required: 3-Day Grace Period Active for {org.name}",
                                text_body=f"Your 7-day trial has ended. You have {days_left} days left in your settlement grace period. Please upgrade to maintain uninterrupted service: https://www.thefinishercrm.tech/#/upgrade",
                                recipient_list=[admin.user.email],
                                html_body=email_html
                            )
                        grace_notified_count += 1

            # Check if Grace Period Expired (Day 11+) and not paid
            elif org.is_grace_expired:
                # Lock access but NEVER delete data (data preservation)
                admins = UserProfile.objects.filter(organization=org, role='admin').select_related('user')
                notif_tag = f"locked_{now.date().isoformat()}"
                
                for admin in admins:
                    if not admin.user:
                        continue
                    if not Notification.objects.filter(recipient=admin.user, meta__tag=notif_tag).exists():
                        Notification.objects.create(
                            recipient=admin.user,
                            title="Workspace Quarantined — Payment Required",
                            message="Your 7-day trial and 3-day grace period have concluded. Settle your monthly allocation to restore immediate access.",
                            entity_type="billing",
                            meta={'tag': notif_tag}
                        )
                        if admin.user.email:
                            email_html = render_luxury_email_html(
                                title="Workspace Snapshot Quarantined",
                                subtitle=f"{org.name} &middot; Secure Storage Vault",
                                recipient_name=admin.user.first_name or admin.user.username,
                                message_paragraphs=[
                                    "Your 7-day VIP trial and 3-day settlement grace period have elapsed without payment confirmation.",
                                    "In accordance with our enterprise retention policy, your workspace has been placed into <strong>Secure Quarantine</strong>.",
                                    "All client records, pipeline deals, contacts, and configuration data are 100% safely preserved in our encrypted vault. Settle your monthly allocation to instantly restore access."
                                ],
                                cta_text="Reactivate Workspace Now",
                                cta_url="https://www.thefinishercrm.tech/#/upgrade",
                                security_note="Mtambo Holdings Data Protection Vault (mtamboholdings@outlook.com). Your records are secured under POPIA Section 19."
                            )
                            send_email_async(
                                subject=f"Workspace Quarantined — Settle to Restore {org.name}",
                                text_body=f"Your workspace for {org.name} has been placed into secure quarantine. Settle your allocation to restore instant access: https://www.thefinishercrm.tech/#/upgrade",
                                recipient_list=[admin.user.email],
                                html_body=email_html
                            )

                record_audit_event(
                    'TRIAL_LIFECYCLE_QUARANTINE',
                    f"Organization '{org.name}' transitioned to quarantined status following expiration of 7-day trial + 3-day grace period. Data preserved.",
                    user=None,
                    organization=org,
                    severity='WARNING'
                )
                locked_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully completed trial lifecycle run: {grace_notified_count} grace notices sent, {locked_count} quarantined."
        ))
