"""
THE FINISHER LUXURY - Tier Limits & Quota Enforcement Engine
Configures commercial limits for:
  - basic (Corporate Sovereign - R0/month Permanent Free)
  - luxury (Luxury Team - R999/month Flagship)
  - executive (Executive Suite - R1,500/month)
  - enterprise (Enterprise Cluster)
"""

TIER_QUOTAS = {
    'basic': {
        'max_users': 5,
        'max_companies': None,  # Unlimited
        'max_contacts': 6000,   # Corporate Sovereign allocation
        'max_deals': None,      # Unlimited
        'max_products': 100,
        'max_campaigns': 5,
        'max_templates': 10,
        'max_workflows': 5,
        'max_tickets': None,
        'max_assets': 10,
        'can_export_reports': True,
        'manager_can_add_employees': True,
        'manager_max_subordinates': 2,
    },
    'luxury': {
        'max_users': 5,
        'max_companies': None,  # Unlimited
        'max_contacts': None,
        'max_deals': None,
        'max_products': None,
        'max_campaigns': None,
        'max_templates': None,
        'max_workflows': None,
        'max_tickets': None,
        'max_assets': None,
        'can_export_reports': True,
        'manager_can_add_employees': True,
        'manager_max_subordinates': 2,
    },
    'executive': {
        'max_users': 15,
        'max_companies': None,
        'max_contacts': None,
        'max_deals': None,
        'max_products': None,
        'max_campaigns': None,
        'max_templates': None,
        'max_workflows': None,
        'max_tickets': None,
        'max_assets': None,
        'can_export_reports': True,
        'manager_can_add_employees': True,
        'manager_max_subordinates': None,
    },
    'enterprise': {
        'max_users': 999,
        'max_companies': None,
        'max_contacts': None,
        'max_deals': None,
        'max_products': None,
        'max_campaigns': None,
        'max_templates': None,
        'max_workflows': None,
        'max_tickets': None,
        'max_assets': None,
        'can_export_reports': True,
        'manager_can_add_employees': True,
        'manager_max_subordinates': None,
    },
}

# Legacy 'trial' tier maps to 'basic' (Corporate Sovereign)
TIER_QUOTAS['trial'] = TIER_QUOTAS['basic']

def check_org_quota(organization, resource: str, current_count: int = None):
    """
    Checks if an organization can create another item of `resource`.
    Returns (allowed: bool, limit: int or None, message: str).
    """
    if not organization:
        return True, None, ""
    
    tier = (organization.subscription_tier or 'basic').lower()
    if tier == 'trial':
        tier = 'basic'
    quotas = TIER_QUOTAS.get(tier, TIER_QUOTAS['basic'])
    limit = quotas.get(f'max_{resource}')
    
    if limit is None:
        return True, None, ""
        
    if current_count is not None and current_count >= limit:
        tier_title = "Corporate Sovereign" if tier == "basic" else tier.title()
        msg = f"{tier_title} allocation limit reached ({limit} {resource} max). Upgrade to Executive Suite for unrestricted fleet allocation."
        return False, limit, msg
        
    return True, limit, ""

def can_add_user(organization=None, user=None):
    """Check if another user can be onboarded into organization"""
    if not organization:
        return True
    tier = (organization.subscription_tier or 'basic').lower()
    if tier == 'trial':
        tier = 'basic'
    limit = TIER_QUOTAS.get(tier, {}).get('max_users', 5)
    from .models import UserProfile
    count = UserProfile.objects.filter(organization=organization).count()
    return count < limit

def get_remaining_user_slots(organization=None):
    """Calculate remaining slots available for this organization"""
    if not organization:
        return 999
    tier = (organization.subscription_tier or 'basic').lower()
    if tier == 'trial':
        tier = 'basic'
    limit = TIER_QUOTAS.get(tier, {}).get('max_users', 5)
    from .models import UserProfile
    count = UserProfile.objects.filter(organization=organization).count()
    return max(0, limit - count)

# Compatibility alias for legacy lookups
LUXURY_TIER_LIMITS = {
    'max_users': 50,
    'max_companies': None,
    'max_contacts': None,
    'max_deals': None,
}
