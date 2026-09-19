"""
THE FINISHER LUXURY - Fix Trial Accounts Management Command
Bulk-patches all legacy 'trial' records to 'basic' (Corporate Sovereign) / 'active'.
Run this ONCE after deploying the trial-elimination update.

Usage:
    python manage.py fix_trial_accounts
    python manage.py fix_trial_accounts --dry-run
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Migrate all legacy trial accounts to Corporate Sovereign (basic) with active status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without writing to database',
        )

    def handle(self, *args, **options):
        from crm.models import Organization, OrganizationSubscription, UserProfile

        dry_run = options['dry_run']
        now = timezone.now()
        far_future = now + timedelta(days=3650)  # 10 years

        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('THE FINISHER LUXURY - Trial Account Migration'))
        self.stdout.write(self.style.NOTICE('=' * 60))
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be saved'))
        self.stdout.write('')

        # ─── 1. Fix Organizations with trial tier ───
        trial_orgs = Organization.objects.filter(subscription_tier='trial')
        count_orgs = trial_orgs.count()
        self.stdout.write(f'Organizations with trial tier: {count_orgs}')

        if not dry_run and count_orgs > 0:
            trial_orgs.update(
                subscription_tier='basic',
                trial_end_date=far_future,
                is_active=True,
                can_export_csv=True,
            )
            self.stdout.write(self.style.SUCCESS(f'  [OK] Updated {count_orgs} organizations -> basic (Corporate Sovereign)'))

        # ─── 2. Fix Organizations with expired trial_end_date ───
        expired_orgs = Organization.objects.filter(
            trial_end_date__lt=now,
            subscription_tier='basic',
        )
        count_expired = expired_orgs.count()
        self.stdout.write(f'Organizations with expired trial dates: {count_expired}')

        if not dry_run and count_expired > 0:
            expired_orgs.update(
                trial_end_date=far_future,
                is_active=True,
                can_export_csv=True,
            )
            self.stdout.write(self.style.SUCCESS(f'  [OK] Extended {count_expired} expired organizations -> 10-year validity'))

        # ─── 3. Fix ALL organizations - ensure none are locked ───
        all_inactive = Organization.objects.filter(is_active=False)
        count_inactive = all_inactive.count()
        self.stdout.write(f'Inactive organizations: {count_inactive}')

        if not dry_run and count_inactive > 0:
            all_inactive.update(is_active=True)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Activated {count_inactive} inactive organizations'))

        # ─── 4. Fix OrganizationSubscriptions with trial status ───
        trial_subs = OrganizationSubscription.objects.filter(status='trial')
        count_subs = trial_subs.count()
        self.stdout.write(f'Subscriptions with trial status: {count_subs}')

        if not dry_run and count_subs > 0:
            trial_subs.update(status='active')
            self.stdout.write(self.style.SUCCESS(f'  [OK] Updated {count_subs} subscriptions -> active'))

        # ─── 5. Fix UserProfiles with trial payment_status ───
        trial_profiles = UserProfile.objects.filter(payment_status='trial')
        count_profiles = trial_profiles.count()
        self.stdout.write(f'User profiles with trial payment status: {count_profiles}')

        if not dry_run and count_profiles > 0:
            trial_profiles.update(payment_status='paid')
            self.stdout.write(self.style.SUCCESS(f'  [OK] Updated {count_profiles} user profiles -> paid'))

        # ─── 6. Fix UserProfiles with pending payment_status ───
        pending_profiles = UserProfile.objects.filter(payment_status='pending')
        count_pending = pending_profiles.count()
        self.stdout.write(f'User profiles with pending payment status: {count_pending}')

        if not dry_run and count_pending > 0:
            pending_profiles.update(payment_status='paid')
            self.stdout.write(self.style.SUCCESS(f'  [OK] Updated {count_pending} pending user profiles -> paid'))

        # ─── 7. Unban all users that were banned for trial expiry ───
        banned_trial = UserProfile.objects.filter(
            is_banned=True,
            ban_reason__icontains='trial'
        )
        count_banned = banned_trial.count()
        self.stdout.write(f'Users banned for trial reasons: {count_banned}')

        if not dry_run and count_banned > 0:
            for profile in banned_trial:
                profile.is_banned = False
                profile.ban_reason = ''
                profile.banned_at = None
                profile.user.is_active = True
                profile.save()
                profile.user.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Unbanned {count_banned} users with trial-related bans'))

        # ─── 8. Also unban any user with unpaid subscription bans ───
        banned_sub = UserProfile.objects.filter(
            is_banned=True,
            ban_reason__icontains='subscription'
        )
        count_sub_banned = banned_sub.count()
        self.stdout.write(f'Users banned for unpaid subscription: {count_sub_banned}')

        if not dry_run and count_sub_banned > 0:
            for profile in banned_sub:
                profile.is_banned = False
                profile.ban_reason = ''
                profile.banned_at = None
                profile.user.is_active = True
                profile.save()
                profile.user.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Unbanned {count_sub_banned} subscription-banned users'))

        # ─── Summary ───
        self.stdout.write('\n' + '=' * 60)
        total_fixed = count_orgs + count_expired + count_inactive + count_subs + count_profiles + count_pending + count_banned + count_sub_banned
        if dry_run:
            self.stdout.write(self.style.WARNING(f'DRY RUN: {total_fixed} records would be updated'))
        else:
            self.stdout.write(self.style.SUCCESS(f'SUCCESS: {total_fixed} records patched. All accounts are now ACTIVE and UNLOCKED.'))
        self.stdout.write('=' * 60 + '\n')
