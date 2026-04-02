<template>
  <div class="leads-master-page">
    <div class="page-header">
      <div>
        <h1>VIP Leads Triage</h1>
        <p class="page-subtitle">Master Inbox & Lead Qualification Command Center</p>
      </div>
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

    <!-- The Split-Screen "Inbox" Design -->
    <div class="triage-container">
      
      <!-- Left Panel (The List) -->
      <div class="inbox-panel">
        <div class="inbox-feed">
          <div v-if="leads.length === 0" class="empty-feed">
            <p>No leads found in this queue.</p>
          </div>
          
          <div 
            v-for="lead in leads" 
            :key="lead.id"
            class="lead-card"
            :class="{ active: activeLead && activeLead.id === lead.id }"
            @click="activeLead = lead"
          >
            <div class="lead-card-header">
              <strong>{{ lead.contact_name }}</strong>
              <span class="time-ago">{{ formatShortDate(lead.inbound_received_at) }}</span>
            </div>
            <div class="lead-email">{{ lead.contact_email }}</div>
            
            <div class="lead-badges">
              <span v-if="lead.is_spam_risk" class="badge badge-red">🔴 Spam Risk</span>
              <span v-else-if="lead.spam_score >= 20" class="badge badge-green">🟢 Hot Lead</span>
              <span v-else class="badge badge-yellow">🟡 Standard</span>
              
              <span v-if="lead.response_status === 'new'" class="badge badge-blue">New</span>
              <span v-if="lead.response_status === 'promoted'" class="badge badge-green">Promoted</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel (The Detail View) -->
      <div class="detail-panel">
        <div v-if="!activeLead" class="empty-detail">
          <svg width="48" height="48" fill="none" stroke="var(--gray-500)" stroke-width="1.5"><rect x="3" y="3" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
          <h3>Select a lead to view details</h3>
        </div>
        
        <div v-else class="lead-detail-content">
          <div class="detail-header">
            <h2>{{ activeLead.contact_name }}</h2>
            <div class="detail-contact-info">
              <span>📧 {{ activeLead.contact_email }}</span>
              <span v-if="activeLead.contact_phone">📱 {{ activeLead.contact_phone }}</span>
            </div>
            <div class="detail-quality">
              <span v-if="activeLead.is_spam_risk" class="quality-flag flag-red">🔴 Flagged by Bullshit Filter (Score: {{ activeLead.spam_score }})</span>
              <span v-else-if="activeLead.spam_score >= 20" class="quality-flag flag-green">🟢 High Quality Lead (Score: {{ activeLead.spam_score }})</span>
              <span v-else class="quality-flag flag-yellow">🟡 Standard Lead (Score: {{ activeLead.spam_score }})</span>
            </div>
          </div>

          <div class="detail-message-box">
            <h4>Message</h4>
            <div class="message-body">
              <p>{{ activeLead.inbound_message || "No message provided." }}</p>
            </div>
          </div>

          <div class="audit-trail">
            <h4>Activity Audit Trail</h4>
            <ul>
              <li><strong>Received:</strong> {{ formatFullDate(activeLead.inbound_received_at) }} via {{ activeLead.source }}</li>
              <li v-if="activeLead.handled_by_username"><strong>Last Handled By:</strong> {{ activeLead.handled_by_username }}</li>
              <li v-if="activeLead.responded_at"><strong>Replied:</strong> {{ formatFullDate(activeLead.responded_at) }}</li>
              <li v-if="activeLead.response_status === 'promoted'"><strong>Status:</strong> Successfully Promoted to Deal</li>
            </ul>
          </div>

          <!-- 1-Click Actions -->
          <div class="detail-actions" v-if="activeLead.response_status !== 'promoted'">
            <button class="action-btn btn-engage" @click="openReplyModal">
              ✉️ Reply / Engage
            </button>
            <button class="action-btn btn-reject" @click="markAsSpam(activeLead)">
              🗑️ Reject / Spam
            </button>
            <button class="action-btn btn-promote" @click="promoteToDeal(activeLead)">
              🚀 PROMOTE TO DEAL
            </button>
          </div>
          <div class="detail-actions" v-else>
            <div class="promoted-alert">✅ This lead has been successfully promoted to your Deal Pipeline.</div>
          </div>

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
      showReplyModal: false,
      submitting: false,
      replyForm: {
        subject: '',
        message: ''
      }
    }
  },
  computed: {
    apiBase() {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      return isLocal ? 'http://localhost:8000/api' : 'https://the-finisher-luxury-be.fly.dev/api';
    },
    token() {
      return localStorage.getItem('thefinisher_access_token');
    }
  },
  async mounted() {
    await this.loadInbox();
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
    async loadInbox() {
      try {
        let endpoint = '/admin/website-leads/inbox/';
        if (this.filter !== 'all') {
          endpoint += `?status=${this.filter}`;
        }
        const data = await this.fetchApi(endpoint);
        this.summary = data.summary || {};
        this.leads = data.results || [];
        
        // Auto-select first lead if none selected
        if (this.leads.length > 0) {
          if (!this.activeLead || !this.leads.find(l => l.id === this.activeLead.id)) {
            this.activeLead = this.leads[0];
          }
        } else {
          this.activeLead = null;
        }
      } catch (error) {
        console.error('Failed to load inbox:', error);
      }
    },
    openReplyModal() {
      if (!this.activeLead) return;
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
    async markAsSpam(lead) {
      if (!confirm(`Are you sure you want to mark ${lead.contact_name}'s message as spam/rejected?`)) return;
      
      try {
        await this.fetchApi(`/website-leads/${lead.id}/update_workflow/`, {
          method: 'POST',
          body: JSON.stringify({ response_status: 'closed' })
        });
        await this.loadInbox();
        this.dispatchEvent('show-toast', { message: 'Lead rejected.', type: 'success' });
      } catch (error) {
        this.dispatchEvent('show-toast', { message: error.message, type: 'error' });
      }
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
        await this.loadInbox();
        this.dispatchEvent('show-toast', { message: '🚀 Lead successfully promoted to Deal!', type: 'success' });
      } catch (error) {
        this.dispatchEvent('show-toast', { message: error.message, type: 'error' });
      }
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
.leads-master-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header h1 {
  font-size: 1.875rem;
  color: var(--gray-900);
  margin: 0 0 0.5rem 0;
}
.page-subtitle {
  color: var(--gray-500);
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
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}
.kpi-card:hover, .kpi-card.active {
  transform: translateY(-2px);
  border-color: var(--primary-500);
  box-shadow: var(--shadow-md);
}
.kpi-val {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--gray-900);
}
.kpi-lbl {
  font-size: 0.875rem;
  color: var(--gray-500);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.text-blue { color: var(--blue-600); }
.text-amber { color: var(--amber-600); }
.text-green { color: var(--green-600); }

/* Split Screen */
.triage-container {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 1.5rem;
  height: 65vh;
  min-height: 600px;
}

/* Left Panel (Inbox) */
.inbox-panel {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.inbox-feed {
  flex: 1;
  overflow-y: auto;
}
.empty-feed {
  padding: 2rem;
  text-align: center;
  color: var(--gray-500);
}
.lead-card {
  padding: 1.25rem;
  border-bottom: 1px solid var(--gray-100);
  cursor: pointer;
  transition: background 0.2s;
}
.lead-card:hover {
  background: var(--gray-50);
}
.lead-card.active {
  background: var(--blue-50);
  border-left: 4px solid var(--primary-500);
}
.lead-card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
  font-size: 0.9375rem;
}
.time-ago {
  font-size: 0.75rem;
  color: var(--gray-500);
}
.lead-email {
  font-size: 0.8125rem;
  color: var(--gray-600);
  margin-bottom: 0.5rem;
}
.lead-preview {
  font-size: 0.8125rem;
  color: var(--gray-700);
  line-height: 1.4;
  margin-bottom: 0.75rem;
}
.lead-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Right Panel (Details) */
.detail-panel {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow-y: auto;
  box-shadow: var(--shadow-sm);
}
.empty-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--gray-400);
}
.empty-detail h3 {
  margin-top: 1rem;
  font-weight: 500;
}
.lead-detail-content {
  padding: 2rem;
}
.detail-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
}
.detail-header h2 {
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  color: var(--gray-900);
}
.detail-contact-info {
  display: flex;
  gap: 1.5rem;
  color: var(--gray-600);
  font-size: 0.9375rem;
  margin-bottom: 1rem;
}
.detail-quality {
  display: flex;
  gap: 1rem;
}
.quality-flag {
  font-size: 0.8125rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
}
.flag-green { background: #d1fae5; color: #065f46; }
.flag-red { background: #fee2e2; color: #991b1b; }
.flag-yellow { background: #fef3c7; color: #92400e; }

.detail-message-box {
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--gray-200);
}
.detail-message-box h4 {
  margin: 0 0 1rem 0;
  color: var(--gray-700);
  font-size: 0.875rem;
  text-transform: uppercase;
}
.message-body {
  white-space: pre-wrap;
  color: var(--gray-800);
  line-height: 1.6;
}

.audit-trail {
  margin-bottom: 2.5rem;
}
.audit-trail h4 {
  margin: 0 0 1rem 0;
  color: var(--gray-700);
  font-size: 0.875rem;
  text-transform: uppercase;
}
.audit-trail ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.audit-trail li {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}
.audit-trail li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--primary-500);
}

.detail-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}
.action-btn {
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  cursor: pointer;
  border: none;
  font-size: 0.9375rem;
  transition: all 0.2s;
}
.btn-engage {
  background: var(--blue-50);
  color: var(--blue-700);
}
.btn-engage:hover { background: var(--blue-100); }

.btn-reject {
  background: var(--red-50);
  color: var(--red-700);
}
.btn-reject:hover { background: var(--red-100); }

.btn-promote {
  background: var(--primary-500);
  color: white;
  flex: 1;
  box-shadow: 0 4px 6px rgba(212, 175, 55, 0.2);
}
.btn-promote:hover {
  background: var(--primary-600);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(212, 175, 55, 0.3);
}

.promoted-alert {
  width: 100%;
  padding: 1rem;
  background: #ecfdf5;
  color: #065f46;
  border-radius: var(--radius-md);
  text-align: center;
  font-weight: 600;
  border: 1px solid #a7f3d0;
}
</style>