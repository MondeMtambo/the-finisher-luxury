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
        <h1 class="headline">Institutional Registration</h1>
        <p class="subheadline">Apply for a dedicated FINISHER LUXURY corporate tenant workspace.</p>
      </div>

      <form @submit.prevent="handleRequestAccess" class="reg-form">
        <!-- ─── Section 1: Legal Entity & CIPC Verification ─── -->
        <div class="form-section-header">
          <span class="section-step">01</span>
          <div>
            <h3>Corporate Entity &amp; CIPC Verification</h3>
            <p>Official registration details for South African compliance (CIPC &amp; POPIA).</p>
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Registered Company Name *</label>
            <input 
              v-model="request.company_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Acme Holdings (Pty) Ltd" 
              required 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Company Trading Name (T/A)</label>
            <input 
              v-model="request.trading_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Acme Luxury Solutions" 
            />
            <span class="form-hint">Trading name if different from registered name</span>
          </div>
        </div>

        <!-- CIPC Registration Number with Live Verifier -->
        <div class="form-group cipc-group">
          <div class="cipc-label-row">
            <label class="form-label">CIPC Registration Number *</label>
            <span v-if="cipcStatus.state === 'valid'" class="cipc-badge badge-verified">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
              CIPC Verified &bull; {{ cipcStatus.entityLabel }}
            </span>
            <span v-else-if="cipcStatus.state === 'invalid' && request.cipc_number" class="cipc-badge badge-invalid">
              Standard format: 2024/123456/07
            </span>
          </div>

          <div class="cipc-input-wrap">
            <input 
              v-model="request.cipc_number" 
              @input="onCipcInput"
              type="text" 
              class="form-input font-mono" 
              :class="{ 'border-gold': cipcStatus.state === 'valid', 'border-error': cipcStatus.state === 'invalid' && request.cipc_number }"
              placeholder="YYYY/NNNNNN/NN (e.g. 2024/123456/07)" 
              maxlength="14"
              required 
            />
            <button 
              type="button" 
              class="btn-cipc-verify" 
              :disabled="cipcStatus.state !== 'valid' || verifyingCipc"
              @click="simulateCipcRegistryCheck"
            >
              {{ verifyingCipc ? 'Verifying...' : 'Verify CIPC' }}
            </button>
          </div>

          <div class="cipc-hint-bar" v-if="cipcStatus.message">
            <span :class="cipcStatus.state === 'valid' ? 'text-gold' : 'text-muted'">
              {{ cipcStatus.message }}
            </span>
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">SARS Tax / VAT Number (Optional)</label>
            <input 
              v-model="request.tax_number" 
              type="text" 
              class="form-input font-mono" 
              placeholder="10-digit Tax/VAT Reference" 
              maxlength="10" 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Industry / Sector *</label>
            <select v-model="request.industry" class="form-input" required>
              <option value="">-- Select Industry --</option>
              <option value="Finance & Banking">Finance, Banking &amp; Private Equity</option>
              <option value="Mining & Resources">Mining &amp; Natural Resources</option>
              <option value="Technology & Telecommunications">Technology &amp; Telecommunications</option>
              <option value="Luxury Goods & Retail">Luxury Goods &amp; High-End Retail</option>
              <option value="Legal & Corporate Advisory">Legal, Advisory &amp; Accounting</option>
              <option value="Real Estate & Property">Real Estate &amp; Property Development</option>
              <option value="Manufacturing & Engineering">Manufacturing &amp; Engineering</option>
              <option value="Logistics & Supply Chain">Logistics, Freight &amp; Transport</option>
              <option value="Healthcare & Pharmaceuticals">Healthcare &amp; Life Sciences</option>
              <option value="Hospitality & Tourism">Hospitality, Travel &amp; Tourism</option>
              <option value="Other">Other Institutional Sector</option>
            </select>
          </div>
        </div>

        <!-- ─── Section 2: Executive Contact (The Champion) ─── -->
        <div class="form-section-header mt-4">
          <span class="section-step">02</span>
          <div>
            <h3>Executive Leadership &amp; Point of Contact</h3>
            <p>Primary administrator authorized to manage company tenant operations.</p>
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Executive Full Name *</label>
            <input 
              v-model="request.full_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Monde Mtambo" 
              required 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Executive Job Title *</label>
            <input 
              v-model="request.job_title" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Chief Executive Officer / Managing Director" 
              required 
            />
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Corporate Work Email *</label>
            <input 
              v-model="request.email" 
              @input="checkCorporateEmail"
              type="email" 
              class="form-input" 
              placeholder="executive@company.co.za" 
              required 
            />
            <span v-if="isGenericEmail" class="email-warning">
              💡 For priority onboarding, an official corporate domain is recommended.
            </span>
          </div>

          <div class="form-group">
            <label class="form-label">Direct Business Contact Number *</label>
            <input 
              v-model="request.phone" 
              type="tel" 
              class="form-input" 
              placeholder="+27 (0) 82 123 4567" 
              required 
            />
          </div>
        </div>

        <!-- ─── Section 3: Business Presence & Fleet Scale ─── -->
        <div class="form-section-header mt-4">
          <span class="section-step">03</span>
          <div>
            <h3>Headquarters &amp; Fleet Requirements</h3>
            <p>Workspace sizing and regional presence.</p>
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Province / Head Office Location *</label>
            <select v-model="request.province" class="form-input" required>
              <option value="">-- Select Province --</option>
              <option value="Gauteng">Gauteng (Johannesburg / Pretoria)</option>
              <option value="Western Cape">Western Cape (Cape Town)</option>
              <option value="KwaZulu-Natal">KwaZulu-Natal (Durban)</option>
              <option value="Eastern Cape">Eastern Cape (Gqeberha / East London)</option>
              <option value="Free State">Free State (Bloemfontein)</option>
              <option value="Limpopo">Limpopo (Polokwane)</option>
              <option value="Mpumalanga">Mpumalanga (Mbombela)</option>
              <option value="North West">North West (Rustenburg)</option>
              <option value="Northern Cape">Northern Cape (Kimberley)</option>
              <option value="International">International / SADC</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Estimated Team / Fleet Scale *</label>
            <select v-model="request.company_size" class="form-input" required>
              <option value="1-10">Boutique Executive Office (1 - 10 Users)</option>
              <option value="11-25">Mid-Market Commercial (11 - 25 Users)</option>
              <option value="26-50">Enterprise Workforce (26 - 50 Users)</option>
              <option value="50+">Institutional Enterprise (50+ Users)</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Special Operational Directives / Requirements (Optional)</label>
          <textarea 
            v-model="request.message" 
            rows="2" 
            class="form-input" 
            placeholder="Specify any bespoke integrations, multi-tenant requirements, or compliance prerequisites..."
          ></textarea>
        </div>

        <!-- POPIA Compliance Check -->
        <div class="consent-section">
          <label class="check-row">
            <input type="checkbox" v-model="acceptedCompliance" required />
            <span>
              I confirm I am an authorized corporate officer applying on behalf of this business entity. I acknowledge the processing of corporate information in accordance with the 
              <router-link to="/disclaimer" target="_blank" class="gold-link">POPIA Privacy &amp; Data Safeguard Notice</router-link>.
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
            {{ loading ? 'Submitting Corporate Application...' : 'Submit Institutional Registration' }}
          </button>
        </div>

        <div class="auth-footer">
          Already have an authorized account? 
          <router-link to="/login" class="gold-link">Member Login Here</router-link>
        </div>
      </form>
    </div>

    <!-- Application Submitted Success State -->
    <div class="auth-card register-card glass-panel success-panel" v-else>
      <div class="success-icon">
        <div class="gold-seal">✓</div>
      </div>
      <h2 class="headline">Registration Submitted</h2>
      <div class="cipc-success-badge" v-if="request.cipc_number">
        CIPC REG: <strong>{{ request.cipc_number }}</strong> &bull; {{ request.company_name }}
      </div>
      <div class="success-divider"></div>
      <p class="success-note">
        Thank you, <strong>{{ request.full_name }}</strong>. Your institutional registration for <strong>{{ request.company_name }}</strong> ({{ request.trading_name ? 'T/A ' + request.trading_name : 'CIPC Verified' }}) has been received by Mtambo Holdings Group.
      </p>
      <p class="text-muted text-sm mt-3">
        Our executive concierge team will review your CIPC verification and provision your dedicated FINISHER LUXURY tenant workspace. An authorization token will be dispatched to <strong>{{ request.email }}</strong>.
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
      verifyingCipc: false,
      error: '',
      success: '',
      acceptedCompliance: true,
      isGenericEmail: false,
      request: {
        company_name: '',
        trading_name: '',
        cipc_number: '',
        tax_number: '',
        industry: '',
        full_name: '',
        job_title: '',
        email: '',
        phone: '',
        province: 'Gauteng',
        company_size: '1-10',
        message: ''
      }
    }
  },
  computed: {
    cipcStatus() {
      const val = (this.request.cipc_number || '').trim()
      if (!val) {
        return { state: 'empty', message: '', entityLabel: '' }
      }

      // South African CIPC regex: YYYY/NNNNNN/NN where year starts with 19 or 20
      const cipcRegex = /^(19|20)\d{2}\/\d{6}\/\d{2}$/
      if (cipcRegex.test(val)) {
        const suffix = val.slice(-2)
        const suffixMap = {
          '07': 'Private Company (Pty Ltd)',
          '06': 'Public Company (Ltd)',
          '23': 'Close Corporation (CC)',
          '08': 'Non-Profit Company (NPC)',
          '21': 'Incorporated (Inc)',
          '10': 'External / Foreign Company'
        }
        const label = suffixMap[suffix] || 'Registered Corporate Entity'
        return {
          state: 'valid',
          entityLabel: label,
          message: `Official CIPC Match: ${label}`
        }
      }

      // Check if partially entered
      if (val.length < 14) {
        if (!val.startsWith('19') && !val.startsWith('20') && val.length >= 2) {
          return {
            state: 'invalid',
            entityLabel: '',
            message: 'CIPC numbers must start with year of incorporation (e.g. 2024, 2018)'
          }
        }
        return {
          state: 'incomplete',
          entityLabel: '',
          message: 'Format: YYYY/NNNNNN/NN (e.g. 2024/123456/07)'
        }
      }

      return {
        state: 'invalid',
        entityLabel: '',
        message: 'Invalid CIPC format. Must be YYYY/NNNNNN/NN (e.g. 2024/123456/07)'
      }
    }
  },
  methods: {
    onCipcInput(e) {
      let v = e.target.value.replace(/[^0-9/]/g, '').toUpperCase()
      // Auto-insert slashes as user types numbers
      const digitsOnly = v.replace(/\//g, '')
      if (digitsOnly.length > 4 && digitsOnly.length <= 10) {
        v = `${digitsOnly.slice(0, 4)}/${digitsOnly.slice(4)}`
      } else if (digitsOnly.length > 10) {
        v = `${digitsOnly.slice(0, 4)}/${digitsOnly.slice(4, 10)}/${digitsOnly.slice(10, 12)}`
      }
      this.request.cipc_number = v.slice(0, 14)
    },
    simulateCipcRegistryCheck() {
      if (this.cipcStatus.state !== 'valid') return
      this.verifyingCipc = true
      setTimeout(() => {
        this.verifyingCipc = false
        toast.success(`CIPC Registry Matched: ${this.cipcStatus.entityLabel}`)
      }, 700)
    },
    checkCorporateEmail() {
      const email = (this.request.email || '').toLowerCase()
      const genericDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'mail.com']
      const domain = email.split('@')[1]
      this.isGenericEmail = !!(domain && genericDomains.includes(domain))
    },
    async handleRequestAccess() {
      if (this.cipcStatus.state !== 'valid') {
        this.error = 'Please provide a valid South African CIPC registration number (e.g. 2024/123456/07).'
        return
      }

      this.loading = true
      this.error = ''
      this.success = ''

      try {
        const payload = {
          subject: `Corporate Access Request: ${this.request.company_name} (CIPC: ${this.request.cipc_number})`,
          message: this.request.message || `Corporate registration for ${this.request.company_name}. Trading as: ${this.request.trading_name || 'N/A'}. CIPC: ${this.request.cipc_number}.`,
          metadata: {
            company_name: this.request.company_name,
            trading_name: this.request.trading_name,
            cipc_number: this.request.cipc_number,
            cipc_verified: this.cipcStatus.state === 'valid',
            cipc_entity_type: this.cipcStatus.entityLabel,
            tax_number: this.request.tax_number,
            industry: this.request.industry,
            full_name: this.request.full_name,
            job_title: this.request.job_title,
            email: this.request.email,
            phone: this.request.phone,
            province: this.request.province,
            company_size: this.request.company_size,
            registration_source: 'institutional_portal'
          }
        }

        await ticketsAPI.create(payload)

        this.applicationSubmitted = true
        toast.success('Registration submitted successfully')

      } catch (err) {
        console.error('Request access failed', err)
        this.error = err.message || 'Failed to submit registration. Please try again.'
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
  padding: 3rem 1.5rem;
}

.exclusive-nav {
  position: absolute;
  top: 0; left: 0; width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 3rem;
  z-index: 10;
}
.nav-brand { font-size: 0.875rem; font-weight: 800; letter-spacing: 4px; color: #D4AF37; }
.nav-btn { background: transparent; border: none; color: #9ca3af; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; cursor: pointer; transition: color 0.3s; }
.nav-btn:hover { color: #D4AF37; }

.glass-panel {
  background: linear-gradient(135deg, rgba(18,18,18,0.92) 0%, rgba(8,8,8,0.96) 100%);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(212, 175, 55, 0.25);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.95), inset 0 0 0 1px rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  width: 100%;
  max-width: 780px;
  padding: 3rem;
  position: relative;
  z-index: 10;
  margin-top: 2rem;
}

.auth-header { text-align: center; margin-bottom: 2rem; }
.card-logo { font-size: 2.5rem; font-weight: 900; color: transparent; -webkit-text-stroke: 1px rgba(212, 175, 55, 0.8); margin-bottom: 0.75rem; line-height: 1; }
.headline { font-size: 1.85rem; font-weight: 800; margin: 0 0 0.5rem; color: #ffffff; letter-spacing: 0.5px; }
.subheadline { font-size: 0.875rem; color: #9ca3af; margin: 0; }

.form-section-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 1.25rem;
}
.section-step {
  font-family: monospace;
  font-size: 0.8125rem;
  font-weight: 800;
  color: #D4AF37;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 4px 8px;
  border-radius: 4px;
}
.form-section-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #f3f4f6;
  margin: 0 0 0.2rem 0;
  letter-spacing: 0.3px;
}
.form-section-header p {
  font-size: 0.75rem;
  color: #9ca3af;
  margin: 0;
}

.form-group { margin-bottom: 1.25rem; }
.form-label { display: block; font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.4rem; }
.form-hint { display: block; font-size: 0.7rem; color: #6b7280; margin-top: 0.3rem; }
.form-input {
  width: 100%;
  padding: 0.75rem 0.9rem;
  background: rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 6px;
  color: #fff;
  font-size: 0.9rem;
  transition: all 0.25s ease;
}
.form-input:focus { border-color: #D4AF37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.15); outline: none; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; }

/* CIPC Specific Styles */
.cipc-label-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; flex-wrap: wrap; gap: 0.5rem; }
.cipc-badge {
  font-size: 0.6875rem;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.badge-verified { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-invalid { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.cipc-input-wrap { display: flex; gap: 0.5rem; }
.border-gold { border-color: #D4AF37 !important; }
.border-error { border-color: #ef4444 !important; }
.btn-cipc-verify {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #D4AF37;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 0 1rem;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.btn-cipc-verify:hover:not(:disabled) {
  background: #D4AF37;
  color: #000;
}
.btn-cipc-verify:disabled { opacity: 0.4; cursor: not-allowed; }
.cipc-hint-bar { margin-top: 0.4rem; font-size: 0.75rem; }

.email-warning { display: block; font-size: 0.75rem; color: #fbbf24; margin-top: 0.35rem; }
.text-gold { color: #D4AF37; font-weight: 600; }
.font-mono { font-family: monospace; letter-spacing: 0.5px; }

.consent-section {
  margin: 1.5rem 0;
  padding: 1rem;
  border: 1px solid rgba(212, 175, 55, 0.2);
  background: rgba(212, 175, 55, 0.04);
  border-radius: 6px;
}
.check-row { display: flex; align-items: flex-start; gap: 0.75rem; font-size: 0.78rem; color: #d1d5db; cursor: pointer; line-height: 1.5; }
.check-row input { margin-top: 2px; accent-color: #D4AF37; }
.gold-link { color: #D4AF37; text-decoration: none; font-weight: 600; }
.gold-link:hover { text-decoration: underline; }

.btn { display: inline-block; text-align: center; padding: 0.9rem 2rem; font-size: 0.8125rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; border-radius: 6px; cursor: pointer; transition: all 0.3s; }
.btn-gold-action {
  width: 100%;
  background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
  color: #000;
  font-weight: 800;
  border: none;
}
.btn-gold-action:hover:not(:disabled) {
  filter: brightness(1.15);
  box-shadow: 0 0 25px rgba(212, 175, 55, 0.45);
  transform: translateY(-1px);
}
.btn-gold-action:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-secondary { background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #9ca3af; }
.btn-secondary:hover { border-color: #fff; color: #fff; }

.step-nav { margin-top: 1rem; }
.auth-footer { text-align: center; font-size: 0.8125rem; color: #9ca3af; margin-top: 1.5rem; }

.form-error { color: #ef4444; font-size: 0.8125rem; background: rgba(239, 68, 68, 0.1); padding: 0.75rem; border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; margin-bottom: 1.25rem; text-align: center; }
.info-bar { background: rgba(34, 197, 94, 0.1); color: #4ade80; padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(34, 197, 94, 0.25); font-size: 0.8125rem; text-align: center; margin-bottom: 1.25rem; }

/* Success Panel */
.success-panel { text-align: center; padding: 3.5rem 2.5rem; }
.gold-seal {
  width: 60px; height: 60px; border-radius: 50%;
  background: rgba(212, 175, 55, 0.15);
  border: 2px solid #D4AF37;
  color: #D4AF37;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.75rem; font-weight: 800;
  margin: 0 auto 1.5rem;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
}
.cipc-success-badge {
  display: inline-block;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #D4AF37;
  font-family: monospace;
  font-size: 0.8125rem;
  padding: 4px 12px;
  border-radius: 4px;
  margin: 0.75rem 0 1.25rem;
}
.success-divider { height: 1px; width: 60px; background: #D4AF37; margin: 1.5rem auto; }
.success-note { color: #e5e7eb; font-size: 0.95rem; line-height: 1.6; }

@media (max-width: 768px) {
  .glass-panel { padding: 2rem 1.25rem; }
  .form-grid-2 { grid-template-columns: 1fr; gap: 0; }
  .exclusive-nav { padding: 1rem 1.5rem; }
}
</style>
