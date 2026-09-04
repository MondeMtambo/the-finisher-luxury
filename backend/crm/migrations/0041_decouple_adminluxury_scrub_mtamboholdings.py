# Generated data migration to decouple adminluxury and scrub Mtambo Holdings from database

from django.db import migrations
from django.db.models import Q


def decouple_adminluxury_and_scrub_mtambo(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('crm', 'UserProfile')
    Organization = apps.get_model('crm', 'Organization')
    CorporateAccessRequest = apps.get_model('crm', 'CorporateAccessRequest')
    Company = apps.get_model('crm', 'Company')
    TenantVerification = apps.get_model('crm', 'TenantVerification')
    WebsiteLead = apps.get_model('crm', 'WebsiteLead')

    # 1. Decouple adminluxury: set organization and company_name to NULL
    admin_user = User.objects.filter(username__iexact='adminluxury').first()
    if admin_user:
        if not admin_user.email or 'mtambo' in admin_user.email.lower():
            admin_user.email = 'adminluxury@thefinishercrm.tech'
            admin_user.save(update_fields=['email'])

        admin_profile = UserProfile.objects.filter(user=admin_user).first()
        if admin_profile:
            admin_profile.organization = None
            admin_profile.company_name = ''
            admin_profile.save(update_fields=['organization', 'company_name'])

    # 2. Scrub any non-adminluxury users using Mtambo Holdings emails or usernames
    mtambo_emails = [
        'sales@mtamboholdings.dev',
        'monde@mtamboholdings.dev',
        'mtambo@mtamboholdings.dev',
    ]
    User.objects.filter(
        Q(email__in=mtambo_emails) | Q(username__in=mtambo_emails)
    ).exclude(username__iexact='adminluxury').delete()

    # 3. Scrub any CorporateAccessRequest records for Mtambo Holdings
    CorporateAccessRequest.objects.filter(
        Q(email__in=mtambo_emails) | 
        Q(company_name__icontains='mtambo') | 
        Q(cipc_number='2026/614054/07') |
        Q(tax_number='9089227301')
    ).delete()

    # 4. Unlink and remove any Organization named Mtambo Holdings
    mtambo_orgs = Organization.objects.filter(name__icontains='mtambo')
    for org in mtambo_orgs:
        UserProfile.objects.filter(organization=org).update(organization=None)
        org.delete()

    # 5. Scrub Company, TenantVerification, and WebsiteLeads
    Company.objects.filter(name__icontains='mtambo').delete()
    TenantVerification.objects.filter(
        Q(company_name__icontains='mtambo') | Q(cipc_number='2026/614054/07')
    ).delete()
    WebsiteLead.objects.filter(
        Q(email__in=mtambo_emails) | Q(inbound_message__icontains='mtambo')
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0040_corporateaccessrequest_verification_ttl'),
    ]

    operations = [
        migrations.RunPython(decouple_adminluxury_and_scrub_mtambo, migrations.RunPython.noop),
    ]
