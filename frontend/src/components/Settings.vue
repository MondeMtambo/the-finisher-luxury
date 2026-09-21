<template>
  <div class="settings-page">
    <div class="page-header">
      <div>
        <h1>Settings</h1>
        <p class="page-subtitle">Customize your experience</p>
      </div>
    </div>

    <div class="settings-sections">

      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon blue">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="9" r="7"/><path d="M6 9h6M9 6v6"/></svg>
          </div>
          <div>
            <h3 class="sc-title">Visual Effects</h3>
            <p class="sc-desc">Control animations and visual enhancements</p>
          </div>
        </div>
        <div class="sc-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-name">Animations</span>
              <span class="setting-hint">Enable subtle animations like hover effects, smooth transitions, and glowing accents.</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="animationsEnabled" @change="onAnimationsToggle" />
              <span class="toggle-track"></span>
            </label>
          </div>
          <div v-if="animationsEnabled" class="setting-row preview-row">
            <div class="setting-info">
              <span class="setting-name">Preview</span>
              <span class="setting-hint">See what the animations look like</span>
            </div>
            <div class="preview-area">
              <div class="preview-card">
                <div class="preview-dot"></div>
                <div class="preview-lines"><div class="preview-line long"></div><div class="preview-line short"></div></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon purple">
            <span style="font-weight: 900; font-size: 15px; font-family: serif; color: #a855f7;">Aa</span>
          </div>
          <div>
            <h3 class="sc-title">Display &amp; Font Size</h3>
            <p class="sc-desc">Control viewport typography scale and text density</p>
          </div>
        </div>
        <div class="sc-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-name">Text Density Scale</span>
              <span class="setting-hint">Adjust text size across the entire application for optimal reading comfort.</span>
            </div>
            <div class="font-scale-selector">
              <button 
                v-for="s in fontSizes" 
                :key="s.key" 
                type="button"
                class="scale-btn" 
                :class="{ active: currentFontSize === s.key }"
                @click="changeFontSize(s.key)"
              >
                <span class="scale-icon">{{ s.icon }}</span>
                <span class="scale-label">{{ s.label }}</span>
              </button>
            </div>
          </div>
          <div class="setting-row preview-row">
            <div class="setting-info">
              <span class="setting-name">Live Typography Preview</span>
              <span class="setting-hint">Rendering at {{ activeFontSizeScale }} scale ({{ activeBasePx }})</span>
            </div>
            <div class="preview-area">
              <div class="preview-card" style="padding: 12px; width: 100%;">
                <div style="font-weight: 700; color: #D4AF37; margin-bottom: 4px;">THE FINISHER LUXURY CRM</div>
                <div style="font-size: 1em; color: var(--text-primary, #fff); line-height: 1.4;">
                  Ultra-fast sovereign CRM workflows with customized visual comfort and responsive density.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══ OFFICIAL SOUTH AFRICAN LANGUAGES MATRIX ═══ -->
      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon gold">
            <span style="font-size: 16px;">🇿🇦</span>
          </div>
          <div>
            <h3 class="sc-title">Official SA Languages Matrix</h3>
            <p class="sc-desc">Select from all 11 official South African languages (POPIA Section 19 Sovereign Compliance)</p>
          </div>
        </div>
        <div class="sc-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-name">System Language</span>
              <span class="setting-hint">Instantly translates UI navigation, headers, tables, buttons, and status indicators across PC, Mobile, and PWA.</span>
            </div>
            <div class="lang-grid-selector">
              <button 
                v-for="l in availableLanguages" 
                :key="l.code" 
                type="button"
                class="lang-grid-btn" 
                :class="{ active: currentLangCode === l.code }"
                @click="changeLanguage(l.code)"
              >
                <span class="lang-grid-flag">{{ l.flag }}</span>
                <span class="lang-grid-label">{{ l.label }}</span>
                <span class="lang-grid-native">{{ l.native }}</span>
                <span v-if="currentLangCode === l.code" class="lang-grid-check">✓</span>
              </button>
            </div>
          </div>
          <div class="setting-row preview-row">
            <div class="setting-info">
              <span class="setting-name">Linguistic Sovereignty Status</span>
              <span class="setting-hint">POPIA Section 19 Non-Disclosure & Local Dialect Data Guarantee</span>
            </div>
            <div class="preview-area">
              <div class="preview-card" style="padding: 12px; width: 100%; border-color: rgba(212, 175, 55, 0.4);">
                <div style="font-weight: 700; color: #D4AF37; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                  <span>🇿🇦 {{ activeLanguageObj.label }} ({{ activeLanguageObj.native }})</span>
                  <span style="font-size: 10px; background: rgba(212, 175, 55, 0.2); color: #D4AF37; padding: 1px 6px; border-radius: 4px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 0.9em; color: var(--text-secondary, #94a3b8); line-height: 1.4;">
                  Realtime Autonomous Linguistic Interpreter active. Client records and confidential business data remain strictly secured.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon green">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="6" r="4"/><path d="M2 17c0-3.3 2.7-6 7-6s7 2.7 7 6"/></svg>
          </div>
          <div>
            <h3 class="sc-title">Account</h3>
            <p class="sc-desc">Your account information</p>
          </div>
        </div>
        <div class="sc-body">
          <div class="setting-row"><div class="setting-info"><span class="setting-name">Name</span></div><span class="setting-val">{{ fullName || '\u2014' }}</span></div>
          <div class="setting-row"><div class="setting-info"><span class="setting-name">Email</span></div><span class="setting-val">{{ email || '\u2014' }}</span></div>
          <div class="setting-row"><div class="setting-info"><span class="setting-name">Company</span></div><span class="setting-val">{{ companyName || '\u2014' }}</span></div>
          <div class="setting-row">
            <div class="setting-info"><span class="setting-name">Role</span></div>
            <span class="badge" :class="'role-' + role">{{ roleDisplay }}</span>
          </div>
          <div class="setting-row">
            <div class="setting-info"><span class="setting-name">Tier</span></div>
            <span class="badge" :class="'tier-' + (isAdminUser ? 'ultimate' : tier)">{{ tierDisplay }}</span>
          </div>
        </div>
      </div>

      <!-- Corporate White-Label & Custom Branding Card -->
      <div class="card settings-card white-label-card">
        <div class="sc-header">
          <div class="sc-icon gold">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          </div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
              <h3 class="sc-title">Corporate White-Label &amp; Custom Branding</h3>
              <span v-if="whiteLabelStatus.is_white_labeled" class="badge" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);">ACTIVE (R199/mo)</span>
              <span v-else class="badge" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3);">ADD-ON AVAILABLE</span>
            </div>
            <p class="sc-desc">Remove Finisher network watermarks and establish independent corporate identity on quotes &amp; invoices</p>
          </div>
        </div>

        <div class="sc-body">
          <!-- Active White-Label State -->
          <div v-if="whiteLabelStatus.is_white_labeled" class="white-label-active-box">
            <div class="setting-row">
              <div class="setting-info">
                <span class="setting-name">Network Watermark Status</span>
                <span class="setting-hint">Client-facing quotes, tax invoices, and emails are 100% white-labeled.</span>
              </div>
              <span style="color: #10b981; font-weight: 700;">✓ Watermark Disabled</span>
            </div>

            <div class="setting-row" style="align-items: flex-start;">
              <div class="setting-info">
                <span class="setting-name">Enterprise Letterhead &amp; Logo</span>
                <span class="setting-hint">Upload your high-resolution PNG or JPG company logo (max 5MB).</span>
              </div>
              <div class="logo-upload-box">
                <div v-if="whiteLabelStatus.custom_logo" class="current-logo-preview">
                  <img :src="whiteLabelStatus.custom_logo" alt="Corporate Logo" class="preview-img" />
                </div>
                <div class="upload-controls">
                  <input type="file" ref="logoInput" accept="image/*" @change="onLogoSelected" class="file-input-hidden" id="logoUpload" />
                  <label for="logoUpload" class="btn btn-secondary btn-sm" style="cursor: pointer;">
                    {{ uploadingLogo ? 'Uploading...' : (whiteLabelStatus.custom_logo ? 'Replace Logo' : 'Upload Corporate Logo') }}
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Inactive / Locked State -->
          <div v-else class="white-label-locked-box" style="padding: 1.25rem;">
            <div class="locked-watermark-preview">
              <div class="watermark-notice-title">Default Network Watermark Active:</div>
              <div class="watermark-tag">Secured by THE FINISHER LUXURY CRM Enterprise Network • thefinisher.co.za</div>
            </div>
            <p class="locked-hint" style="margin: 0.75rem 0; font-size: 0.85rem; color: var(--gray-600); line-height: 1.5;">
              White-label authorization removes this watermark from all official PDFs, tax invoices, client pro-formas, and transactional emails. 
              Billing is processed via automated PayFast monthly subscription of R199.00 ZAR.
            </p>
            <div class="action-row" style="margin-top: 1rem;">
              <button 
                class="btn btn-primary" 
                :disabled="activatingWhiteLabel" 
                @click="activateWhiteLabel"
              >
                <span v-if="activatingWhiteLabel">Connecting to PayFast...</span>
                <span v-else>Activate White-Label Subscription (R199 / month)</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon" style="background: rgba(212, 175, 55, 0.1); color: #D4AF37;">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <div>
            <h3 class="sc-title">Profile Avatar</h3>
            <p class="sc-desc">Select your executive identity</p>
          </div>
        </div>
        <div class="sc-body" style="padding: 1.25rem;">
          <div class="avatar-grid">
            <div v-for="avatar in availableAvatars" :key="avatar.id" class="avatar-item" :class="{ selected: selectedAvatar === avatar.id }" @click="selectAvatar(avatar.id)" :title="avatar.style + ' - ' + avatar.skinTone" v-html="avatar.svg"></div>
          </div>
        </div>
      </div>

      <!-- Enterprise Storage & PWA Cache Control Card -->
      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon gold">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <div>
            <h3 class="sc-title">System Integrity & Cache Control</h3>
            <p class="sc-desc">Purge stale browser bundles, reset service worker cache & force deep re-sync</p>
          </div>
        </div>
        <div class="sc-body">
          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-name">PWA Acceleration Protocol</span>
              <span class="setting-hint">Active client-side cache & instant sub-millisecond route transitions.</span>
            </div>
            <span class="badge badge-sw" :class="storageInfo.swActive ? 'sw-active' : 'sw-idle'">
              <span class="pulse-dot-mini" v-if="storageInfo.swActive"></span>
              {{ storageInfo.swActive ? 'Active & Accelerated' : 'Standard Web Mode' }}
            </span>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-name">Cached Storage Footprint</span>
              <span class="setting-hint">Local static bundle files, offline assets, and application state.</span>
            </div>
            <span class="setting-val font-mono text-gold">{{ storageInfo.formatted || 'Calculating...' }}</span>
          </div>

          <div class="setting-row action-setting-row">
            <div class="setting-info">
              <span class="setting-name">Instant App Re-Sync</span>
              <span class="setting-hint">Purges stale ServiceWorker caches and fetches latest production build. <strong>Preserves your active login session</strong>.</span>
            </div>
            <button 
              type="button" 
              class="btn btn-gold btn-sm" 
              :disabled="clearingCache" 
              @click="handleClearCache(true)"
            >
              <span v-if="clearingCache" class="btn-spinner-mini"></span>
              {{ clearingCache ? 'Purging Cache...' : '⚡ Clear Cache & Re-Sync' }}
            </button>
          </div>

          <div class="setting-row action-setting-row nuclear-row">
            <div class="setting-info">
              <span class="setting-name text-danger">Nuclear Factory Reset</span>
              <span class="setting-hint">Wipes all cached bundles, service workers, and local credentials. Requires logging in again.</span>
            </div>
            <button 
              type="button" 
              class="btn btn-outline-danger btn-sm" 
              :disabled="clearingCache" 
              @click="handleClearCache(false)"
            >
              🗑️ Full Reset
            </button>
          </div>
        </div>
      </div>

      <div class="card settings-card">
        <div class="sc-header">
          <div class="sc-icon gray">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="9" r="7"/><line x1="9" y1="7" x2="9" y2="11"/><circle cx="9" cy="5" r=".5" fill="currentColor"/></svg>
          </div>
          <div>
            <h3 class="sc-title">About</h3>
            <p class="sc-desc">Application information</p>
          </div>
        </div>
        <div class="sc-body">
          <div class="setting-row"><div class="setting-info"><span class="setting-name">Application</span></div><span class="setting-val">THE FINISHER &mdash; LUXURY Edition</span></div>
          <div class="setting-row"><div class="setting-info"><span class="setting-name">Version</span></div><span class="setting-val">Version 1.7</span></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import animationsPreference from '../utils/animations'
