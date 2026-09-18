<template>
  <div class="integrations-hub luxury-theme">
    <!-- Header -->
    <div class="page-header">
      <div class="header-title-row">
        <div class="title-with-badge">
          <h1>Enterprise Integrations Hub</h1>
          <span class="live-badge"><span class="pulse-dot"></span> LIVE SYNC MATRIX</span>
        </div>
        <div class="header-actions">
          <button class="btn btn-secondary" @click="fetchIntegrations" :disabled="loading">
            🔄 {{ loading ? 'Syncing...' : 'Refresh Status' }}
          </button>
        </div>
      </div>
      <p class="page-subtitle">
        Seamlessly interconnect Meta Lead Ads, Google Workspace, Microsoft 365, WhatsApp Business, and Payment Gateways with automated zero-loss ingestion.
      </p>
    </div>

    <!-- Alert / Toast Banner -->
    <transition name="fade">
      <div v-if="alertMessage" :class="['alert-banner', alertType]">
        <span>{{ alertMessage }}</span>
        <button class="alert-close" @click="alertMessage = ''">&times;</button>
      </div>
    </transition>

    <!-- Top KPI Strip -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon gold-glow">🔗</div>
        <div class="kpi-info">
          <span class="kpi-label">Active Connectors</span>
          <span class="kpi-value font-mono">{{ activeIntegrationsCount }} / {{ integrations.length }}</span>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon blue-glow">🎯</div>
        <div class="kpi-info">
          <span class="kpi-label">Facebook Leads Ingested</span>
          <span class="kpi-value font-mono text-gold">{{ totalFacebookLeads }}</span>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon purple-glow">⚡</div>
        <div class="kpi-info">
          <span class="kpi-label">Webhook Protocol</span>
          <span class="kpi-value font-mono text-emerald">HTTPS POST / 200 OK</span>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon cyan-glow">🛡️</div>
        <div class="kpi-info">
          <span class="kpi-label">Tenant Isolation</span>
          <span class="kpi-value font-mono">POPIA Strict Lock</span>
        </div>
      </div>
    </div>

    <!-- Filter Category Tabs -->
    <div class="category-tabs">
      <button 
        v-for="tab in categoryTabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeCategory === tab.id }]"
        @click="activeCategory = tab.id"
      >
        <span>{{ tab.icon }}</span> {{ tab.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading && integrations.length === 0" class="loading-state">
      <div class="spinner"></div>
      <p>Synchronizing enterprise integration matrix...</p>
    </div>

    <!-- Providers Grid -->
    <div v-else class="providers-grid">
      <div 
        v-for="provider in filteredIntegrations" 
        :key="provider.provider"
        :class="['provider-card', { active: provider.is_active }]"
      >
        <!-- Card Header -->
        <div class="card-header">
          <div class="provider-badge-icon" :style="{ background: provider.badge_bg || '#1a1a24' }">
            <span class="provider-icon-text">{{ getProviderIcon(provider.provider) }}</span>
          </div>
          <div class="provider-title-group">
            <div class="provider-name-row">
              <h3>{{ provider.name }}</h3>
              <span :class="['status-pill', provider.is_active ? 'pill-active' : 'pill-inactive']">
                {{ provider.is_active ? 'Active' : 'Standby' }}
              </span>
            </div>
            <span class="provider-category">{{ provider.category }}</span>
          </div>
        </div>

        <!-- Description -->
        <p class="provider-desc">{{ provider.description }}</p>

        <!-- Meta / Facebook Specific Webhook Config Block -->
        <div v-if="provider.provider === 'facebook'" class="webhook-info-block">
          <div class="info-row">
            <span class="info-label">Callback Webhook URL:</span>
            <div class="copy-input-group">
              <input type="text" readonly :value="provider.webhook_url" class="font-mono" />
              <button class="btn-copy" @click="copyText(provider.webhook_url, 'Webhook URL')">
                {{ copiedField === provider.webhook_url ? '✓ Copied' : 'Copy' }}
              </button>
            </div>
          </div>
          <div class="info-row">
            <span class="info-label">Verify Token:</span>
            <div class="copy-input-group">
              <input type="text" readonly :value="provider.verify_token" class="font-mono" />
              <button class="btn-copy" @click="copyText(provider.verify_token, 'Verify Token')">
                {{ copiedField === provider.verify_token ? '✓ Copied' : 'Copy' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Telemetry & Metrics -->
        <div class="telemetry-box">
          <div class="telemetry-item">
            <span class="tel-label">Events Processed</span>
            <span class="tel-val font-mono">{{ provider.total_events_ingested || 0 }}</span>
          </div>
          <div class="telemetry-item">
            <span class="tel-label">Last Synchronization</span>
            <span class="tel-val font-mono">{{ formatDate(provider.last_sync_at) }}</span>
          </div>
        </div>

        <!-- Card Footer Actions -->
        <div class="card-footer">
          <button class="btn btn-secondary btn-sm" @click="openConfigModal(provider)">
            ⚙️ Configure Settings
          </button>
          <button 
            class="btn btn-gold btn-sm" 
            :disabled="testingProvider === provider.provider"
            @click="testProvider(provider)"
          >
            <span v-if="testingProvider === provider.provider" class="spinner-inline"></span>
            <span v-else>🚀 Test Dispatch</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Configuration Modal -->
    <div v-if="selectedProvider" class="modal-backdrop" @click.self="selectedProvider = null">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title-group">
            <h3>Configure {{ selectedProvider.name }}</h3>
            <span class="modal-sub">Enterprise Credentials &amp; Routing Configuration</span>
          </div>
          <button class="close-modal" @click="selectedProvider = null">&times;</button>
        </div>

        <form @submit.prevent="saveConfiguration" class="modal-body">
          <!-- Active Switch -->
          <div class="form-group toggle-group">
            <label class="toggle-label">
              <span class="font-bold">Integration Status</span>
              <span class="text-muted text-xs">Enable or disable real-time data flow for this provider</span>
            </label>
            <label class="switch">
              <input type="checkbox" v-model="formState.is_active" />
              <span class="slider round"></span>
            </label>
          </div>

          <!-- Provider Specific Fields -->
          <!-- Facebook Settings -->
          <template v-if="selectedProvider.provider === 'facebook'">
            <div class="form-group">
              <label>Facebook Page ID</label>
              <input 
                type="text" 
                v-model="formState.config.page_id" 
                placeholder="e.g. 1029384756" 
                class="form-input" 
              />
            </div>
            <div class="form-group">
              <label>Custom Verification Token (Optional)</label>
              <input 
                type="text" 
                v-model="formState.config.verify_token" 
                placeholder="Defaults to standard security token" 
                class="form-input font-mono" 
              />
            </div>
            <div class="form-group">
              <label>Meta App Secret (HMAC-SHA256 Payload Verification)</label>
              <input 
                type="password" 
                v-model="formState.config.app_secret" 
                placeholder="••••••••••••••••••••••••" 
                class="form-input font-mono" 
              />
            </div>
          </template>

          <!-- Gmail Settings -->
          <template v-if="selectedProvider.provider === 'gmail'">
            <div class="form-group">
              <label>Sender Email Address</label>
              <input 
                type="email" 
                v-model="formState.config.sender_email" 
                placeholder="executive@yourcompany.co.za" 
                class="form-input" 
                required 
              />
            </div>
            <div class="form-group">
              <label>Display Name</label>
              <input 
                type="text" 
                v-model="formState.config.sender_name" 
                placeholder="Executive Suite" 
                class="form-input" 
              />
            </div>
            <div class="form-group">
              <label>Google App Password / OAuth Token</label>
              <input 
                type="password" 
                v-model="formState.config.app_password" 
                placeholder="16-character Google App Password" 
                class="form-input font-mono" 
              />
              <span class="input-hint">Generate in Google Account &gt; Security &gt; 2-Step Verification &gt; App passwords.</span>
            </div>
          </template>

          <!-- Outlook Settings -->
          <template v-if="selectedProvider.provider === 'outlook'">
            <div class="form-group">
              <label>Microsoft 365 Account Email</label>
              <input 
                type="email" 
                v-model="formState.config.sender_email" 
                placeholder="office@yourfirm.com" 
                class="form-input" 
                required 
              />
            </div>
            <div class="form-group">
              <label>Display Name</label>
              <input 
                type="text" 
                v-model="formState.config.sender_name" 
                placeholder="Corporate Desk" 
                class="form-input" 
              />
            </div>
            <div class="form-group">
              <label>Azure AD Tenant ID</label>
              <input 
                type="text" 
                v-model="formState.config.tenant_id" 
                placeholder="e.g. 8f9b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d" 
                class="form-input font-mono" 
              />
            </div>
            <div class="form-group">
              <label>Client Secret / Password</label>
              <input 
                type="password" 
                v-model="formState.config.client_secret" 
                placeholder="••••••••••••••••••••••••" 
                class="form-input font-mono" 
              />
            </div>
          </template>

          <!-- WhatsApp Settings -->
          <template v-if="selectedProvider.provider === 'whatsapp'">
            <div class="form-group">
              <label>WhatsApp Business Phone Number ID</label>
              <input 
                type="text" 
                v-model="formState.config.phone_number_id" 
                placeholder="e.g. 109876543210" 
                class="form-input font-mono" 
              />
            </div>
            <div class="form-group">
              <label>Cloud API Permanent Token</label>
              <input 
                type="password" 
                v-model="formState.config.access_token" 
                placeholder="EAAG..." 
                class="form-input font-mono" 
              />
            </div>
          </template>

          <!-- PayFast Settings -->
          <template v-if="selectedProvider.provider === 'payfast'">
            <div class="form-group">
              <label>PayFast Merchant ID</label>
              <input 
                type="text" 
                v-model="formState.config.merchant_id" 
                placeholder="10000100" 
                class="form-input font-mono" 
              />
            </div>
            <div class="form-group">
              <label>PayFast Merchant Key</label>
              <input 
                type="password" 
                v-model="formState.config.merchant_key" 
                placeholder="46f0cd694581a" 
                class="form-input font-mono" 
              />
            </div>
            <div class="form-group">
              <label>Passphrase (Optional MD5 Security)</label>
              <input 
                type="password" 
                v-model="formState.config.passphrase" 
                placeholder="••••••••••••" 
                class="form-input font-mono" 
              />
            </div>
          </template>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedProvider = null">
              Cancel
            </button>
            <button type="submit" class="btn btn-gold" :disabled="saving">
              {{ saving ? 'Saving Configuration...' : 'Save & Activate' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { integrationsAPI } from '../api'

export default {
  name: 'IntegrationsHub',
  data() {
    return {
      loading: false,
      saving: false,
      testingProvider: null,
      integrations: [],
      activeCategory: 'all',
      alertMessage: '',
      alertType: 'success',
      copiedField: null,
      selectedProvider: null,
      formState: {
        provider: '',
        is_active: true,
        config: {}
      },
      categoryTabs: [
        { id: 'all', label: 'All Integrations', icon: '🌐' },
        { id: 'advertising', label: 'Advertising & Leads', icon: '🎯' },
        { id: 'email', label: 'Email & Workspaces', icon: '✉️' },
        { id: 'messaging', label: 'Messaging & Payments', icon: '💳' }
      ]
    }
  },
  computed: {
    activeIntegrationsCount() {
      return this.integrations.filter(i => i.is_active).length
    },
    totalFacebookLeads() {
      const fb = this.integrations.find(i => i.provider === 'facebook')
      return fb ? fb.total_events_ingested || 0 : 0
    },
    filteredIntegrations() {
      if (this.activeCategory === 'all') return this.integrations
      if (this.activeCategory === 'advertising') {
        return this.integrations.filter(i => i.provider === 'facebook')
      }
      if (this.activeCategory === 'email') {
        return this.integrations.filter(i => ['gmail', 'outlook'].includes(i.provider))
      }
      if (this.activeCategory === 'messaging') {
        return this.integrations.filter(i => ['whatsapp', 'payfast'].includes(i.provider))
      }
      return this.integrations
    }
  },
  async created() {
    await this.fetchIntegrations()
  },
  methods: {
    async fetchIntegrations() {
      this.loading = true
      try {
        const response = await integrationsAPI.getAll()
        this.integrations = response.data.integrations || []
      } catch (err) {
        console.error('Failed to load integrations:', err)
        this.showAlert('Could not load integrations. Re-syncing...', 'error')
      } finally {
        this.loading = false
      }
    },

    getProviderIcon(provider) {
      const icons = {
        facebook: '📘',
        gmail: '🔴',
        outlook: '🔷',
        whatsapp: '💬',
        payfast: '💳'
      }
      return icons[provider] || '⚡'
    },

    formatDate(dateStr) {
      if (!dateStr) return 'Never'
      const d = new Date(dateStr)
      return d.toLocaleDateString('en-ZA', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    async copyText(text, label) {
      if (!text) return
      try {
        await navigator.clipboard.writeText(text)
        this.copiedField = text
        this.showAlert(`${label} copied to clipboard!`, 'success')
        setTimeout(() => {
          if (this.copiedField === text) this.copiedField = null
        }, 3000)
      } catch (err) {
        console.error('Clipboard copy failed:', err)
        this.showAlert(`Please manually copy: ${text}`, 'info')
      }
    },

    openConfigModal(provider) {
      this.selectedProvider = provider
      this.formState = {
        provider: provider.provider,
        is_active: provider.is_active,
        config: JSON.parse(JSON.stringify(provider.config || {}))
      }
    },

    async saveConfiguration() {
      this.saving = true
      try {
        const resp = await integrationsAPI.save({
          provider: this.formState.provider,
          is_active: this.formState.is_active,
          config: this.formState.config
        })
        this.showAlert(resp.data.message || 'Configuration saved successfully.', 'success')
        this.selectedProvider = null
        await this.fetchIntegrations()
      } catch (err) {
        console.error('Failed to save integration:', err)
        const msg = err.response?.data?.error || 'Failed to save configuration.'
        this.showAlert(msg, 'error')
      } finally {
        this.saving = false
      }
    },

    async testProvider(provider) {
      this.testingProvider = provider.provider
      try {
        const resp = await integrationsAPI.test(provider.provider, {})
        this.showAlert(resp.data.message || `${provider.name} test dispatch succeeded!`, 'success')
        await this.fetchIntegrations()
      } catch (err) {
        console.error('Test dispatch failed:', err)
        const msg = err.response?.data?.error || `Test dispatch for ${provider.name} failed.`
        this.showAlert(msg, 'error')
      } finally {
        this.testingProvider = null
      }
    },

    showAlert(message, type = 'success') {
      this.alertMessage = message
      this.alertType = type
      setTimeout(() => {
        if (this.alertMessage === message) this.alertMessage = ''
      }, 6000)
    }
  }
}
</script>

<style scoped>
.integrations-hub {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  color: #e2e8f0;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}
.header-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.title-with-badge {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.title-with-badge h1 {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #ffffff 0%, #d4af37 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.page-subtitle {
  color: #94a3b8;
  font-size: 0.95rem;
  margin-top: 0.5rem;
  max-width: 800px;
}

/* Live Badge */
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: #d4af37;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 4px 10px;
  border-radius: 9999px;
}
.pulse-dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px #10b981;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.8; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.8; }
}

/* Alert Banner */
.alert-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: 1px solid;
}
.alert-banner.success {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.4);
  color: #34d399;
}
.alert-banner.error {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
  color: #f87171;
}
.alert-banner.info {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.4);
  color: #60a5fa;
}
.alert-close {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2rem;
  cursor: pointer;
  line-height: 1;
}

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.kpi-card {
  background: rgba(18, 18, 26, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  backdrop-filter: blur(10px);
}
.kpi-icon {
  font-size: 1.8rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}
.gold-glow { background: rgba(212, 175, 55, 0.12); }
.blue-glow { background: rgba(59, 130, 246, 0.12); }
.purple-glow { background: rgba(168, 85, 247, 0.12); }
.cyan-glow { background: rgba(6, 182, 212, 0.12); }
.kpi-info {
  display: flex;
  flex-direction: column;
}
.kpi-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.kpi-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
}
.text-gold { color: #d4af37 !important; }
.text-emerald { color: #10b981 !important; }

/* Category Tabs */
.category-tabs {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  overflow-x: auto;
  padding-bottom: 4px;
}
.tab-btn {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #94a3b8;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}
.tab-btn:hover {
  background: rgba(212, 175, 55, 0.08);
  color: #ffffff;
  border-color: rgba(212, 175, 55, 0.3);
}
.tab-btn.active {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0.05) 100%);
  color: #d4af37;
  border-color: #d4af37;
}

/* Providers Grid */
.providers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.5rem;
}
.provider-card {
  background: rgba(18, 18, 26, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  backdrop-filter: blur(12px);
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.provider-card:hover {
  transform: translateY(-2px);
  border-color: rgba(212, 175, 55, 0.3);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
.provider-card.active {
  border-color: rgba(212, 175, 55, 0.35);
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.provider-badge-icon {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.provider-title-group {
  flex: 1;
}
.provider-name-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.provider-name-row h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}
.provider-category {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.status-pill {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 9999px;
  text-transform: uppercase;
}
.pill-active {
  background: rgba(16, 185, 129, 0.18);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.4);
}
.pill-inactive {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.3);
}

.provider-desc {
  font-size: 0.88rem;
  color: #94a3b8;
  line-height: 1.4;
  margin-bottom: 1.25rem;
}

/* Webhook Info Block */
.webhook-info-block {
  background: rgba(10, 10, 15, 0.6);
  border: 1px dashed rgba(212, 175, 55, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 1.25rem;
}
.info-row {
  margin-bottom: 0.5rem;
}
.info-row:last-child {
  margin-bottom: 0;
}
.info-label {
  display: block;
  font-size: 0.72rem;
  color: #d4af37;
  font-weight: 600;
  margin-bottom: 3px;
}
.copy-input-group {
  display: flex;
  gap: 6px;
}
.copy-input-group input {
  flex: 1;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 4px;
}
.btn-copy {
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #d4af37;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}
.btn-copy:hover {
  background: #d4af37;
  color: #000000;
}

/* Telemetry Box */
.telemetry-box {
  background: rgba(10, 10, 15, 0.4);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.04);
}
.telemetry-item {
  display: flex;
  flex-direction: column;
}
.tel-label {
  font-size: 0.7rem;
  color: #64748b;
  text-transform: uppercase;
}
.tel-val {
  font-size: 0.85rem;
  font-weight: 600;
  color: #cbd5e1;
}

/* Card Footer */
.card-footer {
  display: flex;
  gap: 0.75rem;
}
.card-footer .btn {
  flex: 1;
  text-align: center;
  justify-content: center;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}
.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}
.btn-gold {
  background: linear-gradient(135deg, #d4af37 0%, #b8972f 100%);
  color: #0b0b10;
  box-shadow: 0 2px 10px rgba(212, 175, 55, 0.25);
}
.btn-gold:hover:not(:disabled) {
  background: linear-gradient(135deg, #e5c158 0%, #d4af37 100%);
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}
.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.12);
  color: #e2e8f0;
}
.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Spinner */
.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(212, 175, 55, 0.2);
  border-top-color: #d4af37;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}
.spinner-inline {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.loading-state {
  text-align: center;
  padding: 4rem 1rem;
  color: #94a3b8;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}
.modal-card {
  background: #14141e;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 16px;
  width: 100%;
  max-width: 540px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.modal-title-group h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #ffffff;
}
.modal-sub {
  font-size: 0.78rem;
  color: #94a3b8;
}
.close-modal {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}
.modal-body {
  padding: 1.5rem;
}
.form-group {
  margin-bottom: 1.25rem;
}
.form-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 6px;
}
.form-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #ffffff;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s ease;
}
.form-input:focus {
  border-color: #d4af37;
}
.input-hint {
  display: block;
  font-size: 0.72rem;
  color: #64748b;
  margin-top: 4px;
}
.toggle-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}
.toggle-label {
  display: flex;
  flex-direction: column;
}
.text-xs { font-size: 0.72rem; }
.text-muted { color: #64748b; }
.font-bold { font-weight: 700; color: #ffffff; }

/* Switch slider */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: #334155;
  transition: .3s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
}
input:checked + .slider {
  background-color: #d4af37;
}
input:checked + .slider:before {
  transform: translateX(20px);
}
.slider.round {
  border-radius: 24px;
}
.slider.round:before {
  border-radius: 50%;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
</style>
