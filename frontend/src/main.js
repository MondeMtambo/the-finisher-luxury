import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/animations.css'
import animationsPreference from './utils/animations'

// Apply saved animation preference on startup
animationsPreference.init()

createApp(App).use(router).mount('#app')