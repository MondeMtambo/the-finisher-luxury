<template>
  <div 
    class="auth-page split-login-page" 
    :data-theme="currentTheme"
  >
    <!-- Dynamic Ambient Particles -->
    <div class="particles">
      <div class="particle" v-for="n in 18" :key="n"></div>
    </div>

    <!-- Luxury Ocean Wave Accents -->
    <div class="ocean">
      <div class="wave"></div>
      <div class="wave"></div>
    </div>

    <!-- Exclusive Header Bar with Theme Switcher -->
    <header class="login-nav">
      <div class="nav-brand-wrap" @click="$router.push('/')">
        <div class="brand-crest">F</div>
        <div class="brand-text">
          <span class="brand-name">THE FINISHER</span>
          <span class="brand-edition">LUXURY PRIVATE OS</span>
        </div>
      </div>
      <div class="nav-controls">
        <button 
          class="theme-toggle-btn" 
          @click="toggleTheme" 
          :title="currentTheme === 'dark' ? 'Switch to Light Platinum' : 'Switch to Obsidian Dark'"
        >
          <span v-if="currentTheme === 'dark'">☀️ Executive Light</span>
          <span v-else>🌙 Luxury Obsidian</span>
        </button>
        <router-link to="/register" class="request-access-pill">
          ⭐ Take Our 7-Day Trial &rarr;
        </router-link>
      </div>
    </header>

    <!-- Split Screen 50/50 Container -->
    <div class="split-viewport">
      
      <!-- LEFT HALF: Login Column (Stable login + Medium hover card on top) -->
      <div class="split-half login-half">
        
        <!-- Medium Top Luxury Card (Only hovers smoothly when mouse passes over it) -->
        <div class="top-luxury-card" title="The Finisher Luxury Enterprise">
          <div class="top-card-left">
            <div class="top-card-crest">F</div>
          </div>
          <div class="top-card-center">
            <div class="top-card-title">THE FINISHER LUXURY</div>
            <div class="top-card-subtitle">Executive Enterprise Gateway</div>
          </div>
          <div class="top-card-right">
            <span class="vip-status-pill">
              <span class="pulse-gold-dot"></span>
              VIP ACTIVE
            </span>
          </div>
        </div>

        <!-- Stable Luxury Glass Login Card (No Shaking / Tilting) -->
        <div 
          class="auth-card stable-login-card" 
          v-if="!showMFAModal && !showForceChangeModal"
        >
          <div class="card-inner-header">
            <h1 class="card-title">Member Authentication</h1>
            <p class="card-desc">Enter your authorized enterprise credentials to access your isolated workspace.</p>
          </div>

          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label class="form-label" for="username">Email Address / Admin Identifier</label>
              <div class="input-with-icon">
                <span class="input-icon">✉️</span>
                <input 
                  id="username" 
                  class="form-input with-icon" 
                  v-model="form.username" 
                  type="text" 
                  placeholder="executive@company.co.za" 
                  required 
                  autofocus
                >
              </div>
            </div>

            <div class="form-group">
              <div class="label-row flex-between">
                <label class="form-label" for="password">Workspace Password</label>
                <router-link to="/forgot-password" class="forgot-link">Forgot Password?</router-link>
              </div>
              <div class="input-with-icon">
                <span class="input-icon">🔒</span>
                <input 
                  id="password" 
                  class="form-input with-icon" 
                  v-model="form.password" 
                  :type="showPassword ? 'text' : 'password'" 
                  placeholder="••••••••••••" 
                  required
                >
                <button type="button" class="eye-toggle-btn" @click="showPassword = !showPassword">
                  {{ showPassword ? '👁️' : '🔒' }}
                </button>
              </div>
            </div>

            <label class="form-check-label">
              <input type="checkbox" v-model="form.acceptPolicy">
              <span>I confirm adherence to the <router-link to="/disclaimer" class="gold-link">POPIA Data Safeguard Policy</router-link></span>
            </label>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <button type="submit" class="btn btn-primary btn-block btn-gold-action" :disabled="loading || !form.acceptPolicy">
              <span v-if="loading" class="btn-spinner"></span>
              {{ loading ? 'Authenticating Workspace...' : 'Log In to Workspace' }}
            </button>

            <div class="auth-card-footer">
              <span class="footer-prompt">New organization?</span>
              <router-link to="/register" class="register-action-link">Take Our 7-Day Free Trial &rarr;</router-link>
            </div>
          </form>
        </div>

        <!-- Force Password Change Modal Card -->
        <div class="auth-card stable-login-card" v-if="showForceChangeModal">
          <div class="card-inner-header">
            <div class="modal-badge">🔒 SECURITY REQUIRED</div>
            <h1 class="card-title">Update Temporary Password</h1>
            <p class="card-desc">Changing password for <strong>{{ fpEmail }}</strong></p>
          </div>

          <form @submit.prevent="submitForceChange" class="auth-form">
            <div class="form-group">
              <label class="form-label" for="newPassword">New Secure Password</label>
              <input id="newPassword" class="form-input" v-model="forceNewPassword" type="password" placeholder="Minimum 8 characters" required>
            </div>

            <div class="form-group">
              <label class="form-label" for="newPassword2">Confirm New Password</label>
              <input id="newPassword2" class="form-input" v-model="forceNewPassword2" type="password" placeholder="Confirm password" required>
            </div>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <button type="submit" class="btn btn-primary btn-block btn-gold-action" :disabled="loading">
              {{ loading ? 'Updating...' : 'Update Password & Continue' }}
            </button>

            <div class="mfa-actions text-center">
              <button type="button" @click="showForceChangeModal = false" class="btn-link">Back to Login</button>
            </div>
          </form>
        </div>

        <!-- MFA Verification Modal Card -->
        <div class="auth-card stable-login-card" v-if="showMFAModal">
          <div class="card-inner-header">
            <div class="modal-badge">🛡️ POPIA SECTION 19</div>
            <h1 class="card-title">Multi-Factor Verification</h1>
            <p class="card-desc">A 6-digit verification code has been dispatched to <strong>{{ mfaEmail }}</strong></p>
          </div>

          <div class="mfa-container">
            <div class="form-group">
              <label class="form-label" for="mfaCode">Enter 6-Digit OTP</label>
              <input 
                id="mfaCode" 
                class="form-input mfa-code-input" 
                v-model="mfaCode" 
                type="text" 
                placeholder="000000" 
                maxlength="6"
                inputmode="numeric"
                @keyup.enter="verifyMFA"
                :disabled="mfaLoading"
                autofocus
              >
            </div>

            <div v-if="mfaError" class="alert alert-danger">{{ mfaError }}</div>

            <button @click="verifyMFA" class="btn btn-primary btn-block btn-gold-action" :disabled="mfaLoading || mfaCode.length !== 6">
              {{ mfaLoading ? 'Verifying OTP...' : 'Confirm & Authenticate' }}
            </button>

            <div class="mfa-actions">
              <button @click="resendMFACode" class="btn-link" :disabled="mfaLoading">
                Resend Code
              </button>
              <span class="link-sep">&middot;</span>
              <button @click="closeMFAModal" class="btn-link" :disabled="mfaLoading">
                Back to Login
              </button>
            </div>
          </div>
        </div>

      </div>

      <!-- RIGHT HALF: Animated Value / Advertisement Carousel (I-animate eceleni) -->
      <div class="split-half showcase-half">
        
        <div class="showcase-container">
          
          <!-- Slide Stage -->
          <div class="carousel-stage">
            <transition name="slide-fade" mode="out-in">
              <div 
                :key="activeSlideIndex" 
                class="carousel-card-slide"
                @mouseenter="pauseCarousel"
                @mouseleave="resumeCarousel"
              >
                <div class="slide-badge">
                  <span class="slide-badge-dot"></span>
                  {{ currentSlide.badge }}
                </div>

                <div class="slide-icon-halo">
                  <span class="slide-icon">{{ currentSlide.icon }}</span>
                </div>

                <h2 class="slide-title">{{ currentSlide.title }}</h2>
                <h3 class="slide-subtitle">{{ currentSlide.subtitle }}</h3>
                <p class="slide-description">{{ currentSlide.description }}</p>

                <!-- Feature Pill Highlights -->
                <div class="slide-highlights">
                  <div class="highlight-tag" v-for="(tag, idx) in currentSlide.tags" :key="idx">
                    {{ tag }}
                  </div>
                </div>

                <!-- Live Metric Display -->
                <div class="slide-metric-strip">
                  <div class="metric-item">
                    <span class="metric-val">{{ currentSlide.metricValue }}</span>
                    <span class="metric-lbl">{{ currentSlide.metricLabel }}</span>
                  </div>
                  <div class="metric-divider"></div>
                  <div class="metric-item">
                    <span class="metric-val">{{ currentSlide.secondMetricValue }}</span>
                    <span class="metric-lbl">{{ currentSlide.secondMetricLabel }}</span>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Carousel Controls -->
          <div class="carousel-nav-bar">
            <button class="nav-arrow-btn prev" @click="prevSlide" title="Previous Slide">&#8249;</button>
            <div class="carousel-indicators">
              <button 
                v-for="(slide, index) in slides" 
                :key="index"
                class="carousel-dot"
                :class="{ active: activeSlideIndex === index }"
                @click="goToSlide(index)"
                :title="slide.title"
              ></button>
            </div>
            <button class="nav-arrow-btn next" @click="nextSlide" title="Next Slide">&#8250;</button>
          </div>

          <!-- Corporate Trust Seal Footer -->
          <div class="trust-endorsement">
            <span>POPIA Section 19 Certified &middot; Multi-Tenant Cryptographic Isolation &middot; CIPC Integrated</span>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script>
import { authAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'Login',
  data() {
    return {
      currentTheme: localStorage.getItem('finisher_theme') || 'dark',
      showPassword: false,
      form: {
        username: '',
        password: '',
        acceptPolicy: true
      },
      loading: false,
      error: '',

      // Force-change-password flow
      showForceChangeModal: false,
      forceNewPassword: '',
      forceNewPassword2: '',
      fpUserId: null,
      fpEmail: '',

      // MFA Flow
      showMFAModal: false,
      mfaCode: '',
      mfaError: '',
      mfaLoading: false,
      mfaUserId: null,
      mfaEmail: '',
      mfaAttempts: 0,

      // Animated Carousel
      activeSlideIndex: 0,
      carouselTimer: null,
      slides: [
        {
          badge: 'PIPELINE & DEALS MASTERY',
          icon: '📈',
          title: 'Scale Your High-Ticket Pipeline',
          subtitle: 'The Finisher Deal Acceleration Engine',
          description: 'Consolidate 7-figure enterprise opportunities, track multi-stakeholder decisions, and accelerate deal closure with real-time executive velocity.',
          tags: ['Multi-Stage Kanban', 'Deal Health Scoring', 'Executive Forecasts', 'Contract Tracking'],
          metricValue: '+48%',
          metricLabel: 'Average Deal Velocity',
          secondMetricValue: 'R25M+',
          secondMetricLabel: 'Pipeline Capacity'
        },
        {
          badge: 'AUTONOMOUS WORKFLOWS',
          icon: '⚡',
          title: 'Autonomous 1-Click Operations',
          subtitle: 'Eliminate Repetitive Administrative Friction',
          description: 'Trigger automated VIP client alerts, instant quote generation, invoice tracking, and automated task escalations without manual overhead.',
          tags: ['Trigger Automation', 'Multi-Step Sequences', 'Webhook Web-API', 'Custom Webhooks'],
          metricValue: '100%',
          metricLabel: 'Zero Manual Overheads',
          secondMetricValue: '24/7',
          secondMetricLabel: 'Autonomous Execution'
        },
        {
          badge: 'BANK-GRADE SECURITY',
          icon: '🛡️',
          title: 'POPIA Section 19 Compliance',
          subtitle: 'Multi-Tenant Cryptographic Isolation',
          description: 'Guaranteed customer data sovereignty. Each enterprise organization operates in strict cryptographic isolation with full immutable audit trails.',
          tags: ['Hardware MFA', 'Audit Trails', 'Role-Based ACL', 'Cold-Storage Backups'],
          metricValue: '256-Bit',
          metricLabel: 'AES Data Encryption',
          secondMetricValue: '100%',
          secondMetricLabel: 'POPIA Compliant'
        },
        {
          badge: 'INSTITUTIONAL VERIFICATION',
          icon: '🏛️',
          title: 'CIPC Registry & SARS Integration',
          subtitle: 'Instant South African Enterprise Validation',
          description: 'Automated company registration lookup, director verification, and tax reference cross-checking to onboard verified corporate partners.',
          tags: ['CIPC BizPortal Ready', 'VAT/Tax Verification', 'Direct Corporate EFT', 'PayFast Gateway'],
          metricValue: 'Instant',
          metricLabel: 'Company Verification',
          secondMetricValue: 'Verified',
          secondMetricLabel: 'Enterprise Onboarding'
        }
      ]
    }
  },
  computed: {
    currentSlide() {
      return this.slides[this.activeSlideIndex]
    }
  },
  mounted() {
    if (authService.isAuthenticated()) {
      this.$router.push('/dashboard')
    }
    document.documentElement.setAttribute('data-theme', this.currentTheme)
    this.startCarousel()
  },
  beforeUnmount() {
    this.stopCarousel()
  },
  methods: {
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('finisher_theme', this.currentTheme)
      document.documentElement.setAttribute('data-theme', this.currentTheme)
    },
    startCarousel() {
      this.stopCarousel()
      this.carouselTimer = setInterval(() => {
        this.nextSlide()
      }, 5500)
    },
    stopCarousel() {
      if (this.carouselTimer) {
        clearInterval(this.carouselTimer)
        this.carouselTimer = null
      }
    },
    pauseCarousel() {
      this.stopCarousel()
    },
    resumeCarousel() {
      this.startCarousel()
    },
    nextSlide() {
      this.activeSlideIndex = (this.activeSlideIndex + 1) % this.slides.length
    },
    prevSlide() {
      this.activeSlideIndex = (this.activeSlideIndex - 1 + this.slides.length) % this.slides.length
    },
    goToSlide(index) {
      this.activeSlideIndex = index
      this.startCarousel()
    },

    async handleLogin() {
      this.loading = true
      this.error = ''

      try {
        if (!this.form.acceptPolicy) {
          this.error = 'Please accept the POPIA Data Safeguard notice to continue.'
          return
        }

        const loginResponse = await authAPI.login({
          username: this.form.username,
          password: this.form.password
        })

        if (loginResponse.data.requires_password_reset) {
          this.fpUserId = loginResponse.data.user_id
          this.fpEmail = loginResponse.data.email
          this.showForceChangeModal = true
          this.loading = false
          return
        }

        if (loginResponse.data.requires_mfa) {
          this.mfaUserId = loginResponse.data.user_id
          this.mfaEmail = loginResponse.data.email
          this.mfaError = ''
          this.mfaCode = ''
          this.mfaAttempts = 0
          this.showMFAModal = true
          toast.info('Verification Code Sent', 'Check your email inbox for the 6-digit code')
          return
        }

        if (loginResponse.data.access && loginResponse.data.refresh) {
          authService.setTokens(loginResponse.data.access, loginResponse.data.refresh)
        }

        let profile
        try {
          profile = await authAPI.getProfile()
          authService.setUser(profile.data)
        } catch (profileError) {
          console.warn('Failed to load profile:', profileError)
        }

        toast.success('Welcome back', 'Authenticated into Finisher Luxury')
        this.$router.push('/dashboard')

      } catch (error) {
        console.error('Login failed:', error)
        const data = error.response?.data
        this.error = data?.detail || data?.message || data?.error || error.message || 'Invalid login details'
      } finally {
        this.loading = false
      }
    },

    async submitForceChange() {
      if (!this.forceNewPassword || this.forceNewPassword !== this.forceNewPassword2) {
        toast.error('Passwords must match')
        return
      }
      this.loading = true
      try {
        const resp = await authAPI.forceChangePassword({
          user_id: this.fpUserId,
          old_password: this.form.password,
          password: this.forceNewPassword,
          password2: this.forceNewPassword2
        })

        if (resp.data.access && resp.data.refresh) {
          authService.setTokens(resp.data.access, resp.data.refresh)
          if (resp.data.user) {
            authService.setUser(resp.data.user)
          } else {
            try {
              const profile = await authAPI.getProfile()
              authService.setUser(profile.data)
            } catch (e) {
              console.warn('Profile fetch warning:', e)
            }
          }
          this.showForceChangeModal = false
          toast.success('Access Granted', 'Welcome to your Executive Workspace')
          this.$router.push('/dashboard')
          return
        }

        if (resp.data.requires_mfa) {
          this.showForceChangeModal = false
          this.mfaUserId = resp.data.user_id
          this.mfaEmail = resp.data.email
          this.showMFAModal = true
          toast.info('Verification code sent', 'Check your email for the 6-digit code')
        } else {
          toast.success('Password Updated', 'Please log in with your new password')
          this.showForceChangeModal = false
          this.form.password = this.forceNewPassword
        }

      } catch (error) {
        console.error('Force change failed:', error)
        toast.error(error.message || 'Failed to change password')
      } finally {
        this.loading = false
      }
    },

    async verifyMFA() {
      if (!this.mfaCode.trim() || this.mfaCode.length !== 6) {
        this.mfaError = 'Code must be exactly 6 digits'
        return
      }

      this.mfaLoading = true
      this.mfaError = ''

      try {
        const response = await authAPI.verifyMFA({
          user_id: this.mfaUserId,
          mfa_code: this.mfaCode
        })

        if (response.data.access && response.data.refresh) {
          authService.setTokens(response.data.access, response.data.refresh)
          authService.setUser(response.data.user)
        }

        toast.success('Verified', 'Welcome to The Finisher')
        this.showMFAModal = false
        this.$router.push('/dashboard')

      } catch (error) {
        console.error('MFA verification failed:', error)
        const data = error.response?.data
        this.mfaError = data?.message || data?.error || 'Verification failed. Please try again.'
        this.mfaAttempts += 1
      } finally {
        this.mfaLoading = false
      }
    },

    closeMFAModal() {
      this.showMFAModal = false
      this.mfaCode = ''
      this.mfaError = ''
    },

    async resendMFACode() {
      this.mfaLoading = true
      try {
        const response = await authAPI.login({
          username: this.form.username,
          password: this.form.password
        })
        if (response.data.requires_mfa) {
          this.mfaCode = ''
          this.mfaError = ''
          toast.success('Code Resent', 'New verification code sent to your email')
        }
      } catch (error) {
        this.mfaError = 'Failed to resend code. Please try again.'
      } finally {
        this.mfaLoading = false
      }
    }
  }
}
</script>

