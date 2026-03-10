#!/usr/bin/env python
"""
Check all users in the system
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

def check_users():
    """Check all users and their roles"""
    all_users = User.objects.all()
    
    print(f"Total users in system: {all_users.count()}\n")
    
    for user in all_users:
        print(f"Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Superuser: {user.is_superuser}")
        print(f"  Staff: {user.is_staff}")
        
        if hasattr(user, 'profile'):
            print(f"  Role: {user.profile.role}")
            print(f"  Company: {user.profile.company_name or 'N/A'}")
            print(f"  Tier: {user.profile.tier}")
        else:
            print(f"  ⚠️ NO PROFILE")
        print()

if __name__ == '__main__':
    check_users()
