# Generated migration for THE FINISHER LUXURY
# Add is_cipc_verified to Organization and create TenantVerification model

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0034_add_company_cipc_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_cipc_verified',
            field=models.BooleanField(default=False, help_text='CIPC business entity verified'),
        ),
        migrations.CreateModel(
            name='TenantVerification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(help_text='Official CIPC registered legal entity name', max_length=200)),
                ('trading_name', models.CharField(blank=True, help_text='Trading As (T/A)', max_length=200)),
                ('cipc_number', models.CharField(help_text='Official CIPC Registration Number (e.g. 2024/123456/07)', max_length=30)),
                ('tax_number', models.CharField(blank=True, help_text='SARS Tax / VAT Reference Number', max_length=30)),
                ('director_name', models.CharField(blank=True, help_text='Director / Authorized Officer', max_length=150)),
                ('cipc_certificate', models.FileField(blank=True, help_text='CIPC CoR 14.3 / CK Certificate', null=True, upload_to='verification_docs/')),
                ('proof_of_address', models.FileField(blank=True, help_text='Proof of Business Physical Address', null=True, upload_to='verification_docs/')),
                ('director_id_doc', models.FileField(blank=True, help_text='Director ID or Passport', null=True, upload_to='verification_docs/')),
                ('status', models.CharField(choices=[('pending', 'Pending Verification'), ('verified', 'Verified & Approved'), ('rejected', 'Rejected / Re-submission Required')], default='pending', max_length=20)),
                ('internal_notes', models.TextField(blank=True, help_text='Internal compliance check notes (CIPC BizPortal confirmation)')),
                ('rejection_reason', models.TextField(blank=True, help_text='Feedback provided to client if verification rejected')),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to='crm.organization')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_verifications', to='auth.user')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitted_verifications', to='auth.user')),
            ],
            options={
                'verbose_name': 'Tenant Verification',
                'verbose_name_plural': 'Tenant Verifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
