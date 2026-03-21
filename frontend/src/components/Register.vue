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

      <div class="vip-steps">
        <div class="vip-step" :class="{ active: currentStep === 1, done: currentStep > 1 }">
          <span>I. Identity</span>
        </div>
        <div class="vip-step-divider"></div>
        <div class="vip-step" :class="{ active: currentStep === 2, done: currentStep > 2 }">
          <span>II. Organisation</span>
        </div>
      </div>

      <form @submit.prevent="handleRegister" class="reg-form">

        <div v-show="currentStep === 1" class="form-step">

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">First Name *</label>
              <input v-model="form.first_name" type="text" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Last Name *</label>
              <input v-model="form.last_name" type="text" class="form-input" required />
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">Corporate Email *</label>
              <input v-model="form.email" type="email" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Direct Phone *</label>
              <input v-model="form.phone" type="tel" class="form-input" required />
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">Secure Password *</label>
              <input v-model="form.password" type="password" class="form-input" required @input="validatePasswordRealtime" />
            </div>
            <div class="form-group">
              <label class="form-label">Confirm Password *</label>
              <input v-model="form.password2" type="password" class="form-input" required />
            </div>
          </div>

          <div v-if="form.password" class="pw-rules">
            <div class="pw-rule" :class="{ passed: passwordChecks.length }"><span class="rule-dot"></span>At least 8 characters</div>
            <div class="pw-rule" :class="{ passed: passwordChecks.uppercase }"><span class="rule-dot"></span>At least 1 uppercase letter</div>
            <div class="pw-rule" :class="{ passed: passwordChecks.lowercase }"><span class="rule-dot"></span>At least 1 lowercase letter</div>
            <div class="pw-rule" :class="{ passed: passwordChecks.number }"><span class="rule-dot"></span>At least 1 number</div>
            <div class="pw-rule" :class="{ passed: passwordChecks.special }"><span class="rule-dot"></span>At least 1 special character</div>
            <div class="pw-bar"><div class="pw-bar-fill" :style="{ width: passwordStrengthPercent + '%' }" :class="passwordStrengthClass"></div></div>
            <p class="pw-strength-label" :class="passwordStrengthClass">{{ passwordStrengthLabel }}</p>
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">Work Phone *</label>
              <input v-model="form.phone" type="tel" class="form-input" placeholder="+27 12 345 6789" required />
            </div>
            <div class="form-group">
              <label class="form-label">Country</label>
              <select v-model="form.country" class="form-input">
                <option value="ZA">South Africa</option>
                <option value="US">United States</option>
                <option value="GB">United Kingdom</option>
                <option value="CA">Canada</option>
                <option value="AU">Australia</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">Team Size</label>
              <select v-model="form.company_size" class="form-input">
                <option value="">Select Size</option>
                <option value="1-5">1-5 people</option>
                <option value="6-20">6-20 people</option>
                <option value="21-50">21-50 people</option>
                <option value="51-200">51-200 people</option>
                <option value="200+">200+ people</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Expected Contacts</label>
              <select v-model="form.expected_contacts" class="form-input">
                <option value="">Select Range</option>
                <option value="0-100">Up to 100</option>
                <option value="100-500">100-500</option>
                <option value="500-2000">500-2,000</option>
                <option value="2000+">2,000+</option>
              </select>
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">How'd You Find Us?</label>
              <select v-model="form.referral_source" class="form-input">
                <option value="">Select Source</option>
                <option value="google">Google Search</option>
                <option value="social_media">Social Media</option>
                <option value="referral">Friend/Colleague</option>
                <option value="advertisement">Advertisement</option>
                <option value="blog">Blog/Article</option>
                <option value="event">Event/Conference</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Current CRM</label>
              <input v-model="form.current_crm" type="text" class="form-input" placeholder="e.g., Salesforce, None" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">How will you use THE FINISHER?</label>
            <textarea v-model="form.intended_use_case" rows="2" class="form-input" placeholder="e.g., CRM for sales tracking, ticketing system..."></textarea>
          </div>

          <div class="step-nav">
            <button type="button" class="btn btn-secondary" @click="goToStep(1)">Back</button>
            <button type="button" class="btn btn-primary" @click="goToStep(3)" :disabled="!step2Valid">Next: Choose Plan</button>
          </div>
        </div>

        <div v-show="currentStep === 3" class="form-step">
          <h3 class="step-title">Choose Your Plan</h3>

          <div class="tier-grid">
            <div class="tier-card tier-locked" @click="attemptSelectTier('free')">
              <div class="locked-overlay"><span>NOT AVAILABLE</span></div>
              <h4>CLASSIC</h4>
              <p class="tier-price">FREE</p>
              <ul><li>1 User</li><li>Basic CRM</li></ul>
            </div>
            <div class="tier-card tier-active" :class="{ selected: form.tier === 'luxury' }" @click="attemptSelectTier('luxury')">
              <span class="badge badge-blue" style="position:absolute;top:.75rem;right:.75rem;font-size:.625rem">ACTIVE</span>
              <h4>LUXURY</h4>
              <p class="tier-price">R249<small>/mo</small></p>
              <ul><li>10 Users</li><li>API Access</li><li>Integrations</li><li>Priority Support</li></ul>
              <span class="badge badge-green" style="font-size:.625rem;margin-top:.5rem">RECOMMENDED</span>
            </div>
            <div class="tier-card tier-locked" @click="attemptSelectTier('premium')">
              <div class="locked-overlay"><span>Q2 2026</span></div>
              <h4>PREMIUM</h4>
              <p class="tier-price">R499<small>/mo</small></p>
              <ul><li>Unlimited</li><li>White-Label</li><li>24/7 Support</li></ul>
            </div>
          </div>

          <div v-if="form.tier === 'luxury'" class="info-bar" style="margin-top:1rem">
            <strong>LUXURY EDITION</strong> &mdash; 10 users, API access, integrations &amp; priority support. Payment after account creation.
          </div>
          <div v-if="tierBlockMessage" class="info-bar" style="margin-top:.75rem;background:#fef2f2;color:var(--red-500)">{{ tierBlockMessage }}</div>

          <div class="consent-section">
            <label class="check-row">
              <input type="checkbox" v-model="termsAccepted" />
              <span>I accept the <a href="#" @click.prevent="showTermsModal = true" class="link">Terms &amp; Conditions</a> *</span>
            </label>
            <label class="check-row">
              <input type="checkbox" v-model="form.marketing_consent" />
              <span>Send me updates, tips &amp; offers</span>
            </label>
          </div>

          <div v-if="error" class="form-error" style="margin-bottom:.75rem">{{ error }}</div>
          <div v-if="success" class="info-bar" style="background:#ecfdf5;color:var(--green-500);margin-bottom:.75rem">{{ success }}</div>

          <div class="step-nav">
            <button type="button" class="btn btn-secondary" @click="goToStep(2)">Back</button>
            <button type="submit" class="btn btn-primary" :disabled="loading || !termsAccepted">
              {{ loading ? 'Creating Account...' : 'Create Account' }}
            </button>
          </div>
        </div>

        <div class="auth-footer">Already have an account? <router-link to="/login" class="link">Login Here</router-link></div>
      </form>
    </div>

    <TermsModal :show="showTermsModal" @close="showTermsModal = false" @accept="handleTermsAccept" />
  </div>
