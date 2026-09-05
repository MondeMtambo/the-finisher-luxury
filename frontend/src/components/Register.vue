<template>
  <div class="auth-page luxury-auth-bg" :data-theme="currentTheme">
    <!-- Ambient Background Particles -->
    <div class="particles">
      <div class="particle" v-for="n in 15" :key="n"></div>
    </div>

    <!-- Exclusive Header Bar -->
    <nav class="exclusive-nav">
      <div class="nav-brand-group">
        <div class="brand-crest">F</div>
        <div class="brand-text">
          <span class="brand-title">THE FINISHER</span>
          <span class="brand-edition">LUXURY PRIVATE OS</span>
        </div>
      </div>
      <div class="nav-actions">
        <button class="theme-pill-btn" @click="toggleTheme" :title="currentTheme === 'dark' ? 'Switch to Light' : 'Switch to Dark'">
          {{ currentTheme === 'dark' ? '☀️ Light' : '🌙 Dark' }}
        </button>
        <button class="nav-btn" @click="$router.push('/login')">Member Login</button>
      </div>
    </nav>

    <!-- Step Progress Indicator -->
    <div class="wizard-progress-bar" v-if="currentStep < 4">
      <div class="progress-step" :class="{ active: currentStep === 1, completed: currentStep > 1 }" @click="currentStep > 1 && currentStep < 3 && (currentStep = 1)">
        <div class="step-bubble">1</div>
        <span class="step-label">Applicant Auth</span>
      </div>
      <div class="progress-line" :class="{ active: currentStep > 1 }"></div>
      <div class="progress-step" :class="{ active: currentStep === 2, completed: currentStep > 2 }" @click="currentStep > 2 && currentStep < 3 && (currentStep = 2)">
        <div class="step-bubble">2</div>
        <span class="step-label">Corporate Dossier</span>
      </div>
      <div class="progress-line" :class="{ active: currentStep > 2 }"></div>
      <div class="progress-step" :class="{ active: currentStep === 3, completed: currentStep > 3 }">
        <div class="step-bubble">3</div>
        <span class="step-label">5-Min Verification</span>
      </div>
    </div>

    <!-- STEP 1: Applicant & Executive Authentication -->
    <div class="auth-card register-card glass-panel" v-if="currentStep === 1">
      <div class="auth-header">
        <div class="vip-badge-pill">
          <span class="vip-badge-dot"></span>
          ⭐ 7-DAY VIP EXECUTIVE ACCESS &middot; CORPORATE ONBOARDING
        </div>
        <div class="scarcity-pill-banner">
          <span class="scarcity-fire">🔥</span>
          <span>Strictly Limited: <strong>Only 15 Private Fleet Allocations Active</strong> &mdash; Secure Your Space Now</span>
        </div>
        <h1 class="headline">Request Executive Access</h1>
        <p class="subheadline">Step 1: Verify your authorized executive credentials to initiate corporate workspace provisioning.</p>
      </div>

      <form @submit.prevent="proceedToStep2" class="reg-form">
        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">First Name *</label>
            <input 
              v-model="form.first_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Monde" 
              required 
              autofocus
            />
          </div>
          <div class="form-group">
            <label class="form-label">Last Name *</label>
            <input 
              v-model="form.last_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Mtambo" 
              required 
            />
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Corporate Designation / Role *</label>
            <select v-model="form.job_title" class="form-input form-select" required>
              <option value="" disabled>Select your corporate designation</option>
              <option value="Chief Executive Officer (CEO)">Chief Executive Officer (CEO)</option>
              <option value="Managing Director (MD)">Managing Director (MD)</option>
              <option value="Founder / Principal Owner">Founder / Principal Owner</option>
              <option value="Chief Operating Officer (COO)">Chief Operating Officer (COO)</option>
              <option value="Chief Financial Officer (CFO)">Chief Financial Officer (CFO)</option>
              <option value="Vice President / Partner">Vice President / Partner</option>
              <option value="Head of Operations / Revenue">Head of Operations / Revenue</option>
              <option value="Associate / Senior Officer">Associate / Senior Officer</option>
              <option value="Other Corporate Officer">Other Corporate Officer</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Direct Phone Number *</label>
            <input 
              v-model="form.phone" 
              type="tel" 
              class="form-input" 
              placeholder="+27 (0) 82 000 0000" 
              required 
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Corporate Work Email *</label>
          <input 
            v-model="form.email" 
            type="email" 
            class="form-input" 
            placeholder="executive@company.co.za" 
            @blur="checkCorporateEmail"
            required 
          />
          <span class="form-hint" v-if="isGenericEmail" style="color:#f59e0b">
            Enterprise Note: Using your corporate domain (e.g. @company.co.za) expedites priority workspace provisioning.
          </span>
        </div>

        <!-- CEO Toggle -->
        <div class="toggle-card">
          <label class="toggle-row">
            <input type="checkbox" v-model="form.is_ceo" class="toggle-checkbox" @change="onCEOToggleChange" />
            <div class="toggle-info">
              <span class="toggle-title">I am the Chief Executive Officer (CEO) / Principal Officer</span>
              <span class="toggle-desc">Check if you are establishing a new corporate organization with principal signing authority.</span>
            </div>
          </label>

          <!-- CEO SEARCH ENGINE (When applicant is NOT the CEO) -->
          <div v-if="!form.is_ceo" class="ceo-search-engine-wrap">
            <div class="ceo-search-header">
              <span class="search-engine-title">🔍 Search Registered CEO / Enterprise Organization</span>
              <p class="search-engine-desc">
                Only verified Chief Executive Officers can establish new workspaces. As a corporate officer, please search for your registered CEO or company name to associate your access request.
              </p>
            </div>

            <!-- Active Selection Card -->
            <div v-if="selectedCEO" class="selected-ceo-card">
              <div class="selected-ceo-info">
                <div class="selected-badge">✓ VERIFIED ENTERPRISE CONNECTED</div>
                <div class="selected-org-name">{{ selectedCEO.company_name }}</div>
                <div class="selected-ceo-name">
                  Principal Executive: <strong>{{ selectedCEO.ceo_name }}</strong> ({{ selectedCEO.job_title }})
                </div>
              </div>
              <button type="button" class="btn-change-ceo" @click="clearSelectedCEO">
                Change Selection
              </button>
            </div>

            <!-- Live Search Bar -->
            <div v-else class="search-bar-wrap">
              <div class="search-input-box">
                <span class="search-lens-icon">🔎</span>
                <input 
                  type="text" 
                  class="form-input search-input" 
                  v-model="ceoSearchQuery" 
                  @input="handleCEOSearchInput" 
                  placeholder="Type CEO Name (e.g. Adrian Gore, Monde Mtambo) or Company Name..."
                />
                <span v-if="searchingCEO" class="search-spinner"></span>
              </div>

              <!-- Live Search Results Dropdown / Cards -->
              <div v-if="ceoSearchResults.length > 0" class="search-results-list">
                <div 
                  v-for="(res, idx) in ceoSearchResults" 
                  :key="idx" 
                  class="search-result-item"
                  @click="selectCEO(res)"
                >
                  <div class="result-crest">F</div>
                  <div class="result-details">
                    <div class="result-company">
                      {{ res.company_name }}
                      <span v-if="res.is_verified" class="verified-pill">✓ CIPC Verified</span>
                    </div>
                    <div class="result-ceo">
                      Executive: <strong>{{ res.ceo_name }}</strong> &middot; <span class="text-gold">{{ res.job_title }}</span>
                    </div>
                  </div>
                  <button type="button" class="btn-connect-pill">
                    Connect &rarr;
                  </button>
                </div>
              </div>

              <!-- No Results Warning -->
              <div v-else-if="ceoSearchQuery.trim().length >= 2 && !searchingCEO" class="no-results-alert">
                <div class="alert-icon">⚠️</div>
                <div class="alert-content">
                  <strong>No registered CEO or Company found matching "{{ ceoSearchQuery }}".</strong>
                  <p>
                    You cannot apply on behalf of an unverified organization. If you are establishing this enterprise as the authorized CEO, please check <strong>"I am the Chief Executive Officer"</strong> above to register your workspace.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Automated Enterprise Credentials Notification Badge (NO MANUAL PASSWORD INPUT) -->
        <div class="credentials-info-card">
          <div class="credentials-info-icon">🔑</div>
          <div class="credentials-info-text">
            <span class="credentials-info-title">Automated Secure Enterprise Credentials</span>
            <span class="credentials-info-desc">
              To guarantee zero-trust compliance, a high-entropy workspace password will be auto-generated by the system and dispatched directly to your corporate email (<strong>{{ form.email || 'your email' }}</strong>) upon executive authorization.
            </span>
          </div>
        </div>

        <div v-if="step1Error" class="form-error">{{ step1Error }}</div>

        <div class="step-nav">
          <button 
            type="submit" 
            class="btn btn-primary btn-gold-action"
            :disabled="!form.is_ceo && !selectedCEO"
          >
            {{ (!form.is_ceo && !selectedCEO) ? 'Select Verified CEO Above to Proceed' : 'Proceed to Step 2: Company Dossier →' }}
          </button>
        </div>

        <div class="auth-footer">
          Already have an authorized workspace? 
          <router-link to="/login" class="gold-link">Member Login Here</router-link>
        </div>
      </form>
    </div>

    <!-- STEP 2: Company Dossier & Physical / Postal Address -->
    <div class="auth-card register-card glass-panel" v-if="currentStep === 2">
      <div class="auth-header">
        <div class="vip-badge-pill">
          <span class="vip-badge-dot"></span>
          STEP 2 OF 2 &middot; CORPORATE DOSSIER
        </div>
        <h1 class="headline">Corporate Entity Dossier</h1>
        <p class="subheadline">
          {{ form.is_ceo 
              ? 'Provide legal entity details for multi-tenant POPIA Section 19 isolation and compliance verification.' 
              : `Associating workspace access with ${form.company_name} under CEO ${form.target_ceo_name}.` }}
        </p>
      </div>

      <form @submit.prevent="handleFinalSubmit" class="reg-form">
        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">Company Legal Registered Name *</label>
            <input 
              v-model="form.company_name" 
              type="text" 
              class="form-input" 
              :placeholder="form.is_ceo ? 'e.g. Apex Strategic Holdings (Pty) Ltd' : 'Corporate Entity'" 
              :readonly="!form.is_ceo"
              required 
            />
            <span v-if="!form.is_ceo" class="form-hint text-gold">
              ✓ Locked to registered entity associated with CEO {{ form.target_ceo_name }}.
            </span>
          </div>

          <div class="form-group">
            <label class="form-label">Trading Name (Trading As - T/A)</label>
            <input 
              v-model="form.trading_name" 
              type="text" 
              class="form-input" 
              placeholder="e.g. Apex Strategic" 
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Industry Sector *</label>
          <select v-model="form.industry" class="form-input form-select" required>
            <option value="consulting">Consulting &amp; Professional Services</option>
            <option value="finance">Finance, Banking &amp; Private Equity</option>
            <option value="it">Information Technology &amp; Software</option>
            <option value="real_estate">Real Estate &amp; Property Development</option>
            <option value="construction">Construction &amp; Engineering</option>
            <option value="healthcare">Healthcare &amp; Pharmaceuticals</option>
            <option value="logistics">Logistics, Supply Chain &amp; Freight</option>
            <option value="manufacturing">Manufacturing &amp; Industrial</option>
            <option value="legal">Legal, Audit &amp; Compliance</option>
            <option value="other">Other Enterprise Sector</option>
          </select>
        </div>

        <!-- Physical Business Address -->
        <div class="address-card">
          <div class="address-header">
            <span class="address-title">🏢 Physical Business Address *</span>
          </div>

          <div class="form-group">
            <label class="form-label">Street Address &amp; Suite / Office Number *</label>
            <input 
              v-model="form.physical_address" 
              type="text" 
              class="form-input" 
              placeholder="e.g. 5th Floor, Sandton City Office Tower, 83 Rivonia Rd" 
              required 
            />
          </div>

          <div class="form-grid-3">
            <div class="form-group">
              <label class="form-label">City *</label>
              <input 
                v-model="form.city" 
                type="text" 
                class="form-input" 
                placeholder="Johannesburg" 
                required 
              />
            </div>
            <div class="form-group">
              <label class="form-label">Province *</label>
              <select v-model="form.province" class="form-input form-select" required>
                <option value="Gauteng">Gauteng</option>
                <option value="Western Cape">Western Cape</option>
                <option value="KwaZulu-Natal">KwaZulu-Natal</option>
                <option value="Eastern Cape">Eastern Cape</option>
                <option value="Free State">Free State</option>
                <option value="Mpumalanga">Mpumalanga</option>
                <option value="Limpopo">Limpopo</option>
                <option value="North West">North West</option>
                <option value="Northern Cape">Northern Cape</option>
                <option value="International">International</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Postal Code *</label>
              <input 
                v-model="form.postal_code" 
                type="text" 
                class="form-input" 
                placeholder="2196" 
                required 
              />
            </div>
          </div>
        </div>

        <!-- Postal Address -->
        <div class="address-card">
          <div class="address-header flex-between">
            <span class="address-title">📬 Postal Address</span>
            <label class="same-as-physical">
              <input type="checkbox" v-model="sameAsPhysical" @change="syncPostalAddress" />
              <span>Same as Physical Address</span>
            </label>
          </div>

          <div class="form-group" v-if="!sameAsPhysical">
            <label class="form-label">Postal Address Details</label>
            <input 
              v-model="form.postal_address" 
              type="text" 
              class="form-input" 
              placeholder="e.g. P.O. Box 78123, Sandton, 2146" 
            />
          </div>
          <div v-else class="synced-badge">
            ✓ Postal address synchronized with physical address.
          </div>
        </div>

        <!-- CIPC & SARS -->
        <div class="form-grid-2">
          <div class="form-group">
            <label class="form-label">CIPC Registration Number</label>
            <input 
              v-model="form.cipc_number" 
              type="text" 
              class="form-input" 
              placeholder="e.g. 2024/123456/07" 
            />
            <span class="form-hint">Optional: Enables instant CIPC verification badge.</span>
          </div>

          <div class="form-group">
            <label class="form-label">SARS Tax / VAT Number</label>
            <input 
              v-model="form.tax_number" 
              type="text" 
              class="form-input" 
              placeholder="e.g. 9123456789" 
            />
            <span class="form-hint">Optional: Required for B2B tax invoicing.</span>
          </div>
        </div>

        <!-- POPIA Consent -->
        <div class="consent-section">
          <label class="check-row">
            <input type="checkbox" v-model="acceptedCompliance" required />
            <span>
              I confirm I am an authorized corporate officer applying on behalf of this business entity. 
              I agree to the processing of enterprise information in compliance with the 
              <router-link to="/disclaimer" target="_blank" class="gold-link">POPIA Section 19 Data Safeguard Policy</router-link>.
            </span>
          </label>
        </div>

        <div v-if="error" class="form-error">{{ error }}</div>

        <div class="step-nav flex-between">
          <button type="button" class="btn btn-secondary" @click="currentStep = 1">
            &larr; Back to Step 1
          </button>
          <button 
            type="submit" 
            class="btn btn-primary btn-gold-action" 
            :disabled="loading || !acceptedCompliance"
          >
            {{ loading ? 'Transmitting Application...' : '⚡ Submit Corporate Access Application' }}
          </button>
        </div>
      </form>
    </div>

    <!-- STEP 3: 5-Minute Ephemeral Identity Verification -->
    <div class="auth-card register-card glass-panel" v-if="currentStep === 3">
      <div class="auth-header">
        <div class="vip-badge-pill">
          <span class="vip-badge-dot"></span>
          ⏱️ 5-MINUTE EPHEMERAL VERIFICATION &middot; ZERO-TRUST SECURITY
        </div>
        <h1 class="headline">Confirm Corporate Identity</h1>
        <p class="subheadline">Step 3: Verify your corporate email to submit your dossier for executive review.</p>
      </div>

      <!-- Ephemeral Countdown Timer Card -->
      <div class="ephemeral-timer-card" style="background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; text-align: center;">
        <div style="font-size: 0.75rem; font-weight: 800; letter-spacing: 1.5px; color: #d4af37; margin-bottom: 0.25rem;">
          SESSION SECURITY COUNTDOWN (5-MINUTE PURGE)
        </div>
        <div class="font-mono" style="font-size: 2.4rem; font-weight: 800; color: #fff; letter-spacing: 2px; margin: 0.25rem 0;">
          {{ formattedTimeLeft }}
        </div>
        <div style="font-size: 0.78rem; color: #9ca3af; line-height: 1.4; max-width: 460px; margin: 0 auto;">
          In accordance with enterprise zero-trust protocol and POPIA Section 19, unverified application records are automatically wiped and permanently purged from the database after 5 minutes.
        </div>
      </div>

      <div v-if="verificationExpired" class="alert-box danger-box mb-4" style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); padding: 1.25rem; border-radius: 8px; text-align: center;">
        <h4 style="color: #fca5a5; margin: 0 0 0.5rem 0; font-size: 1.1rem;">⏱️ 5-Minute Verification Window Expired</h4>
        <p style="color: #e5e7eb; font-size: 0.85rem; margin-bottom: 1rem;">
          Your temporary application record has been permanently purged from the database for security compliance.
        </p>
        <button type="button" class="btn btn-gold btn-sm" @click="restartRegistration">
          🔄 Restart Application
        </button>
      </div>

      <form v-else @submit.prevent="verifyAndSubmit" class="reg-form">
        <div class="form-group" style="text-align: center;">
          <label class="form-label" style="display: block; margin-bottom: 0.5rem;">Enter 6-Digit Verification Code *</label>
          <input 
            v-model="verificationInput" 
            type="text" 
            class="form-input font-mono" 
            style="font-size: 1.5rem; letter-spacing: 8px; text-align: center; max-width: 260px; margin: 0 auto;"
            placeholder="••••••" 
            maxlength="6"
            required 
            autofocus
          />
          <span class="form-hint" style="color: #9ca3af; margin-top: 0.5rem; display: block;">
            Code dispatched to: <strong>{{ form.email }}</strong> (Check your email inbox)
          </span>
        </div>

        <div v-if="verificationError" class="form-error">{{ verificationError }}</div>

        <div class="step-nav" style="margin-top: 1.5rem;">
          <button 
            type="submit" 
            class="btn btn-primary btn-gold-action"
            :disabled="verifying || verificationInput.trim().length !== 6"
          >
            {{ verifying ? 'Verifying Identity...' : '🔒 Verify & Submit Application →' }}
          </button>
        </div>

        <div class="auth-footer" style="margin-top: 1rem; text-align: center;">
          Didn't receive code? 
          <button type="button" class="gold-link" style="background: none; border: none; cursor: pointer; text-decoration: underline;" @click="handleFinalSubmit" :disabled="loading">
            Resend Code
          </button>
        </div>
      </form>
    </div>

    <!-- STEP 4: Executive Review Confirmation Screen -->
    <div class="auth-card register-card glass-panel success-panel" v-if="currentStep === 4">
      <div class="success-icon-wrap">
        <div class="gold-seal-crest">
          <span class="seal-f">F</span>
        </div>
      </div>
      <div class="vip-badge-pill">
        <span class="vip-badge-dot"></span>
        APPLICATION UNDER REVIEW &middot; MTAMBO HOLDINGS
      </div>
      <h2 class="headline success-headline">Application Submitted For Executive Review</h2>
      <div class="success-divider"></div>

      <div class="review-dossier-card">
        <div class="dossier-row">
          <span class="dossier-key">Corporate Entity:</span>
          <span class="dossier-val highlight-gold">{{ form.company_name }}</span>
        </div>
        <div class="dossier-row">
          <span class="dossier-key">Principal Officer:</span>
          <span class="dossier-val">{{ form.first_name }} {{ form.last_name }} ({{ form.job_title }})</span>
        </div>
        <div class="dossier-row" v-if="!form.is_ceo && form.target_ceo_name">
          <span class="dossier-key">Target Verified CEO:</span>
          <span class="dossier-val">{{ form.target_ceo_name }}</span>
        </div>
        <div class="dossier-row">
          <span class="dossier-key">Official Work Email:</span>
          <span class="dossier-val">{{ form.email }}</span>
        </div>
        <div class="dossier-row">
          <span class="dossier-key">Physical Headquarters:</span>
          <span class="dossier-val">{{ form.physical_address }}, {{ form.city }}, {{ form.province }} {{ form.postal_code }}</span>
        </div>
        <div class="dossier-row">
          <span class="dossier-key">Allocation Tier:</span>
          <span class="dossier-val highlight-gold">7-Day VIP Executive Private OS</span>
        </div>
        <div class="dossier-row">
          <span class="dossier-key">Executive Dispatch:</span>
          <span class="dossier-val">noreply@mtamboholdings.dev</span>
        </div>
      </div>

      <p class="success-note">
        Your corporate access dossier has been verified and transmitted to the executive registrations desk (<strong>noreply@mtamboholdings.dev</strong>).
      </p>
      <p class="text-muted text-sm mt-3">
        Upon 1-click authorization by the Executive Directorate, your <strong>auto-generated secure password</strong> and direct workspace portal URL will be dispatched to <strong>{{ form.email }}</strong>.
      </p>

      <div class="mt-4 success-actions">
        <button class="btn btn-primary btn-gold-action" @click="$router.push('/login')">
          Return to Member Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { accessRequestsAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'Register',
  data() {
    return {
      currentStep: 1,
      currentTheme: localStorage.getItem('finisher_theme') || 'dark',
      loading: false,
      error: '',
      step1Error: '',
      acceptedCompliance: true,
      sameAsPhysical: true,
      isGenericEmail: false,

      // CEO Search Engine State
      ceoSearchQuery: '',
      searchingCEO: false,
      ceoSearchResults: [],
      ceoSearchTimer: null,
      selectedCEO: null,

      // 5-Minute TTL Ephemeral Verification State
      activeRequestId: null,
      verificationInput: '',
      verificationError: '',
      verifying: false,
      timerSecondsLeft: 300,
      verificationTimer: null,
      verificationExpired: false,

      form: {
        first_name: '',
        last_name: '',
        job_title: 'Chief Executive Officer (CEO)',
        email: '',
        phone: '',
        is_ceo: true,
        target_ceo_name: '',
        target_organization_id: '',
        company_name: '',
        trading_name: '',
        industry: 'consulting',
        physical_address: '',
        city: 'Johannesburg',
        province: 'Gauteng',
        postal_code: '',
        postal_address: '',
        cipc_number: '',
        tax_number: ''
      }
    }
  },
  computed: {
    formattedTimeLeft() {
      const mins = Math.floor(this.timerSecondsLeft / 60)
      const secs = this.timerSecondsLeft % 60
      return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    }
  },
  beforeUnmount() {
    if (this.verificationTimer) clearInterval(this.verificationTimer)
  },
  mounted() {
    document.documentElement.setAttribute('data-theme', this.currentTheme)
  },
  methods: {
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('finisher_theme', this.currentTheme)
      document.documentElement.setAttribute('data-theme', this.currentTheme)
    },
    checkCorporateEmail() {
      const email = (this.form.email || '').toLowerCase()
      const genericDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'mail.com']
      const domain = email.split('@')[1]
      this.isGenericEmail = !!(domain && genericDomains.includes(domain))
    },
    onCEOToggleChange() {
      if (this.form.is_ceo) {
        this.selectedCEO = null
        this.form.target_ceo_name = ''
        this.form.target_organization_id = ''
        this.step1Error = ''
      }
    },
    handleCEOSearchInput() {
      if (this.ceoSearchTimer) clearTimeout(this.ceoSearchTimer)
      const q = this.ceoSearchQuery.trim()
      if (q.length < 2) {
        this.ceoSearchResults = []
        this.searchingCEO = false
        return
      }

      this.searchingCEO = true
      this.ceoSearchTimer = setTimeout(async () => {
        try {
          const res = await accessRequestsAPI.searchCEO(q)
          this.ceoSearchResults = Array.isArray(res.data) ? res.data : []
        } catch (err) {
          console.warn('CEO search error:', err)
          this.ceoSearchResults = []
        } finally {
          this.searchingCEO = false
        }
      }, 350)
    },
    selectCEO(ceoRecord) {
      this.selectedCEO = ceoRecord
      this.form.company_name = ceoRecord.company_name
      this.form.target_ceo_name = ceoRecord.ceo_name
      this.form.target_organization_id = ceoRecord.organization_id
      this.ceoSearchResults = []
      this.ceoSearchQuery = ''
      this.step1Error = ''
      toast.success('Enterprise Selected', `Linked to ${ceoRecord.company_name} (CEO: ${ceoRecord.ceo_name})`)
    },
    clearSelectedCEO() {
      this.selectedCEO = null
      this.form.company_name = ''
      this.form.target_ceo_name = ''
      this.form.target_organization_id = ''
      this.ceoSearchQuery = ''
      this.ceoSearchResults = []
    },
    syncPostalAddress() {
      if (this.sameAsPhysical) {
        this.form.postal_address = `${this.form.physical_address}, ${this.form.city}, ${this.form.province} ${this.form.postal_code}`
      }
    },
    proceedToStep2() {
      this.step1Error = ''
      if (!this.form.first_name || !this.form.last_name) {
        this.step1Error = 'Please enter your first and last name.'
        return
      }
      if (!this.form.email || !this.form.phone) {
        this.step1Error = 'Please enter your work email and direct phone number.'
        return
      }
      if (!this.form.is_ceo && !this.selectedCEO) {
        this.step1Error = 'Non-CEOs must search and connect with a verified registered CEO / Company in the system.'
        return
      }

      this.currentStep = 2
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    async handleFinalSubmit() {
      if (!this.form.company_name) {
        this.error = 'Please provide the company name.'
        return
      }
      if (!this.form.physical_address || !this.form.city || !this.form.postal_code) {
        this.error = 'Please provide complete physical address details.'
        return
      }
      if (!this.acceptedCompliance) {
        this.error = 'Please acknowledge the POPIA Section 19 compliance notice.'
        return
      }

      this.loading = true
      this.error = ''

      try {
        const payload = {
          first_name: this.form.first_name,
          last_name: this.form.last_name,
          job_title: this.form.job_title,
          email: this.form.email,
          phone: this.form.phone,
          is_ceo: this.form.is_ceo,
          target_ceo_name: this.form.target_ceo_name,
          target_organization_id: this.form.target_organization_id,
          company_name: this.form.company_name,
          trading_name: this.form.trading_name,
          industry: this.form.industry,
          physical_address: this.form.physical_address,
          city: this.form.city,
          province: this.form.province,
          postal_code: this.form.postal_code,
          postal_address: this.sameAsPhysical 
            ? `${this.form.physical_address}, ${this.form.city}, ${this.form.province} ${this.form.postal_code}`
            : (this.form.postal_address || this.form.physical_address),
          cipc_number: this.form.cipc_number,
          tax_number: this.form.tax_number
        }

        const res = await accessRequestsAPI.submitPublic(payload)

        this.activeRequestId = res.data?.request_id
        this.verificationInput = ''
        this.verificationError = ''
        this.verificationExpired = false
        this.currentStep = 3
        this.start5MinuteTimer()
        toast.info('Verification Code Dispatched', 'You have 5 minutes to verify your application.')
        window.scrollTo({ top: 0, behavior: 'smooth' })

      } catch (err) {
        console.error('Corporate request submission error:', err)
        const msg = err.response?.data?.error || err.response?.data?.message || err.message || 'Unable to submit application at this time.'
        this.error = msg
        toast.error('Submission Failed', msg)
      } finally {
        this.loading = false
      }
    },
    start5MinuteTimer() {
      if (this.verificationTimer) clearInterval(this.verificationTimer)
      this.timerSecondsLeft = 300
      this.verificationExpired = false
      this.verificationTimer = setInterval(() => {
        this.timerSecondsLeft--
        if (this.timerSecondsLeft <= 0) {
          clearInterval(this.verificationTimer)
          this.verificationExpired = true
          this.handleTimerExpired()
        }
      }, 1000)
    },
    async handleTimerExpired() {
      if (this.activeRequestId) {
        try {
          await accessRequestsAPI.cancelPublic(this.activeRequestId)
        } catch (e) {
          console.warn('Auto-purge cancel error:', e)
        }
      }
    },
    restartRegistration() {
      this.currentStep = 1
      this.verificationExpired = false
      this.activeRequestId = null
      this.verificationInput = ''
      this.verificationError = ''
      if (this.verificationTimer) clearInterval(this.verificationTimer)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    async verifyAndSubmit() {
      if (!this.verificationInput || this.verificationInput.trim().length !== 6) {
        this.verificationError = 'Please enter your 6-digit verification code.'
        return
      }

      this.verifying = true
      this.verificationError = ''

      try {
        await accessRequestsAPI.verifyPublic({
          request_id: this.activeRequestId,
          verification_code: this.verificationInput.trim()
        })

        if (this.verificationTimer) clearInterval(this.verificationTimer)
        this.currentStep = 4
        toast.success('Identity Verified', 'Application submitted for executive review.')
        window.scrollTo({ top: 0, behavior: 'smooth' })

      } catch (err) {
        console.error('Verification error:', err)
        const msg = err.response?.data?.error || err.response?.data?.message || err.message || 'Verification failed.'
        this.verificationError = msg
        if (msg.toLowerCase().includes('expired')) {
          this.verificationExpired = true
        }
      } finally {
        this.verifying = false
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
  padding: 6rem 1.5rem 3rem;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  position: relative;
  overflow-x: hidden;
  transition: background 0.3s ease, color 0.3s ease;
}

/* Dark Theme Background */
.auth-page[data-theme="dark"] {
  background: radial-gradient(circle at 50% 20%, #151922 0%, #0b0f19 70%, #05070d 100%);
  color: #f3f4f6;
}

/* Light Theme Background */
.auth-page[data-theme="light"] {
  background: radial-gradient(circle at 50% 20%, #fdfbf7 0%, #f1f5f9 60%, #e2e8f0 100%);
  color: #0f172a;
}

/* Background floating particles */
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.25);
  animation: floatParticle 8s infinite ease-in-out;
}
.particle:nth-child(odd) { width: 6px; height: 6px; animation-duration: 9s; }
.particle:nth-child(even) { width: 10px; height: 10px; animation-duration: 7s; }
.particle:nth-child(1) { left: 8%; top: 20%; animation-delay: 0s; }
.particle:nth-child(2) { left: 25%; top: 70%; animation-delay: 1.5s; }
.particle:nth-child(3) { left: 45%; top: 15%; animation-delay: 3s; }
.particle:nth-child(4) { left: 65%; top: 80%; animation-delay: 0.5s; }
.particle:nth-child(5) { left: 85%; top: 30%; animation-delay: 2s; }

@keyframes floatParticle {
  0% { transform: translateY(0) scale(1); opacity: 0.2; }
  50% { transform: translateY(-30px) scale(1.3); opacity: 0.6; }
  100% { transform: translateY(0) scale(1); opacity: 0.2; }
}

/* Exclusive Header Bar */
.exclusive-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 1.25rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(16px);
  z-index: 50;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}
.auth-page[data-theme="dark"] .exclusive-nav {
  background: rgba(11, 15, 25, 0.85);
}
.auth-page[data-theme="light"] .exclusive-nav {
  background: rgba(255, 255, 255, 0.88);
}

.nav-brand-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.brand-crest {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: linear-gradient(135deg, #d4af37, #b48608);
  color: #000;
  font-weight: 900;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.35);
}
.brand-text {
  display: flex;
  flex-direction: column;
}
.brand-title {
  font-weight: 800;
  font-size: 1.05rem;
  letter-spacing: 0.12em;
  color: #d4af37;
}
.brand-edition {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  opacity: 0.7;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.theme-pill-btn {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #d4af37;
  padding: 0.45rem 0.9rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.theme-pill-btn:hover {
  background: rgba(212, 175, 55, 0.25);
  transform: translateY(-1px);
}
.nav-btn {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(212, 175, 55, 0.05));
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: #d4af37;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.nav-btn:hover {
  background: #d4af37;
  color: #000;
  box-shadow: 0 4px 14px rgba(212, 175, 55, 0.4);
}

/* Wizard Progress Bar */
.wizard-progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 620px;
  width: 100%;
  margin: 0 auto 2rem;
  z-index: 10;
}
.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  cursor: default;
}
.progress-step.completed {
  cursor: pointer;
}
.step-bubble {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid rgba(212, 175, 55, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  background: rgba(0, 0, 0, 0.2);
  color: #9ca3af;
  transition: all 0.3s ease;
}
.progress-step.active .step-bubble {
  border-color: #d4af37;
  background: #d4af37;
  color: #000;
  box-shadow: 0 0 16px rgba(212, 175, 55, 0.5);
}
.progress-step.completed .step-bubble {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}
.step-label {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: #9ca3af;
}
.progress-step.active .step-label {
  color: #d4af37;
}
.progress-line {
  flex: 1;
  height: 2px;
  background: rgba(212, 175, 55, 0.2);
  margin: 0 0.75rem 1.25rem;
  transition: all 0.3s;
}
.progress-line.active {
  background: #d4af37;
}

/* Glass Card */
.register-card {
  width: 100%;
  max-width: 760px;
  padding: 2.75rem;
  border-radius: 16px;
  z-index: 10;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
  transition: all 0.3s;
}
.auth-page[data-theme="dark"] .register-card {
  background: rgba(17, 23, 35, 0.85);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(212, 175, 55, 0.3);
}
.auth-page[data-theme="light"] .register-card {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(212, 175, 55, 0.4);
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.15);
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}
.vip-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 1rem;
  border-radius: 20px;
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #d4af37;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  margin-bottom: 1rem;
}
.vip-badge-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #d4af37;
  box-shadow: 0 0 8px #d4af37;
  animation: pulseDot 2s infinite;
}
@keyframes pulseDot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.5; }
}

