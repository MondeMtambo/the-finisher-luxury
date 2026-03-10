# The Completer CRM - Development Guidelines

## Code Quality Standards

### Documentation Standards
- **Docstrings**: Use triple-quoted strings for module and function documentation
- **Inline Comments**: Include Django-standard comments with URLs to official documentation
- **File Headers**: Include descriptive headers explaining file purpose and Django version context

### Python/Django Conventions
- **Import Organization**: Standard library imports first, then Django imports, then local imports
- **Path Handling**: Use `pathlib.Path` for file system operations instead of `os.path`
- **Settings Structure**: Follow Django's default settings.py organization with clear section comments
- **Environment Variables**: Use `os.environ.setdefault()` for Django settings module configuration

### JavaScript/Vue.js Conventions  
- **ES6+ Syntax**: Use modern JavaScript features (import/export, const/let)
- **Module System**: Use ES6 modules with explicit imports
- **Configuration**: Use object destructuring and modern syntax in config files

## Structural Conventions

### Django Project Structure
- **Project vs App Separation**: Main project (`completer_api`) contains global settings, individual apps (`crm`) contain business logic
- **URL Configuration**: Keep main `urls.py` minimal, delegate to app-specific URL configs
- **Settings Organization**: Group related settings with descriptive comments and Django documentation links

### Frontend Architecture
- **Component Structure**: Single File Components (.vue) for Vue.js
- **Build Configuration**: Use Vite with Vue plugin for modern build tooling
- **Development Server**: Configure custom ports (3000 for frontend)

## Configuration Patterns

### Django Settings Patterns
```python
# Use pathlib for path construction
BASE_DIR = Path(__file__).resolve().parent.parent

# Group related settings with comments
# Application definition
INSTALLED_APPS = [
    # Django core apps first
    'django.contrib.admin',
    # Custom apps last
]

# Include documentation references
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
```

### Vite Configuration Pattern
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000  // Custom development port
  }
})
```

### Vue.js Bootstrap Pattern
```javascript
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

## Security Practices

### Django Security
- **Secret Key Management**: Use environment variables for production (currently hardcoded for development)
- **Debug Mode**: Set `DEBUG = True` only for development
- **Allowed Hosts**: Configure appropriately for deployment environment

### Development vs Production
- **Database**: SQLite for development, PlanetScale MySQL for production
- **Static Files**: Standard Django static file handling
- **CORS**: Configure django-cors-headers for API access

## Error Handling Patterns

### Django Management Commands
```python
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc
```

## Development Workflow

### File Organization
- **Backend**: Separate Django project and apps with clear responsibility boundaries
- **Frontend**: Minimal structure with main.js as entry point and App.vue as root component
- **Configuration**: Keep build and development configs at project root level

### Naming Conventions
- **Python**: Snake_case for variables, PascalCase for classes
- **JavaScript**: camelCase for variables, PascalCase for components
- **Files**: Lowercase with underscores for Python, camelCase for JavaScript

### Import Patterns
- **Absolute Imports**: Use full module paths in Django
- **Relative Imports**: Use relative imports for Vue components
- **Third-party First**: Import external libraries before local modules