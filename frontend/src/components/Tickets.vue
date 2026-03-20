<template>
  <div class="tickets-page">
    <div class="page-header">
      <div>
        <h1>Tickets &amp; Tasks</h1>
        <p class="page-subtitle">Track and manage your project tickets</p>
      </div>
      <button v-if="isAdmin" class="btn btn-primary" @click="showCreateModal = true">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="8" y1="3" x2="8" y2="13"/><line x1="3" y1="8" x2="13" y2="8"/></svg>
        Create Ticket
      </button>
    </div>

    <div class="summary-row">
      <div class="stat-card">
        <div class="stat-icon-wrap green"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="9" r="7"/></svg></div>
        <div class="stat-body"><span class="stat-value">{{ openTickets }}</span><span class="stat-label">Open</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-wrap amber"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 2v7l4 2"/><circle cx="9" cy="9" r="7"/></svg></div>
        <div class="stat-body"><span class="stat-value">{{ inProgressTickets }}</span><span class="stat-label">In Progress</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-wrap blue"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 9 7 12 14 5"/></svg></div>
        <div class="stat-body"><span class="stat-value">{{ completedTickets }}</span><span class="stat-label">Completed</span></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-wrap red"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="5" x2="13" y2="13"/><line x1="13" y1="5" x2="5" y2="13"/></svg></div>
        <div class="stat-body"><span class="stat-value">{{ failedTickets }}</span><span class="stat-label">Failed</span></div>
      </div>
    </div>

    <div v-if="loading" style="text-align:center;padding:3rem"><span class="spinner"></span></div>

    <div v-else-if="tickets.length === 0" class="empty-state">
      <svg width="48" height="48" fill="none" stroke="var(--gray-400)" stroke-width="1.5"><rect x="6" y="6" width="36" height="36" rx="4"/><line x1="14" y1="16" x2="34" y2="16"/><line x1="14" y1="24" x2="28" y2="24"/><line x1="14" y1="32" x2="22" y2="32"/></svg>
      <h3>No Tickets Yet</h3>
      <p v-if="isAdmin">Create your first ticket to get started</p>
      <p v-else>No tickets have been assigned to you yet</p>
    </div>

    <div v-else class="ticket-list">
      <div v-for="ticket in tickets" :key="ticket.id" :id="`ticket-${ticket.id}`" class="ticket-card card">
        <div class="ticket-top">
          <div class="ticket-title-wrap">
            <h3 class="ticket-title">{{ ticket.title }}</h3>
            <span class="badge" :class="statusBadge(ticket.status)">{{ formatStatus(ticket.status) }}</span>
          </div>
          <span class="badge" :class="priorityBadge(ticket.priority)">{{ (ticket.priority || 'normal').replace('_',' ') }}</span>
        </div>

        <p v-if="ticket.description" class="ticket-desc">{{ ticket.description }}</p>

        <div class="meta-row">
          <span class="meta-tag">Category: {{ (ticket.category || 'general').replace('_',' ') }}</span>
          <span class="meta-tag">Dept: {{ (ticket.department || 'support').replace('_',' ') }}</span>
          <span v-if="ticket.deal" class="meta-tag">Deal: {{ ticket.contact_name || 'N/A' }}</span>
          <span class="meta-tag">Assigned: {{ ticket.assigned_to_username }}</span>
          <span v-if="ticket.created_by_username" class="meta-tag">By: {{ ticket.created_by_username }}</span>
          <span v-if="ticket.due_at" class="meta-tag">Due: {{ formatDate(ticket.due_at) }}</span>
          <span v-if="ticket.duration_seconds > 0" class="meta-tag">Time: {{ formatDuration(ticket.duration_seconds) }}</span>
        </div>

        <div class="ticket-actions">
          <template v-if="isAdmin">
            <button v-if="ticket.status === 'open'" @click="startTicket(ticket.id)" class="btn btn-sm btn-primary">Start</button>
            <button v-if="ticket.status === 'in_progress' && !ticket.started_at" @click="stopTicket(ticket.id)" class="btn btn-sm btn-secondary">Pause</button>
            <button v-if="ticket.status !== 'completed'" @click="completeTicket(ticket.id)" class="btn btn-sm btn-success">Complete</button>
            <button @click="openEditModal(ticket)" class="btn btn-sm btn-secondary">Edit</button>
            <button @click="deleteTicket(ticket.id)" class="btn btn-sm btn-danger">Delete</button>
          </template>
          <template v-else>
            <button v-if="ticket.status !== 'completed' && ticket.assigned_to_username === currentUsername" @click="completeTicket(ticket.id)" class="btn btn-sm btn-success">Mark Complete</button>
          </template>
        </div>
      </div>
    </div>

    <div v-if="showCreateModal" class="modal-overlay" @click="closeCreateModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Create New Ticket</h3>
          <button class="modal-close" @click="closeCreateModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Title *</label>
            <input v-model="newTicket.title" placeholder="Enter ticket title" class="form-input" ref="titleInput">
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea v-model="newTicket.description" placeholder="Describe the task..." class="form-input" rows="4"></textarea>
          </div>
          <div class="form-grid-3">
            <div class="form-group">
              <label class="form-label">Priority</label>
              <select v-model="newTicket.priority" class="form-input">
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Category</label>
              <select v-model="newTicket.category" class="form-input">
                <option value="general">General</option>
                <option value="support">Support</option>
                <option value="bug">Bug</option>
                <option value="feature">Feature Request</option>
                <option value="task">Task</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Department</label>
              <select v-model="newTicket.department" class="form-input">
                <option value="support">Support</option>
                <option value="sales">Sales</option>
                <option value="operations">Operations</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Deal (Optional)</label>
            <select v-model="newTicket.deal" class="form-input">
              <option :value="null">No Deal</option>
              <option v-for="deal in deals" :key="deal.id" :value="deal.id">{{ deal.title }} - {{ deal.contact_name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Assign To *</label>
            <select v-model="newTicket.assigned_to" class="form-input">
              <option :value="null">Select Employee</option>
              <option v-for="user in users" :key="user.id" :value="user.user">{{ user.full_name || user.username }}<template v-if="user.job_title"> - {{ user.job_title }}</template><template v-if="user.role !== 'user'"> ({{ getRoleLabel(user.role) }})</template></option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Due Date</label>
            <input v-model="newTicket.due_at" type="datetime-local" class="form-input">
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeCreateModal" class="btn btn-secondary">Cancel</button>
          <button @click="createTicket" class="btn btn-primary" :disabled="!canCreate">Create Ticket</button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Edit Ticket</h3>
          <button class="modal-close" @click="closeEditModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Title *</label>
            <input v-model="editTicket.title" placeholder="Enter ticket title" class="form-input">
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea v-model="editTicket.description" placeholder="Describe the task..." class="form-input" rows="4"></textarea>
          </div>
          <div class="form-grid-3">
            <div class="form-group">
              <label class="form-label">Priority</label>
              <select v-model="editTicket.priority" class="form-input">
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Category</label>
              <select v-model="editTicket.category" class="form-input">
                <option value="general">General</option>
                <option value="support">Support</option>
                <option value="bug">Bug</option>
                <option value="feature">Feature Request</option>
                <option value="task">Task</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Department</label>
              <select v-model="editTicket.department" class="form-input">
                <option value="support">Support</option>
                <option value="sales">Sales</option>
                <option value="operations">Operations</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Deal (Optional)</label>
            <select v-model="editTicket.deal" class="form-input">
              <option :value="null">No Deal</option>
              <option v-for="deal in deals" :key="deal.id" :value="deal.id">{{ deal.title }} - {{ deal.contact_name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Assign To *</label>
            <select v-model="editTicket.assigned_to" class="form-input">
              <option :value="null">Select Employee</option>
              <option v-for="user in users" :key="user.id" :value="user.user">{{ user.full_name || user.username }}<template v-if="user.job_title"> - {{ user.job_title }}</template><template v-if="user.role !== 'user'"> ({{ getRoleLabel(user.role) }})</template></option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Due Date</label>
            <input v-model="editTicket.due_at" type="datetime-local" class="form-input">
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeEditModal" class="btn btn-secondary">Cancel</button>
          <button @click="updateTicket" class="btn btn-primary" :disabled="!canEdit">Update Ticket</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ticketsAPI, dealsAPI, employeesAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'Tickets',
  data() {
    return {
      tickets: [],
      deals: [],
      users: [],
      loading: true,
      showCreateModal: false,
      showEditModal: false,
      newTicket: {
        title: '',
        description: '',
        priority: 'normal',
        category: 'general',
        department: 'support',
        deal: null,
        assigned_to: null,
        due_at: ''
      },
      editTicket: {
        id: null,
        title: '',
        description: '',
        priority: 'normal',
        category: 'general',
        department: 'support',
        deal: null,
        assigned_to: null,
        due_at: ''
      },
      isAdmin: false,
      currentUsername: ''
    }
  },
  computed: {
    openTickets() {
      return this.tickets.filter(t => t.status === 'open').length
    },
    inProgressTickets() {
      return this.tickets.filter(t => t.status === 'in_progress').length
    },
    completedTickets() {
      return this.tickets.filter(t => t.status === 'completed').length
    },
    failedTickets() {
      return this.tickets.filter(t => t.status === 'failed').length
    },
    canCreate() {
      return this.newTicket.title.trim() && this.newTicket.assigned_to
    },
    canEdit() {
      return this.editTicket.title.trim() && this.editTicket.assigned_to
    }
  },
  async mounted() {
    await this.checkAdminStatus()
    await this.loadTickets()
    if (this.isAdmin) {
      await this.loadDeals()
      await this.loadUsers()
    }
    
    const qid = this.$route?.query?.ticket
    if (qid) {
      this.$nextTick(() => this.highlightTicket(qid))
    }
  },
  watch: {
    '$route.query.ticket'(newVal) {
      if (newVal) this.$nextTick(() => this.highlightTicket(newVal))
    }
  },
  methods: {
    statusBadge(status) {
      const m = { open: 'badge-blue', in_progress: 'badge-amber', completed: 'badge-green', failed: 'badge-red' }
      return m[status] || 'badge-gray'
    },
    priorityBadge(priority) {
      const m = { urgent: 'badge-red', high: 'badge-amber', normal: 'badge-blue', low: 'badge-gray' }
      return m[priority] || 'badge-gray'
    },
    async checkAdminStatus() {
      const user = authService.getUser()
      this.currentUsername = user?.username || ''
      const isOwnerAdmin = (user?.username || '').toLowerCase() === 'adminluxury'
      const isClientAdmin = Boolean(
        (!user?.is_superuser && !user?.is_staff) && (
          (user?.permissions && user.permissions.is_admin) ||
          (user?.role && (user.role.value === 'admin' || user.role === 'admin')) ||
          (user?.profile && user.profile.role === 'admin')
        )
      )
      this.isAdmin = Boolean(user?.is_superuser || user?.is_staff || isOwnerAdmin || isClientAdmin)
    },
    highlightTicket(id) {
      const el = document.getElementById(`ticket-${id}`)
      if (!el) return
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      el.classList.add('highlight-pulse')
      setTimeout(() => el.classList.remove('highlight-pulse'), 3000)
    },
    async loadTickets(retryCount = 0) {
      try {
        this.loading = true
        const response = await ticketsAPI.getAll()
        this.tickets = response.data || []
      } catch (error) {
        console.error('Failed to load tickets:', error)
        if (retryCount < 2) {
          setTimeout(() => this.loadTickets(retryCount + 1), 3000)
          return
        }
        toast.error('Load Failed', 'Failed to load tickets — try refreshing the page')
      } finally {
        this.loading = false
      }
    },
    async loadDeals() {
      try {
        const response = await dealsAPI.getAll()
        this.deals = response.data || []
      } catch (error) {
        console.error('Failed to load deals:', error)
      }
    },
    async loadUsers() {
      try {
        const response = await employeesAPI.getAll()
        const allUsers = response.data || []
        const user = authService.getUser() || {}
        const isClientAdmin = Boolean(
          (!user.is_superuser && !user.is_staff) && (
            (user.permissions && user.permissions.is_admin) ||
            (user.role && (user.role.value === 'admin' || user.role === 'admin')) ||
            (user.profile && user.profile.role === 'admin')
          )
        )
        
        this.users = this.isAdmin || isClientAdmin
          ? allUsers
          : (allUsers.filter(u => (u.role === 'admin') || (u.role?.value === 'admin'))) 
      } catch (error) {
        console.error('Failed to load employees:', error)
      }
    },
    async createTicket() {
      if (!this.canCreate) return

      try {
        await ticketsAPI.create({
          title: this.newTicket.title,
          description: this.newTicket.description,
          priority: this.newTicket.priority,
          category: this.newTicket.category,
          department: this.newTicket.department,
          deal: this.newTicket.deal,
          assigned_to: this.newTicket.assigned_to,
          due_at: this.newTicket.due_at || null
        })
        
        this.closeCreateModal()
        await this.loadTickets()
        toast.success('Ticket Created', 'Ticket has been created successfully!')
      } catch (error) {
        console.error('Failed to create ticket:', error)
        toast.error('Create Failed', 'Failed to create ticket: ' + (error.response?.data?.detail || error.message))
      }
    },
    openEditModal(ticket) {
      this.editTicket = {
        id: ticket.id,
        title: ticket.title,
        description: ticket.description || '',
        priority: ticket.priority || 'normal',
        category: ticket.category || 'general',
        department: ticket.department || 'support',
        deal: ticket.deal,
        assigned_to: ticket.assigned_to,
        due_at: ticket.due_at ? new Date(ticket.due_at).toISOString().slice(0, 16) : ''
      }
      this.showEditModal = true
    },
    closeEditModal() {
      this.showEditModal = false
      this.editTicket = {
        id: null,
        title: '',
        description: '',
        priority: 'normal',
        category: 'general',
        department: 'support',
        deal: null,
        assigned_to: null,
        due_at: ''
      }
    },
    async updateTicket() {
      if (!this.canEdit) return

      try {
        await ticketsAPI.update(this.editTicket.id, {
          title: this.editTicket.title,
          description: this.editTicket.description,
          priority: this.editTicket.priority,
          category: this.editTicket.category,
          department: this.editTicket.department,
          deal: this.editTicket.deal,
          assigned_to: this.editTicket.assigned_to,
          due_at: this.editTicket.due_at || null
        })
        
        this.closeEditModal()
        await this.loadTickets()
        toast.success('Ticket Updated', 'Ticket has been updated successfully!')
      } catch (error) {
        console.error('Failed to update ticket:', error)
        toast.error('Update Failed', 'Failed to update ticket: ' + (error.response?.data?.detail || error.message))
      }
    },
    async startTicket(id) {
      const ok = await modal.confirm('Start Ticket', 'Start working on this ticket?', 'info', { confirmText: 'Start' })
      if (!ok) return
      
      try {
        await ticketsAPI.start(id)
        await this.loadTickets()
      } catch (error) {
        console.error('Failed to start ticket:', error)
        toast.error('Start Failed', 'Failed to start ticket')
      }
    },
    async stopTicket(id) {
      const ok = await modal.confirm('Stop Ticket', 'Pause work on this ticket?', 'warning', { confirmText: 'Stop' })
      if (!ok) return
      
      try {
        await ticketsAPI.stop(id)
        await this.loadTickets()
      } catch (error) {
        console.error('Failed to stop ticket:', error)
        toast.error('Stop Failed', 'Failed to stop ticket')
      }
    },
    async completeTicket(id) {
      const ok = await modal.confirm('Complete Ticket', 'Mark this ticket as completed?', 'success', { confirmText: 'Complete' })
      if (!ok) return
      
      try {
        await ticketsAPI.complete(id)
        await this.loadTickets()
        toast.success('Ticket Completed', 'Ticket has been marked as completed!')
      } catch (error) {
        console.error('Failed to complete ticket:', error)
        toast.error('Complete Failed', 'Failed to complete ticket: ' + (error.response?.data?.detail || error.message))
      }
    },
    async deleteTicket(id) {
      const ok = await modal.danger('Delete Ticket', 'Delete this ticket? This action cannot be undone.')
      if (!ok) return
      
      try {
        await ticketsAPI.delete(id)
        await this.loadTickets()
        toast.success('Ticket Deleted', 'Ticket has been removed.')
      } catch (error) {
        console.error('Failed to delete ticket:', error)
        toast.error('Delete Failed', 'Failed to delete ticket')
      }
    },
    closeCreateModal() {
      this.showCreateModal = false
      this.newTicket = {
        title: '',
        description: '',
        priority: 'normal',
        category: 'general',
        department: 'support',
        deal: null,
        assigned_to: null,
        due_at: ''
      }
    },
    formatStatus(status) {
      const statusMap = {
        'open': 'Open',
        'in_progress': 'In Progress',
        'completed': 'Completed',
        'failed': 'Failed'
      }
      return statusMap[status] || status
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-ZA', { day: '2-digit', month: 'short', year: 'numeric' })
    },
    formatDuration(seconds) {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      if (hours > 0) {
        return `${hours}h ${minutes}m`
      }
      return `${minutes}m`
    },
    getRoleLabel(role) {
      const labels = {
        admin: 'Admin',
        manager: 'Manager',
        supervisor: 'Supervisor',
        user: 'User'
      }
      return labels[role] || role
    }
  }
}
</script>
<style scoped>
.tickets-page { padding: 1.5rem 2rem; }

/* Summary row */
.summary-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card { background: #fff; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem 1.25rem; display: flex; align-items: center; gap: .75rem; }
.stat-icon-wrap { width: 40px; height: 40px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; }
.stat-icon-wrap.green { background: #ecfdf5; color: var(--green-500); }
.stat-icon-wrap.amber { background: #fffbeb; color: var(--amber-500); }
.stat-icon-wrap.blue  { background: #eff6ff; color: var(--primary-500); }
.stat-icon-wrap.red   { background: #fef2f2; color: var(--red-500); }
.stat-body { display: flex; flex-direction: column; }
.stat-value { font-size: 1.25rem; font-weight: 700; color: var(--gray-900); }
.stat-label { font-size: .75rem; color: var(--gray-500); text-transform: uppercase; letter-spacing: .04em; }

/* Ticket list */
.ticket-list { display: flex; flex-direction: column; gap: .75rem; }
.ticket-card { padding: 1.25rem; }
.ticket-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: .5rem; }
.ticket-title-wrap { display: flex; align-items: center; gap: .625rem; flex: 1; min-width: 0; }
.ticket-title { font-size: .9375rem; font-weight: 600; color: var(--gray-900); margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ticket-desc { font-size: .8125rem; color: var(--gray-600); margin: 0 0 .75rem; line-height: 1.5; }
.meta-row { display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: .75rem; }
.meta-tag { font-size: .75rem; color: var(--gray-600); background: var(--gray-100); padding: .25rem .5rem; border-radius: var(--radius-sm); white-space: nowrap; }
.ticket-actions { display: flex; gap: .5rem; flex-wrap: wrap; padding-top: .75rem; border-top: 1px solid var(--border-color); }

/* Form grid */
.form-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }

@media (max-width: 768px) {
  .summary-row { grid-template-columns: repeat(2, 1fr); }
  .form-grid-3 { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .summary-row { grid-template-columns: 1fr; }
}
</style>
