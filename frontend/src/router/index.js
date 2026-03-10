import { createRouter, createWebHashHistory } from 'vue-router'
import authService from '../services/auth'
import { systemAPI, authAPI } from '../api'
import toast from '../utils/toast'
import modal from '../utils/modal'
import LandingPage from '../components/LandingPage.vue'
import Dashboard from '../components/Dashboard.vue'
import Contacts from '../components/Contacts.vue'
import Companies from '../components/Companies.vue'
import Deals from '../components/Deals.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import VerifyOTP from '../components/VerifyOTP.vue'
import Disclaimer from '../components/Disclaimer.vue'
import HelpCenter from '../components/HelpCenter.vue'
import AdminConsole from '../components/AdminConsole.vue'
import UpgradePage from '../components/UpgradePage.vue'
import Reports from '../components/Reports.vue'
import Tickets from '../components/Tickets.vue'
import Employees from '../components/Employees.vue'
import ClientAdminConsole from '../components/ClientAdminConsole.vue'
import Settings from '../components/Settings.vue'
import Assets from '../components/Assets.vue'
import Products from '../components/Products.vue'
import EmailCampaigns from '../components/EmailCampaigns.vue'
import Workflows from '../components/Workflows.vue'
import CustomDashboard from '../components/CustomDashboard.vue'
import PrivacyPolicy from '../components/docs/PrivacyPolicy.vue'
import TermsOfService from '../components/docs/TermsOfService.vue'
import PopiaCompliance from '../components/docs/PopiaCompliance.vue'
import ApiDocs from '../components/docs/ApiDocs.vue'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { requiresAuth: false }
  },
  {
    path: '/verify-otp',
    name: 'VerifyOTP',
    component: VerifyOTP,
    meta: { requiresAuth: false }
  },
  {
    path: '/disclaimer',
    name: 'Disclaimer',
    component: Disclaimer,
    meta: { requiresAuth: false }
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy,
    meta: { requiresAuth: false }
  },
  {
    path: '/terms-of-service',
    name: 'TermsOfService',
    component: TermsOfService,
    meta: { requiresAuth: false }
  },
  {
    path: '/popia-compliance',
    name: 'PopiaCompliance',
    component: PopiaCompliance,
    meta: { requiresAuth: false }
  },
  {
    path: '/api-docs',
    name: 'ApiDocs',
    component: ApiDocs,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: Contacts,
    meta: { requiresAuth: true }
  },
  {
    path: '/companies',
    name: 'Companies',
    component: Companies,
    meta: { requiresAuth: true }
  },
  {
    path: '/deals',
    name: 'Deals',
    component: Deals,
    meta: { requiresAuth: true }
  },
  {
    path: '/help',
    name: 'Help',
    component: HelpCenter,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true }
  },
  {
    path: '/tickets',
    name: 'Tickets',
    component: Tickets,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees',
    name: 'Employees',
    component: Employees,
    meta: { requiresAuth: true }
  },
  {
    path: '/assets',
    name: 'Assets',
    component: Assets,
    meta: { requiresAuth: true }
  },
  {
    path: '/products',
    name: 'Products',
    component: Products,
    meta: { requiresAuth: true }
  },
  {
    path: '/campaigns',
    name: 'EmailCampaigns',
    component: EmailCampaigns,
    meta: { requiresAuth: true }
  },
  {
    path: '/workflows',
    name: 'Workflows',
    component: Workflows,
    meta: { requiresAuth: true }
  },
  {
    path: '/custom-dashboard',
    name: 'CustomDashboard',
    component: CustomDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/team',
    name: 'ClientAdminConsole',
    component: ClientAdminConsole,
    meta: { requiresAuth: true, requiresClientAdmin: true }
  },
  {
    path: '/admin/console',
    name: 'AdminConsole',
    component: AdminConsole,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  },
  {
    path: '/upgrade',
    redirect: '/upgrade/luxury',
    meta: { requiresAuth: true }
  },
  {
    path: '/upgrade/:plan',
    name: 'Upgrade',
    component: UpgradePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Navigation guard: Redirect to login if not authenticated and enforce prerequisites
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  let isAuthenticated = authService.isAuthenticated()

  // If authenticated but access token expired, try silent refresh before deciding
  if (isAuthenticated && authService.isAccessTokenExpired()) {
    const refreshed = await authService.tryRefresh()
    if (!refreshed) {
      isAuthenticated = false
    }
  }

  // If logged in and visiting landing, login, or register — go straight to dashboard
  if (isAuthenticated && ['/', '/login', '/register'].includes(to.path)) {
    next('/dashboard')
    return
  }

  if (requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  if (!requiresAuth) {
    next()
    return
  }

  // Restrict employee-only accounts from admin CRM sections
  const userForRole = authService.getUser()
  const isEmployeeOnly = userForRole && !userForRole.is_superuser && !userForRole.is_staff && !(
    (userForRole.permissions && userForRole.permissions.is_admin) ||
    (userForRole.role && (userForRole.role.value === 'admin' || userForRole.role === 'admin')) ||
    (userForRole.profile && userForRole.profile.role === 'admin')
  )
  if (isEmployeeOnly && ['/contacts', '/companies', '/deals'].includes(to.path)) {
    toast.warning('This section is for administrators. Your role is focused on tickets only.', 'Access Restricted')
    next('/tickets')
    return
  }

  if (to.meta.requiresAdmin) {
    let user = authService.getUser()
  const isOwnerAdmin = user?.username && user.username.toLowerCase() === 'adminluxury'
  const hasAdminAccess = Boolean(user && (user.is_superuser || isOwnerAdmin))
    if (!hasAdminAccess) {
      try {
        const response = await authAPI.getProfile()
        authService.setUser(response.data)
        user = response.data
      } catch (error) {
        console.warn('Admin verification failed:', error)
  next('/dashboard')
        return
      }
      const refreshedOwnerAdmin = user?.username && user.username.toLowerCase() === 'adminluxury'
      if (!(user && (user.is_superuser || refreshedOwnerAdmin))) {
  next('/dashboard')
        return
      }
    }
  }

  // Check if client admin access is required
  if (to.meta.requiresClientAdmin) {
    let user = authService.getUser()
    const hasClientAdminAccess = user && !user.is_superuser && !user.is_staff && (
      (user.permissions && user.permissions.is_admin) ||
      (user.role && (user.role.value === 'admin' || user.role === 'admin')) ||
      (user.profile && user.profile.role === 'admin')
    )
    
    if (!hasClientAdminAccess) {
      try {
        const response = await authAPI.getProfile()
        authService.setUser(response.data)
        user = response.data
        const refreshedClientAdmin = user && !user.is_superuser && !user.is_staff && (
          (user.permissions && user.permissions.is_admin) ||
          (user.role && (user.role.value === 'admin' || user.role === 'admin')) ||
          (user.profile && user.profile.role === 'admin')
        )
        if (!refreshedClientAdmin) {
          toast.warning('This page is for client administrators only.', 'Access Restricted')
          next('/dashboard')
          return
        }
      } catch (error) {
        console.warn('Client admin verification failed:', error)
  next('/dashboard')
        return
      }
    }
  }

  if (['/companies', '/deals'].includes(to.path)) {
    try {
      const response = await systemAPI.getPrerequisites()
      const stats = response.data || {}
      const hasContacts = (stats.contacts || 0) > 0
      const hasCompanies = (stats.companies || 0) > 0
      const hasLinkedContacts = Math.max((stats.contacts || 0) - (stats.contacts_missing_company || 0), 0) > 0

      if (to.path === '/companies' && !hasContacts) {
        toast.warning('Capture a contact first before managing company records.', 'Contact Required')
        next('/contacts')
        return
      }

      if (to.path === '/deals') {
        if (!hasContacts) {
          toast.warning('Add a contact before working with deals.', 'Contact Required')
          next('/contacts')
          return
        }
        if (!hasCompanies) {
          toast.warning('Create a company before working with deals.', 'Company Required')
          next('/companies')
          return
        }
        if (!hasLinkedContacts) {
          toast.warning('Link at least one contact to a company before creating deals.', 'Link Required')
          next('/contacts')
          return
        }
      }
    } catch (error) {
      console.warn('Prerequisite check failed - allowing navigation:', error)
    }
  }

  next()
})

export default router