<style scoped>
/* Page Layout */
.split-login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-x: hidden;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  transition: background 0.3s ease, color 0.3s ease;
}

/* Dark Obsidian Theme */
.split-login-page[data-theme="dark"] {
  background: radial-gradient(circle at 20% 30%, #151922 0%, #0b0f19 70%, #06080e 100%);
  color: #f3f4f6;
}

/* Light Platinum Theme */
.split-login-page[data-theme="light"] {
  background: radial-gradient(circle at 20% 30%, #fdfbf7 0%, #f1f5f9 65%, #e2e8f0 100%);
  color: #0f172a;
}

/* Floating Particles */
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.35);
  animation: floatParticle 8s infinite ease-in-out;
}
.particle:nth-child(odd) { width: 7px; height: 7px; animation-duration: 9s; }
.particle:nth-child(even) { width: 11px; height: 11px; animation-duration: 7s; }
.particle:nth-child(1) { left: 12%; top: 25%; animation-delay: 0s; }
.particle:nth-child(2) { left: 30%; top: 65%; animation-delay: 1.5s; }
.particle:nth-child(3) { left: 50%; top: 15%; animation-delay: 2.8s; }
.particle:nth-child(4) { left: 70%; top: 75%; animation-delay: 0.8s; }
.particle:nth-child(5) { left: 88%; top: 35%; animation-delay: 2.2s; }

