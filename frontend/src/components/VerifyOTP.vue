<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="brand-mark">F</div>
      <h1 class="auth-title">Verify OTP &amp; Reset Password</h1>
      <p class="auth-sub">Enter the 6-digit code sent to <strong>{{ displayEmail }}</strong></p>

      <form @submit.prevent="handleResetPassword" class="auth-form">
        <div class="form-group">
          <label class="form-label">6-Digit OTP Code</label>
          <input v-model="form.otp_code" type="text" maxlength="6" pattern="[0-9]{6}" placeholder="123456" required class="form-input otp-input" @input="validateOTP" />
          <span class="form-hint">Code expires in 10 minutes</span>
        </div>

        <div class="form-group">
          <label class="form-label">New Password</label>
          <input v-model="form.new_password" type="password" placeholder="Enter new password" required class="form-input" />
        </div>

        <div class="form-group">
          <label class="form-label">Confirm New Password</label>
          <input v-model="form.confirm_password" type="password" placeholder="Confirm new password" required class="form-input" />
        </div>

        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading || !isOTPValid">
          {{ loading ? 'Resetting Password...' : 'Reset Password' }}
        </button>

        <div class="auth-links">
          <router-link to="/forgot-password">Resend OTP</router-link>
          <span class="divider">|</span>
          <router-link to="/login">Back to Login</router-link>
        </div>
      </form>

      <div class="security-note">
        <h4>Security Tips</h4>
        <ul>
          <li>Never share your OTP code with anyone</li>
          <li>OTP codes are single-use only</li>
          <li>Request a new OTP if yours expired</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../api'

export default {
  name: 'VerifyOTP',
  data() {
    return {
      form: {
        email: this.$route.query.email || '',
        otp_code: '',
        new_password: '',
        confirm_password: ''
      },
      loading: false,
      error: '',
      success: ''
    }
  },
  computed: {
    displayEmail() {
      return this.form.email || 'your email'
    },
    isOTPValid() {
      return /^\d{6}$/.test(this.form.otp_code)
    }
  },
  methods: {
    validateOTP(event) {
      
      this.form.otp_code = event.target.value.replace(/\D/g, '')
    },
    async handleResetPassword() {
      this.loading = true
      this.error = ''
      this.success = ''

      
      if (this.form.new_password !== this.form.confirm_password) {
        this.error = '❌ Passwords do not match!'
        this.loading = false
        return
      }

      
      if (this.form.new_password.length < 8) {
        this.error = '❌ Password must be at least 8 characters long'
        this.loading = false
        return
      }

      try {
        
        await authAPI.verifyOTP(this.form.email, this.form.otp_code)
        
        
        const response = await authAPI.passwordResetConfirm({
          email: this.form.email,
          otp_code: this.form.otp_code,
          new_password: this.form.new_password
        })
        
        this.success = response.data.message || '✅ Password reset successful!'
        
        
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)

      } catch (error) {
        console.error('Password reset failed:', error)
        const data = error.response?.data
        
        if (data) {
          if (typeof data === 'object') {
            this.error = data.error || data.detail || data.otp_code?.[0] || 'Invalid OTP or reset failed'
          } else {
            this.error = data
          }
        } else {
          this.error = 'Password reset failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    
    if (!this.form.email) {
      this.$router.push('/forgot-password')
    }
  }
}
</script>
<style scoped>
.auth-page { min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2rem; background:#111827; }
.auth-card { background:#fff; padding:2.5rem; border-radius:var(--radius-lg); box-shadow:var(--shadow-xl); max-width:480px; width:100%; }
.brand-mark { width:48px; height:48px; background:var(--primary-500); color:#fff; border-radius:var(--radius-md); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.25rem; margin:0 auto 1.5rem; }
.auth-title { text-align:center; font-size:1.5rem; font-weight:700; color:var(--gray-900); margin:0 0 .5rem; }
.auth-sub { text-align:center; font-size:.875rem; color:var(--gray-500); margin:0 0 1.5rem; line-height:1.5; }
.auth-sub strong { color:var(--primary-500); }
.auth-form { display:flex; flex-direction:column; gap:1rem; }
.otp-input { text-align:center; font-size:1.5rem; font-weight:700; letter-spacing:.5rem; font-family:'Courier New',monospace; }
.btn-block { width:100%; padding:.75rem; }
.alert { padding:.75rem 1rem; border-radius:var(--radius-md); font-size:.8125rem; }
.alert-error { background:#fef2f2; color:var(--red-500); border:1px solid #fecaca; }
.alert-success { background:#ecfdf5; color:var(--green-500); border:1px solid #bbf7d0; }
.auth-links { display:flex; justify-content:center; align-items:center; gap:.75rem; font-size:.8125rem; }
.auth-links a { color:var(--primary-500); text-decoration:none; font-weight:600; }
.divider { color:var(--gray-300); }
.security-note { margin-top:1.5rem; background:var(--gray-50); border-radius:var(--radius-md); padding:1rem; border:1px solid var(--border-color); }
.security-note h4 { font-size:.8125rem; font-weight:600; color:var(--gray-900); margin:0 0 .5rem; }
.security-note ul { margin:0; padding-left:1.25rem; font-size:.8125rem; color:var(--gray-600); line-height:1.8; }
@media(max-width:600px){ .auth-card{padding:1.5rem;} }
</style>
