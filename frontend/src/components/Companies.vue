<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Businesses</h1>
        <p class="page-subtitle">Corporate business directory, institutional clients, and CIPC compliance</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="openAddBusiness" :disabled="!canAddCompany">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Add Business
        </button>
      </div>
    </div>

    <div v-if="!canAddCompany" class="info-bar info-bar--amber">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>
      <span>Capture at least one contact before creating a business profile. Add a contact first, then return here.</span>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input class="form-input" v-model="searchTerm" placeholder="Search businesses by name, CIPC number, email...">
      </div>
    </div>

    <div class="card table-card">
      <table class="data-table" v-if="filteredCompanies.length">
        <thead>
          <tr>
            <th>Business Entity &amp; CIPC</th>
            <th>Industry</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Address</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in filteredCompanies" :key="company.id">
            <td>
              <div class="business-name-cell">
                <strong>{{ company.name }}</strong>
                <div v-if="company.trading_name" class="trading-name-tag">
                  T/A {{ company.trading_name }}
                </div>
                <div v-if="company.registration_number" class="cipc-table-tag">
                  <span class="cipc-dot"></span> CIPC: {{ company.registration_number }}
                </div>
              </div>
            </td>
            <td>{{ company.industry || '---' }}</td>
            <td>{{ company.email || '---' }}</td>
            <td>{{ company.phone || '---' }}</td>
            <td class="cell-truncate">{{ company.address || '---' }}</td>
            <td>
              <div class="row-actions">
                <button class="btn btn-sm btn-secondary" @click="editCompany(company)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteCompany(company.id)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v3"/></svg>
        <p>No business profiles found.</p>
      </div>
    </div>

    <!-- Add / Edit Business Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>{{ showAddModal ? 'Add Business' : 'Edit Business' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveCompany">
            <div class="form-group">
              <label class="form-label">Company Registered Legal Name *</label>
              <input class="form-input" v-model="companyForm.name" placeholder="e.g. Acme Holdings (Pty) Ltd" required>
            </div>
            
            <div class="form-group">
              <label class="form-label">Trading Name (Trading As / T/A)</label>
              <input class="form-input" v-model="companyForm.trading_name" placeholder="e.g. Acme Luxury Solutions">
              <span class="form-hint">Trading name if different from official registered entity name</span>
            </div>

            <div class="form-group">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
                <label class="form-label" style="margin:0">CIPC Registration Number</label>
                <span v-if="cipcStatus.state === 'valid'" class="badge-cipc-success">✓ {{ cipcStatus.entityLabel }}</span>
              </div>
              <input 
                class="form-input font-mono" 
                v-model="companyForm.registration_number" 
                @input="onCipcInput"
                placeholder="YYYY/NNNNNN/NN (e.g. 2024/123456/07)"
                maxlength="14"
              >
              <span class="form-hint" v-if="cipcStatus.message">{{ cipcStatus.message }}</span>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">SARS Tax / VAT Number</label>
                <input class="form-input font-mono" v-model="companyForm.tax_number" placeholder="10-digit Tax Ref" maxlength="10">
              </div>
              <div class="form-group">
                <label class="form-label">Industry / Sector</label>
                <input class="form-input" v-model="companyForm.industry" placeholder="e.g. Mining / Finance / Luxury Retail">
              </div>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Official Email</label>
                <input class="form-input" v-model="companyForm.email" type="email" placeholder="corporate@company.co.za">
              </div>
              
              <div class="form-group">
                <label class="form-label">Official Phone</label>
                <input class="form-input" v-model="companyForm.phone" placeholder="+27 (0) 11 ...">
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">Registered Physical Address</label>
              <textarea class="form-input" v-model="companyForm.address" placeholder="Physical head office address..." rows="3"></textarea>
            </div>
            
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary">{{ showAddModal ? 'Create Business' : 'Save Changes' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { companiesAPI, systemAPI } from '../api'
import modal from '../utils/modal'

export default {
  name: 'Companies',
  data() {
    return {
      companies: [],
      contactCount: 0,
      loadingPrereq: false,
      searchTerm: '',
      showAddModal: false,
      showEditModal: false,
      companyForm: {
        name: '',
        trading_name: '',
        registration_number: '',
        tax_number: '',
        industry: '',
        email: '',
        phone: '',
        address: '',
        client_type: 'company'
      },
      editingId: null
    }
  },
  computed: {
    filteredCompanies() {
      const q = (this.searchTerm || '').toLowerCase()
      return this.companies.filter(c => {
        return (c.name && c.name.toLowerCase().includes(q)) ||
          (c.trading_name && c.trading_name.toLowerCase().includes(q)) ||
          (c.registration_number && c.registration_number.toLowerCase().includes(q)) ||
          (c.email && c.email.toLowerCase().includes(q)) ||
          (c.industry && c.industry.toLowerCase().includes(q))
      })
    },
    canAddCompany() {
      return this.contactCount > 0
    },
    cipcStatus() {
      const val = (this.companyForm.registration_number || '').trim()
      if (!val) return { state: 'empty', message: '', entityLabel: '' }
      const cipcRegex = /^(19|20)\d{2}\/\d{6}\/\d{2}$/
      if (cipcRegex.test(val)) {
        const suffix = val.slice(-2)
        const suffixMap = {
          '07': 'Private Company (Pty Ltd)',
          '06': 'Public Company (Ltd)',
          '23': 'Close Corporation (CC)',
          '08': 'Non-Profit Company (NPC)',
          '21': 'Incorporated (Inc)',
          '10': 'External / Foreign'
        }
        const label = suffixMap[suffix] || 'Registered Corporate Entity'
        return { state: 'valid', entityLabel: label, message: `Official CIPC Match: ${label}` }
      }
      return { state: 'incomplete', entityLabel: '', message: 'Standard CIPC format: YYYY/NNNNNN/NN (e.g. 2024/123456/07)' }
    }
  },
  async mounted() {
    await this.refreshPrerequisites()
    await this.loadCompanies()
  },
  methods: {
    async refreshPrerequisites() {
      if (this.loadingPrereq) return
      this.loadingPrereq = true
      try {
        const response = await systemAPI.getPrerequisites()
        this.contactCount = response.data?.contacts || 0
      } catch (error) {
        console.warn('Could not refresh prerequisites for companies:', error)
        this.contactCount = 0
      } finally {
        this.loadingPrereq = false
      }
    },
    async loadCompanies() {
      try {
        const response = await companiesAPI.getAll()
        this.companies = response.data
      } catch (error) {
        console.error('Error loading companies:', error)
      }
    },
    async openAddBusiness() {
      await this.refreshPrerequisites()
      if (!this.canAddCompany) {
        await modal.warning('Contact Required', 'Capture at least one contact before creating a business client profile. Add a contact first, then return here.')
        this.$router.push('/contacts')
        return
      }
      this.resetForm()
      this.showAddModal = true
    },
    resetForm() {
      this.companyForm = {
        name: '',
        trading_name: '',
        registration_number: '',
        tax_number: '',
        industry: '',
        email: '',
        phone: '',
        address: '',
        client_type: 'company'
      }
      this.editingId = null
    },
    onCipcInput(e) {
      let v = e.target.value.replace(/[^0-9/]/g, '').toUpperCase()
      const digitsOnly = v.replace(/\//g, '')
      if (digitsOnly.length > 4 && digitsOnly.length <= 10) {
        v = `${digitsOnly.slice(0, 4)}/${digitsOnly.slice(4)}`
      } else if (digitsOnly.length > 10) {
        v = `${digitsOnly.slice(0, 4)}/${digitsOnly.slice(4, 10)}/${digitsOnly.slice(10, 12)}`
      }
      this.companyForm.registration_number = v.slice(0, 14)
    },
    async saveCompany() {
      try {
        this.companyForm.client_type = 'company'
        if (this.showAddModal) {
          await companiesAPI.create(this.companyForm)
        } else {
          await companiesAPI.update(this.editingId, this.companyForm)
        }
        await this.loadCompanies()
        await this.refreshPrerequisites()
        this.closeModal()
      } catch (error) {
        console.error('Error saving company:', error)
      }
    },
    editCompany(company) {
      this.companyForm = { 
        ...company,
        client_type: 'company'
      }
      this.editingId = company.id
      this.showEditModal = true
    },
    async deleteCompany(id) {
      const ok = await modal.danger('Delete Business', 'Are you sure you want to delete this business profile? This action cannot be undone.')
      if (ok) {
        try {
          await companiesAPI.delete(id)
          await this.loadCompanies()
        } catch (error) {
          console.error('Error deleting company:', error)
        }
      }
    },
    closeModal() {
      this.showAddModal = false
      this.showEditModal = false
      this.resetForm()
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 2rem; max-width: 1400px; margin: 0 auto; }
.page-header { 
  display: flex; justify-content: space-between; align-items: flex-start; 
  margin-bottom: 2rem; gap: 1rem;
}
.page-header h1 { 
  font-size: 1.875rem; font-weight: 700; color: var(--gray-900); 
  margin-bottom: 0.25rem; 
}
.page-subtitle { color: var(--gray-500); font-size: 0.875rem; }

.info-bar { 
  display: flex; align-items: center; gap: 0.75rem; 
  padding: 0.875rem 1.25rem; border-radius: var(--radius-md); 
  margin-bottom: 1.5rem; font-size: 0.875rem; 
}
.info-bar--amber { 
  background: #fffbeb; border: 1px solid #fde68a; color: #92400e; 
}

.toolbar { margin-bottom: 1.5rem; }
.search-box { position: relative; max-width: 450px; }
.search-box svg { 
  position: absolute; left: 1rem; top: 50%; 
  transform: translateY(-50%); color: var(--gray-400); 
}
.search-box .form-input { padding-left: 2.75rem; }

.table-card { overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { 
  background: var(--gray-50); padding: 0.875rem 1rem; 
  text-align: left; font-size: 0.75rem; font-weight: 600; 
  color: var(--gray-600); text-transform: uppercase; 
  letter-spacing: 0.05em; border-bottom: 1px solid var(--gray-200); 
}
.data-table td { 
  padding: 1rem; border-bottom: 1px solid var(--gray-100); 
  font-size: 0.875rem; color: var(--gray-800); 
}
.data-table tbody tr:hover { background: var(--gray-50); }

.business-name-cell {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.trading-name-tag {
  font-size: 0.75rem;
  color: var(--gray-500);
}
.cipc-table-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: monospace;
  font-size: 0.7rem;
  color: #10b981;
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.2);
  padding: 1px 6px;
  border-radius: 4px;
  width: fit-content;
}
.cipc-dot { width: 5px; height: 5px; border-radius: 50%; background: #10b981; }

.cell-truncate { 
  max-width: 240px; white-space: nowrap; 
  overflow: hidden; text-overflow: ellipsis; 
}
.col-actions { width: 140px; text-align: right; }
.row-actions { display: flex; gap: 0.5rem; justify-content: flex-end; }

.empty-state { 
  text-align: center; padding: 4rem 2rem; color: var(--gray-400); 
}
.empty-state svg { margin-bottom: 1rem; }

/* Modal */
.modal-overlay { 
  position: fixed; inset: 0; background: rgba(0,0,0,0.5); 
  display: flex; align-items: center; justify-content: center; 
  z-index: 1000; padding: 1rem; backdrop-filter: blur(4px); 
}
.modal-panel { 
  background: var(--surface); border-radius: var(--radius-lg); 
  width: 100%; max-width: 580px; max-height: 90vh; 
  overflow-y: auto; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2); 
}
.modal-header { 
  display: flex; justify-content: space-between; align-items: center; 
  padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--gray-200); 
}
.modal-header h3 { 
  font-size: 1.125rem; font-weight: 600; color: var(--gray-900); 
}
.modal-close { 
  background: none; border: none; font-size: 1.5rem; 
  color: var(--gray-400); cursor: pointer; line-height: 1; 
}
.modal-close:hover { color: var(--gray-600); }
.modal-body { padding: 1.5rem; }
.modal-footer { 
  display: flex; justify-content: flex-end; gap: 0.75rem; 
  margin-top: 1.5rem; padding-top: 1.25rem; 
  border-top: 1px solid var(--gray-200); 
}

.form-group { margin-bottom: 1.25rem; }
.form-label { 
  display: block; font-size: 0.875rem; font-weight: 500; 
  color: var(--gray-700); margin-bottom: 0.375rem; 
}
.form-input { 
  width: 100%; padding: 0.625rem 0.875rem; 
  border: 1px solid var(--gray-300); border-radius: var(--radius-md); 
  font-size: 0.875rem; background: var(--surface); color: var(--gray-900); 
}
.form-input:focus { 
  outline: none; border-color: var(--primary); 
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); 
}
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }

.header-actions { display: flex; gap: 1rem; align-items: center; }
.badge-cipc-success {
  font-size: 0.7rem;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(16, 185, 129, 0.25);
}
.font-mono { font-family: monospace; letter-spacing: 0.5px; }
.form-hint { font-size: 0.7rem; color: #6b7280; margin-top: 0.25rem; display: block; }

@media (max-width: 768px) {
  .page-wrap { padding: 1rem; }
  .page-header { flex-direction: column; }
  .header-actions { width: 100%; }
  .table-card { overflow-x: auto; }
  .form-grid-2 { grid-template-columns: 1fr; }
}
</style>
