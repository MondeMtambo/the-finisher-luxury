import axios from 'axios'
import authService from '../services/auth'
import router from '../router'
import API_BASE_URL from '../utils/apiBase'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 120 seconds — Render free tier cold starts can take 60s+
  headers: {
    'Content-Type': 'application/json',
  }
})

// ─── Server Wake-Up Banner ───
// Shows a non-blocking notification when the backend is waking from cold start
let _wakeUpBanner = null
function showWakeUpBanner() {
  if (_wakeUpBanner) return
  _wakeUpBanner = document.createElement('div')
  _wakeUpBanner.id = 'render-wakeup-banner'
  _wakeUpBanner.innerHTML = '⏳ Server is warming up — please wait a moment...'
  Object.assign(_wakeUpBanner.style, {
    position: 'fixed', top: '0', left: '0', right: '0', zIndex: '99999',
    padding: '10px 20px', textAlign: 'center', fontWeight: '700',
    fontSize: '0.85rem', letterSpacing: '0.5px',
    background: 'linear-gradient(90deg, #d4af37 0%, #f5d76e 50%, #d4af37 100%)',
    color: '#1a1a2e', boxShadow: '0 2px 12px rgba(212,175,55,0.4)',
    animation: 'slideDown 0.3s ease-out'
  })
  document.body.appendChild(_wakeUpBanner)
}
function hideWakeUpBanner() {
  if (_wakeUpBanner) {
    _wakeUpBanner.remove()
    _wakeUpBanner = null
  }
}

// ─── Intelligent Retry Logic for Render Cold Starts ───
// Supabase DB never sleeps — but Render free tier backend can cold start.
// 3 retries with exponential backoff (5s, 10s, 15s) = 30s total patience.
const MAX_RETRIES = 3
const RETRY_DELAY_MS = 5000

function isRetryable(error) {
  // Retry on network errors, timeouts, and 502/503/504 (Render waking up)
  if (!error.response) return true // network error / timeout
  const status = error.response.status
  return status === 502 || status === 503 || status === 504
}

api.interceptors.request.use(config => {
  if (!config._retryCount) config._retryCount = 0
  return config
})

// Wrap the response interceptor to add retry before other handling
const retryInterceptor = async (error) => {
  const config = error.config
  if (!config || !isRetryable(error) || config._retryCount >= MAX_RETRIES) {
    hideWakeUpBanner()
    return Promise.reject(error)
  }

  config._retryCount += 1
  showWakeUpBanner()

  // Exponential backoff: 5s, 10s, 15s
  await new Promise(r => setTimeout(r, RETRY_DELAY_MS * config._retryCount))

  return api(config)
}

// Insert retry interceptor FIRST (runs before auth refresh interceptor)
api.interceptors.response.use(response => {
  hideWakeUpBanner()
  return response
}, retryInterceptor)

// Request interceptor: Add JWT token to every request
api.interceptors.request.use(
  config => {
    // Do NOT attach token to public auth endpoints
    const publicAuthPaths = [
      '/auth/login/',
      '/auth/register/',
      '/auth/refresh/',
      '/auth/verify-mfa/',
      '/auth/password-reset/',
      '/auth/password-reset-confirm/',
      '/public/request-access/',
      '/public/verify-access-request/',
      '/public/cancel-access-request/',
      '/public/search-ceo/',
      '/public/leads/'
    ]
    const isPublicAuth = publicAuthPaths.some(p => (config.url || '').includes(p))

    if (!isPublicAuth) {
      const token = authService.getAccessToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor: Handle token refresh and errors
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      // If user is already on a public view (register, login, forgot-password, disclaimer)
      // or calling a public endpoint, NEVER force redirect to /login!
      const currentLoc = (typeof window !== 'undefined') ? (window.location.hash + window.location.pathname) : ''
      const isPublicLocation = ['register', 'login', 'forgot-password', 'disclaimer'].some(p => currentLoc.includes(p))
      const isPublicEndpoint = (originalRequest.url || '').includes('/public/')

      if (isPublicLocation || isPublicEndpoint) {
        return Promise.reject(error)
      }

      // Don't immediately logout on first 401 - might be a timing issue
      // Only try refresh if we have a refresh token
      const refreshToken = authService.getRefreshToken()
      
      if (!refreshToken) {
        // No refresh token at all, redirect to login
        authService.clearAuth()
        router.push('/login')
        return Promise.reject(error)
      }

      if (isRefreshing) {
        // Queue requests while refreshing
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // Try to refresh the token
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken
        })

        const newAccessToken = response.data.access
        authService.updateAccessToken(newAccessToken)

        processQueue(null, newAccessToken)
        isRefreshing = false

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return api(originalRequest)

      } catch (refreshError) {
        // Refresh failed, logout user
        processQueue(refreshError, null)
        isRefreshing = false
        authService.clearAuth()
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }

    // Handle other errors
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      // Extract error message (also flatten field errors)
      let message = 'An error occurred'
      if (data?.error) {
        message = data.error
      } else if (data?.detail) {
        message = data.detail
      } else if (data?.message) {
        message = data.message
      } else if (typeof data === 'string') {
        message = data
      } else if (Array.isArray(data?.non_field_errors)) {
        message = data.non_field_errors.join(', ')
      } else if (data && typeof data === 'object') {
        try {
          const parts = []
          Object.entries(data).forEach(([k, v]) => {
            if (Array.isArray(v)) parts.push(`${k}: ${v.join(' ')}`)
            else if (typeof v === 'string') parts.push(`${k}: ${v}`)
          })
          if (parts.length) message = parts.join('\n')
        } catch (_) {}
      }

      error.message = message
    } else if (error.request) {
      error.message = 'Unable to reach the server. Please check your connection or try again.'
    }

    return Promise.reject(error)
  }
)

