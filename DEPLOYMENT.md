# 🏆 Deployment Guide: THE FINISHER LUXURY CRM

Get your premium CRM live in **10 minutes** using free hosting!

## 🎯 Quick Deploy Stack

### Frontend → **Vercel** (Free Forever)
### Backend → **Railway** (Free $5/month credit)

**Total Monthly Cost:** $0 (Railway's $5 credit covers everything!)

**Note:** THE FINISHER LUXURY is a separate deployment from THE FINISHER CRM.
Create new projects on both Vercel and Railway to keep systems independent.

---

## 📦 Part 1: Deploy Backend to Railway (5 min)

### Step 1: Sign Up & Connect GitHub
1. Go to **https://railway.app**
2. Click **"Login"** → Use **GitHub** account
3. You'll need to add a payment method (card won't be charged, just verification)

### Step 2: Deploy from GitHub
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: **Your new LUXURY repository** (when created)
4. Railway auto-detects everything from `railway.json` ✨

### Step 3: Add PostgreSQL Database
1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically creates `DATABASE_URL` environment variable

### Step 4: Add Environment Variables
Railway creates some automatically, but add these manually:

Click **"Variables"** tab and add:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Click "Generate" or use any random 50-char string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.railway.app` |
| `FRONTEND_URL` | `https://your-app.vercel.app` *(update after Vercel deploy)* |
| `CORS_ALLOWED_ORIGINS` | `https://your-app.vercel.app` *(update after Vercel deploy)* |

### Step 5: Deploy!
- Railway auto-deploys on push to main
- First deploy takes ~3-5 minutes
- Copy your backend URL: `https://the-finisher-crmproduction.up.railway.app`

### Step 6: Run Migrations & Create Admin
1. In Railway dashboard, click **"the-finisher-backend"** service
2. Click **"Shell"** tab (or Settings → Deploy → Shell)
3. Run these commands:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

4. Follow prompts to create your admin account

✅ **Backend is LIVE!**

---

## 🎨 Part 2: Deploy Frontend to Vercel (2 min)

### Step 1: Sign Up & Connect GitHub
1. Go to **https://vercel.com**
2. Click **"Sign Up"** → Use **GitHub** account (no card needed!)
3. Click **"Add New"** → **"Project"**
4. Import: **MondeMtambo/the-finisher**

### Step 2: Configure Build
Vercel reads `vercel.json` automatically, but verify these settings:

**Framework Preset:** Vite  
**Root Directory:** `./` (keep as default)  
**Build Command:** `cd frontend && npm install && npm run build`  
**Output Directory:** `frontend/dist`

### Step 3: Add Environment Variable
Click **"Environment Variables"** and add:

| Variable | Value |
|----------|-------|
| `VITE_API_BASE_URL` | `https://the-finisher-crmproduction.up.railway.app` |

*(Paste your Railway backend URL from Part 1, Step 5)*

### Step 4: Deploy!
- Click **"Deploy"**
- Wait ~1-2 minutes
- **Your app is LIVE:** `https://your-app-name.vercel.app` 🎉

---

## � Part 3: Connect Frontend ↔ Backend (1 min)

### Update Backend Environment Variables (Railway)
1. Go back to Railway dashboard → Your backend service
2. Click **"Variables"** tab
3. Update these two:

| Variable | Updated Value |
|----------|---------------|
| `FRONTEND_URL` | `https://your-app-name.vercel.app` |
| `CORS_ALLOWED_ORIGINS` | `https://your-app-name.vercel.app` |

4. Railway auto-redeploys (~1 min)

### Verify Everything Works
1. Open your Vercel URL: `https://your-app-name.vercel.app`
2. You should see THE FINISHER FREE login page
3. Check the "I agree to Disclaimer & Privacy" box
4. Login with your superuser credentials
5. **YOU'RE LIVE!** 🚀

---

## 💰 What You Get (FREE)

### Vercel
- ✅ **Unlimited bandwidth & requests**
- ✅ Auto HTTPS/SSL
- ✅ Global CDN (fast everywhere)
- ✅ Auto-deploy on every git push
- ✅ Free custom domain support

