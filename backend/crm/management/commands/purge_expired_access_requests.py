from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from crm.models import CorporateAccessRequest


class Command(BaseCommand):
    help = 'Purge unverified corporate access requests older than 5 minutes (Ephemeral Retention Policy)'

    def handle(self, *args, **options):
        now = timezone.now()
        cutoff = now - timezone.timedelta(minutes=5)
        
        expired_qs = CorporateAccessRequest.objects.filter(
            is_verified=False
        ).filter(
            Q(expires_at__lte=now) | Q(created_at__lte=cutoff)
        )
        count = expired_qs.count()
        purged_count, _ = expired_qs.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully purged {purged_count} unverified access requests older than 5 minutes."
            )
        )
