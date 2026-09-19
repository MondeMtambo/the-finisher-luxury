<template>
  <transition name="eula-fade">
    <div v-if="isOpen" class="eula-overlay" @click.self="handleBackdropClick">
      <div class="eula-modal card luxury-theme">
        <!-- Header -->
        <div class="eula-header">
          <div class="eula-crest">
            <span class="crest-icon">🛡️</span>
          </div>
          <div class="eula-title-group">
            <div class="eula-badge">POPIA ACT 4 OF 2013 &bull; SECTION 19 COMPLIANT</div>
            <h2>End User License Agreement (EULA)</h2>
            <p class="eula-sub">Official Corporate Software License &amp; Data Processing Covenant</p>
          </div>
          <button v-if="allowDismiss" class="btn-close" @click="closeModal">&times;</button>
        </div>

        <!-- Success State: Certificate Generated -->
        <div v-if="acceptedCertificate" class="eula-success-body">
          <div class="cert-seal">
            <span class="seal-icon">✦</span>
          </div>
          <h3>Agreement Successfully Certified</h3>
          <p class="cert-desc">
            Your enterprise license agreement has been digitally executed and logged into the compliance registry.
          </p>

          <div class="cert-id-card font-mono">
            <span class="cert-label">OFFICIAL CERTIFICATE IDENTIFIER:</span>
            <span class="cert-code">{{ acceptedCertificate.certificate_id }}</span>
          </div>

          <p class="cert-meta">
            A certified PDF copy has been dispatched to <strong>{{ form.signer_email }}</strong> and securely stored in your tenant vault.
          </p>

          <div class="success-actions">
            <a 
              :href="downloadUrl" 
              target="_blank" 
              class="btn btn-gold"
            >
              📥 Download Certified PDF
            </a>
            <button class="btn btn-secondary" @click="closeModal">
              Proceed to Executive Suite
            </button>
          </div>
        </div>

        <!-- Acceptance Form -->
        <form v-else @submit.prevent="submitAcceptance" class="eula-body">
          <!-- Scrollable Agreement Container -->
          <div class="agreement-box" @scroll="checkScrollBottom">
            <div class="article-block">
              <h4>PREAMBLE &amp; JURISDICTION</h4>
              <p>
                This End User License Agreement ("Agreement" or "EULA") is entered into by and between <strong>Mtambo Holdings Group</strong> ("Licensor", "Operator") and the organization identified below ("Licensee", "Responsible Party"). This Agreement is governed by the laws of the Republic of South Africa, specifically the Protection of Personal Information Act 4 of 2013 ("POPIA"), the Electronic Communications and Transactions Act 25 of 2002 ("ECTA"), and the Cybercrimes Act 19 of 2020.
              </p>
            </div>

            <div class="article-block">
              <h4>ARTICLE 1 &mdash; ENTERPRISE LICENSE GRANT</h4>
              <p>
                1.1. Licensor grants Licensee a non-exclusive, non-transferable, multi-tenant enterprise software license to access and utilize <strong>THE FINISHER LUXURY CRM</strong> platform solely for legitimate business operations during active subscription periods.
              </p>
              <p>
                1.2. Access is strictly partitioned per Organization. Cross-tenant data extraction, reverse engineering, unauthorized API harvesting, and sharing of authenticated administrative credentials are strictly prohibited.
              </p>
            </div>

            <div class="article-block">
              <h4>ARTICLE 2 &mdash; POPIA SECTION 19 COMPLIANCE &amp; SECURITY</h4>
              <p>
                2.1. In accordance with Section 19 of POPIA, Licensor implements and maintains appropriate, reasonable technical and organizational measures to prevent loss of, damage to, or unauthorized destruction of personal information, and unlawful access to or processing of personal information.
              </p>
              <p>
                2.2. The Licensee acknowledges that it acts as the <strong>Responsible Party</strong> regarding all contact, lead, and client data uploaded into the system. The Licensor acts strictly as an <strong>Operator</strong> processing information under encrypted parameters.
              </p>
            </div>

            <div class="article-block">
              <h4>ARTICLE 3 &mdash; DATA LOCKDOWN &amp; RETENTION</h4>
              <p>
                3.1. All organizational databases are maintained under cryptographic tenant locks. Data export functions remain subject to anti-theft validation and tier verification.
              </p>
              <p>
                3.2. Upon account termination or written request pursuant to Section 24 of POPIA, organizational data shall be securely archived or deleted in accordance with statutory retention schedules.
              </p>
            </div>

            <div class="article-block">
              <h4>ARTICLE 4 &mdash; SERVICE LEVEL AGREEMENT &amp; AUDIT</h4>
              <p>
                4.1. Platform updates, security patches, and cloud synchronization are maintained continuously. Mandatory Multi-Factor Authentication (MFA) is enforced for administrative and executive users.
              </p>
              <p>
                4.2. Every digital transaction, lead ingestion, and agreement execution is logged with timestamp, user identity, and IP address for compliance verification.
              </p>
            </div>
          </div>

          <!-- Mandatory Legal Checkboxes -->
          <div class="checklist-section">
            <label class="check-item">
              <input type="checkbox" v-model="checks.authority" required />
              <span>I confirm I am an authorized officer with legal capacity to bind this enterprise.</span>
            </label>
            <label class="check-item">
              <input type="checkbox" v-model="checks.popia" required />
              <span>I acknowledge and agree to the POPIA Section 19 Data Protection Covenants.</span>
            </label>
            <label class="check-item">
              <input type="checkbox" v-model="checks.ecta" required />
              <span>I agree that digital execution constitutes a valid, legally binding signature under ECTA Act 25 of 2002.</span>
            </label>
          </div>

          <!-- Signatory Credentials Inputs -->
          <div class="signatory-inputs">
            <div class="input-row">
              <div class="input-group">
                <label>Signatory Full Legal Name</label>
                <input 
                  type="text" 
                  v-model="form.signer_full_name" 
                  placeholder="e.g. Monde Mtambo" 
                  class="form-input" 
                  required 
                />
              </div>
              <div class="input-group">
                <label>Corporate Title / Capacity</label>
                <input 
                  type="text" 
                  v-model="form.signer_title" 
                  placeholder="e.g. Chief Executive Officer" 
                  class="form-input" 
                  required 
                />
              </div>
            </div>
            <div class="input-group">
              <label>Corporate Email (Certificate will be dispatched here)</label>
              <input 
                type="email" 
                v-model="form.signer_email" 
                placeholder="executive@yourcompany.co.za" 
                class="form-input" 
                required 
              />
            </div>
          </div>

          <!-- Footer Actions -->
          <div class="eula-footer">
            <span class="eula-audit-note">
              🔒 IP &amp; Device Identity will be stamped onto the cryptographic certificate.
            </span>
            <button 
              type="submit" 
              class="btn btn-gold btn-sign" 
              :disabled="submitting || !allChecked"
            >
              <span v-if="submitting">Processing Cryptographic Signature...</span>
              <span v-else>✍️ Digitally Sign &amp; Accept EULA</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script>
import { eulaAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'

export default {
  name: 'EulaModal',
  data() {
    return {
      isOpen: false,
      allowDismiss: false,
      submitting: false,
      acceptedCertificate: null,
      downloadUrl: '',
      checks: {
        authority: false,
        popia: false,
        ecta: false
      },
      form: {
        signer_full_name: '',
        signer_title: 'Authorized Executive',
        signer_email: ''
      }
    }
  },
  computed: {
    allChecked() {
      return this.checks.authority && this.checks.popia && this.checks.ecta
    }
  },
  mounted() {
    this.checkEulaStatus()
    window.addEventListener('tfl-auth-changed', this.checkEulaStatus)
    window.addEventListener('open-eula-modal', this.openManually)
  },
  beforeUnmount() {
    window.removeEventListener('tfl-auth-changed', this.checkEulaStatus)
    window.removeEventListener('open-eula-modal', this.openManually)
  },
  methods: {
    async checkEulaStatus() {
      if (!authService.isAuthenticated()) {
        this.isOpen = false
        return
      }

      // System Owner (adminluxury) is sovereign and never blocked by onboarding EULA
      const user = authService.getUser()
      const isOwner = Boolean(user && user.username && user.username.toLowerCase() === 'adminluxury')
      if (isOwner) {
        this.isOpen = false
        return
      }

      // If user has already completed/acknowledged EULA, never show again
      if (localStorage.getItem('tfl_eula_accepted') === 'true') {
        this.isOpen = false
        return
      }

      // STRICT FIRST-TIME ONLY RULE: EULA only triggers on the Dashboard on initial launch
      if (this.$route?.path !== '/dashboard') {
        this.isOpen = false
        return
      }

      try {
        const resp = await eulaAPI.getStatus()
        if (!resp.data.accepted) {
          this.allowDismiss = false
          this.prefillUser()
          this.isOpen = true
        } else {
          localStorage.setItem('tfl_eula_accepted', 'true')
          this.isOpen = false
        }
      } catch (err) {
        console.warn('[EULA] Status check warning:', err)
        this.isOpen = false
      }
    },

    prefillUser() {
      const user = authService.getUser()
      if (user) {
        this.form.signer_full_name = `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username || ''
        this.form.signer_email = user.email || ''
        this.form.signer_title = user.is_superuser ? 'Managing Director / Owner' : 'Authorized Corporate Officer'
      }
    },

    openManually() {
      this.allowDismiss = true
      this.prefillUser()
      this.isOpen = true
    },

    handleBackdropClick() {
      if (this.allowDismiss) {
        this.closeModal()
      }
    },

    closeModal() {
      this.isOpen = false
      this.acceptedCertificate = null
      localStorage.setItem('tfl_eula_accepted', 'true')
    },

    checkScrollBottom() {
      // Optional interactive scroll completion
    },

    async submitAcceptance() {
      if (!this.allChecked) {
        toast.warning('Please acknowledge all legal covenants to execute the EULA.')
        return
      }

      this.submitting = true
      try {
        const resp = await eulaAPI.accept({
          signer_full_name: this.form.signer_full_name,
          signer_title: this.form.signer_title,
          signer_email: this.form.signer_email
        })

        this.acceptedCertificate = resp.data
        this.downloadUrl = resp.data.download_url
        localStorage.setItem('tfl_eula_accepted', 'true')
        toast.success('EULA Executed', 'PDF certificate dispatched to corporate email')
      } catch (err) {
        console.error('EULA acceptance error:', err)
        toast.error('Failed to register EULA acceptance. Please retry.')
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.eula-overlay {
  position: fixed;
  inset: 0;
  background: rgba(4, 6, 12, 0.88);
  backdrop-filter: blur(12px);
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.eula-modal {
  background: #10131c;
  border: 1px solid rgba(212, 175, 55, 0.4);
  border-radius: 18px;
  width: 100%;
  max-width: 720px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(212, 175, 55, 0.15);
  color: #e2e8f0;
  overflow: hidden;
}

.eula-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  background: linear-gradient(180deg, rgba(212, 175, 55, 0.08) 0%, transparent 100%);
}

.eula-crest {
  width: 52px;
  height: 52px;
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.4);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
}

.eula-title-group h2 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.3px;
}

.eula-badge {
  font-size: 0.68rem;
  font-weight: 800;
  color: #d4af37;
  letter-spacing: 1px;
  margin-bottom: 2px;
}

.eula-sub {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: 2px 0 0;
}

.btn-close {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.6rem;
  cursor: pointer;
  line-height: 1;
}

.eula-body {
  padding: 1.5rem 1.75rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Scrollable Legal Box */
.agreement-box {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 1.25rem;
  max-height: 200px;
  overflow-y: auto;
  font-size: 0.82rem;
  color: #cbd5e1;
  line-height: 1.6;
}

.article-block {
  margin-bottom: 1.25rem;
}

.article-block:last-child {
  margin-bottom: 0;
}

.article-block h4 {
  font-size: 0.78rem;
  font-weight: 800;
  color: #d4af37;
  margin: 0 0 6px 0;
  letter-spacing: 0.5px;
}

.article-block p {
  margin: 0 0 6px 0;
}

/* Checklist */
.checklist-section {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  background: rgba(212, 175, 55, 0.05);
  border: 1px dashed rgba(212, 175, 55, 0.3);
  padding: 0.9rem 1.1rem;
  border-radius: 10px;
}

.check-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #e2e8f0;
  cursor: pointer;
}

.check-item input[type="checkbox"] {
  margin-top: 2px;
  accent-color: #d4af37;
  width: 16px;
  height: 16px;
}

/* Signatory Inputs */
.signatory-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.input-group label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 4px;
}

.form-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #ffffff;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
}

.form-input:focus {
  outline: none;
  border-color: #d4af37;
}

/* Footer */
.eula-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.eula-audit-note {
  font-size: 0.72rem;
  color: #94a3b8;
}

.btn-sign {
  padding: 10px 20px;
  font-size: 0.92rem;
  font-weight: 700;
  background: linear-gradient(135deg, #d4af37 0%, #b8972f 100%);
  color: #0b0f19;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-sign:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Success Card */
.eula-success-body {
  padding: 2.5rem 2rem;
  text-align: center;
}

.cert-seal {
  width: 64px;
  height: 64px;
  background: rgba(16, 185, 129, 0.15);
  border: 2px solid #10b981;
  border-radius: 50%;
  margin: 0 auto 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #10b981;
}

.cert-id-card {
  background: rgba(0, 0, 0, 0.5);
  border: 1px dashed rgba(212, 175, 55, 0.4);
  padding: 1rem;
  border-radius: 8px;
  margin: 1.25rem auto;
  max-width: 440px;
}

.cert-label {
  display: block;
  font-size: 0.72rem;
  color: #94a3b8;
  margin-bottom: 4px;
}

.cert-code {
  font-size: 1.15rem;
  font-weight: 800;
  color: #d4af37;
}

.cert-desc {
  font-size: 0.95rem;
  color: #e2e8f0;
  max-width: 500px;
  margin: 0 auto;
}

.cert-meta {
  font-size: 0.82rem;
  color: #94a3b8;
  margin: 0.75rem auto 1.75rem;
  max-width: 480px;
}

.success-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
</style>
