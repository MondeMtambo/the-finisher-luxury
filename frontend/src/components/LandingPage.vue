<template>
  <div class="landing-page" @mousemove="handleMouseMove" ref="container">
    <nav class="exclusive-nav">
      <div class="nav-brand-group">
        <div class="nav-brand">THE FINISHER</div>
        <div class="nav-brand-sub">LUXURY PRIVATE OS</div>
      </div>
      <div class="nav-links">
        <button class="nav-link-btn" @click="scrollToPackages">Packages &amp; Pricing</button>
        <button class="nav-login-btn" @click="$router.push('/login')">
          Existing Member? Login &rarr;
        </button>
        <button class="nav-trial-btn" @click="selectPlanAndRegister('luxury')">
          Start 15-Day Trial
        </button>
      </div>
    </nav>

    <div class="center-stage">
      <div class="card-container" @click="handleCardClick" title="Tap to flip and explore commercial allocations">
        <!-- Sprinkling Champagne Gold Particles -->
        <div class="sparkles-container">
          <span 
            v-for="s in sparkles" 
            :key="s.id" 
            class="sparkle-particle"
            :style="s.style"
          >{{ s.symbol }}</span>
        </div>

        <div 
          class="black-card" 
          ref="blackCard"
          :class="{ 'is-flipped': isFlipped, 'is-slapping': isSlapping }" 
          :style="cardStyle"
        >
          <div class="card-glare" :style="glareStyle"></div>

          <!-- FRONT FACE -->
          <div class="card-face card-front">
            <div class="card-chip"></div>
            <div class="card-logo">F</div>
            <div class="card-title">THE FINISHER</div>
            <div class="card-subtitle">LUXURY PRIVATE OS</div>
            <div class="card-footer-foil">
              <span>VIP EXECUTIVE</span>
              <span class="click-hint">TAP TO EXPLORE &darr;</span>
            </div>
          </div>

          <!-- BACK FACE -->
          <div class="card-face card-back">
            <div class="card-mag-strip"></div>
            <div class="card-sig-panel">
              <span class="sig-line">EXECUTIVE ALLOCATION ACCESS</span>
              <span class="cvv">777</span>
            </div>
            <div class="card-back-brand">THE FINISHER LUXURY</div>
            <div class="card-back-status">
              <span class="back-status-pill">COMMERCIAL EDITIONS UNLOCKED</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="landing-vip-badge">
        <span class="vip-pulse-dot"></span>
        <span>15-DAY VIP EXECUTIVE ALLOCATION &middot; 15 WORKSPACES</span>
      </div>

      <h1 class="headline">Your Pipeline. Elevated.</h1>
      <p class="subheadline">The most exclusive CRM engine built for generational wealth and multi-million rand deals.</p>
      
      <div class="scarcity-sub-badge">
        Secure Your Space Now &mdash; Private Enterprise Allocation Active
      </div>

      <div class="hero-actions">
        <button class="request-btn" @click="selectPlanAndRegister('luxury')">Start 15-Day VIP Trial &rarr;</button>
        <button class="packages-scroll-btn" @click="scrollToPackages">View All Packages &darr;</button>
      </div>
    </div>

    <!-- Commercial Packages & 15-Day Trial Showcase -->
    <div class="packages-section" id="packages" ref="packagesSection">
      <div class="section-tag">COMMERCIAL EDITIONS &amp; EXECUTIVE ALLOCATIONS</div>
      <h2 class="section-title">Select Your Commercial Allocation</h2>
      <p class="section-subtitle">
        Empowering modern business operations with bank-grade CRM infrastructure.
        Fixed ZAR billing &middot; Zero foreign exchange volatility &middot; Cancel anytime.
      </p>

      <div class="landing-plans-grid">
        <!-- Tier 1: Corporate Sovereign (Was R999 -> Scratched to R0 Permanent) -->
        <div class="landing-plan-card featured sovereign-card">
          <div class="popular-ribbon">RECOMMENDED &middot; 5 SEATS</div>
          <div class="tier-badge gold">FLAGSHIP ALLOCATION</div>
          <h3 class="tier-name">Corporate Sovereign</h3>
          <p class="tier-desc">Empower business enterprises with full CRM capabilities.</p>
          <div class="tier-price">
            <span class="scratched-price"><del>R999</del></span>
            <span class="currency">R</span>0<span class="period">/permanent</span>
          </div>
          <div class="seat-pill featured">5 Collaborative Seats &middot; Up to 6,000 Verified Contacts</div>

          <ul class="tier-features">
            <li><strong>5 Collaborative Team Seats</strong> (CEO, Managers &amp; Reps)</li>
            <li><strong>Up to 6,000 Verified Client Contacts</strong></li>
            <li>Full deal pipeline &amp; Kanban stage management</li>
            <li>Meta / Facebook Lead Ads Webhook Integration</li>
            <li>Standard Quotation engine &amp; Invoicing</li>
            <li>Automated Email Workflows &amp; Direct Engagement</li>
            <li>POPIA Section 19 Compliance Vault</li>
            <li>Standard Enterprise Network Security Stamp</li>
          </ul>

          <button class="plan-cta-btn primary sovereign-btn" @click="selectPlanAndRegister('basic')">
            Claim 5 Seats License (R0) &rarr;
          </button>
        </div>

        <!-- Tier 2: Executive Suite -->
        <div class="landing-plan-card">
          <div class="tier-badge">ESTABLISHED FIRM</div>
          <h3 class="tier-name">Executive Suite</h3>
          <p class="tier-desc">For mid-size corporations, regional firms &amp; multi-branch groups.</p>
          <div class="tier-price">
            <span class="currency">R</span>1,500<span class="period">/month</span>
          </div>
          <div class="seat-pill">Up to 15 Users &middot; Unlimited Contacts</div>

          <ul class="tier-features">
            <li><strong>Everything in Corporate Sovereign, plus:</strong></li>
            <li><strong>Unlimited client contacts &amp; accounts</strong></li>
            <li><strong>Up to 15 executive &amp; staff seats</strong></li>
            <li>Multi-branch / department filtering</li>
            <li>Executive KPI scoreboard &amp; custom reports</li>
            <li>Automated email trigger workflows</li>
            <li>POPIA Section 19 compliance vault</li>
            <li>Priority Concierge WhatsApp &amp; Phone</li>
          </ul>

          <button class="plan-cta-btn secondary" @click="selectPlanAndRegister('executive')">
            Start 15-Day Free Trial &rarr;
          </button>
        </div>

        <!-- Tier 3: Enterprise Custom -->
        <div class="landing-plan-card enterprise">
          <div class="tier-badge">INSTITUTIONAL FLEET</div>
          <h3 class="tier-name">Enterprise Custom</h3>
          <p class="tier-desc">For large fleets, bespoke infrastructure &amp; institutional compliance.</p>
          <div class="tier-price">
            <span class="custom-rate">Custom Quote</span>
          </div>
          <div class="seat-pill">15+ Dedicated Seats &middot; Unlimited Contacts</div>

          <ul class="tier-features">
            <li><strong>Everything in Executive Suite, plus:</strong></li>
            <li><strong>Custom user capacity (15 to 1,000+)</strong></li>
            <li>Dedicated isolated cloud database</li>
            <li>Custom ERP &amp; Sage/Xero integration</li>
            <li>99.99% uptime SLA guarantee</li>
            <li>Dedicated Enterprise Technical Director</li>
          </ul>

          <a href="mailto:noreply@mtamboholdings.dev?subject=The%20Finisher%20Luxury%20Enterprise%20Edition" class="plan-cta-btn enterprise">
            Contact Executive Concierge &rarr;
          </a>
        </div>
      </div>

      <!-- Enterprise Add-On Suite -->
      <div class="landing-addons-banner">
        <div class="addons-header">
          <span class="addons-tag">MODULAR ENTERPRISE ADD-ONS</span>
          <h3>Enhance Your Corporate Operations</h3>
          <p>Activate white-label sovereignty and accredited compliance certification on demand.</p>
        </div>
        <div class="addons-grid">
          <div class="addon-card">
            <div class="addon-top">
              <span class="addon-badge">WHITE-LABEL</span>
              <h4>Corporate White-Label Branding</h4>
              <p>Remove the Finisher network watermark from all client-facing quotes, proposals, and automated emails. Upload your custom logo and corporate letterhead.</p>
            </div>
            <div class="addon-bottom">
              <div class="addon-price"><span class="currency">R</span>199<span class="period">/month</span></div>
              <button class="btn-addon" @click="$router.push('/settings')">Manage in Settings &rarr;</button>
            </div>
          </div>
          <div class="addon-card">
            <div class="addon-top">
              <span class="addon-badge gold">TENDER CERTIFICATION</span>
              <h4>Official Tender &amp; SEDA Funding Sales Pack</h4>
              <p>Download a certified, bank-grade 12-Month Audited Sales Ledger with POPIA Section 19 Cryptographic Certification and SHA-256 digital stamp for government tenders.</p>
            </div>
            <div class="addon-bottom">
              <div class="addon-price"><span class="currency">R</span>350<span class="period">/once-off</span></div>
              <button class="btn-addon gold" @click="$router.push('/reports')">Generate in Reports &rarr;</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Returning User Bar -->
      <div class="landing-returning-bar">
        <div class="returning-text">
          <strong>Authorized Member?</strong> Access your corporate workspace command deck.
        </div>
        <button class="returning-btn" @click="$router.push('/login')">
          Sign In to Workspace &rarr;
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      mouseX: 0,
      mouseY: 0,
      containerWidth: 0,
      containerHeight: 0,
      isFlipped: false,
      isSlapping: false,
      sparkles: [],
      slapTimer: null,
      sparkleTimer: null,
      scrollTimer: null
    }
  },
  computed: {
    cardStyle() {
      if (this.containerWidth === 0) return {}
      const centerX = this.containerWidth / 2
      const centerY = this.containerHeight / 2
      const rotateY = ((this.mouseX - centerX) / centerX) * 15
      const rotateX = -((this.mouseY - centerY) / centerY) * 15
      const flipY = this.isFlipped ? 180 : 0
      const scale = this.isSlapping ? 0.93 : 1
      return {
        transform: `rotateX(${rotateX}deg) rotateY(${rotateY + flipY}deg) scale(${scale})`
      }
    },
    glareStyle() {
      if (this.containerWidth === 0) return { opacity: 0 }
      const percentX = (this.mouseX / this.containerWidth) * 100
      const percentY = (this.mouseY / this.containerHeight) * 100
      return {
        background: `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(212, 175, 55, 0.4) 0%, transparent 60%)`,
        opacity: this.isFlipped ? 0.25 : 0.8
      }
    }
  },
  mounted() {
    this.updateDimensions()
    window.addEventListener('resize', this.updateDimensions)
    if (this.$route.hash === '#packages') {
      setTimeout(this.scrollToPackages, 300)
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateDimensions)
    clearTimeout(this.slapTimer)
    clearTimeout(this.sparkleTimer)
    clearTimeout(this.scrollTimer)
  },
  methods: {
    updateDimensions() {
      if (this.$refs.container) {
        this.containerWidth = this.$refs.container.offsetWidth
        this.containerHeight = this.$refs.container.offsetHeight
        this.mouseX = this.containerWidth / 2
        this.mouseY = this.containerHeight / 2
      }
    },
    handleMouseMove(e) {
      requestAnimationFrame(() => {
        this.mouseX = e.clientX
        this.mouseY = e.clientY
      })
    },
    handleCardClick() {
      // 1. Slap flip physics
      this.isFlipped = !this.isFlipped
      this.isSlapping = true

      clearTimeout(this.slapTimer)
      this.slapTimer = setTimeout(() => {
        this.isSlapping = false
      }, 650)

      // 2. Generate champagne gold starlight sprinkle burst
      this.triggerSparkleBurst()

      // 3. Smooth glide down to Commercial Packages at apex
      clearTimeout(this.scrollTimer)
      this.scrollTimer = setTimeout(() => {
        this.scrollToPackages()
      }, 420)
    },
    triggerSparkleBurst() {
      const symbols = ['✦', '✧', '⋆', '•', '✨']
      const colors = ['#f5d76e', '#d4af37', '#ffffff', '#e6ca65', '#ffd700']
      const count = 32
      const burst = []

      for (let i = 0; i < count; i++) {
        const angle = Math.random() * 2 * Math.PI
        const dist = 70 + Math.random() * 190
        const dx = `${Math.cos(angle) * dist}px`
        const dy = `${Math.sin(angle) * dist}px`
        const rot = `${Math.floor(Math.random() * 360 - 180)}deg`
        const size = `${Math.floor(11 + Math.random() * 15)}px`
        const duration = `${Math.floor(750 + Math.random() * 450)}ms`
        const delay = `${Math.floor(Math.random() * 100)}ms`
        const symbol = symbols[Math.floor(Math.random() * symbols.length)]
        const color = colors[Math.floor(Math.random() * colors.length)]

        burst.push({
          id: `${Date.now()}_${i}_${Math.random()}`,
          symbol,
          style: {
            '--dx': dx,
            '--dy': dy,
            '--rot': rot,
            '--size': size,
            '--duration': duration,
            'animation-delay': delay,
            color: color,
            left: '50%',
            top: '50%'
          }
        })
      }

      this.sparkles = burst

      clearTimeout(this.sparkleTimer)
      this.sparkleTimer = setTimeout(() => {
        this.sparkles = []
      }, 1300)
    },
    selectPlanAndRegister(plan) {
      this.$router.push({ path: '/register', query: { plan } })
    },
    scrollToPackages() {
      const el = this.$refs.packagesSection
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' })
      }
    }
  }
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
  font-family: 'Inter', system-ui, sans-serif;
  overflow-x: hidden;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
}

