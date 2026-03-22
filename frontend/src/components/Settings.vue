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
      selectedAvatar: null
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
    }
  }
}
</script>
<style scoped>
.settings-page { max-width: 680px; margin: 0 auto; }

.settings-sections { display: flex; flex-direction: column; gap: 1rem; }

.settings-card { padding: 0; overflow: hidden; }

.sc-header { display: flex; align-items: center; gap: .75rem; padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); }
.sc-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.sc-icon.blue  { background: #eff6ff; color: var(--primary-500); }
.sc-icon.green { background: #ecfdf5; color: var(--green-500); }
.sc-icon.gray  { background: var(--gray-100); color: var(--gray-500); }
.sc-title { font-size: .9375rem; font-weight: 600; color: var(--gray-900); margin: 0; }
.sc-desc  { font-size: .8125rem; color: var(--gray-500); margin: .125rem 0 0; }

.sc-body { padding: 0; }

.setting-row { display: flex; align-items: center; justify-content: space-between; padding: .75rem 1.25rem; border-bottom: 1px solid var(--gray-100); gap: 1rem; }
.setting-row:last-child { border-bottom: none; }
.setting-info { display: flex; flex-direction: column; gap: .125rem; flex: 1; min-width: 0; }
.setting-name { font-size: .875rem; font-weight: 500; color: var(--gray-800); }
.setting-hint { font-size: .75rem; color: var(--gray-500); line-height: 1.4; }
.setting-val  { font-size: .875rem; color: var(--gray-600); white-space: nowrap; }

/* Role / Tier badges */
.role-admin     { background: #eff6ff; color: var(--primary-500); }
.role-employee  { background: #ecfdf5; color: var(--green-500); }
.role-superuser { background: #faf5ff; color: #8b5cf6; }
.tier-sport     { background: #eff6ff; color: var(--primary-500); }
.tier-free      { background: var(--gray-100); color: var(--gray-600); }
.tier-pro       { background: #fffbeb; color: var(--amber-500); }
.tier-enterprise{ background: #faf5ff; color: #8b5cf6; }
.tier-ultimate  { background: linear-gradient(135deg, #1e1b4b, #312e81); color: #e0e7ff; }

/* Toggle */
.toggle { position: relative; display: inline-block; width: 44px; height: 24px; flex-shrink: 0; cursor: pointer; }
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-track { position: absolute; inset: 0; background: var(--gray-300); border-radius: 24px; transition: background .25s; }
.toggle-track::before { content: ''; position: absolute; height: 18px; width: 18px; left: 3px; bottom: 3px; background: #fff; border-radius: 50%; transition: transform .25s; box-shadow: var(--shadow-sm); }
input:checked + .toggle-track { background: var(--primary-500); }
input:checked + .toggle-track::before { transform: translateX(20px); }

/* Preview */
.preview-row { flex-direction: column; align-items: flex-start; }
.preview-area { width: 100%; display: flex; justify-content: center; padding: .5rem 0; }
.preview-card { display: flex; align-items: center; gap: .625rem; background: var(--gray-50); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: .75rem 1rem; width: 180px; animation: pvFloat 3s ease-in-out infinite; transition: transform .3s, box-shadow .3s; }
.preview-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.preview-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--primary-500); animation: pvPulse 2s ease-in-out infinite; flex-shrink: 0; }
.preview-lines { display: flex; flex-direction: column; gap: 5px; flex: 1; }
.preview-line { height: 5px; border-radius: 2px; background: var(--gray-200); }
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

@media (max-width: 640px) {
  .setting-row { padding: .625rem 1rem; }
}
</style>
