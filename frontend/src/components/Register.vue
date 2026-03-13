<template>
  <div class="auth-page">
    <div class="auth-card register-card">

      <div class="auth-brand">
        <div class="brand-mark">F</div>
        <h1 class="brand-title">THE FINISHER</h1>
        <p class="brand-tag">Apply for Access</p>
      </div>
      <p class="admin-notice">Access is for <strong>partner companies</strong> only. Submit an application to get your workspace set up.</p>

      <div class="steps">
        <div class="step" :class="{ active: currentStep === 1, done: currentStep > 1 }">
          <span class="step-num">{{ currentStep > 1 ? '\u2713' : '1' }}</span><span class="step-text">Company</span>
        </div>
        <div class="step-line" :class="{ filled: currentStep > 1 }"></div>
        <div class="step" :class="{ active: currentStep === 2, done: currentStep > 2 }">
          <span class="step-num">{{ currentStep > 2 ? '\u2713' : '2' }}</span><span class="step-text">Account</span>
        </div>
        <div class="step-line" :class="{ filled: currentStep > 2 }"></div>
        <div class="step" :class="{ active: currentStep === 3 }">
          <span class="step-num">3</span><span class="step-text">Plan</span>
        </div>
      </div>

      <form @submit.prevent="handleRegister" class="reg-form">

        <div v-show="currentStep === 1" class="form-step">
          <h3 class="step-title">Company &amp; Role</h3>

          <div class="form-group">
            <label class="form-label">Company Name *</label>
            <select v-model="form.company_name" class="form-input" required>
              <option value="">Select Your Company</option>
              <optgroup label="Financial Services">
                <option value="Discovery">Discovery</option>
                <option value="Momentum">Momentum</option>
                <option value="Sanlam">Sanlam</option>
                <option value="Old Mutual">Old Mutual</option>
                <option value="Liberty">Liberty</option>
                <option value="FNB">First National Bank (FNB)</option>
                <option value="Standard Bank">Standard Bank</option>
                <option value="ABSA">ABSA</option>
                <option value="Nedbank">Nedbank</option>
                <option value="Capitec">Capitec</option>
                <option value="Investec">Investec</option>
                <option value="African Bank">African Bank</option>
                <option value="Allan Gray">Allan Gray</option>
              </optgroup>
              <optgroup label="Insurance">
                <option value="Outsurance">Outsurance</option>
                <option value="MiWay">MiWay</option>
                <option value="Hollard">Hollard</option>
                <option value="King Price">King Price</option>
                <option value="Budget Insurance">Budget Insurance</option>
                <option value="1st for Women">1st for Women</option>
                <option value="Santam">Santam</option>
              </optgroup>
              <optgroup label="Telecommunications">
                <option value="MTN">MTN</option>
                <option value="Vodacom">Vodacom</option>
                <option value="Cell C">Cell C</option>
                <option value="Telkom">Telkom</option>
                <option value="Rain">Rain</option>
              </optgroup>
              <optgroup label="Retail & FMCG">
                <option value="Shoprite">Shoprite</option>
                <option value="Checkers">Checkers</option>
                <option value="Pick n Pay">Pick n Pay</option>
                <option value="Woolworths">Woolworths</option>
                <option value="Spar">Spar</option>
                <option value="Clicks">Clicks</option>
                <option value="Dis-Chem">Dis-Chem</option>
                <option value="Mr Price">Mr Price</option>
                <option value="TFG">The Foschini Group (TFG)</option>
                <option value="Pepkor">Pepkor</option>
              </optgroup>
              <optgroup label="Technology & IT">
                <option value="Naspers">Naspers</option>
                <option value="Takealot">Takealot</option>
                <option value="Dimension Data">Dimension Data</option>
                <option value="BCX">BCX</option>
                <option value="Altron">Altron</option>
                <option value="Datatec">Datatec</option>
              </optgroup>
              <optgroup label="Mining & Energy">
                <option value="Anglo American">Anglo American</option>
                <option value="Sasol">Sasol</option>
                <option value="Eskom">Eskom</option>
                <option value="Gold Fields">Gold Fields</option>
                <option value="Sibanye-Stillwater">Sibanye-Stillwater</option>
                <option value="Exxaro">Exxaro</option>
              </optgroup>
              <optgroup label="Healthcare">
                <option value="Netcare">Netcare</option>
                <option value="Mediclinic">Mediclinic</option>
                <option value="Life Healthcare">Life Healthcare</option>
              </optgroup>
              <optgroup label="Media & Entertainment">
                <option value="MultiChoice">MultiChoice</option>
                <option value="Primedia">Primedia</option>
                <option value="Media24">Media24</option>
              </optgroup>
              <optgroup label="Real Estate & Property">
                <option value="Growthpoint">Growthpoint Properties</option>
                <option value="Redefine Properties">Redefine Properties</option>
                <option value="Pam Golding">Pam Golding Properties</option>
              </optgroup>
              <optgroup label="Logistics & Transport">
                <option value="Imperial">Imperial Logistics</option>
                <option value="Transnet">Transnet</option>
                <option value="Bidvest">Bidvest</option>
              </optgroup>
              <option value="__other__">My company is not listed</option>
            </select>
          </div>

          <div v-if="form.company_name === '__other__'" class="form-group">
            <label class="form-label">Enter Company Name *</label>
            <input v-model="customCompanyName" type="text" class="form-input" placeholder="Enter your company name" required />
            <span class="form-hint" style="color:var(--amber-500)">Unlisted companies require manual verification (24-48 hours).</span>
          </div>

          <div v-if="form.company_name && form.company_name !== '__other__'" class="info-bar" style="margin-bottom:1rem">
            <strong>{{ form.company_name }}</strong> &mdash; Registered partner company
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">Your Role / Position *</label>
              <select v-model="form.job_title" class="form-input" required>
                <option value="">Select Your Role</option>
                <optgroup label="Executive & Leadership">
                  <option value="CEO">Chief Executive Officer (CEO)</option>
                  <option value="COO">Chief Operating Officer (COO)</option>
                  <option value="CFO">Chief Financial Officer (CFO)</option>
                  <option value="CTO">Chief Technology Officer (CTO)</option>
                  <option value="Managing Director">Managing Director</option>
                  <option value="Director">Director</option>
                </optgroup>
                <optgroup label="Sales & CRM">
                  <option value="Sales Director">Sales Director</option>
                  <option value="Sales Manager">Sales Manager</option>
                  <option value="Account Manager">Account Manager</option>
                  <option value="Business Development Manager">Business Development Manager</option>
                  <option value="Sales Representative">Authorized Sales Representative</option>
                </optgroup>
                <optgroup label="IT & Support">
                  <option value="IT Manager">IT Manager</option>
                  <option value="IT Administrator">IT Administrator</option>
                  <option value="Service Desk Manager">Service Desk Manager</option>
                  <option value="Support Manager">Support Manager</option>
                </optgroup>
                <optgroup label="Operations & HR">
                  <option value="Operations Manager">Operations Manager</option>
                  <option value="HR Manager">HR Manager</option>
                  <option value="Office Manager">Office Manager</option>
                  <option value="Project Manager">Project Manager</option>
                </optgroup>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Industry</label>
              <select v-model="form.industry" class="form-input">
                <option value="">Select Industry</option>
                <option value="it">Information Technology</option>
                <option value="retail">Retail & E-commerce</option>
                <option value="healthcare">Healthcare & Medical</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="finance">Finance & Banking</option>
                <option value="real_estate">Real Estate</option>
                <option value="education">Education & Training</option>
                <option value="hospitality">Hospitality & Tourism</option>
                <option value="construction">Construction & Engineering</option>
                <option value="consulting">Consulting & Professional Services</option>
                <option value="marketing">Marketing & Advertising</option>
                <option value="logistics">Logistics & Transportation</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          <div class="who-can-register">
            <h4>Who can register?</h4>
            <ul>
              <li><strong>CEOs / Directors</strong> &mdash; Primary company admin</li>
              <li><strong>Authorized Sales Representatives</strong> &mdash; Given authorization by the CEO</li>
              <li><strong>IT Managers</strong> &mdash; System administrators for the company</li>
            </ul>
            <p class="form-hint">All other employees will be onboarded by the admin after registration.</p>
          </div>

          <button type="button" class="btn btn-primary btn-block" @click="goToStep(2)" :disabled="!step1Valid">Next: Account Details</button>
        </div>

        <div v-show="currentStep === 2" class="form-step">
          <h3 class="step-title">Account Details</h3>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">First Name *</label>
              <input v-model="form.first_name" type="text" class="form-input" placeholder="John" required />
            </div>
            <div class="form-group">
              <label class="form-label">Last Name *</label>
              <input v-model="form.last_name" type="text" class="form-input" placeholder="Doe" required />
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-group">
              <label class="form-label">Username (Company Name) *</label>
              <input v-model="form.username" type="text" class="form-input" readonly style="background:var(--gray-100)" />
              <span class="form-hint">Automatically set to your company name.</span>
            </div>
            <div class="form-group">
              <label class="form-label">Work Email *</label>
              <input v-model="form.email" type="email" class="form-input" placeholder="john@company.com" required />
            </div>
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
              {{ loading ? 'Submitting Application...' : 'Submit Application' }}
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
      customCompanyName: '',
      form: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        company_name: '',
        phone: '',
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
      success: '',
      termsAccepted: false,
      showTermsModal: false,
      tierBlockMessage: '',
    }
  },
  computed: {
    step1Valid() {
      if (this.form.company_name === '__other__') {
        return this.customCompanyName.trim() && this.form.job_title
      }
      return this.form.company_name && this.form.job_title
    },
    step2Valid() {
      return this.form.first_name && this.form.last_name && this.form.username &&
             this.form.email && this.form.phone
    },
    resolvedCompanyName() {
      if (this.form.company_name === '__other__') {
        return this.customCompanyName.trim()
      }
      return this.form.company_name
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
    goToStep(step) {
      if (step === 2 && !this.step1Valid) {
        toast.warning('Please select your company and role before continuing.')
        return
      }
      if (step === 3 && !this.step2Valid) {
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
        toast.warning('Please fill in all required fields before continuing.')
        return
      }
      this.currentStep = step
    },
    attemptSelectTier(tier) {
      this.tierBlockMessage = ''
      if (tier === 'free') {
        this.tierBlockMessage = '🚫 FREE tier is not available in THE FINISHER LUXURY Edition. LUXURY plan (R249/mo) gives you 10-user access, advanced features & priority support!'
        setTimeout(() => { this.tierBlockMessage = '' }, 6000)
        return
      }
      if (tier === 'luxury' || tier === 'premium') {
        this.tierBlockMessage = `🔒 ${tier.toUpperCase()} tier is coming Q2 2026! Start with LUXURY (R249/mo) to access all current features.`
        setTimeout(() => { this.tierBlockMessage = '' }, 5000)
        return
      }
      if (tier === 'luxury') {
        this.form.tier = tier
        this.error = ''
      }
    },
    handleTermsAccept() {
      this.termsAccepted = true
    },
    async handleRegister() {
      this.loading = true
      this.error = ''
      this.success = ''

      try {
        
        const submitData = { ...this.form }
        submitData.company_name = this.resolvedCompanyName
        submitData.is_unlisted_company = this.form.company_name === '__other__'

        const apiUrl = (import.meta.env && import.meta.env.VITE_API_URL) ? import.meta.env.VITE_API_URL : '';
        const response = await fetch(`${apiUrl}/api/auth/request-access/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(submitData)
        });

        if (!response.ok) {
          throw new Error('Application submission failed. Please try again.')
        }

        this.success = 'Application successful! We will contact you soon.'
        
        await modal.alert(
          'Application Received ✨',
          'Thank you for applying!\n\nOur team will review your application and contact you shortly to complete your workspace setup.',
          'success'
        )

        this.$router.push('/login')

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
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem 1rem; background: var(--gray-900); }
.auth-card { background: #fff; border-radius: var(--radius-lg); box-shadow: var(--shadow-xl); width: 100%; padding: 2rem 2.5rem; }
.register-card { max-width: 720px; }

.auth-brand { text-align: center; margin-bottom: .75rem; }
.brand-mark { width: 44px; height: 44px; background: var(--primary-500); color: #fff; border-radius: var(--radius-md); display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.25rem; margin-bottom: .5rem; }
.brand-title { font-size: 1.125rem; font-weight: 700; color: var(--gray-900); margin: 0; }
.brand-tag { font-size: .8125rem; color: var(--gray-500); margin: .125rem 0 0; }
.admin-notice { font-size: .8125rem; color: var(--gray-600); text-align: center; margin: .75rem 0 1.25rem; line-height: 1.5; }

/* Steps */
.steps { display: flex; align-items: center; justify-content: center; gap: 0; margin-bottom: 1.75rem; }
.step { display: flex; align-items: center; gap: .375rem; }
.step-num { width: 26px; height: 26px; border-radius: 50%; border: 2px solid var(--gray-300); display: flex; align-items: center; justify-content: center; font-size: .75rem; font-weight: 600; color: var(--gray-400); transition: all .2s; }
.step-text { font-size: .75rem; color: var(--gray-400); font-weight: 500; }
.step.active .step-num { border-color: var(--primary-500); background: var(--primary-500); color: #fff; }
.step.active .step-text { color: var(--primary-500); }
.step.done .step-num { border-color: var(--green-500); background: var(--green-500); color: #fff; }
.step.done .step-text { color: var(--green-500); }
.step-line { width: 40px; height: 2px; background: var(--gray-200); margin: 0 .5rem; transition: background .2s; }
.step-line.filled { background: var(--green-500); }

/* Form */
.reg-form { }
.step-title { font-size: 1rem; font-weight: 600; color: var(--gray-800); margin: 0 0 1rem; padding-bottom: .5rem; border-bottom: 1px solid var(--gray-100); }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.btn-block { width: 100%; }
.step-nav { display: flex; gap: .75rem; margin-top: 1.25rem; }
.step-nav .btn { flex: 1; }

/* Who can register */
.who-can-register { background: var(--gray-50); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem 1.25rem; margin-bottom: 1.25rem; }
.who-can-register h4 { font-size: .8125rem; font-weight: 600; color: var(--gray-700); margin: 0 0 .5rem; }
.who-can-register ul { margin: 0; padding-left: 1.25rem; font-size: .8125rem; color: var(--gray-600); line-height: 1.7; }

/* Info bar (reuse global if available) */
.info-bar { background: #eff6ff; color: var(--primary-500); padding: .75rem 1rem; border-radius: var(--radius-md); font-size: .8125rem; line-height: 1.5; }

/* Tier cards */
.tier-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; }
.tier-card { position: relative; background: #fff; border: 2px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem 1rem; text-align: center; cursor: pointer; transition: border-color .2s, box-shadow .2s; }
.tier-card h4 { font-size: .8125rem; font-weight: 700; color: var(--gray-800); margin: 0 0 .375rem; letter-spacing: .03em; }
.tier-price { font-size: 1.125rem; font-weight: 700; color: var(--gray-900); margin: 0 0 .5rem; }
.tier-price small { font-size: .75rem; font-weight: 400; color: var(--gray-500); }
.tier-card ul { list-style: none; padding: 0; margin: 0; font-size: .75rem; color: var(--gray-600); line-height: 1.8; }
.tier-active { border-color: var(--primary-500); }
.tier-active.selected { box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
.tier-locked { opacity: .55; pointer-events: none; position: relative; }
.locked-overlay { position: absolute; inset: 0; background: rgba(255,255,255,.7); display: flex; align-items: center; justify-content: center; border-radius: var(--radius-md); z-index: 1; }
.locked-overlay span { font-size: .6875rem; font-weight: 700; color: var(--gray-500); letter-spacing: .05em; }

/* Consent */
.consent-section { margin: 1.25rem 0; display: flex; flex-direction: column; gap: .5rem; }
.check-row { display: flex; align-items: flex-start; gap: .5rem; font-size: .8125rem; color: var(--gray-600); cursor: pointer; }
.check-row input { margin-top: 2px; accent-color: var(--primary-500); }
.link { color: var(--primary-500); text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }

.auth-footer { text-align: center; margin-top: 1.5rem; font-size: .8125rem; color: var(--gray-500); }

@media (max-width: 768px) {
  .auth-card { padding: 1.5rem 1.25rem; }
  .form-grid-2 { grid-template-columns: 1fr; }
  .tier-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
  .tier-grid { grid-template-columns: 1fr; }
  .step-text { display: none; }
}
</style>
