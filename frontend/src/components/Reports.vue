<template>
  <div class="reports-page">
    <div class="page-header">
      <div>
        <h1 v-if="!isEmployeeOnly">Reports &amp; Exports</h1>
        <h1 v-else>My Performance</h1>
        <p class="page-subtitle" v-if="!isEmployeeOnly">Download your CRM data like bank statements</p>
        <p class="page-subtitle" v-else>Your ticket performance summary</p>
      </div>
    </div>

    <section v-if="isEmployeeOnly">
      <EmployeePerformance />
    </section>

    <section v-if="!isEmployeeOnly && (isAdmin || isClientAdmin)" class="card" style="padding:1.25rem;margin-bottom:1.5rem">
      <h3 style="font-size:.9375rem;font-weight:600;color:var(--gray-900);margin:0 0 .75rem">Employee Performance</h3>
      <div class="form-group" style="max-width:400px">
        <label class="form-label">Select Employee</label>
        <select v-model="selectedEmployeeId" @change="loadSelectedEmployeePerformance" class="form-input">
          <option value="">-- Choose an employee --</option>
          <option v-for="emp in employees" :key="emp.id" :value="emp.id">{{ emp.user.first_name }} {{ emp.user.last_name }} - {{ emp.user.email }}</option>
        </select>
      </div>
      <div v-if="selectedEmployeeId">
        <EmployeePerformance :userId="selectedEmployeeId" :key="selectedEmployeeId" />
      </div>
    </section>

    <section v-else class="card" style="padding:1.25rem;margin-bottom:1.5rem">
      <h3 style="font-size:.9375rem;font-weight:600;color:var(--gray-900);margin:0 0 .75rem">Quick Overview</h3>
      <div class="overview-row">
        <div class="ov-stat">
          <span class="ov-val">{{ contacts.length }}</span>
          <span class="ov-lbl">Total Contacts</span>
        </div>
        <div class="ov-stat">
          <span class="ov-val">{{ activeDeals }}</span>
          <span class="ov-lbl">Active Deals</span>
        </div>
        <div class="ov-stat">
          <span class="ov-val">{{ companies.length }}</span>
          <span class="ov-lbl">Companies</span>
        </div>
        <div v-if="!isAdmin" class="ov-stat locked">
          <svg width="16" height="16" fill="none" stroke="var(--gray-400)" stroke-width="2"><rect x="3" y="7" width="10" height="7" rx="1.5"/><path d="M5 7V5a3 3 0 0 1 6 0v2"/></svg>
          <span class="ov-lbl">Advanced Metrics</span>
          <span class="ov-hint">Upgrade to unlock</span>
        </div>
      </div>
      <div v-if="!isAdmin" class="upgrade-tease">
        <p><strong>Want more insights?</strong> Upgrade to unlock revenue forecasting, win rate analytics, custom dashboards and more.</p>
        <button class="btn btn-sm btn-primary" @click="$router.push('/upgrade/luxury')">See Premium Plans</button>
      </div>
    </section>

    <div v-if="!isEmployeeOnly" class="reports-grid">
      <div class="report-card card">
        <div class="rc-icon blue"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10" cy="6" r="4"/><path d="M3 18c0-3.3 3.1-6 7-6s7 2.7 7 6"/></svg></div>
        <h3>Contacts Report</h3>
        <p>Export all contacts with relationship health scores</p>
        <span class="rc-count">{{ contacts.length }} contacts</span>
        <div class="rc-actions">
          <button @click="downloadContactsReport" class="btn btn-sm btn-primary" :disabled="downloading">{{ downloading ? 'Generating...' : 'PDF' }}</button>
          <button @click="downloadContactsCSV" class="btn btn-sm btn-secondary">CSV</button>
        </div>
      </div>

      <div class="report-card card">
        <div class="rc-icon green"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="14" height="14" rx="2"/><line x1="7" y1="8" x2="13" y2="8"/><line x1="7" y1="12" x2="11" y2="12"/></svg></div>
        <h3>Companies Report</h3>
        <p>Export all companies and their contact details</p>
        <span class="rc-count">{{ companies.length }} companies</span>
        <div class="rc-actions">
          <button @click="downloadCompaniesReport" class="btn btn-sm btn-primary" :disabled="downloading">{{ downloading ? 'Generating...' : 'PDF' }}</button>
          <button @click="downloadCompaniesCSV" class="btn btn-sm btn-secondary">CSV</button>
        </div>
      </div>

      <div class="report-card card">
        <div class="rc-icon amber"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="16" height="12" rx="2"/><path d="M6 4V2M14 4V2M2 8h16"/></svg></div>
        <h3>Deals Pipeline</h3>
        <p>Export your deal pipeline with values and stages</p>
        <span class="rc-count">{{ deals.length }} deals &middot; R{{ totalPipelineValue }}</span>
        <div class="rc-actions">
          <button @click="downloadDealsReport" class="btn btn-sm btn-primary" :disabled="downloading">{{ downloading ? 'Generating...' : 'PDF' }}</button>
          <button @click="downloadDealsCSV" class="btn btn-sm btn-secondary">CSV</button>
        </div>
      </div>

      <div class="report-card card">
        <div class="rc-icon blue"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 14 8 8 12 12 16 4"/></svg></div>
        <h3>Activity Report</h3>
        <p>Export your activity log and timeline</p>
        <span class="rc-count">{{ activities.length }} activities</span>
        <div class="rc-actions">
          <button @click="downloadActivitiesReport" class="btn btn-sm btn-primary" :disabled="downloading">{{ downloading ? 'Generating...' : 'PDF' }}</button>
          <button @click="downloadActivitiesCSV" class="btn btn-sm btn-secondary">CSV</button>
        </div>
      </div>

      <div class="report-card card">
        <div class="rc-icon red"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="14" height="14" rx="2"/><line x1="7" y1="7" x2="13" y2="7"/><line x1="7" y1="10" x2="10" y2="10"/><polyline points="7 13 9 15 13 11"/></svg></div>
        <h3>Tickets &amp; Tasks</h3>
        <p>Export tickets with time tracking and performance</p>
        <span class="rc-count">{{ tickets.length }} tickets &middot; {{ completedTicketsCount }} completed</span>
        <div class="rc-actions">
          <button @click="downloadTicketsReport" class="btn btn-sm btn-primary" :disabled="downloading">{{ downloading ? 'Generating...' : 'PDF' }}</button>
          <button @click="downloadTicketsCSV" class="btn btn-sm btn-secondary">CSV</button>
        </div>
      </div>

      <div class="report-card card featured">
        <div class="rc-icon blue"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="16" height="16" rx="2"/><path d="M6 10l3 3 5-6"/></svg></div>
        <h3>Complete CRM Export</h3>
        <p>Download everything &mdash; contacts, companies, deals, and activities</p>
        <span class="rc-count">Full data backup</span>
        <div class="rc-actions">
          <button @click="downloadCompleteReport" class="btn btn-sm btn-primary" :disabled="downloading">{{ downloading ? 'Generating...' : 'Download Complete Report' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { contactsAPI, companiesAPI, dealsAPI, activitiesAPI, ticketsAPI, employeesAPI } from '../api'
import EmployeePerformance from './EmployeePerformance.vue'

export default {
  name: 'Reports',
  components: { EmployeePerformance },
  data() {
    return {
      contacts: [],
      companies: [],
      deals: [],
      activities: [],
      tickets: [],
      downloading: false,
      employees: [],
      selectedEmployeeId: ''
    }
  },
  computed: {
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
    isAdmin() {
      const raw = localStorage.getItem('user')
      const user = raw ? JSON.parse(raw) : null
      return !!(user && (user.is_superuser || (user.username||'').toLowerCase()==='adminluxury'))
    },
    isClientAdmin() {
      const raw = localStorage.getItem('user')
      const user = raw ? JSON.parse(raw) : null
      const isAdminCheck = !!(user && (user.is_superuser || (user.username||'').toLowerCase()==='adminluxury'))
      return !isAdminCheck && !!(user && (
        (user.permissions && user.permissions.is_admin) ||
        (user.role && (user.role.value === 'admin' || user.role === 'admin')) ||
        (user.profile && user.profile.role === 'admin')
      ))
    },
    totalPipelineValue() {
      return this.deals.reduce((sum, deal) => sum + parseFloat(deal.value || 0), 0).toLocaleString()
    },
    activeDeals() {
      return this.deals.filter(d => d.stage !== 'closed_won' && d.stage !== 'closed_lost').length
    },
    completedTicketsCount() {
      return this.tickets.filter(t => t.status === 'completed').length
    }
  },
  async mounted() {
    if (!this.isEmployeeOnly) {
      await this.loadData()
      if (this.isAdmin || this.isClientAdmin) {
        await this.loadEmployees()
      }
    }
    
  },
  beforeUnmount() {
    
  },
  methods: {
    async loadData() {
      try {
        const [contactsRes, companiesRes, dealsRes, activitiesRes, ticketsRes] = await Promise.all([
          contactsAPI.getAll(),
          companiesAPI.getAll(),
          dealsAPI.getAll(),
          activitiesAPI.getAll(),
          ticketsAPI.getAll()
        ])
        
        this.contacts = contactsRes.data
        this.companies = companiesRes.data
        this.deals = dealsRes.data
        this.activities = activitiesRes.data
        this.tickets = ticketsRes.data
      } catch (error) {
        console.error('Error loading data:', error)
      }
    },
    async loadEmployees() {
      try {
        const res = await employeesAPI.getAll()
        this.employees = res.data || []
      } catch (error) {
        console.error('Error loading employees:', error)
      }
    },
    loadSelectedEmployeePerformance() {
      
    },

    downloadContactsCSV() {
      const now = new Date()
      const generatedAt = this.getFormattedTimestamp(now)
      const csv = this.generateContactsCSV(generatedAt)
      const filename = this.buildTimestampedFilename('contacts-report', 'csv', now)
      this.downloadFile(csv, filename, 'text/csv')
    },

    downloadCompaniesCSV() {
      const now = new Date()
      const generatedAt = this.getFormattedTimestamp(now)
      const csv = this.generateCompaniesCSV(generatedAt)
      const filename = this.buildTimestampedFilename('companies-report', 'csv', now)
      this.downloadFile(csv, filename, 'text/csv')
    },

    downloadDealsCSV() {
      const now = new Date()
      const generatedAt = this.getFormattedTimestamp(now)
      const csv = this.generateDealsCSV(generatedAt)
      const filename = this.buildTimestampedFilename('deals-report', 'csv', now)
      this.downloadFile(csv, filename, 'text/csv')
    },

    downloadActivitiesCSV() {
      const now = new Date()
      const generatedAt = this.getFormattedTimestamp(now)
      const csv = this.generateActivitiesCSV(generatedAt)
      const filename = this.buildTimestampedFilename('activities-report', 'csv', now)
      this.downloadFile(csv, filename, 'text/csv')
    },

    downloadTicketsCSV() {
      const now = new Date()
      const generatedAt = this.getFormattedTimestamp(now)
      const csv = this.generateTicketsCSV(generatedAt)
      const filename = this.buildTimestampedFilename('tickets-report', 'csv', now)
      this.downloadFile(csv, filename, 'text/csv')
    },

    async downloadTicketsReport() {
      this.downloading = true
      try {
        const now = new Date()
        const generatedAt = this.getFormattedTimestamp(now)
        const content = this.generateTicketsHTML(generatedAt)
        const filename = this.buildTimestampedFilename('tickets-report', 'html', now)
        this.downloadFile(content, filename, 'text/html')
      } finally {
        this.downloading = false
      }
    },

    async downloadContactsReport() {
      this.downloading = true
      try {
        const now = new Date()
        const generatedAt = this.getFormattedTimestamp(now)
        const content = this.generateContactsHTML(generatedAt)
        const filename = this.buildTimestampedFilename('contacts-report', 'html', now)
        this.downloadFile(content, filename, 'text/html')
      } finally {
        this.downloading = false
      }
    },

    async downloadCompaniesReport() {
      this.downloading = true
      try {
        const now = new Date()
        const generatedAt = this.getFormattedTimestamp(now)
        const content = this.generateCompaniesHTML(generatedAt)
        const filename = this.buildTimestampedFilename('companies-report', 'html', now)
        this.downloadFile(content, filename, 'text/html')
      } finally {
        this.downloading = false
      }
    },

    async downloadDealsReport() {
      this.downloading = true
      try {
        const now = new Date()
        const generatedAt = this.getFormattedTimestamp(now)
        const content = this.generateDealsHTML(generatedAt)
        const filename = this.buildTimestampedFilename('deals-report', 'html', now)
        this.downloadFile(content, filename, 'text/html')
      } finally {
        this.downloading = false
      }
    },

    async downloadActivitiesReport() {
      this.downloading = true
      try {
        const now = new Date()
        const generatedAt = this.getFormattedTimestamp(now)
        const content = this.generateActivitiesHTML(generatedAt)
        const filename = this.buildTimestampedFilename('activities-report', 'html', now)
        this.downloadFile(content, filename, 'text/html')
      } finally {
        this.downloading = false
      }
    },

    async downloadCompleteReport() {
      this.downloading = true
      try {
        const now = new Date()
        const generatedAt = this.getFormattedTimestamp(now)
        const content = this.generateCompleteHTML(generatedAt)
        const filename = this.buildTimestampedFilename('complete-crm-report', 'html', now)
        this.downloadFile(content, filename, 'text/html')
      } finally {
        this.downloading = false
      }
    },

    generateContactsCSV(generatedAt) {
      const headers = ['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Health Score', 'Last Contact']
      const [timestampRow, spacerRow] = this.buildTimestampRows(headers.length, generatedAt)
      const rows = this.contacts.map(c => [
        c.first_name,
        c.last_name,
        c.email,
        c.phone || '',
        c.company_name || c.company_name_manual || '',
        c.health_score || 'N/A',
        c.last_contact_date || 'Never'
      ])

      return [timestampRow, spacerRow, headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n')
    },

    generateCompaniesCSV(generatedAt) {
      const headers = ['Company Name', 'Email', 'Phone', 'Address']
      const [timestampRow, spacerRow] = this.buildTimestampRows(headers.length, generatedAt)
      const rows = this.companies.map(c => [
        c.name,
        c.email || '',
        c.phone || '',
        c.address || ''
      ])

      return [timestampRow, spacerRow, headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n')
    },

  generateDealsCSV(generatedAt) {
      const headers = ['Deal Title', 'Contact', 'Company', 'Value', 'Stage', 'Hours Tracked', 'Created']
      const [timestampRow, spacerRow] = this.buildTimestampRows(headers.length, generatedAt)
      const rows = this.deals.map(d => [
        d.title,
        d.contact_name || '',
        d.company_name || '',
        `R${d.value}`,
        d.stage,
        d.time_spent_hours || 0,
        this.formatISO(d.created_at)
      ])

      return [timestampRow, spacerRow, headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n')
    },

  generateActivitiesCSV(generatedAt) {
      const headers = ['Date', 'Action', 'Type', 'Entity', 'Details']
      const [timestampRow, spacerRow] = this.buildTimestampRows(headers.length, generatedAt)
      const rows = this.activities.map(a => [
        this.formatISO(a.created_at),
        a.action,
        a.entity_type,
        a.entity_name,
        a.details || ''
      ])

      return [timestampRow, spacerRow, headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n')
    },

    generateTicketsCSV(generatedAt) {
      const headers = ['ID', 'Title', 'Status', 'Assigned To', 'Created By', 'Deal', 'Time Spent (min)', 'Due Date', 'Created', 'Completed']
      const [timestampRow, spacerRow] = this.buildTimestampRows(headers.length, generatedAt)
      const rows = this.tickets.map(t => [
        t.id,
        t.title,
        t.status,
        t.assigned_to_username || 'Unassigned',
        t.created_by_username || '',
        t.deal_title || 'N/A',
        t.total_time_spent || 0,
        t.due_at ? this.formatISO(t.due_at) : 'No deadline',
        this.formatISO(t.created_at),
        t.completed_at ? this.formatISO(t.completed_at) : 'Not completed'
      ])

      return [timestampRow, spacerRow, headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n')
    },

    generateContactsHTML(generatedAt) {
      const timestamp = generatedAt || this.getFormattedTimestamp()
      return `
<!DOCTYPE html>
<html>
<head>
  <title>Contacts Report - THE FINISHER LUXURY</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
    .header { text-align: center; margin-bottom: 40px; }
    .header h1 { color: #d4af37; }
    table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #d4af37; color: #000; font-weight: 700; }
    .health-hot { color: #ef4444; font-weight: 700; }
    .health-warm { color: #f59e0b; font-weight: 700; }
    .health-cold { color: #3b82f6; font-weight: 700; }
    .health-risk { color: #dc2626; font-weight: 700; }
    .footer { text-align: center; margin-top: 40px; color: #666; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏆 THE FINISHER LUXURY</h1>
    <h2>Contacts Report</h2>
    <p>Generated on ${timestamp}</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Phone</th>
        <th>Company</th>
        <th>Health Score</th>
        <th>Last Contact</th>
      </tr>
    </thead>
    <tbody>
      ${this.contacts.map(c => `
        <tr>
          <td>${c.first_name} ${c.last_name}</td>
          <td>${c.email}</td>
          <td>${c.phone || 'N/A'}</td>
          <td>${c.company_name || c.company_name_manual || 'N/A'}</td>
          <td class="health-${this.getHealthClass(c.health_score)}">${this.getHealthLabel(c.health_score)}</td>
          <td>${c.last_contact_date || 'Never'}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
  <div class="footer">
    <p>© 2026 MTAMBO HOLDINGS - THE FINISHER LUXURY CRM</p>
    <p>Total Contacts: ${this.contacts.length}</p>
    <p>Report generated on ${timestamp}</p>
  </div>
</body>
</html>`
    },

    generateCompaniesHTML(generatedAt) {
      const timestamp = generatedAt || this.getFormattedTimestamp()
      return `
<!DOCTYPE html>
<html>
<head>
  <title>Companies Report - THE FINISHER LUXURY</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
    .header { text-align: center; margin-bottom: 40px; }
    .header h1 { color: #d4af37; }
    table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #d4af37; color: #000; font-weight: 700; }
    .footer { text-align: center; margin-top: 40px; color: #666; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏆 THE FINISHER LUXURY</h1>
    <h2>Companies Report</h2>
    <p>Generated on ${timestamp}</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Company Name</th>
        <th>Email</th>
        <th>Phone</th>
        <th>Address</th>
      </tr>
    </thead>
    <tbody>
      ${this.companies.map(c => `
        <tr>
          <td><strong>${c.name}</strong></td>
          <td>${c.email || 'N/A'}</td>
          <td>${c.phone || 'N/A'}</td>
          <td>${c.address || 'N/A'}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
  <div class="footer">
    <p>© 2026 MTAMBO HOLDINGS - THE FINISHER LUXURY CRM</p>
    <p>Total Companies: ${this.companies.length}</p>
  </div>
</body>
</html>`
    },

    generateDealsHTML(generatedAt) {
      const timestamp = generatedAt || this.getFormattedTimestamp()
      const total = this.totalPipelineValue
      return `
<!DOCTYPE html>
<html>
<head>
  <title>Deals Report - THE FINISHER LUXURY</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
    .header { text-align: center; margin-bottom: 40px; }
    .header h1 { color: #d4af37; }
    table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #d4af37; color: #000; font-weight: 700; }
    .stage { padding: 4px 8px; border-radius: 4px; font-size: 0.85em; font-weight: 600; }
    .stage-lead { background: #e0e7ff; color: #3730a3; }
    .stage-qualified { background: #dbeafe; color: #1e40af; }
    .stage-proposal { background: #fef3c7; color: #92400e; }
    .stage-negotiation { background: #fed7aa; color: #9a3412; }
    .stage-closed_won { background: #d1fae5; color: #065f46; }
    .stage-closed_lost { background: #fee2e2; color: #991b1b; }
    .footer { text-align: center; margin-top: 40px; color: #666; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏆 THE FINISHER LUXURY</h1>
    <h2>Deals Pipeline Report</h2>
    <p>Generated on ${timestamp}</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Deal Title</th>
        <th>Contact</th>
        <th>Company</th>
        <th>Value</th>
        <th>Stage</th>
        <th>Hours</th>
        <th>Created</th>
      </tr>
    </thead>
    <tbody>
      ${this.deals.map(d => `
        <tr>
          <td><strong>${d.title}</strong></td>
          <td>${d.contact_name || 'N/A'}</td>
          <td>${d.company_name || 'N/A'}</td>
          <td>R${d.value.toLocaleString()}</td>
          <td><span class="stage stage-${d.stage}">${d.stage.replace('_', ' ').toUpperCase()}</span></td>
          <td>${d.time_spent_hours || 0}h</td>
          <td>${this.formatLocal(d.created_at)}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
  <div class="footer">
    <p>© 2026 MTAMBO HOLDINGS - THE FINISHER LUXURY CRM</p>
    <p>Total Deals: ${this.deals.length} | Pipeline Value: R${total}</p>
    <p>Report generated on ${timestamp}</p>
  </div>
</body>
</html>`
    },

    generateActivitiesHTML(generatedAt) {
      const timestamp = generatedAt || this.getFormattedTimestamp()
      return `
<!DOCTYPE html>
<html>
<head>
  <title>Activity Report - THE FINISHER LUXURY</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
    .header { text-align: center; margin-bottom: 40px; }
    .header h1 { color: #d4af37; }
    table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #d4af37; color: #000; font-weight: 700; }
    .action-create { color: #16a34a; font-weight: 600; }
    .action-update { color: #2563eb; font-weight: 600; }
    .action-delete { color: #dc2626; font-weight: 600; }
    .footer { text-align: center; margin-top: 40px; color: #666; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏆 THE FINISHER LUXURY</h1>
    <h2>Activity Report</h2>
    <p>Generated on ${timestamp}</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Date & Time</th>
        <th>Action</th>
        <th>Type</th>
        <th>Entity</th>
        <th>Details</th>
      </tr>
    </thead>
    <tbody>
      ${this.activities.map(a => `
        <tr>
          <td>${this.formatLocal(a.created_at)}</td>
          <td class="action-${a.action}">${a.action.toUpperCase()}</td>
          <td>${a.entity_type}</td>
          <td>${a.entity_name}</td>
          <td>${a.details || 'N/A'}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
  <div class="footer">
    <p>© 2026 MTAMBO HOLDINGS - THE FINISHER LUXURY CRM</p>
    <p>Total Activities: ${this.activities.length}</p>
    <p>Report generated on ${timestamp}</p>
  </div>
</body>
</html>`
    },

    generateTicketsHTML(generatedAt) {
      const timestamp = generatedAt || this.getFormattedTimestamp()
      return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Tickets Report - THE FINISHER LUXURY</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; background: #f8fafc; color: #1e293b; }
    .header { text-align: center; margin-bottom: 40px; padding: 30px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; border-radius: 12px; }
    .header h1 { font-size: 32px; margin-bottom: 10px; }
    .header p { font-size: 16px; opacity: 0.9; }
    .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
    .summary-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }
    .summary-card .number { font-size: 36px; font-weight: 800; margin-bottom: 5px; }
    .summary-card .label { font-size: 14px; color: #64748b; text-transform: uppercase; font-weight: 600; }
    .summary-card.open .number { color: #10b981; }
    .summary-card.progress .number { color: #f59e0b; }
    .summary-card.completed .number { color: #3b82f6; }
    .summary-card.failed .number { color: #ef4444; }
    table { width: 100%; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px; border-collapse: collapse; }
    thead { background: linear-gradient(135deg, #1e293b, #334155); color: white; }
    th { padding: 15px; text-align: left; font-weight: 700; font-size: 14px; text-transform: uppercase; }
    td { padding: 12px 15px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
    tbody tr:hover { background: #f8fafc; }
    .status-open { background: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
    .status-in_progress { background: #fed7aa; color: #92400e; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
    .status-completed { background: #dbeafe; color: #1e40af; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
    .status-failed { background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
    .footer { text-align: center; padding: 30px; color: #64748b; font-size: 14px; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .footer p { margin: 5px 0; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🎫 Tickets & Tasks Report</h1>
    <p>THE FINISHER LUXURY - Performance & Time Tracking</p>
  </div>
  <div class="summary">
    <div class="summary-card open">
      <div class="number">${this.tickets.filter(t => t.status === 'open').length}</div>
      <div class="label">Open</div>
    </div>
    <div class="summary-card progress">
      <div class="number">${this.tickets.filter(t => t.status === 'in_progress').length}</div>
      <div class="label">In Progress</div>
    </div>
    <div class="summary-card completed">
      <div class="number">${this.tickets.filter(t => t.status === 'completed').length}</div>
      <div class="label">Completed</div>
    </div>
    <div class="summary-card failed">
      <div class="number">${this.tickets.filter(t => t.status === 'failed').length}</div>
      <div class="label">Failed</div>
    </div>
  </div>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Status</th>
        <th>Assigned To</th>
        <th>Time Spent</th>
        <th>Due Date</th>
        <th>Created</th>
      </tr>
    </thead>
    <tbody>
      ${this.tickets.map(t => `
        <tr>
          <td>#${t.id}</td>
          <td>${t.title}</td>
          <td><span class="status-${t.status}">${t.status.replace('_', ' ').toUpperCase()}</span></td>
          <td>${t.assigned_to_username || 'Unassigned'}</td>
          <td>${this.formatDuration(t.total_time_spent || 0)}</td>
          <td>${t.due_at ? this.formatLocal(t.due_at) : 'No deadline'}</td>
          <td>${this.formatLocal(t.created_at)}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
  <div class="footer">
    <p>© 2026 MTAMBO HOLDINGS - THE FINISHER LUXURY CRM</p>
    <p>Total Tickets: ${this.tickets.length} | Completed: ${this.completedTicketsCount}</p>
    <p>Report generated on ${timestamp}</p>
  </div>
</body>
</html>`
    },

    generateCompleteHTML(generatedAt) {
      const timestamp = generatedAt || this.getFormattedTimestamp()
      return `
<!DOCTYPE html>
<html>
<head>
  <title>Complete CRM Report - THE FINISHER LUXURY</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
    .header { text-align: center; margin-bottom: 40px; }
    .header h1 { color: #d4af37; }
    .section { margin: 40px 0; }
    .section h2 { color: #333; border-bottom: 3px solid #d4af37; padding-bottom: 10px; }
    table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 20px 0; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #d4af37; color: #000; font-weight: 700; }
    .footer { text-align: center; margin-top: 60px; color: #666; padding: 20px; border-top: 2px solid #d4af37; }
    .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }
    .summary-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .summary-card h3 { color: #d4af37; margin: 0; font-size: 2em; }
    .summary-card p { color: #666; margin: 10px 0 0 0; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏆 THE FINISHER LUXURY CRM</h1>
    <h2>Complete CRM Data Export</h2>
    <p>Generated on ${timestamp}</p>
  </div>
  
  <div class="summary">
    <div class="summary-card">
      <h3>${this.contacts.length}</h3>
      <p>Contacts</p>
    </div>
    <div class="summary-card">
      <h3>${this.companies.length}</h3>
      <p>Companies</p>
    </div>
    <div class="summary-card">
      <h3>${this.deals.length}</h3>
      <p>Deals</p>
    </div>
    <div class="summary-card">
      <h3>R${this.totalPipelineValue}</h3>
      <p>Pipeline Value</p>
    </div>
  </div>

  <div class="section">
    <h2>📞 Contacts (${this.contacts.length})</h2>
    ${this.contacts.length > 0 ? `
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Company</th>
          <th>Health Score</th>
        </tr>
      </thead>
      <tbody>
        ${this.contacts.slice(0, 50).map(c => `
          <tr>
            <td>${c.first_name} ${c.last_name}</td>
            <td>${c.email}</td>
            <td>${c.phone || 'N/A'}</td>
            <td>${c.company_name || c.company_name_manual || 'N/A'}</td>
            <td>${this.getHealthLabel(c.health_score)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    ${this.contacts.length > 50 ? '<p><em>Showing first 50 contacts. Download full CSV for complete data.</em></p>' : ''}
    ` : '<p>No contacts data.</p>'}
  </div>

  <div class="section">
    <h2>🏢 Companies (${this.companies.length})</h2>
    ${this.companies.length > 0 ? `
    <table>
      <thead>
        <tr>
          <th>Company Name</th>
          <th>Email</th>
          <th>Phone</th>
        </tr>
      </thead>
      <tbody>
        ${this.companies.slice(0, 50).map(c => `
          <tr>
            <td><strong>${c.name}</strong></td>
            <td>${c.email || 'N/A'}</td>
            <td>${c.phone || 'N/A'}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    ${this.companies.length > 50 ? '<p><em>Showing first 50 companies. Download full CSV for complete data.</em></p>' : ''}
    ` : '<p>No companies data.</p>'}
  </div>

  <div class="section">
    <h2>💼 Deals (${this.deals.length})</h2>
    ${this.deals.length > 0 ? `
    <table>
      <thead>
        <tr>
          <th>Deal Title</th>
          <th>Contact</th>
          <th>Company</th>
          <th>Value</th>
          <th>Stage</th>
        </tr>
      </thead>
      <tbody>
        ${this.deals.slice(0, 50).map(d => `
          <tr>
            <td><strong>${d.title}</strong></td>
            <td>${d.contact_name || 'N/A'}</td>
            <td>${d.company_name || 'N/A'}</td>
            <td>R${d.value.toLocaleString()}</td>
            <td>${d.stage.replace('_', ' ').toUpperCase()}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    ${this.deals.length > 50 ? '<p><em>Showing first 50 deals. Download full CSV for complete data.</em></p>' : ''}
    ` : '<p>No deals data.</p>'}
  </div>

  <div class="footer">
    <h3>© 2026 MTAMBO HOLDINGS</h3>
    <p>THE FINISHER LUXURY CRM - Premium Edition</p>
    <p>Report generated on ${timestamp}</p>
  </div>
</body>
</html>`
    },

    getHealthLabel(score) {
      if (!score) return 'N/A'
      if (score >= 80) return '🔥 Hot'
      if (score >= 60) return '⚡ Warm'
      if (score >= 40) return '❄️ Cold'
      return '⚠️ At Risk'
    },

    getHealthClass(score) {
      if (!score) return 'risk'
      if (score >= 80) return 'hot'
      if (score >= 60) return 'warm'
      if (score >= 40) return 'cold'
      return 'risk'
    },

    getFormattedTimestamp(date = new Date()) {
      return new Intl.DateTimeFormat('en-ZA', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        timeZoneName: 'short'
      }).format(date)
    },
    formatISO(dateString) {
      try { return new Date(dateString).toISOString() } catch (e) { return '' }
    },
    formatLocal(dateString) {
      try { return new Intl.DateTimeFormat('en-ZA', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(dateString)) } catch (e) { return '' }
    },
    formatDuration(totalSeconds) {
      if (!totalSeconds || totalSeconds === 0) return '0m'
      const hours = Math.floor(totalSeconds / 3600)
      const minutes = Math.floor((totalSeconds % 3600) / 60)
      if (hours > 0) {
        return `${hours}h ${minutes}m`
      }
      return `${minutes}m`
    },
    getTimestampForFilename(date = new Date()) {
      const pad = num => String(num).padStart(2, '0')
      const year = date.getFullYear()
      const month = pad(date.getMonth() + 1)
      const day = pad(date.getDate())
      const hours = pad(date.getHours())
      const minutes = pad(date.getMinutes())
      const seconds = pad(date.getSeconds())
      return `${year}-${month}-${day}_${hours}-${minutes}-${seconds}`
    },
    buildTimestampedFilename(base, ext, date = new Date()) {
      return `${base}-${this.getTimestampForFilename(date)}.${ext}`
    },
    buildTimestampRows(length, generatedAt) {
      const timestampRow = new Array(length).fill('')
      timestampRow[0] = 'Generated At'
      timestampRow[1] = generatedAt
      const spacerRow = new Array(length).fill('')
      return [timestampRow, spacerRow]
    },
    downloadFile(content, filename, mimeType) {
      const blob = new Blob([content], { type: mimeType })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }
  }
}
</script>
<style scoped>
.reports-page { padding: 1.5rem 2rem; }

/* Overview row */
.overview-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem; }
.ov-stat { display: flex; flex-direction: column; align-items: center; padding: .75rem; background: var(--gray-50); border-radius: var(--radius-md); }
.ov-val { font-size: 1.25rem; font-weight: 700; color: var(--gray-900); }
.ov-lbl { font-size: .75rem; color: var(--gray-500); text-transform: uppercase; letter-spacing: .03em; }
.ov-stat.locked { opacity: .5; }
.ov-hint { font-size: .625rem; color: var(--gray-400); }
.upgrade-tease { background: var(--gray-50); border-radius: var(--radius-md); padding: .75rem 1rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.upgrade-tease p { margin: 0; font-size: .8125rem; color: var(--gray-600); }

/* Reports grid */
.reports-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.report-card { padding: 1.25rem; display: flex; flex-direction: column; gap: .5rem; }
.report-card.featured { border: 2px solid var(--primary-500); }
.report-card h3 { font-size: .9375rem; font-weight: 600; color: var(--gray-900); margin: 0; }
.report-card p { font-size: .8125rem; color: var(--gray-500); margin: 0; line-height: 1.4; }
.rc-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; margin-bottom: .25rem; }
.rc-icon.blue  { background: #eff6ff; color: var(--primary-500); }
.rc-icon.green { background: #ecfdf5; color: var(--green-500); }
.rc-icon.amber { background: #fffbeb; color: var(--amber-500); }
.rc-icon.red   { background: #fef2f2; color: var(--red-500); }
.rc-count { font-size: .75rem; color: var(--gray-500); }
.rc-actions { display: flex; gap: .5rem; margin-top: auto; padding-top: .5rem; }

@media (max-width: 768px) {
  .overview-row { grid-template-columns: repeat(2, 1fr); }
  .reports-grid { grid-template-columns: 1fr; }
  .upgrade-tease { flex-direction: column; text-align: center; }
}
</style>
