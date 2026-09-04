import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/animations.css'
import './assets/theme.css'
import animationsPreference from './utils/animations'

// Apply saved animation preference on startup
animationsPreference.init()

// Progressive Web App (PWA) Service Worker Registration
if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => {
        console.log('[PWA] Service Worker registered successfully:', reg.scope)
      })
      .catch((err) => {
        console.warn('[PWA] Service Worker registration failed:', err)
      })
  })
}

createApp(App).use(router).mount('#app')