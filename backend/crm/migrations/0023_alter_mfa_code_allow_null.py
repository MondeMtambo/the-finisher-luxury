from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_userprofile_mfa_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mfa_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
