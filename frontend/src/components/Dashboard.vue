<template>
  <div class="dashboard">

    <div v-if="!isEmployeeOnly" class="page-header">
      <div class="header-row">
        <div>
          <h1>Dashboard</h1>
          <p class="page-subtitle">Welcome back. Here's your CRM overview.</p>
        </div>
        <div class="tier-chip" :class="'tier-' + (isAdminUser ? 'ultimate' : userTier)">
          <span class="tier-label">{{ isAdminUser ? 'ULTIMATE' : tierDisplayName }}</span>
          <span class="tier-price">{{ isAdminUser ? 'Full System Access' : tierSubtitle }}</span>
        </div>
      </div>

      <div v-if="isAdminUser" class="info-bar info-bar--blue">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.399l-.244.012.024-.39 1.958-.36h.17l-.818 3.918zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>
        <span>ULTIMATE: Unlimited Access &middot; All Features &middot; Full Admin Control &middot; System Owner</span>
      </div>

      <div v-if="!isAdminUser && isLuxuryTier" class="info-bar info-bar--blue">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.399l-.244.012.024-.39 1.958-.36h.17l-.818 3.918zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>
        <span>LUXURY EDITION: 10-User Access &middot; API Access &middot; Integrations &middot; Priority Support</span>
      </div>

      <div v-if="!isAdminUser && isFreeTier" class="info-bar info-bar--amber">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>
        <span>You are on the FREE tier. Upgrade to LUXURY (R249/month) to unlock all features.</span>
        <button class="btn btn-sm btn-primary" @click="$router.push('/upgrade/luxury')">Upgrade</button>
      </div>
    </div>

    <div class="grid-stack top-stats-grid" ref="topStatsGrid">
      <div 
        v-for="element in statCards" 
        :key="element.key"
        class="grid-stack-item"
        :gs-id="element.key"
        :gs-x="element.x || 0"
        :gs-y="element.y || 0"
        :gs-w="element.w || 1"
        :gs-h="element.h || 1"
      >
        <div class="grid-stack-item-content stat-card card" @click="onStatCardClick(element.key)" role="button" tabindex="0">
          <span class="drag-handle" title="Drag to reorder" @click.stop>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><circle cx="4" cy="2" r="1.5"/><circle cx="10" cy="2" r="1.5"/><circle cx="4" cy="7" r="1.5"/><circle cx="10" cy="7" r="1.5"/><circle cx="4" cy="12" r="1.5"/><circle cx="10" cy="12" r="1.5"/></svg>
          </span>
          <div class="stat-icon-wrap" :class="element.key">
            <svg v-if="element.key==='contacts'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <svg v-else-if="element.key==='companies'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v3"/></svg>
            <svg v-else-if="element.key==='deals'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            <svg v-else-if="element.key==='revenue'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <svg v-else-if="element.key==='assigned'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
            <svg v-else-if="element.key==='openTickets'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <svg v-else-if="element.key==='inProgress'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <svg v-else-if="element.key==='completedTickets'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
          </div>
          <div class="stat-body">
            <p class="stat-label">{{ element.label }}</p>
            <h3 class="stat-value">{{ element.value }}</h3>
          </div>
        </div>
      </div>
    </div>

    <section v-if="isEmployeeOnly" class="section-card card">
      <div class="section-head">
        <h2>My Assigned Tickets</h2>
        <span class="badge badge-blue">{{ myTopFiveTickets.length }} recent</span>
      </div>
      <div v-if="myTopFiveTickets.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
        <p>No tickets assigned yet.</p>
      </div>
      <div v-else class="tickets-table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Due</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ticket in myTopFiveTickets" :key="ticket.id">
              <td>
                <strong>{{ ticket.title }}</strong>
                <p v-if="ticket.description" class="ticket-desc">{{ ticket.description }}</p>
              </td>
              <td><span class="badge" :class="'badge-' + priorityBadgeColor(ticket.priority)">{{ ticket.priority }}</span></td>
              <td><span class="badge" :class="'badge-' + statusBadgeColor(ticket.status)">{{ formatStatus(ticket.status) }}</span></td>
              <td class="text-muted">{{ ticket.due_at ? formatDueDate(ticket.due_at) : '---' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="!isEmployeeOnly" class="analytics-section">
      <div class="analytics-grid">

        <div class="chart-card card">
          <h3 class="card-title">Deal Pipeline</h3>
          <div class="chart-wrap">
            <canvas ref="pipelineChart"></canvas>
          </div>
          <div class="chart-footer">
            <span>Total: R{{ pipelineSum }}</span>
            <span>Active: {{ activeDeals.length }}</span>
          </div>
        </div>

        <div v-if="!isAdminUser" class="locked-card card">
          <div class="locked-body">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--gray-400)" stroke-width="1.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <h4>Advanced Analytics</h4>
            <p>Unlock revenue trends, activity heatmaps, contact health scoring, custom reports and forecasting tools.</p>
            <button class="btn btn-primary" @click="$router.push('/upgrade/luxury')">Upgrade Plan</button>
          </div>
        </div>
      </div>
    </section>

    <div v-if="!isEmployeeOnly" class="quick-actions-bar">
      <h3>Quick Actions</h3>
      <div class="qa-buttons">
        <button class="btn btn-primary" @click="openAddContact">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Add Contact
        </button>
        <button class="btn btn-secondary" @click="viewCompanies">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v3"/></svg>
          View Companies
        </button>
        <button class="btn btn-secondary" @click="openCreateDeal">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          Create Deal
        </button>
      </div>
    </div>


    <div v-if="showContactModal" class="modal-overlay" @click="closeContactModal">
      <div class="modal-panel" @click.stop tabindex="0" ref="contactModal" @keydown="onModalKeydown">
        <div class="modal-header">
          <h3>Add New Contact</h3>
          <button class="modal-close" @click="closeContactModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveContact" novalidate>
            <div v-if="contactFormErrors.general" class="alert alert-danger">{{ contactFormErrors.general }}</div>

            <div class="form-row-2col">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input class="form-input" v-model="contactForm.first_name" placeholder="First Name" required>
                <p v-if="contactFormErrors.first_name" class="form-error">{{ contactFormErrors.first_name }}</p>
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input class="form-input" v-model="contactForm.last_name" placeholder="Last Name" required>
                <p v-if="contactFormErrors.last_name" class="form-error">{{ contactFormErrors.last_name }}</p>
              </div>
            </div>

            <div class="form-group">
              <label class="form-check">
                <input type="checkbox" v-model="contactForm.is_self_employed">
                <span>Self-employed / Independent</span>
              </label>
            </div>

            <div class="form-group">
              <label class="form-label">Email</label>
              <input class="form-input" v-model="contactForm.email" type="email" :placeholder="contactEmailPlaceholder" required>
              <p class="form-hint">{{ contactEmailHint }}</p>
              <p v-if="contactFormErrors.email" class="form-error">{{ contactFormErrors.email }}</p>
            </div>

            <div class="form-group">
              <label class="form-label">{{ contactForm.is_self_employed ? 'Business Trading Name' : 'Company Name' }}</label>
              <div class="input-dropdown-wrap">
                <input class="form-input" v-model="contactForm.company_name_manual"
                  :placeholder="contactForm.is_self_employed ? 'Business trading name' : 'Type or select company'"
                  :required="!contactForm.is_self_employed"
                  @focus="onQuickCompanyInputFocus"
                  @blur="onQuickCompanyInputBlur"
                  @input="onQuickCompanyInput">
                <ul v-if="showQuickCompanySuggestions" class="dropdown-suggestions">
                  <li v-for="name in quickCompanyNameSuggestions" :key="name" @mousedown.prevent="selectQuickCompanySuggestion(name)">{{ name }}</li>
                </ul>
              </div>
              <p v-if="!contactForm.is_self_employed" class="form-hint">Start typing for SA company suggestions.</p>
              <p v-if="contactFormErrors.company_name_manual" class="form-error">{{ contactFormErrors.company_name_manual }}</p>
            </div>

            <div class="form-group">
              <label class="form-label">Phone</label>
              <input class="form-input" v-model="contactForm.phone" :placeholder="quickCompanyNumberPlaceholder">
              <p v-if="contactFormErrors.phone" class="form-error">{{ contactFormErrors.phone }}</p>
            </div>

            <div v-if="!contactForm.is_self_employed" class="form-group">
              <label class="form-label">Direct Company Line</label>
              <input class="form-input" v-model="contactForm.company_direct_line" placeholder="+27 11 234 5678" required>
              <p v-if="contactFormErrors.company_direct_line" class="form-error">{{ contactFormErrors.company_direct_line }}</p>
            </div>

            <div v-if="companies.length" class="form-group">
              <label class="form-label">Link to Company (optional)</label>
              <select class="form-input" v-model="contactForm.company" :disabled="contactForm.is_self_employed">
                <option value="">Do not link yet</option>
                <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
              </select>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeContactModal" :disabled="contactFormSubmitting">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="contactFormSubmitting">{{ contactFormSubmitting ? 'Saving...' : 'Save Contact' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showCompanyModal" class="modal-overlay" @click="closeCompanyModal">
      <div class="modal-panel" @click.stop tabindex="0" ref="companyModal" @keydown="onModalKeydown">
        <div class="modal-header">
          <h3>Add New Company</h3>
          <button class="modal-close" @click="closeCompanyModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveCompany">
            <div class="form-group">
              <label class="form-label">Company Name</label>
              <input class="form-input" v-model="companyForm.name" placeholder="Company Name" required>
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input class="form-input" v-model="companyForm.email" type="email" placeholder="Email">
            </div>
            <div class="form-group">
              <label class="form-label">Phone</label>
              <input class="form-input" v-model="companyForm.phone" placeholder="Phone">
            </div>
            <div class="form-group">
              <label class="form-label">Address</label>
              <textarea class="form-input" v-model="companyForm.address" placeholder="Address" rows="3"></textarea>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeCompanyModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save Company</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showDealModal" class="modal-overlay" @click="closeDealModal">
      <div class="modal-panel" @click.stop tabindex="0" ref="dealModal" @keydown="onModalKeydown">
        <div class="modal-header">
          <h3>Create New Deal</h3>
          <button class="modal-close" @click="closeDealModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveDeal">
            <div class="form-group">
              <label class="form-label">Deal Title</label>
              <input class="form-input" v-model="dealForm.title" placeholder="Deal Title" required>
            </div>
            <div class="form-group">
              <label class="form-label">Company</label>
              <select class="form-input" v-model="dealForm.company" required @change="onDealCompanyChange">
                <option value="">Select Company</option>
                <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Contact</label>
              <select class="form-input" v-model="dealForm.contact" :disabled="!dealForm.company" required>
                <option value="">Select Contact</option>
                <option v-for="contact in contactsForDeal" :key="contact.id" :value="contact.id">{{ contact.first_name }} {{ contact.last_name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Deal Value (R)</label>
              <input class="form-input" v-model="dealForm.value" type="number" step="0.01" placeholder="0.00" required>
            </div>
            <div class="form-group">
              <label class="form-label">Stage</label>
              <select class="form-input" v-model="dealForm.stage">
                <option value="lead">Lead</option>
                <option value="qualified">Qualified</option>
                <option value="proposal">Proposal</option>
                <option value="negotiation">Negotiation</option>
                <option value="closed_won">Closed Won</option>
                <option value="closed_lost">Closed Lost</option>
              </select>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeDealModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save Deal</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showExampleModal" class="modal-overlay" @click="closeExample">
      <div class="modal-panel modal-lg" @click.stop tabindex="0" ref="exampleModal" @keydown="onModalKeydown">
        <div class="modal-header">
          <h3>Overview &mdash; DIBATA 011</h3>
          <button class="modal-close" @click="closeExample">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="exampleType === 'contacts'">
            <p><strong>Contacts ({{ contacts.length }})</strong></p>
            <ul class="preview-list">
              <li v-for="c in contacts" :key="c.id">
                {{ c.first_name }} {{ c.last_name }}
                <span v-if="c.email"> &mdash; {{ c.email }}</span>
                <span> &mdash; {{ getContactCompany(c) }}</span>
              </li>
            </ul>
          </div>
          <div v-else-if="exampleType === 'companies'">
            <p><strong>Companies ({{ companies.length }})</strong></p>
            <ul class="preview-list">
              <li v-for="co in companies" :key="co.id">
                {{ co.name }}<span v-if="co.email"> &mdash; {{ co.email }}</span>
              </li>
            </ul>
          </div>
          <div v-else-if="exampleType === 'deals'">
            <p><strong>Active Deals ({{ topFiveActiveDeals.length }} of {{ activeDeals.length }})</strong></p>
            <div class="deals-list">
              <div v-for="d in topFiveActiveDeals" :key="d.id" class="deal-row"
                :class="{ selected: selectedDeal && selectedDeal.id === d.id }" @click="selectDeal(d)">
                <span class="deal-name">{{ d.title }}</span>
                <span class="badge badge-blue">{{ d.stage.replace('_',' ') }}</span>
                <span v-if="d.value" class="deal-val">R{{ new Intl.NumberFormat('en-ZA').format(d.value) }}</span>
              </div>
            </div>
            <div v-if="selectedDeal" class="deal-detail card">
              <h4>Deal Details</h4>
              <p><strong>Title:</strong> {{ selectedDeal.title }}</p>
              <p><strong>Contact:</strong> {{ selectedDeal.contact_name || 'N/A' }}</p>
              <p><strong>Stage:</strong> {{ selectedDeal.stage }}</p>
              <p v-if="selectedDeal.value"><strong>Value:</strong> R{{ new Intl.NumberFormat('en-ZA').format(selectedDeal.value) }}</p>
              <div style="margin-top:0.75rem;">
                <button class="btn btn-danger btn-sm" @click.stop="cancelDeal(selectedDeal)">Cancel Deal</button>
              </div>
            </div>
          </div>
          <div v-else>
            <p><strong>Pipeline Value (active deals):</strong> R{{ pipelineSum }}</p>
            <small class="text-muted">Calculated from current deals list.</small>
          </div>
        </div>
        <div class="modal-footer">
          <a href="https://dibata011.co.za" target="_blank" rel="noopener" class="btn btn-secondary">Visit dibata011.co.za</a>
          <button type="button" class="btn btn-primary" @click="closeExample">Close</button>
        </div>
      </div>
    </div>

    <section v-if="isEmployeeOnly" class="emp-perf">
      <EmployeePerformance />
    </section>
  </div>
</template>

<script>
import { contactsAPI, companiesAPI, dealsAPI, ticketsAPI } from '../api'
import { Chart, registerables } from 'chart.js'
import saCompanies from '../utils/saCompanies'
import EmployeePerformance from './EmployeePerformance.vue'
import toast from '../utils/toast'
import modal from '../utils/modal'


Chart.register(...registerables)

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
  name: 'Dashboard',
  components: {
    EmployeePerformance
  },
  data() {
    return {
      grid: null,
      statCards: [],
      charts: {},
      
      totalContacts: 2,
      totalCompanies: 2,
      totalDeals: 2,
      totalRevenue: '75,000',
      showExampleModal: false,
      exampleType: null,
      selectedDeal: null,
      
      tickets: [],
      showContactModal: false,
      showCompanyModal: false,
      showDealModal: false,
      contactForm: {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        is_self_employed: false,
        company_direct_line: '',
        company_name_manual: '',
        company: ''
      },
      contactFormErrors: {},
      contactFormSubmitting: false,
      contactCompanyInputFocused: false,
      contactSelfEmployedGeneratedName: '',
      companyForm: {
        name: '',
        email: '',
        phone: '',
        address: ''
      },
      dealForm: {
        title: '',
        company: '',
        contact: '',
        value: '',
        stage: 'lead'
      },
      companies: [],
      contacts: [],
      deals: []
    }
  },
  computed: {
    isAdminUser() {
      const raw = localStorage.getItem('user')
      const user = raw ? JSON.parse(raw) : null
      return !!(user && (user.is_superuser || (user.username||'').toLowerCase()==='adminluxury'))
    },
    isEmployeeOnly() {
      const raw = localStorage.getItem('user')
      const user = raw ? JSON.parse(raw) : null
      const isAdmin = !!(user && (user.is_superuser || (user.username||'').toLowerCase()==='adminluxury'))
      const isClientAdmin = !!(user && !isAdmin && (
        (user.permissions && user.permissions.is_admin) ||
        (user.role && (user.role.value === 'admin' || user.role === 'admin')) ||
        (user.profile && user.profile.role === 'admin')
      ))
      return !(isAdmin || isClientAdmin)
    },
    currentUser() {
      const raw = localStorage.getItem('user')
      return raw ? JSON.parse(raw) : {}
    },
    myUserId() {
      return Number(this.currentUser?.id || 0)
    },
    userTier() {
      
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.tier || 'luxury' 
    },
    isSportTier() {
      return this.userTier === 'sport'
    },
    isFreeTier() {
      return this.userTier === 'free'
    },
    isLuxuryTier() {
      return this.userTier === 'luxury'
    },
    isPremiumTier() {
      return this.userTier === 'premium'
    },
    tierIcon() {
      const icons = {
        free: '🎯',
        sport: '🏆',
        luxury: '🥈',
        premium: '🥇'
      }
      return icons[this.userTier] || '🏆'
    },
    tierDisplayName() {
      const names = {
        free: 'CLASSIC',
        sport: 'SPORT',
        luxury: 'LUXURY',
        premium: 'PREMIUM'
      }
      return names[this.userTier] || 'LUXURY'
    },
    tierSubtitle() {
      const subtitles = {
        free: 'Free Forever',
        sport: 'R99/month',
        luxury: 'R249/month',
        premium: 'R499/month'
      }
      return subtitles[this.userTier] || 'R99/month'
    },
    tierFeatureAccess() {
      const features = {
        free: {
          maxUsers: 1,
          companyAutoCreate: false,
          advancedReporting: false,
          apiAccess: false,
          customIntegrations: false
        },
        sport: {
          maxUsers: 2,
          companyAutoCreate: true,
          advancedReporting: true,
          apiAccess: false,
          customIntegrations: false
        },
        luxury: {
          maxUsers: 10,
          companyAutoCreate: true,
          advancedReporting: true,
          apiAccess: true,
          customIntegrations: true
        },
        premium: {
          maxUsers: 999,
          companyAutoCreate: true,
          advancedReporting: true,
          apiAccess: true,
          customIntegrations: true,
          whiteLabel: true,
          dedicatedSupport: true
        }
      }
      return features[this.userTier] || features.luxury
    },
    pipelineSum() {
      try {
        return new Intl.NumberFormat('en-ZA').format(
          (this.deals || []).reduce((acc, d) => acc + Number(d.value || 0), 0)
        )
      } catch (e) {
        return (this.deals || []).reduce((acc, d) => acc + Number(d.value || 0), 0)
      }
    },
    activeDeals() {
      return (this.deals || []).filter(d => d.stage !== 'closed_won' && d.stage !== 'closed_lost')
    },
    topFiveActiveDeals() {
      const list = [...this.activeDeals]
      list.sort((a, b) => {
        const ax = a.updated_at || a.created_at || ''
        const bx = b.updated_at || b.created_at || ''
        return String(bx).localeCompare(String(ax))
      })
      return list.slice(0, 5)
    },
    contactsForDeal() {
      if (!this.dealForm.company) {
        return this.contacts.filter(contact => contact.company)
      }
      const companyId = Number(this.dealForm.company)
      return this.contacts.filter(contact => Number(contact.company) === companyId)
    },
    canQuickAddCompany() {
      return this.contacts.length > 0
    },
    averageDealValue() {
      if (!this.deals || this.deals.length === 0) return '0'
      const total = this.deals.reduce((acc, d) => acc + Number(d.value || 0), 0)
      return new Intl.NumberFormat('en-ZA').format(Math.round(total / this.deals.length))
    },
    winRate() {
      if (!this.deals || this.deals.length === 0) return 0
      const won = this.deals.filter(d => d.stage === 'closed_won').length
      return Math.round((won / this.deals.length) * 100)
    },
    weeklyActivities() {
      
      return this.contacts.length + this.companies.length + this.deals.length
    },
    mostActiveDay() {
      return 'Monday'
    },
    healthyContacts() {
      return this.contacts.filter(c => c.health_score >= 70).length
    },
    atRiskContacts() {
      return this.contacts.filter(c => c.health_score < 40).length
    },
    contactEmailPlaceholder() {
      return this.contactForm.is_self_employed ? 'Business email address' : 'Company email address'
    },
    contactEmailHint() {
      return this.contactForm.is_self_employed
        ? 'Use the email address you operate your business with.'
        : 'Use a professional/company email address for this contact.'
    },
    quickCompanyNumberPlaceholder() {
      return 'Company number (optional)'
    },
    quickCompanyNameSuggestions() {
      const query = (this.contactForm.company_name_manual || '').trim().toLowerCase()
      if (!query) {
        return saCompanies.slice(0, 8)
      }
      return saCompanies.filter(name => name.toLowerCase().includes(query)).slice(0, 8)
    },
    showQuickCompanySuggestions() {
      return (
        !this.contactForm.is_self_employed &&
        this.contactCompanyInputFocused &&
        this.quickCompanyNameSuggestions.length > 0
      )
    },
    
    myAssignedTickets() {
      if (!Array.isArray(this.tickets)) return []
      if (!this.myUserId) return []
      return this.tickets.filter(t => Number(t.assigned_to) === this.myUserId)
    },
    ticketStatusCounts() {
      const counts = { open: 0, in_progress: 0, completed: 0, failed: 0 }
      for (const t of this.myAssignedTickets) {
        const s = (t.status || '').toLowerCase()
        if (counts.hasOwnProperty(s)) counts[s]++
      }
      return counts
    },
    
    myTopFiveTickets() {
      const sorted = [...this.myAssignedTickets].sort((a, b) => {
        
        const aDate = a.created_at || ''
        const bDate = b.created_at || ''
        return String(bDate).localeCompare(String(aDate))
      })
      return sorted.slice(0, 5)
    }
  },
  watch: {
    'contactForm.is_self_employed'(isSelf) {
      if (isSelf) {
        this.contactForm.company = ''
        this.contactForm.company_direct_line = ''
        this.refreshQuickSelfEmployedGeneratedName(true)
      } else {
        const manual = (this.contactForm.company_name_manual || '').trim()
        const generated = (this.contactSelfEmployedGeneratedName || '').trim()
        if (manual && generated && manual === generated) {
          this.contactForm.company_name_manual = ''
        }
      }
    },
    'contactForm.first_name'() {
      this.refreshQuickSelfEmployedGeneratedName()
    },
    'contactForm.last_name'() {
      this.refreshQuickSelfEmployedGeneratedName()
    }
  },
  async mounted() {
    
    try {
      await Promise.allSettled([
        this.loadCompanies(),
        this.loadContacts(),
        this.loadDeals(),
        this.loadTickets()
      ])
      this.initializeStatCards()
      await this.$nextTick()
      this.initGrid()
      this.initializeCharts()
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    }
    
    this.refreshTimer = setInterval(async () => {
      try {
        await Promise.all([
          this.loadCompanies(),
          this.loadContacts(),
          this.loadDeals(),
          this.loadTickets()
        ])
        this.updateStatCards()
        this.updateCharts()
      } catch (e) {
        console.error('Auto-refresh failed:', e)
      }
    }, 20000)
  },
  beforeUnmount() {
    if (this.refreshTimer) clearInterval(this.refreshTimer)
    
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy()
    })
  },
  methods: {
    onStatCardClick(key) {
      
      if (this.isEmployeeOnly) return
      this.openExample(key)
    },
    initializeStatCards() {
      
      const savedLayout = localStorage.getItem('dashboardLayout')
      if (savedLayout) {
        try {
          const parsed = JSON.parse(savedLayout)
          // Fallback to rebuild if it's the old layout missing grid coords OR using the broken 4-column scale
          if (parsed.length && (parsed[0].w === undefined || parsed[0].w === 1)) {
            console.log("Old layout detected, resetting to default 2D layout.");
            this.setDefaultLayout()
            this.$nextTick(() => this.initGrid()); // Re-init grid after setting defaults
          } else {
            this.statCards = parsed
            this.updateStatCards()
          }
        } catch (e) {
          this.setDefaultLayout()
          this.$nextTick(() => this.initGrid()); // Re-init grid after setting defaults
        }
      } else {
        this.setDefaultLayout()
      }
    },
    setDefaultLayout() {
      if (this.isEmployeeOnly) {
        
        const c = this.ticketStatusCounts
        this.statCards = [
          { key: 'assigned', icon: '🎟️', label: 'Assigned Tickets', value: this.myAssignedTickets.length, x: 0, y: 0, w: 3, h: 1 },
          { key: 'openTickets', icon: '', label: 'Open', value: c.open || 0, x: 3, y: 0, w: 3, h: 1 },
          { key: 'inProgress', icon: '⏱️', label: 'In Progress', value: c.in_progress || 0, x: 6, y: 0, w: 3, h: 1 },
          { key: 'completedTickets', icon: '✅', label: 'Completed', value: c.completed || 0, x: 9, y: 0, w: 3, h: 1 }
        ]
      } else {
        
        this.statCards = [
          { key: 'contacts', icon: '👥', label: 'Total Contacts', value: this.contacts.length, x: 0, y: 0, w: 3, h: 1 },
          { key: 'companies', icon: '🏢', label: 'Companies', value: this.companies.length, x: 3, y: 0, w: 3, h: 1 },
          { key: 'deals', icon: '💰', label: 'Active Deals', value: this.activeDeals.length, x: 6, y: 0, w: 3, h: 1 },
          { key: 'revenue', icon: '📈', label: 'Pipeline Value', value: `R${this.pipelineSum}`, x: 9, y: 0, w: 3, h: 1 }
        ]
      }
    },
    updateStatCards() {
      
      if (this.isEmployeeOnly) {
        const c = this.ticketStatusCounts
        this.statCards.forEach(card => {
          switch(card.key) {
            case 'assigned':
              card.value = this.myAssignedTickets.length; break;
            case 'openTickets':
              card.value = c.open || 0; break;
            case 'inProgress':
              card.value = c.in_progress || 0; break;
            case 'completedTickets':
              card.value = c.completed || 0; break;
          }
        })
      } else {
        this.statCards.forEach(card => {
          switch(card.key) {
            case 'contacts':
              card.value = this.contacts.length; break;
            case 'companies':
              card.value = this.companies.length; break;
            case 'deals':
              card.value = this.activeDeals.length; break;
            case 'revenue':
              card.value = `R${this.pipelineSum}`; break;
          }
        })
      }
    },
    saveLayout() {
      
      localStorage.setItem('dashboardLayout', JSON.stringify(this.statCards))
    },
    initGrid() {
      if (this.grid) {
        this.grid.destroy(false);
      }
      this.grid = GridStack.init({
        column: 12,
        cellHeight: 110,
        margin: 16,
        handle: '.drag-handle',
        animate: true,
        float: true,
        disableOneColumnMode: true, // Prevent snapping to 1 column on smaller screens
        disableResize: false, // Allow resizing
        disableDrag: false,   // Allow dragging
      }, this.$refs.topStatsGrid);

      this.grid.load(this.statCards.map(card => ({
        id: card.key,
        x: card.x, y: card.y, w: card.w, h: card.h
      })));

      this.grid.on('change', (event, items) => {
        if (!items) return;
        items.forEach(item => {
          const card = this.statCards.find(c => c.key === item.id);
          if (card) {
            card.x = item.x;
            card.y = item.y;
            card.w = item.w;
            card.h = item.h;
          }
        });
        this.saveLayout();
      });
    },
    initializeCharts() {
      
      if (!this.isEmployeeOnly) {
        this.createPipelineChart()
      }
    },
    createPipelineChart() {
      const canvas = this.$refs.pipelineChart
      if (!canvas) return

      const stages = {
        'lead': 0,
        'qualified': 0,
        'proposal': 0,
        'negotiation': 0,
        'closed_won': 0,
        'closed_lost': 0
      }

      this.deals.forEach(deal => {
        if (stages.hasOwnProperty(deal.stage)) {
          stages[deal.stage] += Number(deal.value || 0)
        }
      })

      if (this.charts.pipeline) this.charts.pipeline.destroy()
      
      this.charts.pipeline = new Chart(canvas, {
        type: 'doughnut',
        data: {
          labels: ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost'],
          datasets: [{
            data: Object.values(stages),
            backgroundColor: [
              '#D4AF37', 
              '#10B981', 
              '#3B82F6', 
              '#B49015', 
              '#059669', 
              '#6B7280'  
            ],
            borderWidth: 2,
            borderColor: '#111418'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 15,
                  font: { size: 11 },
                  color: '#9ca3af'
              }
            }
          }
        }
      })
    },
    updateCharts() {
      
      if (this.charts.pipeline) {
        const stages = {
          'lead': 0,
          'qualified': 0,
          'proposal': 0,
          'negotiation': 0,
          'closed_won': 0,
          'closed_lost': 0
        }
        this.deals.forEach(deal => {
          if (stages.hasOwnProperty(deal.stage)) {
            stages[deal.stage] += Number(deal.value || 0)
          }
        })
        this.charts.pipeline.data.datasets[0].data = Object.values(stages)
        this.charts.pipeline.update()
      }
    },
    openExample(type) {
      this.exampleType = type
      if (type === 'deals') this.selectedDeal = null
      this.showExampleModal = true
    },
    async loadDeals() {
      try {
        const response = await dealsAPI.getAll()
        this.deals = response.data
      } catch (error) {
        console.error('Error loading deals:', error)
      }
    },
    async loadTickets() {
      try {
        const response = await ticketsAPI.getAll()
        this.tickets = Array.isArray(response.data) ? response.data : []
      } catch (error) {
        console.error('Error loading tickets:', error)
        this.tickets = []
      }
    },
    priorityBadgeColor(priority) {
      const map = { high: 'red', medium: 'amber', low: 'green' }
      return map[(priority || '').toLowerCase()] || 'gray'
    },
    statusBadgeColor(status) {
      const map = { open: 'blue', in_progress: 'amber', completed: 'green', failed: 'red' }
      return map[(status || '').toLowerCase()] || 'gray'
    },
        formatStatus(status) {
      
      return status.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
    },
    formatDueDate(dueAt) {
      if (!dueAt) return ''
      try {
        const date = new Date(dueAt)
        const now = new Date()
        const diffMs = date - now
        const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))
        
        if (diffDays < 0) {
          return `Overdue by ${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? 's' : ''}`
        } else if (diffDays === 0) {
          return 'Due Today'
        } else if (diffDays === 1) {
          return 'Due Tomorrow'
        } else if (diffDays <= 7) {
          return `Due in ${diffDays} days`
        } else {
          return date.toLocaleDateString('en-ZA', { month: 'short', day: 'numeric', year: 'numeric' })
        }
      } catch (e) {
        return dueAt
      }
    },
    closeExample() {
      this.showExampleModal = false
      this.exampleType = null
      this.selectedDeal = null
    },
    selectDeal(deal) {
      this.selectedDeal = deal
    },
    onModalKeydown(e) {
      const el = e.currentTarget
      const step = 80
      switch (e.key) {
        case 'ArrowDown':
          el.scrollBy({ top: step, behavior: 'smooth' }); e.preventDefault(); break
        case 'ArrowUp':
          el.scrollBy({ top: -step, behavior: 'smooth' }); e.preventDefault(); break
        case 'PageDown':
          el.scrollBy({ top: el.clientHeight - 40, behavior: 'smooth' }); e.preventDefault(); break
        case 'PageUp':
          el.scrollBy({ top: -el.clientHeight + 40, behavior: 'smooth' }); e.preventDefault(); break
        case 'Home':
          el.scrollTo({ top: 0, behavior: 'smooth' }); e.preventDefault(); break
        case 'End':
          el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' }); e.preventDefault(); break
      }
    },
    async cancelDeal(deal) {
      const ok = await modal.danger('Cancel Deal', `Are you sure you want to cancel the deal "${deal.title}"?`, { confirmText: 'Cancel Deal' })
      if (!ok) return
      try {
        await dealsAPI.delete(deal.id)
        toast.success('Deal Cancelled', 'The deal has been cancelled successfully.')
        this.selectedDeal = null
        await this.loadDeals()
      } catch (error) {
        console.error('Error cancelling deal:', error)
        toast.error('Cancel Failed', 'Failed to cancel deal. Please try again.')
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
    viewCompanies() {
      
      this.$router.push('/companies')
    },
    openAddCompany() {
      if (this.contacts.length === 0) {
        modal.warning('Contact Required', 'Capture at least one contact (with their company name) before creating a company profile. Add a contact first, then return here.')
        this.openAddContact()
        return
      }
      this.showCompanyModal = true
    },
    openAddContact() {
      this.showContactModal = true
    },
    getContactCompany(contact) {
      if (!contact.company) {
        return contact.company_name_manual || 'No Linked Company'
      }
      const company = this.companies.find(c => Number(c.id) === Number(contact.company))
      return company ? company.name : (contact.company_name_manual || 'Unknown Company')
    },
    openCreateDeal() {
      
      if (this.companies.length === 0) {
        modal.warning('Company Required', 'You need to formalise a company profile first!\n\nSteps to create a deal:\n1. Add a contact and capture their company name\n2. Click "Add Company" to convert the organisation into a profile\n3. Link the contact to that company\n4. Then you can create deals')
        return
      }
      if (this.contacts.length === 0) {
        modal.warning('Contact Required', 'You need to add a Contact first!\n\nSteps:\n1. Click "Add Contact" button\n2. Fill in contact details and capture their company name\n3. (Optional) Link the contact to an existing company\n4. Then you can create deals for that contact')
        return
      }
      if (!this.contacts.some(contact => contact.company)) {
        modal.warning('Link Required', 'Link at least one contact to a company before creating a deal. Edit a contact, link them to the right company, then try again.')
        return
      }
      this.showDealModal = true
    },
    onDealCompanyChange() {
      if (!this.dealForm.company) {
        this.dealForm.contact = ''
        return
      }
      const contactExists = this.contactsForDeal.some(contact => Number(contact.id) === Number(this.dealForm.contact))
      if (!contactExists) {
        this.dealForm.contact = ''
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
    refreshQuickSelfEmployedGeneratedName(force = false) {
      const newName = this.computeQuickSelfEmployedGeneratedName()
      const previousGenerated = this.contactSelfEmployedGeneratedName
      this.contactSelfEmployedGeneratedName = newName

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
    computeQuickSelfEmployedGeneratedName() {
      const first = (this.contactForm.first_name || '').trim()
      const last = (this.contactForm.last_name || '').trim()
      const combined = [first, last].filter(Boolean).join(' ')
      return combined ? `${combined} (Self-Employed)` : 'Self-Employed Business'
    },
    async saveContact() {
      this.contactFormErrors = {}

      const payload = {
        ...this.contactForm,
        company: this.contactForm.company || null
      }

      payload.company_name_manual = (payload.company_name_manual || '').trim()
      if (payload.is_self_employed && !payload.company_name_manual) {
        payload.company_name_manual = this.computeQuickSelfEmployedGeneratedName()
      }

      payload.company_direct_line = payload.is_self_employed
        ? ''
        : (payload.company_direct_line || '').trim()

      if (payload.phone) {
        payload.phone = payload.phone.trim()
      }

      const validationErrors = this.validateQuickContact(payload)
      if (Object.keys(validationErrors).length) {
        this.contactFormErrors = validationErrors
        return
      }

      this.contactFormSubmitting = true

      try {
        await contactsAPI.create(payload)
        toast.success('Contact Added', 'Contact has been added successfully!')
        this.closeContactModal()
        await Promise.all([this.loadContacts(), this.loadCompanies()])
        this.updateStatCards()
        this.updateCharts()
      } catch (error) {
        console.error('Error saving contact:', error)
        this.contactFormErrors = this.extractContactApiErrors(error)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      } finally {
        this.contactFormSubmitting = false
      }
    },
    validateQuickContact(payload) {
      const errors = {}

      if (!(payload.first_name || '').trim()) {
        errors.first_name = 'First name is required.'
      }
      if (!(payload.last_name || '').trim()) {
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
    extractContactApiErrors(error) {
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
    onQuickCompanyInputFocus() {
      this.contactCompanyInputFocused = true
      if (this._quickCompanyBlurTimeout) {
        clearTimeout(this._quickCompanyBlurTimeout)
        this._quickCompanyBlurTimeout = null
      }
    },
    onQuickCompanyInputBlur() {
      this._quickCompanyBlurTimeout = setTimeout(() => {
        this.contactCompanyInputFocused = false
      }, 150)
    },
    onQuickCompanyInput() {
      if (this.contactForm.is_self_employed) {
        const manual = (this.contactForm.company_name_manual || '').trim()
        const generated = (this.contactSelfEmployedGeneratedName || '').trim()
        if (manual && generated && manual.toLowerCase() !== generated.toLowerCase()) {
          this.contactForm.is_self_employed = false
        }
      }
    },
    selectQuickCompanySuggestion(name) {
      this.contactForm.company_name_manual = name
      this.contactCompanyInputFocused = false
    },
    isPersonalEmailDomain(email) {
      const domain = email.split('@').pop().toLowerCase()
      return PERSONAL_EMAIL_DOMAINS.has(domain)
    },
    isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    },
    async saveCompany() {
      try {
        await companiesAPI.create(this.companyForm)
        toast.success('Company Added', 'Company has been added successfully!')
        this.closeCompanyModal()
        await this.loadCompanies()
      } catch (error) {
        console.error('Error saving company:', error)
        const data = error.response?.data || {}
        const errorMsg =
          data.detail ||
          data.error ||
          data.non_field_errors?.[0] ||
          data.name?.[0] ||
          error.message ||
          'Failed to save company'
        const upgrade = data.upgrade_message ? `\n${data.upgrade_message}` : ''
        toast.error('Save Failed', `${errorMsg}${upgrade}`)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      }
    },
    async saveDeal() {
      try {
        const payload = {
          ...this.dealForm,
          company: this.dealForm.company ? Number(this.dealForm.company) : null,
          contact: this.dealForm.contact ? Number(this.dealForm.contact) : null,
          value: this.dealForm.value
        }
        await dealsAPI.create(payload)
        toast.success('Deal Created', 'Deal has been created successfully!')
        this.closeDealModal()
        await this.loadDeals()
      } catch (error) {
        console.error('Error saving deal:', error)
        const data = error.response?.data || {}
        const errorMsg =
          data.detail ||
          data.error ||
          data.non_field_errors?.[0] ||
          data.title?.[0] ||
          error.message ||
          'Failed to save deal'
        const upgrade = data.upgrade_message ? `\n${data.upgrade_message}` : ''
        toast.error('Save Failed', `${errorMsg}${upgrade}`)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      }
    },
    closeContactModal() {
      this.showContactModal = false
      this.contactForm = {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        is_self_employed: false,
        company_direct_line: '',
        company_name_manual: '',
        company: ''
      }
      this.contactFormErrors = {}
      this.contactFormSubmitting = false
      this.contactCompanyInputFocused = false
      this.contactSelfEmployedGeneratedName = ''
      if (this._quickCompanyBlurTimeout) {
        clearTimeout(this._quickCompanyBlurTimeout)
        this._quickCompanyBlurTimeout = null
      }
    },
    closeCompanyModal() {
      this.showCompanyModal = false
      this.companyForm = {
        name: '',
        email: '',
        phone: '',
        address: ''
      }
    },
    closeDealModal() {
      this.showDealModal = false
      this.dealForm = {
        title: '',
        company: '',
        contact: '',
        value: '',
        stage: 'lead'
      }
    }
  }
}
</script>

<style scoped>
/* ═══ Dashboard — Corporate Clean ═══ */
.dashboard {
  padding: 1.5rem 2rem 3rem;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  margin-bottom: 1rem;
}
.page-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
}
.page-subtitle {
  color: #9ca3af;
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
}

/* Tier Chip */
.tier-chip {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.15rem;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  white-space: nowrap;
}
.tier-chip .tier-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #D4AF37;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.tier-chip .tier-price {
  font-size: 0.75rem;
  color: #9ca3af;
}
.tier-chip.tier-free { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.2); }
.tier-chip.tier-free .tier-label { color: #9ca3af; }
.tier-chip.tier-luxury { background: rgba(212, 175, 55, 0.15); border-color: #D4AF37; }
.tier-chip.tier-luxury .tier-label { color: #D4AF37; }
.tier-chip.tier-premium { background: rgba(212, 175, 55, 0.2); border-color: #D4AF37; }
.tier-chip.tier-premium .tier-label { color: #D4AF37; }
.tier-chip.tier-ultimate { background: linear-gradient(135deg, #D4AF37, #B49015); border-color: #D4AF37; }
.tier-chip.tier-ultimate .tier-label { color: #000; }
.tier-chip.tier-ultimate .tier-price { color: #111; }

/* Info Bars */
.info-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
}
.info-bar svg { flex-shrink: 0; }
.info-bar span { flex: 1; }
.info-bar--blue {
  background: rgba(212, 175, 55, 0.05);
  color: #D4AF37;
  border: 1px solid rgba(212, 175, 55, 0.2);
}
.info-bar--amber {
  background: rgba(212, 175, 55, 0.05);
  color: #D4AF37;
  border: 1px solid rgba(212, 175, 55, 0.2);
}

.top-stats-grid { margin-bottom: 2rem; background: transparent; }
.grid-stack-item-content { border-radius: var(--radius-md); }
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  cursor: pointer;
  position: relative;
  transition: box-shadow 0.2s, transform 0.15s;
  background: rgba(15, 15, 15, 0.8) !important;
  border: 1px solid rgba(212, 175, 55, 0.2);
  height: 100%;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.6), inset 0 0 15px rgba(212,175,55,0.05);
  border-color: rgba(212, 175, 55, 0.5);
}
.drag-handle {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  color: #6b7280;
  cursor: grab;
  padding: 0.25rem;
  line-height: 1;
  opacity: 0;
  transition: opacity 0.2s;
}
.stat-card:hover .drag-handle { opacity: 1; }
.drag-handle:active { cursor: grabbing; }

.stat-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(212, 175, 55, 0.1) !important;
  color: #D4AF37 !important;
}

.stat-body {
  min-width: 0;
}
.stat-label {
  font-size: 0.8rem;
  color: #9ca3af;
  margin: 0 0 0.15rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-weight: 600;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  line-height: 1.2;
}

/* Section Card (tickets) */
.section-card {
  padding: 1.5rem;
  margin-bottom: 2rem;
}
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.section-head h2 {
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
}
.ticket-desc {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #9ca3af;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 320px;
}

/* Analytics */
.analytics-section {
  margin-bottom: 2rem;
}
.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.chart-card {
  padding: 1.5rem;
}
.card-title,
.chart-card h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 1rem;
}
.chart-wrap {
  height: 220px;
  position: relative;
}
.chart-footer {
  display: flex;
  justify-content: space-around;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.1);
  margin-top: 1rem;
}
.chart-footer span {
  font-size: 0.85rem;
  color: #d1d5db;
  font-weight: 600;
}
.locked-card {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed rgba(212, 175, 55, 0.4);
  background: rgba(0, 0, 0, 0.4);
}
.locked-body {
  text-align: center;
  padding: 2rem 1.5rem;
}
.locked-body svg { margin-bottom: 0.75rem; }
.locked-body h4 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #D4AF37;
  margin: 0 0 0.5rem;
}
.locked-body p {
  font-size: 0.875rem;
  color: #9ca3af;
  margin: 0 0 1.25rem;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.5;
}

/* Quick Actions */
.quick-actions-bar {
  margin-bottom: 2rem;
}
.quick-actions-bar h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.75rem;
}
.qa-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.qa-buttons .btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

/* Dropdown suggestions (company input) */
.input-dropdown-wrap {
  position: relative;
}
.dropdown-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #111418;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius-md);
  max-height: 200px;
  overflow-y: auto;
  box-shadow: 0 10px 20px rgba(0,0,0,0.5);
  color: #fff;
  z-index: 20;
  list-style: none;
  padding: 0;
  margin: 0.25rem 0 0;
}
.dropdown-suggestions li {
  padding: 0.6rem 0.75rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.15s;
}
.dropdown-suggestions li:hover {
  background: rgba(212, 175, 55, 0.2);
}

/* Alert */
.alert { padding: 0.75rem 1rem; border-radius: var(--radius-md); font-size: 0.875rem; font-weight: 500; margin-bottom: 1rem; }
.alert-danger { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }

/* Form helpers */
.form-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.form-check {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #d1d5db;
  font-weight: 500;
  cursor: pointer;
}
.form-check input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: var(--primary-500);
}

/* Preview / Example modal */
.preview-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}
.preview-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  font-size: 0.875rem;
  color: #d1d5db;
}
.preview-list li:last-child { border-bottom: none; }

