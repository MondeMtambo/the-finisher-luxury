# Generated for CorporateAccessRequest 5-minute ephemeral verification retention (TTL)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0039_corporateaccessrequest_ceo_search_autopass'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporateaccessrequest',
            name='is_verified',
            field=models.BooleanField(db_index=True, default=False, help_text='Whether applicant verified identity via 6-digit OTP'),
        ),
        migrations.AddField(
            model_name='corporateaccessrequest',
            name='verification_code',
            field=models.CharField(blank=True, help_text='6-digit verification code', max_length=6),
        ),
        migrations.AddField(
            model_name='corporateaccessrequest',
            name='expires_at',
            field=models.DateTimeField(blank=True, db_index=True, help_text='5-minute expiration timestamp for unverified requests', null=True),
        ),
    ]