.headline {
  font-size: 1.85rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 0.5rem;
}
.auth-page[data-theme="dark"] .headline { color: #ffffff; }
.auth-page[data-theme="light"] .headline { color: #0f172a; }

.subheadline {
  font-size: 0.92rem;
  opacity: 0.75;
  margin: 0 auto;
  max-width: 580px;
  line-height: 1.5;
}

/* Form Structure */
.reg-form {
  display: flex;
  flex-direction: column;
  gap: 1.35rem;
}
.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.form-grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
}
@media (max-width: 680px) {
  .form-grid-2, .form-grid-3 {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}
.form-label {
  font-size: 0.85rem;
  font-weight: 600;
}
.auth-page[data-theme="dark"] .form-label { color: #d1d5db; }
.auth-page[data-theme="light"] .form-label { color: #334155; }

.form-input {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  width: 100%;
  box-sizing: border-box;
}
.auth-page[data-theme="dark"] .form-input {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #fff;
}
.auth-page[data-theme="light"] .form-input {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #0f172a;
}
.form-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.25);
}
.form-select {
  appearance: auto;
}
.form-hint {
  font-size: 0.75rem;
  opacity: 0.8;
  margin-top: 0.2rem;
}

/* Toggle Card */
.toggle-card {
  padding: 1.2rem;
  border-radius: 10px;
  background: rgba(212, 175, 55, 0.05);
  border: 1px solid rgba(212, 175, 55, 0.25);
}
.toggle-row {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  cursor: pointer;
}
.toggle-checkbox {
  width: 20px;
  height: 20px;
  accent-color: #d4af37;
  margin-top: 2px;
}
.toggle-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.toggle-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: #d4af37;
}
.toggle-desc {
  font-size: 0.78rem;
  opacity: 0.75;
}

/* CEO SEARCH ENGINE STYLES */
.ceo-search-engine-wrap {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px dashed rgba(212, 175, 55, 0.25);
}
.ceo-search-header {
  margin-bottom: 0.75rem;
}
.search-engine-title {
  font-weight: 700;
  font-size: 0.88rem;
  color: #d4af37;
}
.search-engine-desc {
  font-size: 0.8rem;
  opacity: 0.8;
  margin: 0.25rem 0 0.75rem;
  line-height: 1.45;
}

.search-bar-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.search-input-box {
  position: relative;
  display: flex;
  align-items: center;
}
.search-lens-icon {
  position: absolute;
  left: 0.85rem;
  font-size: 0.95rem;
  opacity: 0.7;
}
.search-input {
  padding-left: 2.6rem !important;
  padding-right: 2.5rem !important;
}
.search-spinner {
  position: absolute;
  right: 0.85rem;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(212, 175, 55, 0.2);
  border-top-color: #d4af37;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.search-results-list {
  background: rgba(17, 23, 35, 0.95);
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 8px;
  max-height: 250px;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
}
.auth-page[data-theme="light"] .search-results-list {
  background: #ffffff;
  border-color: rgba(212, 175, 55, 0.4);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.85rem 1rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.15);
  cursor: pointer;
  transition: all 0.2s;
}
.search-result-item:last-child {
  border-bottom: none;
}
.search-result-item:hover {
  background: rgba(212, 175, 55, 0.12);
}
.result-crest {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: #d4af37;
  color: #000;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}
.result-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.result-company {
  font-weight: 700;
  font-size: 0.88rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.verified-pill {
  font-size: 0.68rem;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  font-weight: 700;
}
.result-ceo {
  font-size: 0.78rem;
  opacity: 0.8;
}
.btn-connect-pill {
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  background: linear-gradient(135deg, #d4af37, #b48608);
  color: #000;
  font-weight: 700;
  font-size: 0.75rem;
  border: none;
  cursor: pointer;
}

.selected-ceo-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1.1rem;
  border-radius: 8px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.4);
}
.selected-badge {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #10b981;
  margin-bottom: 0.2rem;
}
.selected-org-name {
  font-weight: 800;
  font-size: 0.95rem;
}
.selected-ceo-name {
  font-size: 0.8rem;
  opacity: 0.85;
}
.btn-change-ceo {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #d4af37;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
}

.no-results-alert {
  display: flex;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.35);
  color: #f59e0b;
  font-size: 0.8rem;
  line-height: 1.45;
}
.alert-icon { font-size: 1.25rem; }
.alert-content p { margin: 0.25rem 0 0; opacity: 0.9; }

