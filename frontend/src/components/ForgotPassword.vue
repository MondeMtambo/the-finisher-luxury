<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="brand-mark">F</div>
      <h1 class="auth-title">Password Reset</h1>
      <p class="auth-sub">Enter your email address and we'll send you a 6-digit OTP code to reset your password.</p>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label class="form-label">Email Address</label>
          <input v-model="email" type="email" placeholder="your.email@company.com" required class="form-input" />
        </div>

        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? 'Sending OTP...' : 'Send OTP Code' }}
        </button>

        <div class="auth-footer">
          Remember your password? <router-link to="/login">Back to Login</router-link>
        </div>
      </form>

      <div class="otp-info">
        <h3>How OTP Password Reset Works</h3>
        <ol>
          <li><strong>Request OTP:</strong> Enter your email and click "Send OTP Code"</li>
          <li><strong>Check Email:</strong> You'll receive a 6-digit code valid for 10 minutes</li>
          <li><strong>Verify &amp; Reset:</strong> Enter the code and your new password</li>
          <li><strong>Login:</strong> Use your new password to access your account</li>
        </ol>
        <p class="otp-note">Each OTP code can only be used once for security.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../api'

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      loading: false,
      error: '',
      success: ''
    }
  },
  methods: {
    async handleSubmit() {
      this.loading = true
      this.error = ''
      this.success = ''

      try {
        const response = await authAPI.passwordResetRequest(this.email)
        
        this.success = response.data.message || '✅ OTP code sent! Check your email.'
        
        
        setTimeout(() => {
          this.$router.push({
            name: 'VerifyOTP',
            query: { email: this.email }
          })
        }, 2000)

      } catch (error) {
        console.error('Password reset request failed:', error)
        this.error = error.response?.data?.error || error.response?.data?.detail || 'Failed to send OTP. Please try again.'
      } finally {
        this.loading = false
      }
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
.auth-form { display:flex; flex-direction:column; gap:1rem; }
.btn-block { width:100%; padding:.75rem; }
.alert { padding:.75rem 1rem; border-radius:var(--radius-md); font-size:.8125rem; }
.alert-error { background:#fef2f2; color:var(--red-500); border:1px solid #fecaca; }
.alert-success { background:#ecfdf5; color:var(--green-500); border:1px solid #bbf7d0; }
.auth-footer { text-align:center; font-size:.8125rem; color:var(--gray-500); }
.auth-footer a { color:var(--primary-500); text-decoration:none; font-weight:600; }
.otp-info { margin-top:1.5rem; background:var(--gray-50); border-radius:var(--radius-md); padding:1.25rem; border:1px solid var(--border-color); }
.otp-info h3 { font-size:.875rem; font-weight:600; color:var(--gray-900); margin:0 0 .75rem; }
.otp-info ol { margin:0; padding-left:1.25rem; font-size:.8125rem; color:var(--gray-600); line-height:1.8; }
.otp-info strong { color:var(--primary-500); }
.otp-note { margin:.75rem 0 0; padding:.5rem .75rem; background:#fffbeb; border-radius:var(--radius-sm); color:var(--amber-500); font-size:.8125rem; }
@media(max-width:600px){ .auth-card{padding:1.5rem;} }
</style>
