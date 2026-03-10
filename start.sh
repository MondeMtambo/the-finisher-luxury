#!/usr/bin/env bash
set -euo pipefail

# Ensure we're in the repo root (script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Move into backend where manage.py and Django project live
cd backend

# Run database migrations and collect static files (idempotent)
echo "DATABASE_URL is set: $([ -n \"$DATABASE_URL\" ] && echo 'YES' || echo 'NO')"
python manage.py migrate --noinput || { echo "ERROR: Migration failed – check DATABASE_URL env var"; exit 1; }
python manage.py collectstatic --noinput

# Ensure luxury admin account exists and disable legacy sport admin account
python manage.py shell -c "
from django.contrib.auth import get_user_model
from crm.models import UserProfile

User = get_user_model()
username = 'adminluxury'
email = 'admin@thefinisher.co.za'
password = '${DJANGO_SUPERUSER_PASSWORD:-Admin@2026!}'

user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': email, 'is_staff': True, 'is_superuser': True, 'is_active': True}
)

if created:
    user.set_password(password)
    print(f'✓ Created {username} superuser')
else:
    if not user.email:
        user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    if '${DJANGO_SUPERUSER_PASSWORD:-}':
        user.set_password(password)
        print(f'✓ Updated {username} password from env')
    else:
        print(f'✓ Ensured {username} privileges (password unchanged)')

user.save()

profile, _ = UserProfile.objects.get_or_create(user=user)
profile.role = 'admin'
profile.tier = 'luxury'
profile.company_name = profile.company_name or 'THE FINISHER LUXURY'
profile.payment_status = profile.payment_status or 'paid'
profile.save()
print('✓ Ensured adminluxury profile')

legacy = User.objects.filter(username__iexact='adminsport').exclude(id=user.id).first()
if legacy:
    legacy.is_active = False
    legacy.set_unusable_password()
    legacy.save(update_fields=['is_active', 'password'])
    print('✓ Disabled legacy adminsport account')
" || echo "Note: adminluxury bootstrap had issues, check logs"

# Optionally auto-create a Django superuser if env vars are provided
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  echo "Ensuring Django superuser ${DJANGO_SUPERUSER_USERNAME} exists..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model
from crm.models import UserProfile
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME}'
email = '${DJANGO_SUPERUSER_EMAIL}'
password = '${DJANGO_SUPERUSER_PASSWORD}'

user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': email, 'is_staff': True, 'is_superuser': True}
)
if created:
    user.set_password(password)
    user.save()
    print(f'✓ Superuser {username} created')
else:
    # Update password if user exists
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f'✓ Superuser {username} password updated')

# Ensure UserProfile exists
UserProfile.objects.get_or_create(user=user, defaults={'tier': 'free'})
print(f'✓ UserProfile for {username} ensured')
" || echo "Note: Superuser creation had issues, check logs"
fi

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
exec gunicorn finisher_api.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
