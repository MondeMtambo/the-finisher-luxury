"""
THE FINISHER LUXURY - Tier Limits

LUXURY Edition Features:
- Unlimited Contacts ✅ (premium feature!)
- Unlimited Companies ✅
- Up to 10 users (via LUXURY_MAX_USERS env)
- Unlimited activity logs
- All premium features included + API Access, Webhooks, Workflows
"""

import os

LUXURY_MAX_USERS = int(os.environ.get('LUXURY_MAX_USERS', '10') or '10')

LUXURY_TIER_LIMITS = {
    'max_companies': 'unlimited',
    'max_users': LUXURY_MAX_USERS,
    'max_activity_logs': 'unlimited',
    'contacts': 'unlimited',  # Premium feature!
    'deals': 'unlimited',
    'time_tracking': True,
    'email_integration': True,
    'advanced_reporting': True,
}

def can_add_user():
    """Check if another user can be added to the system"""
    from django.contrib.auth.models import User
    current_user_count = User.objects.count()
    return current_user_count < LUXURY_TIER_LIMITS['max_users']

def get_remaining_user_slots():
    """Get number of remaining user slots"""
    from django.contrib.auth.models import User
    current_user_count = User.objects.count()
    return max(0, LUXURY_TIER_LIMITS['max_users'] - current_user_count)

