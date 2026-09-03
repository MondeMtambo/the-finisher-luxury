<template>
  <div class="leads-master-page luxury-theme">
    <div class="page-header">
      <div class="header-title-row">
        <h1>VIP Leads Triage</h1>
        <div class="live-badge"><span class="pulse-dot"></span> LIVE SYNC</div>
      </div>
      <p class="page-subtitle">Master Inbox & Lead Qualification Command Center</p>
    </div>

    <!-- Top KPI Dashboard -->
    <div class="kpi-grid">
      <div class="kpi-card" :class="{ active: filter === 'all' }" @click="setFilter('all')">
        <div class="kpi-val">{{ summary.total || 0 }}</div>
        <div class="kpi-lbl">Total Inquiries</div>
      </div>
      <div class="kpi-card" :class="{ active: filter === 'new' }" @click="setFilter('new')">
        <div class="kpi-val text-blue">{{ summary.new || 0 }}</div>
        <div class="kpi-lbl">Unread / New</div>
      </div>
      <div class="kpi-card" :class="{ active: filter === 'responded' }" @click="setFilter('responded')">
        <div class="kpi-val text-amber">{{ summary.responded || 0 }}</div>
        <div class="kpi-lbl">In Conversation</div>
      </div>
      <div class="kpi-card" :class="{ active: filter === 'promoted' }" @click="setFilter('promoted')">
        <div class="kpi-val text-green">{{ summary.promoted || 0 }}</div>
        <div class="kpi-lbl">Promoted Deals</div>
      </div>
    </div>

    <!-- Kanban Board -->
    <div class="kanban-board">
      <div 
        v-for="status in statuses" 
        :key="status.key"
        class="kanban-column"
        @dragover.prevent
        @drop="handleDrop($event, status.key)"
      >
        <div class="column-header">
          <h3>{{ status.title }}</h3>
          <span class="column-count">{{ getLeadsByStatus(status.key).length }}</span>
        </div>
        <div class="column-body">
          <div 
            v-for="lead in getLeadsByStatus(status.key)" 
            :key="lead.id"
            class="lead-kanban-card"
            :class="getCardClass(lead)"
            draggable="true"
            @dragstart="handleDragStart($event, lead)"
            @click="openLeadDetails(lead)"
          >
            <div class="card-badges">
              <span v-if="lead.is_spam_risk" class="badge badge-red">Spam Risk</span>
              <span v-else-if="lead.spam_score >= 20" class="badge badge-green">Hot Lead</span>
            </div>
            <div class="card-title">{{ lead.contact_name }}</div>
            <div class="card-subtitle">{{ lead.contact_email }}</div>
            <div class="card-message">{{ truncate(lead.inbound_message, 80) }}</div>
            <div class="card-footer">
              <span class="time-ago">{{ formatShortDate(lead.inbound_received_at) }}</span>
            </div>
          </div>
          
          <div v-if="getLeadsByStatus(status.key).length === 0" class="empty-column">
            Drop leads here
          </div>
        </div>
      </div>
    </div>

    <!-- Lead Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-panel modal-lg">
        <div class="modal-header">
          <h3>{{ activeLead?.contact_name }}</h3>
          <button class="modal-close" @click="closeDetailsModal">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-contact-info" style="margin-bottom: 1.5rem; color: #9ca3af; display: flex; gap: 1rem;">
              <span>📧 {{ activeLead?.contact_email }}</span>
              <span v-if="activeLead?.contact_phone">📱 {{ activeLead?.contact_phone }}</span>
          </div>
          
          <div class="detail-quality" style="margin-bottom: 1.5rem; display: flex; gap: 1rem;">
              <span v-if="activeLead?.is_spam_risk" class="quality-flag flag-red">🔴 Bullshit Filter Flag (Score: {{ activeLead?.spam_score }})</span>
              <span v-else-if="activeLead?.spam_score >= 20" class="quality-flag flag-green">🟢 High Quality Lead (Score: {{ activeLead?.spam_score }})</span>
              <span v-else class="quality-flag flag-yellow">🟡 Standard Lead (Score: {{ activeLead?.spam_score }})</span>
          </div>

          <div class="detail-message-box" style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.1); margin-bottom: 1.5rem;">
            <h4 style="margin-top: 0; color: #D4AF37; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">Message</h4>
            <p style="white-space: pre-wrap; color: #e5e7eb; line-height: 1.6; margin-bottom: 0;">{{ activeLead?.inbound_message || "No message provided." }}</p>
          </div>

          <div class="audit-trail">
            <h4 style="margin-top: 0; color: #D4AF37; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">Audit Trail</h4>
            <ul style="list-style: none; padding: 0; margin: 0; color: #d1d5db; font-size: 0.875rem;">
              <li style="margin-bottom: 0.5rem;">• <strong>Received:</strong> {{ formatFullDate(activeLead?.inbound_received_at) }}</li>
              <li v-if="activeLead?.handled_by_username" style="margin-bottom: 0.5rem;">• <strong>Last Handled By:</strong> {{ activeLead?.handled_by_username }}</li>
              <li v-if="activeLead?.response_status === 'promoted'">• <strong>Status:</strong> Promoted to Deal</li>
            </ul>
          </div>
        </div>
        <div class="modal-footer" style="display: flex; gap: 1rem; justify-content: flex-end; align-items: center;">
          <button class="btn btn-secondary" @click="openReplyModal" style="color: #fff; border-color: rgba(255,255,255,0.2);">
            ✉️ Reply
          </button>
          <button class="btn btn-danger" @click="markAsSpam(activeLead)" v-if="activeLead?.response_status !== 'closed'">
            🗑️ Reject
          </button>
          <button class="btn btn-primary" @click="promoteToDeal(activeLead)" v-if="activeLead?.response_status !== 'promoted'" style="margin-left: auto;">
            🚀 PROMOTE TO DEAL
          </button>
        </div>
      </div>
    </div>

    <!-- Reply Modal -->
    <div v-if="showReplyModal" class="modal-overlay" @click.self="closeReplyModal">
      <div class="modal-panel">
        <div class="modal-header">
          <h3>Reply to {{ activeLead?.contact_name }}</h3>
          <button class="modal-close" @click="closeReplyModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Subject</label>
            <input v-model="replyForm.subject" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Message</label>
            <textarea v-model="replyForm.message" class="form-input code-area" rows="8"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeReplyModal">Cancel</button>
          <button class="btn btn-primary" @click="sendReply" :disabled="submitting">
            {{ submitting ? 'Sending...' : 'Send Reply' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'WebsiteLeads',
  data() {
    return {
      leads: [],
      summary: {},
      filter: 'all',
      activeLead: null,
      showDetailsModal: false,
      showReplyModal: false,
      submitting: false,
      draggingLeadId: null,
      replyForm: {
        subject: '',
        message: ''
      },
      pollingInterval: null,
      statuses: [
        { key: 'new', title: 'New Inquiries' },
        { key: 'responded', title: 'In Conversation' },
        { key: 'promoted', title: 'Promoted to Deal' },
        { key: 'closed', title: 'Rejected / Spam' },
      ]
    }
  },
  computed: {
    apiBase() {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      return isLocal ? 'http://localhost:8000/api' : 'https://the-finisher-luxury-api.onrender.com/api';
    },
    token() {
      return localStorage.getItem('thefinisher_access_token');
    }
  },
  async mounted() {
    await this.loadInbox();
    
    // The "Live Engine" - silently checks for new leads every 5 seconds
    this.pollingInterval = setInterval(() => {
      this.loadInbox(true);
    }, 8000);
  },
  beforeUnmount() {
    if (this.pollingInterval) clearInterval(this.pollingInterval);
  },
  methods: {
    async fetchApi(endpoint, options = {}) {
      const url = `${this.apiBase}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
        ...options.headers
      };
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || err.detail || 'API request failed');
      }
      return response.json();
    },
    setFilter(status) {
      this.filter = status;
      this.loadInbox();
    },
    async loadInbox(silent = false) {
      try {
        let endpoint = '/admin/website-leads/inbox/';
        if (this.filter !== 'all') {
          endpoint += `?status=${this.filter}`;
        }
        const data = await this.fetchApi(endpoint);
        this.summary = data.summary || {};
        this.leads = data.results || [];
        
        // Update active lead data dynamically if they are viewing the modal
        if (this.activeLead && !this.leads.find(l => l.id === this.activeLead.id)) {
            this.activeLead = null;
            this.showDetailsModal = false;
        } else if (this.activeLead) {
            this.activeLead = this.leads.find(l => l.id === this.activeLead.id);
        }
      } catch (error) {
        console.error('Failed to load inbox:', error);
      }
    },
    openLeadDetails(lead) {
      this.activeLead = lead;
      this.showDetailsModal = true;
    },
    closeDetailsModal() {
      this.showDetailsModal = false;
      this.activeLead = null;
    },
    openReplyModal() {
      if (!this.activeLead) return;
      this.showDetailsModal = false;
      this.replyForm.subject = `Re: Your inquiry to Mtambo Holdings`;
      this.replyForm.message = `Hi ${this.activeLead.contact_name},\n\nThank you for your inquiry.\n\nBest regards,\nMtambo Holdings Team`;
      this.showReplyModal = true;
    },
    closeReplyModal() {
      this.showReplyModal = false;
    },
    async sendReply() {
      if (!this.activeLead) return;
      this.submitting = true;
      try {
        await this.fetchApi(`/website-leads/${this.activeLead.id}/reply/`, {
          method: 'POST',
          body: JSON.stringify(this.replyForm)
        });
        this.closeReplyModal();
        await this.loadInbox();
        this.dispatchEvent('show-toast', { message: 'Reply sent successfully!', type: 'success' });
      } catch (error) {
        this.dispatchEvent('show-toast', { message: error.message, type: 'error' });
      } finally {
        this.submitting = false;
      }
    },
    async updateLeadStatus(leadId, newStatus) {
        try {
            await this.fetchApi(`/website-leads/${leadId}/update_workflow/`, {
                method: 'POST',
                body: JSON.stringify({ response_status: newStatus })
            });
            await this.loadInbox(true);
        } catch (error) {
            this.dispatchEvent('show-toast', { message: `Failed to move lead: ${error.message}`, type: 'error' });
        }
    },
    async markAsSpam(lead) {
      if (!confirm(`Are you sure you want to mark ${lead.contact_name}'s message as spam/rejected?`)) return;
      await this.updateLeadStatus(lead.id, 'closed');
      this.showDetailsModal = false;
      this.dispatchEvent('show-toast', { message: 'Lead rejected.', type: 'success' });
    },
    async promoteToDeal(lead) {
      if (!confirm(`Promote ${lead.contact_name} to your Deal Pipeline?`)) return;
      
      try {
        await this.fetchApi(`/website-leads/${lead.id}/promote_to_deal/`, {
          method: 'POST',
          body: JSON.stringify({
            title: `Website Lead: ${lead.contact_name}`,
            value: 0
          })
        });
        this.showDetailsModal = false;
        await this.loadInbox();
        this.dispatchEvent('show-toast', { message: '🚀 Lead successfully promoted to Deal!', type: 'success' });
      } catch (error) {
        this.dispatchEvent('show-toast', { message: error.message, type: 'error' });
      }
    },
    handleDragStart(event, lead) {
        event.dataTransfer.setData('leadId', lead.id);
        this.draggingLeadId = lead.id;
    },
    async handleDrop(event, newStatus) {
        const leadId = parseInt(event.dataTransfer.getData('leadId'), 10);
        this.draggingLeadId = null;
        if (!leadId) return;

        const lead = this.leads.find(l => l.id === leadId);
        if (!lead || lead.response_status === newStatus) return;

        if (newStatus === 'promoted') {
            await this.promoteToDeal(lead);
        } else {
            await this.updateLeadStatus(leadId, newStatus);
        }
    },
    getLeadsByStatus(status) {
        return this.leads.filter(lead => lead.response_status === status);
    },
    getCardClass(lead) {
        if (lead.is_spam_risk) return 'spam-risk';
        if (lead.spam_score >= 20) return 'hot-lead';
        return 'standard-lead';
    },
    formatShortDate(dateStr) {
      if (!dateStr) return '';
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-ZA', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    },
    formatFullDate(dateStr) {
      if (!dateStr) return '';
      const d = new Date(dateStr);
      return d.toLocaleString('en-ZA');
    },
    truncate(text, length) {
      if (!text) return '';
      return text.length > length ? text.substring(0, length) + '...' : text;
    },
    dispatchEvent(name, detail) {
      window.dispatchEvent(new CustomEvent(name, { detail }));
    }
  }
}
</script>

<style scoped>
.luxury-theme {
  color: #fff;
}

.leads-master-page {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.live-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  color: #D4AF37;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: #D4AF37;
  border-radius: 50%;
  animation: pulse-animation 1.5s infinite;
}

@keyframes pulse-animation {
  0% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(212, 175, 55, 0); }
  100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }
}

