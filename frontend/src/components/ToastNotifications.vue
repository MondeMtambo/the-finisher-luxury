<template>
  <transition-group name="toast" tag="div" class="toast-container">
    <div v-for="toast in toasts" :key="toast.id" :class="['toast', 'toast-' + toast.type]" @click="onToastClick(toast)">
      <div class="toast-icon">
        <svg width="18" height="18" fill="none" :stroke="getIconColor(toast.type)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path :d="getIconPath(toast.type)"/></svg>
      </div>
      <div class="toast-content">
        <div v-if="toast.title" class="toast-title">{{ toast.title }}</div>
        <div class="toast-message">{{ toast.message }}</div>
        <div v-if="getCopyableCode(toast)" class="toast-actions">
          <button class="toast-copy-btn" :class="{ 'is-copied': toast.copied }" @click.stop="copyCode(toast, getCopyableCode(toast))">
            <svg v-if="!toast.copied" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            <span>{{ toast.copied ? '✓ Copied to Clipboard' : 'Copy ' + getCopyableCode(toast) }}</span>
          </button>
        </div>
      </div>
      <button class="toast-close" @click.stop="removeToast(toast.id)">&times;</button>
    </div>
  </transition-group>
</template>

<script>
export default {
  name: 'ToastNotifications',
  data() {
    return {
      toasts: []
    }
  },
  mounted() {
    window.addEventListener('show-toast', this.handleToastEvent)
  },
  beforeUnmount() {
    window.removeEventListener('show-toast', this.handleToastEvent)
  },
  methods: {
    handleToastEvent(event) {
      this.addToast(event.detail)
    },
    addToast({ message, type = 'info', title = '', duration = 5000 }) {
      const id = Date.now() + Math.random()
      const toast = { id, message, type, title, copied: false }
      this.toasts.push(toast)
      
      const effectiveDuration = this.getCopyableCode(toast) ? Math.max(duration, 9000) : duration
      if (effectiveDuration > 0) {
        setTimeout(() => {
          this.removeToast(id)
        }, effectiveDuration)
      }
    },
    removeToast(id) {
      const index = this.toasts.findIndex(t => t.id === id)
      if (index > -1) {
        this.toasts.splice(index, 1)
      }
    },
    getCopyableCode(toast) {
      const text = `${toast.title || ''} ${toast.message || ''}`
      // Match 6-digit OTP codes or uppercase references (e.g. TND-..., SPLIT-..., RSA-...)
      const match = text.match(/\b\d{6}\b/) || text.match(/\b(?:TND|SPLIT|RSA|REF|PAY)-[A-Z0-9-]{4,}\b/i)
      return match ? match[0] : null
    },
    async copyCode(toast, code) {
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(code)
        } else {
          const ta = document.createElement('textarea')
          ta.value = code
          document.body.appendChild(ta)
          ta.select()
          document.execCommand('copy')
          ta.remove()
        }
        toast.copied = true
        setTimeout(() => { toast.copied = false }, 3000)
      } catch (err) {
        console.warn('Clipboard write failed:', err)
      }
    },
    onToastClick(toast) {
      const code = this.getCopyableCode(toast)
      if (code && !toast.copied) {
        this.copyCode(toast, code)
      }
    },
    getIconPath(type) {
      const paths = {
        success: 'M16 2l-4 4-4-4 M6 6l6 6 6-6',
        error: 'M9 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6z M15 9l-6 6 M9 9l6 6',
        warning: 'M8.57 1.43L.86 14.57a1.6 1.6 0 0 0 1.37 2.4h13.54a1.6 1.6 0 0 0 1.37-2.4L9.43 1.43a1.6 1.6 0 0 0-2.86 0z M9 6.17v3.2 M9 12.57h.01',
        info: 'M9 17a8 8 0 1 1 0-16 8 8 0 0 1 0 16z M9 5.8v3.6 M9 12.6h.01'
      }
      return paths[type] || paths.info
    },
    getIconColor(type) {
      const colors = { success:'var(--green-500)', error:'var(--red-500)', warning:'var(--amber-500)', info:'var(--primary-500)' }
      return colors[type] || 'var(--primary-500)'
    }
  }
}
</script>

<style scoped>
.toast-container { position:fixed;top:calc(var(--topbar-height,56px) + .75rem);right:1rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;max-width:380px;pointer-events:none; }
.toast { display:flex;align-items:flex-start;gap:.75rem;padding:.85rem 1.1rem;background:#0f172a;border-radius:var(--radius-md);box-shadow:0 10px 25px rgba(0,0,0,0.5);border-left:3px solid var(--primary-500);border:1px solid rgba(212,175,55,0.25);pointer-events:auto;cursor:pointer;transition:all .2s;min-width:300px; }
.toast:hover { transform:translateX(-4px); border-color:rgba(212,175,55,0.5); }
.toast-success { border-left:3px solid #22c55e; }
.toast-error { border-left:3px solid #ef4444; }
.toast-warning { border-left:3px solid #f59e0b; }
.toast-info { border-left:3px solid #d4af37; }
.toast-icon { flex-shrink:0;margin-top:2px; }
.toast-content { flex:1; }
.toast-title { font-weight:700;color:#f8fafc;font-size:.875rem;margin-bottom:.2rem;letter-spacing:0.3px; }
.toast-message { color:#cbd5e1;font-size:.825rem;line-height:1.45; }
.toast-actions { margin-top:0.6rem; }
.toast-copy-btn {
  display:inline-flex;
  align-items:center;
  gap:0.4rem;
  background:rgba(212,175,55,0.15);
  border:1px solid #d4af37;
  color:#d4af37;
  padding:0.3rem 0.65rem;
  border-radius:6px;
  font-size:0.75rem;
  font-weight:700;
  cursor:pointer;
  transition:all 0.15s ease;
  font-family:Consolas, Monaco, monospace;
}
.toast-copy-btn:hover {
  background:#d4af37;
  color:#000000;
}
.toast-copy-btn.is-copied {
  background:#22c55e;
  border-color:#22c55e;
  color:#ffffff;
}
.toast-close { background:none;border:none;font-size:1.25rem;color:#94a3b8;cursor:pointer;padding:0;width:20px;height:20px;display:flex;align-items:center;justify-content:center;border-radius:50%;flex-shrink:0; }
.toast-close:hover { background:rgba(255,255,255,0.1);color:#ffffff; }
.toast-enter-active { animation:toast-in .25s ease; }
.toast-leave-active { animation:toast-out .25s ease; }
@keyframes toast-in { from{opacity:0;transform:translateX(100%);} to{opacity:1;transform:translateX(0);} }
@keyframes toast-out { from{opacity:1;transform:translateX(0);} to{opacity:0;transform:translateX(100%);} }
</style>
