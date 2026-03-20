from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='company_direct_line',
            field=models.CharField(blank=True, help_text='Direct company line when using a corporate email', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_self_employed',
            field=models.BooleanField(default=False, help_text='Mark if the contact operates as self-employed'),
        ),
    ]
