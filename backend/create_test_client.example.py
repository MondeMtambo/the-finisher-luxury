#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finisher_api.settings')
django.setup()

from django.contrib.auth.models import User

USERNAME = os.getenv('CLIENT_ADMIN_USERNAME', 'testclient')
EMAIL = os.getenv('CLIENT_ADMIN_EMAIL', 'client@example.com')
PASSWORD = os.getenv('CLIENT_ADMIN_PASSWORD')
FIRST_NAME = os.getenv('CLIENT_ADMIN_FIRST_NAME', 'Test')
LAST_NAME = os.getenv('CLIENT_ADMIN_LAST_NAME', 'Client')

if not PASSWORD:
    raise SystemExit('Set CLIENT_ADMIN_PASSWORD environment variable before running this script.')

user, created = User.objects.get_or_create(username=USERNAME, defaults={'email': EMAIL})
user.email = EMAIL
user.first_name = FIRST_NAME
user.last_name = LAST_NAME
user.set_password(PASSWORD)
user.save()

print('Client admin user created/updated successfully.')
print(f'Username: {USERNAME}')
print(f'Email: {EMAIL}')