<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Deal Pipeline</h1>
        <p class="page-subtitle">Track and manage your sales pipeline</p>
      </div>
      <button class="btn btn-primary" @click="showAddModal = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Create Deal
      </button>
    </div>

    <div class="pipeline-board">
      <div v-for="stage in stages" :key="stage.key" class="pipeline-col">
        <div class="col-header">
          <span class="col-title">{{ stage.label }}</span>
          <span class="col-count badge badge-gray">{{ getDealsInStage(stage.key).length }}</span>
        </div>
        <div class="col-body">
          <div v-for="deal in getDealsInStage(stage.key)" :key="deal.id" class="deal-card card">
            <h4 class="deal-title">{{ deal.title }}</h4>
            <p class="deal-meta-line" v-if="deal.contact_name">{{ deal.contact_name }}</p>
            <p class="deal-meta-line" v-if="deal.company_name">{{ deal.company_name }}</p>
            <p class="deal-value">R{{ formatNumber(deal.value) }}</p>
            <div class="time-tracker">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span class="time-display">{{ deal.total_hours_display || 0 }}h</span>
              <button v-if="!deal.timer_running" @click.stop="startTimer(deal.id)" class="timer-btn timer-start" title="Start Timer">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              </button>
              <button v-else @click.stop="stopTimer(deal.id)" class="timer-btn timer-stop" :disabled="!canStopTimer" :title="canStopTimer ? 'Stop Timer' : 'Only admins can stop timers'">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
              </button>
            </div>
            <div class="deal-actions">
              <button class="btn btn-sm btn-secondary" @click="editDeal(deal)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteDeal(deal.id)" :disabled="!canDeleteDeals">Delete</button>
            </div>
          </div>
          <div v-if="getDealsInStage(stage.key).length === 0" class="col-empty">No deals</div>
        </div>
      </div>
    </div>

    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>{{ showAddModal ? 'Create New Deal' : 'Edit Deal' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveDeal">
            <div class="form-group">
              <label class="form-label">Deal Title</label>
              <input class="form-input" v-model="dealForm.title" placeholder="Deal Title" required>
            </div>
            <div class="form-group">
              <label class="form-label">Company</label>
              <select class="form-input" v-model="dealForm.company" required @change="onCompanyChange">
                <option value="">Select Company</option>
                <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Contact</label>
              <select class="form-input" v-model="dealForm.contact" :disabled="!dealForm.company" required>
                <option value="">Select Contact</option>
                <option v-for="contact in contactsByCompany" :key="contact.id" :value="contact.id">{{ contact.first_name }} {{ contact.last_name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Deal Value (R)</label>
              <input class="form-input" v-model="dealForm.value" type="number" step="0.01" placeholder="0.00" required>
            </div>
            <div class="form-group">
              <label class="form-label">Stage</label>
              <select class="form-input" v-model="dealForm.stage">
                <option v-for="stage in stages" :key="stage.key" :value="stage.key">{{ stage.label }}</option>
              </select>
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
import { dealsAPI, contactsAPI, companiesAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'Deals',
  data() {
    return {
      deals: [],
      contacts: [],
      companies: [],
      showAddModal: false,
      showEditModal: false,
      userPermissions: null,
      dealForm: {
        title: '',
        company: '',
        contact: '',
        value: '',
        stage: 'lead'
      },
      editingId: null,
      stages: [
        { key: 'lead', label: 'Lead' },
        { key: 'qualified', label: 'Qualified' },
        { key: 'proposal', label: 'Proposal' },
        { key: 'negotiation', label: 'Negotiation' },
        { key: 'closed_won', label: 'Closed Won' },
        { key: 'closed_lost', label: 'Closed Lost' }
      ]
    }
  },
  computed: {
    contactsByCompany() {
      if (!this.dealForm.company) {
        return this.contacts.filter(contact => contact.company)
      }
      const companyId = Number(this.dealForm.company)
      return this.contacts.filter(contact => Number(contact.company) === companyId)
    },
    canStopTimer() {
      return this.userPermissions?.can_stop_deal_timers || false
    },
    canDeleteDeals() {
      return this.userPermissions?.can_delete_deals || false
    }
  },
  async mounted() {
    await this.loadUserPermissions()
    await this.loadDeals()
    await this.loadContacts()
    await this.loadCompanies()
  },
  methods: {
    async loadUserPermissions() {
      try {
        const user = authService.getCurrentUser()
        if (user && user.permissions) {
          this.userPermissions = user.permissions
        }
      } catch (error) {
        console.error('Error loading user permissions:', error)
      }
    },
    async loadDeals() {
      try {
        const response = await dealsAPI.getAll()
        this.deals = response.data
      } catch (error) {
        console.error('Error loading deals:', error)
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
    async loadContacts() {
      try {
        const response = await contactsAPI.getAll()
        this.contacts = response.data
      } catch (error) {
        console.error('Error loading contacts:', error)
      }
    },
    getDealsInStage(stage) {
      return this.deals.filter(deal => deal.stage === stage)
    },
    async saveDeal() {
      try {
        const payload = {
          ...this.dealForm,
          company: this.dealForm.company ? Number(this.dealForm.company) : null,
          contact: this.dealForm.contact ? Number(this.dealForm.contact) : null,
          value: this.dealForm.value
        }
        if (this.showAddModal) {
          await dealsAPI.create(payload)
        } else {
          await dealsAPI.update(this.editingId, payload)
        }
        await this.loadDeals()
        this.closeModal()
      } catch (error) {
        console.error('Error saving deal:', error)
      }
    },
    editDeal(deal) {
      this.dealForm = {
        title: deal.title,
        company: deal.company || '',
        contact: deal.contact || '',
        value: deal.value,
        stage: deal.stage
      }
      this.onCompanyChange()
      this.editingId = deal.id
      this.showEditModal = true
    },
    async deleteDeal(id) {
      if (!this.canDeleteDeals) {
        modal.alert('Access Denied', 'Only administrators and managers can delete deals.\n\nContact your system administrator for assistance.', 'lock')
        return
      }
      
      const ok = await modal.danger('Delete Deal', 'Are you sure you want to delete this deal? This action cannot be undone.')
      if (ok) {
        try {
          await dealsAPI.delete(id)
          await this.loadDeals()
        } catch (error) {
          console.error('Error deleting deal:', error)
          toast.error('Delete Failed', 'Failed to delete deal: ' + (error.response?.data?.error || error.message))
        }
      }
    },
    closeModal() {
      this.showAddModal = false
      this.showEditModal = false
      this.dealForm = {
        title: '',
        company: '',
        contact: '',
        value: '',
        stage: 'lead'
      }
      this.editingId = null
    },
    onCompanyChange() {
      if (!this.dealForm.company) {
        this.dealForm.contact = ''
        return
      }
      const contactExists = this.contactsByCompany.some(contact => Number(contact.id) === Number(this.dealForm.contact))
      if (!contactExists) {
        this.dealForm.contact = ''
      }
    },
    formatNumber(value) {
      return new Intl.NumberFormat('en-ZA').format(value)
    },
    async startTimer(dealId) {
      try {
        await dealsAPI.startTimer(dealId)
        await this.loadDeals()
      } catch (error) {
        console.error('Error starting timer:', error)
        toast.error('Timer Error', 'Failed to start timer: ' + (error.response?.data?.error || error.message))
      }
    },
    async stopTimer(dealId) {
      if (!this.canStopTimer) {
        modal.alert('Access Denied', 'Only administrators and managers can stop deal timers.\n\nThis ensures consistent time tracking across your team.', 'lock')
        return
      }
      
      try {
        await dealsAPI.stopTimer(dealId)
        await this.loadDeals()
      } catch (error) {
        console.error('Error stopping timer:', error)
        toast.error('Timer Error', 'Failed to stop timer: ' + (error.response?.data?.error || error.message))
      }
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
/* Pipeline Board */
.pipeline-board { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.75rem; overflow-x: auto; min-height: 500px; }
.pipeline-col { background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-md); display: flex; flex-direction: column; min-width: 200px; }
.col-header { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; border-bottom: 1px solid var(--gray-200); background: #fff; border-radius: var(--radius-md) var(--radius-md) 0 0; }
.col-title { font-size: 0.8rem; font-weight: 700; color: var(--gray-700); text-transform: uppercase; letter-spacing: 0.3px; }
.col-body { padding: 0.5rem; flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.col-empty { text-align: center; color: var(--gray-400); font-size: 0.8rem; padding: 2rem 0.5rem; }
/* Deal Card */
.deal-card { padding: 0.75rem; border-left: 3px solid var(--primary-400); }
.deal-title { font-size: 0.875rem; font-weight: 600; color: var(--gray-900); margin: 0 0 0.35rem; }
.deal-meta-line { font-size: 0.8rem; color: var(--gray-500); margin: 0.15rem 0; }
.deal-value { font-size: 0.9rem; font-weight: 700; color: var(--primary-700); margin: 0.35rem 0; }
/* Timer */
.time-tracker { display: flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.5rem; background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-sm); margin-bottom: 0.5rem; }
.time-tracker svg { color: var(--gray-400); flex-shrink: 0; }
.time-display { font-weight: 700; font-size: 0.85rem; color: var(--gray-700); font-family: 'Courier New', monospace; }
.timer-btn { margin-left: auto; border: none; background: none; cursor: pointer; padding: 0.2rem; display: flex; border-radius: 4px; transition: background 0.15s; }
.timer-btn:hover { background: var(--gray-200); }
.timer-start { color: #16a34a; }
.timer-stop { color: #dc2626; }
.timer-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.timer-stop:not(:disabled) { animation: pulse-stop 1.5s ease-in-out infinite; }
@keyframes pulse-stop { 0%,100%{opacity:1}50%{opacity:0.5} }
.deal-actions { display: flex; gap: 0.35rem; }
@media (max-width: 1024px) {
  .pipeline-board { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .page-wrap { padding: 1rem; }
  .page-header { flex-direction: column; }
  .pipeline-board { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) {
  .pipeline-board { grid-template-columns: 1fr; }
}
</style>
