# Generated migration for EmployeeAddOTP model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0016_userprofile_can_add_employees'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAddOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('employee_data', models.JSONField(help_text='Serialized data for the new employee to create upon approval')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('admin_user', models.ForeignKey(help_text='The company admin who must approve', on_delete=django.db.models.deletion.CASCADE, related_name='employee_add_otps', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ForeignKey(help_text='The delegated employee requesting to add', on_delete=django.db.models.deletion.CASCADE, related_name='employee_add_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