.exclusive-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 4rem;
  position: sticky;
  top: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(12px);
  z-index: 100;
  border-bottom: 1px solid rgba(212, 175, 55, 0.15);
}

.nav-brand-group {
  display: flex;
  flex-direction: column;
}

.nav-brand {
  font-size: 0.95rem;
  font-weight: 900;
  letter-spacing: 3px;
  color: #D4AF37;
}

.nav-brand-sub {
  font-size: 0.6rem;
  letter-spacing: 2px;
  color: #94a3b8;
  font-weight: 700;
  margin-top: 1px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.nav-link-btn {
  background: transparent;
  border: none;
  color: #cbd5e1;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 1px;
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  transition: color 0.2s;
}

.nav-link-btn:hover {
  color: #d4af37;
}

.nav-login-btn {
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.45);
  color: #f5d76e;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0.5rem 1.25rem;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-login-btn:hover {
  background: rgba(212, 175, 55, 0.2);
  border-color: #d4af37;
  color: #ffffff;
  transform: translateY(-1px);
}

.nav-trial-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b48608 100%);
  border: none;
  color: #000000;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 1px;
  padding: 0.55rem 1.35rem;
  border-radius: 999px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.35);
  transition: all 0.2s;
}

.nav-trial-btn:hover {
  background: linear-gradient(135deg, #f5d76e 0%, #d4af37 100%);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.55);
  transform: translateY(-1px);
}

.center-stage {
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 10;
  padding: 2.5rem 2rem 4rem;
}

/* 3D Centurion Luxury Black Card & Flip Animation */
.card-container {
  perspective: 1200px;
  margin: 1.5rem 0 2.5rem;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

/* Golden Starlight Sprinkles Burst */
.sparkles-container {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  pointer-events: none;
  z-index: 80;
}

.sparkle-particle {
  position: absolute;
  font-size: var(--size, 16px);
  color: var(--color, #f5d76e);
  text-shadow: 0 0 8px rgba(212, 175, 55, 0.9), 0 0 16px rgba(245, 215, 110, 0.7);
  transform: translate(-50%, -50%);
  animation: sparkle-burst var(--duration, 900ms) cubic-bezier(0.12, 0.8, 0.32, 1) forwards;
  will-change: transform, opacity;
  pointer-events: none;
}

@keyframes sparkle-burst {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.2) rotate(0deg);
  }
  25% {
    opacity: 1;
    transform: translate(calc(-50% + var(--dx) * 0.45), calc(-50% + var(--dy) * 0.45)) scale(1.4) rotate(calc(var(--rot) * 0.5));
  }
  100% {
    opacity: 0;
    transform: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy) + 40px)) scale(0.2) rotate(var(--rot));
  }
}

