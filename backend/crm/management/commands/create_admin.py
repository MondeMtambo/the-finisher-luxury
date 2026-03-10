from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crm.models import UserProfile


class Command(BaseCommand):
    help = 'Create or repair the default admin user for THE FINISHER LUXURY'

    def handle(self, *args, **options):
        username = 'adminluxury'
        email = 'admin@thefinisher.co.za'
        password = 'Admin@2026!'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Admin',
                'last_name': 'Luxury',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully created admin user: {username}'))
        else:
            changed = False

            if user.email != email:
                user.email = email
                changed = True
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if not user.is_active:
                user.is_active = True
                changed = True

            user.set_password(password)
            changed = True

            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Admin user "{username}" updated with superuser access.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✅ Admin user "{username}" already configured.'))

        # Ensure UserProfile is properly configured
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.role = 'admin'
            profile.tier = 'luxury'
            profile.company_name = 'THE FINISHER LUXURY'
            profile.phone = '+27123456789'
            profile.payment_status = 'paid'
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Profile configured: role=admin, tier=luxury'))
        
        self.stdout.write(self.style.SUCCESS(f'\n📋 Login credentials:'))
        self.stdout.write(self.style.SUCCESS(f'   Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'   Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'   Email: {email}'))
