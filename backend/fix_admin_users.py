#!/usr/bin/env python
"""Fix admin users: delete duplicate admin, set adminluxury role to admin"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth.models import User
from crm.models import UserProfile

def fix_admin_users():
    # 1. Delete the duplicate "admin" user
    try:
        admin_user = User.objects.get(username='admin', email='admin@example.com')
        print(f"Deleting duplicate admin user: {admin_user.username} ({admin_user.email})")
        admin_user.delete()
        print("✓ Deleted duplicate admin user")
    except User.DoesNotExist:
        print("Admin user already deleted or doesn't exist")
    
    # 2. Update adminluxury UserProfile role to 'admin'
    try:
        adminluxury_user = User.objects.get(username='adminluxury')
        profile, created = UserProfile.objects.get_or_create(user=adminluxury_user)
        
        if profile.role != 'admin':
            old_role = profile.role
            profile.role = 'admin'
            profile.save()
            print(f"✓ Updated adminluxury role from '{old_role}' to 'admin'")
        else:
            print("adminluxury already has admin role")
        
        print(f"\nFinal adminluxury status:")
        print(f"  Username: {adminluxury_user.username}")
        print(f"  Email: {adminluxury_user.email}")
        print(f"  is_superuser: {adminluxury_user.is_superuser}")
        print(f"  is_staff: {adminluxury_user.is_staff}")
        print(f"  Profile role: {profile.role}")
        
    except User.DoesNotExist:
        print("ERROR: adminluxury user not found!")

if __name__ == '__main__':
    fix_admin_users()
