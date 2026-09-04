// ═══════════════════════════════════════════════════════════════════════
// THE FINISHER LUXURY — API Base URL Resolution
// Production: Render Backend ONLY. Localhost is BLOCKED in production.
// ═══════════════════════════════════════════════════════════════════════

// Hardcoded production backend — Render Web Service
const PRODUCTION_BACKEND = 'https://the-finisher-luxury-api.onrender.com/api'

const resolveBase = () => {
  const isBrowser = typeof window !== 'undefined'
  const host = isBrowser ? window.location.hostname : ''
  const isLocalHost = host === 'localhost' || host === '127.0.0.1'

  // ─── PRODUCTION LOCKDOWN ───
  // If the app is running from a production domain, ALWAYS use the production backend.
  // Localhost override is IMPOSSIBLE from production — zero-trust security.
  if (!isLocalHost) {
    return PRODUCTION_BACKEND
  }

  // ─── LOCAL DEVELOPMENT ONLY ───
  // Only reachable when running on localhost during development
  return 'http://localhost:8000/api'
}

// ─── BACKEND WARM-UP ───
// Silently ping the health endpoint on app load to wake Render from cold start.
// This ensures the backend is ready BEFORE the user submits any form.
export function warmUpBackend() {
  try {
    const base = PRODUCTION_BACKEND.replace(/\/api$/, '')
    fetch(`${base}/health/`, {
      method: 'GET',
      mode: 'cors',
      cache: 'no-store',
      signal: AbortSignal.timeout(15000) // 15 second max
    }).then(res => {
      if (res.ok) {
        console.log('[WarmUp] Backend is awake and ready ✓')
      }
    }).catch(() => {
      // Silent fail — this is just a warm-up, not critical
      console.log('[WarmUp] Backend warming up...')
    })
  } catch (_) {
    // Ignore errors in environments where fetch/AbortSignal isn't available
  }
}

export const API_BASE_URL = resolveBase()
export default API_BASE_URL
