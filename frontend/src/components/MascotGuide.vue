<template>
  <div class="mascot-wrapper" :class="{ 'is-minimized': isMinimized }">
    <!-- Chat Bubble / Dialogue Window -->
    <transition name="pop-speech">
      <div v-if="isOpen && !isMinimized" class="mascot-speech-panel">
        <div class="speech-header">
          <div class="header-identity">
            <span class="online-sparkle">✨</span>
            <span class="guide-name">LEO &bull; AI EXECUTIVE CONCIERGE</span>
          </div>
          <button class="speech-close" @click="isOpen = false" title="Close Guide">&times;</button>
        </div>

        <div class="speech-body">
          <p class="greeting-text">{{ currentMessage }}</p>

          <div class="quick-chips">
            <button class="chip-btn" @click="handleAction('query')">
              <span>🐛</span> Report Bug / Query
            </button>
            <button class="chip-btn" @click="handleAction('billionaire')">
              <span>💡</span> Billionaire Insight
            </button>
            <button class="chip-btn" @click="handleAction('vault')">
              <span>🛡️</span> 30-Day Vault Policy
            </button>
            <button class="chip-btn" @click="handleAction('refreshTip')">
              <span>🔄</span> Next Tip
            </button>
          </div>
        </div>

        <div class="speech-footer">
          <span>Enterprise AI Assistant &bull; Always by your side</span>
          <button class="minimize-text-btn" @click="minimize">Hide Mascot</button>
        </div>
      </div>
    </transition>

    <!-- The Cute Big-Eyed Animated Character -->
    <div 
      class="mascot-avatar" 
      @click="toggleSpeech" 
      :title="isMinimized ? 'Wake up Leo (AI Guide)' : 'Chat with Leo (AI Guide)'"
    >
      <div class="mascot-body-orb">
        <!-- Golden Tiara / Executive Monogram -->
        <div class="tiara-wrap">
          <span class="tiara-icon">👑</span>
        </div>

        <!-- Big Cute Animated Eyes -->
        <div class="eyes-container" :class="{ 'is-blinking': isBlinking, 'is-happy': isHappy }">
          <div class="eye left-eye">
            <div class="pupil" :style="pupilStyle">
              <div class="eye-shine primary-shine"></div>
              <div class="eye-shine secondary-shine"></div>
            </div>
          </div>
          <div class="eye right-eye">
            <div class="pupil" :style="pupilStyle">
              <div class="eye-shine primary-shine"></div>
              <div class="eye-shine secondary-shine"></div>
            </div>
          </div>
        </div>

        <!-- Cheerful Smile & Rosy Cheeks -->
        <div class="cheeks-row">
          <div class="blush left-blush"></div>
          <div class="mouth" :class="{ 'is-open': isOpen }"></div>
          <div class="blush right-blush"></div>
        </div>
      </div>

      <!-- Floating Tooltip Pill when closed -->
      <div v-if="!isOpen && !isMinimized" class="floating-mascot-pill">
        Need help? Ask Leo! ✨
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MascotGuide',
  emits: ['open-query-modal'],
  data() {
    return {
      isOpen: false,
      isMinimized: false,
      isBlinking: false,
      isHappy: true,
      currentTipIndex: 0,
      pupilX: 0,
      pupilY: 0,
      blinkInterval: null,
      tips: [
        "Welcome to The Finisher Luxury! I'm Leo, your personal concierge. We make enterprise CRM as playful and effortless as ever, keeping you sharp and smiling! 😊",
        "💡 Billionaire Rule #1: High-margin subscription engines thrive on multi-seat retention. Every support ticket is a direct sales opportunity!",
        "🔒 POPIA Section 19: All inactive tenant records are safely quarantined in encrypted vaults for 30 days before clean automated purge.",
        "📊 CEO Tip: You can now initiate commercial deals and license issuance directly from Helpdesk Tickets!",
        "✨ Pro-tip: CSV exports are 100% unlocked with zero restrictions during your VIP trial and grace period."
      ]
    }
  },
  computed: {
    currentMessage() {
      return this.tips[this.currentTipIndex]
    },
    pupilStyle() {
      return {
        transform: `translate(${this.pupilX}px, ${this.pupilY}px)`
      }
    }
  },
  mounted() {
    // Random blink cycle
    this.blinkInterval = setInterval(() => {
      this.isBlinking = true
      setTimeout(() => {
        this.isBlinking = false
      }, 180)
    }, 3500)

    // Eye tracking subtle mouse movement
    window.addEventListener('mousemove', this.trackEyes)
  },
  beforeUnmount() {
    if (this.blinkInterval) clearInterval(this.blinkInterval)
    window.removeEventListener('mousemove', this.trackEyes)
  },
  methods: {
    toggleSpeech() {
      if (this.isMinimized) {
        this.isMinimized = false
        this.isOpen = true
        return
      }
      this.isOpen = !this.isOpen
    },
    minimize() {
      this.isOpen = false
      this.isMinimized = true
    },
    handleAction(action) {
      if (action === 'query') {
        this.$emit('open-query-modal')
        this.isOpen = false
      } else if (action === 'billionaire') {
        this.currentTipIndex = 1
      } else if (action === 'vault') {
        this.currentTipIndex = 2
      } else if (action === 'refreshTip') {
        this.currentTipIndex = (this.currentTipIndex + 1) % this.tips.length
      }
    },
    trackEyes(e) {
      const { innerWidth, innerHeight } = window
      const xRatio = (e.clientX / innerWidth) - 0.5
      const yRatio = (e.clientY / innerHeight) - 0.5
      this.pupilX = Math.round(xRatio * 7)
      this.pupilY = Math.round(yRatio * 5)
    }
  }
}
</script>

