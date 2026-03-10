# The Completer CRM - Project Structure

## Root Directory Structure
```
the-completer-crm/
├── backend/          # Django REST API server
├── frontend/         # Vue.js client application  
├── docs/            # Project documentation
├── .amazonq/        # AI assistant rules and memory bank
├── .gitignore       # Git ignore patterns
└── README.md        # Project overview and setup
```

## Backend Architecture (Django)
```
backend/
├── completer_api/           # Main Django project
│   ├── __init__.py         # Python package marker
│   ├── asgi.py            # ASGI configuration for async
│   ├── settings.py        # Django settings and configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration for deployment
├── crm/                    # Core CRM Django app
│   ├── migrations/         # Database migration files
│   │   └── __init__.py    # Migration package marker
│   ├── __init__.py        # App package marker
│   ├── admin.py           # Django admin interface config
│   ├── apps.py            # App configuration
│   ├── models.py          # Database models (Contact, Company, Deal)
│   ├── tests.py           # Unit tests
│   └── views.py           # API endpoints and business logic
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Frontend Architecture (Vue.js)
```
frontend/
├── src/                    # Source code
│   ├── App.vue            # Root Vue component
│   └── main.js            # Application entry point
├── index.html             # HTML template
├── package.json           # Node.js dependencies and scripts
└── vite.config.js         # Vite build configuration
```

## Core Components & Relationships

### Backend Components
- **completer_api/**: Main Django project containing global settings and URL routing
- **crm/**: Core business logic app handling contacts, companies, deals, and activities
- **models.py**: Defines database schema for CRM entities
- **views.py**: REST API endpoints serving frontend requests
- **settings.py**: Configuration for database, CORS, authentication

### Frontend Components  
- **main.js**: Vue application bootstrap with router and HTTP client setup
- **App.vue**: Root component managing global layout and routing
- **Vite**: Modern build tool for fast development and optimized production builds

## Architectural Patterns

### API-First Architecture
- Backend serves as pure REST API
- Frontend consumes API endpoints
- Clear separation of concerns between client and server

### Django App Structure
- Single `crm` app contains all business logic
- Models represent core CRM entities (Contact, Company, Deal, Activity)
- Views handle API endpoints with DRF (Django REST Framework)

### Vue.js SPA Pattern
- Single Page Application with client-side routing
- Component-based architecture
- Axios for HTTP communication with backend

## Development Environment
- **Backend**: Django development server on localhost
- **Frontend**: Vite dev server with hot reload
- **Database**: PlanetScale MySQL (cloud-hosted)
- **Deployment**: Vercel for both frontend and backend