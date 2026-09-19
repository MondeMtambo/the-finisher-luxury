/**
 * Authentication Service for THE FINISHER CRM
 * Handles JWT token storage, refresh, and auth state
 */

import { reactive } from 'vue'
import axios from 'axios'
import API_BASE_URL from '../utils/apiBase'

const TOKEN_KEY = 'thefinisher_access_token'
const REFRESH_KEY = 'thefinisher_refresh_token'
const USER_KEY = 'thefinisher_user'
const LOGIN_TIME_KEY = 'thefinisher_login_time'

// Maximum session duration (8 hours) — forces re-login for security
const MAX_SESSION_MS = 8 * 60 * 60 * 1000

function getStoredUser() {
  try {
    const raw = typeof window !== 'undefined' ? localStorage.getItem(USER_KEY) : null
    return raw ? JSON.parse(raw) : null
  } catch (_) {
    return null
  }
}

function hasValidToken() {
  if (typeof window === 'undefined') return false
  const token = localStorage.getItem(TOKEN_KEY)
  if (!token) return false
  const loginTime = localStorage.getItem(LOGIN_TIME_KEY)
  if (loginTime) {
    const elapsed = Date.now() - parseInt(loginTime, 10)
    if (elapsed > MAX_SESSION_MS) return false
  }
  return true
}

export const authState = reactive({
  token: typeof window !== 'undefined' ? localStorage.getItem(TOKEN_KEY) : null,
  user: getStoredUser(),
  isAuthenticated: hasValidToken()
})

export default {
  authState,

  /**
   * Login user and store tokens
   */
  async login(username, password) {
    const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
      username,
      password
    })
    
    const { access, refresh, user } = response.data
    
    // Store tokens and login timestamp
    localStorage.setItem(TOKEN_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
    localStorage.setItem(LOGIN_TIME_KEY, Date.now().toString())
    
    const resolvedUser = user || { username }
    // Store user info if available from login response
    localStorage.setItem(USER_KEY, JSON.stringify(resolvedUser))
    localStorage.setItem('user', JSON.stringify(resolvedUser))

    // Update reactive state immediately
    authState.token = access
    authState.user = resolvedUser
    authState.isAuthenticated = true
    
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tfl-auth-changed', { detail: resolvedUser }))
    }
    
    return response.data
  },

  /**
   * Check if user is authenticated (has token + session not expired)
   */
  isAuthenticated() {
    const token = this.getAccessToken()
    if (!token) {
      if (authState.isAuthenticated) authState.isAuthenticated = false
      return false
    }

    // Check if session has exceeded maximum duration
    const loginTime = localStorage.getItem(LOGIN_TIME_KEY)
    if (loginTime) {
      const elapsed = Date.now() - parseInt(loginTime, 10)
      if (elapsed > MAX_SESSION_MS) {
        // Session expired — clear everything
        this.clearAuth()
        return false
      }
    }

    if (!authState.isAuthenticated) {
      authState.isAuthenticated = true
      authState.token = token
    }
    return authState.isAuthenticated
  },

  /**
   * Check if the access token JWT is expired (client-side decode)
   */
  isAccessTokenExpired() {
    const token = this.getAccessToken()
    if (!token) return true
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp ? payload.exp * 1000 < Date.now() : false
    } catch (_) {
      return true
    }
  },

  /**
   * Try to silently refresh the access token. Returns true on success.
   */
  async tryRefresh() {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) return false
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
        refresh: refreshToken
      })
      this.updateAccessToken(response.data.access)
      // If server rotated the refresh token, store the new one
      if (response.data.refresh) {
        localStorage.setItem(REFRESH_KEY, response.data.refresh)
      }
      return true
    } catch (_) {
      this.clearAuth()
      return false
    }
  },

  /**
   * Get access token from localStorage
   */
  getAccessToken() {
    return authState.token || localStorage.getItem(TOKEN_KEY)
  },

  /**
   * Get refresh token from localStorage
   */
  getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY)
  },

  /**
   * Get user data from localStorage
   */
  getUser() {
    if (authState.user) return authState.user
    const userStr = localStorage.getItem(USER_KEY)
    const user = userStr ? JSON.parse(userStr) : null
    if (user && !authState.user) authState.user = user
    return user
  },

  /**
   * Get current user with permissions
   */
  getCurrentUser() {
    return this.getUser()
  },

  setUser(user) {
    if (user) {
      const serialized = JSON.stringify(user)
      localStorage.setItem(USER_KEY, serialized)
      localStorage.setItem('user', serialized)
      authState.user = user
      if (authState.token) authState.isAuthenticated = true
    } else {
      localStorage.removeItem(USER_KEY)
      localStorage.removeItem('user')
      authState.user = null
    }
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tfl-auth-changed', { detail: user }))
    }
  },

  /**
   * Save tokens and user data after login/register
   */
  saveAuth(tokens, user) {
    localStorage.setItem(TOKEN_KEY, tokens.access)
    localStorage.setItem(REFRESH_KEY, tokens.refresh)
    localStorage.setItem(LOGIN_TIME_KEY, Date.now().toString())
    const serialized = JSON.stringify(user)
    localStorage.setItem(USER_KEY, serialized)
    localStorage.setItem('user', serialized)
    authState.token = tokens.access
    authState.user = user
    authState.isAuthenticated = true
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tfl-auth-changed', { detail: user }))
    }
  },

  /**
   * Set tokens after MFA verification (without user data initially)
   */
  setTokens(access, refresh) {
    localStorage.setItem(TOKEN_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
    localStorage.setItem(LOGIN_TIME_KEY, Date.now().toString())
    authState.token = access
    authState.isAuthenticated = true
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tfl-auth-changed', { detail: authState.user }))
    }
  },

  /**
   * Update only access token (after refresh)
   */
  updateAccessToken(token) {
    localStorage.setItem(TOKEN_KEY, token)
    authState.token = token
    authState.isAuthenticated = true
  },

  /**
   * Clear all auth data (logout)
   */
  clearAuth() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem('user')
    localStorage.removeItem(LOGIN_TIME_KEY)
    authState.token = null
    authState.user = null
    authState.isAuthenticated = false
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tfl-auth-changed', { detail: null }))
    }
  },

  /**
   * Logout user
   */
  async logout() {
    try {
      // Call backend logout endpoint (optional - blacklists refresh token)
      const refreshToken = this.getRefreshToken()
      if (refreshToken) {
        await axios.post(`${API_BASE_URL}/auth/logout/`, {
          refresh: refreshToken
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Always clear auth data even if API call fails
      this.clearAuth()
    }
  },

  /**
   * Get Authorization header for API requests
   */
  getAuthHeader() {
    const token = this.getAccessToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  }
}
