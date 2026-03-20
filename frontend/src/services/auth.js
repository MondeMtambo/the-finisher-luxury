/**
 * Authentication Service for THE FINISHER CRM
 * Handles JWT token storage, refresh, and auth state
 */

import axios from 'axios'
import API_BASE_URL from '../utils/apiBase'

const TOKEN_KEY = 'thefinisher_access_token'
const REFRESH_KEY = 'thefinisher_refresh_token'
const USER_KEY = 'thefinisher_user'
const LOGIN_TIME_KEY = 'thefinisher_login_time'

// Maximum session duration (8 hours) — forces re-login for security
const MAX_SESSION_MS = 8 * 60 * 60 * 1000

export default {
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
    
    // Store user info if available from login response
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    } else {
      // Fallback: store basic user info - will be enriched later by profile call
      localStorage.setItem(USER_KEY, JSON.stringify({ username }))
    }
    
    return response.data
  },

  /**
   * Check if user is authenticated (has token + session not expired)
   */
  isAuthenticated() {
    const token = this.getAccessToken()
    if (!token) return false

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

    // We have a token and session is within limits — consider authenticated.
    // The API interceptor handles actual JWT expiry + refresh automatically.
    return true
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
    return localStorage.getItem(TOKEN_KEY)
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
    const userStr = localStorage.getItem(USER_KEY)
    return userStr ? JSON.parse(userStr) : null
  },

  /**
   * Get current user with permissions
   */
  getCurrentUser() {
    return this.getUser()
  },

  setUser(user) {
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    } else {
      localStorage.removeItem(USER_KEY)
    }
  },

  /**
   * Save tokens and user data after login/register
   */
  saveAuth(tokens, user) {
    localStorage.setItem(TOKEN_KEY, tokens.access)
    localStorage.setItem(REFRESH_KEY, tokens.refresh)
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  },

  /**
   * Set tokens after MFA verification (without user data initially)
   */
  setTokens(access, refresh) {
    localStorage.setItem(TOKEN_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
    localStorage.setItem(LOGIN_TIME_KEY, Date.now().toString())
  },

  /**
   * Update only access token (after refresh)
   */
  updateAccessToken(token) {
    localStorage.setItem(TOKEN_KEY, token)
  },

  /**
   * Clear all auth data (logout)
   */
  clearAuth() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(LOGIN_TIME_KEY)
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
