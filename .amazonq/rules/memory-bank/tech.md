# The Completer CRM - Technology Stack

## Programming Languages
- **Python 3.x** - Backend development with Django
- **JavaScript ES6+** - Frontend development with Vue.js
- **HTML5** - Markup and structure
- **CSS3** - Styling and responsive design

## Backend Technology Stack

### Core Framework
- **Django 5.0.4** - Python web framework
- **Django REST Framework 3.16.1** - API development toolkit

### Dependencies
- **django-cors-headers 4.9.0** - Cross-Origin Resource Sharing support
- **python-decouple 3.8** - Environment variable management

### Database
- **PlanetScale** - MySQL-compatible serverless database (5GB free tier)
- **MySQL** - Relational database system

## Frontend Technology Stack

### Core Framework
- **Vue.js 3.4.0** - Progressive JavaScript framework
- **Vue Router 4.2.0** - Client-side routing

### Build Tools
- **Vite 5.0.0** - Fast build tool and dev server
- **@vitejs/plugin-vue 5.0.0** - Vue.js plugin for Vite

### HTTP Client
- **Axios 1.6.0** - Promise-based HTTP client

## Development Commands

### Backend Commands
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Frontend Commands
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment Platform
- **Vercel** - Serverless deployment platform
  - Frontend: Static site deployment
  - Backend: Serverless functions
  - 100% free hosting solution

## Development Environment
- **Node.js** - JavaScript runtime for frontend tooling
- **Python** - Backend runtime environment
- **Git** - Version control system
- **GitHub** - Code repository hosting

## Configuration Files
- **package.json** - Node.js project configuration and dependencies
- **requirements.txt** - Python dependencies
- **vite.config.js** - Vite build configuration
- **settings.py** - Django project settings
- **.gitignore** - Git ignore patterns

## Database Configuration
- **PlanetScale MySQL** - Cloud database service
- **Connection via environment variables** - Secure credential management
- **Django ORM** - Database abstraction layer