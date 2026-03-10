# 🥈 THE FINISHER LUXURY - Implementation Guide

## 1️⃣ Frontend Changes

### A. Register.vue - Tier Selection

**File**: `the-finisher-luxury/frontend/src/components/Register.vue`

**Change**: Default tier to 'luxury' instead of 'luxury'

```javascript
// Line ~285 (in data())
form: {
  // ... other fields
  tier: 'luxury'  // Changed from 'luxury'
}

// Add method to detect edition
computed: {
  isLuxuryEdition() {
    return window.location.hostname.includes('luxury')
  }
}

// Payment amount (line ~395)
const amount = this.form.tier === 'luxury' ? 249 : 99  // Changed amounts
```

**Key Changes**:
- Default tier: 'luxury'
- Block LUXURY tier with message: "Upgrade to LUXURY for premium features (R249/month)"
- Show LUXURY as active with "ACTIVE EDITION" badge
- Payment link: `?tier=luxury&amount=249`

---

### B. Dashboard.vue - Edition Branding

**File**: `the-finisher-luxury/frontend/src/components/Dashboard.vue`

**Change**: Update tier indicators and messaging

```javascript
// Tier display (computed properties)
tierDisplayName() {
  const tier = this.userTier
  const names = { 
    luxury: '🥈 LUXURY',      // Changed from 'luxury': '🏆 LUXURY'
    premium: '🥇 PREMIUM'
  }
  return names[tier] || tier
}

tierSubtitle() {
  return 'R249/month' // Changed from 'R99/month'
}

tierFeatureAccess() {
  return {
    luxury: {
      maxUsers: 10,              // Changed from 2
      companyAutoCreate: true,
      advancedReporting: true,
      apiAccess: true,           // ✨ NEW
      customIntegrations: true   // ✨ NEW
    }
  }
}

// Welcome banner text
welcomeText() {
  return 'Welcome to THE FINISHER LUXURY! 🥈'
}

sportEditionBannerText() {
  return '⚡ LUXURY EDITION ACTIVE: 10-User Access | API Access | Custom Integrations | Priority Support'
}
```

---

### C. Navbar.vue - Branding Update

**File**: `the-finisher-luxury/frontend/src/components/Navbar.vue`

**Change**: Navigation menu text

```vue
<!-- Update app name/logo -->
<div class="navbar-brand">
  <span class="brand-name">THE FINISHER LUXURY</span>
  <span class="badge badge-purple">LUXURY EDITION</span>
</div>
```

---

### D. login.vue - Edition Branding

**File**: `the-finisher-luxury/frontend/src/components/Login.vue`

```javascript
// Page header
<h1>Welcome to THE FINISHER LUXURY 🥈</h1>
<p>Premium CRM for Enterprise Teams</p>
```

---

### E. index.html - Page Title

**File**: `the-finisher-luxury/frontend/index.html`

```html
<!-- Change -->
<title>THE FINISHER LUXURY - Enterprise CRM</title>

<!-- Update meta descriptions -->
<meta name="description" content="THE FINISHER LUXURY - Premium CRM with 10-user access, API integrations, and advanced analytics">
```

---

### F. package.json - Project Name

**File**: `the-finisher-luxury/frontend/package.json`

```json
{
  "name": "finisher-luxury-frontend",
  "version": "1.0.0",
  "description": "THE FINISHER LUXURY - Premium CRM Edition"
}
```

---

## 2️⃣ Backend Changes

### A. tier_limits.py - Max Users

**File**: `the-finisher-luxury/backend/crm/tier_limits.py`

```python
# Change max_users from 2 to 10
SPORT_TIER_LIMITS = {
    'account_type': 'luxury',  # Changed for clarity
    'max_users': 10,           # Changed from 2
    'features': {
        'api_access': True,      # ✨ NEW
        'custom_integrations': True,  # ✨ NEW
        'advanced_reporting': True,
        'email_sync': True,      # ✨ NEW
        'custom_workflows': True  # ✨ NEW
    }
}
```

---

### B. models.py - Tier Configuration

**File**: `the-finisher-luxury/backend/crm/models.py`

