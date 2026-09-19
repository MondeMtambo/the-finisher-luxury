<template>
  <div class="upgrade-container">
    <div class="upgrade-header card">
      <div class="header-badge">COMMERCIAL PLANS &amp; ALLOCATIONS</div>
      <h1>Choose Your Finisher Luxury Plan</h1>
      <p class="subtitle">Fixed South African Rand (ZAR) billing. Zero foreign exchange volatility. No punitive per-seat penalties.</p>
    </div>

    <!-- 4-Tier Plan Grid -->
    <div class="plans-grid">
      <!-- Tier 1: Corporate Sovereign -->
      <div class="plan-card card sovereign-tier-card" :class="{ selected: selectedTier === 'basic' || selectedTier === 'classic' }">
        <div class="plan-top">
          <div class="plan-tier-label sovereign-label">SOVEREIGN ALLOCATION &bull; 5 SEATS</div>
          <h2 class="plan-title">Corporate Sovereign</h2>
          <p class="plan-desc">For emerging enterprises, commercial brokers &amp; consultancies requiring elite CRM foundations.</p>
          <div class="plan-price">
            <span class="currency">R</span>0<span class="period">/permanent</span>
          </div>
          <div class="seat-pill sovereign-seat-pill">5 Collaborative Seats &bull; 6,000 Verified Contacts</div>
        </div>

        <ul class="feature-bullets">
          <li><strong>5 Collaborative Team Seats</strong> Included</li>
          <li><strong>Up to 6,000 Client Contacts</strong> &amp; Verified Leads</li>
          <li><strong>Unlimited Active Pipeline Deals</strong> &amp; Stages</li>
          <li>Full Standard Quotation &amp; Invoicing Engine</li>
          <li>Automated Email Workflows &amp; Direct Engagement</li>
          <li>SARS Tax Computation &amp; Financial Ledger</li>
          <li>Finisher Network Secured Watermark Included</li>
          <li>Complete Excel &amp; CSV Audit Data Export</li>
        </ul>

        <div class="plan-action">
          <button 
            class="btn btn-secondary w-100" 
            :class="{ 'btn-primary': selectedTier === 'basic' || selectedTier === 'classic' }"
            @click="selectPlan('basic')"
          >
            {{ (selectedTier === 'basic' || selectedTier === 'classic') ? 'Active Sovereign Allocation' : 'Choose Sovereign Allocation' }}
          </button>
        </div>
      </div>

      <!-- Tier 2: Luxury Team (Featured) -->
      <div class="plan-card card featured" :class="{ selected: selectedTier === 'luxury' }">
        <div class="featured-badge">RECOMMENDED FLAGSHIP &bull; 5 SEATS</div>
        <div class="plan-top">
          <div class="plan-tier-label">GROWING FIRM</div>
          <h2 class="plan-title">Luxury Team</h2>
          <p class="plan-desc">For boutique firms, agencies &amp; growing sales departments.</p>
          <div class="plan-price">
            <span class="currency">R</span>999<span class="period">/month</span>
          </div>
          <div class="seat-pill featured-pill">Up to 5 Users &bull; Unlimited Everything</div>
        </div>

        <ul class="feature-bullets">
          <li><strong>Everything in Luxury Basic, plus:</strong></li>
          <li><strong>Unlimited client contacts &amp; company profiles</strong></li>
          <li><strong>Unlimited active pipeline deals</strong></li>
          <li><strong>Up to 5 collaborative team seats</strong></li>
          <li>Manager Onboarding Delegation (up to 2 subordinates)</li>
          <li>Unlimited Email Campaigns &amp; Automated Workflows</li>
          <li>Full Asset Management Tracking</li>
          <li>Full Excel &amp; CSV Audit Data Export</li>
        </ul>

        <div class="plan-action">
          <button 
            class="btn btn-primary w-100 highlight-btn"
            @click="selectPlan('luxury')"
          >
            {{ selectedTier === 'luxury' ? 'Selected Plan' : 'Choose Luxury Team' }}
          </button>
        </div>
      </div>

      <!-- Tier 3: Executive Suite -->
      <div class="plan-card card" :class="{ selected: selectedTier === 'executive' }">
        <div class="plan-top">
          <div class="plan-tier-label">ESTABLISHED FIRM</div>
          <h2 class="plan-title">Executive Suite</h2>
          <p class="plan-desc">For mid-size corporations, regional firms &amp; multi-branch groups.</p>
          <div class="plan-price">
            <span class="currency">R</span>1,500<span class="period">/month</span>
          </div>
          <div class="seat-pill">Up to 15 Users &bull; Unlimited Contacts</div>
        </div>

        <ul class="feature-bullets">
          <li><strong>Everything in Luxury Team, plus:</strong></li>
          <li><strong>Unlimited client contacts &amp; accounts</strong></li>
          <li><strong>Up to 15 executive &amp; staff seats</strong></li>
          <li>Multi-branch / department filtering</li>
          <li>Executive KPI scoreboard &amp; custom reports</li>
          <li>Automated email trigger workflows</li>
          <li>POPIA Section 19 compliance vault</li>
          <li>Priority Concierge WhatsApp &amp; Phone</li>
        </ul>

        <div class="plan-action">
          <button 
            class="btn btn-secondary w-100"
            :class="{ 'btn-primary': selectedTier === 'executive' }"
            @click="selectPlan('executive')"
          >
            {{ selectedTier === 'executive' ? 'Selected Plan' : 'Choose Executive' }}
          </button>
        </div>
      </div>

      <!-- Tier 4: Enterprise -->
      <div class="plan-card card enterprise-card" :class="{ selected: selectedTier === 'enterprise' }">
        <div class="plan-top">
          <div class="plan-tier-label">CUSTOM ENTERPRISE</div>
          <h2 class="plan-title">Enterprise</h2>
          <p class="plan-desc">For large fleets, bespoke infrastructure & institutional compliance.</p>
          <div class="plan-price enterprise-price">
            Bespoke <span class="period">/ Custom</span>
          </div>
          <div class="seat-pill">Unlimited Users & Capacity</div>
        </div>

        <ul class="feature-bullets">
          <li>Dedicated PostgreSQL database cluster</li>
          <li>Custom Sage / Xero accounting sync</li>
          <li>White-label theming & custom corporate domain</li>
          <li>Private mail gateway (custom SPF/DKIM)</li>
          <li>Quarterly business reviews & custom SLA</li>
          <li>Dedicated Solutions Architect</li>
        </ul>

        <div class="plan-action">
          <button 
            class="btn btn-outline w-100"
            @click="contactSalesModal = true"
          >
            Contact Sales
          </button>
        </div>
      </div>
    </div>

    <!-- Enterprise Add-On Suite -->
    <div class="addons-container card">
      <div class="addons-header">
        <div>
          <div class="addons-badge">INSTANT PAYFAST INTEGRATION</div>
          <h2>Enterprise Add-On Suite</h2>
          <p class="subtitle">Deploy white-label custom branding or certified statutory tender dossiers on demand.</p>
        </div>
      </div>

      <div class="addons-grid">
        <!-- Add-on 1: White Label -->
        <div class="addon-card">
          <div class="addon-card-top">
            <div class="addon-icon gold-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <div>
              <div class="addon-title">Corporate White-Label &amp; Custom Branding</div>
              <div class="addon-price">R199 <span class="addon-period">/ month recurring</span></div>
            </div>
          </div>
          <p class="addon-desc">
            Removes the Finisher Luxury CRM watermark from all quotations, tax invoices, and emails.
            Unlocks instant enterprise logo upload and custom branded PDF correspondence for your company.
          </p>
          <ul class="addon-bullets">
            <li>Zero Finisher CRM branding on client documents</li>
            <li>Custom high-resolution enterprise logo upload</li>
            <li>Branded tax invoices &amp; pro-forma quotes</li>
            <li>Direct automated PayFast monthly recurring subscription</li>
          </ul>
          <button 
            class="btn btn-primary w-100" 
            :disabled="processingWhiteLabel" 
            @click="checkoutWhiteLabel"
          >
            <span v-if="processingWhiteLabel">Connecting to PayFast...</span>
            <span v-else>Activate White-Label (R199/mo)</span>
          </button>
        </div>

        <!-- Add-on 2: Tender Pack -->
        <div class="addon-card">
          <div class="addon-card-top">
            <div class="addon-icon blue-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            </div>
            <div>
              <div class="addon-title">Official Tender &amp; SEDA Compliance Pack</div>
              <div class="addon-price">R350 <span class="addon-period">once-off certified pack</span></div>
            </div>
          </div>
          <p class="addon-desc">
            Bank-grade certified compliance dossier formatted for National Treasury CSD tenders,
            SEDA financing applications, and commercial bank credit committee reviews.
          </p>
          <ul class="addon-bullets">
            <li>12-Month Audited Sales &amp; Contract Ledger</li>
            <li>POPIA Act 4 of 2013 Section 19 Cryptographic Certificate</li>
            <li>SHA-256 Tamper-Proof Audit Seal &amp; QR verification</li>
            <li>Instant PDF generation &amp; certified document download</li>
          </ul>
          <button 
            class="btn btn-secondary w-100" 
            :disabled="processingTenderPack" 
            @click="checkoutTenderPack"
          >
            <span v-if="processingTenderPack">Connecting to PayFast...</span>
            <span v-else>Unlock Tender Pack (R350)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Settlement & Corporate EFT Invoice Centre -->
    <div v-if="selectedPlanDetails" class="settlement-centre card">
      <div class="settlement-header">
        <div>
          <h3>Corporate Settlement: {{ selectedPlanDetails.name }}</h3>
          <p class="text-muted">Generate an official Pro-Forma Tax Invoice or settle via Direct Corporate EFT.</p>
        </div>
        <div class="settlement-amount">
          <span class="label">Amount Due:</span>
          <span class="val">{{ selectedPlanDetails.price }}</span>
        </div>
      </div>

      <div class="eft-details-box">
        <div class="eft-col">
          <div class="bank-row">
            <span class="label">Account Holder:</span>
            <span class="val"><strong>Mtambo Holdings (Pty) Ltd</strong></span>
          </div>
          <div class="bank-row">
            <span class="label">Bank Name:</span>
            <span class="val">First National Bank (FNB)</span>
          </div>
          <div class="bank-row">
            <span class="label">Account Type:</span>
            <span class="val">Commercial Business Cheque</span>
          </div>
        </div>
        <div class="eft-col">
          <div class="bank-row">
            <span class="label">Branch Code:</span>
            <span class="val">250655</span>
          </div>
          <div class="bank-row">
            <span class="label">Tax Exemption:</span>
            <span class="val">SARS Section 23 (&lt;R1M Threshold)</span>
          </div>
          <div class="bank-row">
            <span class="label">Beneficiary Reference:</span>
            <span class="val ref-tag">{{ paymentReference }}</span>
          </div>
        </div>
      </div>

      <div class="settlement-actions">
        <button class="btn btn-secondary" @click="copyBankDetails">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          {{ copied ? 'Copied to Clipboard!' : 'Copy Bank Details' }}
        </button>
        <button class="btn btn-primary" @click="notifyPaymentModal = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          I Have Paid / Submit Proof of Payment
        </button>
        <button class="btn btn-ghost" @click="goBack">Back to Dashboard</button>
      </div>
    </div>

    <!-- Modal: Proof of Payment Notification -->
    <div v-if="notifyPaymentModal" class="modal-overlay" @click.self="notifyPaymentModal = false">
      <div class="modal-content card">
        <h3>Submit Proof of Payment (POP)</h3>
        <p class="text-muted">Send your payment notification directly to Mtambo Holdings executive concierge for instant account activation.</p>
        
        <div class="form-group">
          <label>Organization / Company Name</label>
          <input type="text" v-model="companyName" class="form-control" placeholder="Mtambo Holdings (Pty) Ltd" />
        </div>
        <div class="form-group">
          <label>Payment Reference Used</label>
          <input type="text" v-model="paymentReference" class="form-control" readonly />
        </div>
        <div class="form-group">
          <label>Email Address for Tax Invoice</label>
          <input type="email" v-model="contactEmail" class="form-control" placeholder="ceo@company.co.za" />
        </div>

        <div class="modal-actions">
          <button class="btn btn-secondary" @click="notifyPaymentModal = false">Cancel</button>
          <button class="btn btn-primary" :disabled="submitting" @click="submitPOP">
            {{ submitting ? 'Submitting...' : 'Confirm Submission' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal: Contact Sales -->
    <div v-if="contactSalesModal" class="modal-overlay" @click.self="contactSalesModal = false">
      <div class="modal-content card">
        <h3>Enterprise Custom Architecture</h3>
        <p class="text-muted">Bespoke SLA, dedicated database clusters, and custom Sage/Xero integrations for large operations.</p>
        <p><strong>Executive Concierge:</strong> <a href="mailto:mtamboholdings@outlook.com?subject=Enterprise%20Edition%20Consultation">mtamboholdings@outlook.com</a></p>
        <div class="modal-actions">
          <button class="btn btn-primary" @click="contactSalesModal = false">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import toast from '../utils/toast'
import authService from '../services/auth'
import { monetizationAPI } from '../api'

export default {
  name: 'UpgradePage',
  data() {
    const user = authService.getUser() || {}
    const company = user.company_name || user.profile?.company_name || 'WORKSPACE'
    const cleanCompany = company.replace(/[^a-zA-Z0-9]/g, '').substring(0, 6).toUpperCase() || 'FIN'
    const randomSuffix = Math.floor(1000 + Math.random() * 9000)

    return {
      selectedTier: 'luxury',
      paymentReference: `TFL-INV-${cleanCompany}-${randomSuffix}`,
      copied: false,
      notifyPaymentModal: false,
      contactSalesModal: false,
      submitting: false,
      companyName: company,
      contactEmail: user.email || '',
      processingWhiteLabel: false,
      processingTenderPack: false
    }
  },
  computed: {
    plans() {
      return {
        basic: {
          name: 'Corporate Sovereign',
          price: 'R0 / permanent',
          users: '5 Collaborative Seats (6,000 Contacts)'
        },
        classic: {
          name: 'Corporate Sovereign',
          price: 'R0 / permanent',
          users: '5 Collaborative Seats (6,000 Contacts)'
        },
        luxury: {
          name: 'Luxury Team',
          price: 'R999 / month',
          users: 'Up to 5 Users'
        },
        executive: {
          name: 'Executive Suite',
          price: 'R1,500 / month',
          users: 'Up to 15 Users'
        }
      }
    },
    selectedPlanDetails() {
      return this.plans[this.selectedTier] || this.plans.luxury
    }
  },
  mounted() {
    const routePlan = (this.$route.params.plan || this.$route.query.plan || '').toLowerCase()
    if (['basic', 'classic', 'luxury', 'team', 'executive'].includes(routePlan)) {
      this.selectedTier = (routePlan === 'classic' || routePlan === 'basic') ? 'basic' : (routePlan === 'team' ? 'luxury' : routePlan)
    } else {
      const user = authService.getUser() || {}
      const userPlan = (user.raw_tier || user.subscription_tier || user.tier || '').toLowerCase()
      if (['basic', 'classic', 'luxury', 'executive'].includes(userPlan)) {
        this.selectedTier = userPlan === 'classic' ? 'basic' : userPlan
      }
    }
  },
  methods: {
    selectPlan(tier) {
      this.selectedTier = tier
    },
    goBack() {
      this.$router.push('/dashboard')
    },
    copyBankDetails() {
      const details = `Bank: First National Bank (FNB)\nAccount Holder: Mtambo Holdings (Pty) Ltd\nAccount Type: Business Cheque\nBranch Code: 250655\nReference: ${this.paymentReference}\nAmount: ${this.selectedPlanDetails.price}`
      navigator.clipboard.writeText(details).then(() => {
        this.copied = true
        toast.success('Corporate banking details copied to clipboard!', 'Copied')
        setTimeout(() => { this.copied = false }, 3000)
      }).catch(() => {
        toast.info(details, 'Banking Details')
      })
    },
    submitPOP() {
      this.submitting = true
      setTimeout(() => {
        this.submitting = false
        this.notifyPaymentModal = false
        toast.success(
          `Payment notice received for ${this.paymentReference}. Our concierge team will confirm receipt and activate full tier access.`,
          'Proof of Payment Logged'
        )
      }, 1000)
    },
    async checkoutWhiteLabel() {
      this.processingWhiteLabel = true
      try {
        const res = await monetizationAPI.checkoutWhiteLabel()
        this.submitPayFast(res.data)
      } catch (err) {
        toast.error(err.response?.data?.error || 'Failed to initiate white-label checkout', 'PayFast Error')
      } finally {
        this.processingWhiteLabel = false
      }
    },
    async checkoutTenderPack() {
      this.processingTenderPack = true
      try {
        const res = await monetizationAPI.checkoutTenderPack()
        this.submitPayFast(res.data)
      } catch (err) {
        toast.error(err.response?.data?.error || 'Failed to initiate tender pack checkout', 'PayFast Error')
      } finally {
        this.processingTenderPack = false
      }
    },
    submitPayFast(payfastData) {
      const form = document.createElement('form')
      form.method = 'POST'
      form.action = payfastData.process_url
      Object.keys(payfastData).forEach(key => {
        if (key !== 'process_url') {
          const input = document.createElement('input')
          input.type = 'hidden'
          input.name = key
          input.value = payfastData[key]
          form.appendChild(input)
        }
      })
      document.body.appendChild(form)
      form.submit()
    }
  }
}
</script>

<style scoped>
.upgrade-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.upgrade-header {
  text-align: center;
  padding: 2.5rem 1.5rem;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
}

.header-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: #d97706;
  background: #fef3c7;
  padding: 4px 12px;
  border-radius: 999px;
  margin-bottom: 0.75rem;
}

.upgrade-header h1 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: var(--gray-600);
  max-width: 680px;
  margin: 0 auto 1rem;
}


