<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="tutorial-overlay" @click.self="closeModal">
      <div class="tutorial-modal luxury-theme">
        <!-- Header -->
        <div class="tutorial-header">
          <div class="header-left">
            <div class="tour-badge">
              <span class="pulse-dot"></span> EXECUTIVE SYSTEM TOUR &bull; 4K MATRIX
            </div>
            <h2>Mastering THE FINISHER LUXURY</h2>
            <p class="tour-sub">Interactive walkthrough of client data isolation, deals, automated lead ads, and workflow engines.</p>
          </div>
          <button class="btn-close" @click="closeModal">&times;</button>
        </div>

        <!-- Main Body -->
        <div class="tutorial-body">
          <!-- Video / Simulation Showcase Stage -->
          <div class="video-stage-container">
            <div class="screen-frame">
              <!-- Top bar of mock interface -->
              <div class="mock-topbar">
                <div class="mock-dots">
                  <span class="dot red"></span>
                  <span class="dot yellow"></span>
                  <span class="dot green"></span>
                </div>
                <div class="mock-title font-mono">
                  thefinisher.luxury / {{ activeChapter.slug }} [LIVE]
                </div>
                <div class="mock-badge font-mono">POPIA S19 LOCKED</div>
              </div>

              <!-- Animated Stage View based on active chapter -->
              <div class="mock-canvas">
                <!-- Chapter 1: Dashboard -->
                <div v-if="activeChapterIndex === 0" class="canvas-slide slide-dashboard">
                  <div class="mock-kpis">
                    <div class="mock-kpi gold"><span class="k-label">Pipeline Value</span><span class="k-val">R 2,450,000</span></div>
                    <div class="mock-kpi blue"><span class="k-label">Verified Clients</span><span class="k-val">128</span></div>
                    <div class="mock-kpi purple"><span class="k-label">Facebook Ingest</span><span class="k-val">42 Leads</span></div>
                  </div>
                  <div class="mock-chart-visual">
                    <div class="bar h-60"></div>
                    <div class="bar h-80"></div>
                    <div class="bar h-40"></div>
                    <div class="bar h-95 gold"></div>
                    <div class="bar h-70"></div>
                  </div>
                  <div class="stage-overlay-text">
                    ✦ Executive Dashboard &bull; Live Telemetry Matrix
                  </div>
                </div>

                <!-- Chapter 2: Client & CIPC -->
                <div v-else-if="activeChapterIndex === 1" class="canvas-slide slide-clients">
                  <div class="mock-client-card">
                    <div class="card-avatar">🏢</div>
                    <div class="card-info">
                      <h4>Anglo American Platinum Ltd</h4>
                      <span class="badge-cipc">✓ CIPC Verified Entity &bull; 2024/104928/07</span>
                      <p>POPIA Section 19 strict tenant boundary &bull; Zero cross-client leakage</p>
                    </div>
                  </div>
                  <div class="stage-overlay-text">
                    ✦ Multi-Tenant Client Data Isolation &bull; POPIA S19 Protected
                  </div>
                </div>

                <!-- Chapter 3: Deals & Pipeline -->
                <div v-else-if="activeChapterIndex === 2" class="canvas-slide slide-deals">
                  <div class="mock-kanban">
                    <div class="mock-col">
                      <span class="col-title">Lead (3)</span>
                      <div class="mock-deal-item">Corporate Fleet &bull; R450k</div>
                    </div>
                    <div class="mock-col">
                      <span class="col-title">Proposal (2)</span>
                      <div class="mock-deal-item gold-border">Sandton VIP Suite &bull; R1.2M</div>
                    </div>
                    <div class="mock-col">
                      <span class="col-title">Closed Won</span>
                      <div class="mock-deal-item green-border">Annual Retainer &bull; R800k</div>
                    </div>
                  </div>
                  <div class="stage-overlay-text">
                    ✦ Drag-and-Drop Deal Pipeline &bull; Negative Working Capital System
                  </div>
                </div>

                <!-- Chapter 4: Integrations Hub -->
                <div v-else-if="activeChapterIndex === 3" class="canvas-slide slide-integrations">
                  <div class="mock-int-grid">
                    <div class="mock-int-card active"><span class="icon">📘</span> Meta / Facebook Ads <span class="badge-green">Instant Webhook</span></div>
                    <div class="mock-int-card active"><span class="icon">🔴</span> Google Workspace <span class="badge-green">Connected</span></div>
                    <div class="mock-int-card active"><span class="icon">🔷</span> Microsoft 365 <span class="badge-green">Connected</span></div>
                    <div class="mock-int-card active"><span class="icon">💬</span> WhatsApp Cloud <span class="badge-green">Active</span></div>
                  </div>
                  <div class="stage-overlay-text">
                    ✦ Meta Lead Ads Ingestion &bull; Google &amp; Microsoft Email Engines
                  </div>
                </div>

                <!-- Chapter 5: Workflows & Campaigns -->
                <div v-else class="canvas-slide slide-workflows">
                  <div class="mock-workflow-flow">
                    <div class="wf-node trigger">⚡ TRIGGER: Meta Lead Submitted</div>
                    <div class="wf-line">↓</div>
                    <div class="wf-node action">✉️ ACTION: Send VIP Proposal Template</div>
                    <div class="wf-line">↓</div>
                    <div class="wf-node notify">🔔 NOTIFY: Executive WhatsApp &amp; In-App Alert</div>
                  </div>
                  <div class="stage-overlay-text">
                    ✦ Autonomous Multi-Step Workflows &bull; 10-Second Automation Trigger
                  </div>
                </div>
              </div>

              <!-- Media Player Controls Bar -->
              <div class="player-controls">
                <button class="btn-play" @click="togglePlay">
                  {{ isPlaying ? '⏸ Pause' : '▶ Play Tour' }}
                </button>
                <div class="progress-track" @click="handleScrub">
                  <div class="progress-fill" :style="{ width: `${progressPercent}%` }"></div>
                </div>
                <span class="time-readout font-mono">{{ currentTimeFormatted }} / 02:30</span>
              </div>
            </div>

            <!-- Chapter Selection Tabs -->
            <div class="chapter-strip">
              <button 
                v-for="(chap, idx) in chapters" 
                :key="chap.id"
                :class="['chap-btn', { active: activeChapterIndex === idx }]"
                @click="selectChapter(idx)"
              >
                <span class="chap-num">0{{ idx + 1 }}</span>
                <span class="chap-title">{{ chap.title }}</span>
              </button>
            </div>
          </div>

          <!-- Feature Takeaway & Action Deck -->
          <div class="chapter-details-card">
            <div class="details-header">
              <span class="chapter-counter">CHAPTER {{ activeChapterIndex + 1 }} OF {{ chapters.length }}</span>
              <h3>{{ activeChapter.headline }}</h3>
              <p class="chapter-desc">{{ activeChapter.description }}</p>
            </div>

            <!-- Pro-Tip / Business Model Card -->
            <div class="pro-tip-box">
              <div class="tip-icon">💡</div>
              <div class="tip-body">
                <strong>EXECUTIVE BILLIONAIRE STRATEGY:</strong>
                <p>{{ activeChapter.proTip }}</p>
              </div>
            </div>

            <!-- Action Navigation -->
            <div class="details-actions">
              <button class="btn btn-gold" @click="jumpToModule(activeChapter.route)">
                🚀 Launch {{ activeChapter.title }} Module
              </button>
              <button class="btn btn-secondary" @click="nextChapter">
                Next Chapter →
              </button>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="tutorial-footer">
          <label class="remember-check">
            <input type="checkbox" v-model="dontShowAgain" @change="savePreference" />
            <span>Do not show this tutorial automatically on login</span>
          </label>
          <button class="btn btn-secondary btn-sm" @click="closeModal">
            Dismiss &amp; Continue
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'SystemTutorialModal',
  data() {
    return {
      isOpen: false,
      isPlaying: true,
      activeChapterIndex: 0,
      progressPercent: 20,
      playTimer: null,
      dontShowAgain: localStorage.getItem('tfl_tutorial_seen') === 'true',
      chapters: [
        {
          id: 'dashboard',
          slug: 'dashboard',
          title: 'Dashboard',
          headline: 'Executive Dashboard & Real-Time Intelligence Matrix',
          description: 'Unified command center featuring live KPI counters, pipeline valuations, world clock matrix, and customizable analytical widgets.',
          proTip: 'Keep tabs on customer acquisition costs and average deal velocity. Fast-growing enterprises monitor daily pipeline expansion over raw headcount.',
          route: '/dashboard'
        },
        {
          id: 'clients',
          slug: 'contacts',
          title: 'Clients & CIPC',
          headline: 'POPIA Section 19 Client Silos & CIPC Verification',
          description: 'Complete data protection barrier. Every client and company record is strictly partitioned to your tenant organization with full CIPC registration lookup.',
          proTip: 'Treat customer data privacy as a premium enterprise moat. Zero data leakage builds trust with corporate partners worth tens of millions.',
          route: '/contacts'
        },
        {
          id: 'deals',
          slug: 'deals',
          title: 'Deal Pipeline',
          headline: 'Drag-and-Drop Deal Pipeline & Quotation Engine',
          description: 'Visualize high-value transactions from initial lead to closed won. Generate official commercial quotations and track negative working capital advances.',
          proTip: 'Billionaire operators collect annual upfront payments before delivering enterprise services, creating negative working capital that self-funds expansion.',
          route: '/deals'
        },
        {
          id: 'integrations',
          slug: 'integrations',
          title: 'Integrations Hub',
          headline: 'Meta Facebook Lead Ads, Gmail & Outlook Connectors',
          description: 'Real-time HTTPS webhook ingestion. Incoming Facebook and Instagram ad inquiries are instantly converted into Website Leads with zero manual entry.',
          proTip: 'Speed to lead is everything. Responding to social inquiries within 60 seconds increases conversion velocity by over 391%.',
          route: '/integrations'
        },
        {
          id: 'workflows',
          slug: 'workflows',
          title: 'Workflows',
          headline: 'Autonomous Trigger-Action Workflows & Email Campaigns',
          description: 'Automate repetitive outreach, send scheduled email newsletters, fire executive WhatsApp alerts, and trigger ticket assignments autonomously.',
          proTip: 'Scale systems that run without human bottleneck. An automated multi-step outreach pipeline works 24 hours a day with zero human fatigue.',
          route: '/workflows'
        }
      ]
    }
  },
  computed: {
    activeChapter() {
      return this.chapters[this.activeChapterIndex]
    },
    currentTimeFormatted() {
      const totalSecs = 150
      const currentSecs = Math.floor((this.progressPercent / 100) * totalSecs)
      const mins = String(Math.floor(currentSecs / 60)).padStart(2, '0')
      const secs = String(currentSecs % 60).padStart(2, '0')
      return `${mins}:${secs}`
    }
  },
  mounted() {
    // Check if auto-launch is required
    const seen = localStorage.getItem('tfl_tutorial_seen')
    const hasToken = localStorage.getItem('thefinisher_access_token')
    const publicPaths = ['/login', '/register', '/forgot-password', '/verify-otp', '/']

    if (hasToken && !seen && !publicPaths.includes(this.$route?.path)) {
      this.isOpen = true
      this.startPlayback()
    }

    window.addEventListener('open-system-tutorial', this.openModal)
  },
  beforeUnmount() {
    this.stopPlayback()
    window.removeEventListener('open-system-tutorial', this.openModal)
  },
  methods: {
    openModal() {
      this.isOpen = true
      this.startPlayback()
    },

    closeModal() {
      this.isOpen = false
      this.stopPlayback()
    },

    togglePlay() {
      this.isPlaying = !this.isPlaying
      if (this.isPlaying) {
        this.startPlayback()
      } else {
        this.stopPlayback()
      }
    },

    startPlayback() {
      this.stopPlayback()
      this.playTimer = setInterval(() => {
        if (!this.isPlaying) return
        this.progressPercent += 1.5
        if (this.progressPercent >= 100) {
          this.progressPercent = 0
          this.activeChapterIndex = (this.activeChapterIndex + 1) % this.chapters.length
        } else {
          const targetIndex = Math.floor((this.progressPercent / 100) * this.chapters.length)
          if (targetIndex !== this.activeChapterIndex && targetIndex < this.chapters.length) {
            this.activeChapterIndex = targetIndex
          }
        }
      }, 500)
    },

    stopPlayback() {
      if (this.playTimer) {
        clearInterval(this.playTimer)
        this.playTimer = null
      }
    },

    selectChapter(index) {
      this.activeChapterIndex = index
      this.progressPercent = (index / this.chapters.length) * 100
    },

    nextChapter() {
      const next = (this.activeChapterIndex + 1) % this.chapters.length
      this.selectChapter(next)
    },

    handleScrub(e) {
      const rect = e.currentTarget.getBoundingClientRect()
      const clickX = e.clientX - rect.left
      const pct = Math.max(0, Math.min(100, (clickX / rect.width) * 100))
      this.progressPercent = pct
      const idx = Math.min(this.chapters.length - 1, Math.floor((pct / 100) * this.chapters.length))
      this.activeChapterIndex = idx
    },

    savePreference() {
      if (this.dontShowAgain) {
        localStorage.setItem('tfl_tutorial_seen', 'true')
      } else {
        localStorage.removeItem('tfl_tutorial_seen')
      }
    },

    jumpToModule(route) {
      this.closeModal()
      this.$router.push(route)
    }
  }
}
</script>

