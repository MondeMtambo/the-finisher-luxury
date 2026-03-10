#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
sys.path.insert(0, 'backend')

django.setup()

from crm.models import User, UserProfile

# Find Adrian
users = User.objects.filter(email__icontains='adrian')
print(f"Found {users.count()} users with 'adrian' in email")

for u in users:
    print(f"\nUser: {u.username}")
    print(f"  Email: {u.email}")
    print(f"  is_superuser: {u.is_superuser}")
    print(f"  is_staff: {u.is_staff}")
    
    try:
        profile = u.profile
        print(f"  Company: {profile.company_name}")
        print(f"  Role: {profile.role}")
        print(f"  is_admin: {profile.is_admin}")
        print(f"  can_add_employees: {profile.can_add_employees}")
    except Exception as e:
        print(f"  Error: {e}")

# Check all profiles with company_name = 'Discovery'
print("\n\n--- Checking all users in company 'Discovery' ---")
profiles = UserProfile.objects.filter(company_name='Discovery')
print(f"Found {profiles.count()} profiles")
for p in profiles:
    print(f"  User: {p.user.username} ({p.user.email}) - Role: {p.role}")