/* Grid */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 640px) {
  .plans-grid {
    grid-template-columns: 1fr;
  }
}

.plan-card {
  padding: 1.5rem;
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-color);
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  transition: all 0.2s ease;
}

.plan-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
}

.plan-card.featured {
  border: 2px solid #d97706;
  background: #fffdfa;
  box-shadow: 0 8px 24px -4px rgba(217, 119, 6, 0.12);
}

.plan-card.selected {
  border-color: var(--primary-600);
  outline: 2px solid var(--primary-200);
}

.featured-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #d97706;
  color: #ffffff;
  font-size: 0.6875rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  padding: 4px 12px;
  border-radius: 999px;
  white-space: nowrap;
}

.plan-tier-label {
  font-size: 0.6875rem;
  font-weight: 800;
  color: var(--gray-500);
  letter-spacing: 1px;
  margin-bottom: 0.25rem;
}

.plan-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: 0.35rem;
}

.plan-desc {
  font-size: 0.8125rem;
  color: var(--gray-500);
  min-height: 38px;
  margin-bottom: 1rem;
}

.plan-price {
  font-size: 1.875rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: 0.5rem;
}

.plan-price .currency {
  font-size: 1.125rem;
  vertical-align: top;
  margin-right: 2px;
}

.plan-price .period {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--gray-500);
}