@keyframes floatParticle {
  0% { transform: translateY(0) scale(1); opacity: 0.2; }
  50% { transform: translateY(-35px) scale(1.3); opacity: 0.7; }
  100% { transform: translateY(0) scale(1); opacity: 0.2; }
}

/* Ocean Ambient Waves */
.ocean {
  height: 120px;
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}
.wave {
  background: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 88.7"%3E%3Cpath d="M800 56.9c-155.5 0-204.9-50-405.5-49.9-200 0-250 49.9-394.5 49.9v31.8h800v-.2-31.6z" fill="%23D4AF37" opacity="0.3"/%3E%3C/svg%3E');
  position: absolute;
  width: 200%;
  height: 100%;
  animation: wave 14s linear infinite;
  opacity: 0.25;
  bottom: 0;
  left: 0;
}
.wave:nth-of-type(2) {
  bottom: -15px;
  animation: wave 22s linear reverse infinite;
  opacity: 0.15;
}
@keyframes wave {
  0% { transform: translateX(0); }
  50% { transform: translateX(-25%); }
  100% { transform: translateX(-50%); }
}

/* Header Bar */
.login-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2.5rem;
  z-index: 20;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(212, 175, 55, 0.18);
}
.split-login-page[data-theme="dark"] .login-nav {
  background: rgba(11, 15, 25, 0.7);
}
.split-login-page[data-theme="light"] .login-nav {
  background: rgba(255, 255, 255, 0.8);
}