### Railway
- ✅ **$5 credit per month** (~500 hours equivalent)
- ✅ Always-on (NO sleep/cold starts!)
- ✅ PostgreSQL database included
- ✅ Auto-deploy from GitHub
- ✅ Easy scaling when ready
- ✅ Great logs and monitoring

**Perfect for launch + first ~50-100 users!**

---

## 📊 Usage Monitoring

### Railway Dashboard
- Check **"Metrics"** tab to see credit usage
- Typically: ~$3-4/month for light traffic
- Set up billing alerts at $4 to get notified

### Vercel Dashboard
- Check **"Analytics"** for traffic
- Vercel free tier = unlimited (no worries!)

---

## 🚨 Post-Deploy Checklist

After going live, do these:

- [ ] Test login/logout flow
- [ ] Create a test contact, company, and deal
- [ ] Verify Disclaimer page loads properly
- [ ] Check footer links (Nated Graphics, LinkedIn, etc.)
- [ ] Update `frontend/src/config/links.js` with real social URLs
- [ ] Replace `legal@yourdomain.co.za` with actual email
- [ ] Set up a custom domain (optional, but professional!)
- [ ] Test on mobile browser
- [ ] Share with first test users!

---

## 🎨 Custom Domain (Optional)

### On Vercel:
1. Go to project **Settings** → **Domains**
2. Add your domain (e.g., `app.yourdomain.com`)
3. Update DNS records as shown (usually CNAME)
4. Auto HTTPS in ~1 minute!

### Update Railway:
1. Update `ALLOWED_HOSTS` to include your domain
2. Update `CORS_ALLOWED_ORIGINS` to your custom domain

---

## 🔧 Common Issues & Fixes

### ❌ "Network Error" when logging in
**Cause:** CORS not configured  
**Fix:** 
- Check `CORS_ALLOWED_ORIGINS` in Railway includes your Vercel URL
- Ensure no trailing slash on URLs
- Railway auto-redeploys when you update variables

### ❌ "This site can't be reached"
**Cause:** Backend still deploying or crashed  
**Fix:**
- Check Railway **"Deployments"** tab for status
- Check **"Logs"** tab for errors
- Common issue: Missing `DATABASE_URL` (ensure PostgreSQL is added)

### ❌ Frontend shows but can't connect to backend
**Cause:** Wrong `VITE_API_BASE_URL`  
**Fix:**
- Verify URL in Vercel **Settings** → **Environment Variables**
- Must start with `https://` and have NO trailing slash
- Redeploy Vercel after fixing

### ❌ "Static files not found"
**Cause:** Collectstatic didn't run  
**Fix:**
- Railway should run this automatically via `railway.json`
- Check deployment logs in Railway
- Manually run in Shell: `cd backend && python manage.py collectstatic --noinput`

---

## � When You Need to Pay (Later)

### Railway (~Month 2-3)
If you go over $5 credit:
- Add more funds (minimum $5)
- Or upgrade to Hobby plan ($5/month = $5 credit included)

### Database
- PostgreSQL is free on Railway (included in $5 credit)
- If you need more storage: ~$1/GB extra

---

## � Scaling Tips (When Growing)

### Performance Optimization:
1. Add Redis caching (Railway plugin)
2. Enable Vercel Analytics (free tier)
3. Set up error monitoring (Sentry free tier)
4. Add Railway's "Autoscaling" when traffic grows

### When to Upgrade:
- Railway Hobby ($5/mo): Better support, more usage
- Railway Pro ($20/mo): Team features, priority support
- Vercel Pro ($20/mo): Team features, better analytics

---

## � Need Help?

### Railway Support:
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

### Vercel Support:
- Docs: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions

### Your Deployment URLs:
- **Frontend:** https://your-app-name.vercel.app
- **Backend API:** https://completer-backend-production-xxxx.up.railway.app
- **Admin Panel:** https://completer-backend-production-xxxx.up.railway.app/admin

---

## � You're Live on Railway + Vercel!

**Pro Stack, Zero Cost (for now)!**

Share your app and get those first users! 🚀

When you're ready to add:
- Custom domain
- Email notifications
- Advanced analytics
- Payment processing

...just shout! 💪


