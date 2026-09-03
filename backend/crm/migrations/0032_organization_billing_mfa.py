# Generated migration for THE FINISHER LUXURY
# Option A: Organization Multi-Tenancy, Billing Engine & 14-Day Trial, Bank-Grade 2FA

import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0031_alter_websitelead_response_status'),
    ]

    operations = [
        # ──────────────────────────────────────────────────────────
        # 1. Organization Model (Multi-Tenant Isolation)
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Official organization / business entity name', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('subscription_tier', models.CharField(choices=[('trial', '14-Day VIP Trial'), ('luxury', 'The Finisher Luxury Private OS'), ('enterprise', 'Enterprise Custom Retainer')], default='trial', max_length=50)),
                ('trial_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('trial_end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('max_users', models.PositiveIntegerField(default=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
                'ordering': ['-created_at'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # 2. Billing & Subscription Models
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tier', models.CharField(max_length=50, unique=True)),
                ('price_cents', models.PositiveIntegerField(help_text='Price in cents (e.g. 1250000 = R12,500.00)')),
                ('currency', models.CharField(default='ZAR', max_length=10)),
                ('billing_period', models.CharField(choices=[('monthly', 'Monthly'), ('annual', 'Annual Upfront (Negative Working Capital)')], default='monthly', max_length=20)),
                ('features', models.JSONField(blank=True, default=list)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('trial', 'Trial Period'), ('active', 'Active Paid'), ('past_due', 'Past Due'), ('canceled', 'Canceled')], default='trial', max_length=30)),
                ('current_period_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_period_end', models.DateTimeField(blank=True, null=True)),
                ('cancel_at_period_end', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='crm.organization')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='crm.subscriptionplan')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway', models.CharField(choices=[('payfast', 'PayFast (South Africa)'), ('peach', 'Peach Payments'), ('ozow', 'Ozow Instant EFT'), ('stripe', 'Stripe (International)'), ('manual_eft', 'Direct Corporate EFT')], default='payfast', max_length=50)),
                ('transaction_reference', models.CharField(max_length=120, unique=True)),
                ('amount_cents', models.PositiveIntegerField()),
                ('currency', models.CharField(default='ZAR', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=30)),
                ('raw_payload', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='crm.organization')),
            ],
        ),

        # ──────────────────────────────────────────────────────────
        # 3. Add Organization & 2FA Hashing Fields to UserProfile
        # ──────────────────────────────────────────────────────────
        migrations.AddField(
            model_name='userprofile',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mfa_code_hash',
            field=models.CharField(blank=True, help_text='Salted SHA-256 hash of OTP code', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mfa_salt',
            field=models.CharField(blank=True, help_text='Cryptographic salt for OTP hash', max_length=64, null=True),
        ),

        # ──────────────────────────────────────────────────────────
        # 4. Add Organization Tenancy to CRM Entities
        # ──────────────────────────────────────────────────────────
        migrations.AddField(
            model_name='company',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='deal',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='asset',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='emailcampaign',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_campaigns', to='crm.organization'),
        ),
        migrations.AddField(
            model_name='workflow',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workflows', to='crm.organization'),
        ),
    ]