.nav-brand-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}
.brand-crest {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #d4af37, #b48608);
  color: #000;
  font-weight: 900;
  font-size: 1.25rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(212, 175, 55, 0.4);
}
.brand-text {
  display: flex;
  flex-direction: column;
}
.brand-name {
  font-weight: 800;
  font-size: 1.05rem;
  letter-spacing: 0.12em;
  color: #d4af37;
}
.brand-edition {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  opacity: 0.7;
}

.nav-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.theme-toggle-btn {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #d4af37;
  padding: 0.45rem 1rem;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.theme-toggle-btn:hover {
  background: rgba(212, 175, 55, 0.25);
  transform: translateY(-1px);
}
.request-access-pill {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.08));
  border: 1px solid rgba(212, 175, 55, 0.45);
  color: #d4af37;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}
.request-access-pill:hover {
  background: #d4af37;
  color: #000;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.45);
}

/* 50/50 Split Viewport */
.split-viewport {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: calc(100vh - 75px);
  position: relative;
  z-index: 10;
}
@media (max-width: 960px) {
  .split-viewport {
    grid-template-columns: 1fr;
  }
  .showcase-half {
    order: 2;
    padding: 2rem 1.5rem 4rem !important;
  }
}

/* Left Login Half */
.login-half {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 2rem;
}

