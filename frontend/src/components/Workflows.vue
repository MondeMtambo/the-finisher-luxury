<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Workflow Automation</h1>
        <p class="page-subtitle">Automate actions when events occur in your CRM</p>
      </div>
      <button class="btn btn-primary" @click="openNew">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        New Workflow
      </button>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-value">{{ workflows.length }}</div>
        <div class="stat-label">Workflows</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ activeCount }}</div>
        <div class="stat-label">Active</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ totalRuns }}</div>
        <div class="stat-label">Total Runs</div>
      </div>
    </div>

    <!-- 1-Click Executive Workflow Recipes Banner -->
    <div class="recipes-section">
      <div class="recipes-header">
        <span class="recipe-pill">⚡ 1-CLICK AUTOMATION RECIPES</span>
        <h2 class="recipes-title">Executive Workflow Templates</h2>
        <p class="recipes-sub">Deploy pre-configured, institutional automations in one click to accelerate pipeline velocity and guarantee client retention.</p>
      </div>

      <div class="recipes-grid">
        <div v-for="r in recipes" :key="r.id" class="recipe-card">
          <div class="recipe-top">
            <div class="recipe-icon-wrap">{{ r.icon }}</div>
            <span class="recipe-badge">{{ r.badge }}</span>
          </div>
          <h4 class="recipe-name">{{ r.title }}</h4>
          <p class="recipe-desc">{{ r.description }}</p>
          <div class="recipe-flow">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
            <span>{{ r.flow }}</span>
          </div>
          <div class="recipe-actions">
            <button class="btn btn-sm btn-primary recipe-btn" @click="installRecipe(r)" :disabled="installingRecipeId === r.id">
              {{ installingRecipeId === r.id ? 'Deploying...' : '⚡ Deploy Recipe' }}
            </button>
            <button class="btn btn-sm btn-secondary recipe-btn-sec" @click="customizeRecipe(r)" :disabled="installingRecipeId === r.id">
              Customize
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading" class="workflows-list">
      <div v-for="wf in workflows" :key="wf.id" class="wf-card card">
        <div class="wf-header">
          <div class="wf-info">
            <div class="wf-status-dot" :class="wf.is_active ? 'dot-active' : 'dot-inactive'"></div>
            <div>
              <h3>{{ wf.name }}</h3>
              <p class="wf-desc">{{ wf.description || 'No description' }}</p>
            </div>
          </div>
          <div class="wf-controls">
            <button :class="['toggle-btn', wf.is_active ? 'on' : 'off']" @click="toggleWorkflow(wf)" :title="wf.is_active ? 'Deactivate' : 'Activate'">
              {{ wf.is_active ? 'ON' : 'OFF' }}
            </button>
          </div>
        </div>

        <div class="wf-trigger">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span class="trigger-label">{{ triggerLabel(wf.trigger_type) }}</span>
          <span v-if="wf.trigger_config && Object.keys(wf.trigger_config).length" class="trigger-config">
            {{ formatTriggerConfig(wf) }}
          </span>
        </div>

        <div class="wf-actions-timeline" v-if="wf.actions && wf.actions.length">
          <div v-for="(action, idx) in wf.actions" :key="action.id || idx" class="action-step">
            <div class="step-indicator">
              <div class="step-num">{{ idx + 1 }}</div>
              <div v-if="idx < wf.actions.length - 1" class="step-line"></div>
            </div>
            <div class="step-content">
              <span class="step-type">{{ actionLabel(action.action_type) }}</span>
              <button class="btn-icon" @click="removeAction(wf, action)" title="Remove action">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
          </div>
        </div>
        <div v-else class="wf-no-actions">No actions configured</div>

        <div class="wf-footer">
          <div class="wf-meta">
            <span>{{ wf.run_count }} runs</span>
            <span v-if="wf.last_run_at">· Last: {{ formatDate(wf.last_run_at) }}</span>
          </div>
          <div class="wf-btns">
            <button class="btn btn-sm btn-secondary" @click="addActionModal(wf)">+ Action</button>
            <button class="btn btn-sm btn-secondary" @click="viewLogs(wf)">Logs</button>
            <button class="btn btn-sm btn-secondary" @click="editWorkflow(wf)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteWorkflow(wf)">Delete</button>
          </div>
        </div>
      </div>

      <div v-if="workflows.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        <h3>No workflows yet</h3>
        <p>Create automation rules to save time and ensure consistency</p>
        <button class="btn btn-primary" @click="openNew">Create Workflow</button>
      </div>
    </div>

    <div v-else class="loading-state"><div class="spinner"></div><p>Loading workflows...</p></div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>{{ editing ? 'Edit Workflow' : 'New Workflow' }}</h3>
          <button class="modal-close" @click="showModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveWorkflow">
            <div class="form-group">
              <label class="form-label">Workflow Name *</label>
              <input class="form-input" v-model="form.name" required placeholder="e.g. Follow-up on new deals">
            </div>
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea class="form-input" v-model="form.description" rows="2" placeholder="What does this workflow do?"></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Trigger *</label>
              <select class="form-input" v-model="form.trigger_type" required>
                <option value="">Select a trigger...</option>
                <option value="deal_stage_change">Deal Stage Changes</option>
                <option value="deal_created">New Deal Created</option>
                <option value="deal_value_above">Deal Value Exceeds Threshold</option>
                <option value="contact_created">New Contact Added</option>
                <option value="contact_no_activity">Contact Inactive For X Days</option>
                <option value="ticket_created">New Ticket Created</option>
                <option value="ticket_overdue">Ticket Past Due Date</option>
              </select>
            </div>

            <div v-if="form.trigger_type === 'deal_stage_change'" class="form-row">
              <div class="form-group flex-1">
                <label class="form-label">From Stage</label>
                <select class="form-input" v-model="triggerConfig.stage_from">
                  <option value="">Any</option>
                  <option value="lead">Lead</option>
                  <option value="qualified">Qualified</option>
                  <option value="proposal">Proposal</option>
                  <option value="negotiation">Negotiation</option>
                </select>
              </div>
              <div class="form-group flex-1">
                <label class="form-label">To Stage</label>
                <select class="form-input" v-model="triggerConfig.stage_to">
                  <option value="">Any</option>
                  <option value="qualified">Qualified</option>
                  <option value="proposal">Proposal</option>
                  <option value="negotiation">Negotiation</option>
                  <option value="won">Won</option>
                  <option value="lost">Lost</option>
                </select>
              </div>
            </div>
            <div v-if="form.trigger_type === 'deal_value_above'" class="form-group">
              <label class="form-label">Threshold (R)</label>
              <input class="form-input" v-model="triggerConfig.value_threshold" type="number" min="0" placeholder="e.g. 50000">
            </div>
            <div v-if="form.trigger_type === 'contact_no_activity'" class="form-group">
              <label class="form-label">Days Inactive</label>
              <input class="form-input" v-model="triggerConfig.days" type="number" min="1" placeholder="e.g. 14">
            </div>

            <div class="form-group">
              <label class="form-label checkbox-label">
                <input type="checkbox" v-model="form.is_active"> Active (workflow will run automatically)
              </label>
            </div>

            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Saving...' : 'Save Workflow' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showActionModal" class="modal-overlay">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Add Action to "{{ actionTargetWf?.name }}"</h3>
          <button class="modal-close" @click="showActionModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveAction">
            <div class="form-group">
              <label class="form-label">Action Type *</label>
              <select class="form-input" v-model="actionForm.action_type" required>
                <option value="">Select action...</option>
                <option value="send_email">Send Email</option>
                <option value="create_task">Create Task/Ticket</option>
                <option value="notify_user">Send Notification</option>
                <option value="change_stage">Change Deal Stage</option>
                <option value="assign_user">Assign To User</option>
                <option value="add_note">Add Note/Activity</option>
                <option value="wait">Wait (Delay)</option>
              </select>
            </div>
            <div v-if="actionForm.action_type === 'wait'" class="form-group">
              <label class="form-label">Delay (hours)</label>
              <input class="form-input" v-model="actionConfig.delay_hours" type="number" min="1" placeholder="e.g. 24">
            </div>
            <div v-if="actionForm.action_type === 'change_stage'" class="form-group">
              <label class="form-label">New Stage</label>
              <select class="form-input" v-model="actionConfig.stage">
                <option value="qualified">Qualified</option>
                <option value="proposal">Proposal</option>
                <option value="negotiation">Negotiation</option>
                <option value="won">Won</option>
              </select>
            </div>
            <div v-if="actionForm.action_type === 'notify_user' || actionForm.action_type === 'add_note'" class="form-group">
              <label class="form-label">Message</label>
              <textarea class="form-input" v-model="actionConfig.message" rows="3" placeholder="Notification or note content..."></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="showActionModal = false">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">Add Action</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showLogsModal" class="modal-overlay">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>Logs: {{ logsWf?.name }}</h3>
          <button class="modal-close" @click="showLogsModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="logs.length === 0" class="empty-state"><p>No logs yet — workflow hasn't been triggered.</p></div>
          <div v-else class="logs-list">
            <div v-for="log in logs" :key="log.id" class="log-entry">
              <span :class="['badge', log.status === 'success' ? 'badge-green' : log.status === 'partial' ? 'badge-yellow' : 'badge-red']">{{ log.status }}</span>
              <span class="log-entity">{{ log.trigger_entity_type }}: {{ log.trigger_entity_name }}</span>
              <span class="log-date">{{ formatDate(log.created_at) }}</span>
              <p v-if="log.error_message" class="log-error">{{ log.error_message }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { workflowsAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'Workflows',
  data() {
    return {
      workflows: [],
      loading: true,
      saving: false,
      showModal: false,
      showActionModal: false,
      showLogsModal: false,
      editing: null,
      actionTargetWf: null,
      logsWf: null,
      logs: [],
      form: this.emptyForm(),
      triggerConfig: {},
      actionForm: { action_type: '' },
      actionConfig: {},
      installingRecipeId: null,
      recipes: [
        {
          id: 'high_value_deal',
          badge: 'REVENUE PROTECTION',
          icon: '🏆',
          title: 'High-Ticket Deal Alert (> R100k)',
          description: 'Instantly notify executive leadership and generate a white-glove onboarding ticket when a major deal is logged.',
          trigger_type: 'deal_value_above',
          trigger_config: { value_threshold: 100000 },
          flow: 'Deal > R100k ➔ Alert Leadership ➔ VIP Priority Task',
          actions: [
            { action_type: 'notify_user', action_config: { message: '⭐ Executive Alert: High-ticket deal exceeding R100,000 has been logged. Review deal terms immediately.' } },
            { action_type: 'create_task', action_config: { message: 'Executive follow-up: Prepare customized CIPC & corporate compliance onboarding packet.' } },
            { action_type: 'add_note', action_config: { message: 'Automated governance note: High-value enterprise threshold triggered (>R100,000).' } }
          ]
        },
        {
          id: 'inbound_lead_rapid',
          badge: 'INBOUND CONVERSION',
          icon: '🚀',
          title: '48-Hour Lead Rapid Nurture',
          description: 'When a new business client is captured, send automated intro materials, delay 24h, and schedule a discovery call task.',
          trigger_type: 'contact_created',
          trigger_config: {},
          flow: 'New Client ➔ Intro Email ➔ Wait 24h ➔ Call Task',
          actions: [
            { action_type: 'send_email', action_config: { message: 'Welcome to The Finisher Luxury. We have received your inquiry and look forward to partnering.' } },
            { action_type: 'wait', action_config: { delay_hours: 24 } },
            { action_type: 'create_task', action_config: { message: 'Schedule 15-minute introductory discovery session with primary representative.' } }
          ]
        },
        {
          id: 'deal_won_onboarding',
          badge: 'VIP CLIENT ONBOARDING',
          icon: '🎉',
          title: 'Deal Won Onboarding Engine',
          description: 'When a deal closes as Won, automatically trigger client provisioning, send a formal welcome packet, and assign an account executive.',
          trigger_type: 'deal_stage_change',
          trigger_config: { stage_from: '', stage_to: 'won' },
          flow: 'Deal Won ➔ Retainer Email ➔ Provisioning Task ➔ Audit Note',
          actions: [
            { action_type: 'send_email', action_config: { message: 'Congratulations on partnering with us. Your institutional onboarding packet is attached.' } },
            { action_type: 'create_task', action_config: { message: 'Provision dedicated client assets, issue VAT invoice, and verify CIPC documents.' } },
            { action_type: 'add_note', action_config: { message: 'Audit Trail: Deal successfully closed as Won. Institutional onboarding initiated.' } }
          ]
        },
        {
          id: 'dormant_reengagement',
          badge: 'RETENTION SAFEGUARD',
          icon: '⏰',
          title: '30-Day Dormant Account Revival',
          description: 'Detect when a high-value client has had zero contact for 30 days and alert the relationship manager to conduct a check-in.',
          trigger_type: 'contact_no_activity',
          trigger_config: { days: 30 },
          flow: '30 Days Inactive ➔ Relationship Alert ➔ Portfolio Review',
          actions: [
            { action_type: 'notify_user', action_config: { message: '⚠️ Account Retention Alert: Client has been dormant for 30+ days. Schedule relationship check-in.' } },
            { action_type: 'create_task', action_config: { message: 'Conduct executive portfolio health check & schedule quarterly partnership review.' } }
          ]
        }
      ]
    }
  },
  computed: {
    activeCount() { return this.workflows.filter(w => w.is_active).length },
    totalRuns() { return this.workflows.reduce((s, w) => s + (w.run_count || 0), 0) }
  },
  mounted() { this.fetchWorkflows() },
  methods: {
    emptyForm() {
      return { name: '', description: '', trigger_type: '', is_active: true }
    },
    triggerLabel(type) {
      const map = {
        deal_stage_change: 'Deal Stage Changes', deal_created: 'New Deal Created',
        deal_value_above: 'Deal Value Exceeds Threshold', contact_created: 'New Contact Added',
        contact_no_activity: 'Contact Inactive', ticket_created: 'New Ticket', ticket_overdue: 'Ticket Overdue'
      }
      return map[type] || type
    },
    actionLabel(type) {
      const map = {
        send_email: 'Send Email', create_task: 'Create Task', notify_user: 'Send Notification',
        change_stage: 'Change Stage', assign_user: 'Assign User', add_note: 'Add Note', wait: 'Wait (Delay)'
      }
      return map[type] || type
    },
    formatTriggerConfig(wf) {
      const c = wf.trigger_config
      if (!c) return ''
      if (c.stage_from || c.stage_to) return `${c.stage_from || 'any'} → ${c.stage_to || 'any'}`
      if (c.value_threshold) return `> R${parseFloat(c.value_threshold).toLocaleString()}`
      if (c.days) return `${c.days} days`
      return ''
    },
    formatDate(d) {
      if (!d) return '—'
      return new Date(d).toLocaleDateString('en-ZA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
    },
    async fetchWorkflows() {
      this.loading = true
      try {
        const res = await workflowsAPI.getAll()
        this.workflows = res.data.results || res.data || []
      } catch (e) {
        toast.error('Failed to load workflows')
      } finally {
        this.loading = false
      }
    },
    openNew() {
      this.form = this.emptyForm()
      this.triggerConfig = {}
      this.editing = null
      this.showModal = true
    },
    editWorkflow(wf) {
      this.form = { name: wf.name, description: wf.description || '', trigger_type: wf.trigger_type, is_active: wf.is_active }
      this.triggerConfig = { ...(wf.trigger_config || {}) }
      this.editing = wf
      this.showModal = true
    },
    async saveWorkflow() {
      this.saving = true
      try {
        const payload = { ...this.form, trigger_config: this.triggerConfig }
        if (this.editing) {
          await workflowsAPI.update(this.editing.id, payload)
          toast.success('Workflow updated')
        } else {
          await workflowsAPI.create(payload)
          toast.success('Workflow created')
        }
        this.showModal = false
        this.fetchWorkflows()
      } catch (e) {
        toast.error(e.message || 'Failed to save workflow')
      } finally {
        this.saving = false
      }
    },
    async toggleWorkflow(wf) {
      try {
        await workflowsAPI.toggle(wf.id)
        wf.is_active = !wf.is_active
        toast.success(wf.is_active ? 'Workflow activated' : 'Workflow deactivated')
      } catch (e) {
        toast.error(e.message || 'Failed to toggle workflow')
      }
    },
    async deleteWorkflow(wf) {
      if (!confirm(`Delete workflow "${wf.name}"?`)) return
      try {
        await workflowsAPI.delete(wf.id)
        toast.success('Workflow deleted')
        this.fetchWorkflows()
      } catch (e) {
        toast.error(e.message || 'Failed to delete workflow')
      }
    },
    addActionModal(wf) {
      this.actionTargetWf = wf
      this.actionForm = { action_type: '' }
      this.actionConfig = {}
      this.showActionModal = true
    },
    async saveAction() {
      this.saving = true
      try {
        await workflowsAPI.addAction(this.actionTargetWf.id, {
          action_type: this.actionForm.action_type,
          action_config: this.actionConfig
        })
        toast.success('Action added')
        this.showActionModal = false
        this.fetchWorkflows()
      } catch (e) {
        toast.error(e.message || 'Failed to add action')
      } finally {
        this.saving = false
      }
    },
    async removeAction(wf, action) {
      if (!confirm('Remove this action step?')) return
      try {
        await workflowsAPI.removeAction(wf.id, action.id)
        toast.success('Action removed')
        this.fetchWorkflows()
      } catch (e) {
        toast.error(e.message || 'Failed to remove action')
      }
    },
    async viewLogs(wf) {
      this.logsWf = wf
      this.logs = []
      this.showLogsModal = true
      try {
        const res = await workflowsAPI.getLogs(wf.id)
        this.logs = res.data.results || res.data || []
      } catch (e) {
        toast.error('Failed to load logs')
      }
    },
    async installRecipe(recipe) {
      this.installingRecipeId = recipe.id
      try {
        const res = await workflowsAPI.create({
          name: recipe.title,
          description: recipe.description,
          trigger_type: recipe.trigger_type,
          trigger_config: recipe.trigger_config,
          is_active: true
        })
        const wf = res.data
        if (recipe.actions && recipe.actions.length) {
          for (const act of recipe.actions) {
            await workflowsAPI.addAction(wf.id, {
              action_type: act.action_type,
              action_config: act.action_config
            })
          }
        }
        toast.success(`✓ "${recipe.title}" deployed & activated!`)
        await this.fetchWorkflows()
      } catch (err) {
        toast.error(err.message || 'Failed to deploy recipe')
      } finally {
        this.installingRecipeId = null
      }
    },
    customizeRecipe(recipe) {
      this.form = {
        name: recipe.title,
        description: recipe.description,
        trigger_type: recipe.trigger_type,
        is_active: true
      }
      this.triggerConfig = { ...(recipe.trigger_config || {}) }
      this.editing = null
      this.showModal = true
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 24px; max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.page-header h1 { font-size: 24px; font-weight: 700; color: var(--gray-900, #111); margin: 0; }
.page-subtitle { color: var(--gray-500, #6b7280); font-size: 14px; margin-top: 4px; }

.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: var(--card-bg, #fff); border: 1px solid var(--border, #e5e7eb); border-radius: 12px; padding: 20px; text-align: center; }
.stat-value { font-size: 28px; font-weight: 700; color: var(--primary, #6366f1); }
.stat-label { font-size: 12px; color: var(--gray-500, #6b7280); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }

.workflows-list { display: flex; flex-direction: column; gap: 16px; }
.wf-card { padding: 20px; border-radius: 12px; background: var(--card-bg, #fff); border: 1px solid var(--border, #e5e7eb); }
.wf-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.wf-info { display: flex; gap: 12px; align-items: flex-start; }
.wf-info h3 { font-size: 16px; font-weight: 600; margin: 0; color: var(--gray-900); }
.wf-desc { font-size: 13px; color: var(--gray-500); margin: 4px 0 0 0; }

.wf-status-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.dot-active { background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,0.4); }
.dot-inactive { background: var(--gray-300, #d1d5db); }

.toggle-btn { padding: 4px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; border: none; cursor: pointer; transition: all 0.2s; }
.toggle-btn.on { background: #dcfce7; color: #166534; }
.toggle-btn.off { background: #f3f4f6; color: #6b7280; }

.wf-trigger { display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: var(--gray-50, #f9fafb); border-radius: 8px; margin-bottom: 12px; }
.trigger-label { font-size: 13px; font-weight: 500; color: var(--gray-700); }
.trigger-config { font-size: 12px; color: var(--primary, #6366f1); background: #eef2ff; padding: 2px 8px; border-radius: 4px; }

.wf-actions-timeline { margin-bottom: 12px; padding-left: 8px; }
.action-step { display: flex; gap: 12px; align-items: flex-start; }
.step-indicator { display: flex; flex-direction: column; align-items: center; }
.step-num { width: 24px; height: 24px; border-radius: 50%; background: var(--primary, #6366f1); color: #fff; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.step-line { width: 2px; height: 16px; background: var(--gray-200, #e5e7eb); }
.step-content { display: flex; align-items: center; gap: 8px; padding: 4px 0; flex: 1; justify-content: space-between; }
.step-type { font-size: 13px; font-weight: 500; color: var(--gray-700); }

.wf-no-actions { font-size: 13px; color: var(--gray-400); padding: 8px 0; margin-bottom: 12px; }

.wf-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid var(--border, #e5e7eb); }
.wf-meta { font-size: 12px; color: var(--gray-500); }
.wf-btns { display: flex; gap: 6px; }

.btn-icon { background: none; border: none; cursor: pointer; padding: 4px; color: var(--gray-400); border-radius: 4px; }
.btn-icon:hover { background: #fee2e2; color: #991b1b; }

.logs-list { display: flex; flex-direction: column; gap: 8px; }
.log-entry { display: flex; align-items: center; gap: 12px; padding: 10px; background: var(--gray-50); border-radius: 8px; flex-wrap: wrap; }
.log-entity { font-size: 13px; color: var(--gray-700); }
.log-date { font-size: 12px; color: var(--gray-500); margin-left: auto; }
.log-error { font-size: 12px; color: #991b1b; width: 100%; margin: 4px 0 0 0; }

.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: capitalize; }
.badge-green { background: #dcfce7; color: #166534; }
.badge-yellow { background: #fef9c3; color: #854d0e; }
.badge-red { background: #fee2e2; color: #991b1b; }

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
.modal-panel { background: var(--card-bg, #fff); border-radius: 16px; width: 95%; max-width: 600px; max-height: 90vh; overflow-y: auto; }
.modal-lg { max-width: 700px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border, #e5e7eb); }
.modal-header h3 { font-size: 18px; font-weight: 600; margin: 0; }
.modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--gray-400); }
.modal-body { padding: 24px; }
.form-group { margin-bottom: 16px; }
.form-label { display: block; font-size: 13px; font-weight: 500; color: var(--gray-700); margin-bottom: 6px; }
.form-input { width: 100%; padding: 10px 12px; border: 1px solid var(--border, #e5e7eb); border-radius: 8px; font-size: 14px; background: var(--card-bg, #fff); color: var(--gray-900); box-sizing: border-box; }
.form-input:focus { outline: none; border-color: var(--primary, #6366f1); box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.form-row { display: flex; gap: 16px; }
.form-row .form-group { flex: 1; }
.flex-1 { flex: 1; }
.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; accent-color: var(--primary, #6366f1); }

.loading-state { display: flex; flex-direction: column; align-items: center; padding: 60px; color: var(--gray-500); }
.spinner { width: 32px; height: 32px; border: 3px solid var(--border, #e5e7eb); border-top-color: var(--primary, #6366f1); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .form-row { flex-direction: column; gap: 0; }
  .wf-footer { flex-direction: column; gap: 8px; align-items: flex-start; }
}

/* Executive 1-Click Recipes */
.recipes-section {
  background: rgba(17, 18, 23, 0.65);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 28px;
}
[data-theme="light"] .recipes-section {
  background: rgba(255, 255, 255, 0.85);
  border-color: rgba(184, 134, 11, 0.25);
}
.recipes-header {
  margin-bottom: 20px;
}
.recipe-pill {
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #d4af37;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 3px 10px;
  border-radius: 20px;
  margin-bottom: 6px;
  text-transform: uppercase;
}
.recipes-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: var(--gray-900, #fff);
}
.recipes-sub {
  font-size: 13px;
  color: var(--gray-500, #9ca3af);
  margin: 4px 0 0 0;
}
.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}
.recipe-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}
[data-theme="light"] .recipe-card {
  background: #fdfdfd;
  border-color: #e5e7eb;
}
.recipe-card:hover {
  border-color: rgba(212, 175, 55, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
.recipe-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.recipe-icon-wrap {
  font-size: 20px;
}
.recipe-badge {
  font-size: 10px;
  font-weight: 700;
  color: #d4af37;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.recipe-name {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 6px 0;
  color: var(--gray-900, #fff);
}
.recipe-desc {
  font-size: 12px;
  color: var(--gray-500, #9ca3af);
  line-height: 1.4;
  margin: 0 0 12px 0;
  flex: 1;
}
.recipe-flow {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 500;
  color: #60a5fa;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 14px;
}
.recipe-actions {
  display: flex;
  gap: 8px;
}
.recipe-btn {
  flex: 2;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  background: #d4af37;
  color: #000;
  border: none;
}
.recipe-btn:hover {
  background: #e6c35c;
}
.recipe-btn-sec {
  flex: 1;
  justify-content: center;
  font-size: 12px;
}
</style>
