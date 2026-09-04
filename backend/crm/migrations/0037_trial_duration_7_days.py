# Generated migration for THE FINISHER LUXURY
# Update Organization subscription_tier choice to 7-Day VIP Trial

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0036_contact_cipc_and_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='subscription_tier',
            field=models.CharField(
                choices=[
                    ('trial', '7-Day VIP Trial'),
                    ('luxury', 'The Finisher Luxury Private OS'),
                    ('enterprise', 'Enterprise Custom Retainer'),
                ],
                default='trial',
                max_length=50
            ),
        ),
    ]
