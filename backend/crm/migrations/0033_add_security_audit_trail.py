# Generated migration for THE FINISHER LUXURY
# POPIA Section 19 & ISO 27001 Security Audit Trail

import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0032_organization_billing_mfa'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityAuditTrail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username_attempted', models.CharField(blank=True, max_length=150)),
                ('event_type', models.CharField(choices=[
                    ('AUTH_LOGIN_SUCCESS', 'Login Success'),
                    ('AUTH_LOGIN_FAILED', 'Login Failed'),
                    ('AUTH_LOGOUT', 'Logout'),
                    ('MFA_CHALLENGE', 'MFA Verification Challenge'),
                    ('MFA_VERIFIED', 'MFA Verification Success'),
                    ('DATA_EXPORT', 'POPIA Data Export (CSV/PDF)'),
                    ('DATA_DELETE', 'Record Deletion / Purge'),
                    ('PRIVILEGE_CHANGE', 'User Role / Plan Mutation'),
                    ('SECURITY_POLICY_VIOLATION', 'Security Policy Violation')
                ], db_index=True, max_length=50)),
                ('severity', models.CharField(choices=[
                    ('INFO', 'Informational'),
                    ('WARNING', 'Warning / Anomaly'),
                    ('CRITICAL', 'Critical Security Alert')
                ], db_index=True, default='INFO', max_length=20)),
                ('description', models.TextField()),
                ('ip_address', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='security_audit_logs', to='crm.organization')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='security_audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Security Audit Trail',
                'verbose_name_plural': 'Security Audit Trails',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='securityaudittrail',
            index=models.Index(fields=['event_type', '-timestamp'], name='crm_sec_ev_ts_idx'),
        ),
        migrations.AddIndex(
            model_name='securityaudittrail',
            index=models.Index(fields=['ip_address', '-timestamp'], name='crm_sec_ip_ts_idx'),
        ),
    ]
