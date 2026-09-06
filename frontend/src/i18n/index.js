// ==============================================================================
// THE FINISHER LUXURY — REACIVE I18N RUNTIME CONTROLLER
// Supports instantaneous language switching across all 11 official SA languages
// ==============================================================================

import { reactive } from 'vue'
import { languages, translations } from './translations'
export { languages, translations }

const SAVED_LANG_KEY = 'finisher_selected_lang'
const DEFAULT_LANG = 'en'

// Read persisted language or fallback to default
const initialLang = localStorage.getItem(SAVED_LANG_KEY) || DEFAULT_LANG
const safeInitialLang = translations[initialLang] ? initialLang : DEFAULT_LANG

export const i18nState = reactive({
  currentLang: safeInitialLang,
  languages: languages
})

/**
 * Switch active language and persist to localStorage
 * @param {string} langCode - e.g. 'zu', 'xh', 'af', 'en'
 */
export function setLanguage(langCode) {
  if (translations[langCode]) {
    i18nState.currentLang = langCode
    localStorage.setItem(SAVED_LANG_KEY, langCode)
    document.documentElement.setAttribute('lang', langCode)
  } else {
    console.warn(`[i18n] Language code '${langCode}' not recognized.`)
  }
}

/**
 * Get active language object (with flag, native label, etc.)
 */
export function getActiveLanguage() {
  return languages.find(l => l.code === i18nState.currentLang) || languages[0]
}

/**
 * Translate a dot-separated key, with fallback to English then to key itself
 * Example: $t('nav.clients') => 'Amakhasimende' in isiZulu
 * @param {string} keyPath
 * @param {object} [params]
 * @returns {string}
 */
export function translate(keyPath, params = {}) {
  const lang = i18nState.currentLang
  const currentDict = translations[lang] || translations.en
  const fallbackDict = translations.en

  const resolve = (dict, path) => {
    if (!dict) return null
    const parts = path.split('.')
    let curr = dict
    for (const p of parts) {
      if (curr && typeof curr === 'object' && p in curr) {
        curr = curr[p]
      } else {
        return null
      }
    }
    return typeof curr === 'string' ? curr : null
  }

  let result = resolve(currentDict, keyPath)
  if (!result && lang !== 'en') {
    result = resolve(fallbackDict, keyPath)
  }
  if (!result) {
    result = keyPath.split('.').pop()
  }

  // Parameter replacement: {name} => params.name
  if (params && typeof params === 'object') {
    Object.keys(params).forEach(k => {
      result = result.replace(new RegExp(`\\{${k}\\}`, 'g'), params[k])
    })
  }

  return result
}

// Vue plugin installer
export const i18nPlugin = {
  install(app) {
    app.config.globalProperties.$t = translate
    app.config.globalProperties.$i18n = i18nState
    app.config.globalProperties.$setLanguage = setLanguage
    app.config.globalProperties.$getActiveLanguage = getActiveLanguage
  }
}

export default i18nPlugin
