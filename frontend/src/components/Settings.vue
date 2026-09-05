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
          <div class="setting-row"><div class="setting-info"><span class="setting-name">Version</span></div><span class="setting-val">1.0.0</span></div>
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
import { authAPI } from '../api'
import { getStorageEstimate, clearAppCache } from '../utils/cacheManager'

export default {
  name: 'Settings',
  data() {
    return {
      animationsEnabled: true,
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
      clearingCache: false
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
      const map = { sport: 'SPORT', luxury: 'LUXURY', free: 'Free', pro: 'Pro', enterprise: 'Enterprise' }
      return map[this.tier] || this.tier || '—'
    }
  },
  mounted() {
    this.animationsEnabled = animationsPreference.isEnabled()
    this.loadProfile()
    this.loadStorageInfo()
  },
  methods: {
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
.sc-icon.blue  { background: rgba(212, 175, 55, 0.1); color: #D4AF37; }
.sc-icon.green { background: rgba(34, 197, 94, 0.1); color: #22c55e; }
.sc-icon.gray  { background: rgba(255, 255, 255, 0.05); color: #9ca3af; }
.sc-title { font-size: .9375rem; font-weight: 600; color: #ffffff; margin: 0; }
.sc-desc  { font-size: .8125rem; color: #9ca3af; margin: .125rem 0 0; }

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
</style>
