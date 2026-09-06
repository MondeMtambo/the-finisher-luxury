<template>
  <div v-if="isOpen" class="world-clock-overlay" @click.self="close">
    <div class="world-clock-card">
      <div class="modal-gold-bar"></div>

      <div class="modal-header">
        <div class="header-badge">
          <span class="badge-icon">🌐</span>
          <span class="badge-text">GLOBAL FINANCIAL CAPITALS TIME MATRIX</span>
        </div>
        <button class="close-btn" @click="close" aria-label="Close modal">&times;</button>
      </div>

      <div class="modal-title-row">
        <div>
          <h2>World Clock Matrix</h2>
          <p>Real-time synchronized international financial center clocks. Standard time without fractional split-seconds.</p>
        </div>
        <div class="pinned-notice" v-if="pinnedCity">
          <span>Pinned to Header:</span>
          <strong>{{ getCityName(pinnedCity) }}</strong>
        </div>
      </div>

      <div class="cities-grid">
        <div 
          v-for="c in cities" 
          :key="c.id" 
          class="city-card"
          :class="{ 'is-pinned': pinnedCity === c.id }"
        >
          <div class="city-top">
            <div class="city-flag-name">
              <span class="flag-icon">{{ c.flag }}</span>
              <div>
                <div class="city-name">{{ c.name }}</div>
                <div class="city-country">{{ c.country }} &bull; {{ c.tzLabel }}</div>
              </div>
            </div>
            <div class="day-night-indicator" :title="c.isDaytime ? 'Daytime' : 'Nighttime'">
              <span>{{ c.isDaytime ? '☀️' : '🌙' }}</span>
            </div>
          </div>

          <!-- Digital Time (Clean, No Split-Seconds) -->
          <div class="city-time-display">
            <div class="time-string">{{ c.timeString }}</div>
            <div class="date-string">{{ c.dateString }}</div>
          </div>

          <!-- Market Trading Status -->
          <div class="city-market-row">
            <div class="market-name">
              <span class="market-dot" :class="c.isMarketOpen ? 'dot-open' : 'dot-closed'"></span>
              <span>{{ c.exchange }}</span>
            </div>
            <span class="market-badge" :class="c.isMarketOpen ? 'badge-open' : 'badge-closed'">
              {{ c.isMarketOpen ? 'TRADING OPEN' : 'CLOSED' }}
            </span>
          </div>

          <div class="city-footer">
            <span class="tz-offset">{{ c.offsetString }}</span>
            <button 
              class="pin-btn" 
              :class="{ 'pinned': pinnedCity === c.id }"
              @click="setPinnedCity(c.id)"
              :title="pinnedCity === c.id ? 'Currently shown in topbar' : 'Show this clock in topbar'"
            >
              {{ pinnedCity === c.id ? '✓ Active in Topbar' : 'Pin to Topbar' }}
            </button>
          </div>
        </div>
      </div>

      <div class="modal-footer-bar">
        <div class="footnote">
          <span>⚡ High-precision UTC sync &bull; Johannesburg HQ Standard Time: <strong>{{ joburgTime }}</strong></span>
        </div>
        <button class="btn-done" @click="close">Done</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WorldClockModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'city-pinned'],
  data() {
    return {
      pinnedCity: localStorage.getItem('finisher_pinned_city') || 'johannesburg',
      timer: null,
      citiesConfig: [
        { id: 'johannesburg', name: 'Johannesburg / Pretoria', country: 'South Africa', flag: '🇿🇦', tz: 'Africa/Johannesburg', tzLabel: 'SAST (UTC+2)', exchange: 'JSE', openHour: 9, closeHour: 17 },
        { id: 'london', name: 'London', country: 'United Kingdom', flag: '🇬🇧', tz: 'Europe/London', tzLabel: 'GMT/BST', exchange: 'LSE', openHour: 8, closeHour: 16.5 },
        { id: 'new_york', name: 'New York', country: 'United States', flag: '🇺🇸', tz: 'America/New_York', tzLabel: 'EST/EDT', exchange: 'NYSE / NASDAQ', openHour: 9.5, closeHour: 16 },
        { id: 'tokyo', name: 'Tokyo', country: 'Japan', flag: '🇯🇵', tz: 'Asia/Tokyo', tzLabel: 'JST (UTC+9)', exchange: 'TSE', openHour: 9, closeHour: 15.5 },
        { id: 'dubai', name: 'Dubai', country: 'United Arab Emirates', flag: '🇦🇪', tz: 'Asia/Dubai', tzLabel: 'GST (UTC+4)', exchange: 'DFM', openHour: 10, closeHour: 15 },
        { id: 'zurich', name: 'Zurich / Frankfurt', country: 'Switzerland / Germany', flag: '🇨🇭', tz: 'Europe/Zurich', tzLabel: 'CET/CEST', exchange: 'SIX / Deutsche Börse', openHour: 9, closeHour: 17.5 },
        { id: 'singapore', name: 'Singapore', country: 'Singapore', flag: '🇸🇬', tz: 'Asia/Singapore', tzLabel: 'SGT (UTC+8)', exchange: 'SGX', openHour: 9, closeHour: 17 },
        { id: 'sydney', name: 'Sydney', country: 'Australia', flag: '🇦🇺', tz: 'Australia/Sydney', tzLabel: 'AEST/AEDT', exchange: 'ASX', openHour: 10, closeHour: 16 }
      ],
      cities: [],
      joburgTime: ''
    }
  },
  computed: {
    isOpen() {
      return this.modelValue
    }
  },
  watch: {
    modelValue(val) {
      if (val) {
        this.updateTimes()
        if (!this.timer) {
          this.timer = setInterval(this.updateTimes, 1000)
        }
      } else {
        if (this.timer) {
          clearInterval(this.timer)
          this.timer = null
        }
      }
    }
  },
  mounted() {
    this.updateTimes()
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    close() {
      this.$emit('update:modelValue', false)
    },
    getCityName(id) {
      const c = this.citiesConfig.find(item => item.id === id)
      return c ? c.name : 'Johannesburg'
    },
    setPinnedCity(id) {
      this.pinnedCity = id
      localStorage.setItem('finisher_pinned_city', id)
      this.$emit('city-pinned', id)
    },
    updateTimes() {
      const now = new Date()

      this.cities = this.citiesConfig.map(cfg => {
        // Formatted cleanly with 24-hour hour and minute and second (NO split seconds)
        const timeFormatter = new Intl.DateTimeFormat('en-GB', {
          timeZone: cfg.tz,
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false
        })

        const dateFormatter = new Intl.DateTimeFormat('en-ZA', {
          timeZone: cfg.tz,
          weekday: 'short',
          day: '2-digit',
          month: 'short',
          year: 'numeric'
        })

        const hourFormatter = new Intl.DateTimeFormat('en-US', {
          timeZone: cfg.tz,
          hour: 'numeric',
          minute: 'numeric',
          hour12: false
        })

        const timeString = timeFormatter.format(now)
        const dateString = dateFormatter.format(now)

        // Calculate decimal hour for market open/close checks
        const parts = hourFormatter.formatToParts(now)
        const h = parseInt(parts.find(p => p.type === 'hour')?.value || '0', 10)
        const m = parseInt(parts.find(p => p.type === 'minute')?.value || '0', 10)
        const decimalHour = h + (m / 60)

        // Check if market is open (assuming Monday-Friday)
        const dayOfWeek = new Intl.DateTimeFormat('en-US', { timeZone: cfg.tz, weekday: 'narrow' }).format(now)
        const isWeekday = !['S', 'U'].includes(dayOfWeek) // Rough check for Sat/Sun
        const isMarketOpen = isWeekday && decimalHour >= cfg.openHour && decimalHour < cfg.closeHour
        const isDaytime = decimalHour >= 6 && decimalHour < 18

        // Calculate offset difference vs SAST
        const diffHours = (decimalHour - (new Date().getUTCHours() + 2))
        const offsetSign = diffHours >= 0 ? `+${Math.round(diffHours)}h` : `${Math.round(diffHours)}h`
        const offsetString = diffHours === 0 ? 'Same as SAST' : `${offsetSign} vs SAST`

        return {
          ...cfg,
          timeString,
          dateString,
          isDaytime,
          isMarketOpen,
          offsetString
        }
      })

      const jhb = this.cities.find(c => c.id === 'johannesburg')
      if (jhb) this.joburgTime = jhb.timeString
    }
  }
}
</script>

