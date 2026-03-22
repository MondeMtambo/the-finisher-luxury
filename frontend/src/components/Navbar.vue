<template>

  <div v-if="isAuthenticated && !isPublicPage" class="app-shell">

    <header class="topbar" :class="{ 'menu-open': mobileMenuOpen }">
      <div class="topbar-left">
        <button class="sidebar-toggle" @click="toggleSidebar" title="Toggle sidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
        </button>
        <div class="global-search">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <input 
            v-model="searchQuery" 
            @input="handleSearch"
            @focus="showSearchResults = true"
            @blur="hideSearchResults"
            placeholder="Search clients, deals, tickets..."
            class="search-input"
          >
          <div v-if="showSearchResults && searchQuery.length > 0" class="search-dropdown">
            <div v-if="searchResults.length === 0" class="search-empty">No results found</div>
            <div v-else v-for="result in searchResults" :key="result.type + result.id" @mousedown="navigateToResult(result)" class="search-result">
              <span class="result-icon">{{ result.icon }}</span>
              <div>
                <div class="result-title">{{ result.title }}</div>
                <div class="result-sub">{{ result.subtitle }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="topbar-right">

        <div class="notif-wrapper" ref="notifWrapper">
          <button class="topbar-icon-btn" title="Notifications" @click.stop="toggleNotifications">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            <span v-if="unreadCount > 0" class="notif-badge">{{ unreadCount > 9 ? '9+' : unreadCount }}</span>
          </button>
          <transition name="fade">
            <div v-if="showNotifications" class="notif-dropdown">
              <div class="notif-dropdown-header">
                <h4>Notifications</h4>
                <div class="notif-controls">
                  <div v-if="isAdmin || isClientAdmin" class="scope-toggle">
                    <button :class="{ active: notifScope === 'mine' }" @click="setNotifScope('mine')">Mine</button>
                    <button v-if="isAdmin" :class="{ active: notifScope === 'all' }" @click="setNotifScope('all')">All</button>
                    <button v-else-if="isClientAdmin" :class="{ active: notifScope === 'company' }" @click="setNotifScope('company')">Company</button>
                  </div>
                  <button v-if="notifications.length > 0" @click="markAllRead" class="mark-read-btn">Mark all read</button>
                </div>
              </div>
              <div class="notif-list">
                <div v-if="loadingNotifications" class="notif-loading"><div class="spinner"></div></div>
                <div v-else-if="notifications.length === 0" class="notif-empty">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                  <p>No notifications</p>
                </div>
                <div v-else v-for="notif in notifications.slice(0, 8)" :key="notif.id" class="notif-item" :class="{ unread: !notif.read_at }" @click="openNotification(notif)">
                  <div class="notif-dot" v-if="!notif.read_at"></div>
                  <div class="notif-content">
                    <div class="notif-title">{{ notif.title }}</div>
                    <div class="notif-msg">{{ notif.message }}</div>
                    <div class="notif-time">{{ formatNotificationTime(notif.created_at) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <div class="user-menu" ref="userWrapper">
          <button class="user-btn" @click.stop="toggleUserMenu">
            <div v-if="!userAvatarSvg" class="user-avatar-sm">{{ userInitials }}</div>
            <div v-else class="user-avatar-sm svg-avatar" v-html="userAvatarSvg"></div>
            <div class="user-info-sm">
              <span class="user-name-sm">{{ userFullName }}</span>
              <span class="user-role-sm">{{ userCompany }}</span>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <transition name="fade">
            <div v-if="showUserMenu" class="user-dropdown">
              <div class="user-dropdown-header">
                <div v-if="!userAvatarSvg" class="user-avatar-lg">{{ userInitials }}</div>
                <div v-else class="user-avatar-lg svg-avatar" v-html="userAvatarSvg"></div>
                <div>
                  <div class="dropdown-name">{{ userFullName }}</div>
                  <div class="dropdown-email">{{ userEmail }}</div>
                  <div v-if="userRole" class="dropdown-role">{{ userRole }}</div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/settings" class="dropdown-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                Settings
              </router-link>
              <button @click="handleLogout" class="dropdown-item logout-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/></svg>
                Logout
              </button>
            </div>
          </transition>
        </div>
      </div>
    </header>

    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed, 'mobile-open': mobileMenuOpen }">
      <div class="sidebar-brand" @click="$router.push('/dashboard')">
        <div class="brand-icon"><span>F</span></div>
        <div v-if="!sidebarCollapsed" class="brand-text">
          <span class="brand-name">THE FINISHER</span>
          <span class="brand-edition">LUXURY EDITION</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-label">MAIN</span>
          <router-link to="/dashboard" class="nav-item" active-class="active" exact>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            <span v-if="!sidebarCollapsed">Dashboard</span>
          </router-link>
          <router-link v-if="!isEmployeeOnly" to="/contacts" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span v-if="!sidebarCollapsed">Clients</span>
          </router-link>
          <router-link v-if="!isEmployeeOnly" to="/companies" class="nav-item" active-class="active" @click.prevent="handleCompaniesNavigation">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 7v14M21 7v14M6 11h4M6 15h4M14 11h4M14 15h4M9 21v-4h6v4M12 3l9 4M12 3L3 7"/></svg>
            <span v-if="!sidebarCollapsed">Companies</span>
          </router-link>
          <router-link v-if="!isEmployeeOnly" to="/deals" class="nav-item" active-class="active" @click.prevent="handleDealsNavigation">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
            <span v-if="!sidebarCollapsed">Deals</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-label">WORKSPACE</span>
          <router-link to="/tickets" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5v2M15 11v2M15 17v2M5 5h14a2 2 0 0 1 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3a2 2 0 0 0 0-4V7a2 2 0 0 1 2-2z"/></svg>
            <span v-if="!sidebarCollapsed">Tickets</span>
          </router-link>
          <router-link to="/employees" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><path d="M20 8v6M23 11h-6"/></svg>
            <span v-if="!sidebarCollapsed">Employee Directory</span>
          </router-link>
          <router-link to="/assets" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            <span v-if="!sidebarCollapsed">Assets (ADMP)</span>
          </router-link>
          <router-link to="/reports" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
            <span v-if="!sidebarCollapsed">Reports</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-label">LUXURY</span>
          <router-link v-if="!isEmployeeOnly" to="/products" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
            <span v-if="!sidebarCollapsed">Products</span>
          </router-link>
          <router-link v-if="!isEmployeeOnly" to="/campaigns" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <span v-if="!sidebarCollapsed">Campaigns</span>
          </router-link>
          <router-link v-if="!isEmployeeOnly" to="/workflows" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
            <span v-if="!sidebarCollapsed">Workflows</span>
          </router-link>
          <router-link to="/custom-dashboard" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
            <span v-if="!sidebarCollapsed">My Dashboard</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-label">SYSTEM</span>
          <router-link v-if="isAdmin" to="/admin/console" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            <span v-if="!sidebarCollapsed">Admin Console</span>
          </router-link>
          <router-link to="/settings" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
            <span v-if="!sidebarCollapsed">Settings</span>
          </router-link>
          <router-link to="/help" class="nav-item" active-class="active">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <span v-if="!sidebarCollapsed">Help</span>
          </router-link>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div v-if="!sidebarCollapsed" class="plan-badge" :class="{ 'plan-ultimate': isAdmin }">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <span>{{ isAdmin ? 'ULTIMATE' : 'LUXURY Edition' }}</span>
        </div>
      </div>
    </aside>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="mobileMenuOpen = false"></div>
  </div>
</template>

<script>
import authService from '../services/auth'
import { authAPI, systemAPI, contactsAPI, companiesAPI, dealsAPI, notificationsAPI } from '../api'
import toast from '../utils/toast'
import modal from '../utils/modal'
import { getRandomAvatar, getAvatarById } from '../utils/avatars.js'

export default {
  name: 'Navbar',
  data() {
    return {
      sidebarCollapsed: false,
      mobileMenuOpen: false,
      searchQuery: '',
      searchResults: [],
      showSearchResults: false,
      searchTimeout: null,
      showNotifications: false,
      showUserMenu: false,
      notifications: [],
      loadingNotifications: false,
      unreadCount: 0,
      notifScope: 'mine',
      notificationInterval: null,
      userName: 'User',
      userFullName: 'User',
      userCompany: '',
      userRole: '',
      userEmail: '',
      userAvatarSvg: null,
      isAdmin: false,
      isClientAdmin: false,
      profileLoaded: false,
      hasContacts: false,
      hasCompanies: false,
      hasLinkedContacts: false,
      checkingPrereqs: false
    }
  },
  computed: {
    isPublicPage() {
      return ['/', '/login', '/register', '/forgot-password', '/verify-otp', '/disclaimer', '/privacy-policy', '/terms-of-service', '/popia-compliance'].includes(this.$route.path)
    },
    isAuthenticated() {
      return authService.isAuthenticated()
    },
    userInitials() {
      const user = authService.getUser()
      if (user) {
        const first = (user.first_name || '').charAt(0).toUpperCase()
        const last = (user.last_name || '').charAt(0).toUpperCase()
        return first && last ? `${first}${last}` : (user.username || 'U').charAt(0).toUpperCase()
      }
      return 'U'
    },
    isEmployeeOnly() {
      return !this.isAdmin && !this.isClientAdmin
    }
  },
  mounted() {
    if (!authService.isAuthenticated()) return
    this.loadUserName()
    this.hydrateProfile()
    this.refreshPrerequisites()
    this.fetchNotifications()
    this.notificationInterval = setInterval(this.fetchNotifications, 60000)
    if (window.innerWidth <= 1024) this.sidebarCollapsed = true
    window.addEventListener('resize', this.handleResize)
    document.addEventListener('click', this.handleClickOutside)
    this.updateLayoutOffsets()
  },
  watch: {
    '$route.path'(newPath) {
      if (this.isPublicPage) return
      this.loadUserName()
      if (['/deals', '/companies'].includes(newPath)) this.refreshPrerequisites()
      this.mobileMenuOpen = false
      this.updateLayoutOffsets()
    },
    sidebarCollapsed() {
      this.updateLayoutOffsets()
    },
    mobileMenuOpen() {
      this.updateLayoutOffsets()
    }
  },
  beforeUnmount() {
    if (this.notificationInterval) clearInterval(this.notificationInterval)
    window.removeEventListener('resize', this.handleResize)
    document.removeEventListener('click', this.handleClickOutside)
    document.documentElement.style.setProperty('--sidebar-current-width', '0px')
  },
  methods: {
    toggleNotifications() {
      this.showNotifications = !this.showNotifications
      if (this.showNotifications) this.showUserMenu = false
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
      if (this.showUserMenu) this.showNotifications = false
    },
    handleClickOutside(e) {
      if (this.showNotifications && this.$refs.notifWrapper && !this.$refs.notifWrapper.contains(e.target)) {
        this.showNotifications = false
      }
      if (this.showUserMenu && this.$refs.userWrapper && !this.$refs.userWrapper.contains(e.target)) {
        this.showUserMenu = false
      }
    },
    toggleSidebar() {
      if (window.innerWidth <= 768) {
        this.mobileMenuOpen = !this.mobileMenuOpen
      } else {
        this.sidebarCollapsed = !this.sidebarCollapsed
      }
      this.updateLayoutOffsets()
    },
    updateLayoutOffsets() {
      if (!this.isAuthenticated || this.isPublicPage) {
        document.documentElement.style.setProperty('--sidebar-current-width', '0px')
        return
      }

      let width = 0
      if (window.innerWidth <= 768) {
        width = this.mobileMenuOpen ? 240 : 0
      } else {
        width = this.sidebarCollapsed ? 64 : 240
      }

      document.documentElement.style.setProperty('--sidebar-current-width', `${width}px`)
    },
    handleResize() {
      if (window.innerWidth <= 768) {
        this.sidebarCollapsed = true
      } else if (window.innerWidth <= 1024) {
        this.sidebarCollapsed = true
        this.mobileMenuOpen = false
      } else {
        this.sidebarCollapsed = false
        this.mobileMenuOpen = false
      }
      this.updateLayoutOffsets()
    },
    async fetchNotifications() {
      try {
        this.loadingNotifications = true
        const scopeParam = (this.isAdmin && this.notifScope === 'all') ? 'all'
          : (this.isClientAdmin && this.notifScope === 'company') ? 'company' : 'mine'
        const res = await notificationsAPI.getAll({ scope: scopeParam })
        const list = Array.isArray(res.data) ? res.data : (res.data?.results || [])
        this.notifications = list
        this.unreadCount = list.filter(n => !n.read_at).length
      } catch (e) { /* silent */ } finally { this.loadingNotifications = false }
    },
    setNotifScope(scope) {
      this.notifScope = scope
      this.fetchNotifications()
    },
    async markAllRead() {
      try {
        const unread = this.notifications.filter(n => !n.read_at)
        await Promise.all(unread.map(n => notificationsAPI.markRead(n.id)))
        await this.fetchNotifications()
      } catch (e) { console.error('Failed to mark all read:', e) }
    },
    async openNotification(notif) {
      try {
        if (!notif.read_at) {
          await notificationsAPI.markRead(notif.id)
          await this.fetchNotifications()
        }
      } catch (e) { /* non-blocking */ }

      // Show notification details in a modal and let user choose to open linked route
      try {
        const confirmed = await modal.confirm(notif.title || 'Notification', notif.message || '', 'info', { confirmText: 'Open', cancelText: 'Close' })
        if (confirmed) {
          const routes = { ticket: '/tickets', deal: '/deals', contact: '/contacts', company: '/companies' }
          const route = routes[notif.entity_type]
          if (route) {
            const query = notif.entity_type === 'ticket' && notif.entity_id ? `?ticket=${notif.entity_id}` : ''
            this.$router.push(route + query)
          }
        }
      } catch (e) {
        // Fallback: just close the dropdown
      }

      this.showNotifications = false
    },
    formatNotificationTime(dateString) {
      if (!dateString) return ''
      const now = new Date(), date = new Date(dateString)
      const mins = Math.floor((now - date) / 60000)
      if (mins < 1) return 'Just now'
      if (mins < 60) return `${mins}m ago`
      const hrs = Math.floor(mins / 60)
      if (hrs < 24) return `${hrs}h ago`
      const days = Math.floor(hrs / 24)
      if (days < 7) return `${days}d ago`
      return date.toLocaleDateString('en-ZA', { month: 'short', day: 'numeric' })
    },
    handleSearch() {
      clearTimeout(this.searchTimeout)
      if (this.searchQuery.length < 2) { this.searchResults = []; return }
      this.searchTimeout = setTimeout(async () => {
        const q = this.searchQuery.toLowerCase()
        const results = []
        try {
          const [contacts, companies, deals] = await Promise.allSettled([
            contactsAPI.getAll(), companiesAPI.getAll(), dealsAPI.getAll()
          ])
          if (contacts.status === 'fulfilled') {
            (contacts.value.data || []).filter(c =>
              `${c.first_name} ${c.last_name} ${c.email}`.toLowerCase().includes(q)
            ).slice(0, 3).forEach(c => results.push({
              type: 'contact', id: c.id, icon: '\u{1F464}',
              title: `${c.first_name} ${c.last_name}`, subtitle: c.email || 'Contact'
            }))
          }
          if (companies.status === 'fulfilled') {
            (companies.value.data || []).filter(c => c.name.toLowerCase().includes(q))
            .slice(0, 3).forEach(c => results.push({
              type: 'company', id: c.id, icon: '\u{1F3E2}', title: c.name, subtitle: 'Company'
            }))
          }
          if (deals.status === 'fulfilled') {
            (deals.value.data || []).filter(d => d.title.toLowerCase().includes(q))
            .slice(0, 3).forEach(d => results.push({
              type: 'deal', id: d.id, icon: '\u{1F4BC}', title: d.title, subtitle: `R${d.value}`
            }))
          }
        } catch (e) { /* silent */ }
        this.searchResults = results
      }, 300)
    },
    hideSearchResults() { setTimeout(() => { this.showSearchResults = false }, 200) },
    navigateToResult(result) {
      const routes = { contact: '/contacts', company: '/companies', deal: '/deals' }
      this.$router.push(routes[result.type] || '/dashboard')
      this.searchQuery = ''
      this.showSearchResults = false
    },
    loadUserName() {
      const user = authService.getUser()
      if (!user) return
      const first = (user.first_name || '').trim()
      const last = (user.last_name || '').trim()
      this.userFullName = [first, last].filter(Boolean).join(' ') || user.username || 'User'
      this.userCompany = user.company_name || (user.profile && user.profile.company_name) || ''
      this.userEmail = user.email || ''
      const jobTitle = user.job_title || (user.profile && user.profile.job_title) || ''
      const roleDisplay = (user.role && typeof user.role === 'object' && user.role.display) || ''
      this.userRole = jobTitle || roleDisplay || ''
      const isOwnerAdmin = (user?.username || '').toLowerCase() === 'adminluxury'
      this.isAdmin = Boolean(user.is_superuser || isOwnerAdmin)
      const hasClientAdminPermission = !!(user.permissions && user.permissions.is_admin)
      const hasAdminRole = !!(user.role && (user.role.value === 'admin' || user.role === 'admin' || (user.profile && user.profile.role === 'admin')))
      this.isClientAdmin = !this.isAdmin && (hasClientAdminPermission || hasAdminRole)
    },
    async hydrateProfile() {
      if (this.profileLoaded || this.isPublicPage) return
      const cached = authService.getUser()
      if (cached && (cached.is_staff !== undefined || cached.is_superuser !== undefined)) {
        this.loadUserName()
        this.profileLoaded = true
        return
      }
      try {
        const response = await authAPI.getProfile()
        authService.setUser(response.data)
        this.loadUserName()
      } catch (e) { console.warn('Unable to hydrate profile') }
      finally { this.profileLoaded = true }
    },
    async refreshPrerequisites() {
      if (this.isPublicPage || this.checkingPrereqs) return
      this.checkingPrereqs = true
      try {
        const response = await systemAPI.getPrerequisites()
        const p = response.data || {}
        this.hasContacts = (p.contacts || 0) > 0
        this.hasCompanies = (p.companies || 0) > 0
        const orphan = p.contacts_missing_company || 0
        this.hasLinkedContacts = Math.max((p.contacts || 0) - orphan, 0) > 0
      } catch (e) {
        this.hasContacts = true; this.hasCompanies = true; this.hasLinkedContacts = true
      } finally { this.checkingPrereqs = false }
    },
    async handleCompaniesNavigation() {
      if (this.isEmployeeOnly) {
        toast.warning('This section is for administrators.')
        this.$router.push('/tickets'); return
      }
      this.$router.push('/companies')
    },
    async handleDealsNavigation() {
      if (this.isEmployeeOnly) {
        toast.warning('This section is for administrators.')
        this.$router.push('/tickets'); return
      }
      await this.refreshPrerequisites()
      if (!this.hasContacts) {
        await modal.warning('Contacts Required', 'Add at least one contact before managing deals.')
        this.$router.push('/contacts'); return
      }
      if (!this.hasCompanies) {
        await modal.warning('Company Required', 'You need at least one company before managing deals.')
        this.$router.push('/companies'); return
      }
      if (!this.hasLinkedContacts) {
        await modal.warning('Link Required', 'Link a contact to a company before creating deals.')
        return
      }
      this.$router.push('/deals')
    },
    async handleLogout() {
      const confirmed = await modal.confirm('Logout', 'Are you sure you want to logout?', 'warning', { confirmText: 'Logout', cancelText: 'Stay' })
      if (!confirmed) return
      toast.info('Logging out...', 'Session ending')
      authService.clearAuth()
      authAPI.logout().catch(() => {})
      setTimeout(() => this.$router.replace('/'), 250)
    }
  }
}
</script>

<style scoped>
/* Shell wrapper — all children are position:fixed, so keep this out of flow */
.app-shell {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  overflow: visible;
  z-index: 100;
}

/* TOP BAR */
.topbar {
  position: fixed;
  top: 0;
  left: var(--sidebar-current-width, var(--sidebar-width));
  right: 0;
  height: var(--topbar-height);
  background: #000;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 100;
  transition: left 0.2s ease;
}
.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}
.sidebar-toggle {
  background: none;
  border: none;
  color: var(--gray-500);
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  display: flex;
  align-items: center;
}
.sidebar-toggle:hover { background: rgba(212, 175, 55, 0.1); color: #D4AF37; }

.global-search {
  position: relative;
  flex: 1;
  max-width: 480px;
}
.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 13px;
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
  outline: none;
  transition: all 0.15s;
  font-family: inherit;
}
.search-input:focus {
  background: rgba(0, 0, 0, 0.5);
  border-color: #D4AF37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}
.search-input::placeholder { color: #9ca3af; }

.search-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 8px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.9);
  z-index: 200;
  max-height: 320px;
  overflow-y: auto;
}
.search-empty { padding: 20px; text-align: center; color: #9ca3af; font-size: 13px; }
.search-result {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.1s;
}
.search-result:hover { background: rgba(212, 175, 55, 0.1); }
.result-icon { font-size: 18px; }
.result-title { font-size: 14px; font-weight: 500; color: #fff; }
.result-sub { font-size: 12px; color: #9ca3af; }

.topbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Notification Button */
.topbar-icon-btn {
  position: relative;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
}
.topbar-icon-btn:hover { background: rgba(212, 175, 55, 0.1); color: #D4AF37; }
.notif-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: var(--red-500);
  color: #fff;
  font-size: 10px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 9999px;
  min-width: 16px;
  text-align: center;
  line-height: 1.4;
}

.notif-wrapper { position: relative; }

.notif-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 380px;
  background: rgba(15, 15, 15, 0.95);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.9), inset 0 0 15px rgba(212, 175, 55, 0.05);
  z-index: 200;
}
.notif-dropdown-header {
  padding: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.notif-dropdown-header h4 { font-size: 15px; font-weight: 600; color: #fff; margin-bottom: 8px; }
.notif-controls { display: flex; gap: 8px; align-items: center; justify-content: space-between; }
.scope-toggle {
  display: flex;
  background: rgba(255,255,255,0.05);
  border-radius: 6px;
  overflow: hidden;
}
.scope-toggle button {
  padding: 4px 10px;
  font-size: 12px;
  border: none;
  background: transparent;
  color: #9ca3af;
  cursor: pointer;
  font-weight: 500;
  font-family: inherit;
}
.scope-toggle button.active {
  background: transparent;
  color: #D4AF37;
  text-shadow: 0 0 8px rgba(212, 175, 55, 0.4);
}
.mark-read-btn {
  font-size: 12px;
  color: #D4AF37;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
  font-family: inherit;
}
.mark-read-btn:hover { color: #B49015; }

.notif-list {
  max-height: 360px;
  overflow-y: auto;
}
.notif-loading { padding: 30px; display: flex; justify-content: center; }
.notif-empty {
  padding: 40px 20px;
  text-align: center;
  color: #9ca3af;
}
.notif-empty p { margin-top: 8px; font-size: 13px; }
.notif-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  transition: background 0.1s;
}
.notif-item:hover { background: rgba(212, 175, 55, 0.1); }
.notif-item.unread { background: rgba(212, 175, 55, 0.05); }
.notif-item.unread:hover { background: rgba(212, 175, 55, 0.15); }
.notif-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-500);
  margin-top: 6px;
  flex-shrink: 0;
}
.notif-content { flex: 1; min-width: 0; }
.notif-title { font-size: 13px; font-weight: 600; color: #fff; }
.notif-msg { font-size: 13px; color: #d1d5db; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.notif-time { font-size: 11px; color: #9ca3af; margin-top: 4px; }

/* User Menu */
.user-menu { position: relative; }
.user-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 10px;
  background: none;
  border: 1px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
}
.user-btn:hover { background: rgba(212, 175, 55, 0.05); border-color: rgba(212, 175, 55, 0.2); }
.user-avatar-sm {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--primary-500);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}
.user-info-sm { text-align: left; }
.user-name-sm { display: block; font-size: 13px; font-weight: 600; color: #fff; line-height: 1.3; }
.user-role-sm { display: block; font-size: 11px; color: #9ca3af; line-height: 1.3; }
.user-btn svg { color: #9ca3af; }

.svg-avatar {
  background: transparent !important;
  padding: 0 !important;
  overflow: hidden;
  border: 1px solid rgba(212, 175, 55, 0.4);
}
.svg-avatar :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 260px;
  background: rgba(15, 15, 15, 0.95);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.9), inset 0 0 15px rgba(212, 175, 55, 0.05);
  z-index: 200;
  overflow: hidden;
}
.user-dropdown-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.user-avatar-lg {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--primary-500);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}
.dropdown-name { font-size: 14px; font-weight: 600; color: #fff; }
.dropdown-email { font-size: 12px; color: #9ca3af; }
.dropdown-role { font-size: 11px; color: #D4AF37; margin-top: 2px; font-weight: 500; }
.dropdown-divider { height: 1px; background: rgba(255,255,255,0.1); }
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  font-size: 14px;
  color: #d1d5db;
  cursor: pointer;
  text-decoration: none;
  border: none;
  background: none;
  width: 100%;
  transition: background 0.1s;
  font-family: inherit;
}
.dropdown-item:hover { background: rgba(212, 175, 55, 0.1); color: #fff; }
.dropdown-item svg { color: #9ca3af; }
.logout-item { color: #ef4444; }
.logout-item svg { color: #ef4444; }
.logout-item:hover { background: rgba(239, 68, 68, 0.1); }

/* SIDEBAR */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: #000;
  border-right: 1px solid rgba(212, 175, 55, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 110;
  transition: width 0.2s ease;
  overflow: hidden;
}
.sidebar.collapsed {
  width: 64px;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
  min-height: var(--topbar-height);
}
.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #D4AF37;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}
.brand-icon span {
  animation: f-pulse 2.5s infinite ease-in-out;
}
@keyframes f-pulse {
  0%, 100% { opacity: 1; text-shadow: 0 0 12px rgba(212, 175, 55, 0.8); transform: scale(1); }
  50% { opacity: 0.4; text-shadow: none; transform: scale(0.96); }
}
.brand-text { min-width: 0; }
.brand-name {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #D4AF37;
  white-space: nowrap;
  letter-spacing: -0.02em;
}
.brand-edition {
  display: block;
  font-size: 10px;
  font-weight: 600;
  color: var(--primary-500);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 12px 8px;
}

.nav-section { margin-bottom: 20px; }
.nav-section-label {
  display: block;
  font-size: 10px;
  font-weight: 600;
  color: var(--gray-400);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0 12px;
  margin-bottom: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  color: #9ca3af;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.12s ease;
  margin-bottom: 2px;
  white-space: nowrap;
}
.nav-item:hover {
  background: rgba(212, 175, 55, 0.05);
  color: #D4AF37;
}
.nav-item.active {
  background: rgba(212, 175, 55, 0.1);
  color: #D4AF37;
  text-shadow: 0 0 8px rgba(212, 175, 55, 0.4);
}
.nav-item.active svg { stroke: #D4AF37; filter: drop-shadow(0 0 4px rgba(212, 175, 55, 0.6)); }
.nav-item svg {
  flex-shrink: 0;
  color: #6b7280;
  transition: color 0.12s;
}
.nav-item:hover svg { color: #D4AF37; }

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 10px;
}
.sidebar.collapsed .nav-section-label { display: none; }

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
}
.plan-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #D4AF37;
}
.plan-badge svg { color: #D4AF37; }
.plan-badge.plan-ultimate {
  background: linear-gradient(135deg, #D4AF37, #B49015);
  color: #000;
}
.plan-badge.plan-ultimate svg { color: #000; }

/* Mobile Overlay */
.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  z-index: 105;
}

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Responsive */
@media (max-width: 1024px) {
  .sidebar { width: 64px; }
  .sidebar .brand-text,
  .sidebar .nav-section-label,
  .sidebar .sidebar-footer .plan-badge span,
  .sidebar .nav-item span { display: none; }
  .sidebar .nav-item { justify-content: center; padding: 10px; }
  .topbar { left: 64px; }
  .user-info-sm { display: none; }
}

@media (max-width: 768px) {
  .sidebar { display: none; }
  .sidebar.mobile-open {
    display: flex;
    width: var(--sidebar-width);
    z-index: 120;
  }
  .topbar { left: 0; }
  .topbar.menu-open .global-search { display: none; }
  .global-search { max-width: 200px; }
  .user-info-sm { display: none; }
}
</style>
