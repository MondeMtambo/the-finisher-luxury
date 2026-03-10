# 🚀 THE FINISHER LUXURY - Azure Deployment Guide

## ✅ What You Get (FREE!)
- **Azure App Service** - Free tier (1 GB RAM, 1 CPU)
- **Azure Database for PostgreSQL** - Free tier (1 vCore, 32GB storage)
- **SSL/HTTPS** - Included
- No credit card required initially

---

## 📋 ARCHITECTURE

```
Vercel (Frontend - Vue.js)
    ↓
    ↓ HTTPS
    ↓
Azure App Service (Backend - Django)
    ↓
    ↓
Azure PostgreSQL Database
```

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### **STEP 1: Sign Up & Create Resource Group**

1. Go to **https://portal.azure.com**
2. Sign up with Microsoft account (free)
3. Once logged in, search for **"Resource Groups"**
4. Click **"Create"**
5. Fill in:
   - **Subscription:** Choose your subscription
   - **Resource group name:** `finisher-luxury-rg`
   - **Region:** Choose closest to you (e.g., `East US`, `West Europe`)
6. Click **"Review + Create"** → **"Create"**

---

### **STEP 2: Create PostgreSQL Database**

1. Search for **"Azure Database for PostgreSQL flexible server"**
2. Click **"Create"**
3. Fill in:
   - **Resource group:** `finisher-luxury-rg`
   - **Server name:** `finisher-luxury-db`
   - **Region:** Same as resource group
   - **PostgreSQL version:** `15`
   - **Admin username:** `adminuser`
   - **Admin password:** Create strong password (save it!)
   - **Pricing tier:** **Burstable** → **B1ms** (free tier eligible)
4. Click **"Review + Create"** → **"Create"**
5. Wait 5-10 minutes for deployment

---

### **STEP 3: Get Database Connection String**

1. Go to your database resource
2. Click **"Connection strings"** in left menu
3. Copy the **"psycopg2"** connection string
4. It will look like:
```
postgresql://adminuser:YOUR_PASSWORD@finisher-luxury-db.postgres.database.azure.com/postgres?sslmode=require
```
5. **Save this!** You'll need it in Step 5

---

### **STEP 4: Create App Service (Backend)**

1. Search for **"App Services"**
2. Click **"Create"**
3. Fill in:
   - **Resource group:** `finisher-luxury-rg`
   - **Name:** `finisher-luxury-backend`
   - **Publish:** `Code`
   - **Runtime stack:** `Python 3.11`
   - **Operating System:** `Linux`
   - **Region:** Same as database
   - **Pricing plan:** **Free F1** (free tier)
4. Click **"Review + Create"** → **"Create"**

---

### **STEP 5: Configure App Service Environment Variables**

1. Go to your **App Service** → **finisher-luxury-backend**
2. Click **"Configuration"** in left menu
3. Click **"+ New application setting"** for each variable:

| Name | Value |
|------|-------|
| `PYTHON_VERSION` | `3.11` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate random 50-char string (use Python: `import secrets; print(secrets.token_urlsafe(50))`) |
| `DATABASE_URL` | Paste from Step 3 |
| `ALLOWED_HOSTS` | `.azurewebsites.net,.vercel.app` |
| `FRONTEND_URL` | `https://the-finisher-luxury.vercel.app` |
| `CORS_ALLOW_ALL_ORIGINS` | `True` |
| `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` |
| `EMAIL_HOST` | `smtp-mail.outlook.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `your-email@outlook.com` |
| `EMAIL_HOST_PASSWORD` | (leave empty for now) |
| `DEFAULT_FROM_EMAIL` | `your-email@outlook.com` |
| `DJANGO_SUPERUSER_USERNAME` | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | `admin@thefinisher.com` |
| `DJANGO_SUPERUSER_PASSWORD` | `Admin@2025!` |

4. Click **"Save"** at top

---

### **STEP 6: Deploy Code via Git**

1. In App Service, click **"Deployment Center"** (left menu)
2. **Source:** Select `GitHub`
3. Sign in with GitHub
4. **Organization:** `MondeMtambo`
5. **Repository:** `the-finisher-luxury`
6. **Branch:** `main`
7. Click **"Save"**

Azure will automatically deploy when you push to main branch!

**First deploy takes 5-10 minutes.** Check **"Logs"** tab to see progress.

---

### **STEP 7: Create Django Superuser (if needed)**

Once deploy finishes:

1. In App Service, click **"SSH"** (left menu)
2. Click **"Go"** to open terminal
3. Run:
```bash
cd site/wwwroot
python manage.py migrate
python manage.py createsuperuser
```

(Or the environment variables will auto-create it from Step 5)

---

### **STEP 8: Get Your Backend URL**

1. In App Service overview, copy the **URL** at top
2. It will look like: `https://finisher-luxury-backend.azurewebsites.net`
3. **Save this!**

---

### **STEP 9: Update Vercel Frontend**

1. Go to **https://vercel.com** → Your project
2. **Settings** → **Environment Variables**
3. Create/update `VITE_API_BASE_URL`:
   - **Value:** `https://finisher-luxury-backend.azurewebsites.net`
4. Click **"Save"**
5. Go to **"Deployments"** tab
6. Click **"..."** on latest → **"Redeploy"**

---

## ✅ **YOU'RE LIVE!**

- **Frontend:** `https://the-finisher-luxury.vercel.app`
- **Backend:** `https://finisher-luxury-backend.azurewebsites.net`
- **Admin:** username: `admin`, password: `Admin@2025!`

---

## 🔍 **Testing**

1. Try login at your Vercel URL
2. Create test contacts/companies
3. If issues, check App Service **Logs** tab

---

## 💡 **Notes**

- Free tier has limits (1GB RAM, limited connections)
- For production, upgrade to **Standard** tier
- Database auto-backs up daily
- Scale horizontally if needed (more App Service instances)

---

## 🆘 **Troubleshooting**

**"Backend not responding"**
- Check App Service Logs
- Verify DATABASE_URL is correct
- Make sure PostgreSQL firewall allows App Service

**"CORS errors"**
- Verify `CORS_ALLOW_ALL_ORIGINS=True`
- Check `FRONTEND_URL` matches Vercel URL

**"Database connection failed"**
- Test connection string locally
- Check PostgreSQL server is running
- Verify firewall rules allow App Service


