<template>
  <div class="auth-page">
    <!-- Live Luxury Background -->
    <div class="particles">
      <div class="particle" v-for="n in 20" :key="n"></div>
    </div>
    <div class="ocean">
      <div class="wave"></div><div class="wave"></div><div class="wave"></div>
    </div>

    <div class="auth-card" v-if="!showMFAModal">
      <div class="auth-brand">
        <div class="brand-mark">F</div>
        <h1>THE FINISHER</h1>
        <p class="brand-sub">Luxury Edition</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label" for="username">Email (or adminluxury username)</label>
          <input id="username" class="form-input" v-model="form.username" type="text" placeholder="Enter your email" required autofocus>
        </div>
        <div class="form-group">
          <label class="form-label" for="password">Password</label>
          <input id="password" class="form-input" v-model="form.password" type="password" placeholder="Enter your password" required>
        </div>

        <label class="form-check-label">
          <input type="checkbox" v-model="form.acceptPolicy">
          <span>I agree to the <router-link to="/disclaimer">Disclaimer &amp; Privacy</router-link></span>
        </label>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading || !form.acceptPolicy">
          {{ loading ? 'Logging in...' : 'Log In' }}
        </button>

        <div class="auth-links">
          <router-link to="/forgot-password">Forgot Password?</router-link>
          <span class="link-sep">&middot;</span>
          <router-link to="/register" class="link">Request Access</router-link>
        </div>
      </form>
    </div>

    <div class="auth-card" v-if="showMFAModal">
      <div class="auth-brand">
        <div class="brand-mark">✓</div>
        <h1>Verify Your Identity</h1>
        <p class="brand-sub">Multi-Factor Authentication</p>
      </div>

      <div class="mfa-container">
        <p class="mfa-message">
          A 6-digit verification code has been sent to <strong>{{ mfaEmail }}</strong>
        </p>

        <div class="form-group">
          <label class="form-label" for="mfaCode">Verification Code</label>
          <input 
            id="mfaCode" 
            class="form-input mfa-code-input" 
            v-model="mfaCode" 
            type="text" 
            placeholder="000000" 
            maxlength="6"
            inputmode="numeric"
            @keyup.enter="verifyMFA"
            :disabled="mfaLoading"
          >
          <span class="form-hint">Enter 6 digits from your email</span>
        </div>

        <div v-if="mfaError" class="alert alert-danger">{{ mfaError }}</div>

        <button @click="verifyMFA" class="btn btn-primary btn-block" :disabled="mfaLoading || mfaCode.length !== 6">
          {{ mfaLoading ? 'Verifying...' : 'Verify Code' }}
        </button>

        <div class="mfa-actions">
          <button @click="resendMFACode" class="btn-link" :disabled="mfaLoading">
            Didn't receive a code?
          </button>
          <span class="link-sep">&middot;</span>
          <button @click="closeMFAModal" class="btn-link" :disabled="mfaLoading">
            Back to Login
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: '',
        acceptPolicy: false
      },
      loading: false,
      error: '',
      
      showMFAModal: false,
      mfaCode: '',
      mfaError: '',
      mfaLoading: false,
      mfaUserId: null,
      mfaEmail: '',
      mfaAttempts: 0,
    }
  },
  mounted() {
    if (authService.isAuthenticated()) {
      this.$router.push('/dashboard')
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''

      try {
        if (!this.form.acceptPolicy) {
          this.error = 'Please accept the Disclaimer & Privacy to continue.'
          return
        }
        
        
        const loginResponse = await authAPI.login({
          username: this.form.username,
          password: this.form.password
        })
        
        
        if (loginResponse.data.requires_mfa) {
          this.mfaUserId = loginResponse.data.user_id
          this.mfaEmail = loginResponse.data.email
          this.mfaError = ''
          this.mfaCode = ''
          this.mfaAttempts = 0
          this.showMFAModal = true
          toast.info('Verification Code Sent', 'Check your email inbox for the 6-digit code')
          return
        }
        
        
        if (loginResponse.data.access && loginResponse.data.refresh) {
          authService.setTokens(loginResponse.data.access, loginResponse.data.refresh)
        }

        
        let profile
        try {
          profile = await authAPI.getProfile()
          authService.setUser(profile.data)
        } catch (profileError) {
          console.warn('Failed to load profile:', profileError)
        }
        
        
        try {
          const requiresReset = profile?.data?.requires_password_reset === true
          const isSuperOrStaff = Boolean(profile?.data?.is_superuser || profile?.data?.is_staff)
          if (requiresReset && !isSuperOrStaff) {
            const newPwd = await modal.prompt('Set New Password', 'Security: Please set a new password now (minimum 8 characters):', { inputType: 'password', confirmText: 'Update Password' })
            if (newPwd && newPwd.length >= 8) {
              try {
                await authAPI.changePassword({
                  old_password: this.form.password,
                  new_password: newPwd,
                  new_password2: newPwd
                })
                toast.success('Password Updated', 'Your password has been updated successfully!')
              } catch (e) {
                console.error('Password change failed:', e)
                toast.error('Password Change Failed', 'Could not update password. You can change it from your profile later.')
              }
            }
          }
        } catch (_) {}

        this.$router.push('/dashboard')

      } catch (error) {
        console.error('Login failed:', error)
        const data = error.response?.data
        this.error = data?.detail || data?.message || data?.error || error.message || 'Invalid login details'
      } finally {
        this.loading = false
      }
    },

    async verifyMFA() {
      if (!this.mfaCode.trim()) {
        this.mfaError = 'Please enter the verification code'
        return
      }
      
      if (this.mfaCode.length !== 6 || !/^\d+$/.test(this.mfaCode)) {
        this.mfaError = 'Code must be 6 digits'
        return
      }
      
      this.mfaLoading = true
      this.mfaError = ''
      
      try {
        const response = await authAPI.verifyMFA({
          user_id: this.mfaUserId,
          mfa_code: this.mfaCode
        })
        
        
        if (response.data.access && response.data.refresh) {
          authService.setTokens(response.data.access, response.data.refresh)
          authService.setUser(response.data.user)
        }
        
        toast.success('Verified', 'You have been logged in successfully!')
        this.showMFAModal = false
        this.$router.push('/dashboard')
        
      } catch (error) {
        console.error('MFA verification failed:', error)
        const data = error.response?.data
        this.mfaError = data?.message || data?.error || 'Verification failed. Please try again.'
        this.mfaAttempts += 1
      } finally {
        this.mfaLoading = false
      }
    },

    closeMFAModal() {
      this.showMFAModal = false
      this.mfaCode = ''
      this.mfaError = ''
      this.mfaAttempts = 0
    },

    async resendMFACode() {
      this.mfaLoading = true
      try {
        
        const response = await authAPI.login({
          username: this.form.username,
          password: this.form.password
        })
        if (response.data.requires_mfa) {
          this.mfaCode = ''
          this.mfaError = ''
          this.mfaAttempts = 0
          toast.success('Code Resent', 'New verification code sent to your email')
        }
      } catch (error) {
        this.mfaError = 'Failed to resend code. Please try again.'
      } finally {
        this.mfaLoading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(-45deg, #0B0C10, #111418, #4A3B05, #D4AF37, #0B0C10);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}
@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
/* Waves */
.ocean { height: 10%; width: 100%; position: absolute; bottom: 0; left: 0; }
.wave {
  background: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 88.7"%3E%3Cpath d="M800 56.9c-155.5 0-204.9-50-405.5-49.9-200 0-250 49.9-394.5 49.9v31.8h800v-.2-31.6z" fill="%23D4AF37" opacity="0.3"/%3E%3C/svg%3E');
  position: absolute;
  width: 200%;
  height: 100%;
  animation: wave 10s -3s linear infinite;
  transform: translate3d(0, 0, 0);
  opacity: 0.8;
  bottom: 0;
  left: 0;
}
.wave:nth-of-type(2) { bottom: -1.25em; animation: wave 18s linear reverse infinite; opacity: 0.5; }
.wave:nth-of-type(3) { bottom: -2.5em; animation: wave 20s -1s reverse infinite; opacity: 0.2; }
@keyframes wave {
  2% { transform: translateX(1); }
  25% { transform: translateX(-25%); }
  50% { transform: translateX(-50%); }
  75% { transform: translateX(-25%); }
  100% { transform: translateX(1); }
}
/* Particles */
.particles { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.5);
  animation: float 7s infinite ease-in-out;
}
.particle:nth-child(odd) { width: 8px; height: 8px; animation-duration: 6s; }
.particle:nth-child(even) { width: 12px; height: 12px; animation-duration: 8s; }
.particle:nth-child(3n) { width: 5px; height: 5px; animation-duration: 5s; }
.particle:nth-child(1) { left: 10%; animation-delay: 0s; }
.particle:nth-child(2) { left: 20%; animation-delay: 2s; }
.particle:nth-child(3) { left: 30%; animation-delay: 1s; }
.particle:nth-child(4) { left: 40%; animation-delay: 3s; }
.particle:nth-child(5) { left: 50%; animation-delay: 0.5s; }
.particle:nth-child(6) { left: 60%; animation-delay: 2.5s; }
.particle:nth-child(7) { left: 70%; animation-delay: 1.5s; }
.particle:nth-child(8) { left: 80%; animation-delay: 0.2s; }
.particle:nth-child(9) { left: 90%; animation-delay: 3.5s; }
.particle:nth-child(10) { left: 15%; animation-delay: 1.2s; }
@keyframes float {
  0% { transform: translateY(100vh) scale(0); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateY(-100px) scale(1); opacity: 0; }
}
.auth-card {
  background: rgba(17, 20, 24, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: var(--radius-lg);
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8), inset 0 0 15px rgba(212,175,55,0.1);
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
  animation: slideUp 0.3s ease-out;
  z-index: 10;
  color: #fff;
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.auth-brand {
  text-align: center;
  margin-bottom: 2rem;
}
.brand-mark {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #D4AF37, #B49015);
  color: #000;
  font-size: 1.5rem;
  font-weight: 900;
  border-radius: var(--radius-md);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
}
.auth-brand h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  letter-spacing: 0.5px;
}
.brand-sub {
  color: #D4AF37;
  font-size: 0.85rem;
  margin: 0.25rem 0 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.auth-form,
.mfa-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #d1d5db;
}
.form-input {
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: border-color 0.2s;
}
.form-input:focus {
  outline: none;
  border-color: #D4AF37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}
.form-input:disabled {
  background-color: var(--gray-100);
  cursor: not-allowed;
}
.form-hint {
  font-size: 0.75rem;
  color: var(--gray-500);
  margin-top: 0.25rem;
}
.mfa-code-input {
  font-size: 1.5rem;
  letter-spacing: 0.5em;
  font-weight: 600;
  text-align: center;
  font-family: 'Courier New', monospace;
}
.mfa-message {
  text-align: center;
  color: var(--gray-700);
  font-size: 0.95rem;
  line-height: 1.5;
}
.form-check-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #9ca3af;
  cursor: pointer;
}
.form-check-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #D4AF37;
  cursor: pointer;
}
.form-check-label a {
  color: #D4AF37;
  font-weight: 600;
  text-decoration: none;
}
.form-check-label a:hover {
  text-decoration: underline;
}
.alert {
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
}
.alert-danger {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary {
  background: linear-gradient(135deg, #D4AF37, #B49015);
  color: #000;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
}
.btn-primary:disabled {
  background: var(--gray-300);
  cursor: not-allowed;
}
.btn-block {
  width: 100%;
  justify-content: center;
}
.btn-link {
  background: none;
  border: none;
  padding: 0;
  color: #D4AF37;
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: none;
}
.btn-link:hover:not(:disabled) {
  text-decoration: underline;
}
.btn-link:disabled {
  color: var(--gray-400);
  cursor: not-allowed;
}
.auth-links,
.mfa-actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}
.auth-links a {
  color: #D4AF37;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.85rem;
}
.auth-links a:hover {
  text-decoration: underline;
}
.link-sep {
  color: var(--gray-300);
}
</style>