/* MEDIUM TOP LUXURY CARD: Nice medium card on top of login with hover effect ONLY when mouse passes over it */
.top-luxury-card {
  width: 100%;
  max-width: 440px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1.35rem;
  border-radius: 12px;
  margin-bottom: 1.25rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
}

.split-login-page[data-theme="dark"] .top-luxury-card {
  background: rgba(17, 23, 35, 0.85);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(212, 175, 55, 0.35);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
}

.split-login-page[data-theme="light"] .top-luxury-card {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(212, 175, 55, 0.45);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

/* Hover effect ONLY triggers when mouse passes over THIS card */
.top-luxury-card:hover {
  transform: translateY(-3px);
  border-color: #d4af37;
  box-shadow: 0 12px 28px -4px rgba(212, 175, 55, 0.3);
}

.top-card-left {
  display: flex;
  align-items: center;
}
.top-card-crest {
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg, #d4af37, #b48608);
  color: #000;
  font-weight: 900;
  font-size: 1.15rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}
.top-luxury-card:hover .top-card-crest {
  transform: scale(1.08);
}

.top-card-center {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  margin: 0 1rem;
  flex: 1;
}
.top-card-title {
  font-size: 0.88rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #d4af37;
}
.top-card-subtitle {
  font-size: 0.72rem;
  font-weight: 600;
  opacity: 0.75;
}

.top-card-right {
  display: flex;
  align-items: center;
}
.vip-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #d4af37;
  padding: 0.3rem 0.65rem;
  border-radius: 12px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
}
.pulse-gold-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #d4af37;
  box-shadow: 0 0 6px #d4af37;
  animation: pulseDot 1.8s infinite;
}
@keyframes pulseDot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.5; }
}

