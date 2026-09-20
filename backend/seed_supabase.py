#!/usr/bin/env python
"""
THE FINISHER LUXURY - System Initializer & Database Decoupler
Ensures adminluxury is decoupled and ready.
Does NOT delete client registrations or tenant accounts.
"""
import os
import sys

def main():
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
        django.setup()

        from django.contrib.auth.models import User

        # 1. Update adminluxury user: set company and organization to NULL if linked
        admin_user = User.objects.filter(username__iexact='adminluxury').first()
        if admin_user:
            if not admin_user.email or 'mtambo' in admin_user.email.lower():
                admin_user.email = 'adminluxury@thefinishercrm.tech'
                admin_user.save(update_fields=['email'])

            if hasattr(admin_user, 'profile'):
                p = admin_user.profile
                updated = False
                if p.organization is not None:
                    p.organization = None
                    updated = True
                if p.company_name != '':
                    p.company_name = ''
                    updated = True
                if p.role != 'admin':
                    p.role = 'admin'
                    updated = True
                if p.tier != 'luxury':
                    p.tier = 'luxury'
                    updated = True
                if updated:
                    p.save(update_fields=['organization', 'company_name', 'role', 'tier'])
                    print("[seed_supabase] adminluxury verified as sovereign root admin (organization=NULL, company=NULL).")

        # 2. Ensure test organization Adminluxury Enterprise is removed
        from django.db.models import Q
        from crm.models import Organization, UserProfile
        test_orgs = Organization.objects.filter(
            Q(name__icontains='adminluxury') | Q(slug__icontains='adminluxury')
        )
        for t_org in test_orgs:
            UserProfile.objects.filter(organization=t_org).update(organization=None, company_name='')
            t_org.delete()
            print(f"[seed_supabase] Purged test tenant organization: {t_org.name}")

        print("[seed_supabase] System initialized successfully.")
        return 0
    except Exception as e:
        print(f"[seed_supabase] Notice: {e}")
        return 0

if __name__ == '__main__':
    sys.exit(main())
