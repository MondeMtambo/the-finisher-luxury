# 🔒 Security & Credentials Overview

## About This Repository

This is a **production-ready CRM application** with proper security practices implemented. All sensitive credentials have been removed from this public repository.

## 🛡️ Security Measures Implemented

### 1. Environment Variables
All sensitive configuration is managed through environment variables:
- **DATABASE_URL** - PostgreSQL connection string (Neon database)
- **SECRET_KEY** - Django secret key for cryptographic signing  
- **EMAIL_HOST_PASSWORD** - SMTP credentials for email functionality
- **API keys and tokens** - Stored in deployment platform secrets (Fly.io, Vercel, Railway)

### 2. Files Excluded from Version Control
The following files are **gitignored** and never committed:
- `.env` and `.env.*` - Environment variable files
- `LOGIN_DETAILS.md` - Development credentials
- `secrets/` - Any local credential storage
- `db.sqlite3` - Local development database

### 3. Configuration Files
Sensitive configuration is loaded via:
- **Django settings.py**: Uses `python-decouple` to read from environment variables
- **Default values**: Development-safe defaults only (marked with `django-insecure-` prefix)
- **Production**: All secrets injected via Fly.io secrets, Railway variables, or Azure App Settings

### 4. Database Credentials
- **Production database**: PostgreSQL hosted on Neon (credentials stored in `DATABASE_URL` environment variable)
- **Connection pooling**: SSL-enabled connections
- **No hardcoded credentials** in codebase

### 5. Email Configuration  
- **SMTP provider**: Microsoft Outlook
- **Credentials**: Managed via environment variables
- **App passwords**: Using Outlook app-specific passwords (not account password)

## 🔐 How Credentials Are Managed in Production

### Backend (Fly.io)
```bash
flyctl secrets set DATABASE_URL="postgresql://..." -a the-finisher-luxury-be
flyctl secrets set SECRET_KEY="..." -a the-finisher-luxury-be
flyctl secrets set EMAIL_HOST_PASSWORD="..." -a the-finisher-luxury-be
```

### Frontend (Vercel/Render)
Environment variables configured in deployment dashboard:
- `VITE_API_BASE_URL` - Backend API endpoint
- No sensitive keys in frontend (public client)

## 📋 What You'll Find in This Repo

✅ **Safe for public viewing:**
- Complete application source code
- Django models, views, serializers
- Vue.js frontend components
- API endpoint definitions
- Database migrations (schema only)
- Deployment guides with **placeholder** values
- Architecture documentation

❌ **NOT included (excluded via .gitignore):**
- Actual database credentials
- Production secret keys
- Email passwords
- API tokens
- User data

## 🔍 Code Review Highlights

### Authentication & Authorization
- JWT token-based authentication ([backend/crm/auth_views.py](backend/crm/auth_views.py))
- Role-based access control (RBAC) with 4 user tiers
- Password reset with OTP email verification
- CSRF protection enabled

### Database Security
- Django ORM (prevents SQL injection)
- Parameterized queries throughout
- Transaction atomicity for critical operations
- SSL-required connections to production database

### API Security
- CORS configured for specific origins only
- Rate limiting on authentication endpoints
- Input validation via Django REST Framework serializers
- Password complexity requirements

## 🚀 Deployment Architecture

```
┌─────────────────┐
│  Vercel/Render  │  Frontend (Vue.js)
│  (Static files) │
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│    Fly.io       │  Backend API (Django)
│  (Docker + SSL) │
└────────┬────────┘
         │ SSL
         ↓
┌─────────────────┐
│   Neon DB       │  PostgreSQL Database
│  (Managed PG)   │  (Encrypted at rest)
└─────────────────┘
```

## 📝 Setting Up for Development

If you want to run this project locally:

1. **Clone the repository**
```bash
git clone [this-repo]
cd the-finisher-luxury
```

2. **Create your own `.env` file** (never commit this!)
```bash
cd backend
cp .env.example .env  # Then edit with your values
```

3. **Set required environment variables:**
```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/finisher_dev
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-app-password
```

4. **Install dependencies and run:**
```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```

## 🤝 Questions?

If you have questions about the security architecture, deployment setup, or credential management:
- Review the deployment guides in this repository (with placeholder values)
- Check the documentation in `/docs` folder
- All production credentials are managed via platform-specific secret management

---

**Note to Reviewers:** This application follows industry-standard security practices for credential management. No sensitive data has been committed to this public repository. All production secrets are managed via environment variables and deployment platform secret stores (Fly.io, Vercel, Railway).
