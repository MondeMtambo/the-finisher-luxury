import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'adminluxury')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

if not ADMIN_PASSWORD:
    raise SystemExit('Set ADMIN_PASSWORD environment variable before running this script.')

admin_user, created = User.objects.get_or_create(
    username=ADMIN_USERNAME,
    defaults={'email': ADMIN_EMAIL}
)

admin_user.email = ADMIN_EMAIL
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.set_password(ADMIN_PASSWORD)
admin_user.save()

print('Superuser created/updated successfully.')
print(f'Username: {ADMIN_USERNAME}')
print(f'Email: {ADMIN_EMAIL}')