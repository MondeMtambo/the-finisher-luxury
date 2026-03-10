"""
Test script to verify company auto-creation from contacts.
Run this to verify the ensure_company_for_contact function works correctly.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth.models import User
from crm.models import Contact, Company
from crm.views import ensure_company_for_contact

def test_company_auto_creation():
    print("=" * 60)
    print("Testing Company Auto-Creation from Contact")
    print("=" * 60)
    
    # Get or create a test user
    test_user, created = User.objects.get_or_create(
        username='test_company_user',
        defaults={'email': 'test@example.com'}
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✓ Created test user: {test_user.username}")
    else:
        print(f"✓ Using existing test user: {test_user.username}")
    
    # Test Case 1: Corporate contact with manual company name
    print("\n--- Test Case 1: Corporate Contact ---")
    contact1 = Contact.objects.create(
        user=test_user,
        first_name="John",
        last_name="Doe",
        email="john.doe@testcorp.com",
        phone="+27123456789",
        is_self_employed=False,
        company_direct_line="+27987654321",
        company_name_manual="Test Corporation"
    )
    print(f"✓ Created contact: {contact1.first_name} {contact1.last_name}")
    print(f"  Email: {contact1.email}")
    print(f"  Company Name Manual: {contact1.company_name_manual}")
    
    # Run the auto-creation function
    ensure_company_for_contact(contact1)
    contact1.refresh_from_db()
    
    if contact1.company:
        print(f"✓ Company auto-created: {contact1.company.name}")
        print(f"  Company ID: {contact1.company.id}")
        print(f"  Company Phone: {contact1.company.phone}")
        print(f"  Company Email: {contact1.company.email}")
    else:
        print("✗ FAILED: No company linked to contact!")
    
    # Test Case 2: Self-employed contact
    print("\n--- Test Case 2: Self-Employed Contact ---")
    contact2 = Contact.objects.create(
        user=test_user,
        first_name="Jane",
        last_name="Smith",
        email="jane@gmail.com",
        phone="+27111222333",
        is_self_employed=True,
        company_name_manual="Jane Smith (Self-Employed)"
    )
    print(f"✓ Created contact: {contact2.first_name} {contact2.last_name}")
    print(f"  Email: {contact2.email}")
    print(f"  Company Name Manual: {contact2.company_name_manual}")
    
    ensure_company_for_contact(contact2)
    contact2.refresh_from_db()
    
    if contact2.company:
        print(f"✓ Company auto-created: {contact2.company.name}")
        print(f"  Company ID: {contact2.company.id}")
    else:
        print("✗ FAILED: No company linked to contact!")
    
    # Verify companies in database
    print("\n--- Companies in Database ---")
    companies = Company.objects.filter(user=test_user)
    print(f"Total companies for test user: {companies.count()}")
    for company in companies:
        print(f"  • {company.name} (ID: {company.id})")
    
    # Cleanup
    print("\n--- Cleanup ---")
    Contact.objects.filter(user=test_user).delete()
    Company.objects.filter(user=test_user).delete()
    if created:
        test_user.delete()
        print("✓ Cleaned up test data")
    else:
        print("✓ Kept existing test user, removed test contacts/companies")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_company_auto_creation()
