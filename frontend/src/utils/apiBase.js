// Utility for determining the API base URL consistently across the app

// Hardcoded production backend — single source of truth
const PRODUCTION_BACKEND = 'https://the-finisher-luxury-be.fly.dev/api'

const ensureProtocol = (url) => {
  if (!url) return url
  // If URL doesn't start with http:// or https://, prepend https://
  if (!/^https?:\/\//i.test(url)) {
    url = `https://${url}`
  }
  return url
}

const withApiPath = (base) => {
  if (!base) return base
  base = ensureProtocol(base)
  const trimmed = base.replace(/\/$/, '')
  return trimmed.endsWith('/api') ? trimmed : `${trimmed}/api`
}

const resolveBase = () => {
  let base

  const isBrowser = typeof window !== 'undefined'
  const host = isBrowser ? window.location.hostname : ''
  const isLocalHost = host === 'localhost' || host === '127.0.0.1'

  if (isLocalHost) {
    base = 'http://localhost:8000/api'
  } else {
    // In production, ALWAYS use the hardcoded backend URL
    // VITE_API_URL is ignored in production to prevent misconfiguration
    base = PRODUCTION_BACKEND
  }

  if (isBrowser) {
    try {
      const params = new URLSearchParams(window.location.search)
      const qp = params.get('api')
      if (qp) {
        localStorage.setItem('API_BASE_OVERRIDE', qp)
      }
      const stored = localStorage.getItem('API_BASE_OVERRIDE')
      if (stored) {
        if (stored === 'local') {
          base = 'http://localhost:8000/api'
        } else if (/^https?:\/\//i.test(stored)) {
          base = withApiPath(stored)
        }
      }
    } catch (_) {
      // ignore storage errors
    }
  }

  console.log('[apiBase] Resolved API URL:', base)
  return base
}

export const API_BASE_URL = resolveBase()
export default API_BASE_URL
