# Generated data migration to purge test tenant Adminluxury Enterprise

from django.db import migrations
from django.db.models import Q


def purge_adminluxury_enterprise(apps, schema_editor):
    Organization = apps.get_model('crm', 'Organization')
    UserProfile = apps.get_model('crm', 'UserProfile')
    User = apps.get_model('auth', 'User')

    # Find and delete test organization Adminluxury Enterprise
    test_orgs = Organization.objects.filter(
        Q(name__icontains='adminluxury') | Q(slug__icontains='adminluxury')
    )
    for org in test_orgs:
        UserProfile.objects.filter(organization=org).update(organization=None, company_name='')
        org.delete()

    # Ensure sovereign adminluxury user is decoupled from any tenant
    admin_user = User.objects.filter(username__iexact='adminluxury').first()
    if admin_user:
        profile = UserProfile.objects.filter(user=admin_user).first()
        if profile and profile.organization_id is not None:
            profile.organization = None
            profile.company_name = ''
            profile.save(update_fields=['organization', 'company_name'])


def reverse_purge(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0051_remove_organization_tender_pack_unlocked'),
    ]

    operations = [
        migrations.RunPython(purge_adminluxury_enterprise, reverse_purge),
    ]
