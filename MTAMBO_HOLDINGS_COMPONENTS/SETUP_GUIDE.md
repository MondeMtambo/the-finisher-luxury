# MTAMBO HOLDINGS WEBSITE - SETUP GUIDE

## 🎯 Overview
This is the corporate website for Mtambo Holdings, showcasing services, THE FINISHER CRM system, and company information.

---

## 📁 Files Created (Copy to MTAMBO HOLDINGS folder)

I've created these files in `THE FINISHER LUXURY/MTAMBO_HOLDINGS_COMPONENTS/`:

### 1. **Navbar.vue** → Copy to `MTAMBO HOLDINGS/src/components/`
### 2. **HomePage.vue** → Copy to `MTAMBO HOLDINGS/src/components/`
### 3. **SystemsPage.vue** → Copy to `MTAMBO HOLDINGS/src/components/`

---

## 🛠️ Setup Instructions

### Step 1: Copy Components
```bash
cd "C:\Users\mtamb\Desktop\MTAMBO HOLDINGS"

# Create components directory if not exists
mkdir src\components -Force

# Copy files from THE FINISHER LUXURY\MTAMBO_HOLDINGS_COMPONENTS\
Copy-Item "C:\Users\mtamb\Desktop\THE FINISHER LUXURY\MTAMBO_HOLDINGS_COMPONENTS\*.vue" "C:\Users\mtamb\Desktop\MTAMBO HOLDINGS\src\components\"
```

### Step 2: Install Vue Router
```bash
cd "C:\Users\mtamb\Desktop\MTAMBO HOLDINGS"
npm install vue-router@4
```

### Step 3: Create Router Configuration
Create file: `src/router/index.js`
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import SystemsPage from '../components/SystemsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/systems',
    name: 'Systems',
    component: SystemsPage
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../components/AboutPage.vue')
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('../components/ServicesPage.vue')
  },
  {
    path: '/careers',
    name: 'Careers',
    component: () => import('../components/CareersPage.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../components/ContactPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
```

### Step 4: Update main.js
Edit `src/main.js`:
```javascript
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

createApp(App)
  .use(router)
  .mount('#app')
```

### Step 5: Update App.vue
Edit `src/App.vue`:
```vue
<template>
  <div id="app">
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
```

### Step 6: Create Footer Component
Create file: `src/components/Footer.vue`
```vue
<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-brand">
        <h3>🏢 MTAMBO HOLDINGS</h3>
        <p>Getting It Done Before Someone Else Does</p>
      </div>
      <div class="footer-links">
        <div class="footer-column">
          <h4>Company</h4>
          <router-link to="/about">About Us</router-link>
          <router-link to="/services">Services</router-link>
          <router-link to="/careers">Careers</router-link>
        </div>
        <div class="footer-column">
          <h4>Products</h4>
          <router-link to="/systems">THE FINISHER CRM</router-link>
          <a href="https://thefinisher.co.za" target="_blank">Launch App</a>
        </div>
        <div class="footer-column">
          <h4>Contact</h4>
          <a href="mailto:info@mtamboholdings.co.za">info@mtamboholdings.co.za</a>
          <a href="tel:+27101234567">+27 (0)10 123 4567</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025 Mtambo Holdings. All rights reserved. Built with 🔥 in South Africa</p>
      <p>🇿🇦 Proudly South African • Nhlangothi • Gomazane • Vezi • Masilela</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background: #0a1628;
  color: white;
  padding: 4rem 2rem 2rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto 3rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem;
}

.footer-brand h3 {
  color: #FFD700;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.footer-brand p {
  color: #94a3b8;
  font-style: italic;
}

.footer-column h4 {
  color: #FFD700;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.footer-column a {
  display: block;
  color: #cbd5e1;
  text-decoration: none;
  margin-bottom: 0.75rem;
  transition: color 0.3s ease;
}

.footer-column a:hover {
  color: #FFD700;
}

.footer-bottom {
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 2rem;
  color: #94a3b8;
}

.footer-bottom p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

@media (max-width: 968px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
```

### Step 7: Run Development Server
```bash
cd "C:\Users\mtamb\Desktop\MTAMBO HOLDINGS"
npm run dev
```

---

## 🚀 Deployment Options

### Option 1: Netlify (Recommended - Free)
1. Create account at netlify.com
2. Drag & drop your `dist` folder after running `npm run build`
3. Set custom domain: mtamboholdings.co.za

### Option 2: Vercel (Free)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts

### Option 3: GitHub Pages
1. Create GitHub repo
2. Push code
3. Enable GitHub Pages in settings

---

## 📝 Still Need to Create:

### AboutPage.vue
- Company history
- Team members
- Values & culture

### ServicesPage.vue
- Graphic Design showcase
- Web Development portfolio
- Systems Engineering capabilities
- C++, JavaScript, Python services

### CareersPage.vue
- Open positions
- Company culture
- Application form

### ContactPage.vue
- Contact form
- Office location
- Email/phone

---

## 🎨 Customization

### Colors:
- Primary Gold: #FFD700
- Dark Navy: #0a1628
- Accent Orange: #FFA500

### Fonts:
- Main: 'Segoe UI'
- Headings: Bold 900

---

## 🔗 Integration with THE FINISHER

All "Launch THE FINISHER" buttons link to:
- Production: `https://thefinisher.co.za`
- Local testing: `http://localhost:5173`

---

## ✅ Next Steps:

1. Copy all component files
2. Install Vue Router
3. Create router config
4. Create Footer component
5. Update App.vue and main.js
6. Run `npm run dev` to test
7. Create remaining pages (About, Services, Careers, Contact)
8. Build for production: `npm run build`
9. Deploy to Netlify/Vercel

---

## 💡 Tips:

- Keep design consistent with gold/navy theme
- All external links use `target="_blank"`
- Mobile-first responsive design
- Smooth scroll animations included
- Professional, modern aesthetic

---

Need help with any step? Let me know! 🚀