/* STABLE LUXURY GLASS LOGIN CARD: Completely rock-solid, zero shaking */
.stable-login-card {
  width: 100%;
  max-width: 440px;
  padding: 2.5rem;
  border-radius: 16px;
  position: relative;
  transform: none !important; /* Zero tilt / zero shaking */
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.6);
  box-sizing: border-box;
}

.split-login-page[data-theme="dark"] .stable-login-card {
  background: rgba(17, 23, 35, 0.85);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(212, 175, 55, 0.35);
}

.split-login-page[data-theme="light"] .stable-login-card {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(212, 175, 55, 0.45);
  box-shadow: 0 15px 45px -10px rgba(0, 0, 0, 0.1);
}

.card-inner-header {
  margin-bottom: 1.75rem;
}
.card-title {
  font-size: 1.65rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 0.35rem;
}
.split-login-page[data-theme="dark"] .card-title { color: #ffffff; }
.split-login-page[data-theme="light"] .card-title { color: #0f172a; }

.card-desc {
  font-size: 0.85rem;
  line-height: 1.45;
  opacity: 0.75;
  margin: 0;
}

/* Form Styling */
.auth-form, .mfa-container {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.form-label {
  font-size: 0.82rem;
  font-weight: 600;
}
.split-login-page[data-theme="dark"] .form-label { color: #d1d5db; }
.split-login-page[data-theme="light"] .form-label { color: #334155; }

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}
.input-icon {
  position: absolute;
  left: 0.9rem;
  font-size: 0.95rem;
  pointer-events: none;
  opacity: 0.6;
}
.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  box-sizing: border-box;
}
.form-input.with-icon {
  padding-left: 2.6rem;
  padding-right: 2.6rem;
}
.split-login-page[data-theme="dark"] .form-input {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #fff;
}
.split-login-page[data-theme="light"] .form-input {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #0f172a;
}
.form-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.25);
}

.eye-toggle-btn {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}
.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.forgot-link {
  font-size: 0.78rem;
  color: #d4af37;
  text-decoration: none;
  font-weight: 500;
}
.forgot-link:hover {
  text-decoration: underline;
}

.form-check-label {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  font-size: 0.8rem;
  line-height: 1.4;
  cursor: pointer;
  opacity: 0.85;
}
.form-check-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #d4af37;
  margin-top: 1px;
}
.gold-link {
  color: #d4af37;
  text-decoration: underline;
}

.alert {
  padding: 0.7rem 1rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
}
.alert-danger {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid #ef4444;
  color: #fca5a5;
}

