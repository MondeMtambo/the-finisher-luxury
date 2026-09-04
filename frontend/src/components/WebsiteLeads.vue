<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Website Leads</h1>
        <p class="page-subtitle">Admin inbox for website inquiries with follow-up controls</p>
      </div>
      <div class="header-btns">
        <select class="form-input" v-model="statusFilter" @change="loadInbox">
          <option value="all">All Statuses</option>
          <option value="new">New</option>
          <option value="responded">Responded</option>
          <option value="closed">Closed</option>
        </select>
        <button class="btn btn-secondary" @click="loadInbox">Refresh</button>
      </div>
    </div>

    <div class="summary-grid">
      <div class="summary-card">
        <span class="label">Total</span>
        <strong>{{ summary.total || 0 }}</strong>
      </div>
      <div class="summary-card">
        <span class="label">New</span>
        <strong>{{ summary.new || 0 }}</strong>
      </div>
      <div class="summary-card">
        <span class="label">Responded</span>
        <strong>{{ summary.responded || 0 }}</strong>
      </div>
      <div class="summary-card">
        <span class="label">Meeting Accepted</span>
        <strong>{{ summary.meeting_accepted || 0 }}</strong>
      </div>
    </div>

    <div class="card table-card">
      <table class="data-table" v-if="leads.length">
        <thead>
          <tr>
            <th>Client</th>
            <th>Source</th>
            <th>Message</th>
            <th>Status</th>
            <th>Meeting</th>
            <th>Received</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lead in leads" :key="lead.id">
            <td>
              <strong>{{ lead.contact_name }}</strong>
              <div class="cell-sub">{{ lead.contact_email }}</div>
              <div class="cell-sub">{{ lead.contact_phone || 'No phone' }}</div>
            </td>
            <td>{{ lead.source }}</td>
            <td class="msg-cell">{{ truncate(lead.inbound_message, 110) }}</td>
            <td>
              <span class="badge" :class="statusClass(lead.response_status)">{{ lead.response_status }}</span>
            </td>
            <td>
              <span class="badge" :class="meetingClass(lead.meeting_status)">{{ lead.meeting_status }}</span>
            </td>
            <td>{{ formatDate(lead.inbound_received_at) }}</td>
            <td>
              <div class="row-actions">
                <button class="btn btn-sm btn-secondary" @click="quickMarkResponded(lead)">Responded</button>
                <button class="btn btn-sm btn-secondary" @click="quickMarkMeetingAccepted(lead)">Meeting Accepted</button>
                <button class="btn btn-sm btn-secondary" @click="quickMarkClosed(lead)">Close</button>
                <button class="btn btn-sm btn-primary" @click="openReply(lead)">Reply</button>
                <button class="btn btn-sm btn-secondary" @click="openCallLog(lead)">Log Call</button>
                <button class="btn btn-sm btn-secondary" @click="openMeeting(lead)">Meeting</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <p>No website leads in this filter.</p>
      </div>
    </div>

    <div v-if="activeLead" class="card detail-card">
      <h3>Selected Lead</h3>
      <p><strong>{{ activeLead.contact_name }}</strong> - {{ activeLead.contact_email }}</p>
      <p class="full-message">{{ activeLead.inbound_message || 'No message provided.' }}</p>
      <p class="meta">Handled by: {{ activeLead.handled_by_username || 'Not yet' }}</p>
      <p class="meta">Response notes: {{ activeLead.response_notes || 'None' }}</p>
      <p class="meta">Call notes: {{ activeLead.call_notes || 'None' }}</p>
      <p class="meta">Meeting notes: {{ activeLead.meeting_notes || 'None' }}</p>
    </div>

    <div v-if="showReplyModal" class="modal-overlay">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Reply to {{ activeLead?.contact_name }}</h3>
          <button class="modal-close" @click="closeReplyModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Subject</label>
            <input class="form-input" v-model="replyForm.subject" placeholder="Subject" />
          </div>
          <div class="form-group">
            <label class="form-label">Message</label>
            <textarea class="form-input" rows="6" v-model="replyForm.message" placeholder="Write your response"></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Internal Notes</label>
            <textarea class="form-input" rows="3" v-model="replyForm.response_notes" placeholder="Optional notes"></textarea>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeReplyModal">Cancel</button>
            <button class="btn btn-primary" :disabled="submitting" @click="sendReply">{{ submitting ? 'Sending...' : 'Send Reply' }}</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showCallModal" class="modal-overlay">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Log Call - {{ activeLead?.contact_name }}</h3>
          <button class="modal-close" @click="closeCallModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Call Notes</label>
            <textarea class="form-input" rows="5" v-model="callForm.call_notes" placeholder="Call notes"></textarea>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeCallModal">Cancel</button>
            <button class="btn btn-primary" :disabled="submitting" @click="saveCall">Save Call Log</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showMeetingModal" class="modal-overlay">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Meeting Update - {{ activeLead?.contact_name }}</h3>
          <button class="modal-close" @click="closeMeetingModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-row-2col">
            <div class="form-group">
              <label class="form-label">Meeting Status</label>
              <select class="form-input" v-model="meetingForm.meeting_status">
                <option value="none">none</option>
                <option value="proposed">proposed</option>
                <option value="accepted">accepted</option>
                <option value="declined">declined</option>
                <option value="completed">completed</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Meeting Date/Time</label>
              <input class="form-input" type="datetime-local" v-model="meetingForm.meeting_datetime" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Meeting Notes</label>
            <textarea class="form-input" rows="4" v-model="meetingForm.meeting_notes"></textarea>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeMeetingModal">Cancel</button>
            <button class="btn btn-primary" :disabled="submitting" @click="saveMeeting">Save Meeting</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { systemAPI, websiteLeadsAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'WebsiteLeads',
  data() {
    return {
      leads: [],
      summary: {},
      statusFilter: 'all',
      activeLead: null,
      showReplyModal: false,
      showCallModal: false,
      showMeetingModal: false,
      submitting: false,
      replyForm: {
        subject: '',
        message: '',
        response_notes: ''
      },
      callForm: {
        call_notes: ''
      },
      meetingForm: {
        meeting_status: 'none',
        meeting_datetime: '',
        meeting_notes: ''
      }
    }
  },
  async mounted() {
    await this.loadInbox()
  },
  methods: {
    async loadInbox() {
      try {
        const params = {}
        if (this.statusFilter !== 'all') params.status = this.statusFilter
        const response = await systemAPI.getWebsiteLeadInbox(params)
        this.summary = response.data.summary || {}
        this.leads = response.data.results || []
        this.activeLead = this.leads[0] || null
      } catch (error) {
        console.error('Failed to load website leads inbox:', error)
        toast.error(error.message || 'Failed to load website leads inbox')
      }
    },
    async quickMarkResponded(lead) {
      try {
        await websiteLeadsAPI.updateWorkflow(lead.id, {
          response_status: 'responded'
        })
        toast.success('Lead marked as responded')
        await this.loadInbox()
      } catch (error) {
        console.error('Failed to mark responded:', error)
        toast.error(error.message || 'Failed to update lead')
      }
    },
    async quickMarkMeetingAccepted(lead) {
      try {
        await websiteLeadsAPI.updateWorkflow(lead.id, {
          response_status: 'responded',
          meeting_status: 'accepted'
        })
        toast.success('Lead marked as meeting accepted')
        await this.loadInbox()
      } catch (error) {
        console.error('Failed to mark meeting accepted:', error)
        toast.error(error.message || 'Failed to update lead')
      }
    },
    async quickMarkClosed(lead) {
      try {
        await websiteLeadsAPI.updateWorkflow(lead.id, {
          response_status: 'closed'
        })
        toast.success('Lead closed')
        await this.loadInbox()
      } catch (error) {
        console.error('Failed to close lead:', error)
        toast.error(error.message || 'Failed to close lead')
      }
    },
    statusClass(value) {
      return value === 'new' ? 'badge-warning' : value === 'responded' ? 'badge-success' : 'badge-neutral'
    },
    meetingClass(value) {
      if (value === 'accepted') return 'badge-success'
      if (value === 'declined') return 'badge-danger'
      if (value === 'proposed') return 'badge-warning'
      return 'badge-neutral'
    },
    formatDate(value) {
      if (!value) return '-'
      return new Date(value).toLocaleString()
    },
    truncate(text, maxLen) {
      if (!text) return '-'
      return text.length > maxLen ? `${text.slice(0, maxLen)}...` : text
    },
    openReply(lead) {
      this.activeLead = lead
      this.replyForm = {
        subject: `Re: Your inquiry to Mtambo Holdings`,
        message: `Hi ${lead.contact_name || ''},\n\nThank you for your inquiry.\n\nBest regards,\nMtambo Holdings`,
        response_notes: lead.response_notes || ''
      }
      this.showReplyModal = true
    },
    closeReplyModal() {
      this.showReplyModal = false
    },
    async sendReply() {
      if (!this.activeLead) return
      this.submitting = true
      try {
        await websiteLeadsAPI.reply(this.activeLead.id, this.replyForm)
        toast.success('Reply sent successfully')
        this.closeReplyModal()
        await this.loadInbox()
      } catch (error) {
        console.error('Failed to send reply:', error)
        toast.error(error.message || 'Failed to send reply')
      } finally {
        this.submitting = false
      }
    },
    openCallLog(lead) {
      this.activeLead = lead
      this.callForm.call_notes = lead.call_notes || ''
      this.showCallModal = true
    },
    closeCallModal() {
      this.showCallModal = false
    },
    async saveCall() {
      if (!this.activeLead) return
      this.submitting = true
      try {
        await websiteLeadsAPI.updateWorkflow(this.activeLead.id, {
          call_notes: this.callForm.call_notes,
          response_status: 'responded'
        })
        toast.success('Call log saved')
        this.closeCallModal()
        await this.loadInbox()
      } catch (error) {
        console.error('Failed to save call notes:', error)
        toast.error(error.message || 'Failed to save call notes')
      } finally {
        this.submitting = false
      }
    },
    openMeeting(lead) {
      this.activeLead = lead
      this.meetingForm = {
        meeting_status: lead.meeting_status || 'none',
        meeting_datetime: lead.meeting_datetime ? this.toLocalDateTimeInput(lead.meeting_datetime) : '',
        meeting_notes: lead.meeting_notes || ''
      }
      this.showMeetingModal = true
    },
    closeMeetingModal() {
      this.showMeetingModal = false
    },
    toLocalDateTimeInput(isoDate) {
      const date = new Date(isoDate)
      const pad = (n) => String(n).padStart(2, '0')
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
    },
    async saveMeeting() {
      if (!this.activeLead) return
      this.submitting = true
      try {
        await websiteLeadsAPI.updateWorkflow(this.activeLead.id, {
          meeting_status: this.meetingForm.meeting_status,
          meeting_datetime: this.meetingForm.meeting_datetime || null,
          meeting_notes: this.meetingForm.meeting_notes,
          response_status: 'responded'
        })
        toast.success('Meeting update saved')
        this.closeMeetingModal()
        await this.loadInbox()
      } catch (error) {
        console.error('Failed to save meeting update:', error)
        toast.error(error.message || 'Failed to save meeting update')
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}
.summary-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.summary-card .label {
  color: var(--gray-500);
  font-size: 0.8rem;
}
.msg-cell {
  max-width: 320px;
}
.cell-sub {
  font-size: 0.75rem;
  color: var(--gray-500);
}
.detail-card {
  margin-top: 1rem;
}
.full-message {
  white-space: pre-wrap;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
}
.meta {
  margin: 0.25rem 0;
  color: var(--gray-500);
}
.badge-warning {
  background: rgba(245, 158, 11, 0.16);
  color: #d97706;
}
.badge-success {
  background: rgba(34, 197, 94, 0.16);
  color: #15803d;
}
.badge-danger {
  background: rgba(239, 68, 68, 0.16);
  color: #b91c1c;
}
.badge-neutral {
  background: rgba(100, 116, 139, 0.16);
  color: #334155;
}
@media (max-width: 1024px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