.deals-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 0.75rem 0;
}
.deal-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.deal-row:hover { background: rgba(212, 175, 55, 0.1); border-color: rgba(212, 175, 55, 0.3); }
.deal-row.selected { background: rgba(212, 175, 55, 0.2); border-color: #D4AF37; }
.deal-name { font-weight: 600; color: #fff; }
.deal-val { font-weight: 600; color: #D4AF37; font-size: 0.9rem; }
.deal-detail {
  margin-top: 1rem;
  padding: 1rem;
}
.deal-detail h4 {
  margin: 0 0 0.75rem;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
}
.deal-detail p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #d1d5db;
}

.modal-lg {
  max-width: 640px;
}

/* Base overrides for inside components */
.modal-panel { background: rgba(17, 20, 24, 0.95); border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8); color: #fff; }
.modal-header { border-bottom: 1px solid rgba(255,255,255,0.1); }
.modal-header h3 { color: #fff; }
.form-input { background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: #fff; }
.form-input:focus { border-color: #D4AF37; box-shadow: 0 0 0 3px rgba(212,175,55,0.2); }
.form-label { color: #d1d5db; }
.form-hint { color: #9ca3af; }
.modal-footer { border-top: 1px solid rgba(255,255,255,0.1); }
.data-table th { background: rgba(255,255,255,0.05); color: #9ca3af; border-bottom: 1px solid rgba(255,255,255,0.1); padding: 10px; text-align: left; }
.data-table td { border-bottom: 1px solid rgba(255,255,255,0.05); color: #fff; padding: 10px; }
.btn-secondary { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #fff; }
.btn-secondary:hover { border-color: #D4AF37; color: #D4AF37; }

/* Text helpers */
.text-muted { color: var(--gray-500); }
.fw-600 { font-weight: 600; }

/* Employee Performance wrapper */
.emp-perf {
  margin-top: 1.5rem;
}

/* ═══ Responsive ═══ */
@media (max-width: 768px) {
  .dashboard { padding: 1rem; }
  .header-row { flex-direction: column; gap: 0.75rem; }
  .tier-chip { align-items: flex-start; }
  .analytics-grid { grid-template-columns: 1fr; }
  .qa-buttons { flex-direction: column; }
  .qa-buttons .btn { width: 100%; justify-content: center; }
  .form-row-2col { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
}
</style>
