<template>
  <div class="auth-page luxury-auth-bg">
    <nav class="exclusive-nav">
      <div class="nav-brand">THE FINISHER</div>
      <div class="nav-links">
        <button class="nav-btn" @click="$router.push('/login')">Member Login</button>
      </div>
    </nav>

    <div class="auth-card register-card glass-panel" v-if="!applicationSubmitted">

      <div class="auth-header">
        <div class="card-logo">F</div>
        <h1 class="headline">Request Access</h1>
        <p class="subheadline">The Finisher Luxury Edition is available by invitation and application only.</p>
      </div>

      <form @submit.prevent="handleRequestAccess" class="reg-form simple-request-form">
        <div class="form-group">
          <label class="form-label">Full Name *</label>
          <input v-model="request.full_name" type="text" class="form-input" required />
        </div>

        <div class="form-group">
          <label class="form-label">Work Email *</label>
          <input v-model="request.email" type="email" class="form-input" required />
        </div>

        <div class="form-group">
          <label class="form-label">Company</label>
          <input v-model="request.company_name" type="text" class="form-input" />
        </div>

        <div class="form-group">
          <label class="form-label">Phone (optional)</label>
          <input v-model="request.phone" type="tel" class="form-input" />
        </div>

        <div class="form-group">
          <label class="form-label">Message (optional)</label>
          <textarea v-model="request.message" rows="3" class="form-input" placeholder="Briefly describe your use case or request"></textarea>
        </div>

        <div v-if="error" class="form-error" style="margin-bottom:.75rem">{{ error }}</div>
        <div v-if="success" class="info-bar" style="background:#ecfdf5;color:var(--green-500);margin-bottom:.75rem">{{ success }}</div>

        <div class="step-nav">
          <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? 'Sending...' : 'Request Access' }}</button>
        </div>

        <div class="auth-footer">Already have an account? <router-link to="/login" class="link">Login Here</router-link></div>
      </form>

    </div>

    <TermsModal :show="showTermsModal" @close="showTermsModal = false" @accept="handleTermsAccept" />
  </div>
</template>

<script>
import { ticketsAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'Register',
  data() {
    return {
      applicationSubmitted: false,
      loading: false,
      error: '',
      success: '',
      request: {
        full_name: '',
        email: '',
        company_name: '',
        phone: '',
        message: ''
      }
    }
  },
  methods: {
    async handleRequestAccess() {
      this.loading = true
      this.error = ''
      this.success = ''

      try {
        const payload = {
          subject: 'Request Access: ' + (this.request.company_name || this.request.full_name),
          message: this.request.message || 'Requesting access',
          metadata: {
            full_name: this.request.full_name,
            email: this.request.email,
            company: this.request.company_name,
            phone: this.request.phone
          }
        }

        await ticketsAPI.create(payload)

        this.success = 'Request sent. We will review and contact you shortly.'
        this.applicationSubmitted = true
        toast.success('Request sent')

      } catch (err) {
        console.error('Request access failed', err)
        this.error = err.message || 'Failed to send request. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
<style scoped>
.luxury-auth-bg {
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
  font-family: 'Inter', system-ui, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 2rem;
}

.exclusive-nav {
  position: absolute;
  top: 0; left: 0; width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 4rem;
  z-index: 10;
}
.nav-brand { font-size: 0.875rem; font-weight: 800; letter-spacing: 4px; color: #D4AF37; }
.nav-btn { background: transparent; border: none; color: #9ca3af; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; cursor: pointer; transition: color 0.3s; }
.nav-btn:hover { color: #D4AF37; }

.glass-panel {
  background: linear-gradient(135deg, rgba(15,15,15,0.8) 0%, rgba(5,5,5,0.9) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.2);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.9), inset 0 0 0 1px rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  padding: 3rem;
  position: relative;
  z-index: 10;
}
.success-panel { text-align: center; padding: 4rem 3rem; }
.success-icon { margin-bottom: 2rem; }
.success-divider { height: 1px; width: 50px; background: #D4AF37; margin: 2rem auto; }
.success-note { color: #9ca3af; font-size: 0.95rem; line-height: 1.6; }

.auth-header { text-align: center; margin-bottom: 2rem; }
.card-logo { font-size: 2.5rem; font-weight: 900; color: transparent; -webkit-text-stroke: 1px rgba(212, 175, 55, 0.8); margin-bottom: 1rem; line-height: 1; }
.headline { font-size: 2rem; font-weight: 800; margin: 0 0 0.5rem; color: #ffffff; letter-spacing: 1px; }
.subheadline { font-size: 0.875rem; color: #9ca3af; margin: 0; }

.vip-steps { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 2.5rem; }
.vip-step { font-size: 0.75rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; transition: color 0.3s; }
.vip-step.active { color: #D4AF37; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); }
.vip-step.done { color: #ffffff; }
.vip-step-divider { width: 40px; height: 1px; background: rgba(255,255,255,0.1); }

.form-group { margin-bottom: 1.5rem; }
.form-label { display: block; font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
.form-input { width: 100%; padding: 0.875rem 1rem; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; color: #fff; font-size: 0.95rem; transition: all 0.3s; }
.form-input:focus { border-color: #D4AF37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.1); outline: none; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }

.btn { display: inline-block; text-align: center; padding: 1rem 2rem; font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; border-radius: 4px; cursor: pointer; transition: all 0.3s; }
.btn-primary { background: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; color: #D4AF37; }
.btn-primary:hover:not(:disabled) { background: #D4AF37; color: #000; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; border-color: rgba(255,255,255,0.1); color: #6b7280; }
.btn-secondary { background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #9ca3af; }
.btn-secondary:hover { border-color: #fff; color: #fff; }
.btn-block { width: 100%; display: block; }
.step-nav { display: flex; gap: .75rem; margin-top: 1.25rem; }
.step-nav .btn { flex: 1; }

.pw-rules { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 1.5rem; }
.pw-rule { font-size: 0.7rem; color: #6b7280; display: flex; align-items: center; gap: 4px; }
.pw-rule.passed { color: #D4AF37; }
.rule-dot { width: 4px; height: 4px; border-radius: 50%; background: #6b7280; }
.pw-rule.passed .rule-dot { background: #D4AF37; box-shadow: 0 0 5px #D4AF37; }

.consent-section { margin: 2rem 0; padding: 1rem; border: 1px solid rgba(212, 175, 55, 0.2); background: rgba(212, 175, 55, 0.05); border-radius: 4px; }
.check-row { display: flex; align-items: flex-start; gap: 0.75rem; font-size: 0.8125rem; color: #d1d5db; cursor: pointer; line-height: 1.5; }
.check-row input { margin-top: 3px; accent-color: #D4AF37; }
.link { color: var(--primary-500); text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }

.form-error { color: #ef4444; font-size: 0.875rem; background: rgba(239, 68, 68, 0.1); padding: 0.75rem; border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 4px; margin-bottom: 1.5rem; text-align: center; }

@media (max-width: 480px) {
  .glass-panel { padding: 2rem 1.5rem; }
  .form-grid-2 { grid-template-columns: 1fr; gap: 0; }
  .step-nav { flex-direction: column; }
  .exclusive-nav { padding: 1.5rem 2rem; }
}
</style>
