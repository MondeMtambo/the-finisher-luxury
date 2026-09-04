<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Clients</h1>
        <p class="page-subtitle">Manage your corporate B2B clients, relationships, and compliance documents</p>
      </div>
      <div class="header-btns">
        <button class="btn btn-secondary" @click="showUploadModal = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          Upload CSV
        </button>
        <button class="btn btn-primary btn-add-business" @click="openAddContact">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          + Add Business Client
        </button>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input class="form-input" v-model="searchTerm" placeholder="Search clients, companies, or CIPC reg...">
      </div>
    </div>

    <div class="card table-card">
      <table class="data-table" v-if="filteredContacts.length">
        <thead>
          <tr>
            <th>Client Name</th>
            <th>Business / Trading Entity</th>
            <th>CIPC / Tax Ref</th>
            <th>Email &amp; Direct Line</th>
            <th>Compliance Docs</th>
            <th>Health</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contact in filteredContacts" :key="contact.id">
            <td>
              <strong>{{ contact.first_name }} {{ contact.last_name }}</strong>
              <div v-if="contact.is_self_employed" class="badge-tag-wrap mt-1">
                <span class="badge badge-warning">Freelancer / Sole Prop</span>
              </div>
              <div v-else class="badge-tag-wrap mt-1">
                <span class="badge badge-business">Corporate B2B</span>
              </div>
            </td>
            <td>
              <div class="company-cell-name">{{ contact.company_name || contact.company_name_manual || '---' }}</div>
            </td>
            <td>
              <div v-if="contact.cipc_number" class="cipc-chip font-mono">
                <span class="cipc-label">CIPC:</span> {{ contact.cipc_number }}
              </div>
              <div v-if="contact.tax_number" class="text-muted text-xs mt-1 font-mono">
                VAT: {{ contact.tax_number }}
              </div>
              <span v-if="!contact.cipc_number && !contact.tax_number" class="text-muted text-xs">—</span>
            </td>
            <td>
              <div>{{ contact.email }}</div>
              <div class="text-muted text-xs mt-1">{{ contact.company_direct_line || contact.phone || '—' }}</div>
            </td>
            <td>
              <a v-if="contact.document_url" :href="formatDocUrl(contact.document_url)" target="_blank" class="doc-attachment-badge" title="View attached compliance document">
                📄 View Doc
              </a>
              <span v-else class="text-muted text-xs">None</span>
            </td>
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
        <p>No business clients found.</p>
        <button class="btn btn-primary btn-sm mt-3" @click="openAddContact">+ Add First Business Client</button>
      </div>
    </div>

    <!-- CSV Upload Modal -->
    <div v-if="showUploadModal" class="modal-overlay" @click="closeUploadModal">
      <div class="modal-panel luxury-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title-wrap">
            <span class="modal-badge-tag">BULK ONBOARDING</span>
            <h3>Upload Clients from CSV</h3>
          </div>
          <button class="modal-close" @click="closeUploadModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="upload-info">
            <p><strong>Required CSV Headers:</strong></p>
            <p class="text-muted">first_name, last_name, email, phone, company_name_manual, cipc_number</p>
            <p class="upload-example">Example: John, Doe, john@acme.co.za, +27112345678, Acme Holdings (Pty) Ltd, 2024/123456/07</p>
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

    <!-- Add / Edit Business Client Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel luxury-modal modal-scrollable" @click.stop>
        <div class="modal-header">
          <div class="modal-title-wrap">
            <span class="modal-badge-tag">B2B CLIENT REGISTRATION</span>
            <h3>{{ showAddModal ? 'Add Business Client' : 'Edit Business Client' }}</h3>
            <p class="modal-sub">Register corporate B2B clients or freelance consultants with compliance validation.</p>
          </div>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveContact" novalidate>
            <div v-if="formErrors.general" class="alert alert-danger">{{ formErrors.general }}</div>

            <!-- SECTION 1: PRIMARY CONTACT REPRESENTATIVE -->
            <div class="form-section-card">
              <div class="section-card-title">
                <span class="section-num">1</span>
                <h4>Primary Representative</h4>
              </div>
              <div class="form-row-2col">
                <div class="form-group">
                  <label class="form-label">First Name *</label>
                  <input class="form-input" v-model="contactForm.first_name" placeholder="First Name" required>
                  <p v-if="formErrors.first_name" class="form-error">{{ formErrors.first_name }}</p>
                </div>
                <div class="form-group">
                  <label class="form-label">Last Name *</label>
                  <input class="form-input" v-model="contactForm.last_name" placeholder="Last Name" required>
                  <p v-if="formErrors.last_name" class="form-error">{{ formErrors.last_name }}</p>
                </div>
              </div>

              <div class="form-row-2col">
                <div class="form-group">
                  <label class="form-label">{{ contactForm.is_self_employed ? 'Contact / Business Email *' : 'Corporate Email Address *' }}</label>
                  <input class="form-input" v-model="contactForm.email" type="email" :placeholder="emailPlaceholder" required>
                  <p class="form-hint">{{ emailHint }}</p>
                  <p v-if="formErrors.email" class="form-error">{{ formErrors.email }}</p>
                </div>
                <div class="form-group">
                  <label class="form-label">Direct Mobile Phone</label>
                  <input class="form-input" v-model="contactForm.phone" placeholder="+27 82 123 4567">
                  <p v-if="formErrors.phone" class="form-error">{{ formErrors.phone }}</p>
                </div>
              </div>
            </div>

            <!-- SECTION 2: BUSINESS STRUCTURE & CLASSIFICATION -->
            <div class="form-section-card">
              <div class="section-card-title">
                <span class="section-num">2</span>
                <h4>Business Entity &amp; Structure</h4>
              </div>

              <!-- SELF-EMPLOYED / FREELANCER TOGGLE -->
              <div class="self-employed-box" :class="{ active: contactForm.is_self_employed }">
                <label class="form-check-row">
                  <input type="checkbox" v-model="contactForm.is_self_employed">
                  <div>
                    <span class="checkbox-headline">Self-employed / Freelancer / Sole Proprietor</span>
                    <p class="checkbox-desc">Tick if this client is an independent contractor, doctor, attorney, or freelancer without corporate company registration.</p>
                  </div>
                </label>
              </div>

              <!-- IF FREELANCE / SELF-EMPLOYED -->
              <div v-if="contactForm.is_self_employed" class="form-group mt-3">
                <label class="form-label">Practice / Trading Name *</label>
                <input class="form-input" v-model="contactForm.company_name_manual" placeholder="e.g. Dr. Jane Smith Consulting" required>
                <p class="form-hint">Trading name or practice identity used for invoicing and client representation.</p>
                <p v-if="formErrors.company_name_manual" class="form-error">{{ formErrors.company_name_manual }}</p>
              </div>

              <!-- IF CORPORATE / REGISTERED BUSINESS -->
              <div v-else class="corporate-fields-block mt-3">
                <div class="form-group">
                  <label class="form-label">Search Registered SA Companies (Optional Autocomplete)</label>
                  <div class="company-search-wrap">
                    <input 
                      class="form-input" 
                      v-model="contactForm.company_search"
                      @focus="showCompanyDropdown = true"
                      @blur="onCompanySearchBlur"
                      @input="onCompanySearchInput"
                      placeholder="Type to search known entities (ABSA, FNB, Discovery, Vodacom...)"
                      type="text"
                    >
                    <ul v-if="showCompanyDropdown && filteredCompanies.length" class="company-dropdown">
                      <li v-for="company in filteredCompanies" :key="company.id" @mousedown.prevent="selectCompany(company)">
                        <span class="company-logo">{{ company.logo }}</span>
                        <div class="company-info">
                          <strong>{{ company.name }}</strong>
                          <span class="company-type">{{ company.type }}</span>
                        </div>
                      </li>
                    </ul>
                  </div>
                  <p v-if="selectedCompany" class="form-hint text-gold">✓ {{ selectedCompany.name }} profile linked</p>
                </div>

                <div class="form-group" v-if="!contactForm.company_search">
                  <label class="form-label">Company Legal Name *</label>
                  <div class="input-dropdown-wrap">
                    <input class="form-input" v-model="contactForm.company_name_manual"
                      placeholder="e.g. Acme Logistics (Pty) Ltd"
                      required
                      @focus="onCompanyInputFocus" @blur="onCompanyInputBlur" @input="onCompanyInput">
                    <ul v-if="showCompanySuggestions" class="dropdown-suggestions">
                      <li v-for="name in companyNameSuggestions" :key="name" @mousedown.prevent="selectCompanySuggestion(name)">{{ name }}</li>
                    </ul>
                  </div>
                  <p class="form-hint">Official registered name as per CIPC registry.</p>
                  <p v-if="formErrors.company_name_manual" class="form-error">{{ formErrors.company_name_manual }}</p>
                </div>

                <div class="form-row-2col">
                  <div class="form-group">
                    <label class="form-label">CIPC Registration Number</label>
                    <input class="form-input font-mono" v-model="contactForm.cipc_number" placeholder="2024/123456/07">
                    <p class="form-hint">Official South African CIPC registration format (YYYY/NNNNNN/NN).</p>
                    <p v-if="formErrors.cipc_number" class="form-error">{{ formErrors.cipc_number }}</p>
                  </div>
                  <div class="form-group">
                    <label class="form-label">SARS Tax / VAT Number</label>
                    <input class="form-input font-mono" v-model="contactForm.tax_number" placeholder="4123456789">
                    <p class="form-hint">SARS corporate tax reference or VAT identification number.</p>
                    <p v-if="formErrors.tax_number" class="form-error">{{ formErrors.tax_number }}</p>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">Direct Company Landline *</label>
                  <input class="form-input" v-model="contactForm.company_direct_line" placeholder="+27 11 234 5678" required>
                  <p class="form-hint">Mandatory direct line for institutional verification.</p>
                  <p v-if="formErrors.company_direct_line" class="form-error">{{ formErrors.company_direct_line }}</p>
                </div>

                <div v-if="companies.length" class="form-group">
                  <label class="form-label">Link to Existing Workspace Company</label>
                  <select class="form-input" v-model="contactForm.company">
                    <option value="">Do not link to an existing company</option>
                    <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
                  </select>
                </div>
              </div>

              <!-- DYNAMIC ENTERPRISE FIELDS IF SA COMPANY SELECTED -->
              <div v-if="selectedCompany && selectedCompany.requiredFields && selectedCompany.requiredFields.length" class="dynamic-fields-section">
                <div class="section-divider">
                  <h4>{{ selectedCompany.name }} - Specialized Institutional Fields</h4>
                  <span class="section-icon">{{ selectedCompany.logo }}</span>
                </div>
                <div v-for="fieldKey in selectedCompany.requiredFields" :key="fieldKey" class="form-group">
                  <component 
                    :is="getDynamicFieldComponent(fieldKey)"
                    :field-key="fieldKey"
                    :field-def="getDynamicFieldDef(fieldKey)"
                    :value="contactForm.dynamicFields[fieldKey]"
                    @input="contactForm.dynamicFields[fieldKey] = $event"
                  />
                </div>
              </div>
            </div>

            <!-- SECTION 3: COMPLIANCE & CLIENT DOCUMENTS -->
            <div class="form-section-card">
              <div class="section-card-title">
                <span class="section-num">3</span>
                <h4>Compliance &amp; Verification Documents</h4>
              </div>
              <p class="text-muted text-sm mb-3">Upload official client compliance records (CIPC CoR 14.3 certificate, proof of business address, SARS tax clearance, or director ID).</p>

              <div class="custom-file-box">
                <input type="file" ref="clientDocInput" id="client-doc-file" accept=".pdf,.png,.jpg,.jpeg,.docx" @change="handleDocFileSelect" class="d-none">
                <label for="client-doc-file" class="file-drop-label">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
                  <span v-if="!selectedDocFile && !existingDocUrl">Click to attach CIPC / Compliance document (PDF, PNG, JPG)</span>
                  <span v-else-if="selectedDocFile" class="text-gold font-bold">📄 Selected: {{ selectedDocFile.name }}</span>
                  <span v-else class="text-green font-bold">✓ Existing Document Attached (Click to replace)</span>
                </label>
              </div>

              <div v-if="existingDocUrl" class="mt-2 text-sm">
                <a :href="formatDocUrl(existingDocUrl)" target="_blank" class="doc-attachment-badge">
                  📄 View currently attached document
                </a>
              </div>
            </div>

            <!-- SECTION 4: NOTES & RELATIONSHIP -->
            <div class="form-section-card">
              <div class="section-card-title">
                <span class="section-num">4</span>
                <h4>Relationship &amp; Engagement Notes</h4>
              </div>
              <div class="form-group">
                <textarea class="form-input form-textarea" v-model="contactForm.notes" rows="3" placeholder="Key context, partnership terms, deal background, or engagement guidelines..."></textarea>
              </div>
            </div>

            <div class="modal-footer sticky-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal" :disabled="formSubmitting">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="formSubmitting">
                {{ formSubmitting ? 'Saving...' : (showAddModal ? 'Save Business Client' : 'Update Business Client') }}
              </button>
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
import { searchCompanies, findCompanyByName, getRequiredFields, DYNAMIC_FIELDS } from '../utils/companyTypes'
import DynamicSelectField from './DynamicSelectField.vue'
import DynamicTextField from './DynamicTextField.vue'
import DynamicNumberField from './DynamicNumberField.vue'

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
  components: {
    DynamicSelectField,
    DynamicTextField,
    DynamicNumberField
  },
  data() {
    return {
      contacts: [],
      companies: [],
      searchTerm: '',
      showAddModal: false,
      showEditModal: false,
      showUploadModal: false,
      selectedFile: null,
      selectedDocFile: null,
      existingDocUrl: null,
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
        cipc_number: '',
        tax_number: '',
        notes: '',
        company_search: '',
        dynamicFields: {}
      },
      editingId: null,
      formErrors: {},
      formSubmitting: false,
      companyInputFocused: false,
      selfEmployedGeneratedName: '',
      showCompanyDropdown: false,
      filteredCompanies: [],
      selectedCompany: null,
      companySearchTimeout: null
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
      const term = (this.searchTerm || '').toLowerCase()
      return this.contacts.filter(contact => 
        (contact.first_name || '').toLowerCase().includes(term) ||
        (contact.last_name || '').toLowerCase().includes(term) ||
        (contact.email || '').toLowerCase().includes(term) ||
        (contact.cipc_number && contact.cipc_number.toLowerCase().includes(term)) ||
        (contact.company_name && contact.company_name.toLowerCase().includes(term)) ||
        (contact.company_name_manual && contact.company_name_manual.toLowerCase().includes(term))
      )
    },
    emailPlaceholder() {
      return this.contactForm.is_self_employed ? 'e.g. jane@consulting.co.za or gmail' : 'e.g. john@acmeholdings.co.za'
    },
    emailHint() {
      return this.contactForm.is_self_employed
        ? 'Independent consultants & freelancers may use professional or personal domain emails.'
        : 'Corporate clients must register with their official business domain email.'
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
    formatDocUrl(url) {
      if (!url) return '#'
      if (url.startsWith('http://') || url.startsWith('https://')) return url
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      const base = isLocal ? 'http://localhost:8000' : 'https://the-finisher-luxury-api.onrender.com'
      return `${base}${url}`
    },
    async loadContacts() {
      try {
        const response = await contactsAPI.getAll()
        this.contacts = Array.isArray(response.data) ? response.data : (response.data.results || [])
      } catch (error) {
        console.error('Error loading contacts:', error)
      }
    },
    async loadCompanies() {
      try {
        const response = await companiesAPI.getAll()
        this.companies = Array.isArray(response.data) ? response.data : (response.data.results || [])
      } catch (error) {
        console.error('Error loading companies:', error)
      }
    },
    openAddContact() {
      this.resetForm()
      this.showAddModal = true
      this.resetCompanySelection()
    },
    onCompanySearchInput() {
      clearTimeout(this.companySearchTimeout)
      this.companySearchTimeout = setTimeout(() => {
        const query = (this.contactForm.company_search || '').trim()
        if (query.length > 0) {
          this.filteredCompanies = searchCompanies(query)
          this.showCompanyDropdown = true
        } else {
          this.filteredCompanies = []
          this.showCompanyDropdown = false
        }
      }, 300)
    },
    onCompanySearchBlur() {
      setTimeout(() => {
        this.showCompanyDropdown = false
      }, 200)
    },
    selectCompany(company) {
      this.selectedCompany = company
      this.contactForm.company_search = company.name
      this.contactForm.company_name_manual = company.name
      this.showCompanyDropdown = false
      this.filteredCompanies = []
      
      this.contactForm.dynamicFields = {}
      if (company.requiredFields && company.requiredFields.length) {
        company.requiredFields.forEach(field => {
          this.contactForm.dynamicFields[field] = ''
        })
      }
    },
    resetCompanySelection() {
      this.selectedCompany = null
      this.filteredCompanies = []
      this.showCompanyDropdown = false
      this.contactForm.company_search = ''
      this.contactForm.dynamicFields = {}
    },
    getDynamicFieldComponent(fieldKey) {
      const fieldDef = DYNAMIC_FIELDS[fieldKey]
      if (!fieldDef) return 'div'
      if (fieldDef.type === 'select') return 'DynamicSelectField'
      if (fieldDef.type === 'number') return 'DynamicNumberField'
      return 'DynamicTextField'
    },
    getDynamicFieldDef(fieldKey) {
      return DYNAMIC_FIELDS[fieldKey] || {}
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
      return combined ? `${combined} Consulting` : 'Self-Employed Professional'
    },
    handleDocFileSelect(event) {
      this.selectedDocFile = event.target.files[0]
    },
    async saveContact() {
      this.formErrors = {}

      const isSelf = Boolean(this.contactForm.is_self_employed)
      let companyManual = (this.contactForm.company_name_manual || '').trim()
      if (isSelf && !companyManual) {
        companyManual = this.computeSelfEmployedGeneratedName()
      }

      let directLine = (this.contactForm.company_direct_line || '').trim()
      if (isSelf) {
        directLine = ''
      }

      const validationErrors = this.performClientValidation({
        first_name: this.contactForm.first_name,
        last_name: this.contactForm.last_name,
        email: this.contactForm.email,
        is_self_employed: isSelf,
        company_direct_line: directLine,
        company_name_manual: companyManual,
        cipc_number: (this.contactForm.cipc_number || '').trim()
      })

      if (Object.keys(validationErrors).length) {
        this.formErrors = validationErrors
        return
      }

      this.formSubmitting = true

      try {
        let requestPayload
        let config = {}

        if (this.selectedDocFile) {
          const formData = new FormData()
          formData.append('first_name', this.contactForm.first_name.trim())
          formData.append('last_name', this.contactForm.last_name.trim())
          formData.append('email', this.contactForm.email.trim())
          formData.append('phone', (this.contactForm.phone || '').trim())
          formData.append('is_self_employed', isSelf ? 'true' : 'false')
          formData.append('company_direct_line', directLine)
          formData.append('company_name_manual', companyManual)
          if (this.contactForm.company) formData.append('company', this.contactForm.company)
          if (this.contactForm.cipc_number) formData.append('cipc_number', this.contactForm.cipc_number.trim())
          if (this.contactForm.tax_number) formData.append('tax_number', this.contactForm.tax_number.trim())
          if (this.contactForm.notes) formData.append('notes', this.contactForm.notes.trim())
          formData.append('document', this.selectedDocFile)
          
          requestPayload = formData
          config = { headers: { 'Content-Type': 'multipart/form-data' } }
        } else {
          requestPayload = {
            first_name: this.contactForm.first_name.trim(),
            last_name: this.contactForm.last_name.trim(),
            email: this.contactForm.email.trim(),
            phone: (this.contactForm.phone || '').trim(),
            is_self_employed: isSelf,
            company_direct_line: directLine,
            company_name_manual: companyManual,
            company: this.contactForm.company || null,
            cipc_number: (this.contactForm.cipc_number || '').trim(),
            tax_number: (this.contactForm.tax_number || '').trim(),
            notes: (this.contactForm.notes || '').trim()
          }
        }

        if (this.showAddModal) {
          await contactsAPI.create(requestPayload, config)
        } else {
          await contactsAPI.update(this.editingId, requestPayload, config)
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
        first_name: contact.first_name || '',
        last_name: contact.last_name || '',
        email: contact.email || '',
        phone: contact.phone || '',
        is_self_employed: Boolean(contact.is_self_employed),
        company_direct_line: contact.company_direct_line || '',
        company_name_manual: contact.company_name_manual || contact.company_name || '',
        company: contact.company || '',
        cipc_number: contact.cipc_number || '',
        tax_number: contact.tax_number || '',
        notes: contact.notes || '',
        company_search: '',
        dynamicFields: {}
      }
      this.existingDocUrl = contact.document_url || null
      this.selectedDocFile = null
      this.editingId = contact.id
      this.showEditModal = true
      this.formErrors = {}
      this.companyInputFocused = false
      this.refreshSelfEmployedGeneratedName(false)
    },
    async deleteContact(id) {
      const ok = await modal.danger('Delete Business Client', 'Are you sure you want to delete this business client record? This action cannot be undone.')
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
        errors.email = 'Email address is required.'
      } else if (!this.isValidEmail(email)) {
        errors.email = 'Enter a valid email address.'
      } else if (!payload.is_self_employed && this.isPersonalEmailDomain(email)) {
        errors.email = 'Corporate clients must use their official company email domain.'
      }

      if (!payload.is_self_employed && !payload.company_direct_line) {
        errors.company_direct_line = 'Corporate clients must include a direct landline.'
      }

      if (!payload.is_self_employed && !payload.company_name_manual) {
        errors.company_name_manual = 'Company legal name is required for corporate clients.'
      }

      if (payload.cipc_number) {
        const cipcClean = payload.cipc_number.trim()
        const cipcPattern = /^\d{4}\/\d{6}\/\d{2}$/
        if (!cipcPattern.test(cipcClean)) {
          errors.cipc_number = 'CIPC format must be YYYY/NNNNNN/NN (e.g. 2024/123456/07).'
        }
      }

      return errors
    },
    extractErrors(error) {
      const fallback = { general: 'Unable to save client record. Please try again.' }
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
        cipc_number: '',
        tax_number: '',
        notes: '',
        company_search: '',
        dynamicFields: {}
      }
      this.selectedDocFile = null
      this.existingDocUrl = null
      this.formErrors = {}
      this.formSubmitting = false
      this.companyInputFocused = false
      this.editingId = null
      this.selfEmployedGeneratedName = ''
      this.resetCompanySelection()
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
.btn-add-business { 
  background: linear-gradient(135deg, #d4af37 0%, #aa820a 100%);
  color: #0b0c10;
  font-weight: 700;
  border: none;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.25);
}
.btn-add-business:hover {
  background: linear-gradient(135deg, #f3cf55 0%, #c49a15 100%);
  transform: translateY(-1px);
}
.toolbar { margin-bottom: 1rem; }
.search-box { position: relative; max-width: 420px; }
.search-box svg { position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: var(--gray-400); pointer-events: none; }
.search-box .form-input { padding-left: 2.25rem; }
.table-card { padding: 0; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch; }
.col-actions { width: 140px; }
.row-actions { display: flex; gap: 0.5rem; }
.health-pill { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; min-width: 32px; text-align: center; }

/* Badges & Chips */
.badge-tag-wrap { display: flex; }
.badge-business { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 4px; }
.badge-warning { background: rgba(212, 175, 55, 0.15); color: #d4af37; border: 1px solid rgba(212, 175, 55, 0.35); font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 4px; }
.cipc-chip { background: rgba(255, 255, 255, 0.05); padding: 0.2rem 0.45rem; border-radius: 4px; font-size: 0.75rem; color: #d4af37; display: inline-block; border: 1px solid rgba(212, 175, 55, 0.2); }
.cipc-label { color: #888; font-size: 0.68rem; margin-right: 2px; }
.doc-attachment-badge { display: inline-flex; align-items: center; gap: 0.25rem; color: #60a5fa; font-size: 0.75rem; text-decoration: none; font-weight: 600; padding: 0.2rem 0.5rem; background: rgba(59, 130, 246, 0.1); border-radius: 4px; border: 1px solid rgba(59, 130, 246, 0.25); }
.doc-attachment-badge:hover { text-decoration: underline; background: rgba(59, 130, 246, 0.2); }
.company-cell-name { font-weight: 600; color: var(--gray-900); }

/* Luxury Modal Architecture */
.luxury-modal {
  max-width: 680px;
  width: 95%;
  background: #111217;
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
  color: #e5e7eb;
}
.modal-scrollable {
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}
.modal-scrollable .modal-body {
  overflow-y: auto;
  padding: 1.5rem;
}
.modal-title-wrap { display: flex; flex-direction: column; gap: 0.25rem; }
.modal-badge-tag { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.1em; color: #d4af37; text-transform: uppercase; }
.modal-header h3 { margin: 0; font-size: 1.35rem; font-weight: 700; color: #fff; }
.modal-sub { margin: 0; font-size: 0.8rem; color: #9ca3af; }

/* Form Sections */
.form-section-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}
.section-card-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.section-card-title h4 { margin: 0; font-size: 0.95rem; font-weight: 700; color: #f3f4f6; }
.section-num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  font-size: 0.75rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Self-Employed Box */
.self-employed-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}
.self-employed-box.active {
  background: rgba(212, 175, 55, 0.08);
  border-color: rgba(212, 175, 55, 0.4);
}
.checkbox-headline { font-weight: 700; color: #fff; font-size: 0.9rem; }
.checkbox-desc { margin: 0.25rem 0 0; font-size: 0.78rem; color: #9ca3af; line-height: 1.35; }
.form-check-row { display: flex; align-items: flex-start; gap: 0.75rem; cursor: pointer; }
.form-check-row input[type="checkbox"] { width: 18px; height: 18px; margin-top: 2px; accent-color: #d4af37; cursor: pointer; }

/* Custom Document Upload */
.custom-file-box {
  border: 2px dashed rgba(212, 175, 55, 0.3);
  border-radius: 8px;
  padding: 1.25rem;
  text-align: center;
  background: rgba(0, 0, 0, 0.2);
  transition: border-color 0.2s;
  cursor: pointer;
}
.custom-file-box:hover {
  border-color: #d4af37;
}
.file-drop-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #9ca3af;
  cursor: pointer;
}
.file-drop-label svg { color: #d4af37; }
.d-none { display: none; }

/* Form inputs styling */
.form-row-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { margin-bottom: 1rem; }
.form-label { display: block; font-size: 0.82rem; font-weight: 600; color: #d1d5db; margin-bottom: 0.35rem; }
.form-input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  background: #181a20;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  color: #fff;
  font-size: 0.875rem;
  box-sizing: border-box;
}
.form-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}
.form-textarea { resize: vertical; min-height: 70px; }
.form-hint { font-size: 0.72rem; color: #9ca3af; margin: 0.25rem 0 0; }
.form-error { font-size: 0.72rem; color: #f87171; margin: 0.25rem 0 0; font-weight: 500; }
.text-gold { color: #d4af37; }
.font-mono { font-family: monospace; }
.font-bold { font-weight: 700; }

/* Dropdown Autocomplete */
.input-dropdown-wrap, .company-search-wrap { position: relative; }
.dropdown-suggestions, .company-dropdown {
  position: absolute; top: 100%; left: 0; right: 0;
  background: #1e2029;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  max-height: 220px;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
  z-index: 50;
  list-style: none;
  padding: 0;
  margin: 0.25rem 0 0;
}
.dropdown-suggestions li, .company-dropdown li {
  padding: 0.65rem 0.85rem;
  font-size: 0.85rem;
  color: #e5e7eb;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.company-dropdown li { display: flex; align-items: center; gap: 0.75rem; }
.company-dropdown li:hover, .dropdown-suggestions li:hover { background: rgba(212, 175, 55, 0.15); color: #fff; }
.company-logo { font-size: 1.25rem; }
.company-info { display: flex; flex-direction: column; }
.company-type { font-size: 0.7rem; color: #9ca3af; }

/* Dynamic enterprise fields */
.dynamic-fields-section {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(212, 175, 55, 0.05);
  border-left: 3px solid #d4af37;
  border-radius: 6px;
}
.section-divider { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 0.5rem; }
.section-divider h4 { margin: 0; font-size: 0.88rem; color: #d4af37; }

/* Sticky footer in modal */
.sticky-footer {
  position: sticky;
  bottom: 0;
  background: #111217;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
}

/* Upload modal styling */
.file-upload-area { margin: 1rem 0; }
.file-upload-area input[type="file"] { display: none; }
.file-label {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.85rem 1rem;
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  color: #9ca3af;
}
.file-label:hover { border-color: #d4af37; color: #fff; }
.upload-example { font-family: monospace; font-size: 0.75rem; color: #9ca3af; background: rgba(0,0,0,0.3); padding: 0.4rem; border-radius: 4px; }

/* Alerts */
.alert { padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem; font-weight: 500; margin-bottom: 1rem; }
.alert-danger { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); color: #fca5a5; }
.alert-success { background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.35); color: #86efac; }

@media (max-width: 768px) {
  .page-wrap { padding: 1rem; }
  .page-header { flex-direction: column; }
  .header-btns { width: 100%; }
  .header-btns .btn { flex: 1; justify-content: center; }
  .form-row-2col { grid-template-columns: 1fr; }
}
</style>