/* AUTOMATED CREDENTIALS BADGE */
.credentials-info-card {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  padding: 1rem 1.25rem;
  border-radius: 10px;
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.28);
}
.credentials-info-icon {
  font-size: 1.4rem;
}
.credentials-info-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.credentials-info-title {
  font-weight: 700;
  font-size: 0.88rem;
  color: #d4af37;
}
.credentials-info-desc {
  font-size: 0.8rem;
  opacity: 0.8;
  line-height: 1.45;
}

/* Address Card */
.address-card {
  padding: 1.25rem;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.auth-page[data-theme="light"] .address-card {
  background: rgba(241, 245, 249, 0.8);
  border-color: rgba(212, 175, 55, 0.3);
}

.address-header {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.address-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: #d4af37;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.same-as-physical {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.8rem;
  cursor: pointer;
  color: #d4af37;
}
.synced-badge {
  font-size: 0.82rem;
  color: #10b981;
  padding: 0.4rem 0.6rem;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 6px;
}

/* Consent Section */
.consent-section {
  padding: 0.5rem 0;
}
.check-row {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.82rem;
  line-height: 1.45;
  cursor: pointer;
  opacity: 0.9;
}
.check-row input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #d4af37;
  margin-top: 2px;
}
.gold-link {
  color: #d4af37;
  text-decoration: underline;
  font-weight: 600;
}