import authService from '../services/auth'
import toast from '../utils/toast'
import { avatars } from '../utils/avatars.js'
import { authAPI, monetizationAPI } from '../api'
import { getStorageEstimate, clearAppCache } from '../utils/cacheManager'
import fontSizeService from '../utils/fontSize'
import { languages, setLanguage, getActiveLanguage, i18nState } from '../i18n'

export default {
  name: 'Settings',
  data() {
    return {
      animationsEnabled: true,
      currentFontSize: fontSizeService.getCurrentSize(),
      fontSizes: fontSizeService.getAvailableSizes(),
      fontSizeListener: null,
      currentLangCode: i18nState.currentLang,
      availableLanguages: languages,
      langListener: null,
      username: '',
      fullName: '',
      email: '',
      companyName: '',
      role: '',
      tier: '',
      availableAvatars: avatars,
      selectedAvatar: null,
      storageInfo: {
        formatted: 'Calculating...',
        swActive: true
      },
      clearingCache: false,
      whiteLabelStatus: {
        is_white_labeled: false,
        subscription_id: '',
        custom_logo: '',
        watermark_text: ''
      },
      activatingWhiteLabel: false,
      uploadingLogo: false
    }
  },
  computed: {
    isAdminUser() {
      const user = authService.getUser()
      return !!(user && (user.is_superuser || (user.username||'').toLowerCase()==='adminluxury'))
    },
    roleDisplay() {
      const map = { admin: 'Admin', employee: 'Employee', superuser: 'System Admin' }
      return map[this.role] || this.role || '—'
    },
    tierDisplay() {
      if (this.isAdminUser) return 'ULTIMATE'
      const map = {
        sport: 'SPORT',
        luxury: 'LUXURY',
        free: 'CORPORATE SOVEREIGN',
        basic: 'CORPORATE SOVEREIGN',
        classic: 'CORPORATE SOVEREIGN',
        executive: 'EXECUTIVE SUITE',
        pro: 'PRO',
        enterprise: 'ENTERPRISE'
      }
      return map[this.tier] || this.tier || 'CORPORATE SOVEREIGN'
    },
    activeFontSizeScale() {
      const s = this.fontSizes.find(x => x.key === this.currentFontSize)
      return s ? `${Math.round(parseFloat(s.scale) * 100)}%` : '100%'
    },
    activeBasePx() {
      const s = this.fontSizes.find(x => x.key === this.currentFontSize)
      return s ? s.basePx : '14px'
    },
    activeLanguageObj() {
      return getActiveLanguage()
    }
  },
  mounted() {
    this.animationsEnabled = animationsPreference.isEnabled()
    this.loadProfile()
    this.loadStorageInfo()
    this.loadWhiteLabelStatus()
    this.fontSizeListener = (e) => {
      this.currentFontSize = e.detail?.key || fontSizeService.getCurrentSize()
    }
    window.addEventListener('tfl-font-size-changed', this.fontSizeListener)
    this.langListener = (e) => {
      this.currentLangCode = e.detail?.lang || i18nState.currentLang
    }
    window.addEventListener('tfl-language-changed', this.langListener)
    if (this.$route.query.white_label === 'success') {
      toast.success('Your Corporate White-Label subscription has been activated!', 'White-Label Active')
    } else if (this.$route.query.white_label === 'cancel') {
      toast.info('White-label subscription checkout was cancelled. No charges were made.', 'Checkout Cancelled')
    }
  },
  beforeUnmount() {
    if (this.fontSizeListener) {
      window.removeEventListener('tfl-font-size-changed', this.fontSizeListener)
    }
    if (this.langListener) {
      window.removeEventListener('tfl-language-changed', this.langListener)
    }
  },
  methods: {
    changeLanguage(code) {
      setLanguage(code)
      this.currentLangCode = code
      const active = getActiveLanguage()
      const nativePhrases = {
        en: 'Language set to English',
        zu: 'Ulimi luhlelelwe ku-isiZulu 🇿🇦',
        xh: 'Ulwimi lutshintshelwe kwisiXhosa 🇿🇦',
        af: 'Taal suksesvol verander na Afrikaans 🇿🇦',
        nso: 'Leleme le beilwe go Sesotho sa Leboa 🇿🇦',
        tn: 'Puo e beilwe mo go Setswana 🇿🇦',
        st: 'Puo e behiloe ho Sesotho 🇿🇦',
        ts: 'Ririmi ri vekiwile eka Xitsonga 🇿🇦',
        ss: 'Lulwimi luhlelelwe ku-siSwati 🇿🇦',
        ve: 'Luambo lwo vhewa kha Tshivenḓa 🇿🇦',
        nr: 'Ilimi lihlelelwe ku-isiNdebele 🇿🇦'
      }
      toast.success(nativePhrases[code] || `Language set to ${active.label}`)
    },
    changeFontSize(key) {
      const s = fontSizeService.setSize(key)
      this.currentFontSize = s.key
      toast.info(`Text scale set to ${s.label}`)
    },
    onAnimationsToggle() {
      animationsPreference.setEnabled(this.animationsEnabled)
    },
    async loadProfile() {
      try {
        const response = await authAPI.getProfile()
        const data = response.data
        this.username = data.username || ''
        this.fullName = data.full_name || `${data.first_name || ''} ${data.last_name || ''}`.trim()
        this.email = data.email || ''
        this.companyName = data.company_name || ''
        this.role = data.role || ''
        this.tier = data.tier || ''
        if (this.username) {
          this.selectedAvatar = localStorage.getItem(`avatar_${this.username}`) || avatars[0].id
        }
      } catch (err) {
        
        const user = authService.getUser()
        if (user) {
          this.fullName = user.full_name || ''
          this.email = user.email || ''
          this.companyName = user.company_name || ''
          this.role = user.role || ''
          this.tier = user.tier || ''
          this.username = user.username || ''
          if (this.username) {
            this.selectedAvatar = localStorage.getItem(`avatar_${this.username}`) || avatars[0].id
          }
        }
      }
    },
    selectAvatar(id) {
      this.selectedAvatar = id
      if (this.username) {
        localStorage.setItem(`avatar_${this.username}`, id)
        toast.success('Avatar Updated', 'Your executive identity has been set.')
        setTimeout(() => window.location.reload(), 800)
      }
    },
    async loadStorageInfo() {
      try {
        this.storageInfo = await getStorageEstimate()
      } catch (e) {
        console.warn('Storage estimate failed:', e)
      }
    },
    async handleClearCache(preserveAuth) {
      if (!preserveAuth) {
        const ok = confirm('Nuclear Reset: This will purge all offline caches, remove service workers, and log you out. Continue?')
        if (!ok) return
      }

      this.clearingCache = true
      toast.info('Purging Cache', preserveAuth ? 'Flushing cache and re-syncing latest build...' : 'Performing nuclear wipe...')

      setTimeout(async () => {
        try {
          await clearAppCache({ preserveAuth })
        } catch (err) {
          console.error('Cache purge failed:', err)
          this.clearingCache = false
          toast.error('Failed to clear cache')
        }
      }, 350)
    },
    async loadWhiteLabelStatus() {
      try {
        const res = await monetizationAPI.getWhiteLabelStatus()
        this.whiteLabelStatus = res.data
      } catch (err) {
        console.warn('Could not load white-label status', err)
      }
    },
    async activateWhiteLabel() {
      this.activatingWhiteLabel = true
      try {
        const res = await monetizationAPI.checkoutWhiteLabel()
        this.submitPayFast(res.data)
      } catch (err) {
        toast.error(err.response?.data?.error || 'Failed to initialize PayFast checkout', 'PayFast Error')
      } finally {
        this.activatingWhiteLabel = false
      }
    },
    async onLogoSelected(e) {
      const file = e.target.files[0]
      if (!file) return
      this.uploadingLogo = true
      try {
        const formData = new FormData()
        formData.append('logo', file)
        const res = await monetizationAPI.uploadWhiteLabelLogo(formData)
        toast.success(res.data.message || 'Corporate logo uploaded successfully!', 'Branding Updated')
        await this.loadWhiteLabelStatus()
      } catch (err) {
        toast.error(err.response?.data?.error || 'Failed to upload corporate logo', 'Upload Error')
      } finally {
        this.uploadingLogo = false
      }
    },
    submitPayFast(payfastData) {
      const form = document.createElement('form')
      form.method = 'POST'
      form.action = payfastData.process_url
      Object.keys(payfastData).forEach(key => {
        if (key !== 'process_url') {
          const input = document.createElement('input')
          input.type = 'hidden'
          input.name = key
          input.value = payfastData[key]
          form.appendChild(input)
        }
      })
      document.body.appendChild(form)
      form.submit()
    }
  }
}
</script>
<style scoped>
.settings-page { max-width: 680px; margin: 0 auto; }

