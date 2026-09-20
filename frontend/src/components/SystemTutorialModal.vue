<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="tutorial-overlay" @click.self="closeModal">
      <div class="tutorial-modal luxury-theme">
        <!-- Header -->
        <div class="tutorial-header">
          <div class="header-left">
            <div class="tour-badge">
              <span class="pulse-dot"></span> EXECUTIVE MASTERCLASS &bull; 4K MEDIA PLAYER
            </div>
            <h2>Mastering THE FINISHER LUXURY</h2>
            <p class="tour-sub">Comprehensive executive onboarding: client data isolation, deals, automated lead ads, and statutory compliance.</p>
          </div>
          <div class="header-right">
            <button class="btn-source-toggle" @click="showUrlInput = !showUrlInput" title="Switch or embed custom video URL">
              {{ showUrlInput ? '✕ Close URL' : '🔗 Video Source' }}
            </button>
            <button class="btn-close" @click="closeModal">&times;</button>
          </div>
        </div>

        <!-- Optional URL input bar for custom stream/CDN/YouTube -->
        <div v-if="showUrlInput" class="video-url-bar">
          <input 
            type="text" 
            v-model="customVideoUrl" 
            placeholder="Paste MP4, Loom, or embed link (e.g., https://cdn.example.com/tutorial.mp4)..." 
            class="url-input"
            @keyup.enter="applyCustomUrl"
          />
          <button class="btn-apply-url" @click="applyCustomUrl">Apply Video</button>
          <button class="btn-reset-url" @click="resetToDefaultVideo">Reset to Default</button>
        </div>

        <!-- Main Body -->
        <div class="tutorial-body">
          <!-- Video Player Showcase Stage -->
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
                  thefinisher.luxury / onboarding-player &bull; Chapter {{ activeChapterIndex + 1 }}: {{ activeChapter.title }}
                </div>
                <div class="mock-badge font-mono">POPIA S19 &bull; TLS 1.3</div>
              </div>

              <!-- Media Player Stage -->
              <div class="media-stage-viewport">
                <!-- 1. Real Video Player (If active) -->
                <div v-if="hasPlayableVideo" class="video-player-box">
                  <video
                    ref="masterVideo"
                    class="embedded-media-element"
                    :src="activeVideoSource"
                    controls
                    playsinline
                    :poster="activeChapter.poster"
                    @timeupdate="onVideoTimeUpdate"
                    @play="isVideoPlaying = true"
                    @pause="isVideoPlaying = false"
                    @ended="onVideoEnded"
                    @error="onVideoError"
                  >
                    Your browser does not support the video tag.
                  </video>
                </div>

                <!-- 2. Fallback Studio Carousel (Before user uploads MP4) -->
                <div v-else class="video-fallback-box" :style="{ backgroundImage: `url(${activeChapter.poster})` }">
                  <div class="fallback-glass-scrim">
                    <div class="player-ready-badge">
                      <span class="glow-icon">🎬</span>
                      <div>
                        <strong>4K LUXURY MEDIA PLAYER EMBEDDED</strong>
                        <p>Place your generated video in <code>/public/videos/master_tutorial.mp4</code> or click "🔗 Video Source" above.</p>
                      </div>
                    </div>

                    <div class="active-slide-caption">
                      <span class="caption-tag">CHAPTER {{ activeChapterIndex + 1 }} &bull; {{ activeChapter.timestamp }}</span>
                      <h4>{{ activeChapter.headline }}</h4>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Player Chapter Quick-Seek Controls Bar -->
              <div class="player-controls">
                <button class="btn-play" @click="togglePlay">
                  {{ isPlaying ? '⏸ Pause' : '▶ Play Tutorial' }}
                </button>
                <div class="progress-track" @click="handleScrub">
                  <div class="progress-fill" :style="{ width: `${progressPercent}%` }"></div>
                  <!-- Chapter cue points on timeline -->
                  <div 
                    v-for="(chap, idx) in chapters" 
                    :key="chap.id" 
                    class="chapter-cue-point"
                    :style="{ left: `${(idx / (chapters.length - 1)) * 100}%` }"
                    :title="`${chap.title} (${chap.timestamp})`"
                  ></div>
                </div>
                <span class="time-readout font-mono">{{ currentTimeFormatted }} / {{ totalDurationFormatted }}</span>
              </div>
            </div>

            <!-- Chapter Selection Tabs (All 9 Modules) -->
            <div class="chapter-strip">
              <button 
                v-for="(chap, idx) in chapters" 
                :key="chap.id"
                :class="['chap-btn', { active: activeChapterIndex === idx }]"
                @click="selectChapter(idx)"
              >
                <span class="chap-num">0{{ idx + 1 }}</span>
                <span class="chap-title">{{ chap.title }}</span>
                <span class="chap-time font-mono">{{ chap.timestamp }}</span>
              </button>
            </div>
          </div>

          <!-- Feature Takeaway & Action Deck -->
          <div class="chapter-details-card">
            <div class="details-header">
              <span class="chapter-counter">CHAPTER {{ activeChapterIndex + 1 }} OF {{ chapters.length }} &bull; {{ activeChapter.timestamp }}</span>
              <h3>{{ activeChapter.headline }}</h3>
              <p class="chapter-desc">{{ activeChapter.description }}</p>
            </div>

            <!-- Pro-Tip / Billionaire Business Model Card -->
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
      isPlaying: false,
      hasPlayableVideo: true,
      activeVideoSource: '/videos/master_tutorial.mp4',
      customVideoUrl: '',
      showUrlInput: false,
      activeChapterIndex: 0,
      progressPercent: 0,
      playTimer: null,
      videoDuration: 180, // Default 3 minutes (180s)
      dontShowAgain: localStorage.getItem('tfl_tutorial_seen') === 'true',
      chapters: [
        {
          id: 'dashboard',
          title: 'Command Center',
          timestamp: '00:00',
          startSec: 0,
          poster: '/screenshots/01_executive_dashboard.png',
          headline: 'Executive Dashboard & R64.5M Pipeline Telemetry',
          description: 'High-altitude visibility over active opportunities, deal conversion velocity, cashflow projections, and team pipeline distribution.',
          proTip: 'Billionaire operators monitor pipeline velocity daily. Speed of deal flow is the leading indicator of company valuation.',
          route: '/dashboard'
        },
        {
          id: 'contacts',
          title: 'VIP Contacts',
          timestamp: '00:20',
          startSec: 20,
          poster: '/screenshots/02_clients_contacts.png',
          headline: 'Corporate B2B Stakeholders & Decision Makers',
          description: 'Capture key executive sponsors, direct lines, and tax IDs. Every contact is permanently partitioned with zero cross-tenant leakage.',
          proTip: 'Multi-million Rand deals are closed with people, not logos. Maintain direct communication with the real signing authorities.',
          route: '/contacts'
        },
        {
          id: 'companies',
          title: 'CIPC Businesses',
          timestamp: '00:40',
          startSec: 40,
          poster: '/screenshots/03_companies_directory.png',
          headline: 'Verified Corporate Business Directory',
          description: 'Official enterprise business records verified against CIPC registration numbers, eliminating duplicate and ghost client records.',
          proTip: 'Institutional compliance is a competitive moat. Verified enterprise records allow clients to pass institutional vendor audits.',
          route: '/companies'
        },
        {
          id: 'deals',
          title: 'Deals & Splits',
          timestamp: '01:00',
          startSec: 60,
          poster: '/screenshots/04_deals_pipeline.png',
          headline: 'Deal Pipeline & Instant PayFast Split Settlement',
          description: 'Kanban pipeline with real-time billable advisory hour timers, instant PDF quote generation, and 1-click PayFast split escrow settlement.',
          proTip: 'Tollbooth business model: Collecting an automated 2-3% platform slice on high-ticket closed deals creates permanent recurring cashflow.',
          route: '/deals'
        },
        {
          id: 'integrations',
          title: 'Webhooks & Speed',
          timestamp: '01:30',
          startSec: 90,
          poster: '/screenshots/05_payfast_integrations.png',
          headline: 'Enterprise Integrations & 10-Second Auto-Outreach',
          description: 'Zero-latency webhooks ingest Meta lead ads and WhatsApp Business queries, triggering automated executive responses within 10 seconds.',
          proTip: 'Speed to lead: Responding to corporate inquiries in under 60 seconds increases deal closure probability by over 300%.',
          route: '/integrations'
        },

        {
          id: 'enablement',
          title: 'Executive SOP',
          timestamp: '02:20',
          startSec: 140,
          poster: '/screenshots/07_help_and_enablement.png',
          headline: '5-Step Standard Operating Protocol',
          description: 'Institutional guidelines training corporate staff in data discipline, contact onboarding, and enterprise deal execution.',
          proTip: 'Standardization unlocks valuation. Systems that run with documented operational discipline command 10x higher enterprise multiples.',
          route: '/help'
        },
        {
          id: 'onboarding',
          title: 'Workspace Access',
          timestamp: '02:40',
          startSec: 160,
          poster: '/screenshots/08_registration_onboarding.png',
          headline: 'Rapid 3-Step Workspace Provisioning',
          description: 'Frictionless executive onboarding with dual navigation buttons and automated tenant cryptographic isolation.',
          proTip: 'Eliminate registration dead-ends. Smooth enterprise onboarding converts curious executives into lifetime corporate advocates.',
          route: '/register'
        },
        {
          id: 'governance',
          title: 'Team Security',
          timestamp: '02:55',
          startSec: 175,
          poster: '/screenshots/09_employee_directory.png',
          headline: 'Zero-Trust Role-Based Access Control',
          description: 'Strict security boundaries ensuring staff access only authorized modules, protecting proprietary corporate IP.',
          proTip: 'Security is currency. Enterprise enterprise customers will pay 5x premiums for systems that guarantee absolute employee data isolation.',
          route: '/employees'
        }
      ]
    }
  },
  computed: {
    activeChapter() {
      return this.chapters[this.activeChapterIndex]
    },
    currentTimeFormatted() {
      const currentSecs = Math.floor((this.progressPercent / 100) * this.videoDuration)
      const mins = String(Math.floor(currentSecs / 60)).padStart(2, '0')
      const secs = String(currentSecs % 60).padStart(2, '0')
      return `${mins}:${secs}`
    },
    totalDurationFormatted() {
      const mins = String(Math.floor(this.videoDuration / 60)).padStart(2, '0')
      const secs = String(this.videoDuration % 60).padStart(2, '0')
      return `${mins}:${secs}`
    }
  },
  mounted() {
    // Check if video file exists via silent HEAD request
    this.detectPlayableVideo()

    // Check if auto-launch is required for new users
    const seen = localStorage.getItem('tfl_tutorial_seen')
    const hasToken = localStorage.getItem('thefinisher_access_token')
    const publicPaths = ['/login', '/register', '/forgot-password', '/verify-otp', '/']

    // Strict Once-Only Policy: only launch automatically for a fresh user ONCE, and NEVER again
    if (hasToken && !seen && !publicPaths.includes(this.$route?.path)) {
      this.isOpen = true
      localStorage.setItem('tfl_tutorial_seen', 'true')
      localStorage.setItem('thefinisher_tutorial_state', 'completed')
      this.startPlayback()
    }

    window.addEventListener('open-system-tutorial', this.openModal)
  },
  beforeUnmount() {
    this.stopPlayback()
    window.removeEventListener('open-system-tutorial', this.openModal)
  },
  methods: {
    async detectPlayableVideo() {
      if (this.activeVideoSource === '/videos/master_tutorial.mp4') {
        this.hasPlayableVideo = true
        return
      }
      try {
        const res = await fetch(this.activeVideoSource, { method: 'HEAD' })
        this.hasPlayableVideo = res.ok
      } catch (_) {
        this.hasPlayableVideo = true
      }
    },

    openModal() {
      this.isOpen = true
      this.detectPlayableVideo()
    },

    closeModal() {
      this.isOpen = false
      localStorage.setItem('tfl_tutorial_seen', 'true')
      localStorage.setItem('thefinisher_tutorial_state', 'completed')
      this.pauseVideo()
      this.stopPlayback()
    },

    togglePlay() {
      this.isPlaying = !this.isPlaying
      if (this.hasPlayableVideo && this.$refs.masterVideo) {
        if (this.isPlaying) {
          this.$refs.masterVideo.play().catch(() => {})
        } else {
          this.$refs.masterVideo.pause()
        }
      } else {
        if (this.isPlaying) {
          this.startSimulationTimer()
        } else {
          this.stopPlayback()
        }
      }
    },

    pauseVideo() {
      this.isPlaying = false
      if (this.$refs.masterVideo) {
        this.$refs.masterVideo.pause()
      }
    },

    selectChapter(index) {
      this.activeChapterIndex = index
      const chapter = this.chapters[index]
      this.progressPercent = (chapter.startSec / this.videoDuration) * 100

      if (this.hasPlayableVideo && this.$refs.masterVideo) {
        this.$refs.masterVideo.currentTime = chapter.startSec
        this.$refs.masterVideo.play().catch(() => {})
        this.isPlaying = true
      }
    },

    nextChapter() {
      const nextIdx = (this.activeChapterIndex + 1) % this.chapters.length
      this.selectChapter(nextIdx)
    },

    handleScrub(event) {
      const rect = event.currentTarget.getBoundingClientRect()
      const clickX = event.clientX - rect.left
      const percent = Math.max(0, Math.min(100, (clickX / rect.width) * 100))
      this.progressPercent = percent
      const targetSec = (percent / 100) * this.videoDuration

      if (this.hasPlayableVideo && this.$refs.masterVideo) {
        this.$refs.masterVideo.currentTime = targetSec
      }

      // Sync active chapter based on timestamp
      for (let i = this.chapters.length - 1; i >= 0; i--) {
        if (targetSec >= this.chapters[i].startSec) {
          this.activeChapterIndex = i
          break
        }
      }
    },

    onVideoTimeUpdate(e) {
      const video = e.target
      if (!video || !video.duration) return
      this.videoDuration = Math.round(video.duration)
      const current = video.currentTime
      this.progressPercent = (current / video.duration) * 100

      for (let i = this.chapters.length - 1; i >= 0; i--) {
        if (current >= this.chapters[i].startSec) {
          this.activeChapterIndex = i
          break
        }
      }
    },

    onVideoEnded() {
      this.isPlaying = false
      this.progressPercent = 100
    },

    onVideoError() {
      this.hasPlayableVideo = false
    },

    applyCustomUrl() {
      if (this.customVideoUrl.trim()) {
        this.activeVideoSource = this.customVideoUrl.trim()
        this.hasPlayableVideo = true
        this.showUrlInput = false
        this.$nextTick(() => {
          if (this.$refs.masterVideo) {
            this.$refs.masterVideo.load()
            this.$refs.masterVideo.play().catch(() => {})
            this.isPlaying = true
          }
        })
      }
    },

    resetToDefaultVideo() {
      this.customVideoUrl = ''
      this.activeVideoSource = '/videos/master_tutorial.mp4'
      this.detectPlayableVideo()
      this.showUrlInput = false
    },

    startPlayback() {
      this.isPlaying = true
      if (this.hasPlayableVideo && this.$refs.masterVideo) {
        this.$refs.masterVideo.play().catch(() => {})
      } else {
        this.startSimulationTimer()
      }
    },

    startSimulationTimer() {
      this.stopPlayback()
      this.playTimer = setInterval(() => {
        if (!this.isPlaying) return
        this.progressPercent += 1.0
        if (this.progressPercent >= 100) {
          this.progressPercent = 0
          this.activeChapterIndex = 0
        } else {
          const currentSec = (this.progressPercent / 100) * this.videoDuration
          for (let i = this.chapters.length - 1; i >= 0; i--) {
            if (currentSec >= this.chapters[i].startSec) {
              this.activeChapterIndex = i
              break
            }
          }
        }
      }, 1000)
    },

    stopPlayback() {
      if (this.playTimer) {
        clearInterval(this.playTimer)
        this.playTimer = null
      }
    },

    jumpToModule(route) {
      this.closeModal()
      if (this.$route?.path !== route) {
        this.$router.push(route)
      }
    },

    savePreference() {
      if (this.dontShowAgain) {
        localStorage.setItem('tfl_tutorial_seen', 'true')
      } else {
        localStorage.removeItem('tfl_tutorial_seen')
      }
    }
  }
}
</script>