<style scoped>
.world-clock-overlay {
  position: fixed;
  inset: 0;
  background: rgba(8, 12, 23, 0.85);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100000;
  padding: 1.5rem;
  animation: fadeIn 0.2s ease-out;
}

.world-clock-card {
  position: relative;
  width: 100%;
  max-width: 960px;
  max-height: 90vh;
  background: linear-gradient(180deg, #111827 0%, #0a0e1a 100%);
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 18px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 35px rgba(212, 175, 55, 0.15);
  color: #f1f5f9;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: scaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-gold-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #d4af37, #f59e0b, #d4af37);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.75rem 0.5rem;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #fbbf24;
}

.close-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.7rem;
  cursor: pointer;
  line-height: 1;
  transition: color 0.15s;
}
.close-btn:hover {
  color: #fff;
}

.modal-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0 1.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.modal-title-row h2 {
  font-size: 1.45rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 0.25rem;
}

.modal-title-row p {
  font-size: 0.825rem;
  color: #94a3b8;
  margin: 0;
}

.pinned-notice {
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.75rem;
  color: #cbd5e1;
  display: flex;
  gap: 6px;
  align-items: center;
}
.pinned-notice strong {
  color: #facc15;
}

/* Grid of Cities */
.cities-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1.5rem 1.75rem;
  overflow-y: auto;
}