```python
# In UserProfile model
ROLE_CHOICES = (
    ('admin', 'CEO / Administrator'),
    ('executive', 'Executive'),
    ('manager', 'Manager'),
    ('supervisor', 'Supervisor'),
    ('user', 'Standard Employee'),
)

TIER_CHOICES = (
    ('luxury', 'LUXURY Tier'),   # Changed from 'luxury'
)

# Default tier
tier = models.CharField(
    max_length=20,
    choices=TIER_CHOICES,
    default='luxury'  # Changed from 'luxury'
)

# Property for max users
@property
def max_users_for_tier(self):
    return 10  # Changed from 2
```

---

### C. settings.py - Edition Name

**File**: `the-finisher-luxury/backend/finisher_api/settings.py`

```python
# Update constants
APP_EDITION = 'LUXURY'
MAX_USERS_PER_COMPANY = 10  # Changed from 2
TIER_PRICING = 'R249/month'  # Changed from R99
TIER_NAME = 'LUXURY'
```

---

### D. auth_views.py - User Limit Check

**File**: `the-finisher-luxury/backend/crm/auth_views.py` (register method)

```python
# The max user check already uses tier_limits.py, so it will 
# automatically enforce 10 users when we update tier_limits.py above

# Current code (no change needed):
def register(request):
    max_users = int(SPORT_TIER_LIMITS.get('max_users', 50))
    current_count = User.objects.filter(...).count()
    
    if current_count >= max_users:
        return Response({
            'error': f'Maximum {max_users} users allowed on LUXURY tier'
        }, status=403)
```

---

### E. README.md - Documentation

**File**: `the-finisher-luxury/README.md`

```markdown
# 🥈 THE FINISHER LUXURY

Premium CRM solution with enterprise features.

**Edition**: LUXURY (R249/month)
**Max Users**: 10
**Key Features**: 
- ✅ 10-user access
- ✅ Full API access
- ✅ Custom integrations
- ✅ Advanced analytics
- ✅ Email synchronization
- ✅ Custom workflows
- ✅ Priority support

**Deployment**: The LUXURY system runs on separate cloud infrastructure.
```

---

## 3️⃣ Environment Variables (Render)

### Backend Environment Variables

```env
# LUXURY Backend Database
DATABASE_URL=postgresql://user:password@neon.tech/finisher_luxury_db

# API Configuration
API_URL=https://the-finisher-luxury-api.onrender.com
FRONTEND_URL=https://the-finisher-luxury.onrender.com

# Edition Configuration
APP_EDITION=LUXURY
TIER_NAME=luxury
MAX_USERS=10
TIER_PRICING=R249/month

# Payment Gateway
PAYMENT_GATEWAY_URL=https://payment-gateway.com/checkout?tier=luxury
PAYMENT_TIER_ID=luxury_249

# Email/Notifications
EMAIL_FROM=noreply@finisher-luxury.com
SUPPORT_EMAIL=support@finisher-luxury.com
```

### Frontend Environment Variables

**File**: `.env.production` (create or update)

```env
VITE_API_URL=https://the-finisher-luxury-api.onrender.com
VITE_APP_EDITION=LUXURY
VITE_TIER_PRICING=R249
VITE_MAX_USERS=10
```

---

## 4️⃣ Database Setup

### PostgreSQL Database Creation

```sql
-- Create separate database for LUXURY tier
CREATE DATABASE finisher_luxury_db;

-- Create user
CREATE USER finisher_luxury_user WITH PASSWORD 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE finisher_luxury_db TO finisher_luxury_user;

-- Tables will be created by Django migrations (same schema as LUXURY)
```

### Connection String
```
postgresql://finisher_luxury_user:password@neon.tech/finisher_luxury_db
```

---

## 5️⃣ Git & Deployment

### Initialize LUXURY as Separate Project

```bash
cd c:\Users\mtamb\Desktop\the-finisher-luxury

# Update git remote to new repository
git remote remove origin
git remote add origin https://github.com/MondeMtambo/the-finisher-luxury.git

# Or just change the remote URL if repo exists
git remote set-url origin https://github.com/MondeMtambo/the-finisher-luxury.git

# Commit all changes
git add .
git commit -m "Initialize LUXURY Edition - separate system from Luxury Edition

- Default tier: LUXURY (R249/month, 10 users max)
- Backend: 10-user limit enforcement
- Frontend: LUXURY branding and UI
- Database: Separate PostgreSQL instance
- Deployment: Independent Render services"

# Push to GitHub
git push -u origin main
```