.page-header h1 {
  font-size: 1.875rem;
  color: #D4AF37;
  margin: 0 0 0.5rem 0;
}
.page-subtitle {
  color: #9ca3af;
  font-size: 0.9375rem;
  margin: 0 0 2rem 0;
}

/* KPI Dashboard */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}
.kpi-card {
  background: linear-gradient(135deg, rgba(20,20,20,0.95) 0%, rgba(10,10,10,0.95) 100%);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}
.kpi-card:hover, .kpi-card.active {
  transform: translateY(-2px);
  border-color: #D4AF37;
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.15);
}
.kpi-val {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #fff;
}
.kpi-lbl {
  font-size: 0.875rem;
  color: #a0aec0;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.text-blue { color: #60a5fa !important; }
.text-amber { color: #fbbf24 !important; }
.text-green { color: #34d399 !important; }

/* Kanban Board */
.kanban-board {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.kanban-column {
  background: rgba(10, 10, 10, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
}

.column-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.column-header h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.column-count {
  background: rgba(212, 175, 55, 0.1);
  color: #D4AF37;
  padding: 0.125rem 0.5rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
}

.column-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 60vh;
}

.empty-column {
  padding: 2rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.2);
  border: 2px dashed rgba(212, 175, 55, 0.2);
  border-radius: var(--radius-md);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 0.8125rem;
}

.lead-kanban-card {
  background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
  border-left: 3px solid rgba(212, 175, 55, 0.3);
  padding: 1rem;
  border-radius: var(--radius-md);
  box-shadow: 0 5px 15px rgba(0,0,0,0.4);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  position: relative;
}
.lead-kanban-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.6);
}
.lead-kanban-card.hot-lead { border-left-color: #D4AF37; }
.lead-kanban-card.hot-lead:hover { box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2); }
.lead-kanban-card.spam-risk { border-left-color: #ef4444; }
.lead-kanban-card.spam-risk:hover { box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2); }

.card-title { font-weight: 600; color: #fff; margin-bottom: 0.25rem; font-size: 0.9375rem; }
.card-subtitle { font-size: 0.8125rem; color: #9ca3af; margin-bottom: 0.75rem; }
.card-message { font-size: 0.875rem; color: #d1d5db; line-height: 1.5; margin-bottom: 0.75rem; }
.card-footer { font-size: 0.75rem; color: #718096; }
.card-badges { position: absolute; top: 0.75rem; right: 0.75rem; display: flex; gap: 0.5rem; }

.quality-flag {
  font-size: 0.8125rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
}
.flag-green { background: #d1fae5; color: #065f46; }
.flag-red { background: #fee2e2; color: #991b1b; }
.flag-yellow { background: #fef3c7; color: #92400e; }
</style>