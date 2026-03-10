"""
Create adminluxury superuser for THE FINISHER LUXURY
Run this script to create the main admin account
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth.models import User
from crm.models import UserProfile

def create_luxury_admin():
    username = 'adminluxury'
    email = 'admin@thefinisher.co.za'
    password = 'Admin@2026!'
    
    print("=" * 60)
    print("  THE FINISHER LUXURY - Admin Account Creator")
    print("=" * 60)
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"\n❌ User '{username}' already exists!")
        user = User.objects.get(username=username)
        print(f"\n📋 Existing user details:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   is_staff: {user.is_staff}")
        if hasattr(user, 'profile'):
            print(f"   Role: {user.profile.role}")
            print(f"   Tier: {user.profile.tier}")
            print(f"   Company: {user.profile.company_name}")
        
        # Update password anyway
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"\n✅ Password and permissions updated for '{username}'!")
        
    else:
        # Create new superuser
        print(f"\n🔨 Creating superuser: {username}")
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='Luxury'
        )
        print(f"✅ Superuser '{username}' created successfully!")
    
    # Ensure profile exists and set role to admin
    if hasattr(user, 'profile'):
        profile = user.profile
        profile.role = 'admin'
        profile.tier = 'luxury'
        profile.company_name = 'THE FINISHER LUXURY'
        profile.phone = '+27123456789'
        profile.payment_status = 'paid'
        profile.save()
        print(f"✅ Profile updated with admin role and luxury tier")
    
    print(f"\n📋 Login Credentials:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Role: admin")
    print(f"   Tier: luxury")
    print(f"\n🌐 Login at: https://the-finisher-luxury.onrender.com/#/login")
    print("=" * 60)

if __name__ == '__main__':
    create_luxury_admin()
