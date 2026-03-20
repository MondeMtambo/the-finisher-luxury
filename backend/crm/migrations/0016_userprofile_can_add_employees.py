# Generated migration for can_add_employees field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_userprofile_business_website_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='can_add_employees',
            field=models.BooleanField(default=False, help_text='Delegated permission: employee can add new employees (requires admin OTP)'),
        ),
    ]
