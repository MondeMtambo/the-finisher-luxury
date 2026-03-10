<template>
  <Teleport to="body">
    <transition name="modal-fade">
      <div v-if="visible" class="confirm-overlay" @click.self="handleCancel">
        <transition name="modal-scale">
          <div v-if="visible" class="confirm-dialog">
            <div class="confirm-stripe" :class="'stripe-' + type"></div>
            <div class="confirm-icon-wrap">
              <div class="confirm-icon"><svg width="28" height="28" fill="none" :stroke="iconColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path :d="iconPath"/></svg></div>
            </div>
            <h3 class="confirm-title">{{ title }}</h3>
            <p class="confirm-message" v-html="formattedMessage"></p>
            <div v-if="showInput" class="confirm-input-wrap">
              <input ref="promptInput" v-model="inputValue" :type="inputType" :placeholder="inputPlaceholder" class="form-input" @keyup.enter="handleConfirm" />
            </div>
            <div class="confirm-actions">
              <button v-if="showCancel" class="btn btn-secondary" @click="handleCancel">{{ cancelText }}</button>
              <button class="btn" :class="confirmBtnClass" @click="handleConfirm">{{ confirmText }}</button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </Teleport>
</template>

<script>
export default {
  name: 'ConfirmModal',
  data() {
    return {
      visible: false,
      title: '',
      message: '',
      type: 'info', 
      confirmText: 'OK',
      cancelText: 'Cancel',
      showCancel: true,
      showInput: false,
      inputType: 'text',
      inputPlaceholder: '',
      inputValue: '',
      resolvePromise: null,
      iconMap: {
        info: 'ℹ️',
        success: '✅',
        warning: '⚠️',
        error: '❌',
        danger: '🗑️',
        payment: '💳',
        lock: '🔒'
      }
    }
  },
  computed: {
    iconPath() {
      const paths = {
        info: 'M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z M12 16v-4 M12 8h.01',
        success: 'M22 11.08V12a10 10 0 1 1-5.93-9.14 M22 4L12 14.01l-3-3',
        warning: 'M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z M12 9v4 M12 17h.01',
        error: 'M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z M15 9l-6 6 M9 9l6 6',
        danger: 'M3 6h18 M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2',
        payment: 'M21 4H3a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z M1 10h22',
        lock: 'M19 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2z M7 11V7a5 5 0 0 1 10 0v4'
      }
      return paths[this.type] || paths.info
    },
    iconColor() {
      const colors = { info:'var(--primary-500)', success:'var(--green-500)', warning:'var(--amber-500)', error:'var(--red-500)', danger:'var(--red-500)', payment:'var(--amber-500)', lock:'var(--amber-500)' }
      return colors[this.type] || 'var(--primary-500)'
    },
    confirmBtnClass() {
      if (this.type === 'error' || this.type === 'danger') return 'btn-danger'
      if (this.type === 'success') return 'btn-success'
      return 'btn-primary'
    },
    formattedMessage() {
      return this.message.replace(/\n/g, '<br/>')
    }
  },
  mounted() {
    window.addEventListener('show-confirm', this.handleEvent)
  },
  beforeUnmount() {
    window.removeEventListener('show-confirm', this.handleEvent)
  },
  methods: {
    handleEvent(e) {
      this.open(e.detail)
    },
    open({ title, message, type = 'info', confirmText = 'OK', cancelText = 'Cancel', showCancel = true, showInput = false, inputType = 'text', inputPlaceholder = '', _resolve = null }) {
      this.title = title
      this.message = message
      this.type = type
      this.confirmText = confirmText
      this.cancelText = cancelText
      this.showCancel = showCancel
      this.showInput = showInput
      this.inputType = inputType
      this.inputPlaceholder = inputPlaceholder
      this.inputValue = ''
      this.visible = true

      if (showInput) {
        this.$nextTick(() => {
          this.$refs.promptInput?.focus()
        })
      }

      this.resolvePromise = typeof _resolve === 'function' ? _resolve : null

      return new Promise(resolve => {
        if (!this.resolvePromise) {
          this.resolvePromise = resolve
        }
      })
    },
    handleConfirm() {
      this.visible = false
      if (this.resolvePromise) {
        this.resolvePromise(this.showInput ? this.inputValue : true)
        this.resolvePromise = null
      }
    },
    handleCancel() {
      this.visible = false
      if (this.resolvePromise) {
        this.resolvePromise(this.showInput ? null : false)
        this.resolvePromise = null
      }
    }
  }
}
</script>
<style scoped>
.confirm-overlay { position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:10000;padding:1rem; }
.confirm-dialog { background:#fff;border-radius:var(--radius-lg);padding:2rem 1.75rem 1.5rem;max-width:420px;width:100%;text-align:center;box-shadow:var(--shadow-xl);position:relative;overflow:hidden; }
.confirm-stripe { position:absolute;top:0;left:0;right:0;height:3px; }
.stripe-info,.stripe-lock { background:var(--primary-500); }
.stripe-success { background:var(--green-500); }
.stripe-warning,.stripe-payment { background:var(--amber-500); }
.stripe-error,.stripe-danger { background:var(--red-500); }
.confirm-icon-wrap { margin-bottom:.75rem; }
.confirm-icon { display:inline-flex; }
.confirm-title { font-size:1.125rem;font-weight:700;color:var(--gray-900);margin:0 0 .5rem; }
.confirm-message { font-size:.875rem;color:var(--gray-600);line-height:1.5;margin:0 0 1.25rem; }
.confirm-input-wrap { margin-bottom:1.25rem; }
.confirm-actions { display:flex;gap:.5rem;justify-content:center; }
.confirm-actions .btn { min-width:110px; }
.modal-fade-enter-active,.modal-fade-leave-active { transition:opacity .2s; }
.modal-fade-enter-from,.modal-fade-leave-to { opacity:0; }
.modal-scale-enter-active { transition:transform .2s; }
.modal-scale-enter-from { transform:scale(.95); }
</style>