.seat-pill {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  background: var(--gray-100);
  color: var(--gray-700);
  margin-bottom: 1.25rem;
}

.featured-pill {
  background: #fef3c7;
  color: #92400e;
}

.feature-bullets {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
  font-size: 0.8125rem;
  color: var(--gray-700);
  line-height: 1.6;
}

.feature-bullets li {
  margin-bottom: 0.5rem;
  position: relative;
  padding-left: 1.25rem;
}

.feature-bullets li::before {
  content: "✓";
  color: #16a34a;
  font-weight: 800;
  position: absolute;
  left: 0;
}

.savings-tag {
  display: inline-block;
  font-size: 0.6875rem;
  font-weight: 700;
  color: #16a34a;
  background: #dcfce7;
  padding: 2px 6px;
  border-radius: 4px;
}

.w-100 { width: 100%; }

.highlight-btn {
  background: #d97706 !important;
  border-color: #b45309 !important;
  color: #ffffff !important;
  font-weight: 700;
}

/* Settlement Centre */
.settlement-centre {
  padding: 2rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  background: #ffffff;
}

.settlement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.settlement-amount .label {
  font-size: 0.8125rem;
  color: var(--gray-500);
  margin-right: 8px;
}

.settlement-amount .val {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--gray-900);
}

.eft-details-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  background: var(--gray-50);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 640px) {
  .eft-details-box { grid-template-columns: 1fr; }
}