.black-card {
  width: 360px;
  height: 225px;
  border-radius: 18px;
  border: 1.5px solid rgba(212, 175, 55, 0.45);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.95), 0 0 35px rgba(212, 175, 55, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.2);
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.15s ease-out, border-color 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.black-card.is-slapping {
  transition: transform 0.65s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s, box-shadow 0.3s;
}

.black-card:hover {
  border-color: rgba(212, 175, 55, 0.8);
  box-shadow: 0 30px 75px rgba(0, 0, 0, 0.98), 0 0 55px rgba(212, 175, 55, 0.35), inset 0 1px 2px rgba(255, 255, 255, 0.3);
}

.card-glare {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
  mix-blend-mode: screen;
  border-radius: 17px;
  transition: opacity 0.3s;
}

/* Card Faces (Front & Back) */
.card-face {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 17px;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  box-sizing: border-box;
}

/* FRONT FACE */
.card-front {
  background: radial-gradient(circle at 30% 20%, #1a2230 0%, #0a0d14 55%, #000000 100%);
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: rotateY(0deg) translateZ(1px);
  z-index: 2;
}

.card-chip {
  width: 42px;
  height: 30px;
  background: linear-gradient(135deg, #d4af37 0%, #8a6d1c 100%);
  border-radius: 6px;
  align-self: flex-start;
  margin-bottom: 0.25rem;
  box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.card-logo {
  font-size: 3.6rem;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(135deg, #ffffff 0%, #f5d76e 50%, #d4af37 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.45));
  margin-bottom: 0.35rem;
}

.card-title {
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: 6px;
  color: #d4af37;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
  margin-bottom: 0.2rem;
}

.card-subtitle {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 4px;
  color: #94a3b8;
  text-transform: uppercase;
}

.card-footer-foil {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 1.25rem;
  font-family: monospace;
  font-size: 0.65rem;
  letter-spacing: 2px;
  color: rgba(212, 175, 55, 0.75);
}

.click-hint {
  color: #f5d76e;
  font-weight: 700;
  letter-spacing: 1px;
  animation: hint-pulse 2s infinite ease-in-out;
}

@keyframes hint-pulse {
  0%, 100% {
    opacity: 0.55;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(2px);
  }
}

/* BACK FACE */
.card-back {
  background: radial-gradient(circle at 70% 80%, #161d28 0%, #080a0f 60%, #000000 100%);
  transform: rotateY(180deg) translateZ(1px);
  padding: 1.25rem 0 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 17px;
}

.card-mag-strip {
  width: 100%;
  height: 40px;
  background: linear-gradient(180deg, #111111 0%, #1f2530 50%, #080808 100%);
  margin-top: 0.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  border-bottom: 1px solid rgba(0, 0, 0, 0.9);
}

.card-sig-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: repeating-linear-gradient(45deg, #e5e7eb, #e5e7eb 6px, #cbd5e1 6px, #cbd5e1 12px);
  color: #0f172a;
  height: 36px;
  margin: 0 1.5rem;
  padding: 0 0.85rem;
  border-radius: 4px;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.35);
}

.sig-line {
  font-family: 'Courier New', monospace;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #1e293b;
}

.cvv {
  font-family: monospace;
  font-size: 0.85rem;
  font-weight: 900;
  font-style: italic;
  background: #ffffff;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  letter-spacing: 2px;
  color: #000;
}

.card-back-brand {
  font-size: 0.75rem;
  font-weight: 900;
  letter-spacing: 3px;
  color: #d4af37;
  text-align: center;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
}

.card-back-status {
  display: flex;
  justify-content: center;
  margin-bottom: 0.25rem;
}

.back-status-pill {
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #000;
  background: linear-gradient(135deg, #f5d76e 0%, #d4af37 100%);
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  box-shadow: 0 2px 10px rgba(212, 175, 55, 0.4);
  text-transform: uppercase;
}

/* Hero Typography & Urgency */
.headline {
  font-size: 4.2rem;
  font-weight: 900;
  letter-spacing: -1px;
  margin: 0 0 1rem;
  background: linear-gradient(180deg, #ffffff 30%, #e2e8f0 70%, #d4af37 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
  text-align: center;
  line-height: 1.15;
}

.subheadline {
  font-size: 1.25rem;
  color: #94a3b8;
  margin: 0 0 1.75rem;
  text-align: center;
  max-width: 650px;
  line-height: 1.6;
}

.landing-vip-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #f5d76e;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0.45rem 1.35rem;
  border-radius: 999px;
  margin-bottom: 0.75rem;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.12);
}

.vip-pulse-dot {
  width: 8px;
  height: 8px;
  background-color: #d4af37;
  border-radius: 50%;
  box-shadow: 0 0 8px #d4af37;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(212, 175, 55, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }
}

.scarcity-sub-badge {
  font-size: 0.75rem;
  letter-spacing: 2px;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
  justify-content: center;
}

.request-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b48608 100%);
  border: none;
  color: #000000;
  padding: 1.15rem 2.8rem;
  font-size: 0.9rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.35);
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
}

.request-btn:hover {
  background: linear-gradient(135deg, #f5d76e 0%, #d4af37 100%);
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(212, 175, 55, 0.55);
}

.packages-scroll-btn {
  background: rgba(15, 23, 42, 0.6);
  border: 1.5px solid rgba(212, 175, 55, 0.4);
  color: #f8fafc;
  padding: 1.15rem 2.4rem;
  font-size: 0.875rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-radius: 6px;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
}

.packages-scroll-btn:hover {
  border-color: #d4af37;
  color: #d4af37;
  background: rgba(212, 175, 55, 0.12);
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(212, 175, 55, 0.2);
}

/* Packages Section */
.packages-section {
  padding: 5rem 3rem 6rem;
  background: linear-gradient(180deg, #000000 0%, #060911 50%, #020408 100%);
  position: relative;
  z-index: 10;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
}

.section-tag {
  text-align: center;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 3px;
  color: #d4af37;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.section-title {
  text-align: center;
  font-size: 2.25rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.5px;
  margin: 0 0 0.75rem;
}

.section-subtitle {
  text-align: center;
  max-width: 680px;
  margin: 0 auto 3.75rem;
  color: #94a3b8;
  font-size: 0.95rem;
  line-height: 1.7;
}

.landing-plans-grid {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.75rem;
  align-items: stretch;
}

.landing-plan-card {
  background: linear-gradient(180deg, #0b0f17 0%, #060910 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 2.75rem 1.85rem 2.25rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.landing-plan-card:hover {
  transform: translateY(-4px);
  border-color: rgba(212, 175, 55, 0.4);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.8), 0 0 20px rgba(212, 175, 55, 0.15);
}

.landing-plan-card.featured {
  border: 1.5px solid #d4af37;
  background: linear-gradient(180deg, #101622 0%, #090d15 100%);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(212, 175, 55, 0.15);
}

.popular-ribbon {
  position: absolute;
  top: -13px;
  left: 50%;
  transform: translateX(-50%);
  background: #d4af37;
  color: #000000;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  padding: 4px 14px;
  border-radius: 3px;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
  text-transform: uppercase;
}

.tier-badge {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.tier-badge.gold {
  color: #d4af37;
}

.tier-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 0.5rem;
}

.tier-desc {
  font-size: 0.8rem;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0 0 1.25rem;
  min-height: 2.5rem;
}

.tier-price {
  font-size: 2.25rem;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
}

.scratched-price {
  font-size: 1.35rem;
  color: #ef4444;
  text-decoration: line-through;
  margin-right: 0.5rem;
  font-weight: 700;
  opacity: 0.85;
}

.tier-price .currency {
  font-size: 1.25rem;
  color: #d4af37;
  margin-right: 2px;
}

.tier-price .period {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.custom-rate {
  font-size: 1.75rem;
  font-weight: 800;
  color: #d4af37;
}

.seat-pill {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  display: inline-block;
  margin-bottom: 1.5rem;
}

.seat-pill.featured {
  background: rgba(212, 175, 55, 0.15);
  border-color: rgba(212, 175, 55, 0.35);
  color: #fde68a;
}

.tier-features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem;
  flex: 1;
}

.tier-features li {
  font-size: 0.8rem;
  color: #cbd5e1;
  padding: 6px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  line-height: 1.4;
}

.tier-features li:last-child {
  border-bottom: none;
}

.savings-tag {
  color: #34d399;
  font-weight: 700;
}

.plan-cta-btn {
  width: 100%;
  padding: 0.85rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.2s;
  border: none;
}

.plan-cta-btn.primary {
  background: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
}

.plan-cta-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.6);
}

.plan-cta-btn.secondary {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #f8fafc;
}

.plan-cta-btn.secondary:hover {
  background: rgba(212, 175, 55, 0.12);
  border-color: #d4af37;
  color: #d4af37;
}

.plan-cta-btn.enterprise {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #e2e8f0;
}

.plan-cta-btn.enterprise:hover {
  border-color: #d4af37;
  color: #d4af37;
  background: rgba(212, 175, 55, 0.08);
}

.landing-returning-bar {
  max-width: 1280px;
  margin: 3.5rem auto 0;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 10px;
  padding: 1.25rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.returning-text {
  font-size: 0.9rem;
  color: #cbd5e1;
}

.returning-text strong {
  color: #d4af37;
}

.returning-btn {
  background: transparent;
  border: 1px solid #d4af37;
  color: #d4af37;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.returning-btn:hover {
  background: #d4af37;
  color: #000;
}

/* Sovereign Card & Addons Banner */
.sovereign-card {
  border-color: rgba(59, 130, 246, 0.4) !important;
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
}
.sovereign-badge {
  background: rgba(59, 130, 246, 0.15) !important;
  color: #60a5fa !important;
  border: 1px solid rgba(59, 130, 246, 0.4);
}
.sovereign-pill {
  background: rgba(59, 130, 246, 0.12) !important;
  color: #93c5fd !important;
}
.sovereign-btn {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
  color: #ffffff !important;
  border: 1px solid rgba(147, 197, 253, 0.4) !important;
}
.sovereign-btn:hover {
  background: #3b82f6 !important;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
}

.landing-addons-banner {
  margin-top: 3rem;
  background: rgba(15, 23, 42, 0.65);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 12px;
  padding: 2rem;
}
.addons-header {
  text-align: center;
  margin-bottom: 1.5rem;
}
.addons-tag {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #d4af37;
  display: inline-block;
  margin-bottom: 4px;
}
.addons-header h3 {
  font-size: 1.3rem;
  color: #ffffff;
  font-weight: 700;
  margin: 0 0 4px;
}
.addons-header p {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 0;
}
.addons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}
.addon-card {
  background: rgba(10, 15, 29, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.addon-badge {
  font-size: 0.68rem;
  font-weight: 800;
  color: #60a5fa;
  background: rgba(59, 130, 246, 0.12);
  padding: 3px 8px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 8px;
}
.addon-badge.gold {
  color: #d4af37;
  background: rgba(212, 175, 55, 0.12);
}
.addon-card h4 {
  color: #f8fafc;
  font-size: 1.05rem;
  font-weight: 700;
  margin: 0 0 6px;
}
.addon-card p {
  color: #94a3b8;
  font-size: 0.8rem;
  line-height: 1.45;
  margin: 0 0 1.25rem;
}
.addon-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.addon-price {
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff;
}
.addon-price .currency { color: #d4af37; }
.addon-price .period { font-size: 0.75rem; color: #64748b; }
.btn-addon {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e2e8f0;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-addon:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
}
.btn-addon.gold {
  border-color: rgba(212, 175, 55, 0.4);
  color: #d4af37;
}
.btn-addon.gold:hover {
  background: #d4af37;
  color: #000;
}

@media(max-width: 1100px) {
  .landing-plans-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media(max-width: 768px) {
  .headline { font-size: 2.5rem; }
  .subheadline { font-size: 1rem; padding: 0 1rem; }
  .exclusive-nav { padding: 1rem 1.5rem; }
  .black-card { width: 280px; height: 180px; }
  .landing-plans-grid { grid-template-columns: 1fr; }
  .packages-section { padding: 3rem 1.5rem; }
  .landing-returning-bar { flex-direction: column; text-align: center; }
}
</style>
