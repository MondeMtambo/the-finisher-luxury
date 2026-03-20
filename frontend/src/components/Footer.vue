<template>
  <footer v-if="!isLandingPage || isAuthenticated" class="app-footer">
    <div class="footer-inner">
      <div class="footer-top">
        <div class="footer-brand">
          <div class="fb-mark">F</div>
          <div>
            <div class="fb-name">&copy; THE FINISHER LUXURY</div>
            <div class="fb-sub">MTAMBO HOLDINGS CRM SUITE</div>
          </div>
        </div>
        <nav class="footer-nav">
          <div class="fn-col">
            <div class="fn-title">Product</div>
            <router-link to="/">Dashboard</router-link>
            <router-link to="/contacts">Contacts</router-link>
            <router-link to="/companies">Companies</router-link>
            <router-link to="/deals">Deals</router-link>
            <router-link to="/reports">Reports</router-link>
          </div>
          <div class="fn-col">
            <div class="fn-title">Legal</div>
            <router-link to="/disclaimer">Disclaimer &amp; Privacy</router-link>
            <router-link to="/disclaimer">Copyright</router-link>
            <a href="#" @click.prevent="showRights">All Rights Reserved</a>
          </div>
          <div class="fn-col">
            <div class="fn-title">Partners</div>
            <a href="https://www.facebook.com/NatedGraphics" target="_blank" rel="noopener">Nated Graphics</a>
          </div>
          <div class="fn-col">
            <div class="fn-title">Contact</div>
            <a href="mailto:legal@mtamboholdings.co.za">legal@mtamboholdings.co.za</a>
            <a href="mailto:support@thefinishersport.co.za">support@thefinishersport.co.za</a>
          </div>
        </nav>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 MTAMBO HOLDINGS. All rights reserved.</p>
        <div class="fb-notice">
          <p>THE FINISHER LUXURY CRM - PREMIUM LUXURY EDITION</p>
          <p class="fb-warn">Protected by Copyright Law &bull; Unauthorized Use Prohibited</p>
        </div>
        <div class="social-row">
          <a v-if="links.facebookNated" class="social-btn" :href="links.facebookNated" target="_blank" rel="noopener" aria-label="Facebook"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
          <a v-if="links.linkedinCompany" class="social-btn" :href="links.linkedinCompany" target="_blank" rel="noopener" aria-label="LinkedIn"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
          <a v-if="links.linkedinMonde" class="social-btn" :href="links.linkedinMonde" target="_blank" rel="noopener" aria-label="Profile"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { SOCIAL_LINKS } from '../config/links'
import authService from '../services/auth'
import modal from '../utils/modal'

export default {
  name: 'AppFooter',
  computed: {
    isLandingPage() {
      return this.$route.path === '/'
    },
    isAuthenticated() {
      return authService.isAuthenticated()
    }
  },
  data() {
    return { links: SOCIAL_LINKS }
  },
  methods: {
    showRights() {
      modal.alert('All Rights Reserved', '🏆 THE FINISHER LUXURY CRM\n\n© 2026 MTAMBO HOLDINGS — Proprietary & Confidential\n\nThis software is protected by:\n• South African Copyright Law\n• International Intellectual Property Treaties\n• Trade Secret Protection\n• Patent Pending Technologies\n\nUnauthorised use is strictly prohibited. Any attempt to copy, reproduce, modify, distribute, or reverse engineer this software will result in immediate legal action.\n\nLicensing: legal@mtamboholdings.co.za', 'info')
    }
  }
}
</script>
<style scoped>
.app-footer { margin-top:2rem; background:var(--gray-900); color:#e5e7eb; border-top:1px solid var(--gray-800); }
.footer-inner { max-width:1100px; margin:0 auto; padding:2rem 1.5rem 1.25rem; }
.footer-top { display:flex; gap:2.5rem; flex-wrap:wrap; margin-bottom:1.5rem; }
.footer-brand { display:flex; align-items:flex-start; gap:.625rem; min-width:220px; }
.fb-mark { width:32px; height:32px; background:var(--primary-500); color:#fff; border-radius:var(--radius-sm); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:.875rem; flex-shrink:0; }
.fb-name { font-weight:700; font-size:.875rem; }
.fb-sub { color:#9ca3af; font-size:.75rem; }
.footer-nav { display:flex; gap:2rem; flex:1; flex-wrap:wrap; }
.fn-col { display:flex; flex-direction:column; min-width:140px; }
.fn-title { font-size:.6875rem; font-weight:600; color:#d1d5db; text-transform:uppercase; letter-spacing:.04em; margin-bottom:.5rem; }
.fn-col a { color:#9ca3af; text-decoration:none; font-size:.8125rem; margin-bottom:.25rem; transition:color .15s; }
.fn-col a:hover { color:#fff; }
.footer-bottom { border-top:1px solid rgba(255,255,255,.08); padding-top:1rem; display:flex; flex-direction:column; align-items:center; gap:.5rem; text-align:center; }
.footer-bottom p { font-size:.75rem; color:#9ca3af; margin:0; }
.fb-notice { background:rgba(37,99,235,.08); border:1px solid rgba(37,99,235,.2); border-radius:var(--radius-sm); padding:.375rem .75rem; }
.fb-notice p { margin:.125rem 0; font-size:.75rem; color:var(--primary-500); font-weight:600; }
.fb-warn { font-size:.6875rem !important; color:#9ca3af !important; font-weight:500 !important; }
.social-row { display:flex; gap:.375rem; }
.social-btn { width:28px; height:28px; background:var(--primary-500); color:#fff; border-radius:var(--radius-sm); display:flex; align-items:center; justify-content:center; text-decoration:none; transition:background .15s; }
.social-btn:hover { background:#1d4ed8; }
@media(max-width:768px){ .footer-top{flex-direction:column;gap:1.5rem;} .footer-nav{flex-direction:column;gap:1rem;} }
</style>
