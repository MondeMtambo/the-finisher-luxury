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
                if p.organization is not None or p.company_name:
                    p.organization = None
                    p.company_name = ''
                    p.save(update_fields=['organization', 'company_name'])
                    print("[seed_supabase] adminluxury organization and company_name set to NULL.")

        print("[seed_supabase] System initialized successfully.")
        return 0
    except Exception as e:
        print(f"[seed_supabase] Notice: {e}")
        return 0

if __name__ == '__main__':
    sys.exit(main())
