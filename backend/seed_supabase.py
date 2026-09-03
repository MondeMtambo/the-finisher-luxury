#!/usr/bin/env python
"""
THE FINISHER LUXURY - Supabase Database Initializer & Migration Runner
Provisions all database tables, creates Mtambo Holdings Group organization,
and sets up the master executive login account.
"""
import os
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')

import django
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from crm.models import Organization, UserProfile, SubscriptionPlan, OrganizationSubscription


def initialize_supabase(admin_password=""):
    print("=" * 60)
    print("THE FINISHER LUXURY - SUPABASE DATABASE INITIALIZER")
    print("Mtambo Holdings Group")
    print("=" * 60)

    # 1. Run Migrations
    print("\n[1/3] Running database migrations on Supabase...")
    try:
        call_command('migrate', interactive=False)
        print("✓ All tables created successfully (Auth, Organization, Billing, CRM entities).")
    except Exception as e:
        print(f"✗ Migration error: {e}")
        return False

    # 2. Provision Mtambo Holdings Group Organization
    print("\n[2/3] Provisioning Mtambo Holdings Group Organization...")
    org, org_created = Organization.objects.get_or_create(
        name="Mtambo Holdings Group",
        defaults={
            'slug': 'mtambo-holdings-group',
            'subscription_tier': 'luxury',
            'trial_start_date': timezone.now(),
            'trial_end_date': timezone.now() + timedelta(days=365),
            'is_active': True,
            'max_users': 50,
        }
    )
    if org_created:
        print(f"✓ Created Organization: {org.name} (UUID: {org.id})")
    else:
        print(f"✓ Organization already exists: {org.name} (UUID: {org.id})")

    # Ensure Subscription Plan exists
    plan, _ = SubscriptionPlan.objects.get_or_create(
        tier='luxury',
        defaults={
            'name': 'The Finisher Luxury Private OS',
            'price_cents': 1250000,
            'currency': 'ZAR',
            'billing_period': 'annual',
            'is_active': True,
        }
    )
    OrganizationSubscription.objects.get_or_create(
        organization=org,
        defaults={
            'plan': plan,
            'status': 'active',
            'current_period_start': timezone.now(),
            'current_period_end': timezone.now() + timedelta(days=365),
        }
    )

    # 3. Create or Update Master Admin Account (Monde Mtambo)
    print("\n[3/3] Setting up Master Executive Account...")
    explicit_password = admin_password or os.environ.get('DEFAULT_ADMIN_PASSWORD')
    admin_user = User.objects.filter(username='adminluxury').first()
    if not admin_user:
        import secrets
        initial_password = explicit_password or secrets.token_urlsafe(16)
        admin_user = User.objects.create_user(
            username='adminluxury',
            email='MondeM@mtamboholdings.dev',
            password=initial_password,
            first_name='Monde',
            last_name='Mtambo',
            is_staff=True,
            is_superuser=True,
        )
        print(f"✓ Created master user: {admin_user.username} ({admin_user.email})")
    else:
        admin_user.first_name = 'Monde'
        admin_user.last_name = 'Mtambo'
        admin_user.email = 'MondeM@mtamboholdings.dev'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        if explicit_password:
            admin_user.set_password(explicit_password)
            print(f"✓ Updated master password from explicit configuration")
        admin_user.save()
        print(f"✓ Master user ready: {admin_user.username} ({admin_user.first_name} {admin_user.last_name})")

    # Link Profile to Organization
    profile, _ = UserProfile.objects.get_or_create(user=admin_user)
    profile.organization = org
    profile.role = 'admin'
    profile.company_name = org.name
    profile.save()
    print(f"✓ Linked profile to organization: {org.name} with role: admin")

    print("\n" + "=" * 60)
    print("SUPABASE PROVISIONING COMPLETE! 🚀")
    print("=" * 60)
    print(f"Executive Name : Monde Mtambo")
    print(f"Username       : adminluxury")
    print(f"Email          : monde@mtamboholdings.com")
    print(f"Organization   : Mtambo Holdings Group")
    print(f"Tier           : Luxury Private OS (Active)")
    print("=" * 60)
    return True


if __name__ == '__main__':
    pwd = sys.argv[1] if len(sys.argv) > 1 else ""
    initialize_supabase(pwd)
