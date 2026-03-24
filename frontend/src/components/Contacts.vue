<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Clients</h1>
        <p class="page-subtitle">Manage your CRM clients and relationships</p>
      </div>
      <div class="header-btns">
        <button class="btn btn-secondary" @click="showUploadModal = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          Upload CSV
        </button>
        <div class="add-menu">
          <button class="btn btn-primary" @click="toggleAddMenu">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Add Client
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
          <div v-if="showAddMenu" class="dropdown-menu">
            <button class="dropdown-item" @click="openAddClient('individual')">Add Individual Client</button>
            <button class="dropdown-item" @click="openAddClient('business')">Add Business Client</button>
          </div>
        </div>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input class="form-input" v-model="searchTerm" placeholder="Search clients...">
      </div>
    </div>

    <div class="card table-card">
      <table class="data-table" v-if="filteredContacts.length">
        <thead>
          <tr>
            <th>Type</th>
            <th>Name</th>
            <th>Email</th>
            <th>Company</th>
            <th>Phone</th>
            <th>Health</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contact in filteredContacts" :key="contact.id">
            <td>
              <span class="badge" :class="contact.client_type === 'individual' ? 'badge-individual' : 'badge-business'">
                {{ contact.client_type === 'individual' ? 'Individual' : 'Business' }}
              </span>
            </td>
            <td>
              <strong>{{ contact.first_name }} {{ contact.last_name }}</strong>
              <span v-if="contact.is_self_employed" class="badge badge-green" style="margin-left:0.5rem;">Self-employed</span>
            </td>
            <td>{{ contact.email }}</td>
            <td>{{ contact.company_name || contact.company_name_manual || '---' }}</td>
            <td>{{ contact.phone || contact.company_direct_line || '---' }}</td>
            <td>
              <span class="health-pill" :style="{ background: contact.health_status?.color || '#e5e7eb', color: (contact.health_status?.color && contact.health_status.color !== '#ccc') ? '#fff' : '#374151' }">
                {{ contact.health_score || 0 }}
              </span>
            </td>
            <td>
              <div class="row-actions">
                <button class="btn btn-sm btn-secondary" @click="editContact(contact)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteContact(contact.id)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <p>No clients found.</p>
      </div>
    </div>

    <div v-if="showUploadModal" class="modal-overlay" @click="closeUploadModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Upload Clients from CSV</h3>
          <button class="modal-close" @click="closeUploadModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="upload-info">
            <p><strong>CSV Format Required:</strong></p>
            <p class="text-muted">first_name, last_name, email, phone, company_name_manual</p>
            <p class="upload-example">Example: John, Doe, john@example.com, +27123456789, Acme Corp</p>
          </div>
          <div class="file-upload-area">
            <input type="file" accept=".csv" @change="handleFileSelect" ref="fileInput" id="csv-file-input">
            <label for="csv-file-input" class="file-label">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              <span v-if="!selectedFile">Choose CSV File</span>
              <span v-else>{{ selectedFile.name }}</span>
            </label>
          </div>
          <div v-if="uploadMessage" class="alert" :class="uploadMessageType === 'success' ? 'alert-success' : 'alert-danger'">{{ uploadMessage }}</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeUploadModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="uploadCSV" :disabled="!selectedFile || uploading">{{ uploading ? 'Uploading...' : 'Upload' }}</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>{{ showAddModal ? (contactForm.client_type === 'individual' ? 'Add Individual Client' : 'Add Business Client') : 'Edit Client' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveContact" novalidate>
            <div v-if="formErrors.general" class="alert alert-danger">{{ formErrors.general }}</div>

            <div v-if="showAddModal" class="form-group">
              <label class="form-label">Client Type</label>
              <div class="type-selector">
                <button 
                  type="button" 
                  class="type-btn" 
                  :class="{ active: contactForm.client_type === 'individual' }" 
                  @click="contactForm.client_type = 'individual'"
                >
                  <span class="type-icon">👤</span>
                  <span class="type-name">Individual</span>
                </button>
                <button 
                  type="button" 
                  class="type-btn" 
                  :class="{ active: contactForm.client_type === 'business' }" 
                  @click="contactForm.client_type = 'business'"
                >
                  <span class="type-icon">🏢</span>
                  <span class="type-name">Business</span>
                </button>
              </div>
            </div>

            <div class="form-row-2col">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input class="form-input" v-model="contactForm.first_name" placeholder="First Name" required>
                <p v-if="formErrors.first_name" class="form-error">{{ formErrors.first_name }}</p>
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input class="form-input" v-model="contactForm.last_name" placeholder="Last Name" required>
                <p v-if="formErrors.last_name" class="form-error">{{ formErrors.last_name }}</p>
              </div>
            </div>

            <div v-if="contactForm.client_type === 'business'" class="form-group">
              <label class="form-check-row">
                <input type="checkbox" v-model="contactForm.is_self_employed">
                <span>Self-employed / Independent</span>
              </label>
            </div>

            <div class="form-group">
              <label class="form-label">Email</label>
              <input class="form-input" v-model="contactForm.email" type="email" :placeholder="emailPlaceholder" required>
              <p class="form-hint">{{ emailHint }}</p>
              <p v-if="formErrors.email" class="form-error">{{ formErrors.email }}</p>
            </div>

            <div v-if="contactForm.client_type === 'business'" class="form-group">
              <label class="form-label">{{ contactForm.is_self_employed ? 'Business Trading Name' : 'Company Name' }}</label>
              <div class="input-dropdown-wrap">
                <input class="form-input" v-model="contactForm.company_name_manual"
                  :placeholder="contactForm.is_self_employed ? 'Business trading name' : 'Type or select company'"
                  :required="!contactForm.is_self_employed"
                  @focus="onCompanyInputFocus" @blur="onCompanyInputBlur" @input="onCompanyInput">
                <ul v-if="showCompanySuggestions" class="dropdown-suggestions">
                  <li v-for="name in companyNameSuggestions" :key="name" @mousedown.prevent="selectCompanySuggestion(name)">{{ name }}</li>
                </ul>
              </div>
              <p v-if="!contactForm.is_self_employed" class="form-hint">Start typing for SA company suggestions.</p>
              <p v-if="formErrors.company_name_manual" class="form-error">{{ formErrors.company_name_manual }}</p>
            </div>

            <div class="form-group">
              <label class="form-label">Phone</label>
              <input class="form-input" v-model="contactForm.phone" :placeholder="companyNumberPlaceholder">
              <p v-if="formErrors.phone" class="form-error">{{ formErrors.phone }}</p>
            </div>

            <div v-if="contactForm.client_type === 'business' && !contactForm.is_self_employed" class="form-group">
              <label class="form-label">Direct Company Line</label>
              <input class="form-input" v-model="contactForm.company_direct_line" placeholder="+27 11 234 5678" required>
              <p v-if="formErrors.company_direct_line" class="form-error">{{ formErrors.company_direct_line }}</p>
            </div>

            <div v-if="contactForm.client_type === 'business' && companies.length" class="form-group">
              <label class="form-label">Link to Company (optional)</label>
              <select class="form-input" v-model="contactForm.company" :disabled="contactForm.is_self_employed">
                <option value="">Do not link yet</option>
                <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
              </select>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal" :disabled="formSubmitting">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="formSubmitting">{{ formSubmitting ? 'Saving...' : 'Save' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { contactsAPI, companiesAPI } from '../api'
import saCompanies from '../utils/saCompanies'
import modal from '../utils/modal'

const PERSONAL_EMAIL_DOMAINS = new Set([
  'gmail.com',
  'yahoo.com',
  'outlook.com',
  'hotmail.com',
  'icloud.com',
  'live.com',
  'msn.com',
  'aol.com',
  'protonmail.com',
  'zoho.com',
  'yahoo.co.uk',
  'ymail.com',
  'googlemail.com'
])

export default {
  name: 'Contacts',
  data() {
    return {
      contacts: [],
      companies: [],
      searchTerm: '',
      showAddModal: false,
      showEditModal: false,
      showUploadModal: false,
      showAddMenu: false,
      selectedFile: null,
      uploading: false,
      uploadMessage: '',
      uploadMessageType: '',
      contactForm: {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        is_self_employed: false,
        company_direct_line: '',
        company_name_manual: '',
        company: '',
        client_type: 'business'
      },
      editingId: null,
      formErrors: {},
      formSubmitting: false,
      companyInputFocused: false,
      selfEmployedGeneratedName: ''
    }
  },
  watch: {
    searchTerm: {
      handler(val) {
        clearTimeout(this._searchTimer)
        this._searchTimer = setTimeout(() => this.loadContacts(val), 300)
      }
    },
    'contactForm.is_self_employed'(isSelf) {
      if (isSelf) {
        this.contactForm.company = ''
        this.contactForm.company_direct_line = ''
        this.refreshSelfEmployedGeneratedName(true)
      } else {
        const manual = (this.contactForm.company_name_manual || '').trim()
        const generated = (this.selfEmployedGeneratedName || '').trim()
        if (manual && generated && manual === generated) {
          this.contactForm.company_name_manual = ''
        }
      }
    },
    'contactForm.first_name'() {
      this.refreshSelfEmployedGeneratedName()
    },
    'contactForm.last_name'() {
      this.refreshSelfEmployedGeneratedName()
    }
  },
  computed: {
    filteredContacts() {
      const term = this.searchTerm.toLowerCase()
      return this.contacts.filter(contact => 
        contact.first_name.toLowerCase().includes(term) ||
        contact.last_name.toLowerCase().includes(term) ||
        contact.email.toLowerCase().includes(term) ||
        (contact.company_name && contact.company_name.toLowerCase().includes(term)) ||
        (contact.company_name_manual && contact.company_name_manual.toLowerCase().includes(term))
      )
    },
    emailPlaceholder() {
      return this.contactForm.is_self_employed ? 'Business email address' : 'Company email address'
    },
    emailHint() {
      return this.contactForm.is_self_employed
        ? 'Use the email address you operate your business with.'
        : 'Use a professional/company email address for this contact.'
    },
    companyNumberPlaceholder() {
      return this.contactForm.is_self_employed
        ? 'Company number (optional)'
        : 'Company number (optional)'
    },
    companyNameSuggestions() {
      const query = (this.contactForm.company_name_manual || '').trim().toLowerCase()
      if (!query) {
        return saCompanies.slice(0, 8)
      }
      return saCompanies
        .filter(name => name.toLowerCase().includes(query))
        .slice(0, 8)
    },
    showCompanySuggestions() {
      return (
        !this.contactForm.is_self_employed &&
        this.companyInputFocused &&
        this.companyNameSuggestions.length > 0
      )
    }
  },
  async mounted() {
    await this.loadContacts()
    await this.loadCompanies()
  },
  methods: {
    async loadContacts() {
      try {
        const response = await contactsAPI.getAll()
        this.contacts = response.data
      } catch (error) {
        console.error('Error loading contacts:', error)
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
    toggleAddMenu() {
      this.showAddMenu = !this.showAddMenu
    },
    openAddClient(clientType) {
      this.contactForm.client_type = clientType
      this.showAddModal = true
      this.showAddMenu = false
    },
    refreshSelfEmployedGeneratedName(force = false) {
      const newName = this.computeSelfEmployedGeneratedName()
      const previousGenerated = this.selfEmployedGeneratedName
      this.selfEmployedGeneratedName = newName

      if (!this.contactForm.is_self_employed) {
        return
      }

      const manual = (this.contactForm.company_name_manual || '').trim()
      const shouldReplace =
        force ||
        !manual ||
        manual === previousGenerated ||
        manual === 'Self-Employed' ||
        manual === 'Self-Employed Business'

      if (shouldReplace) {
        this.contactForm.company_name_manual = newName
      }
    },
    computeSelfEmployedGeneratedName() {
      const first = (this.contactForm.first_name || '').trim()
      const last = (this.contactForm.last_name || '').trim()
      const combined = [first, last].filter(Boolean).join(' ')
      return combined ? `${combined} (Self-Employed)` : 'Self-Employed Business'
    },
    async saveContact() {
      this.formErrors = {}

      const payload = {
        ...this.contactForm,
        company: this.contactForm.company || null
      }

      payload.company_name_manual = (payload.company_name_manual || '').trim()
      if (payload.is_self_employed && !payload.company_name_manual) {
        payload.company_name_manual = 'Self-Employed'
      }

      if (payload.is_self_employed) {
        payload.company_direct_line = ''
      } else {
        payload.company_direct_line = (payload.company_direct_line || '').trim()
      }

      const validationErrors = this.performClientValidation(payload)
      if (Object.keys(validationErrors).length) {
        this.formErrors = validationErrors
        return
      }

      this.formSubmitting = true

      try {
        if (this.showAddModal) {
          await contactsAPI.create(payload)
        } else {
          await contactsAPI.update(this.editingId, payload)
        }
        await this.loadContacts()
        await this.loadCompanies()
        this.closeModal()
      } catch (error) {
        console.error('Error saving contact:', error)
        this.formErrors = this.extractErrors(error)
      } finally {
        this.formSubmitting = false
      }
    },
    editContact(contact) {
      this.contactForm = {
        first_name: contact.first_name,
        last_name: contact.last_name,
        email: contact.email,
        phone: contact.phone || '',
        is_self_employed: Boolean(contact.is_self_employed),
        company_direct_line: contact.company_direct_line || '',
        company_name_manual: contact.company_name_manual || contact.company_name || '',
        company: contact.company || '',
        client_type: contact.client_type || 'business'
      }
      this.editingId = contact.id
      this.showEditModal = true
      this.formErrors = {}
      this.companyInputFocused = false
      this.refreshSelfEmployedGeneratedName(false)
    },
    async deleteContact(id) {
      const ok = await modal.danger('Delete Contact', 'Are you sure you want to delete this contact? This action cannot be undone.')
      if (ok) {
        try {
          await contactsAPI.delete(id)
          await this.loadContacts()
        } catch (error) {
          console.error('Error deleting contact:', error)
        }
      }
    },
    closeModal() {
      this.showAddModal = false
      this.showEditModal = false
      this.showAddMenu = false
      this.resetForm()
    },
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0]
      this.uploadMessage = ''
    },
    closeUploadModal() {
      this.showUploadModal = false
      this.selectedFile = null
      this.uploadMessage = ''
      this.uploading = false
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },
    async uploadCSV() {
      if (!this.selectedFile) return
      
      this.uploading = true
      this.uploadMessage = ''
      
      try {
        const response = await contactsAPI.importCSV(this.selectedFile)
        this.uploadMessage = `✅ Successfully uploaded ${response.data.created || 0} contacts!`
        this.uploadMessageType = 'success'
        await this.loadContacts()
        
        setTimeout(() => {
          this.closeUploadModal()
        }, 2000)
      } catch (error) {
        console.error('Error uploading CSV:', error)
        this.uploadMessage = `❌ Upload failed: ${error.response?.data?.error || error.message || 'Unknown error'}`
        this.uploadMessageType = 'error'
      } finally {
        this.uploading = false
      }
    },
    onCompanyInputFocus() {
      this.companyInputFocused = true
      if (this._companyBlurTimeout) {
        clearTimeout(this._companyBlurTimeout)
        this._companyBlurTimeout = null
      }
    },
    onCompanyInputBlur() {
      this._companyBlurTimeout = setTimeout(() => {
        this.companyInputFocused = false
      }, 150)
    },
    onCompanyInput() {
      if (this.contactForm.is_self_employed) {
        const manual = (this.contactForm.company_name_manual || '').trim()
        const generated = (this.selfEmployedGeneratedName || '').trim()
        if (manual && generated && manual.toLowerCase() !== generated.toLowerCase()) {
          this.contactForm.is_self_employed = false
        }
      }
    },
    selectCompanySuggestion(name) {
      this.contactForm.company_name_manual = name
      this.companyInputFocused = false
    },
    performClientValidation(payload) {
      const errors = {}

      if (!payload.first_name.trim()) {
        errors.first_name = 'First name is required.'
      }
      if (!payload.last_name.trim()) {
        errors.last_name = 'Last name is required.'
      }

      const email = (payload.email || '').trim()
      if (!email) {
        errors.email = 'Email is required.'
      } else if (!this.isValidEmail(email)) {
        errors.email = 'Enter a valid email address.'
      } else if (!payload.is_self_employed && this.isPersonalEmailDomain(email)) {
        errors.email = 'Please use a professional/company email address unless the contact is self-employed.'
      }

      if (!payload.is_self_employed && !payload.company_direct_line) {
        errors.company_direct_line = 'Corporate contacts must include a direct company line.'
      }

      if (!payload.is_self_employed && !payload.company_name_manual) {
        errors.company_name_manual = 'Please capture the company name for this contact.'
      }

      return errors
    },
    extractErrors(error) {
      const fallback = { general: 'Unable to save contact. Please try again.' }
      if (!error.response || !error.response.data) {
        return fallback
      }

      const data = error.response.data
      const mapped = {}

      Object.entries(data).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          mapped[key] = value.join(' ')
        } else if (typeof value === 'string') {
          mapped[key] = value
        } else if (value && typeof value === 'object') {
          mapped[key] = Object.values(value).join(' ')
        }
      })

      if (mapped.non_field_errors) {
        mapped.general = mapped.non_field_errors
        delete mapped.non_field_errors
      }

      return Object.keys(mapped).length ? mapped : fallback
    },
    resetForm() {
      this.contactForm = {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        is_self_employed: false,
        company_direct_line: '',
        company_name_manual: '',
        company: '',
        client_type: 'business'
      }
      this.formErrors = {}
      this.formSubmitting = false
      this.companyInputFocused = false
      this.editingId = null
      this.selfEmployedGeneratedName = ''
    },
    isPersonalEmailDomain(email) {
      const domain = email.split('@').pop().toLowerCase()
      return PERSONAL_EMAIL_DOMAINS.has(domain)
    },
    isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 1.5rem 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; gap: 1rem; flex-wrap: wrap; }