<style scoped>
.tutorial-overlay {
  position: fixed;
  inset: 0;
  background: rgba(5, 7, 14, 0.9);
  backdrop-filter: blur(14px);
  z-index: 100001;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.tutorial-modal {
  background: #0f121d;
  border: 1px solid rgba(212, 175, 55, 0.4);
  border-radius: 20px;
  width: 100%;
  max-width: 980px;
  max-height: 92vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(212, 175, 55, 0.2);
  color: #e2e8f0;
  overflow: hidden;
}

/* Header */
.tutorial-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: linear-gradient(180deg, rgba(212, 175, 55, 0.08) 0%, transparent 100%);
}

.tour-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  font-weight: 800;
  color: #d4af37;
  letter-spacing: 1px;
  margin-bottom: 4px;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px #10b981;
}

.tutorial-header h2 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 800;
  color: #ffffff;
}

.tour-sub {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 4px 0 0;
}

.btn-close {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.8rem;
  cursor: pointer;
  line-height: 1;
}

/* Body */
.tutorial-body {
  padding: 1.75rem 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Video / Simulator Container */
.video-stage-container {
  background: #080a10;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.mock-topbar {
  background: #151824;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.mock-dots {
  display: flex;
  gap: 6px;
}

.mock-dots .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.dot.red { background: #ef4444; }
.dot.yellow { background: #eab308; }
.dot.green { background: #10b981; }

.mock-title {
  font-size: 0.72rem;
  color: #94a3b8;
}

.mock-badge {
  font-size: 0.65rem;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  padding: 2px 6px;
  border-radius: 4px;
}

/* Canvas Slide */
.mock-canvas {
  height: 220px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at center, #161a29 0%, #080a11 100%);
  padding: 1.5rem;
  overflow: hidden;
}

.stage-overlay-text {
  position: absolute;
  bottom: 12px;
  left: 16px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #d4af37;
  letter-spacing: 0.5px;
  background: rgba(0, 0, 0, 0.6);
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(212, 175, 55, 0.2);
}

/* Slide 1: Dashboard */
.slide-dashboard {
  width: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.mock-kpis {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.mock-kpi {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 6px 12px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
}
.k-label { font-size: 0.65rem; color: #94a3b8; }
.k-val { font-size: 1rem; font-weight: 700; color: #ffffff; }
.mock-kpi.gold { border-left: 3px solid #d4af37; }
.mock-kpi.blue { border-left: 3px solid #3b82f6; }
.mock-kpi.purple { border-left: 3px solid #a855f7; }

.mock-chart-visual {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 120px;
}
.mock-chart-visual .bar {
  width: 20px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease;
}
.bar.h-60 { height: 60px; }
.bar.h-80 { height: 80px; }
.bar.h-40 { height: 40px; }
.bar.h-95 { height: 95px; background: #d4af37 !important; box-shadow: 0 0 10px #d4af37; }
.bar.h-70 { height: 70px; }

/* Slide 2: Clients */
.slide-clients {
  width: 100%;
  display: flex;
  justify-content: center;
}
.mock-client-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 1.25rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  max-width: 480px;
}
.card-avatar {
  font-size: 2.2rem;
  width: 56px;
  height: 56px;
  background: rgba(212, 175, 55, 0.15);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-info h4 { margin: 0 0 4px; font-size: 1.05rem; color: #fff; }
.badge-cipc { font-size: 0.72rem; color: #10b981; font-weight: 700; display: block; margin-bottom: 4px; }
.card-info p { font-size: 0.78rem; color: #94a3b8; margin: 0; }

/* Slide 3: Deals */
.slide-deals { width: 100%; }
.mock-kanban { display: flex; gap: 1rem; width: 100%; justify-content: center; }
.mock-col { background: rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 10px; width: 160px; }
.col-title { font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; display: block; }
.mock-deal-item { background: rgba(255, 255, 255, 0.06); padding: 8px; border-radius: 6px; font-size: 0.75rem; color: #fff; margin-bottom: 6px; }
.gold-border { border-left: 3px solid #d4af37; }
.green-border { border-left: 3px solid #10b981; }

/* Slide 4: Integrations */
.slide-integrations { width: 100%; }
.mock-int-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-width: 500px; margin: 0 auto; }
.mock-int-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); padding: 10px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }
.badge-green { font-size: 0.65rem; color: #10b981; background: rgba(16, 185, 129, 0.15); padding: 2px 6px; border-radius: 4px; }

/* Slide 5: Workflows */
.slide-workflows { width: 100%; }
.mock-workflow-flow { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.wf-node { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 6px 14px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; color: #fff; }
.wf-node.trigger { border-color: #d4af37; color: #d4af37; }
.wf-line { font-size: 0.7rem; color: #64748b; }

/* Player Controls */
.player-controls {
  background: #111420;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.btn-play {
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: #d4af37;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.progress-track {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37 0%, #10b981 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.time-readout {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Chapter Selection Strip */
.chapter-strip {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  background: #0d101a;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.chap-btn {
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  padding: 10px 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chap-btn:hover {
  background: rgba(255, 255, 255, 0.03);
}

.chap-btn.active {
  background: rgba(212, 175, 55, 0.08);
  border-bottom-color: #d4af37;
}

.chap-num {
  display: block;
  font-size: 0.65rem;
  color: #64748b;
  font-family: monospace;
}

.chap-btn.active .chap-num {
  color: #d4af37;
}

.chap-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: #cbd5e1;
}

.chap-btn.active .chap-title {
  color: #ffffff;
}

/* Chapter Details Card */
.chapter-details-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-counter {
  font-size: 0.68rem;
  font-weight: 800;
  color: #d4af37;
  letter-spacing: 1px;
}

.details-header h3 {
  margin: 4px 0 6px;
  font-size: 1.2rem;
  color: #ffffff;
}

.chapter-desc {
  font-size: 0.88rem;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0;
}

.pro-tip-box {
  background: rgba(212, 175, 55, 0.06);
  border: 1px dashed rgba(212, 175, 55, 0.3);
  border-radius: 8px;
  padding: 0.9rem 1.1rem;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.tip-icon {
  font-size: 1.3rem;
}

.tip-body strong {
  font-size: 0.75rem;
  color: #d4af37;
  letter-spacing: 0.5px;
  display: block;
  margin-bottom: 2px;
}

.tip-body p {
  font-size: 0.82rem;
  color: #e2e8f0;
  margin: 0;
  line-height: 1.4;
}

.details-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* Footer */
.tutorial-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: #0c0e17;
}

.remember-check {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.78rem;
  color: #94a3b8;
  cursor: pointer;
}

.remember-check input {
  accent-color: #d4af37;
}

.btn-gold {
  background: linear-gradient(135deg, #d4af37 0%, #b8972f 100%);
  color: #0b0f19;
  border: none;
  font-weight: 700;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
</style>
