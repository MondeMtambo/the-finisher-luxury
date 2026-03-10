# 🏆 THE FINISHER LUXURY CRM
**Professional CRM for Growth Teams**

> Premium customer relationship management platform built with Django & Vue.js

[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)

---

## 📋 Overview

THE FINISHER LUXURY is a full-stack CRM application designed for small to medium-sized teams (up to 10 users). This repository showcases enterprise-grade architecture, modern development practices, and production-ready code.

## ✨ Key Features

### Core CRM Functionality
- **Contact Management** - Comprehensive contact profiles with relationship tracking
- **Company Management** - Hierarchical organization structure
- **Deal Pipeline** - Visual deal stages with value tracking
- **Activity Logging** - Complete audit trail of all interactions

### Advanced Features
- **Relationship Health Scoring** - Algorithmic engagement tracking (Hot/Warm/Cold/At Risk)
- **Time Tracking** - Built-in timer for billable hours
- **Multi-User Collaboration** - Role-based access control (Admin, Manager, Sales, User)
- **Global Search** - Real-time search across all entities
- **CSV Import/Export** - Bulk data operations

### Technical Highlights
- JWT authentication with refresh tokens
- RESTful API architecture
- Real-time form validation
- Responsive mobile-first design
- Optimistic UI updates
- Transaction-safe database operations

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL (Neon)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Email:** SMTP with OTP verification
- **Deployment:** Fly.io (Docker)

### Frontend
- **Framework:** Vue.js 3 (Composition API)
- **Router:** Vue Router
- **HTTP:** Axios
- **Styling:** Custom CSS with glassmorphism
- **Build:** Vite
- **Deployment:** Vercel/Render

## 📁 Project Structure

```
the-finisher-luxury/
├── backend/
│   ├── crm/                    # Main application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data validation
│   │   ├── auth_views.py      # Authentication
│   │   └── migrations/        # Database schema
│   ├── finisher_api/          # Project settings
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── router/            # Route definitions
│   │   └── main.js            # App entry point
│   └── package.json           # Node dependencies
├── docs/                      # Technical documentation
├── LICENSE                    # Proprietary license
└── SECURITY_README.md         # Security practices
```

## 🔐 Security

This application implements industry-standard security practices:
- Environment-based configuration (no hardcoded secrets)
- Password hashing with Django's PBKDF2
- CSRF protection
- CORS configuration
- SQL injection prevention via ORM
- XSS protection through framework defaults

See [SECURITY_README.md](SECURITY_README.md) for detailed information.

## 💼 Portfolio Project

This repository is maintained as a portfolio piece demonstrating:
- Full-stack development expertise
- Clean code architecture
- Production deployment experience
- Security best practices
- API design patterns
- Modern frontend development

## 📄 License

**Proprietary License** - This code is provided for review and evaluation purposes only.  
Commercial use, copying, or redistribution is prohibited without explicit permission.

See [LICENSE](LICENSE) for full terms.

---

**THE FINISHER™** is a trademark of MTAMBO HOLDINGS RECRUITMENT.  
© 2025-2026 MTAMBO HOLDINGS RECRUITMENT. All Rights Reserved.

For inquiries: Available upon request
