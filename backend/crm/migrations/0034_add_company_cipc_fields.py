# Generated migration for THE FINISHER LUXURY
# Add trading_name, registration_number (CIPC), tax_number, industry, and cipc_verified to Company

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0033_add_security_audit_trail'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='trading_name',
            field=models.CharField(blank=True, help_text='Trading As / T/A', max_length=200),
        ),
        migrations.AddField(
            model_name='company',
            name='registration_number',
            field=models.CharField(blank=True, help_text='CIPC Registration Number (e.g. 2024/123456/07)', max_length=30),
        ),
        migrations.AddField(
            model_name='company',
            name='tax_number',
            field=models.CharField(blank=True, help_text='SARS Tax / VAT Number', max_length=30),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.CharField(blank=True, help_text='Industry / Sector', max_length=100),
        ),
        migrations.AddField(
            model_name='company',
            name='cipc_verified',
            field=models.BooleanField(default=False, help_text='Verified against CIPC format / database'),
        ),
    ]