---

## 6️⃣ Render Deployment Setup

### Create New Render Services

#### 1️⃣ LUXURY Backend API
```
Name: the-finisher-luxury-api
GitHub Branch: main
Build Command: pip install -r requirements.txt && python manage.py migrate
Start Command: gunicorn finisher_api.wsgi:application --bind 0.0.0.0:$PORT
Environment Variables: (use values from Environment Variables section above)
```

#### 2️⃣ LUXURY Frontend Static Site
```
Name: the-finisher-luxury
GitHub Branch: main
Root Directory: frontend
Build Command: cd frontend && npm install && npm run build
Publish Directory: frontend/dist
Environment Variables: VITE_API_URL, etc.
```

---

## 7️⃣ File Changes Summary

### List of Files to Modify in `the-finisher-luxury`

```
Frontend:
  ✓ frontend/src/components/Register.vue      (tier='luxury', amounts)
  ✓ frontend/src/components/Dashboard.vue     (branding, features)
  ✓ frontend/src/components/Login.vue         (header text)
  ✓ frontend/src/components/Navbar.vue        (app name)
  ✓ frontend/index.html                       (page title)
  ✓ frontend/package.json                     (project name)
  ✓ .env.production (create new)              (API URLs)

Backend:
  ✓ backend/crm/tier_limits.py                (max_users=10)
  ✓ backend/crm/models.py                     (tier defaults)
  ✓ backend/finisher_api/settings.py          (edition config)
  ✓ backend/README.md                         (documentation)

Documentation:
  ✓ README.md                                 (edition branding)
  ✓ .gitignore                                (same)

Files NOT to modify (both systems can share):
  - backend/crm/views.py                      (logic is tier-agnostic)
  - backend/crm/serializers.py                (same)
  - backend/crm/urls.py                       (same)
```

---

## 8️⃣ Testing Checklist

### Pre-Deployment Testing

```
Local Testing:
  [ ] npm install && npm run dev (frontend works)
  [ ] python manage.py runserver (backend starts)
  [ ] Registration shows LUXURY tier selected
  [ ] Dashboard shows LUXURY branding
  [ ] Can create max 10 users (test user limit)
  [ ] Payment link shows R249 amount

Production Testing:
  [ ] Frontend deploys to Render
  [ ] Backend deploys to Render
  [ ] Register page loads correctly
  [ ] Can register as LUXURY tier
  [ ] Dashboard shows LUXURY features
  [ ] API endpoints work with new max_users
  [ ] Database migrations applied successfully
```

---

## 9️⃣ Parallel Systems Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    LUXURY vs LUXURY                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🏆 Luxury Edition                  🥈 LUXURY EDITION       │
│  ├─ R99/month                      ├─ R249/month           │
│  ├─ 2 users max                    ├─ 10 users max         │
│  ├─ Basic reporting                ├─ Advanced analytics   │
│  ├─ No API access                  ├─ Full API access      │
│  ├─ No integrations                ├─ Custom integrations  │
│  ├─ No email sync                  ├─ Email sync support   │
│  │                                 ├─ Workflows            │
│  │                                 └─ Priority support     │
│  │                                                         │
│  URL: luxury.onrender.com           URL: luxury.onrender.com
│  API: luxury-api.onrender.com       API: luxury-api.onrender.com
│  DB: finisher_sport_db             DB: finisher_luxury_db  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔟 Next Steps

1. **Immediate** (Today):
   - [ ] Review this guide
   - [ ] Make all frontend changes (Register, Dashboard, etc.)
   - [ ] Update backend tier_limits.py and settings.py
   - [ ] Test locally

2. **Short-term** (This week):
   - [ ] Create new GitHub repo for LUXURY
   - [ ] Push code to GitHub
   - [ ] Create Render applications
   - [ ] Configure PostgreSQL on Neon
   - [ ] Deploy both services

3. **Medium-term** (Next 1-2 weeks):
   - [ ] Test payment flows
   - [ ] Monitor logs and errors
   - [ ] Update marketing/pricing pages
   - [ ] Train team on tier selection

4. **Long-term** (Month 2+):
   - [ ] Implement API endpoints (for API access feature)
   - [ ] Add analytics dashboard
   - [ ] Email integration
   - [ ] Custom workflows
   - [ ] Advanced reporting/exports


