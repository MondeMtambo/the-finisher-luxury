<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Clients</h1>
        <p class="page-subtitle">Manage company and individual clients</p>
      </div>
      <div class="header-actions">
        <div class="btn-group">
          <button 
            class="btn btn-secondary" 
            :class="{ active: filterType === 'all' }" 
            @click="filterType = 'all'"
          >
            All Clients
          </button>
          <button 
            class="btn btn-secondary" 
            :class="{ active: filterType === 'company' }" 
            @click="filterType = 'company'"
          >
            Companies
          </button>
          <button 
            class="btn btn-secondary" 
            :class="{ active: filterType === 'individual' }" 
            @click="filterType = 'individual'"
          >
            Individuals
          </button>
        </div>
        <div class="add-menu">
          <button class="btn btn-primary" @click="toggleAddMenu" :disabled="!canAddCompany">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Add Client
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
          <div v-if="showAddMenu" class="dropdown-menu">
            <button class="dropdown-item" @click="openAddClient('company')">Add Company</button>
            <button class="dropdown-item" @click="openAddClient('individual')">Add Individual Client</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!canAddCompany" class="info-bar info-bar--amber">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>
      <span>Capture at least one contact before creating a company profile. Add a contact first, then return here.</span>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input class="form-input" v-model="searchTerm" placeholder="Search companies...">
      </div>
    </div>

    <div class="card table-card">
      <table class="data-table" v-if="filteredCompanies.length">
        <thead>
          <tr>
            <th>Type</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Address</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in filteredCompanies" :key="company.id">
            <td>
              <span class="badge" :class="company.client_type === 'individual' ? 'badge-gold' : 'badge-blue'">
                {{ company.client_type === 'individual' ? 'Individual' : 'Company' }}
              </span>
            </td>
            <td><strong>{{ company.name }}</strong></td>
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
        <p>No clients found.</p>
      </div>
    </div>

    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>{{ showAddModal ? (companyForm.client_type === 'individual' ? 'Add Individual Client' : 'Add Company') : 'Edit Client' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveCompany">
            <div v-if="showAddModal" class="form-group">
              <label class="form-label">Client Type</label>
              <div class="type-selector">
                <button 
                  type="button" 
                  class="type-btn" 
                  :class="{ active: companyForm.client_type === 'company' }" 
                  @click="companyForm.client_type = 'company'"
                >
                  <span class="type-icon">🏢</span>
                  <span class="type-name">Company</span>
                </button>
                <button 
                  type="button" 
                  class="type-btn" 
                  :class="{ active: companyForm.client_type === 'individual' }" 
                  @click="companyForm.client_type = 'individual'"
                >
                  <span class="type-icon">👤</span>
                  <span class="type-name">Individual</span>
                </button>
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">{{ companyForm.client_type === 'individual' ? 'Full Name' : 'Company Name' }}</label>
              <input class="form-input" v-model="companyForm.name" :placeholder="companyForm.client_type === 'individual' ? 'John Doe' : 'Company Name'" required>
            </div>
            
            <div class="form-group">
              <label class="form-label">Email</label>
              <input class="form-input" v-model="companyForm.email" type="email" placeholder="Email">
            </div>
            
            <div class="form-group">
              <label class="form-label">Phone</label>
              <input class="form-input" v-model="companyForm.phone" placeholder="Phone">
            </div>
            
            <div v-if="companyForm.client_type === 'company'" class="form-group">
              <label class="form-label">Address</label>
              <textarea class="form-input" v-model="companyForm.address" placeholder="Business Address" rows="3"></textarea>
            </div>
            
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save</button>
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
      showAddMenu: false,
      filterType: 'all',
      companyForm: {
        name: '',
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
      return this.companies.filter(company => {
        const matchesSearch = company.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          (company.email && company.email.toLowerCase().includes(this.searchTerm.toLowerCase()))
        const matchesType = this.filterType === 'all' || company.client_type === this.filterType
        return matchesSearch && matchesType
      })
    },
    canAddCompany() {
      return this.contactCount > 0
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
    toggleAddMenu() {
      this.showAddMenu = !this.showAddMenu
    },
    async openAddClient(clientType) {
      await this.refreshPrerequisites()
      if (!this.canAddCompany) {
        await modal.warning('Contact Required', 'Capture at least one contact before creating a client profile. Add a contact first, then come back here.')
        this.$router.push('/contacts')
        return
      }
      this.companyForm.client_type = clientType
      this.showAddModal = true
      this.showAddMenu = false
    },
    async saveCompany() {
      try {
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
      this.companyForm = { ...company }
      this.editingId = company.id
      this.showEditModal = true
    },
    async deleteCompany(id) {
      const ok = await modal.danger('Delete Company', 'Are you sure you want to delete this company? This action cannot be undone.')
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
      this.showAddMenu = false
      this.companyForm = {
        name: '',
        email: '',
        phone: '',
        address: '',
        client_type: 'company'
      }
      this.editingId = null
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 1.5rem 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; gap: 1rem; }
.page-header h1 { font-size: 1.75rem; font-weight: 700; color: var(--gray-900); margin: 0; }
.page-subtitle { color: var(--gray-500); font-size: 0.9rem; margin: 0.25rem 0 0; }
.page-header .btn { display: inline-flex; align-items: center; gap: 0.5rem; }
.info-bar { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; border-radius: var(--radius-md); font-size: 0.875rem; font-weight: 500; margin-bottom: 1rem; }
.info-bar svg { flex-shrink: 0; }
.info-bar span { flex: 1; }
.info-bar--amber { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
.toolbar { margin-bottom: 1rem; }
.search-box { position: relative; max-width: 360px; }
.search-box svg { position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: var(--gray-400); pointer-events: none; }
.search-box .form-input { padding-left: 2.25rem; }
.table-card { padding: 0; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch; }
.col-actions { width: 160px; }
.cell-truncate { max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.row-actions { display: flex; gap: 0.5rem; }

/* Header actions layout */
.header-actions { display: flex; gap: 1rem; align-items: center; }
.btn-group { display: flex; gap: 0.5rem; }
.btn-group .btn { padding: 0.5rem 1rem; font-size: 0.875rem; }
.btn-group .btn.active { background: var(--primary); color: white; }

/* Add menu dropdown */
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
}
.dropdown-item:hover { background: var(--gray-100); }
.dropdown-item:first-child { border-radius: var(--radius-md) var(--radius-md) 0 0; }
.dropdown-item:last-child { border-radius: 0 0 var(--radius-md) var(--radius-md); }

/* Type selector for modal */
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
.badge { 
  display: inline-block; padding: 0.25rem 0.75rem; 
  border-radius: var(--radius-full); font-size: 0.75rem; 
  font-weight: 700; white-space: nowrap;
}
.badge-gold { background: #fef3c7; color: #92400e; }
.badge-blue { background: #dbeafe; color: #1e3a8a; }

@media (max-width: 768px) {
  .page-wrap { padding: 1rem; }
  .page-header { flex-direction: column; }
  .header-actions { flex-direction: column; width: 100%; }
  .btn-group { width: 100%; flex-wrap: wrap; }
  .table-card { overflow-x: auto; }
}
</style>
