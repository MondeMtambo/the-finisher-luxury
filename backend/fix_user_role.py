#!/usr/bin/env python
"""
Fix user role to make them a client admin
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth.models import User
from crm.models import UserProfile

def fix_user_roles():
    """Make all non-superuser users into client admins"""
    # Get all regular users (not superusers/staff)
    regular_users = User.objects.filter(is_superuser=False, is_staff=False)
    
    print(f"Found {regular_users.count()} regular users")
    
    for user in regular_users:
        if hasattr(user, 'profile'):
            old_role = user.profile.role
            user.profile.role = 'admin'
            user.profile.save()
            print(f"✅ Updated {user.username}: {old_role} -> admin")
        else:
            print(f"⚠️ {user.username} has no profile")
    
    print("\n✅ All regular users are now client admins!")
    print("They can now add employees to their company.")

if __name__ == '__main__':
    fix_user_roles()
