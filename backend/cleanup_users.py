#!/usr/bin/env python
"""
Database cleanup script: Remove all users except superuser
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth.models import User
from crm.models import UserProfile, Division, OnboardingLog

# Show current state
print("=" * 80)
print("CURRENT DATABASE STATE")
print("=" * 80)

all_users = User.objects.all()
print(f"\nTotal users: {all_users.count()}")
for u in all_users:
    p = u.profile if hasattr(u, 'profile') else None
    print(f"  {u.id:3d} | {u.username:30s} | role={p.role if p else 'N/A':12s} | superuser={u.is_superuser}")

print(f"\nTotal divisions: {Division.objects.count()}")
for d in Division.objects.all()[:5]:
    print(f"  {d.id} | {d.name} | company={d.company_name}")

print(f"\nTotal onboarding logs: {OnboardingLog.objects.count()}")

# Find superuser
superuser = User.objects.filter(is_superuser=True).first()
print(f"\n" + "=" * 80)
print(f"SUPERUSER: {superuser.username if superuser else 'NOT FOUND'} (id={superuser.id if superuser else 'N/A'})")
print("=" * 80)

# Get all non-superuser accounts
non_admin_users = User.objects.filter(is_superuser=False, is_staff=False)
print(f"\n\nUsers to delete: {non_admin_users.count()}")
for u in non_admin_users:
    print(f"  Deleting: {u.username}")

# Confirm deletion
response = input("\n\nDELETE ALL NON-ADMIN USERS? Type 'YES' to confirm: ").strip().upper()
if response == 'YES':
    count = non_admin_users.count()
    non_admin_users.delete()
    print(f"\n✓ Deleted {count} users")
    
    # Delete orphaned onboarding logs
    orphaned_logs = OnboardingLog.objects.filter(employee__isnull=True)
    log_count = orphaned_logs.count()
    if log_count > 0:
        orphaned_logs.delete()
        print(f"✓ Deleted {log_count} orphaned onboarding logs")
    
    # Verify final state
    print("\n" + "=" * 80)
    print("FINAL DATABASE STATE")
    print("=" * 80)
    remaining = User.objects.all()
    print(f"\nRemaining users: {remaining.count()}")
    for u in remaining:
        p = u.profile if hasattr(u, 'profile') else None
        print(f"  {u.id:3d} | {u.username:30s} | role={p.role if p else 'N/A':12s} | superuser={u.is_superuser}")
    
    print(f"\nDivisions (preserved): {Division.objects.count()}")
    print("\n✓ Database ready for fresh onboarding!")
else:
    print("\n✗ Deletion cancelled")