<style scoped>
.tutorial-overlay {
  position: fixed;
  inset: 0;
  background: rgba(4, 6, 12, 0.88);
  backdrop-filter: blur(12px);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.tutorial-modal {
  width: 100%;
  max-width: 1100px;
  max-height: 94vh;
  background: #0d111d;
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 18px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(212, 175, 55, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.tutorial-header {
  padding: 1.25rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: linear-gradient(180deg, #131826 0%, #0d111d 100%);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-source-toggle {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #d4af37;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-source-toggle:hover {
  background: rgba(212, 175, 55, 0.25);
}

.tour-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 1.2px;
  color: #d4af37;
  margin-bottom: 4px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #d4af37;
  box-shadow: 0 0 10px #d4af37;
  animation: pulse 1.8s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.6; }
  50% { transform: scale(1.25); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.6; }
}

.tutorial-header h2 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.3px;
}

.tour-sub {
  margin: 3px 0 0;
  font-size: 0.85rem;
  color: #94a3b8;
}

.btn-close {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.8rem;
  cursor: pointer;
  line-height: 1;
}

.video-url-bar {
  display: flex;
  gap: 8px;
  padding: 10px 2rem;
  background: #151926;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.url-input {
  flex: 1;
  background: #090c14;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 0.85rem;
}

.btn-apply-url {
  background: #d4af37;
  color: #0b0f19;
  border: none;
  font-weight: 700;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-reset-url {
  background: transparent;
  color: #94a3b8;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}

/* Body */
.tutorial-body {
  padding: 1.5rem 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Video Stage Container */
.video-stage-container {
  background: #080a10;
  border: 1px solid rgba(255, 255, 255, 0.12);
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
  font-size: 0.75rem;
  color: #94a3b8;
}

.mock-badge {
  font-size: 0.7rem;
  background: rgba(212, 175, 55, 0.15);
  color: #d4af37;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid rgba(212, 175, 55, 0.3);
}

/* Viewport Area */
.media-stage-viewport {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000000;
  overflow: hidden;
}

.video-player-box {
  width: 100%;
  height: 100%;
}

.embedded-media-element {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000000;
}

/* Fallback Stage Box */
.video-fallback-box {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: flex-end;
  transition: background-image 0.5s ease-in-out;
}

.fallback-glass-scrim {
  width: 100%;
  padding: 1.5rem 2rem;
  background: linear-gradient(180deg, transparent 0%, rgba(8, 10, 16, 0.85) 40%, rgba(8, 10, 16, 0.98) 100%);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.player-ready-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(13, 17, 29, 0.85);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 10px 16px;
  border-radius: 10px;
}

.glow-icon {
  font-size: 1.8rem;
}

.player-ready-badge strong {
  display: block;
  font-size: 0.82rem;
  color: #d4af37;
  letter-spacing: 0.8px;
}

.player-ready-badge p {
  margin: 2px 0 0;
  font-size: 0.74rem;
  color: #cbd5e1;
}

.player-ready-badge code {
  color: #fcd34d;
  background: rgba(0, 0, 0, 0.4);
  padding: 1px 4px;
  border-radius: 3px;
}

.active-slide-caption {
  text-align: right;
}

.caption-tag {
  font-size: 0.72rem;
  font-weight: 700;
  color: #d4af37;
  letter-spacing: 1px;
}

.active-slide-caption h4 {
  margin: 4px 0 0;
  font-size: 1.15rem;
  color: #ffffff;
}

/* Controls */
.player-controls {
  background: #11141f;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-play {
  background: #d4af37;
  color: #0b0f19;
  font-weight: 800;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-play:hover {
  background: #e6c253;
}

.progress-track {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #fcd34d);
  border-radius: 4px;
  transition: width 0.2s ease-out;
}

.chapter-cue-point {
  position: absolute;
  top: -2px;
  width: 4px;
  height: 12px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 1px;
  pointer-events: none;
}

.time-readout {
  font-size: 0.8rem;
  color: #94a3b8;
  white-space: nowrap;
}

/* Chapter Tabs (9 Modules) */
.chapter-strip {
  display: flex;
  background: #0a0d16;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  overflow-x: auto;
  scrollbar-width: thin;
}

.chap-btn {
  flex: 1;
  min-width: 110px;
  background: transparent;
  border: none;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.chap-btn:hover {
  background: rgba(255, 255, 255, 0.04);
}

.chap-btn.active {
  background: rgba(212, 175, 55, 0.1);
  border-bottom: 2px solid #d4af37;
}

.chap-num {
  font-size: 0.68rem;
  font-weight: 800;
  color: #d4af37;
}

.chap-title {
  font-size: 0.75rem;
  color: #cbd5e1;
  white-space: nowrap;
  margin: 2px 0;
}

.chap-btn.active .chap-title {
  color: #ffffff;
  font-weight: 700;
}

.chap-time {
  font-size: 0.65rem;
  color: #64748b;
}

/* Chapter Details Card */
.chapter-details-card {
  background: #111522;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-counter {
  font-size: 0.72rem;
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
  padding: 0.8rem 1.1rem;
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
  padding: 8px 18px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  padding: 8px 18px;
  border-radius: 6px;
  cursor: pointer;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
</style>
