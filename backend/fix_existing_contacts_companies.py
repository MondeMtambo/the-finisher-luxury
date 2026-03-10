"""
Script to auto-create companies for ALL existing contacts that don't have them.
Run this ONCE to fix the issue with existing contacts.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from crm.models import Contact, Company
from crm.views import ensure_company_for_contact

def fix_all_contacts():
    print("=" * 70)
    print("FIXING ALL EXISTING CONTACTS - AUTO-CREATING COMPANIES")
    print("=" * 70)
    
    # Get all contacts that have company_name_manual but no linked company
    contacts_without_companies = Contact.objects.filter(
        company_name_manual__isnull=False
    ).exclude(
        company_name_manual=''
    )
    
    total_contacts = contacts_without_companies.count()
    print(f"\n📊 Found {total_contacts} contacts with company names")
    
    if total_contacts == 0:
        print("✓ No contacts need fixing. All contacts are properly linked!")
        return
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for contact in contacts_without_companies:
        try:
            print(f"\n--- Processing Contact: {contact.first_name} {contact.last_name} ---")
            print(f"  Email: {contact.email}")
            print(f"  Company Name Manual: {contact.company_name_manual}")
            print(f"  Currently Linked Company: {contact.company.name if contact.company else 'None'}")
            
            # Run the auto-creation function
            ensure_company_for_contact(contact)
            
            # Refresh to see the result
            contact.refresh_from_db()
            
            if contact.company:
                print(f"  ✓ SUCCESS: Company '{contact.company.name}' (ID: {contact.company.id})")
                fixed_count += 1
            else:
                print(f"  ⚠️ SKIPPED: No company could be created")
                skipped_count += 1
                
        except Exception as e:
            print(f"  ✗ ERROR: {str(e)}")
            error_count += 1
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Successfully fixed: {fixed_count} contacts")
    print(f"⚠️ Skipped: {skipped_count} contacts")
    print(f"✗ Errors: {error_count} contacts")
    print(f"📊 Total processed: {total_contacts} contacts")
    
    # Show all companies now in database
    print("\n" + "=" * 70)
    print("ALL COMPANIES IN DATABASE (by user)")
    print("=" * 70)
    
    from django.contrib.auth.models import User
    for user in User.objects.all():
        companies = Company.objects.filter(user=user)
        if companies.exists():
            print(f"\n👤 User: {user.username}")
            print(f"   Companies: {companies.count()}")
            for company in companies:
                contacts_count = Contact.objects.filter(company=company).count()
                print(f"   • {company.name} (ID: {company.id}) - {contacts_count} contacts")
    
    print("\n" + "=" * 70)
    print("SCRIPT COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    fix_all_contacts()