/* Form Errors */
.form-error {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid #ef4444;
  color: #fca5a5;
  font-size: 0.85rem;
  font-weight: 600;
}

/* Step Nav */
.step-nav {
  margin-top: 1rem;
}
.btn {
  padding: 0.85rem 1.75rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.btn-primary {
  background: linear-gradient(135deg, #d4af37, #b48608);
  color: #000;
  border: none;
  box-shadow: 0 4px 18px rgba(212, 175, 55, 0.35);
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.55);
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-gold-action {
  width: 100%;
}
.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: inherit;
}
.btn-secondary:hover {
  background: rgba(212, 175, 55, 0.15);
}

.auth-footer {
  text-align: center;
  font-size: 0.85rem;
  opacity: 0.8;
  margin-top: 1rem;
}

/* STEP 3 Confirmation Seal */
.success-panel {
  text-align: center;
}
.success-icon-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}
.gold-seal-crest {
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: radial-gradient(circle, #fbf2c4 0%, #d4af37 60%, #997819 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 35px rgba(212, 175, 55, 0.6), inset 0 0 10px rgba(0, 0, 0, 0.3);
  border: 3px solid #fef3c7;
  animation: pulseSeal 3s infinite ease-in-out;
}
@keyframes pulseSeal {
  0%, 100% { transform: scale(1); box-shadow: 0 0 30px rgba(212, 175, 55, 0.5); }
  50% { transform: scale(1.05); box-shadow: 0 0 45px rgba(212, 175, 55, 0.8); }
}
.seal-f {
  font-size: 2.75rem;
  font-weight: 900;
  color: #1a1608;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.4);
}

.success-headline {
  font-size: 1.65rem;
  margin-top: 0.5rem;
}
.success-divider {
  width: 80px;
  height: 2px;
  background: #d4af37;
  margin: 1rem auto 1.5rem;
}

.review-dossier-card {
  text-align: left;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.auth-page[data-theme="light"] .review-dossier-card {
  background: rgba(241, 245, 249, 0.9);
}
.dossier-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.88rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.12);
  padding-bottom: 0.4rem;
}
.dossier-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.dossier-key {
  opacity: 0.75;
  font-weight: 500;
}
.dossier-val {
  font-weight: 700;
}
.highlight-gold {
  color: #d4af37;
}

.success-note {
  font-size: 0.95rem;
  line-height: 1.6;
  margin-top: 1rem;
}
.success-actions {
  max-width: 320px;
  margin: 1.5rem auto 0;
}

.scarcity-pill-banner {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.35);
  color: #fcd34d;
  padding: 0.4rem 0.9rem;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  margin-bottom: 0.75rem;
}
.scarcity-pill-banner strong {
  color: #fbbf24;
}
.scarcity-fire {
  font-size: 0.95rem;
  animation: pvPulse 1.5s infinite;
}
</style>
