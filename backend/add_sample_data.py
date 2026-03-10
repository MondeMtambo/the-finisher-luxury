import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from crm.models import Company, Contact, Deal

# Create sample companies
company1 = Company.objects.create(
    name="Acme Corp",
    email="info@acme.com",
    phone="+27 11 123 4567",
    address="123 Business St, Johannesburg"
)

company2 = Company.objects.create(
    name="Tech Solutions SA",
    email="hello@techsolutions.co.za",
    phone="+27 21 987 6543",
    address="456 Innovation Ave, Cape Town"
)

# Create sample contacts
contact1 = Contact.objects.create(
    first_name="John",
    last_name="Smith",
    email="john@acme.com",
    phone="+27 82 123 4567",
    company=company1
)

contact2 = Contact.objects.create(
    first_name="Sarah",
    last_name="Johnson",
    email="sarah@techsolutions.co.za",
    phone="+27 83 987 6543",
    company=company2
)

# Create sample deals
Deal.objects.create(
    title="Website Redesign Project",
    contact=contact1,
    value=25000.00,
    stage="qualified"
)

Deal.objects.create(
    title="CRM Implementation",
    contact=contact2,
    value=50000.00,
    stage="proposal"
)

print("✅ Sample data created successfully!")
print("- 2 Companies")
print("- 2 Contacts") 
print("- 2 Deals")