#!/usr/bin/env python
"""
Create a test client admin account
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

def create_client_admin():
    """Create a test client admin (CRM buyer)"""
    
    # Check if user already exists
    if User.objects.filter(username='testclient').exists():
        print("❌ User 'testclient' already exists. Updating their role...")
        user = User.objects.get(username='testclient')
    else:
        # Create new user
        user = User.objects.create_user(
            username='testclient',
            email='client@test.com',
            password='Test1234!',
            first_name='Test',
            last_name='Client'
        )
        print("✅ Created user 'testclient'")
    
    # Update profile
    if hasattr(user, 'profile'):
        user.profile.role = 'admin'  # CLIENT ADMIN
        user.profile.company_name = 'Test Company'
        user.profile.tier = 'luxury'
        user.profile.phone = '0123456789'
        user.profile.payment_status = 'paid'
        user.profile.save()
        
        print(f"✅ Profile updated:")
        print(f"   Role: {user.profile.role} (CLIENT ADMIN)")
        print(f"   Company: {user.profile.company_name}")
        print(f"   Tier: {user.profile.tier}")
        print(f"   Payment: {user.profile.payment_status}")
        print(f"\n🔐 Login credentials:")
        print(f"   Username: testclient")
        print(f"   Password: Test1234!")
        print(f"\n✅ This user can now add 1 employee!")
    else:
        print("⚠️ No profile found for user")

if __name__ == '__main__':
    create_client_admin()