.page-header h1 { font-size: 1.75rem; font-weight: 700; color: var(--gray-900); margin: 0; }
.page-subtitle { color: var(--gray-500); font-size: 0.9rem; margin: 0.25rem 0 0; }
.header-btns { display: flex; gap: 0.75rem; }
.header-btns .btn { display: inline-flex; align-items: center; gap: 0.5rem; }
.toolbar { margin-bottom: 1rem; }
.search-box { position: relative; max-width: 360px; }
.search-box svg { position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: var(--gray-400); pointer-events: none; }
.search-box .form-input { padding-left: 2.25rem; }
.table-card { padding: 0; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch; }
.col-actions { width: 160px; }
.row-actions { display: flex; gap: 0.5rem; }
.health-pill { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; min-width: 32px; text-align: center; }
/* Upload */
.upload-info { margin-bottom: 1rem; }
.upload-info p { margin: 0.25rem 0; font-size: 0.875rem; }
.upload-example { font-family: monospace; font-size: 0.8rem; color: var(--gray-500); }
.text-muted { color: var(--gray-500); }
.file-upload-area { margin-bottom: 1rem; }
.file-upload-area input[type="file"] { display: none; }
.file-label { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; border: 2px dashed var(--gray-300); border-radius: var(--radius-md); cursor: pointer; font-size: 0.875rem; color: var(--gray-600); transition: border-color 0.2s; }
.file-label:hover { border-color: var(--primary-400); }
.alert { padding: 0.75rem 1rem; border-radius: var(--radius-md); font-size: 0.875rem; font-weight: 500; margin-bottom: 1rem; }
.alert-danger { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
.alert-success { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
/* Form helpers */
.form-row-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-check-row { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: var(--gray-700); font-weight: 500; cursor: pointer; }
.form-check-row input[type="checkbox"] { width: 16px; height: 16px; accent-color: var(--primary-500); }
.input-dropdown-wrap { position: relative; }
.dropdown-suggestions { position: absolute; top: 100%; left: 0; right: 0; background: #fff; border: 1px solid var(--gray-200); border-radius: var(--radius-md); max-height: 200px; overflow-y: auto; box-shadow: var(--shadow-md); z-index: 20; list-style: none; padding: 0; margin: 0.25rem 0 0; }
.dropdown-suggestions li { padding: 0.6rem 0.75rem; font-size: 0.875rem; cursor: pointer; }
.dropdown-suggestions li:hover { background: var(--primary-50); }

/* Type selector */
.type-selector { 
  display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; 
  margin-bottom: 1rem;
}
.type-btn { 
  display: flex; flex-direction: column; align-items: center; gap: 0.75rem; 
  padding: 1rem; border: 2px solid var(--gray-300); border-radius: var(--radius-md); 
  background: var(--gray-50); cursor: pointer; 
  transition: all 0.2s;
  font-family: inherit;
}
.type-btn:hover { border-color: var(--primary); background: #eff6ff; }
.type-btn.active { 
  border-color: var(--primary); background: var(--primary); color: white; 
}
.type-icon { font-size: 2rem; }
.type-name { font-size: 0.875rem; font-weight: 600; }

/* Client type badges */
.badge-individual { background: #fef3c7; color: #92400e; }
.badge-business { background: #dbeafe; color: #1e3a8a; }

/* Dropdown menu */
.add-menu { position: relative; }
.dropdown-menu { 
  position: absolute; top: 100%; right: 0; 
  background: var(--gray-50); border: 1px solid var(--gray-200); 
  border-radius: var(--radius-md); min-width: 200px; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
  z-index: 100; margin-top: 0.5rem;
}
.dropdown-item { 
  display: block; width: 100%; padding: 0.75rem 1rem; 
  background: none; border: none; text-align: left; 
  font-size: 0.875rem; cursor: pointer; 
  transition: background 0.2s;
  font-family: inherit;
}
.dropdown-item:hover { background: var(--gray-100); }
.dropdown-item:first-child { border-radius: var(--radius-md) var(--radius-md) 0 0; }
.dropdown-item:last-child { border-radius: 0 0 var(--radius-md) var(--radius-md); }

@media (max-width: 768px) {
  .page-wrap { padding: 1rem; }
  .page-header { flex-direction: column; }
  .header-btns { width: 100%; }
  .header-btns .btn { flex: 1; justify-content: center; }
  .table-card { overflow-x: auto; }
  .form-row-2col { grid-template-columns: 1fr; }
}
</style>
