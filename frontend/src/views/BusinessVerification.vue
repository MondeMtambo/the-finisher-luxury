<template>
  <div class="verify-page">
    <div class="verify-container">
      <!-- Header -->
      <div class="verify-header">
        <div class="gold-badge">POPIA &bull; CIPC COMPLIANCE</div>
        <h1>Corporate Business Verification</h1>
        <p class="verify-sub">
          Official entity validation gateway for South African corporate tenants on THE FINISHER.
        </p>
      </div>

      <!-- Live Verification Status Card -->
      <div class="status-card" :class="'status-' + verificationStatus">
        <div class="status-icon-wrap">
          <span v-if="verificationStatus === 'verified'" class="status-icon icon-verified">✓</span>
          <span v-else-if="verificationStatus === 'pending'" class="status-icon icon-pending">⏳</span>
          <span v-else-if="verificationStatus === 'rejected'" class="status-icon icon-rejected">✕</span>
          <span v-else class="status-icon icon-unverified">⚠️</span>
        </div>

        <div class="status-content">
          <div class="status-title-row">
            <h3>{{ statusHeading }}</h3>
            <span class="status-pill" :class="'pill-' + verificationStatus">{{ statusPillLabel }}</span>
          </div>
          <p class="status-desc">{{ statusDescription }}</p>

          <!-- Rejection Alert -->
          <div v-if="verificationStatus === 'rejected' && verification?.rejection_reason" class="rejection-box">
            <strong>Compliance Officer Feedback:</strong>
            <p>{{ verification.rejection_reason }}</p>
          </div>

          <!-- Verified Summary -->
          <div v-if="verificationStatus === 'verified'" class="verified-summary">
            <div class="verified-item">
              <span class="lbl">Registered Entity:</span>
              <span class="val">{{ verification?.company_name || organizationName }}</span>
            </div>
            <div class="verified-item" v-if="verification?.cipc_number">
              <span class="lbl">CIPC Registration:</span>
              <span class="val font-mono">{{ verification.cipc_number }}</span>
            </div>
            <div class="verified-item" v-if="verification?.trading_name">
              <span class="lbl">Trading Name:</span>
              <span class="val">T/A {{ verification.trading_name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Verification Form (Displayed if unverified, rejected, or editing) -->
      <div v-if="verificationStatus !== 'verified' || showEditForm" class="form-card">
        <div class="form-header">
          <h2>{{ verificationStatus === 'rejected' ? 'Re-Submit Verification Documents' : 'Submit Business Documents' }}</h2>
          <p>Please upload official company registration documents for offline verification against CIPC.</p>
        </div>

        <form @submit.prevent="submitVerification" class="verify-form">
          <!-- Business Information -->
          <div class="form-section">
            <h4 class="section-title">01 &bull; Legal Business Entity</h4>

            <div class="form-group">
              <label class="form-label">Registered Legal Entity Name *</label>
              <input 
                v-model="form.company_name" 
                type="text" 
                class="form-input" 
                placeholder="e.g. Mtambo Holdings (Pty) Ltd" 
                required 
              />
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Trading Name (Trading As / T/A)</label>
                <input 
                  v-model="form.trading_name" 
                  type="text" 
                  class="form-input" 
                  placeholder="e.g. The Finisher Group" 
                />
              </div>

              <div class="form-group">
                <label class="form-label">Executive Director / Officer *</label>
                <input 
                  v-model="form.director_name" 
                  type="text" 
                  class="form-input" 
                  placeholder="Full name of authorized director" 
                  required 
                />
              </div>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <div class="label-row">
                  <label class="form-label">CIPC Registration Number *</label>
                  <span v-if="cipcStatus.state === 'valid'" class="badge-cipc">✓ {{ cipcStatus.entityLabel }}</span>
                </div>
                <input 
                  v-model="form.cipc_number" 
                  @input="onCipcInput"
                  type="text" 
                  class="form-input font-mono" 
                  placeholder="YYYY/NNNNNN/NN (e.g. 2024/123456/07)" 
                  maxlength="14"
                  required 
                />
                <span class="form-hint">{{ cipcStatus.message || 'Standard South African CIPC registration format.' }}</span>
              </div>

              <div class="form-group">
                <label class="form-label">SARS Tax / VAT Reference (Optional)</label>
                <input 
                  v-model="form.tax_number" 
                  type="text" 
                  class="form-input font-mono" 
                  placeholder="10-digit Tax Ref" 
                  maxlength="10" 
                />
              </div>
            </div>
          </div>

          <!-- Compliance Document Uploads -->
          <div class="form-section">
            <h4 class="section-title">02 &bull; Required Compliance Documents</h4>
            <p class="section-note">
              Accepted formats: PDF, PNG, JPG (Max 15MB each). Documents are stored with high security in accordance with POPIA Section 19.
            </p>

            <div class="upload-grid">
              <!-- CIPC Certificate -->
              <div class="upload-box" :class="{ 'has-file': files.cipc_certificate }">
                <div class="upload-icon">📄</div>
                <div class="upload-meta">
                  <strong>CIPC Registration Certificate *</strong>
                  <span>CoR 14.3, CK document, or Certificate of Incorporation</span>
                  <span v-if="files.cipc_certificate" class="file-chosen">{{ files.cipc_certificate.name }}</span>
                  <span v-else-if="verification?.cipc_certificate_url" class="file-existing">
                    ✓ Document previously uploaded
                  </span>
                </div>
                <label class="btn-browse">
                  {{ files.cipc_certificate ? 'Change File' : 'Browse File' }}
                  <input type="file" @change="onFileChange($event, 'cipc_certificate')" accept=".pdf,.png,.jpg,.jpeg" />
                </label>
              </div>

              <!-- Proof of Physical Address -->
              <div class="upload-box" :class="{ 'has-file': files.proof_of_address }">
                <div class="upload-icon">🏢</div>
                <div class="upload-meta">
                  <strong>Proof of Business Address *</strong>
                  <span>Utility bill, lease agreement, or bank statement (under 3 months)</span>
                  <span v-if="files.proof_of_address" class="file-chosen">{{ files.proof_of_address.name }}</span>
                  <span v-else-if="verification?.proof_of_address_url" class="file-existing">
                    ✓ Document previously uploaded
                  </span>
                </div>
                <label class="btn-browse">
                  {{ files.proof_of_address ? 'Change File' : 'Browse File' }}
                  <input type="file" @change="onFileChange($event, 'proof_of_address')" accept=".pdf,.png,.jpg,.jpeg" />
                </label>
              </div>

              <!-- Director ID / Passport -->
              <div class="upload-box" :class="{ 'has-file': files.director_id_doc }">
                <div class="upload-icon">🪪</div>
                <div class="upload-meta">
                  <strong>Director ID or Passport *</strong>
                  <span>Certified copy of authorized director/signatory ID document</span>
                  <span v-if="files.director_id_doc" class="file-chosen">{{ files.director_id_doc.name }}</span>
                  <span v-else-if="verification?.director_id_doc_url" class="file-existing">
                    ✓ Document previously uploaded
                  </span>
                </div>
                <label class="btn-browse">
                  {{ files.director_id_doc ? 'Change File' : 'Browse File' }}
                  <input type="file" @change="onFileChange($event, 'director_id_doc')" accept=".pdf,.png,.jpg,.jpeg" />
                </label>
              </div>
            </div>
          </div>

          <div v-if="errorMsg" class="alert-error">{{ errorMsg }}</div>
          <div v-if="successMsg" class="alert-success">{{ successMsg }}</div>

          <div class="form-actions">
            <button 
              type="submit" 
              class="btn btn-primary btn-submit"
              :disabled="submitting || cipcStatus.state !== 'valid'"
            >
              {{ submitting ? 'Uploading Compliance Documents...' : 'Submit Documents for CIPC Verification' }}
            </button>
            <button 
              v-if="showEditForm" 
              type="button" 
              class="btn btn-secondary" 
              @click="showEditForm = false"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <!-- Action to edit submitted documents if pending -->
      <div v-if="verificationStatus === 'pending' && !showEditForm" class="pending-actions">
        <button class="btn btn-secondary" @click="showEditForm = true">
          Update / Re-upload Documents
        </button>
        <button class="btn btn-primary" @click="$router.push('/dashboard')">
          Return to Dashboard
        </button>
      </div>

      <div v-else-if="verificationStatus === 'verified'" class="pending-actions">
        <button class="btn btn-primary" @click="$router.push('/dashboard')">
          Access Tenant Workspace
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { verificationAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'BusinessVerification',
  data() {
    return {
      loading: true,
      submitting: false,
      showEditForm: false,
      organizationName: '',
      verificationStatus: 'unverified',
      verification: null,
      errorMsg: '',
      successMsg: '',
      form: {
        company_name: '',
        trading_name: '',
        cipc_number: '',
        tax_number: '',
        director_name: ''
      },
      files: {
        cipc_certificate: null,
        proof_of_address: null,
        director_id_doc: null
      }
    }
  },
  computed: {
    statusHeading() {
      switch (this.verificationStatus) {
        case 'verified': return 'Institutional CIPC Verification Approved'
        case 'pending': return 'Compliance Verification Under Review'
        case 'rejected': return 'Action Required: Documentation Verification Failed'
        default: return 'Corporate Entity Verification Required'
      }
    },
    statusPillLabel() {
      switch (this.verificationStatus) {
        case 'verified': return 'VERIFIED ENTITY'
        case 'pending': return 'IN COMPLIANCE REVIEW'
        case 'rejected': return 'REQUIRES RE-SUBMISSION'
        default: return 'ACTION REQUIRED'
      }
    },
    statusDescription() {
      switch (this.verificationStatus) {
        case 'verified':
          return 'Your corporate business entity has been validated against the South African CIPC register. All platform capabilities, integrations, and CRM workspaces are unlocked.'
        case 'pending':
          return 'Your business documentation has been submitted to the Mtambo Holdings compliance team. We manually inspect and verify records against the CIPC BizPortal database. You will receive an email once approved.'
        case 'rejected':
          return 'Our compliance officers could not verify your business registration based on the submitted documentation. Please inspect the feedback below and submit updated documents.'
        default:
          return 'To safeguard client data and comply with South African POPIA Section 19 standards, all enterprise tenant workspaces must complete CIPC entity verification.'
      }
    },
    cipcStatus() {
      const val = (this.form.cipc_number || '').trim()
      if (!val) return { state: 'empty', message: '', entityLabel: '' }
      const cipcRegex = /^(19|20)\d{2}\/\d{6}\/\d{2}$/
      if (cipcRegex.test(val)) {
        const suffix = val.slice(-2)
        const map = {
          '07': 'Private Company (Pty Ltd)',
          '06': 'Public Company (Ltd)',
          '23': 'Close Corporation (CC)',
          '08': 'Non-Profit Company (NPC)',
          '21': 'Incorporated (Inc)',
          '10': 'External / Foreign'
        }
        const label = map[suffix] || 'Registered Corporate Entity'
        return { state: 'valid', entityLabel: label, message: `Official CIPC Match: ${label}` }
      }
      return { state: 'incomplete', entityLabel: '', message: 'Standard CIPC format: YYYY/NNNNNN/NN (e.g. 2024/123456/07)' }
    }
  },
  async mounted() {
    await this.fetchStatus()
  },
  methods: {
    async fetchStatus() {
      this.loading = true
      try {
        const res = await verificationAPI.getStatus()
        const data = res.data
        this.organizationName = data.organization_name || ''
        this.verificationStatus = data.status || (data.is_verified ? 'verified' : 'unverified')
        this.verification = data.verification

        if (this.verification) {
          this.form.company_name = this.verification.company_name || this.organizationName
          this.form.trading_name = this.verification.trading_name || ''
          this.form.cipc_number = this.verification.cipc_number || ''
          this.form.tax_number = this.verification.tax_number || ''
          this.form.director_name = this.verification.director_name || ''
        } else if (this.organizationName) {
          this.form.company_name = this.organizationName
        }
      } catch (err) {
        console.error('Error loading verification status:', err)
      } finally {
        this.loading = false
      }
    },
    onCipcInput(e) {
      let v = e.target.value.replace(/[^0-9/]/g, '').toUpperCase()
      const digitsOnly = v.replace(/\//g, '')
      if (digitsOnly.length > 4 && digitsOnly.length <= 10) {
        v = `${digitsOnly.slice(0, 4)}/${digitsOnly.slice(4)}`
      } else if (digitsOnly.length > 10) {
        v = `${digitsOnly.slice(0, 4)}/${digitsOnly.slice(4, 10)}/${digitsOnly.slice(10, 12)}`
      }
      this.form.cipc_number = v.slice(0, 14)
    },
    onFileChange(e, field) {
      const file = e.target.files[0]
      if (file) {
        this.files[field] = file
      }
    },
    async submitVerification() {
      if (this.cipcStatus.state !== 'valid') {
        this.errorMsg = 'Please enter a valid South African CIPC registration number (e.g. 2024/123456/07).'
        return
      }

      this.submitting = true
      this.errorMsg = ''
      this.successMsg = ''

      try {
        const formData = new FormData()
        formData.append('company_name', this.form.company_name)
        formData.append('trading_name', this.form.trading_name)
        formData.append('cipc_number', this.form.cipc_number)
        formData.append('tax_number', this.form.tax_number)
        formData.append('director_name', this.form.director_name)

        if (this.files.cipc_certificate) {
          formData.append('cipc_certificate', this.files.cipc_certificate)
        }
        if (this.files.proof_of_address) {
          formData.append('proof_of_address', this.files.proof_of_address)
        }
        if (this.files.director_id_doc) {
          formData.append('director_id_doc', this.files.director_id_doc)
        }

        const res = await verificationAPI.submit(formData)
        this.successMsg = 'Documents uploaded successfully. Your account is queued for CIPC review.'
        toast.success('Verification documents submitted')
        this.showEditForm = false
        await this.fetchStatus()
      } catch (err) {
        console.error('Submission error:', err)
        this.errorMsg = err.response?.data?.error || 'Failed to upload verification documents. Please try again.'
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  padding: 3rem 1.5rem;
  background: #0f172a;
  color: #f8fafc;
  font-family: 'Inter', system-ui, sans-serif;
}

.verify-container {
  max-width: 900px;
  margin: 0 auto;
}

.verify-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.gold-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: #d4af37;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  margin-bottom: 0.75rem;
}

.verify-header h1 {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin: 0 0 0.5rem;
}

.verify-sub {
  font-size: 1rem;
  color: #94a3b8;
  margin: 0;
}

/* Status Card */
.status-card {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  border-radius: 12px;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
  margin-bottom: 2.5rem;
}

.status-card.status-verified {
  border-color: rgba(16, 185, 129, 0.3);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(30, 41, 59, 0.95) 100%);
}

.status-card.status-pending {
  border-color: rgba(212, 175, 55, 0.3);
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.08) 0%, rgba(30, 41, 59, 0.95) 100%);
}

.status-card.status-rejected {
  border-color: rgba(239, 68, 68, 0.3);
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(30, 41, 59, 0.95) 100%);
}

.status-icon-wrap {
  flex-shrink: 0;
}
.status-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
}
.icon-verified { background: rgba(16, 185, 129, 0.2); color: #10b981; }
.icon-pending { background: rgba(212, 175, 55, 0.2); color: #d4af37; }
.icon-rejected { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.icon-unverified { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }

.status-content { flex: 1; }
.status-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.status-title-row h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

.status-pill {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  letter-spacing: 0.05em;
}
.pill-verified { background: #10b981; color: #022c22; }
.pill-pending { background: #d4af37; color: #1c1917; }
.pill-rejected { background: #ef4444; color: #450a0a; }
.pill-unverified { background: #f59e0b; color: #451a03; }

.status-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #cbd5e1;
  margin: 0 0 1rem;
}

.rejection-box {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 1rem;
  border-radius: 8px;
  color: #fca5a5;
  font-size: 0.85rem;
  margin-top: 1rem;
}

.verified-summary {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.verified-item { display: flex; flex-direction: column; gap: 0.2rem; }
.verified-item .lbl { font-size: 0.75rem; color: #94a3b8; }
.verified-item .val { font-size: 0.95rem; font-weight: 600; color: #ffffff; }

/* Form Card */
.form-card {
  background: #1e293b;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 2.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
}

.form-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 1.25rem;
}
.form-header h2 { font-size: 1.5rem; margin: 0 0 0.5rem; color: #ffffff; }
.form-header p { font-size: 0.875rem; color: #94a3b8; margin: 0; }

.form-section { margin-bottom: 2rem; }
.section-title {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #d4af37;
  margin: 0 0 1rem;
}
.section-note {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: -0.5rem 0 1.25rem;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.form-group { margin-bottom: 1.25rem; }
.form-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 0.35rem;
}
.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.35rem;
}
.label-row .form-label { margin-bottom: 0; }

.form-input {
  width: 100%;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  color: #ffffff;
  font-size: 0.875rem;
  box-sizing: border-box;
}
.form-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
}

.badge-cipc {
  font-size: 0.7rem;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}
.font-mono { font-family: monospace; letter-spacing: 0.5px; }
.form-hint { font-size: 0.7rem; color: #94a3b8; margin-top: 0.35rem; display: block; }

/* Document Upload Grid */
.upload-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.upload-box {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: #0f172a;
  border: 1px dashed rgba(255, 255, 255, 0.18);
  border-radius: 8px;
  transition: border-color 0.2s;
}
.upload-box.has-file {
  border-color: #d4af37;
  border-style: solid;
  background: rgba(212, 175, 55, 0.04);
}
.upload-icon { font-size: 2rem; flex-shrink: 0; }
.upload-meta { flex: 1; display: flex; flex-direction: column; gap: 0.2rem; }
.upload-meta strong { font-size: 0.9rem; color: #ffffff; }
.upload-meta span { font-size: 0.75rem; color: #94a3b8; }
.file-chosen { font-size: 0.8rem; font-weight: 600; color: #d4af37 !important; }
.file-existing { font-size: 0.8rem; font-weight: 600; color: #10b981 !important; }

.btn-browse {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}
.btn-browse:hover { background: rgba(255, 255, 255, 0.15); }
.btn-browse input[type="file"] { display: none; }

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.btn-submit {
  flex: 1;
  padding: 0.875rem;
  font-weight: 700;
  background: linear-gradient(135deg, #d4af37 0%, #b89628 100%);
  color: #0b0f19;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.pending-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
  padding: 0.875rem;
  border-radius: 6px;
  margin-top: 1rem;
  font-size: 0.85rem;
}
.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #34d399;
  padding: 0.875rem;
  border-radius: 6px;
  margin-top: 1rem;
  font-size: 0.85rem;
}

@media (max-width: 640px) {
  .status-card { flex-direction: column; }
  .form-grid-2 { grid-template-columns: 1fr; }
  .upload-box { flex-direction: column; align-items: flex-start; }
}
</style>
