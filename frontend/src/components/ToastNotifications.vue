<template>
  <transition-group name="toast" tag="div" class="toast-container">
    <div v-for="toast in toasts" :key="toast.id" :class="['toast', 'toast-' + toast.type]" @click="removeToast(toast.id)">
      <div class="toast-icon">
        <svg width="18" height="18" fill="none" :stroke="getIconColor(toast.type)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path :d="getIconPath(toast.type)"/></svg>
      </div>
      <div class="toast-content">
        <div v-if="toast.title" class="toast-title">{{ toast.title }}</div>
        <div class="toast-message">{{ toast.message }}</div>
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
      const toast = { id, message, type, title }
      this.toasts.push(toast)
      
      if (duration > 0) {
        setTimeout(() => {
          this.removeToast(id)
        }, duration)
      }
    },
    removeToast(id) {
      const index = this.toasts.findIndex(t => t.id === id)
      if (index > -1) {
        this.toasts.splice(index, 1)
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
    },
    _getIconLegacy(type) {
      const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
      }
      return icons[type] || 'ℹ️'
    }
  }
}
</script>
<style scoped>
.toast-container { position:fixed;top:calc(var(--topbar-height,56px) + .75rem);right:1rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;max-width:380px;pointer-events:none; }
.toast { display:flex;align-items:flex-start;gap:.75rem;padding:.75rem 1rem;background:#fff;border-radius:var(--radius-md);box-shadow:var(--shadow-lg);border-left:3px solid var(--primary-500);pointer-events:auto;cursor:pointer;transition:all .2s;min-width:300px; }
.toast:hover { transform:translateX(-4px); }
.toast-success { border-left-color:var(--green-500);background:#f0fdf4; }
.toast-error { border-left-color:var(--red-500);background:#fef2f2; }
.toast-warning { border-left-color:var(--amber-500);background:#fffbeb; }
.toast-info { border-left-color:var(--primary-500);background:#eff6ff; }
.toast-icon { flex-shrink:0;margin-top:1px; }
.toast-content { flex:1; }
.toast-title { font-weight:600;color:var(--gray-900);font-size:.8125rem;margin-bottom:.125rem; }
.toast-message { color:var(--gray-600);font-size:.8125rem;line-height:1.4; }
.toast-close { background:none;border:none;font-size:1.25rem;color:var(--gray-400);cursor:pointer;padding:0;width:20px;height:20px;display:flex;align-items:center;justify-content:center;border-radius:50%;flex-shrink:0; }
.toast-close:hover { background:var(--gray-100);color:var(--gray-700); }
.toast-enter-active { animation:toast-in .25s ease; }
.toast-leave-active { animation:toast-out .25s ease; }
@keyframes toast-in { from{opacity:0;transform:translateX(100%);} to{opacity:1;transform:translateX(0);} }
@keyframes toast-out { from{opacity:1;transform:translateX(0);} to{opacity:0;transform:translateX(100%);} }
</style>