.city-card {
  background: rgba(17, 24, 39, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.2s ease;
  position: relative;
}

.city-card:hover {
  border-color: rgba(212, 175, 55, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
}

.city-card.is-pinned {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.06);
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.15);
}

.city-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.city-flag-name {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.flag-icon {
  font-size: 1.4rem;
}

.city-name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
}

.city-country {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 2px;
}

.day-night-indicator {
  font-size: 1rem;
}

.city-time-display {
  margin: 0.6rem 0 0.85rem;
}

.time-string {
  font-family: 'JetBrains Mono', monospace, sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #fde047;
  letter-spacing: 0.05em;
  line-height: 1;
  text-shadow: 0 0 12px rgba(253, 224, 71, 0.25);
}

.date-string {
  font-size: 0.72rem;
  color: #94a3b8;
  margin-top: 5px;
}

.city-market-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  margin-bottom: 0.75rem;
  font-size: 0.7rem;
}

.market-name {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #cbd5e1;
  font-weight: 600;
}

.market-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.dot-open {
  background: #22c55e;
  box-shadow: 0 0 6px #22c55e;
}
.dot-closed {
  background: #64748b;
}

.market-badge {
  font-size: 0.62rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.04em;
}
.badge-open {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.35);
}
.badge-closed {
  background: rgba(100, 116, 139, 0.15);
  color: #94a3b8;
  border: 1px solid rgba(100, 116, 139, 0.3);
}

.city-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.tz-offset {
  font-size: 0.68rem;
  color: #64748b;
}

.pin-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #cbd5e1;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.68rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.pin-btn:hover {
  background: rgba(212, 175, 55, 0.15);
  border-color: #d4af37;
  color: #fff;
}

.pin-btn.pinned {
  background: rgba(212, 175, 55, 0.25);
  border-color: #d4af37;
  color: #fde047;
  font-weight: 800;
}

.modal-footer-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.25);
}

.footnote {
  font-size: 0.74rem;
  color: #94a3b8;
}
.footnote strong {
  color: #facc15;
}

.btn-done {
  background: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
  border: none;
  color: #0b0f19;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-size: 0.825rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-done:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.96); }
  to { opacity: 1; transform: scale(1); }
}

@media (max-width: 900px) {
  .cities-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 550px) {
  .cities-grid {
    grid-template-columns: 1fr;
  }
}
</style>
