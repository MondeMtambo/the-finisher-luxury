from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_remove_known_test_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mfa_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mfa_code',
            field=models.CharField(blank=True, default='', max_length=6),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mfa_code_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mfa_code_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mfa_verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
