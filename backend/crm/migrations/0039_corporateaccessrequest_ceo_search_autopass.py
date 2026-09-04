# Generated manually for CorporateAccessRequest CEO Search & Auto-Generated Password fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0038_corporateaccessrequest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporateaccessrequest',
            name='target_ceo_name',
            field=models.CharField(blank=True, help_text='Matched CEO if applicant is non-CEO', max_length=150),
        ),
        migrations.AddField(
            model_name='corporateaccessrequest',
            name='target_organization_id',
            field=models.CharField(blank=True, help_text='Matched Organization ID if applicant is non-CEO', max_length=100),
        ),
        migrations.AddField(
            model_name='corporateaccessrequest',
            name='auto_generated_password',
            field=models.CharField(blank=True, help_text='Auto-generated credentials dispatched upon executive approval', max_length=100),
        ),
    ]