// Authentication API
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  verifyMFA: (data) => api.post('/auth/verify-mfa/', data),
  forceChangePassword: (data) => api.post('/auth/force-change-password/', data),
  refresh: (refreshToken) => api.post('/auth/refresh/', { refresh: refreshToken }),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.put('/auth/profile/', data),
  changePassword: (data) => api.post('/auth/change-password/', data),
  // OTP-based password reset
  passwordResetRequest: (email) => api.post('/auth/password-reset/', { email }),
  verifyOTP: (email, otp_code) => api.post('/auth/password-reset/verify-otp/', { email, otp_code }),
  passwordResetConfirm: (data) => api.post('/auth/password-reset-confirm/', data),
}

export const contactsAPI = {
  getAll: () => api.get('/contacts/'),
  create: (data, config = {}) => api.post('/contacts/', data, config),
  update: (id, data, config = {}) => api.put(`/contacts/${id}/`, data, config),
  delete: (id) => api.delete(`/contacts/${id}/`),
  importCSV: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/contacts/import_csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export const companiesAPI = {
  getAll: () => api.get('/companies/'),
  create: (data) => api.post('/companies/', data),
  update: (id, data) => api.put(`/companies/${id}/`, data),
  delete: (id) => api.delete(`/companies/${id}/`)
}

export const dealsAPI = {
  getAll: () => api.get('/deals/'),
  create: (data) => api.post('/deals/', data),
  update: (id, data) => api.put(`/deals/${id}/`, data),
  delete: (id) => api.delete(`/deals/${id}/`),
  startTimer: (id) => api.post(`/deals/${id}/start_timer/`),
  stopTimer: (id) => api.post(`/deals/${id}/stop_timer/`)
}

export const activitiesAPI = {
  getAll: () => api.get('/activities/')  // FREE tier: last 5 only
}

export const ticketsAPI = {
  getAll: () => api.get('/tickets/'),
  create: (data) => api.post('/tickets/', data),
  update: (id, data) => api.put(`/tickets/${id}/`, data),
  delete: (id) => api.delete(`/tickets/${id}/`),
  start: (id) => api.post(`/tickets/${id}/start/`),
  stop: (id) => api.post(`/tickets/${id}/stop/`),
  complete: (id) => api.post(`/tickets/${id}/complete/`)
}

export const notificationsAPI = {
  getAll: (params = {}) => api.get('/notifications/', { params }),
  create: (data) => api.post('/notifications/', data),
  markRead: (id) => api.post(`/notifications/${id}/mark_read/`),
  delete: (id) => api.delete(`/notifications/${id}/`)
}

export const performanceAPI = {
  getMine: () => api.get('/performance/me/'),
  getForUser: (userId) => api.get(`/performance/user/${userId}/`)
}

export const systemAPI = {
  getPrerequisites: () => api.get('/prerequisites/'),
  getAdminOverview: () => api.get('/admin/overview/'),
  getWebsiteLeadInbox: (params = {}) => api.get('/admin/website-leads/inbox/', { params }),
  getUserManagement: () => api.get('/admin/users/'),
  getClientsEmployees: () => api.get('/admin/clients-employees/'),
  banUser: (userId, reason) => api.post('/admin/users/', { action: 'ban', user_id: userId, reason }),
  unbanUser: (userId) => api.post('/admin/users/', { action: 'unban', user_id: userId }),
  updatePaymentStatus: (userId, paymentStatus) => api.post('/admin/users/', { action: 'update_payment', user_id: userId, payment_status: paymentStatus }),
  deleteUser: (userId, deleteReason) => api.post('/admin/users/', { action: 'delete', user_id: userId, delete_reason: deleteReason }),
  resetUserPassword: (userId) => api.post('/admin/clients-employees/', { action: 'reset_password', user_id: userId }),
  toggleUserActive: (userId) => api.post('/admin/clients-employees/', { action: 'toggle_active', user_id: userId }),
  banClient: (userId, reason) => api.post('/admin/clients-employees/', { action: 'ban', user_id: userId, reason }),
  unbanClient: (userId) => api.post('/admin/clients-employees/', { action: 'unban', user_id: userId })
}

export const websiteLeadsAPI = {
  getAll: (params = {}) => api.get('/website-leads/', { params }),
  updateWorkflow: (id, data) => api.post(`/website-leads/${id}/update_workflow/`, data),
  reply: (id, data) => api.post(`/website-leads/${id}/reply/`, data)
}

export const employeesAPI = {
  getAll: () => api.get('/employees/'),
  getById: (id) => api.get(`/employees/${id}/`),
  create: (data) => api.post('/employees/', data),
  update: (id, data) => api.put(`/employees/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/employees/${id}/`, data),
  delete: (id) => api.delete(`/employees/${id}/`),
  getAvailableSlots: () => api.get('/employees/available_slots/'),
  // ADMP Employee Directory
  getOnboardingLogs: (params = {}) => api.get('/employees/onboarding_logs/', { params }),
  getOffboardingRequests: (params = {}) => api.get('/employees/offboarding_requests/', { params }),
  requestOffboarding: (data) => api.post('/employees/offboarding_requests/', data),
  processOffboarding: (data) => api.post('/employees/process_offboarding/', data),
  getOrgChart: () => api.get('/employees/org_chart/'),
}

// ============================================================================
// ADMP (Asset & Data Management Platform) API
// ============================================================================

export const assetsAPI = {
  getAll: (params = {}) => api.get('/assets/', { params }),
  getById: (id) => api.get(`/assets/${id}/`),
  create: (data) => api.post('/assets/', data),
  update: (id, data) => api.put(`/assets/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/assets/${id}/`, data),
  delete: (id) => api.delete(`/assets/${id}/`),
  getStats: () => api.get('/assets/stats/'),
  assign: (id, employeeId) => api.post(`/assets/${id}/assign/`, { employee_id: employeeId }),
  unassign: (id) => api.post(`/assets/${id}/unassign/`)
}

export const assetCategoriesAPI = {
  getAll: () => api.get('/asset-categories/'),
  getById: (id) => api.get(`/asset-categories/${id}/`),
  create: (data) => api.post('/asset-categories/', data),
  update: (id, data) => api.put(`/asset-categories/${id}/`, data),
  delete: (id) => api.delete(`/asset-categories/${id}/`),
  seedDefaults: () => api.post('/asset-categories/seed_defaults/')
}

export const divisionsAPI = {
  getAll: () => api.get('/divisions/'),
  getById: (id) => api.get(`/divisions/${id}/`),
  create: (data) => api.post('/divisions/', data),
  update: (id, data) => api.put(`/divisions/${id}/`, data),
  delete: (id) => api.delete(`/divisions/${id}/`)
}

// ============================================================================
// LUXURY Phase 1: Product Catalog & Line Items
// ============================================================================

export const productsAPI = {
  getAll: (params = {}) => api.get('/products/', { params }),
  getById: (id) => api.get(`/products/${id}/`),
  create: (data) => api.post('/products/', data),
  update: (id, data) => api.put(`/products/${id}/`, data),
  delete: (id) => api.delete(`/products/${id}/`)
}

export const lineItemsAPI = {
  getAll: (params = {}) => api.get('/line-items/', { params }),
  getById: (id) => api.get(`/line-items/${id}/`),
  create: (data) => api.post('/line-items/', data),
  update: (id, data) => api.put(`/line-items/${id}/`, data),
  delete: (id) => api.delete(`/line-items/${id}/`),
  getDealSummary: (dealId) => api.get(`/line-items/deal-summary/${dealId}/`)
}

// ============================================================================
// LUXURY Phase 1: Email Campaigns
// ============================================================================

export const emailTemplatesAPI = {
  getAll: () => api.get('/email-templates/'),
  getById: (id) => api.get(`/email-templates/${id}/`),
  create: (data) => api.post('/email-templates/', data),
  update: (id, data) => api.put(`/email-templates/${id}/`, data),
  delete: (id) => api.delete(`/email-templates/${id}/`)
}

export const emailCampaignsAPI = {
  getAll: () => api.get('/email-campaigns/'),
  getById: (id) => api.get(`/email-campaigns/${id}/`),
  create: (data) => api.post('/email-campaigns/', data),
  update: (id, data) => api.put(`/email-campaigns/${id}/`, data),
  delete: (id) => api.delete(`/email-campaigns/${id}/`),
  send: (id) => api.post(`/email-campaigns/${id}/send/`),
  getRecipients: (id) => api.get(`/email-campaigns/${id}/recipients/`),
  trackOpen: (id, recipientId) => api.post(`/email-campaigns/${id}/track-open/`, { recipient_id: recipientId }),
  trackClick: (id, recipientId) => api.post(`/email-campaigns/${id}/track-click/`, { recipient_id: recipientId })
}

// ============================================================================
// LUXURY Phase 1: Workflow Automation
// ============================================================================

export const workflowsAPI = {
  getAll: () => api.get('/workflows/'),
  getById: (id) => api.get(`/workflows/${id}/`),
  create: (data) => api.post('/workflows/', data),
  update: (id, data) => api.put(`/workflows/${id}/`, data),
  delete: (id) => api.delete(`/workflows/${id}/`),
  toggle: (id) => api.post(`/workflows/${id}/toggle/`),
  addAction: (id, data) => api.post(`/workflows/${id}/add-action/`, data),
  removeAction: (id, actionId) => api.post(`/workflows/${id}/remove-action/`, { action_id: actionId }),
  getLogs: (id) => api.get(`/workflows/${id}/logs/`)
}

// ============================================================================
// LUXURY Phase 1: Custom Dashboard
// ============================================================================

export const dashboardWidgetsAPI = {
  getAll: () => api.get('/dashboard-widgets/'),
  getById: (id) => api.get(`/dashboard-widgets/${id}/`),
  create: (data) => api.post('/dashboard-widgets/', data),
  update: (id, data) => api.put(`/dashboard-widgets/${id}/`, data),
  delete: (id) => api.delete(`/dashboard-widgets/${id}/`),
  reorder: (widgets) => api.post('/dashboard-widgets/reorder/', { widgets }),
  resetDefaults: () => api.post('/dashboard-widgets/reset-defaults/'),
  getWidgetData: (type) => api.get(`/dashboard-widgets/widget-data/${type}/`)
}

export const dashboardLayoutsAPI = {
  getAll: () => api.get('/dashboard-layouts/'),
  create: (data) => api.post('/dashboard-layouts/', data),
  update: (id, data) => api.put(`/dashboard-layouts/${id}/`, data),
  delete: (id) => api.delete(`/dashboard-layouts/${id}/`)
}

export const verificationAPI = {
  getStatus: () => api.get('/tenant/verification/'),
  submit: (formData) => api.post('/tenant/verification/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  adminGetAll: () => api.get('/admin/tenant-verifications/'),
  adminReview: (id, data) => api.post(`/admin/tenant-verifications/${id}/review/`, data)
}

export const accessRequestsAPI = {
  submitPublic: (data) => api.post('/public/request-access/', data),
  verifyPublic: (data) => api.post('/public/verify-access-request/', data),
  cancelPublic: (id) => api.delete(`/public/cancel-access-request/${id}/`),
  searchCEO: (query) => api.get('/public/search-ceo/', { params: { q: query } }),
  adminGetAll: () => api.get('/admin/access-requests/'),
  adminAction: (id, action, notes = '', rejectionReason = '') =>
    api.post(`/admin/access-requests/${id}/action/`, { action, notes, rejection_reason: rejectionReason })
}

export default api