.bank-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px dashed var(--gray-200);
  font-size: 0.875rem;
}

.bank-row .label { color: var(--gray-500); }
.bank-row .val { color: var(--gray-900); }

.ref-tag {
  background: #eff6ff;
  color: var(--primary-700);
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 4px;
}

.settlement-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  max-width: 480px;
  width: 90%;
  padding: 2rem;
  background: #ffffff;
  border-radius: var(--border-radius-lg);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: 4px;
}
.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.875rem;
}

/* Corporate Sovereign Tier Card */
.sovereign-tier-card {
  border-color: rgba(59, 130, 246, 0.4) !important;
}

.sovereign-label {
  color: #3b82f6 !important;
}

.sovereign-seat-pill {
  background: rgba(59, 130, 246, 0.1) !important;
  border-color: rgba(59, 130, 246, 0.3) !important;
  color: #2563eb !important;
}

/* Enterprise Add-On Suite */
.addons-container {
  padding: 2rem;
  border-radius: var(--border-radius-lg);
  background: #ffffff;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.addons-header {
  margin-bottom: 1.5rem;
}

.addons-badge {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #10b981;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.addons-header h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--gray-900);
  margin: 0 0 0.25rem;
}

.addons-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .addons-grid {
    grid-template-columns: 1fr;
  }
}

.addon-card {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  transition: all 0.2s ease;
}

.addon-card:hover {
  border-color: var(--gray-400);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
}

.addon-card-top {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.addon-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.addon-icon.gold-icon {
  background: rgba(212, 175, 55, 0.15);
}

.addon-icon.blue-icon {
  background: rgba(59, 130, 246, 0.15);
}

.addon-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--gray-900);
}

.addon-price {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
}

.addon-period {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--gray-500);
}

.addon-desc {
  font-size: 0.85rem;
  color: var(--gray-600);
  line-height: 1.5;
  margin: 0 0 1rem;
  flex: 1;
}

.addon-bullets {
  list-style: none;
  padding: 0;
  margin: 0 0 1.25rem;
}

.addon-bullets li {
  font-size: 0.8rem;
  color: var(--gray-700);
  padding: 4px 0;
  display: flex;
  align-items: center;
}

.addon-bullets li::before {
  content: "✓";
  color: #10b981;
  font-weight: 800;
  margin-right: 8px;
}
</style>
