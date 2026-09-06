<template>
  <div class="landing-page" @mousemove="handleMouseMove" ref="container">
    <nav class="exclusive-nav">
      <div class="nav-brand-group">
        <div class="nav-brand">THE FINISHER</div>
        <div class="nav-brand-sub">LUXURY PRIVATE OS</div>
      </div>
      <div class="nav-links">
        <button class="nav-link-btn" @click="scrollToPackages">Packages &amp; Pricing</button>
        <button class="nav-trial-btn" @click="selectPlanAndRegister('luxury')">⭐ Start 7-Day Trial</button>
        <button class="nav-login-btn" @click="$router.push('/login')">
          Existing Member? Login &rarr;
        </button>
      </div>
    </nav>

    <div class="center-stage">
      <div class="card-container">
        <div class="black-card" :style="cardStyle">
          <div class="card-glare" :style="glareStyle"></div>
          <div class="card-content">
            <div class="card-logo">F</div>
            <div class="card-title">THE FINISHER</div>
            <div class="card-subtitle">LUXURY EDITION</div>
          </div>
        </div>
      </div>
      
      <h1 class="headline">Your Pipeline. Elevated.</h1>
      <p class="subheadline">The most exclusive CRM engine built for generational wealth.</p>
      
      <div class="landing-vip-badge">
        <span class="vip-pulse-dot"></span>
        ⭐ 7-Day VIP Executive Access &middot; Strictly Capped at 15 Workspaces
      </div>
      <div class="scarcity-sub-badge">
        Secure Your Space Now &mdash; Private Enterprise Allocation Active
      </div>

      <div class="hero-actions">
        <button class="request-btn" @click="selectPlanAndRegister('luxury')">Take Our 7-Day Trial &rarr;</button>
        <button class="packages-scroll-btn" @click="scrollToPackages">View All Packages &darr;</button>
      </div>
    </div>

    <!-- Commercial Packages & 7-Day Trial Showcase -->
    <div class="packages-section" id="packages" ref="packagesSection">
      <div class="section-tag">COMMERCIAL EDITIONS &amp; 7-DAY VIP ALLOCATIONS</div>
      <h2 class="section-title">Select Your 7-Day VIP Free Trial</h2>
      <p class="section-subtitle">
        Every edition includes an unrestricted 7-day executive trial before standard monthly billing.
        Billed in South African Rand (ZAR) &middot; Zero foreign exchange fees &middot; Cancel anytime.
      </p>

      <div class="vat-strip">
        <span>🛡️ <strong>SARS Section 23 Advantage:</strong> VAT exempt (&lt;R1M threshold) &mdash; you pay zero tax surcharge on all monthly tiers.</span>
      </div>

      <div class="landing-plans-grid">
        <!-- Tier 1: Luxury Basic -->
        <div class="landing-plan-card">
          <div class="tier-badge">SOLO OPERATOR</div>
          <h3 class="tier-name">Luxury Basic</h3>
          <p class="tier-desc">For independent brokers, elite consultants &amp; single operators.</p>
          <div class="tier-price">
            <span class="currency">R</span>349<span class="period">/month</span>
          </div>
          <div class="seat-pill">1 Dedicated User (Hook Tier)</div>

          <ul class="tier-features">
            <li><strong>Unlimited</strong> contacts &amp; company accounts</li>
            <li>Full deal pipeline &amp; stage management</li>
            <li>Fleet asset tracking (up to 5 items)</li>
            <li>Task manager &amp; automatic reminders</li>
            <li>CIPC entity verification badge</li>
            <li>Standard email concierge</li>
          </ul>

          <button class="plan-cta-btn secondary" @click="selectPlanAndRegister('basic')">
            Start 7-Day Free Trial &rarr;
          </button>
        </div>

        <!-- Tier 2: Luxury Team (Featured Flagship) -->
        <div class="landing-plan-card featured">
          <div class="popular-ribbon">⭐ MOST POPULAR &middot; BEST VALUE &middot; FLAGSHIP VIP TRIAL</div>
          <div class="tier-badge gold">GROWING FIRM</div>
          <h3 class="tier-name">Luxury Team</h3>
          <p class="tier-desc">For boutique firms, agencies &amp; collaborative sales departments.</p>
          <div class="tier-price">
            <span class="currency">R</span>999<span class="period">/month</span>
          </div>
          <div class="seat-pill featured">Up to 5 Users Included (~R200/seat)</div>

          <ul class="tier-features">
            <li><strong>Everything in Luxury Basic, plus:</strong></li>
            <li><strong>Up to 5 collaborative seats</strong></li>
            <li>Shared team pipelines &amp; deal assignment</li>
            <li>Support ticket helpdesk system</li>
            <li>Full luxury fleet vehicle tracking</li>
            <li>Company laptop &amp; hardware serial register</li>
            <li>Client Admin Team Console</li>
            <li><span class="savings-tag">Saves ~R100,000/yr vs Salesforce</span></li>
          </ul>

          <button class="plan-cta-btn primary" @click="selectPlanAndRegister('luxury')">
            Start 7-Day Free Trial &rarr;
          </button>
        </div>

        <!-- Tier 3: Executive Suite -->
        <div class="landing-plan-card">
          <div class="tier-badge">ESTABLISHED FIRM</div>
          <h3 class="tier-name">Executive Suite</h3>
          <p class="tier-desc">For mid-size corporations, regional firms &amp; multi-branch groups.</p>
          <div class="tier-price">
            <span class="currency">R</span>1,500<span class="period">/month</span>
          </div>
          <div class="seat-pill">Up to 15 Users Included (~R100/seat)</div>

          <ul class="tier-features">
            <li><strong>Everything in Luxury Team, plus:</strong></li>
            <li><strong>Up to 15 executive &amp; staff seats</strong></li>
            <li>Multi-branch / department filtering</li>
            <li>Executive KPI scoreboard &amp; custom reports</li>
            <li>Automated email trigger workflows</li>
            <li>POPIA Section 19 compliance vault</li>
            <li>Priority Concierge WhatsApp &amp; Phone</li>
          </ul>

          <button class="plan-cta-btn secondary" @click="selectPlanAndRegister('executive')">
            Start 7-Day Free Trial &rarr;
          </button>
        </div>

        <!-- Tier 4: Enterprise Custom -->
        <div class="landing-plan-card enterprise">
          <div class="tier-badge">INSTITUTIONAL FLEET</div>
          <h3 class="tier-name">Enterprise Custom</h3>
          <p class="tier-desc">For large fleets, bespoke infrastructure &amp; institutional compliance.</p>
          <div class="tier-price">
            <span class="custom-rate">Custom Quote</span>
          </div>
          <div class="seat-pill">15+ Dedicated Seats</div>

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

      <!-- Bottom Returning User Bar -->
      <div class="landing-returning-bar">
        <div class="returning-text">
          👑 <strong>Already an Authorized Executive?</strong> Return to your private enterprise command deck.
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
    }
  },
  computed: {
    cardStyle() {
      if (this.containerWidth === 0) return {}
      const centerX = this.containerWidth / 2
      const centerY = this.containerHeight / 2
      const rotateY = ((this.mouseX - centerX) / centerX) * 15
      const rotateX = -((this.mouseY - centerY) / centerY) * 15
      return {
        transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
      }
    },
    glareStyle() {
      if (this.containerWidth === 0) return { opacity: 0 }
      const percentX = (this.mouseX / this.containerWidth) * 100
      const percentY = (this.mouseY / this.containerHeight) * 100
      return {
        background: `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(212, 175, 55, 0.4) 0%, transparent 60%)`,
        opacity: 1
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
  transition: all 0.2s;
  padding: 0.5rem 0.75rem;
}

.nav-link-btn:hover {
  color: #d4af37;
}

.nav-trial-btn {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #d4af37;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0.5rem 1.1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-trial-btn:hover {
  background: rgba(212, 175, 55, 0.25);
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
}

.nav-login-btn {
  background: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
  border: none;
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 1px;
  padding: 0.55rem 1.25rem;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(212, 175, 55, 0.35);
  transition: all 0.2s;
}

.nav-login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
}

.center-stage {
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 10;
  padding: 3rem 2rem;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.packages-scroll-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e2e8f0;
  padding: 1rem 2rem;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.packages-scroll-btn:hover {
  border-color: #d4af37;
  color: #d4af37;
  background: rgba(212, 175, 55, 0.08);
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
  max-width: 700px;
  margin: 0 auto 2rem;
  color: #94a3b8;
  font-size: 0.95rem;
  line-height: 1.6;
}

.vat-strip {
  max-width: 680px;
  margin: 0 auto 3rem;
  background: rgba(34, 197, 94, 0.08);
  border: 1px solid rgba(34, 197, 94, 0.25);
  border-radius: 999px;
  padding: 8px 20px;
  text-align: center;
  font-size: 0.8rem;
  color: #86efac;
}

.landing-plans-grid {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  align-items: stretch;
}

.landing-plan-card {
  background: linear-gradient(180deg, #0d131f 0%, #080c14 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 2.25rem 1.75rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.landing-plan-card:hover {
  transform: translateY(-4px);
  border-color: rgba(212, 175, 55, 0.4);
  box-shadow: 0 20px 40px rgba(0,0,0,0.8), 0 0 20px rgba(212, 175, 55, 0.15);
}

.landing-plan-card.featured {
  border: 1.5px solid #d4af37;
  background: linear-gradient(180deg, #131c2e 0%, #0c121e 100%);
  box-shadow: 0 15px 45px rgba(0,0,0,0.7), 0 0 30px rgba(212, 175, 55, 0.2);
}

.popular-ribbon {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(90deg, #d4af37, #f59e0b);
  color: #000;
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 1px;
  padding: 4px 12px;
  border-radius: 999px;
  white-space: nowrap;
  box-shadow: 0 2px 10px rgba(212, 175, 55, 0.4);
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
