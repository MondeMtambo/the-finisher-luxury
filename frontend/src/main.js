import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/animations.css'
import './assets/theme.css'
import animationsPreference from './utils/animations'
import { warmUpBackend } from './utils/apiBase'

// Apply saved animation preference on startup
animationsPreference.init()

// ─── BACKEND WARM-UP ───
// Immediately wake the Render backend on app load (prevents cold-start errors)
warmUpBackend()

// Progressive Web App (PWA) Service Worker Registration & Realtime Cache Invalidation
if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => {
        console.log('[PWA] Service Worker registered successfully:', reg.scope)
        // Check for updates on every load
        reg.update()
        reg.addEventListener('updatefound', () => {
          const newWorker = reg.installing
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                console.log('[PWA] New version installed, reloading for instant update...')
                window.location.reload()
              }
            })
          }
        })
      })
      .catch((err) => {
        console.warn('[PWA] Service Worker registration failed:', err)
      })
  })

  // Reload when a new service worker takes over to eliminate any stale bundle execution
  let refreshing = false
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!refreshing) {
      refreshing = true
      window.location.reload()
    }
  })
}

createApp(App).use(router).mount('#app')