<style scoped>
.mascot-wrapper {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 99990;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  pointer-events: none;
}

.mascot-wrapper * {
  pointer-events: auto;
}

/* Avatar orb */
.mascot-avatar {
  position: relative;
  cursor: pointer;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.45));
  transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.mascot-avatar:hover {
  transform: scale(1.1) translateY(-4px);
}

.mascot-body-orb {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #fff6cc 0%, #facc15 35%, #d4af37 75%, #92400e 100%);
  border: 2.5px solid #fff;
  box-shadow: 0 0 20px rgba(234, 179, 8, 0.6), inset 0 -4px 8px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: gentleFloat 3.5s ease-in-out infinite alternate;
}

.tiara-wrap {
  position: absolute;
  top: -14px;
  font-size: 1.15rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
  animation: tiaraBounce 2s ease-in-out infinite alternate;
}

/* Big Cute Eyes */
.eyes-container {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

.eye {
  width: 17px;
  height: 22px;
  background: #0f172a;
  border-radius: 50%;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.6);
  transition: transform 0.1s ease;
}

.pupil {
  width: 100%;
  height: 100%;
  position: relative;
  transition: transform 0.05s ease-out;
}

.eye-shine {
  position: absolute;
  background: #ffffff;
  border-radius: 50%;
}

.primary-shine {
  width: 8px;
  height: 10px;
  top: 3px;
  left: 3px;
  box-shadow: 0 0 4px #ffffff;
}

.secondary-shine {
  width: 4px;
  height: 4px;
  bottom: 3px;
  right: 3px;
}

/* Blinking */
.eyes-container.is-blinking .eye {
  transform: scaleY(0.08);
}

/* Cheeks & Smile */
.cheeks-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 3px;
}

.blush {
  width: 8px;
  height: 5px;
  background: rgba(239, 68, 68, 0.45);
  border-radius: 50%;
}

.mouth {
  width: 8px;
  height: 4px;
  border-bottom: 2px solid #581c87;
  border-radius: 0 0 6px 6px;
  transition: height 0.15s;
}

.mouth.is-open {
  height: 6px;
  background: #701a75;
  border-radius: 0 0 8px 8px;
}

/* Floating Pill */
.floating-mascot-pill {
  position: absolute;
  right: 76px;
  top: 18px;
  white-space: nowrap;
  background: #111827;
  border: 1.5px solid #d4af37;
  color: #fde047;
  font-size: 0.76rem;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: 999px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  animation: slidePill 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Speech Panel */
.mascot-speech-panel {
  width: 320px;
  background: #0f172a;
  border: 1.5px solid rgba(212, 175, 55, 0.4);
  border-radius: 14px;
  box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.65), 0 0 20px rgba(212, 175, 55, 0.15);
  margin-bottom: 12px;
  overflow: hidden;
  color: #f1f5f9;
}

.speech-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(212, 175, 55, 0.12);
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.header-identity {
  display: flex;
  align-items: center;
  gap: 6px;
}

.guide-name {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #fbbf24;
}

.speech-close {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.3rem;
  cursor: pointer;
  line-height: 1;
}

.speech-close:hover {
  color: #fff;
}

.speech-body {
  padding: 14px;
}

.greeting-text {
  font-size: 0.825rem;
  line-height: 1.5;
  color: #e2e8f0;
  margin: 0 0 12px;
}

.quick-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chip-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 8px;
  padding: 5px 9px;
  font-size: 0.72rem;
  font-weight: 600;
  color: #f8fafc;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s;
}

.chip-btn:hover {
  background: rgba(212, 175, 55, 0.2);
  border-color: #d4af37;
  transform: translateY(-1px);
}

.speech-footer {
  padding: 8px 14px;
  background: rgba(0, 0, 0, 0.25);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.66rem;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.minimize-text-btn {
  background: none;
  border: none;
  color: #cbd5e1;
  font-size: 0.66rem;
  cursor: pointer;
  text-decoration: underline;
}

/* Animations */
@keyframes gentleFloat {
  0% { transform: translateY(0px) rotate(-1deg); }
  100% { transform: translateY(-7px) rotate(1deg); }
}

@keyframes tiaraBounce {
  0% { transform: translateY(0px); }
  100% { transform: translateY(-3px) scale(1.05); }
}

@keyframes slidePill {
  from { opacity: 0; transform: translateX(10px); }
  to { opacity: 1; transform: translateX(0); }
}

.pop-speech-enter-active,
.pop-speech-leave-active {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.pop-speech-enter-from,
.pop-speech-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(12px);
}
</style>