.settings-sections { display: flex; flex-direction: column; gap: 1rem; }

.settings-card { 
  padding: 0; 
  overflow: hidden;
  background: rgba(15, 15, 15, 0.8) !important;
  border: 1px solid rgba(212, 175, 55, 0.2) !important;
}

.sc-header { display: flex; align-items: center; gap: .75rem; padding: 1rem 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.sc-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.sc-icon.blue   { background: rgba(212, 175, 55, 0.1); color: #D4AF37; }
.sc-icon.purple { background: rgba(168, 85, 247, 0.1); color: #a855f7; }
.sc-icon.green  { background: rgba(34, 197, 94, 0.1); color: #22c55e; }
.sc-icon.gray   { background: rgba(255, 255, 255, 0.05); color: #9ca3af; }
.sc-title { font-size: .9375rem; font-weight: 600; color: #ffffff; margin: 0; }
.sc-desc  { font-size: .8125rem; color: #9ca3af; margin: .125rem 0 0; }

/* Font Scale Controls */
.font-scale-selector { display: flex; gap: 6px; flex-wrap: wrap; }
.scale-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #9ca3af;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.scale-btn:hover {
  background: rgba(212, 175, 55, 0.1);
  color: #D4AF37;
  border-color: rgba(212, 175, 55, 0.3);
}
.scale-btn.active {
  background: rgba(212, 175, 55, 0.2);
  border-color: #D4AF37;
  color: #D4AF37;
}
.scale-icon { font-weight: 800; font-size: 12px; }
.scale-label { font-size: 11px; }

/* Language Matrix Controls */
.lang-grid-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 8px;
  width: 100%;
}

.lang-grid-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  text-align: left;
}

.lang-grid-btn:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.35);
  transform: translateY(-1px);
}

.lang-grid-btn.active {
  background: rgba(212, 175, 55, 0.2);
  border-color: #D4AF37;
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
}

.lang-grid-flag {
  font-size: 16px;
  margin-bottom: 2px;
}

.lang-grid-label {
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
}

.lang-grid-btn.active .lang-grid-label {
  color: #D4AF37;
}

.lang-grid-native {
  font-size: 10px;
  color: #94a3b8;
  margin-top: 1px;
}

.lang-grid-check {
  position: absolute;
  top: 6px;
  right: 8px;
  font-size: 11px;
  font-weight: 900;
  color: #D4AF37;
}

.sc-body { padding: 0; }

.setting-row { display: flex; align-items: center; justify-content: space-between; padding: .75rem 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); gap: 1rem; }
.setting-row:last-child { border-bottom: none; }
.setting-info { display: flex; flex-direction: column; gap: .125rem; flex: 1; min-width: 0; }
.setting-name { font-size: .875rem; font-weight: 500; color: #d1d5db; }
.setting-hint { font-size: .75rem; color: #6b7280; line-height: 1.4; }
.setting-val  { font-size: .875rem; color: #ffffff; white-space: nowrap; }

/* Role / Tier badges */
.role-admin     { background: rgba(212,175,55,0.1); color: #D4AF37; border: 1px solid rgba(212,175,55,0.2); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.role-employee  { background: rgba(34,197,94,0.1); color: #22c55e; border: 1px solid rgba(34,197,94,0.2); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.role-superuser { background: rgba(139,92,246,0.1); color: #8b5cf6; border: 1px solid rgba(139,92,246,0.2); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tier-sport     { background: rgba(212,175,55,0.1); color: #D4AF37; border: 1px solid rgba(212,175,55,0.2); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tier-free      { background: rgba(255,255,255,0.05); color: #9ca3af; border: 1px solid rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tier-pro       { background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.2); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tier-enterprise{ background: rgba(139,92,246,0.1); color: #8b5cf6; border: 1px solid rgba(139,92,246,0.2); padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tier-ultimate  { background: linear-gradient(135deg, #D4AF37, #B49015); color: #000; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 12px; }

/* Toggle */
.toggle { position: relative; display: inline-block; width: 44px; height: 24px; flex-shrink: 0; cursor: pointer; }
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-track { position: absolute; inset: 0; background: rgba(255,255,255,0.2); border-radius: 24px; transition: background .25s; }
.toggle-track::before { content: ''; position: absolute; height: 18px; width: 18px; left: 3px; bottom: 3px; background: #fff; border-radius: 50%; transition: transform .25s; box-shadow: var(--shadow-sm); }
input:checked + .toggle-track { background: var(--primary-500); }
input:checked + .toggle-track::before { transform: translateX(20px); }

/* Preview */
.preview-row { flex-direction: column; align-items: flex-start; }
.preview-area { width: 100%; display: flex; justify-content: center; padding: .5rem 0; }
.preview-card { display: flex; align-items: center; gap: .625rem; background: rgba(0,0,0,0.4); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: var(--radius-md); padding: .75rem 1rem; width: 180px; animation: pvFloat 3s ease-in-out infinite; transition: transform .3s, box-shadow .3s; }
.preview-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.preview-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--primary-500); animation: pvPulse 2s ease-in-out infinite; flex-shrink: 0; }
.preview-lines { display: flex; flex-direction: column; gap: 5px; flex: 1; }
.preview-line { height: 5px; border-radius: 2px; background: rgba(255,255,255,0.1); }
.preview-line.long { width: 100%; }
.preview-line.short { width: 55%; }
@keyframes pvFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
@keyframes pvPulse { 0%,100%{opacity:1} 50%{opacity:.5} }

/* Avatar Grid */
.avatar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(56px, 1fr));
  gap: 12px;
}
.avatar-item {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}
.avatar-item:hover {
  transform: translateY(-2px);
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.avatar-item.selected {
  border-color: #D4AF37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2), 0 8px 16px rgba(0, 0, 0, 0.4);
  transform: scale(1.05);
}
.avatar-item :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}

/* Cache Control & PWA Styles */
.sc-icon.gold { background: rgba(212, 175, 55, 0.15); color: #D4AF37; }
.badge-sw {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.03em;
}
.badge-sw.sw-active {
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}
.badge-sw.sw-idle {
  background: rgba(255, 255, 255, 0.06);
  color: #9ca3af;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.pulse-dot-mini {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 8px #22c55e;
  animation: pvPulse 1.5s infinite;
}
.text-gold { color: #D4AF37 !important; }
.text-danger { color: #ef4444 !important; }
.font-mono { font-family: monospace; }
.action-setting-row {
  flex-wrap: wrap;
  align-items: center;
}
.nuclear-row {
  background: rgba(239, 68, 68, 0.03);
}
.btn-gold {
  background: linear-gradient(135deg, #D4AF37, #B48608);
  color: #000;
  font-weight: 700;
  border: none;
  border-radius: 6px;
  padding: 0.45rem 0.9rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s ease;
}
.btn-gold:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}
.btn-outline-danger {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  padding: 0.45rem 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-outline-danger:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.6);
}
.btn-spinner-mini {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .setting-row { padding: .625rem 1rem; }
  .action-setting-row { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
}

/* White-Label Settings Styles */
.white-label-card {
  border-color: rgba(212, 175, 55, 0.4) !important;
}

.white-label-active-box {
  display: flex;
  flex-direction: column;
}

.logo-upload-box {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.current-logo-preview {
  max-width: 140px;
  max-height: 48px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  padding: 4px 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img {
  max-width: 100%;
  max-height: 40px;
  object-fit: contain;
}

.file-input-hidden {
  display: none;
}

.locked-watermark-preview {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 0.85rem 1rem;
}

.watermark-notice-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--gray-400);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.35rem;
}

.watermark-tag {
  font-size: 0.8rem;
  font-family: monospace;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.04);
  padding: 4px 8px;
  border-radius: 4px;
  border-left: 2px solid #d4af37;
}
</style>