.btn {
  padding: 0.85rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}
.btn-primary {
  background: linear-gradient(135deg, #d4af37, #b48608);
  color: #000;
  box-shadow: 0 4px 18px rgba(212, 175, 55, 0.35);
  letter-spacing: 0.04em;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.55);
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-block { width: 100%; }

.auth-card-footer {
  text-align: center;
  font-size: 0.82rem;
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.footer-prompt {
  opacity: 0.7;
}
.register-action-link {
  color: #d4af37;
  font-weight: 700;
  text-decoration: none;
}
.register-action-link:hover {
  text-decoration: underline;
}

/* Modal styles */
.modal-badge {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: #d4af37;
  margin-bottom: 0.5rem;
}
.mfa-code-input {
  font-size: 1.8rem;
  letter-spacing: 0.5em;
  font-weight: 800;
  text-align: center;
  font-family: monospace;
}
.mfa-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
}
.btn-link {
  background: none;
  border: none;
  color: #d4af37;
  cursor: pointer;
  font-size: 0.82rem;
  text-decoration: underline;
}

/* RIGHT HALF: Animated Showcase Carousel */
.showcase-half {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 4rem;
  position: relative;
}
.showcase-container {
  width: 100%;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.carousel-stage {
  min-height: 380px;
  position: relative;
}

/* Carousel Slide Card */
.carousel-card-slide {
  padding: 2.75rem 2.25rem;
  border-radius: 20px;
  position: relative;
  transition: all 0.3s;
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.4);
}
.split-login-page[data-theme="dark"] .carousel-card-slide {
  background: linear-gradient(135deg, rgba(26, 32, 44, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.3);
}
.split-login-page[data-theme="light"] .carousel-card-slide {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.35);
  box-shadow: 0 15px 40px -10px rgba(0, 0, 0, 0.1);
}

.slide-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.3rem 0.85rem;
  border-radius: 16px;
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #d4af37;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  margin-bottom: 1.25rem;
}
.slide-badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #d4af37;
}

.slide-icon-halo {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
}
.slide-icon {
  font-size: 2rem;
}

.slide-title {
  font-size: 1.7rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 0.4rem;
  line-height: 1.25;
}
.split-login-page[data-theme="dark"] .slide-title { color: #ffffff; }
.split-login-page[data-theme="light"] .slide-title { color: #0f172a; }

.slide-subtitle {
  font-size: 0.88rem;
  font-weight: 600;
  color: #d4af37;
  margin: 0 0 1rem;
}
.slide-description {
  font-size: 0.92rem;
  line-height: 1.6;
  opacity: 0.8;
  margin: 0 0 1.5rem;
}

/* Feature Tag Pills */
.slide-highlights {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.75rem;
}
.highlight-tag {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.2);
  color: #d4af37;
}

/* Metric Strip */
.slide-metric-strip {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
}
.metric-item {
  display: flex;
  flex-direction: column;
}
.metric-val {
  font-size: 1.45rem;
  font-weight: 900;
  color: #d4af37;
}
.metric-lbl {
  font-size: 0.72rem;
  font-weight: 600;
  opacity: 0.7;
}
.metric-divider {
  width: 1px;
  height: 35px;
  background: rgba(212, 175, 55, 0.2);
}

/* Carousel Nav Controls */
.carousel-nav-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
}
.nav-arrow-btn {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #d4af37;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 1.25rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.nav-arrow-btn:hover {
  background: #d4af37;
  color: #000;
  transform: scale(1.05);
}
.carousel-indicators {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.carousel-dot {
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background: rgba(212, 175, 55, 0.25);
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}
.carousel-dot.active {
  width: 28px;
  background: #d4af37;
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.6);
}

.trust-endorsement {
  text-align: center;
  font-size: 0.75rem;
  opacity: 0.65;
  letter-spacing: 0.04em;
  padding: 0 1rem;
}

/* Slide Transition */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(25px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-25px);
}
</style>
