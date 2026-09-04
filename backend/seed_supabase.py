#!/usr/bin/env python
"""
THE FINISHER LUXURY - System Initializer & Database Decoupler
Decouples adminluxury from any company/organization (sets to NULL)
and scrubs any duplicate Mtambo Holdings entries so the CEO can register cleanly.
"""
import os
import sys

def main():
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
        django.setup()

        from django.contrib.auth.models import User
        from crm.models import UserProfile, Organization, CorporateAccessRequest, Company, TenantVerification, WebsiteLead
        from django.db.models import Q

        print("[seed_supabase] Decoupling adminluxury from company/organization...")

        # 1. Update adminluxury user: set company and organization to NULL
        admin_user = User.objects.filter(username__iexact='adminluxury').first()
        if admin_user:
            if not admin_user.email or 'mtambo' in admin_user.email.lower():
                admin_user.email = 'adminluxury@thefinishercrm.tech'
                admin_user.save(update_fields=['email'])
                print(f"[seed_supabase] Updated adminluxury email to: {admin_user.email}")

            if hasattr(admin_user, 'profile'):
                p = admin_user.profile
                p.organization = None
                p.company_name = ''
                p.save(update_fields=['organization', 'company_name'])
                print("[seed_supabase] adminluxury organization and company_name set to NULL.")

        # 2. Scrub any existing Mtambo Holdings data so CEO can register cleanly
        mtambo_emails = [
            'sales@mtamboholdings.dev',
            'monde@mtamboholdings.dev',
            'mtambo@mtamboholdings.dev'
        ]
        
        deleted_users, _ = User.objects.filter(
            Q(email__in=mtambo_emails) | Q(username__in=mtambo_emails)
        ).exclude(username__iexact='adminluxury').delete()
        if deleted_users:
            print(f"[seed_supabase] Deleted {deleted_users} existing user records for Mtambo Holdings.")

        deleted_reqs, _ = CorporateAccessRequest.objects.filter(
            Q(email__in=mtambo_emails) | 
            Q(company_name__icontains='mtambo') |
            Q(cipc_number='2026/614054/07') |
            Q(tax_number='9089227301')
        ).delete()
        if deleted_reqs:
            print(f"[seed_supabase] Deleted {deleted_reqs} CorporateAccessRequests for Mtambo Holdings.")

        mtambo_orgs = Organization.objects.filter(name__icontains='mtambo')
        for org in mtambo_orgs:
            UserProfile.objects.filter(organization=org).update(organization=None)
            org.delete()
            print("[seed_supabase] Deleted existing Mtambo Holdings Organization.")

        Company.objects.filter(name__icontains='mtambo').delete()
        TenantVerification.objects.filter(
            Q(company_name__icontains='mtambo') | Q(cipc_number='2026/614054/07')
        ).delete()
        WebsiteLead.objects.filter(
            Q(email__in=mtambo_emails) | Q(inbound_message__icontains='mtambo')
        ).delete()

        print("[seed_supabase] Database cleaned successfully. Ready for fresh registration.")
        return 0
    except Exception as e:
        print(f"[seed_supabase] Notice: {e}")
        return 0

if __name__ == '__main__':
    sys.exit(main())
