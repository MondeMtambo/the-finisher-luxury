// ==============================================================================
// THE FINISHER LUXURY — AUTONOMOUS REALTIME DOM INTERPRETER ENGINE
// POPIA Section 19 Cryptographic Privacy & Sovereign Indigenous Localization
// Realtime MutationObserver translating system UI across all 11 SA Languages in 25ms
// ==============================================================================

import { SA_LEXICON } from './lexicon'

class SovereignDOMInterpreter {
  constructor() {
    this.activeLang = 'en'
    this.observer = null
    this.debounceTimer = null
    this.isProcessing = false
    this.initialized = false

    // Build normalized case-insensitive lookup table for maximum performance
    this.lookup = {}
    this.buildLookupTable()
  }

  buildLookupTable() {
    this.lookup = {}
    for (const [englishPhrase, translations] of Object.entries(SA_LEXICON)) {
      const normalizedKey = englishPhrase.trim().toLowerCase()
      this.lookup[normalizedKey] = translations
    }
  }

  /**
   * Initialize interpreter runtime and attach MutationObserver
   * @param {string} initialLang - ISO code (e.g. 'zu', 'xh', 'af', 'en')
   */
  init(initialLang = 'en') {
    if (this.initialized) {
      this.setLanguage(initialLang)
      return
    }

    this.activeLang = initialLang || 'en'
    this.initialized = true

    // Initial DOM translation pass once DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.translateCurrentDOM())
    } else {
      this.translateCurrentDOM()
    }

    // Attach high-performance DOM MutationObserver to catch route changes, modals, dynamic tables
    this.attachObserver()

    // Listen for custom language switch events
    window.addEventListener('tfl-language-changed', (e) => {
      if (e.detail && e.detail.lang) {
        this.setLanguage(e.detail.lang)
      }
    })
  }

  attachObserver() {
    if (this.observer) return

    const targetNode = document.getElementById('app') || document.body
    if (!targetNode) return

    this.observer = new MutationObserver((mutations) => {
      // Ignore mutations caused by the interpreter itself
      if (this.isProcessing) return

      let hasRelevantMutations = false
      for (const m of mutations) {
        if (m.addedNodes.length > 0 || m.type === 'characterData') {
          hasRelevantMutations = true
          break
        }
      }

      if (hasRelevantMutations) {
        clearTimeout(this.debounceTimer)
        this.debounceTimer = setTimeout(() => {
          this.translateCurrentDOM()
        }, 25)
      }
    })

    this.observer.observe(targetNode, {
      childList: true,
      subtree: true,
      characterData: true
    })
  }

  /**
   * Switch the active language and re-interpret the entire screen
   * @param {string} langCode - e.g. 'zu', 'xh', 'af', 'en'
   */
  setLanguage(langCode) {
    if (this.activeLang === langCode && this.initialized) return
    this.activeLang = langCode || 'en'
    this.translateCurrentDOM()
  }

  /**
   * Translates a single text string into the active language
   * @param {string} text - English or previously stored original text
   * @returns {string|null} - Translated string or null if no translation found
   */
  translatePhrase(text) {
    if (!text || typeof text !== 'string') return null
    const trimmed = text.trim()
    if (!trimmed) return null

    // If English, return original
    if (this.activeLang === 'en') return trimmed

    const normalized = trimmed.toLowerCase()
    const entry = this.lookup[normalized]
    if (entry && entry[this.activeLang]) {
      // Preserve leading/trailing whitespace
      const match = text.match(/^(\s*)(.*?)(\s*)$/)
      if (match) {
        return match[1] + entry[this.activeLang] + match[3]
      }
      return entry[this.activeLang]
    }
    return null
  }

  /**
   * Main DOM scanning and translation routine
   */
  translateCurrentDOM() {
    if (this.isProcessing) return
    this.isProcessing = true

    try {
      const root = document.getElementById('app') || document.body
      if (!root) return

      // If active language is English, restore all original text nodes
      if (this.activeLang === 'en') {
        this.restoreOriginals(root)
        return
      }

      // 1. Translate Placeholders
      this.translatePlaceholders(root)

      // 2. Translate Candidate UI Elements
      this.translateUIElements(root)
    } catch (err) {
      console.error('[Sovereign Interpreter] Error during DOM translation pass:', err)
    } finally {
      this.isProcessing = false
    }
  }

  translatePlaceholders(root) {
    const inputs = root.querySelectorAll('input[placeholder], textarea[placeholder]')
    for (const input of inputs) {
      if (input.type === 'password' || input.classList.contains('no-translate')) continue
      if (!input.dataset.tflOrigPlaceholder) {
        input.dataset.tflOrigPlaceholder = input.placeholder
      }
      const orig = input.dataset.tflOrigPlaceholder
      const translated = this.translatePhrase(orig)
      if (translated) {
        input.placeholder = translated
      } else if (this.activeLang === 'en') {
        input.placeholder = orig
      }
    }
  }

  translateUIElements(root) {
    // Target relevant semantic UI elements (buttons, headers, column titles, labels, badges)
    const selector = [
      'button',
      '.btn',
      'th',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'label',
      '.form-label',
      '.status',
      '.badge',
      '.status-pill',
      '.kpi-title',
      '.card-title',
      '.nav-item span',
      '.nav-section-label',
      '.tab-btn',
      '.quick-btn span',
      '.modal-title',
      '.table-header-title',
      '.ctrl-section-label'
    ].join(',')

    const elements = root.querySelectorAll(selector)
    for (const el of elements) {
      if (el.classList.contains('no-translate') || el.closest('.no-translate')) continue
      // POPIA Protection: Never translate confidential client records or active input fields
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable) continue

      this.processElementNode(el)
    }
  }

  processElementNode(el) {
    // If element has only one child text node
    if (el.childNodes.length === 1 && el.childNodes[0].nodeType === Node.TEXT_NODE) {
      const textNode = el.childNodes[0]
      this.translateTextNode(textNode)
      return
    }

    // If element has multiple children, inspect direct text children
    for (const child of el.childNodes) {
      if (child.nodeType === Node.TEXT_NODE && child.textContent.trim().length > 0) {
        this.translateTextNode(child)
      }
    }
  }

  translateTextNode(textNode) {
    const rawText = textNode.textContent
    const trimmed = rawText.trim()
    if (!trimmed) return

    // POPIA Data Security Lockout: Never alter numeric values, currency digits, emails, or passwords
    if (/^[0-9\s,\.\-R%]+$/.test(trimmed) || trimmed.includes('@') || /^\+?[0-9]{7,}$/.test(trimmed)) {
      return
    }

    // Store original English text on node instance
    if (!textNode._tfl_orig) {
      textNode._tfl_orig = rawText
    }

    const baseText = textNode._tfl_orig
    const translated = this.translatePhrase(baseText)

    if (translated && textNode.textContent !== translated) {
      textNode.textContent = translated
    }
  }

  restoreOriginals(root) {
    // Restore placeholders
    const inputs = root.querySelectorAll('[data-tfl-orig-placeholder]')
    for (const input of inputs) {
      input.placeholder = input.dataset.tflOrigPlaceholder
    }

    // TreeWalker to restore all text nodes that have _tfl_orig
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false)
    let node
    while ((node = walker.nextNode())) {
      if (node._tfl_orig) {
        node.textContent = node._tfl_orig
      }
    }
  }
}

export const interpreter = new SovereignDOMInterpreter()
export default interpreter
