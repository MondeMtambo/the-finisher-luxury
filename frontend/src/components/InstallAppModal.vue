<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="install-modal-overlay" @click.self="close">
      <div class="install-modal-card">
        <div class="modal-gold-bar"></div>

        <div class="modal-header">
          <div class="header-badge">
            <span class="badge-icon">📲</span>
            <span class="badge-text">PROGRESSIVE WEB APPLICATION</span>
          </div>
          <button class="close-btn" @click="close" aria-label="Close modal">&times;</button>
        </div>

        <div class="modal-title-row">
          <div class="app-icon-preview">
            <img src="/apple-touch-icon.png" alt="The Finisher Luxury Icon" class="app-logo-badge" />
          </div>
          <div class="title-details">
            <h2>Download The Finisher App</h2>
            <p>Install directly to your phone's home screen for an edge-to-edge luxury executive experience — no App Store or Play Store needed.</p>
          </div>
        </div>

        <!-- 1-Click Native Install Trigger (if browser supports beforeinstallprompt) -->
        <div v-if="canPromptInstall" class="quick-install-banner">
          <div class="quick-install-info">
            <span class="quick-install-badge">READY TO INSTALL</span>
            <h4>One-Tap Installation Available</h4>
            <p>Your browser is ready to install the standalone application right now.</p>
          </div>
          <button class="btn-instant-install" @click="triggerInstall">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            <span>Install Now</span>
          </button>
        </div>

        <!-- Platform Tabs -->
        <div class="platform-tabs">
          <button 
            type="button"
            class="platform-tab" 
            :class="{ active: activePlatform === 'ios' }"
            @click="activePlatform = 'ios'"
          >
            <span class="tab-icon">🍏</span>
            <span>iPhone / iPad</span>
          </button>
          <button 
            type="button"
            class="platform-tab" 
            :class="{ active: activePlatform === 'android' }"
            @click="activePlatform = 'android'"
          >
            <span class="tab-icon">🤖</span>
            <span>Android</span>
          </button>
          <button 
            type="button"
            class="platform-tab" 
            :class="{ active: activePlatform === 'desktop' }"
            @click="activePlatform = 'desktop'"
          >
            <span class="tab-icon">💻</span>
            <span>Desktop</span>
          </button>
        </div>

        <!-- iOS Step-by-Step Guide -->
        <div v-if="activePlatform === 'ios'" class="platform-guide">
          <div class="browser-hint">
            <span class="hint-icon">💡</span>
            <span>Open this website in <strong>Apple Safari</strong> on your iPhone or iPad.</span>
          </div>

          <div class="guide-steps">
            <div class="guide-step">
              <div class="step-number">1</div>
              <div class="step-content">
                <div class="step-title">Tap the Share button</div>
                <p>Look at the bottom toolbar in Safari and tap the <strong>Share</strong> button (square with an upward arrow <span class="symbol-badge">⬆️</span>).</p>
              </div>
            </div>

            <div class="guide-step">
              <div class="step-number">2</div>
              <div class="step-content">
                <div class="step-title">Select "Add to Home Screen"</div>
                <p>Scroll down the share options list and tap <strong>Add to Home Screen</strong> (icon with a plus <span class="symbol-badge">➕</span>).</p>
              </div>
            </div>

            <div class="guide-step">
              <div class="step-number">3</div>
              <div class="step-content">
                <div class="step-title">Confirm by tapping "Add"</div>
                <p>Tap <strong>Add</strong> in the top-right corner. The Finisher Luxury icon will immediately appear on your iPhone home screen!</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Android Step-by-Step Guide -->
        <div v-if="activePlatform === 'android'" class="platform-guide">
          <div class="browser-hint">
            <span class="hint-icon">💡</span>
            <span>Works best in <strong>Google Chrome</strong> or <strong>Samsung Internet</strong>.</span>
          </div>

          <div class="guide-steps">
            <div class="guide-step">
              <div class="step-number">1</div>
              <div class="step-content">
                <div class="step-title">Tap the Browser Menu</div>
                <p>Tap the <strong>three vertical dots (⋮)</strong> in the top-right or bottom-right corner of Chrome.</p>
              </div>
            </div>

            <div class="guide-step">
              <div class="step-number">2</div>
              <div class="step-content">
                <div class="step-title">Tap "Install app" or "Add to Home screen"</div>
                <p>Select <strong>Install app</strong> (or <strong>Add to Home screen</strong>) from the dropdown list.</p>
              </div>
            </div>

            <div class="guide-step">
              <div class="step-number">3</div>
              <div class="step-content">
                <div class="step-title">Confirm Installation</div>
                <p>Tap <strong>Install</strong> when prompted. The standalone app will appear in your App Drawer and Home Screen.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Desktop Step-by-Step Guide -->
        <div v-if="activePlatform === 'desktop'" class="platform-guide">
          <div class="browser-hint">
            <span class="hint-icon">💡</span>
            <span>Supported in <strong>Google Chrome</strong>, <strong>Microsoft Edge</strong>, and <strong>Brave</strong>.</span>
          </div>

          <div class="guide-steps">
            <div class="guide-step">
              <div class="step-number">1</div>
              <div class="step-content">
                <div class="step-title">Check the Address Bar</div>
                <p>Look at the right side of your browser URL/address bar for the <strong>Install</strong> icon (computer with a downward arrow or <span class="symbol-badge">⊕</span>).</p>
              </div>
            </div>

            <div class="guide-step">
              <div class="step-number">2</div>
              <div class="step-content">
                <div class="step-title">Click "Install"</div>
                <p>Click the icon and select <strong>Install</strong> to launch the CRM in its own clean dedicated window.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Value / Features Row -->
        <div class="pwa-perks-row">
          <div class="perk-item">
            <span class="perk-icon">⚡</span>
            <div>
              <div class="perk-title">Instant Fullscreen</div>
              <div class="perk-desc">No browser bars</div>
            </div>
          </div>
          <div class="perk-item">
            <span class="perk-icon">🚀</span>
            <div>
              <div class="perk-title">Zero App Store Wait</div>
              <div class="perk-desc">Instant updates</div>
            </div>
          </div>
          <div class="perk-item">
            <span class="perk-icon">🛡️</span>
            <div>
              <div class="perk-title">Encrypted Cache</div>
              <div class="perk-desc">Fast offline shell</div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button class="btn-dismiss" @click="close">
            Got It
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'InstallAppModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  data() {
    return {
      activePlatform: 'ios',
      deferredPrompt: null,
      canPromptInstall: false
    }
  },
  mounted() {
    this.detectPlatform()
    
    // Listen for the native beforeinstallprompt event (Android / Chromium)
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault()
      this.deferredPrompt = e
      this.canPromptInstall = true
    })

    window.addEventListener('appinstalled', () => {
      this.canPromptInstall = false
      this.deferredPrompt = null
    })
  },
  methods: {
    detectPlatform() {
      const ua = navigator.userAgent || ''
      if (/iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
        this.activePlatform = 'ios'
      } else if (/android/i.test(ua)) {
        this.activePlatform = 'android'
      } else {
        this.activePlatform = 'desktop'
      }
    },
    async triggerInstall() {
      if (!this.deferredPrompt) return
      this.deferredPrompt.prompt()
      const { outcome } = await this.deferredPrompt.userChoice
      if (outcome === 'accepted') {
        this.canPromptInstall = false
        this.deferredPrompt = null
        this.close()
      }
    },
    close() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.install-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.78);
  backdrop-filter: blur(12px);
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.install-modal-card {
  position: relative;
  background: var(--surface-card, #0f1217);
  border: 1px solid var(--border-gold, rgba(212, 175, 55, 0.3));
  border-radius: 16px;
  width: 100%;
  max-width: 540px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 30px rgba(212, 175, 55, 0.12);
  color: var(--text-primary, #ffffff);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.modal-gold-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #D4AF37 0%, #FFF3B0 50%, #D4AF37 100%);
  border-radius: 16px 16px 0 0;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--text-gold, #D4AF37);
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: var(--text-muted, #94a3b8);
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--text-primary, #ffffff);
}

.modal-title-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.app-icon-preview {
  flex-shrink: 0;
}

.app-logo-badge {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  border: 2px solid #D4AF37;
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.25);
  background: #0B0C10;
  object-fit: contain;
}

.title-details h2 {
  font-size: 1.35rem;
  font-weight: 700;
  margin: 0 0 0.3rem 0;
  color: var(--text-primary, #ffffff);
}

.title-details p {
  font-size: 0.85rem;
  color: var(--text-secondary, #cbd5e1);
  margin: 0;
  line-height: 1.4;
}

.quick-install-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(15, 18, 23, 0.8) 100%);
  border: 1px solid #D4AF37;
  border-radius: 12px;
}

.quick-install-badge {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 1px;
  color: #10b981;
}

.quick-install-info h4 {
  font-size: 0.95rem;
  font-weight: 700;
  margin: 0.2rem 0;
  color: var(--text-primary, #ffffff);
}

.quick-install-info p {
  font-size: 0.78rem;
  color: var(--text-secondary, #cbd5e1);
  margin: 0;
}

.btn-instant-install {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.15rem;
  background: linear-gradient(135deg, #D4AF37 0%, #B8960C 100%);
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-instant-install:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(212, 175, 55, 0.4);
}

.platform-tabs {
  display: flex;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.35);
  padding: 0.3rem;
  border-radius: 10px;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08));
}

.platform-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.6rem 0.5rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted, #94a3b8);
  cursor: pointer;
  transition: all 0.2s ease;
}

.platform-tab.active {
  background: rgba(212, 175, 55, 0.2);
  color: var(--text-gold, #D4AF37);
  border: 1px solid rgba(212, 175, 55, 0.4);
}

.platform-guide {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.browser-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 0.85rem;
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
  border-radius: 6px;
  font-size: 0.8rem;
  color: var(--text-secondary, #cbd5e1);
}

.browser-hint strong {
  color: var(--text-primary, #ffffff);
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.guide-step {
  display: flex;
  gap: 0.85rem;
  align-items: flex-start;
  padding: 0.85rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.06));
  border-radius: 10px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid #D4AF37;
  color: #D4AF37;
  font-weight: 800;
  font-size: 0.82rem;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary, #ffffff);
  margin-bottom: 0.25rem;
}

.step-content p {
  font-size: 0.8rem;
  color: var(--text-secondary, #cbd5e1);
  margin: 0;
  line-height: 1.4;
}

.symbol-badge {
  display: inline-block;
  padding: 0.1rem 0.35rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-size: 0.85rem;
  margin: 0 0.15rem;
}

.pwa-perks-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.65rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.06));
}

.perk-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
}

.perk-icon {
  font-size: 1.25rem;
}

.perk-title {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-primary, #ffffff);
}

.perk-desc {
  font-size: 0.68rem;
  color: var(--text-muted, #94a3b8);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.5rem;
}

.btn-dismiss {
  padding: 0.6rem 1.5rem;
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: var(--text-gold, #D4AF37);
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-dismiss:hover {
  background: rgba(212, 175, 55, 0.25);
  color: #ffffff;
}

/* Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .pwa-perks-row {
    grid-template-columns: 1fr;
    gap: 0.4rem;
  }
  .quick-install-banner {
    flex-direction: column;
    align-items: stretch;
  }
  .btn-instant-install {
    justify-content: center;
  }
}
</style>
