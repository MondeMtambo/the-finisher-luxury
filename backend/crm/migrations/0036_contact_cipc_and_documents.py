# Generated migration for THE FINISHER LUXURY
# Add cipc_number, tax_number, document, and notes to Contact model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0035_business_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='cipc_number',
            field=models.CharField(
                blank=True,
                help_text='CIPC Registration Number (e.g. 2024/123456/07)',
                max_length=30
            ),
        ),
        migrations.AddField(
            model_name='contact',
            name='tax_number',
            field=models.CharField(
                blank=True,
                help_text='SARS Tax / VAT Number',
                max_length=30
            ),
        ),
        migrations.AddField(
            model_name='contact',
            name='document',
            field=models.FileField(
                blank=True,
                help_text='Client CIPC / registration / compliance document',
                null=True,
                upload_to='contact_docs/'
            ),
        ),
        migrations.AddField(
            model_name='contact',
            name='notes',
            field=models.TextField(
                blank=True,
                help_text='Additional client relationship notes'
            ),
        ),
    ]
