# 🔐 THE FINISHER LUXURY CRM - Login Details Template

**⚠️ IMPORTANT: This is a template file. Copy this to `LOGIN_DETAILS.md` and fill in your actual credentials.**

## Django Admin Access (Development Only)
- **URL:** http://localhost:8000/admin/
- **Username:** `[YOUR_ADMIN_USERNAME]`
- **Password:** `[YOUR_ADMIN_PASSWORD]`
- **Email:** `[YOUR_ADMIN_EMAIL]`

## API Endpoints
- **Base URL:** http://localhost:8000/
- **API Overview:** http://localhost:8000/
- **Contacts API:** http://localhost:8000/api/contacts/
- **Companies API:** http://localhost:8000/api/companies/
- **Deals API:** http://localhost:8000/api/deals/

## Frontend Access
- **URL:** http://localhost:3000/
- **Development Server:** `npm run dev`

## Quick Start Commands
```bash
# Start Backend
cd backend && python manage.py runserver

# Start Frontend  
cd frontend && npm run dev
```

## Sample Data
To create sample data, run:
```bash
cd backend
python add_sample_data.py
```

---
**🔒 SECURITY NOTE:** 
- Keep `LOGIN_DETAILS.md` in your `.gitignore`
- Never commit actual credentials to version control
- Use environment variables for production credentials
- Change all default passwords before deployment
