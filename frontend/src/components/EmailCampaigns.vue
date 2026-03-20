<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Email Campaigns</h1>
        <p class="page-subtitle">Create and track email campaigns to your contacts</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-secondary" @click="activeTab = 'templates'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          Templates
        </button>
        <button class="btn btn-primary" @click="openNewCampaign">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          New Campaign
        </button>
      </div>
    </div>

    <div class="tabs">
      <button :class="['tab', activeTab === 'campaigns' && 'active']" @click="activeTab = 'campaigns'">Campaigns</button>
      <button :class="['tab', activeTab === 'templates' && 'active']" @click="activeTab = 'templates'">Templates</button>
    </div>

    <div v-if="activeTab === 'campaigns'">
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-value">{{ campaigns.length }}</div>
          <div class="stat-label">Total Campaigns</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ totalSent }}</div>
          <div class="stat-label">Emails Sent</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ avgOpenRate }}%</div>
          <div class="stat-label">Avg Open Rate</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ avgClickRate }}%</div>
          <div class="stat-label">Avg Click Rate</div>
        </div>
      </div>

      <div v-if="!loading" class="campaigns-grid">
        <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-card card">
          <div class="campaign-header">
            <h3>{{ campaign.name }}</h3>
            <span :class="['badge', statusBadge(campaign.status)]">{{ campaign.status }}</span>
          </div>
          <p class="campaign-subject">{{ campaign.subject }}</p>
          <div class="campaign-stats">
            <div class="cs-item">
              <span class="cs-val">{{ campaign.total_recipients }}</span>
              <span class="cs-lbl">Recipients</span>
            </div>
            <div class="cs-item">
              <span class="cs-val">{{ campaign.sent_count }}</span>
              <span class="cs-lbl">Sent</span>
            </div>
            <div class="cs-item">
              <span class="cs-val">{{ campaign.open_count }}</span>
              <span class="cs-lbl">Opens</span>
            </div>
            <div class="cs-item">
              <span class="cs-val">{{ campaign.click_count }}</span>
              <span class="cs-lbl">Clicks</span>
            </div>
          </div>
          <div class="campaign-bar">
            <div class="bar-fill bar-sent" :style="{ width: barWidth(campaign.sent_count, campaign.total_recipients) }"></div>
            <div class="bar-fill bar-opened" :style="{ width: barWidth(campaign.open_count, campaign.total_recipients) }"></div>
          </div>
          <div class="campaign-actions">
            <button v-if="campaign.status === 'draft'" class="btn btn-sm btn-primary" @click="sendCampaign(campaign)">Send</button>
            <button class="btn btn-sm btn-secondary" @click="editCampaign(campaign)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteCampaign(campaign)">Delete</button>
          </div>
          <div class="campaign-date">Created {{ formatDate(campaign.created_at) }}</div>
        </div>

        <div v-if="campaigns.length === 0" class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          <h3>No campaigns yet</h3>
          <p>Create your first email campaign to reach your contacts</p>
          <button class="btn btn-primary" @click="openNewCampaign">Create Campaign</button>
        </div>
      </div>

      <div v-else class="loading-state"><div class="spinner"></div><p>Loading campaigns...</p></div>
    </div>

    <div v-if="activeTab === 'templates'">
      <div class="templates-header">
        <h2>Email Templates</h2>
        <button class="btn btn-primary" @click="openNewTemplate">Add Template</button>
      </div>
      <div class="templates-grid">
        <div v-for="tmpl in templates" :key="tmpl.id" class="template-card card">
          <div class="tmpl-type-badge">{{ tmpl.template_type }}</div>
          <h4>{{ tmpl.name }}</h4>
          <p class="tmpl-subject">Subject: {{ tmpl.subject }}</p>
          <div class="tmpl-actions">
            <button class="btn btn-sm btn-secondary" @click="editTemplate(tmpl)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteTemplate(tmpl)">Delete</button>
          </div>
        </div>
        <div v-if="templates.length === 0" class="empty-state">
          <p>No templates yet. Create reusable templates to speed up campaign creation.</p>
          <button class="btn btn-primary" @click="openNewTemplate">Create Template</button>
        </div>
      </div>
    </div>

    <div v-if="showCampaignModal" class="modal-overlay" @click="showCampaignModal = false">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ editingCampaign ? 'Edit Campaign' : 'New Campaign' }}</h3>
          <button class="modal-close" @click="showCampaignModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveCampaign">
            <div class="form-group">
              <label class="form-label">Campaign Name *</label>
              <input class="form-input" v-model="campaignForm.name" required placeholder="e.g. Q1 Newsletter">
            </div>
            <div class="form-group">
              <label class="form-label">Subject Line *</label>
              <input class="form-input" v-model="campaignForm.subject" required placeholder="Email subject line">
            </div>
            <div class="form-group">
              <label class="form-label">Template (optional)</label>
              <select class="form-input" v-model="campaignForm.template" @change="applyTemplate">
                <option :value="null">— No template —</option>
                <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Email Body (HTML) *</label>
              <textarea class="form-input code-area" v-model="campaignForm.body_html" rows="10" required
                placeholder="<h1>Hello {{first_name}},</h1><p>Your email content here...</p>"></textarea>
              <small class="form-hint">Merge fields: <code>{{first_name}}</code>, <code>{{last_name}}</code>, <code>{{company}}</code>, <code>{{email}}</code></small>
            </div>
            <div class="form-group">
              <label class="form-label">Recipients</label>
              <div class="recipient-selector">
                <label class="radio-opt">
                  <input type="radio" v-model="recipientMode" value="all"> All Contacts
                </label>
                <label class="radio-opt">
                  <input type="radio" v-model="recipientMode" value="select"> Select Contacts
                </label>
              </div>
              <div v-if="recipientMode === 'select'" class="contacts-checklist">
                <div v-for="contact in contacts" :key="contact.id" class="contact-check">
                  <label>
                    <input type="checkbox" :value="contact.id" v-model="campaignForm.recipient_ids">
                    {{ contact.first_name }} {{ contact.last_name }} ({{ contact.email }})
                  </label>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="showCampaignModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Saving...' : 'Save Campaign' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showTemplateModal" class="modal-overlay" @click="showTemplateModal = false">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ editingTemplate ? 'Edit Template' : 'New Template' }}</h3>
          <button class="modal-close" @click="showTemplateModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveTemplate">
            <div class="form-row">
              <div class="form-group flex-2">
                <label class="form-label">Template Name *</label>
                <input class="form-input" v-model="templateForm.name" required>
              </div>
              <div class="form-group flex-1">
                <label class="form-label">Type</label>
                <select class="form-input" v-model="templateForm.template_type">
                  <option value="welcome">Welcome</option>
                  <option value="follow_up">Follow-Up</option>
                  <option value="proposal">Proposal</option>
                  <option value="thank_you">Thank You</option>
                  <option value="newsletter">Newsletter</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Subject *</label>
              <input class="form-input" v-model="templateForm.subject" required>
            </div>
            <div class="form-group">
              <label class="form-label">Body HTML *</label>
              <textarea class="form-input code-area" v-model="templateForm.body_html" rows="12" required></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="showTemplateModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Saving...' : 'Save Template' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { emailCampaignsAPI, emailTemplatesAPI, contactsAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'EmailCampaigns',
  data() {
    return {
      activeTab: 'campaigns',
      campaigns: [],
      templates: [],
      contacts: [],
      loading: true,
      saving: false,
      showCampaignModal: false,
      showTemplateModal: false,
      editingCampaign: null,
      editingTemplate: null,
      recipientMode: 'all',
      campaignForm: this.emptyCampaignForm(),
      templateForm: this.emptyTemplateForm()
    }
  },
  computed: {
    totalSent() { return this.campaigns.reduce((s, c) => s + (c.sent_count || 0), 0) },
    avgOpenRate() {
      const sent = this.campaigns.filter(c => c.sent_count > 0)
      if (!sent.length) return 0
      const rate = sent.reduce((s, c) => s + (c.open_count / c.sent_count * 100), 0) / sent.length
      return rate.toFixed(1)
    },
    avgClickRate() {
      const sent = this.campaigns.filter(c => c.sent_count > 0)
      if (!sent.length) return 0
      const rate = sent.reduce((s, c) => s + (c.click_count / c.sent_count * 100), 0) / sent.length
      return rate.toFixed(1)
    }
  },
  mounted() {
    this.fetchAll()
  },
  methods: {
    emptyCampaignForm() {
      return { name: '', subject: '', body_html: '', template: null, recipient_ids: [], recipient_filter: {} }
    },
    emptyTemplateForm() {
      return { name: '', template_type: 'custom', subject: '', body_html: '' }
    },
    statusBadge(status) {
      const map = { draft: 'badge-gray', scheduled: 'badge-blue', sending: 'badge-yellow', sent: 'badge-green', paused: 'badge-yellow', failed: 'badge-red' }
      return map[status] || 'badge-gray'
    },
    barWidth(val, total) {
      return total > 0 ? (val / total * 100) + '%' : '0%'
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-ZA', { day: 'numeric', month: 'short', year: 'numeric' })
    },
    async fetchAll() {
      this.loading = true
      try {
        const [campRes, tmplRes, contRes] = await Promise.all([
          emailCampaignsAPI.getAll(),
          emailTemplatesAPI.getAll(),
          contactsAPI.getAll()
        ])
        this.campaigns = campRes.data.results || campRes.data || []
        this.templates = tmplRes.data.results || tmplRes.data || []
        this.contacts = contRes.data.results || contRes.data || []
      } catch (e) {
        toast.error('Failed to load campaign data')
      } finally {
        this.loading = false
      }
    },
    openNewCampaign() {
      this.campaignForm = this.emptyCampaignForm()
      this.recipientMode = 'all'
      this.editingCampaign = null
      this.showCampaignModal = true
    },
    editCampaign(c) {
      this.campaignForm = {
        name: c.name, subject: c.subject, body_html: c.body_html,
        template: c.template, recipient_ids: c.recipient_ids || [],
        recipient_filter: c.recipient_filter || {}
      }
      this.recipientMode = (c.recipient_ids && c.recipient_ids.length) ? 'select' : 'all'
      this.editingCampaign = c
      this.showCampaignModal = true
    },
    applyTemplate() {
      if (!this.campaignForm.template) return
      const tmpl = this.templates.find(t => t.id === this.campaignForm.template)
      if (tmpl) {
        this.campaignForm.subject = tmpl.subject
        this.campaignForm.body_html = tmpl.body_html
      }
    },
    async saveCampaign() {
      this.saving = true
      try {
        const payload = { ...this.campaignForm }
        if (this.recipientMode === 'all') {
          payload.recipient_ids = this.contacts.map(c => c.id)
          payload.recipient_filter = { all: true }
        }
        if (this.editingCampaign) {
          await emailCampaignsAPI.update(this.editingCampaign.id, payload)
          toast.success('Campaign updated')
        } else {
          await emailCampaignsAPI.create(payload)
          toast.success('Campaign created')
        }
        this.showCampaignModal = false
        this.fetchAll()
      } catch (e) {
        toast.error(e.message || 'Failed to save campaign')
      } finally {
        this.saving = false
      }
    },
    async sendCampaign(campaign) {
      if (!confirm(`Send "${campaign.name}" to ${campaign.total_recipients || 'all'} recipients?`)) return
      try {
        await emailCampaignsAPI.send(campaign.id)
        toast.success('Campaign sent successfully!')
        this.fetchAll()
      } catch (e) {
        toast.error(e.message || 'Failed to send campaign')
      }
    },
    async deleteCampaign(campaign) {
      if (!confirm(`Delete campaign "${campaign.name}"?`)) return
      try {
        await emailCampaignsAPI.delete(campaign.id)
        toast.success('Campaign deleted')
        this.fetchAll()
      } catch (e) {
        toast.error(e.message || 'Failed to delete campaign')
      }
    },
    
    openNewTemplate() {
      this.templateForm = this.emptyTemplateForm()
      this.editingTemplate = null
      this.showTemplateModal = true
    },
    editTemplate(t) {
      this.templateForm = { name: t.name, template_type: t.template_type, subject: t.subject, body_html: t.body_html }
      this.editingTemplate = t
      this.showTemplateModal = true
    },
    async saveTemplate() {
      this.saving = true
      try {
        if (this.editingTemplate) {
          await emailTemplatesAPI.update(this.editingTemplate.id, this.templateForm)
          toast.success('Template updated')
        } else {
          await emailTemplatesAPI.create(this.templateForm)
          toast.success('Template created')
        }
        this.showTemplateModal = false
        this.fetchAll()
      } catch (e) {
        toast.error(e.message || 'Failed to save template')
      } finally {
        this.saving = false
      }
    },
    async deleteTemplate(t) {
      if (!confirm(`Delete template "${t.name}"?`)) return
      try {
        await emailTemplatesAPI.delete(t.id)
        toast.success('Template deleted')
        this.fetchAll()
      } catch (e) {
        toast.error(e.message || 'Failed to delete')
      }
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 24px; max-width: 1400px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.page-header h1 { font-size: 24px; font-weight: 700; color: var(--gray-900, #111); margin: 0; }
.page-subtitle { color: var(--gray-500, #6b7280); font-size: 14px; margin-top: 4px; }
.header-actions { display: flex; gap: 8px; }

.tabs { display: flex; gap: 4px; margin-bottom: 24px; border-bottom: 2px solid var(--border, #e5e7eb); }
.tab { padding: 10px 20px; font-size: 14px; font-weight: 500; background: none; border: none; cursor: pointer; color: var(--gray-500); border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
.tab.active { color: var(--primary, #6366f1); border-bottom-color: var(--primary, #6366f1); }

.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: var(--card-bg, #fff); border: 1px solid var(--border, #e5e7eb); border-radius: 12px; padding: 20px; text-align: center; }
.stat-value { font-size: 28px; font-weight: 700; color: var(--primary, #6366f1); }
.stat-label { font-size: 12px; color: var(--gray-500, #6b7280); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }

.campaigns-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }
.campaign-card { padding: 20px; border-radius: 12px; background: var(--card-bg, #fff); border: 1px solid var(--border, #e5e7eb); }
.campaign-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.campaign-header h3 { font-size: 16px; font-weight: 600; margin: 0; color: var(--gray-900); }
.campaign-subject { font-size: 13px; color: var(--gray-500); margin: 0 0 16px 0; }
.campaign-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; }
.cs-item { text-align: center; }
.cs-val { display: block; font-size: 18px; font-weight: 700; color: var(--gray-900); }
.cs-lbl { font-size: 10px; color: var(--gray-500); text-transform: uppercase; }
.campaign-bar { height: 6px; background: var(--gray-100, #f3f4f6); border-radius: 3px; overflow: hidden; position: relative; margin-bottom: 12px; }
.bar-fill { position: absolute; left: 0; top: 0; height: 100%; border-radius: 3px; }
.bar-sent { background: #93c5fd; }
.bar-opened { background: #6366f1; }
.campaign-actions { display: flex; gap: 6px; margin-bottom: 8px; }
.campaign-date { font-size: 11px; color: var(--gray-400); }

.templates-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.templates-header h2 { font-size: 18px; font-weight: 600; margin: 0; }
.templates-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.template-card { padding: 20px; border-radius: 12px; background: var(--card-bg, #fff); border: 1px solid var(--border, #e5e7eb); }
.template-card h4 { margin: 8px 0 4px; font-size: 15px; }
.tmpl-type-badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; background: #dbeafe; color: #1e40af; text-transform: uppercase; }
.tmpl-subject { font-size: 13px; color: var(--gray-500); margin: 0 0 12px 0; }
.tmpl-actions { display: flex; gap: 6px; }

.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: capitalize; }
.badge-green { background: #dcfce7; color: #166534; }
.badge-yellow { background: #fef9c3; color: #854d0e; }
.badge-red { background: #fee2e2; color: #991b1b; }
.badge-blue { background: #dbeafe; color: #1e40af; }
.badge-gray { background: #f3f4f6; color: #374151; }

.recipient-selector { display: flex; gap: 16px; margin-bottom: 12px; }
.radio-opt { display: flex; align-items: center; gap: 6px; font-size: 14px; cursor: pointer; }
.contacts-checklist { max-height: 200px; overflow-y: auto; border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; }
.contact-check label { display: flex; align-items: center; gap: 8px; padding: 4px 0; font-size: 13px; cursor: pointer; }

.code-area { font-family: 'Fira Code', 'Cascadia Code', monospace; font-size: 13px; }
.form-hint { font-size: 12px; color: var(--gray-500); margin-top: 4px; }
.form-hint code { background: var(--gray-100); padding: 1px 4px; border-radius: 3px; font-size: 11px; }

.empty-state { text-align: center; padding: 60px 20px; color: var(--gray-500); }
.empty-state h3 { color: var(--gray-700); margin: 12px 0 4px; }
.empty-state p { margin-bottom: 16px; }

.btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; border: none; transition: all 0.15s; }
.btn-primary { background: var(--primary, #6366f1); color: #fff; }
.btn-primary:hover { opacity: 0.9; }
.btn-secondary { background: var(--gray-100, #f3f4f6); color: var(--gray-700, #374151); }
.btn-danger { background: #fee2e2; color: #991b1b; }
.btn-sm { padding: 4px 10px; font-size: 12px; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-panel { background: var(--card-bg, #fff); border-radius: 16px; width: 95%; max-width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-lg { max-width: 720px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border, #e5e7eb); }
.modal-header h3 { font-size: 18px; font-weight: 600; margin: 0; }
.modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--gray-400); }
.modal-body { padding: 24px; }
.form-group { margin-bottom: 16px; }
.form-label { display: block; font-size: 13px; font-weight: 500; color: var(--gray-700); margin-bottom: 6px; }
.form-input { width: 100%; padding: 10px 12px; border: 1px solid var(--border, #e5e7eb); border-radius: 8px; font-size: 14px; background: var(--card-bg, #fff); color: var(--gray-900, #111); box-sizing: border-box; }
.form-input:focus { outline: none; border-color: var(--primary, #6366f1); box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.form-row { display: flex; gap: 16px; }
.form-row .form-group { flex: 1; }
.flex-1 { flex: 1; }
.flex-2 { flex: 2; }
.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); }

.loading-state { display: flex; flex-direction: column; align-items: center; padding: 60px; color: var(--gray-500); }
.spinner { width: 32px; height: 32px; border: 3px solid var(--border, #e5e7eb); border-top-color: var(--primary, #6366f1); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .campaigns-grid { grid-template-columns: 1fr; }
  .form-row { flex-direction: column; gap: 0; }
  .header-actions { flex-direction: column; }
}
</style>
