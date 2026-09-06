<template>
  <transition name="splash-fade">
    <div v-if="visible" class="luxury-splash-container" @click="dismiss">
      <div class="splash-backdrop">
        <div class="glow-orb glow-1"></div>
        <div class="glow-orb glow-2"></div>
        <div class="gold-grid-lines"></div>
      </div>

      <div class="splash-content">
        <!-- Monogram Crest with Flying Animation -->
        <div class="crest-wrapper">
          <div class="crest-halo"></div>
          <div class="crest-shield">
            <svg class="crest-svg" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#fff0aa" />
                  <stop offset="35%" stop-color="#d4af37" />
                  <stop offset="70%" stop-color="#b45309" />
                  <stop offset="100%" stop-color="#f59e0b" />
                </linearGradient>
                <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="4" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
              </defs>
              <!-- Outer Octagon Shield -->
              <polygon points="60,6 106,24 114,72 60,114 6,72 14,24" stroke="url(#goldGrad)" stroke-width="2.5" fill="rgba(10, 15, 29, 0.9)" filter="url(#goldGlow)" />
              <polygon points="60,14 98,29 104,68 60,104 16,68 22,29" stroke="url(#goldGrad)" stroke-width="1" fill="none" opacity="0.6" />
              <!-- TFL Monogram -->
              <text x="60" y="68" font-family="'Cinzel', 'Playfair Display', serif" font-size="34" font-weight="900" fill="url(#goldGrad)" text-anchor="middle" letter-spacing="2">TFL</text>
            </svg>
          </div>
          <!-- Shimmer Sweep -->
          <div class="crest-shimmer"></div>
        </div>

        <!-- Typography -->
        <div class="brand-text-block">
          <h1 class="brand-title">THE FINISHER LUXURY</h1>
          <div class="brand-divider">
            <span class="diamond">◆</span>
          </div>
          <p class="brand-subtitle">EXECUTIVE ENTERPRISE CRM &bull; MTAMBO HOLDINGS</p>
          <p class="brand-tagline">POPIA COMPLIANT &bull; ENCRYPTED SAFE VAULT &bull; R25M ASSET ARCHITECTURE</p>
        </div>

        <!-- Progress Bar -->
        <div class="loader-track">
          <div class="loader-progress"></div>
        </div>

        <button class="skip-btn" @click.stop="dismiss">Click anywhere to skip</button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'LuxurySplash',
  data() {
    return {
      visible: false,
      timer: null
    }
  },
  mounted() {
    // Show on initial page load if not shown in current tab session
    const shown = sessionStorage.getItem('tfl_splash_seen')
    if (!shown) {
      this.visible = true
      sessionStorage.setItem('tfl_splash_seen', 'true')
      this.timer = setTimeout(() => {
        this.dismiss()
      }, 2600)
    }
  },
  beforeUnmount() {
    if (this.timer) clearTimeout(this.timer)
  },
  methods: {
    dismiss() {
      this.visible = false
      if (this.timer) clearTimeout(this.timer)
    }
  }
}
</script>

<style scoped>
.luxury-splash-container {
  position: fixed;
  inset: 0;
  z-index: 1000000;
  background: #060913;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  cursor: pointer;
  user-select: none;
}

.splash-backdrop {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.glow-orb {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.25;
}

.glow-1 {
  top: 15%;
  left: 20%;
  background: radial-gradient(circle, #d4af37 0%, transparent 70%);
  animation: pulseGlow 4s ease-in-out infinite alternate;
}

.glow-2 {
  bottom: 15%;
  right: 20%;
  background: radial-gradient(circle, #b45309 0%, transparent 70%);
  animation: pulseGlow 4s ease-in-out infinite alternate-reverse;
}

.gold-grid-lines {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(212, 175, 55, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(212, 175, 55, 0.04) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.7;
}

.splash-content {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

/* Flying Monogram Crest */
.crest-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.75rem;
  animation: flyInCrest 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.crest-shield {
  width: 120px;
  height: 120px;
  position: relative;
  z-index: 2;
}

.crest-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 25px rgba(212, 175, 55, 0.6));
}

.crest-halo {
  position: absolute;
  width: 170px;
  height: 170px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.4) 0%, transparent 75%);
  z-index: 1;
  animation: haloPulse 2s ease-in-out infinite alternate;
}

.crest-shimmer {
  position: absolute;
  top: -20%;
  left: -50%;
  width: 200%;
  height: 140%;
  background: linear-gradient(
    60deg,
    transparent 40%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 60%
  );
  z-index: 3;
  transform: rotate(25deg);
  animation: shimmerSweep 1.6s ease-in-out infinite;
}

/* Brand Text */
.brand-text-block {
  animation: textReveal 1.2s ease-out forwards;
}

.brand-title {
  font-family: 'Cinzel', 'Times New Roman', serif;
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: 0.18em;
  background: linear-gradient(135deg, #fff 0%, #fef08a 30%, #d4af37 70%, #f59e0b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
}

.brand-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0.75rem auto;
  width: 200px;
  position: relative;
}

.brand-divider::before,
.brand-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.6), transparent);
}

.diamond {
  color: #d4af37;
  font-size: 0.65rem;
  padding: 0 0.5rem;
}

.brand-subtitle {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: #e2e8f0;
  margin: 0 0 0.4rem;
}

.brand-tagline {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: #94a3b8;
  margin: 0;
}

/* Track & Progress */
.loader-track {
  width: 220px;
  height: 3px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  margin-top: 1.75rem;
  overflow: hidden;
  position: relative;
}

.loader-progress {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #d4af37, #fde047, #d4af37);
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.8);
  border-radius: 999px;
  animation: loadFill 2.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.skip-btn {
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 0.72rem;
  letter-spacing: 0.05em;
  margin-top: 1.25rem;
  cursor: pointer;
  transition: color 0.2s;
}

.skip-btn:hover {
  color: #d4af37;
}

/* Animations */
@keyframes flyInCrest {
  0% {
    opacity: 0;
    transform: scale(0.2) translateY(60px) rotate(-8deg);
  }
  70% {
    transform: scale(1.08) translateY(-4px) rotate(1deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0) rotate(0deg);
  }
}

@keyframes textReveal {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes haloPulse {
  0% {
    transform: scale(0.9);
    opacity: 0.3;
  }
  100% {
    transform: scale(1.2);
    opacity: 0.65;
  }
}

@keyframes shimmerSweep {
  0% {
    left: -120%;
  }
  50%, 100% {
    left: 140%;
  }
}

@keyframes loadFill {
  0% { width: 5%; }
  50% { width: 65%; }
  100% { width: 100%; }
}

@keyframes pulseGlow {
  0% { transform: scale(1); opacity: 0.18; }
  100% { transform: scale(1.3); opacity: 0.35; }
}

.splash-fade-enter-active,
.splash-fade-leave-active {
  transition: opacity 0.55s ease, transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.04);
}

@media (max-width: 600px) {
  .brand-title {
    font-size: 1.6rem;
  }
  .brand-subtitle {
    font-size: 0.72rem;
  }
}
</style>
