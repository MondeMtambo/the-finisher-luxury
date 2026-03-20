from django.db import migrations
from django.db.models import Q


def remove_known_test_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    test_usernames = [
        'testclient',
        'test_company_user',
    ]
    test_emails = [
        'client@test.com',
        'test@example.com',
        'mtambo@example.com',
        'john.kzn@gmail.com',
        'sarah.durban@gmail.com',
    ]

    # Delete only specific known test accounts.
    User.objects.filter(Q(username__in=test_usernames) | Q(email__in=test_emails)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_luxury_phase1_features'),
    ]

    operations = [
        migrations.RunPython(remove_known_test_users, migrations.RunPython.noop),
    ]
