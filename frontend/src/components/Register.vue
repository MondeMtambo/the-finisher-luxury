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
        <p class="subheadline">Apply for a dedicated FINISHER enterprise workspace.</p>
      </div>

      <form @submit.prevent="handleRequestAccess" class="reg-form">
        <div class="form-group">
          <label class="form-label">Company / Business Name *</label>
          <input 
            v-model="request.company_name" 
            type="text" 
            class="form-input" 
            placeholder="e.g. Acme Holdings (Pty) Ltd" 
            required 
          />
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Contact Person / Executive Name *</label>
            <input 
              v-model="request.full_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Monde Mtambo" 
              required 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Direct Phone Number *</label>
            <input 
              v-model="request.phone" 
              type="tel" 
              class="form-input" 
              placeholder="+27 (0) 11 000 0000" 
              required 
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Work Email Address *</label>
          <input 
            v-model="request.email" 
            type="email" 
            class="form-input" 
            placeholder="executive@company.co.za" 
            @blur="checkCorporateEmail"
            required 
          />
          <span class="form-hint" v-if="isGenericEmail" style="color:#f59e0b">
            Enterprise tip: Using your official corporate domain expedites workspace provisioning.
          </span>
        </div>

        <div class="form-group">
          <label class="form-label">Message / Operational Directives (Optional)</label>
          <textarea 
            v-model="request.message" 
            rows="3" 
            class="form-input" 
            placeholder="Tell us about your team size, CRM requirements, or integrations..."
          ></textarea>
        </div>

        <!-- POPIA Compliance Check -->
        <div class="consent-section">
          <label class="check-row">
            <input type="checkbox" v-model="acceptedCompliance" required />
            <span>
              I confirm I am an authorized corporate officer applying on behalf of this business entity. I acknowledge the processing of business information in accordance with the 
              <router-link to="/disclaimer" target="_blank" class="gold-link">POPIA Data Safeguard Notice</router-link>.
            </span>
          </label>
        </div>

        <div v-if="error" class="form-error">{{ error }}</div>
        <div v-if="success" class="info-bar">{{ success }}</div>

        <div class="step-nav">
          <button 
            type="submit" 
            class="btn btn-primary btn-gold-action" 
            :disabled="loading || !acceptedCompliance"
          >
            {{ loading ? 'Submitting Application...' : 'Request Access' }}
          </button>
        </div>

        <div class="auth-footer">
          Already have an authorized workspace? 
          <router-link to="/login" class="gold-link">Member Login Here</router-link>
        </div>
      </form>
    </div>

    <!-- Application Submitted Success State -->
    <div class="auth-card register-card glass-panel success-panel" v-else>
      <div class="success-icon">
        <div class="gold-seal">✓</div>
      </div>
      <h2 class="headline">Access Request Received</h2>
      <div class="success-divider"></div>
      <p class="success-note">
        Thank you, <strong>{{ request.full_name }}</strong>. Your access request for <strong>{{ request.company_name }}</strong> has been submitted to Mtambo Holdings.
      </p>
      <p class="text-muted text-sm mt-3">
        Our executive onboarding team will review your application and provision your dedicated FINISHER workspace. An activation notice will be dispatched to <strong>{{ request.email }}</strong>.
      </p>
      <div class="mt-4">
        <button class="btn btn-secondary" @click="$router.push('/login')">Return to Member Login</button>
      </div>
    </div>
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
      acceptedCompliance: true,
      isGenericEmail: false,
      request: {
        company_name: '',
        full_name: '',
        email: '',
        phone: '',
        message: ''
      }
    }
  },
  methods: {
    checkCorporateEmail() {
      const email = (this.request.email || '').toLowerCase()
      const genericDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'mail.com']
      const domain = email.split('@')[1]
      this.isGenericEmail = !!(domain && genericDomains.includes(domain))
    },
    async handleRequestAccess() {
      if (!this.request.company_name || !this.request.email || !this.request.full_name) {
        this.error = 'Please fill in all required fields.'
        return
      }

      this.loading = true
      this.error = ''
      this.success = ''

      try {
        const payload = {
          subject: `Corporate Access Request: ${this.request.company_name}`,
          message: this.request.message || `Corporate access request for ${this.request.company_name} by ${this.request.full_name}. Email: ${this.request.email}, Phone: ${this.request.phone}`,
          metadata: {
            company_name: this.request.company_name,
            full_name: this.request.full_name,
            email: this.request.email,
            phone: this.request.phone,
            registration_source: 'minimal_request_access'
          }
        }

        await ticketsAPI.create(payload)

        this.applicationSubmitted = true
        toast.success('Access request submitted successfully')

      } catch (err) {
        console.error('Request access error:', err)
        this.error = err.response?.data?.message || 'Unable to submit request at this time. Please contact support@thefinishercrm.tech.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: #0b0f19;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #f3f4f6;
  position: relative;
}

.exclusive-nav {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 1.5rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-weight: 800;
  letter-spacing: 0.15em;
  font-size: 1rem;
  color: #d4af37;
}

.nav-btn {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #d4af37;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.nav-btn:hover {
  background: #d4af37;
  color: #0b0f19;
}

.auth-card {
  width: 100%;
  max-width: 600px;
  border-radius: 12px;
  padding: 2.5rem;
  background: rgba(17, 24, 39, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(12px);
  margin-top: 3rem;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.card-logo {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%);
  color: #0b0f19;
  font-weight: 900;
  font-size: 1.25rem;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.headline {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin: 0 0 0.5rem;
}

.subheadline {
  font-size: 0.875rem;
  color: #9ca3af;
  margin: 0;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.25rem;
  text-align: left;
}

.form-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #d1d5db;
  margin-bottom: 0.35rem;
  letter-spacing: 0.02em;
}

.form-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #ffffff;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
}

.form-hint {
  font-size: 0.75rem;
  margin-top: 0.35rem;
  display: block;
}

.consent-section {
  margin: 1.5rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 6px;
}

.check-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  font-size: 0.8rem;
  color: #9ca3af;
  line-height: 1.4;
  cursor: pointer;
}

.check-row input[type="checkbox"] {
  margin-top: 0.2rem;
  accent-color: #d4af37;
}

.gold-link {
  color: #d4af37;
  text-decoration: none;
}
.gold-link:hover {
  text-decoration: underline;
}

.btn-gold-action {
  width: 100%;
  padding: 0.875rem;
  background: linear-gradient(135deg, #d4af37 0%, #b89628 100%);
  color: #0b0f19;
  border: none;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-gold-action:hover:not(:disabled) {
  opacity: 0.92;
  box-shadow: 0 4px 14px rgba(212, 175, 55, 0.3);
}
.btn-gold-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.auth-footer {
  text-align: center;
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 1.5rem;
}

/* Success Panel */
.success-panel {
  text-align: center;
  padding: 3.5rem 2.5rem;
}
.gold-seal {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.15);
  border: 2px solid #d4af37;
  color: #d4af37;
  font-size: 1.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}
.success-divider {
  width: 60px;
  height: 2px;
  background: #d4af37;
  margin: 1.25rem auto;
}
.success-note {
  font-size: 1rem;
  line-height: 1.5;
  color: #e5e7eb;
}

@media (max-width: 640px) {
  .form-grid-2 {
    grid-template-columns: 1fr;
  }
  .exclusive-nav {
    padding: 1rem;
  }
  .auth-card {
    padding: 1.5rem;
  }
}
</style>
