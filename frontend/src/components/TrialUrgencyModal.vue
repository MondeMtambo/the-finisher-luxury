<template>
  <div v-if="show" class="trial-modal-overlay" @click.self="close">
    <div class="trial-modal-card">
      <div class="trial-modal-header">
        <div class="vip-tag">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          <span>7-DAY VIP ALLOCATION ACTIVE</span>
        </div>
        <button class="close-btn" @click="close" aria-label="Close modal">&times;</button>
      </div>

      <div class="trial-modal-body">
        <h2 class="trial-title">Unrestricted VIP Operational Access</h2>
        <p class="trial-subtitle">
          Your private operating system is running with <strong>100% unlocked capabilities</strong>: unlimited contacts, collaborative seats, deals pipeline, and analytics.
        </p>

        <!-- Timeline / Progress Indicator -->
        <div class="timeline-container">
          <div class="timeline-header">
            <span class="timeline-label">Allocation Lifecycle</span>
            <span class="timeline-days">{{ daysRemainingText }}</span>
          </div>
          <div class="timeline-bar-bg">
            <div class="timeline-bar-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
          <div class="timeline-footer">
            <span>Day 1 (VIP Launch)</span>
            <span class="grace-marker">Day 7 (Trial End) + 3-Day Grace</span>
            <span>Day 10 (Lock)</span>
          </div>
        </div>

        <!-- Loss Aversion Notice Box -->
        <div class="loss-aversion-box">
          <div class="box-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <div class="box-text">
            <strong>Data Preservation &amp; Vault Quarantine Policy</strong>
            <p>
              In accordance with POPIA Section 19, your pipeline data is never deleted. Workspaces unsettled past the 3-day grace period enter vault quarantine. Settle to keep your business operating continuously.
            </p>
          </div>
        </div>
      </div>

      <div class="trial-modal-footer">
        <button class="btn btn-secondary" @click="acknowledge">
          Continue with VIP Access
        </button>
        <button class="btn btn-primary" @click="goToUpgrade">
          Lock In Allocation (R999/mo) &rarr;
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrialUrgencyModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    daysRemaining: {
      type: Number,
      default: 7
    },
    isInGrace: {
      type: Boolean,
      default: false
    },
    graceDaysRemaining: {
      type: Number,
      default: 3
    }
  },
  emits: ['close', 'acknowledge'],
  computed: {
    daysRemainingText() {
      if (this.isInGrace) {
        return `${this.graceDaysRemaining} Day(s) Left in Grace Period`
      }
      return `${this.daysRemaining} of 7 Days Remaining`
    },
    progressPercent() {
      if (this.isInGrace) {
        const graceUsed = 3 - Math.min(3, Math.max(0, this.graceDaysRemaining))
        return Math.min(100, Math.round(70 + (graceUsed / 3) * 30))
      }
      const daysUsed = 7 - Math.min(7, Math.max(0, this.daysRemaining))
      return Math.min(70, Math.round((daysUsed / 7) * 70))
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    acknowledge() {
      this.$emit('acknowledge')
    },
    goToUpgrade() {
      this.$emit('close')
      this.$router.push('/upgrade')
    }
  }
}
</script>

<style scoped>
.trial-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(4, 7, 12, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.trial-modal-card {
  width: 100%;
  max-width: 540px;
  background: linear-gradient(135deg, rgba(17, 24, 39, 0.98), rgba(10, 15, 26, 0.98));
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 40px rgba(212, 175, 55, 0.15);
  color: #fff;
  overflow: hidden;
  animation: modalFadeIn 0.25s ease-out;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.trial-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.vip-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #D4AF37;
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.15s;
}

.close-btn:hover {
  color: #fff;
}

.trial-modal-body {
  padding: 1.5rem;
}

.trial-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
  line-height: 1.25;
}

.trial-subtitle {
  font-size: 0.875rem;
  color: #94a3b8;
  margin: 0 0 1.25rem 0;
  line-height: 1.5;
}

.trial-subtitle strong {
  color: #f1f5f9;
}

.timeline-container {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.25rem;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.timeline-label {
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.7rem;
  font-weight: 600;
}

.timeline-days {
  color: #D4AF37;
  font-weight: 700;
}

.timeline-bar-bg {
  height: 8px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 9999px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.timeline-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #eab308, #D4AF37);
  border-radius: 9999px;
  transition: width 0.4s ease;
}

.timeline-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #64748b;
}

.grace-marker {
  color: #f59e0b;
}

.loss-aversion-box {
  display: flex;
  gap: 0.85rem;
  background: rgba(212, 175, 55, 0.06);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 10px;
  padding: 1rem;
}

.box-icon {
  color: #D4AF37;
  flex-shrink: 0;
  margin-top: 2px;
}

.box-text strong {
  display: block;
  font-size: 0.8125rem;
  color: #D4AF37;
  margin-bottom: 0.25rem;
}

.box-text p {
  font-size: 0.78125rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.45;
}

.trial-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.2);
}

.btn {
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  border: none;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: #e2e8f0;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
}

.btn-primary {
  background: linear-gradient(135deg, #D4AF37, #AA7C11);
  color: #000;
  font-weight: 700;
}

.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.35);
}

@media (max-width: 600px) {
  .trial-modal-footer {
    flex-direction: column-reverse;
  }
  .btn {
    width: 100%;
    text-align: center;
  }
}
</style>