</template>

<script>
import { authAPI } from '../api'
import authService from '../services/auth'
import TermsModal from './TermsModal.vue'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'Register',
  components: { TermsModal },
  data() {
    return {
      currentStep: 1,
      applicationSubmitted: false,
      customCompanyName: '',
      form: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        company_name: '',
        phone: '',
        password: '',
        password2: '',
        tier: 'luxury',
        job_title: '',
        industry: '',
        company_size: '',
        referral_source: '',
        business_website: '',
        country: 'ZA',
        intended_use_case: '',
        current_crm: '',
        expected_contacts: '',
        marketing_consent: false
      },
      loading: false,
      error: '',
      termsAccepted: false,
      showTermsModal: false,
      passwordChecks: {
        length: false,
        uppercase: false,
        lowercase: false,
        number: false,
        special: false
      }
    }
  },
  computed: {
    step1Valid() {
      return this.form.first_name && this.form.last_name && this.form.email && this.form.phone && this.allPasswordChecksPassed && this.form.password === this.form.password2
    },
    step2Valid() {
      return this.customCompanyName.trim() && this.form.job_title && this.termsAccepted
    },
    allPasswordChecksPassed() {
      return this.passwordChecks.length && this.passwordChecks.uppercase &&
             this.passwordChecks.lowercase && this.passwordChecks.number &&
             this.passwordChecks.special
    },
    resolvedCompanyName() {
      return this.customCompanyName.trim()
    },
    generatedUsername() {
      const name = this.resolvedCompanyName
      if (!name) return ''
      
      return name.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '')
    }
  },
  watch: {
    
    resolvedCompanyName(val) {
      if (val) {
        this.form.username = this.generatedUsername
      } else {
        this.form.username = ''
      }
    }
  },
  methods: {
    validatePasswordRealtime() {
      const pw = this.form.password
      this.passwordChecks = {
        length: pw.length >= 8,
        uppercase: /[A-Z]/.test(pw),
        lowercase: /[a-z]/.test(pw),
        number: /[0-9]/.test(pw),
        special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?`~]/.test(pw)
      }
    },
    goToStep(step) {
        if (!this.form.first_name || !this.form.last_name) {
          toast.warning('Please enter your first and last name.')
          return
        }
        if (!this.form.email) {
          toast.warning('Please enter your work email.')
          return
        }
        if (!this.form.phone) {
          toast.warning('Please enter your work phone number.')
          return
        }
        if (!this.allPasswordChecksPassed) {
          toast.error('Your password does not meet all the required rules. Please check the requirements.')
          return
        }
        if (this.form.password !== this.form.password2) {
          toast.error('Passwords do not match.')
          return
        }
      this.currentStep = step
    },
    handleTermsAccept() {
      this.termsAccepted = true
    },
    async handleRegister() {
      this.loading = true
      this.error = ''

      try {
        
        const submitData = { ...this.form }
        submitData.company_name = this.resolvedCompanyName
        submitData.is_unlisted_company = true // All companies in exclusive mode are manually typed

        const response = await authAPI.register(submitData)

        // Velvet Rope: Do not log them in. Show success screen.
        authService.clearAuth()
        this.applicationSubmitted = true

      } catch (error) {
        console.error('Registration failed:', error)
        const data = error.response?.data
        if (data) {
          if (typeof data === 'object') {
            const errors = []
            for (const [, messages] of Object.entries(data)) {
              if (Array.isArray(messages)) errors.push(...messages)
              else errors.push(messages)
            }
            this.error = errors.join(', ')
          } else {
            this.error = data || 'Registration failed. Please try again.'
          }
        } else {
          this.error = error.message || 'Registration failed. Please try again.'
        }
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
