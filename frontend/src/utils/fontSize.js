/**
 * THE FINISHER LUXURY CRM — Dynamic Font Size Scaling Engine
 * Provides dynamic viewport text-density controls (Small, Normal, Large, Extra-Large)
 * Persisted in localStorage and hydrated on app boot.
 */

const SIZES = [
  { key: 'small', label: 'Compact (Small)', scale: '0.88', icon: 'A⁻', basePx: '12.5px' },
  { key: 'normal', label: 'Default (Normal)', scale: '1.00', icon: 'A', basePx: '14px' },
  { key: 'large', label: 'Executive (Large)', scale: '1.12', icon: 'A⁺', basePx: '15.5px' },
  { key: 'xlarge', label: 'Max Clarity (XL)', scale: '1.25', icon: 'A⁺⁺', basePx: '17px' }
]

export const fontSizeService = {
  getAvailableSizes() {
    return SIZES
  },

  getCurrentSize() {
    try {
      const saved = localStorage.getItem('finisher_font_size')
      if (saved && SIZES.some(s => s.key === saved)) {
        return saved
      }
    } catch (e) {}
    return 'normal'
  },

  setSize(sizeKey) {
    const target = SIZES.find(s => s.key === sizeKey) || SIZES[1]
    try {
      localStorage.setItem('finisher_font_size', target.key)
    } catch (e) {}

    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-font-size', target.key)
      document.documentElement.style.setProperty('--app-font-scale', target.scale)
      document.documentElement.style.setProperty('--app-base-font-size', target.basePx)
    }

    // Broadcast custom event so reactive components can update state
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tfl-font-size-changed', { detail: target }))
    }
    return target
  },

  cycleNext() {
    const current = this.getCurrentSize()
    const currentIndex = SIZES.findIndex(s => s.key === current)
    const nextIndex = (currentIndex + 1) % SIZES.length
    return this.setSize(SIZES[nextIndex].key)
  },

  init() {
    const current = this.getCurrentSize()
    this.setSize(current)
  }
}

export default fontSizeService
