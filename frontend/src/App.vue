<template>
  <div id="app" :class="{ 'has-sidebar': showSidebar }">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <ToastNotifications />
    <ConfirmModal />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import ToastNotifications from './components/ToastNotifications.vue'
import ConfirmModal from './components/ConfirmModal.vue'
import authService from './services/auth'

export default {
  name: 'App',
  components: {
    Navbar,
    ToastNotifications,
    ConfirmModal
  },
  computed: {
    showSidebar() {
      const publicPages = ['/login', '/register', '/forgot-password', '/verify-otp', '/']
      return authService.isAuthenticated() && !publicPages.includes(this.$route.path)
    }
  }
}
</script>

<style>
/* ═══════════════════════════════════════════════════════════
   CORPORATE CLEAN DESIGN SYSTEM — THE FINISHER CRM
   Professional, structured, polished — HubSpot/Salesforce style
   ═══════════════════════════════════════════════════════════ */

:root {
  /* Primary Blues */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-300: #93c5fd;
  --primary-400: #60a5fa;
  --primary-500: #2563eb;
  --primary-600: #1d4ed8;
  --primary-700: #1e40af;
  --primary-800: #1e3a8a;
  --primary-900: #172554;

  /* Neutrals */
  --gray-25: #fcfcfd;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;

  /* Accents */
  --green-500: #22c55e;
  --green-600: #16a34a;
  --green-50: #f0fdf4;
  --red-500: #ef4444;
  --red-600: #dc2626;
  --red-50: #fef2f2;
  --amber-500: #f59e0b;
  --amber-50: #fffbeb;
  --purple-500: #8b5cf6;
  --purple-50: #f5f3ff;

  /* Layout */
  --sidebar-width: 240px;
  --sidebar-collapsed-width: 64px;
  --sidebar-current-width: var(--sidebar-width);
  --topbar-height: 56px;
  --content-max-width: 1400px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);

  /* Borders */
  --border-color: #e5e7eb;
  --border-radius: 8px;
  --border-radius-sm: 6px;
  --border-radius-lg: 12px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--gray-50);
  color: var(--gray-800);
  min-height: 100vh;
  overflow-x: hidden;
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

#app {
  min-height: 100vh;
}

/* When sidebar is active, offset for fixed topbar + sidebar */
#app.has-sidebar {
  padding-top: var(--topbar-height);
  padding-left: var(--sidebar-current-width);
}

/* Main content area */
.main-content {
  padding: 24px 32px;
  min-height: calc(100vh - var(--topbar-height));
  background: var(--gray-50);
  overflow-x: hidden;
}

/* When no sidebar (login/register pages) */
#app:not(.has-sidebar) .main-content {
  padding: 0;
}

/* ─── Typography ─── */
h1 { font-size: 24px; font-weight: 700; color: var(--gray-900); letter-spacing: -0.025em; }
h2 { font-size: 20px; font-weight: 600; color: var(--gray-800); letter-spacing: -0.02em; }
h3 { font-size: 16px; font-weight: 600; color: var(--gray-800); }
h4 { font-size: 14px; font-weight: 600; color: var(--gray-700); }

/* ─── Common Card Style ─── */
.card {
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-xs);
}

/* ─── Common Button Styles ─── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
  line-height: 1.4;
}
.btn-primary { background: var(--primary-500); color: #fff; }
.btn-primary:hover { background: var(--primary-600); box-shadow: var(--shadow-sm); }
.btn-secondary { background: #fff; color: var(--gray-700); border: 1px solid var(--border-color); }
.btn-secondary:hover { background: var(--gray-50); border-color: var(--gray-300); }
.btn-danger { background: var(--red-500); color: #fff; }
.btn-danger:hover { background: var(--red-600); }
.btn-success { background: var(--green-500); color: #fff; }
.btn-success:hover { background: var(--green-600); }
.btn-sm { padding: 6px 12px; font-size: 13px; }
.btn-lg { padding: 10px 20px; font-size: 15px; }

/* ─── Common Form Styles ─── */
.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  color: var(--gray-800);
  background: #fff;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  outline: none;
}
.form-input:focus, .form-select:focus, .form-textarea:focus {
  border-color: var(--primary-400);
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}
.form-input::placeholder { color: var(--gray-400); }
.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--gray-600);
  margin-bottom: 4px;
}

/* ─── Badge ─── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.4;
}
.badge-blue { background: var(--primary-50); color: var(--primary-700); }
.badge-green { background: var(--green-50); color: var(--green-600); }
.badge-red { background: var(--red-50); color: var(--red-600); }
.badge-amber { background: var(--amber-50); color: #b45309; }
.badge-gray { background: var(--gray-100); color: var(--gray-600); }

/* ─── Table ─── */
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
}
.data-table thead th {
  background: var(--gray-50);
  border-bottom: 1px solid var(--border-color);
  padding: 10px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--gray-500);
  white-space: nowrap;
}
.data-table tbody td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--gray-100);
  color: var(--gray-700);
}
.data-table tbody tr:hover {
  background: var(--gray-25);
}
.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* ─── Page Header ─── */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}
.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-900);
}
.page-header .subtitle {
  font-size: 14px;
  color: var(--gray-500);
  margin-top: 2px;
}

/* ─── Empty State ─── */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--gray-400);
}
.empty-state .empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}
.empty-state h3 {
  color: var(--gray-600);
  margin-bottom: 8px;
}
.empty-state p {
  color: var(--gray-400);
  max-width: 400px;
  margin: 0 auto 20px;
}

/* ─── Modal Overlay ─── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}
.modal-panel {
  background: #fff;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 560px;
  max-height: 85vh;
  overflow-y: auto;
}
.modal-header {
  padding: 20px 24px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.modal-header h2 {
  font-size: 18px;
  font-weight: 600;
}
.modal-body { padding: 20px 24px; }
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* ─── Loading Spinner ─── */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--gray-200);
  border-top-color: var(--primary-500);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Responsive ─── */
@media (max-width: 1280px) {
  :root {
    --content-max-width: 100%;
  }
}

@media (max-width: 1024px) {
  .main-content {
    padding: 20px 16px;
  }
}

@media (max-width: 768px) {
  :root {
    --sidebar-current-width: 0px;
  }
  #app.has-sidebar {
    padding-left: 0;
  }
  .main-content {
    padding: 16px 12px;
  }
  .page-header { 
    flex-direction: column; 
    align-items: flex-start; 
  }
  h1 { font-size: 20px; }
  h2 { font-size: 18px; }
}

@media (max-width: 640px) {
  .main-content {
    padding: 12px 8px;
  }
  .card {
    border-radius: 8px;
  }
}
</style>