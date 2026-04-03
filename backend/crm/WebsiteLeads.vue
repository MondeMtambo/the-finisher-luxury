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
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="rgba(212, 175, 55, 0.5)" stroke-width="1">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
          </div>
          <h3>Select an inquiry</h3>
          <p>Your luxury command center awaits.</p>
        </div>
        
        <template v-else>
          <div class="detail-scroll-area">
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
          </div>

          <!-- Fixed Action Footer -->
          <div class="detail-footer" v-if="activeLead.response_status !== 'promoted'">
            <button class="action-btn btn-engage" @click="openReplyModal" title="Reply to Inquiry">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
              Reply
            </button>
            <button class="action-btn btn-reject" @click="markAsSpam(activeLead)" title="Mark as Spam">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
              Reject
            </button>
            <button class="action-btn btn-promote" @click="promoteToDeal(activeLead)">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13.5 2L22 10.5l-9.5 9.5a2.12 2.12 0 0 1-3 0l-7.5-7.5a2.12 2.12 0 0 1 0-3L11.5 2z"></path><path d="M12 12l4-4"></path></svg>
              PROMOTE TO DEAL
            </button>
          </div>
          <div class="detail-footer promoted-footer" v-else>
            <div class="promoted-alert">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
              This lead has been successfully promoted to your Deal Pipeline.
            </div>
          </div>
        </template>
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
      },
      pollingInterval: null
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
    
    // The "Live Engine" - silently checks for new leads every 5 seconds
    this.pollingInterval = setInterval(() => {
      this.loadInbox(true);
    }, 5000);
  },
  beforeUnmount() {
    // Clean up the engine when you leave the page
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
        
        // Smoothly maintain the active lead without flickering
        if (this.activeLead) {
          const stillExists = this.leads.find(l => l.id === this.activeLead.id);
          if (stillExists) this.activeLead = stillExists;
          else if (!silent && this.leads.length > 0) this.activeLead = this.leads[0];
          else if (!silent) this.activeLead = null;
        } else if (this.leads.length > 0 && !silent) {
          this.activeLead = this.leads[0];
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
.luxury-theme {
  color: #fff;
}

.leads-master-page {
  padding: 2rem;
  max-width: 1400px;
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
  background: linear-gradient(135deg, rgba(15,15,15,0.95) 0%, rgba(5,5,5,0.95) 100%);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}
.kpi-card:hover, .kpi-card.active {
  transform: translateY(-4px);
  border-color: #D4AF37;
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2);
}
.kpi-val {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #ffffff;
}
.kpi-lbl {
  font-size: 0.875rem;
  color: #9ca3af;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.text-blue { color: #60a5fa !important; }
.text-amber { color: #fbbf24 !important; }
.text-green { color: #34d399 !important; }

/* Split Screen */
.triage-container {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 1.5rem;
  height: calc(100vh - 280px);
  min-height: 600px;
}

/* Left Panel (Inbox) */
.inbox-panel {
  background: linear-gradient(135deg, rgba(15,15,15,0.95) 0%, rgba(5,5,5,0.95) 100%);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
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
  border-bottom: 1px solid rgba(212, 175, 55, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  background: transparent;
}
.lead-card:hover {
  background: rgba(212, 175, 55, 0.05);
}
.lead-card.active {
  background: rgba(212, 175, 55, 0.15);
  border-left: 4px solid #D4AF37;
}
.lead-card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
  font-size: 0.9375rem;
  color: #ffffff;
}
.time-ago {
  font-size: 0.75rem;
  color: var(--gray-500);
}
.lead-email {
  font-size: 0.8125rem;
  color: #9ca3af;
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
  background: linear-gradient(135deg, rgba(15,15,15,0.95) 0%, rgba(5,5,5,0.95) 100%);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  color: #ffffff;
}
.empty-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--gray-400);
}
.empty-icon {
  margin-bottom: 1.5rem;
  animation: float 4s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.empty-detail h3 {
  font-size: 1.5rem;
  color: #D4AF37;
  margin-bottom: 0.5rem;
}
.empty-detail p {
  color: #9ca3af;
}
.detail-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 2.5rem;
}
.detail-header {
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
  padding-bottom: 1.25rem;
  margin-bottom: 1.5rem;
}
.detail-header h2 {
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  color: #D4AF37;
}
.detail-contact-info {
  display: flex;
  gap: 1.5rem;
  color: #d1d5db;
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
  background: rgba(0, 0, 0, 0.5);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(212, 175, 55, 0.1);
}
.detail-message-box h4 {
  margin: 0 0 1rem 0;
  color: #D4AF37;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.message-body {
  white-space: pre-wrap;
  color: #e5e7eb;
  line-height: 1.6;
}

.audit-trail {
  margin-bottom: 2.5rem;
}
.audit-trail h4 {
  margin: 0 0 1rem 0;
  color: #D4AF37;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.audit-trail ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.audit-trail li {
  font-size: 0.875rem;
  color: #d1d5db;
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}
.audit-trail li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #D4AF37;
}

.detail-footer {
  padding: 1.5rem 2.5rem;
  background: rgba(0, 0, 0, 0.4);
  border-top: 1px solid rgba(212, 175, 55, 0.15);
  display: flex;
  gap: 1rem;
  align-items: center;
}
.promoted-footer {
  justify-content: center;
}
.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: none;
}
.btn-engage {
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.btn-engage:hover { 
  background: rgba(255, 255, 255, 0.1); 
  border-color: #D4AF37;
  color: #D4AF37;
}

.btn-reject {
  background: rgba(239, 68, 68, 0.05);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}
.btn-reject:hover { 
  background: rgba(239, 68, 68, 0.15); 
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
}

.btn-promote {
  background: linear-gradient(135deg, #D4AF37 0%, #AA8010 100%);
  color: #000;
  margin-left: auto;
  font-size: 1rem;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
}
.btn-promote:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
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