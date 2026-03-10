/**
 * Animations preference utility for THE FINISHER LUXURY.
 * Stores user preference in localStorage and toggles a data attribute on <html>.
 */

const STORAGE_KEY = 'finisher_animations_enabled'

const animationsPreference = {
  /**
   * Check if animations are enabled
   */
  isEnabled() {
    const stored = localStorage.getItem(STORAGE_KEY)
    // Default to enabled
    if (stored === null) return true
    return stored === 'true'
  },

  /**
   * Set animations preference and update DOM
   */
  setEnabled(enabled) {
    localStorage.setItem(STORAGE_KEY, String(enabled))
    this._applyToDOM(enabled)
  },

  /**
   * Toggle animations on/off
   */
  toggle() {
    const newValue = !this.isEnabled()
    this.setEnabled(newValue)
    return newValue
  },

  /**
   * Apply the current preference to the DOM
   * Call this on app startup
   */
  init() {
    this._applyToDOM(this.isEnabled())
  },

  /**
   * @private
   */
  _applyToDOM(enabled) {
    if (enabled) {
      document.documentElement.removeAttribute('data-animations')
    } else {
      document.documentElement.setAttribute('data-animations', 'off')
    }
  }
}

export default animationsPreference
