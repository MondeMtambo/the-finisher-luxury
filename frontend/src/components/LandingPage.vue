<template>
  <div class="landing-page" style="min-height:100vh;">

    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">THE FINISHER LUXURY EDITION</div>
        <h1 class="hero-title">Your Sales Pipeline,<br/>Simplified &amp; Powerful</h1>
        <p class="hero-subtitle">The CRM built for South African small teams. Track contacts, close deals faster, and get real-time performance insights — all from one dashboard.</p>
        <div class="hero-cta">
          <button class="cta-primary" @click="$router.push('/register')">Get Started — R249/mo</button>
          <button class="cta-secondary" @click="$router.push('/login')">Sign In</button>
        </div>
        <p class="hero-note">No long-term contracts &bull; Cancel anytime &bull; Built in South Africa</p>
      </div>
      <div class="hero-image">
        <div class="mockup-browser">
          <div class="browser-bar"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
          <div class="browser-content">
            <div class="stats-preview">
              <div class="stat-box"><div class="stat-value">247</div><div class="stat-label">Contacts</div></div>
              <div class="stat-box"><div class="stat-value">52</div><div class="stat-label">Companies</div></div>
              <div class="stat-box"><div class="stat-value">R845K</div><div class="stat-label">Pipeline</div></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="features" class="features-section">
      <h2 class="section-title">Everything You Need to Win</h2>
      <p class="section-subtitle">Built for teams that finish strong</p>
      <div class="features-grid">
        <div class="feature-card" v-for="f in features" :key="f.title">
          <div class="feature-icon"><svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path :d="f.icon"/></svg></div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <section id="pricing" class="pricing-section">
      <h2 class="section-title">Simple, Transparent Pricing</h2>
      <p class="section-subtitle">No hidden fees. Cancel anytime.</p>
      <div class="pricing-grid">
        <div v-for="plan in plans" :key="plan.tier" class="pricing-card" :class="{ featured: plan.featured }">
          <div v-if="plan.featured" class="pricing-pop">MOST POPULAR</div>
          <div class="pricing-tier">{{ plan.tier }}</div>
          <div class="pricing-price">{{ plan.price }}</div>
          <div class="pricing-period">{{ plan.period }}</div>
          <ul class="pricing-features"><li v-for="f in plan.features" :key="f" :class="{ disabled: f.startsWith('x ') }">{{ f.replace(/^x /, '') }}</li></ul>
          <button class="btn" :class="plan.featured ? 'btn-primary' : 'btn-secondary'" @click="$router.push('/register')">{{ plan.cta }}</button>
        </div>
      </div>
    </section>

    <section class="testimonials-section">
      <h2 class="section-title">Trusted by Winners</h2>
      <div class="testimonials-grid">
        <div v-for="t in testimonials" :key="t.name" class="testimonial-card">
          <div class="stars">
            <svg v-for="n in 5" :key="n" width="16" height="16" fill="#f59e0b" viewBox="0 0 20 20"><path d="M10 1l2.39 4.84 5.34.78-3.86 3.76.91 5.32L10 13.27 5.22 15.7l.91-5.32L2.27 6.62l5.34-.78L10 1z"/></svg>
          </div>
          <p class="t-text">"{{ t.quote }}"</p>
          <div class="t-author"><strong>{{ t.name }}</strong><span>{{ t.role }}</span></div>
        </div>
      </div>
    </section>

    <section class="final-cta">
      <h2>Ready to Finish Strong?</h2>
      <p>Join South African businesses closing more deals every week</p>
      <button class="cta-primary large" @click="$router.push('/register')">Get Started — R249/mo</button>
      <p class="cta-note">No long-term contracts &bull; Cancel anytime</p>
    </section>

    <footer class="lp-footer">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="fb-mark">F</div>
          <div><div class="fb-name">THE FINISHER LUXURY</div><p class="fb-tagline">Don't just chase leads - finish every relationship strong.</p></div>
        </div>
        <div class="footer-links">
          <div class="footer-col"><h4>Product</h4>
            <a href="#features" @click.prevent="scrollToSection('features')">Features</a>
            <a href="#pricing" @click.prevent="scrollToSection('pricing')">Pricing</a>
            <a href="#" @click.prevent="$router.push('/help')">Documentation</a>
          </div>
          <div class="footer-col"><h4>Company</h4>
            <a href="mailto:info@thefinisher.co.za">Contact Us</a>
            <a href="mailto:careers@thefinisher.co.za">Careers</a>
            <a href="mailto:partnerships@thefinisher.co.za">Partnerships</a>
          </div>
          <div class="footer-col"><h4>Legal</h4>
            <a href="#" @click.prevent="$router.push('/disclaimer')">Privacy &amp; Disclaimer</a>
            <a href="#" @click.prevent="$router.push('/disclaimer')">Terms of Service</a>
            <a href="#" @click.prevent="$router.push('/disclaimer')">POPIA Compliance</a>
          </div>
          <div class="footer-col"><h4>Support</h4>
            <a href="#" @click.prevent="$router.push('/help')">Help Center</a>
            <a href="mailto:support@thefinisher.co.za">support@thefinisher.co.za</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 THE FINISHER LUXURY by Mtambo Holdings. All rights reserved. Built in South Africa.</p>
        <div class="footer-badges">
          <span>Proudly South African</span>
          <span>POPIA Compliant</span>
          <span>SSL Secured</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      features: [
        { title:'Smart Contact Management', desc:'Auto-create companies from email domains. Track unlimited contacts with self-employed handling built-in.', icon:'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2 M23 21v-2a4 4 0 0 0-3-3.87 M16 3.13a4 4 0 0 1 0 7.75 M9 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0z' },
        { title:'Deal Pipeline Tracking', desc:'Visualize your sales pipeline. Track time spent on deals. Never miss a follow-up with built-in timers.', icon:'M22 12h-4l-3 9L9 3l-3 9H2' },
        { title:'Ticketing & Support', desc:'Internal ticket management for your team. Assign, track, and resolve with priority levels and categories.', icon:'M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8' },
        { title:'Performance Analytics', desc:'Real-time dashboards for employees. Admin oversight with detailed metrics. Know who is crushing it.', icon:'M18 20V10 M12 20V4 M6 20v-6' },
        { title:'Role-Based Access', desc:'Company admins, employees, system staff. Everyone sees exactly what they need -- nothing more.', icon:'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' },
        { title:'Smart Notifications', desc:'Stay in the loop. Scoped notifications for your company. Never miss an important update.', icon:'M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9 M13.73 21a2 2 0 0 1-3.46 0' }
      ],
      plans: [
        { tier:'CLASSIC', price:'FREE', period:'Forever', features:['1 User','Unlimited Contacts','Basic CRM Features','5 Recent Activities','x Company Auto-Create','x Advanced Reporting'], cta:'Start Free', featured:false },
        { tier:'SPORT', price:'R99', period:'per month', features:['2 Users','Everything in Classic','Company Auto-Create','Advanced Reporting','Performance Analytics','Priority Support'], cta:'Get Started', featured:true },
        { tier:'LUXURY', price:'R249', period:'per month', features:['10 Users','Everything in Sport','API Access','Custom Integrations','Dedicated Support','Training Sessions'], cta:'Get Started', featured:false },
        { tier:'PREMIUM', price:'R499', period:'per month', features:['Unlimited Users','Everything in Luxury','White-Label Option','Custom Development','24/7 Phone Support','SLA Guarantee'], cta:'Contact Sales', featured:false }
      ],
      testimonials: [
        { name:'Thabo M.', role:'Sales Director, Velocity Titans', quote:'THE FINISHER helped us close 40% more deals in Q3. The pipeline visibility alone was worth the upgrade.' },
        { name:'Lerato S.', role:'Operations Manager, Apex Solar United', quote:'Finally, a CRM that understands South African business. The company auto-create feature saves us hours every week.' },
        { name:'Sipho K.', role:'CEO, Pulse Logistics FC', quote:'The employee performance tracking changed how we manage our team. Everyone knows their goals and we finish strong together.' }
      ]
    }
  },
  methods: {
    scrollToSection(sectionId) {
      const element = document.getElementById(sectionId)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }
  },
  mounted() {
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault()
        const target = document.querySelector(this.getAttribute('href'))
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' })
        }
      })
    })
  }
}
</script>
<style scoped>
.landing-page { min-height:100vh; background:#fff; font-family:'Inter',system-ui,sans-serif; }

/* Hero */
.hero { display:grid;grid-template-columns:1fr 1fr;gap:4rem;max-width:1200px;margin:0 auto;padding:5rem 2rem;align-items:center; }
.hero-badge { display:inline-block;background:var(--primary-500);color:#fff;padding:.375rem 1rem;border-radius:var(--radius-md);font-weight:700;font-size:.75rem;letter-spacing:.04em;margin-bottom:1.5rem; }
.hero-title { font-size:3rem;font-weight:800;color:var(--gray-900);line-height:1.15;margin:0 0 1.25rem; }
.hero-subtitle { font-size:1.125rem;color:var(--gray-500);line-height:1.6;margin:0 0 2rem;max-width:540px; }
.hero-cta { display:flex;gap:.75rem;margin-bottom:.75rem; }
.cta-primary { background:var(--primary-500);color:#fff;border:none;padding:.875rem 2rem;border-radius:var(--radius-md);font-size:1rem;font-weight:700;cursor:pointer;transition:all .2s; }
.cta-primary:hover { background:#1d4ed8;transform:translateY(-2px);box-shadow:var(--shadow-lg); }
.cta-primary.large { font-size:1.125rem;padding:1rem 2.5rem; }
.cta-secondary { background:#fff;color:var(--gray-900);border:1px solid var(--border-color);padding:.875rem 2rem;border-radius:var(--radius-md);font-size:1rem;font-weight:600;cursor:pointer;transition:all .2s; }
.cta-secondary:hover { border-color:var(--primary-500);color:var(--primary-500); }
.hero-note { color:var(--gray-400);font-size:.8125rem; }
.hero-image { display:flex;justify-content:center;align-items:center; }
.mockup-browser { width:100%;max-width:460px;background:#fff;border-radius:var(--radius-lg);box-shadow:var(--shadow-xl);overflow:hidden;border:1px solid var(--border-color); }
.browser-bar { background:var(--gray-100);padding:.625rem .75rem;display:flex;gap:.375rem; }
.dot { width:10px;height:10px;border-radius:50%; }
.dot.red{background:#ef4444;} .dot.yellow{background:#f59e0b;} .dot.green{background:#22c55e;}
.browser-content { padding:1.5rem;background:var(--gray-50); }
.stats-preview { display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem; }
.stat-box { background:#fff;padding:1.25rem;border-radius:var(--radius-md);text-align:center;box-shadow:var(--shadow-sm);border-left:3px solid var(--primary-500); }
.stat-value { font-size:1.5rem;font-weight:800;color:var(--gray-900); }
.stat-label { font-size:.75rem;color:var(--gray-500);margin-top:.125rem; }

/* Features */
.features-section { background:var(--gray-50);padding:5rem 2rem; }
.section-title { text-align:center;font-size:2rem;font-weight:800;color:var(--gray-900);margin:0 0 .5rem; }
.section-subtitle { text-align:center;font-size:1rem;color:var(--gray-500);margin:0 0 3rem; }
.features-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;max-width:1200px;margin:0 auto; }
.feature-card { background:#fff;padding:2rem;border-radius:var(--radius-lg);border:1px solid var(--border-color);transition:all .2s; }
.feature-card:hover { border-color:var(--primary-500);box-shadow:var(--shadow-md);transform:translateY(-4px); }
.feature-icon { width:48px;height:48px;background:#eff6ff;color:var(--primary-500);border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center;margin-bottom:1rem; }
.feature-card h3 { font-size:1.125rem;font-weight:700;color:var(--gray-900);margin:0 0 .5rem; }
.feature-card p { color:var(--gray-500);line-height:1.6;margin:0;font-size:.875rem; }

/* Pricing */
.pricing-section { padding:5rem 2rem; }
.pricing-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem;max-width:1100px;margin:0 auto; }
.pricing-card { background:#fff;padding:2rem;border-radius:var(--radius-lg);border:1px solid var(--border-color);position:relative;transition:all .2s; }
.pricing-card:hover { transform:translateY(-4px);box-shadow:var(--shadow-lg); }
.pricing-card.featured { border-color:var(--primary-500);box-shadow:0 0 0 1px var(--primary-500); }
.pricing-pop { position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--primary-500);color:#fff;padding:.25rem 1rem;border-radius:var(--radius-md);font-size:.6875rem;font-weight:700;letter-spacing:.04em; }
.pricing-tier { font-size:.875rem;font-weight:700;color:var(--gray-500);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.5rem; }
.pricing-price { font-size:2.5rem;font-weight:800;color:var(--gray-900);margin-bottom:.25rem; }
.pricing-period { color:var(--gray-400);font-size:.8125rem;margin-bottom:1.5rem; }
.pricing-features { list-style:none;padding:0;margin:0 0 1.5rem; }
.pricing-features li { padding:.5rem 0;color:var(--gray-600);border-bottom:1px solid var(--gray-100);font-size:.8125rem; }
.pricing-features li::before { content:''; display:inline-block; width:16px; height:16px; margin-right:.5rem; vertical-align:middle; background:var(--green-500); mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M13.5 4.5l-7 7L3 8' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E"); -webkit-mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M13.5 4.5l-7 7L3 8' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E"); }
.pricing-features li.disabled { color:var(--gray-400); }
.pricing-features li.disabled::before { background:var(--gray-300); mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 8h8' stroke='%23fff' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E"); -webkit-mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 8h8' stroke='%23fff' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E"); }
.pricing-card .btn { width:100%;padding:.75rem; }

/* Testimonials */
.testimonials-section { background:var(--gray-50);padding:5rem 2rem; }
.testimonials-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;max-width:1200px;margin:0 auto; }
.testimonial-card { background:#fff;padding:2rem;border-radius:var(--radius-lg);border:1px solid var(--border-color); }
.stars { display:flex;gap:.125rem;margin-bottom:.75rem; }
.t-text { font-size:.9375rem;color:var(--gray-700);line-height:1.6;font-style:italic;margin:0 0 1rem; }
.t-author { display:flex;flex-direction:column; }
.t-author strong { color:var(--gray-900);font-weight:700;font-size:.875rem; }
.t-author span { color:var(--gray-500);font-size:.8125rem; }

/* Final CTA  */
.final-cta { background:var(--gray-900);color:#fff;padding:5rem 2rem;text-align:center; }
.final-cta h2 { font-size:2.5rem;font-weight:800;margin:0 0 .75rem; }
.final-cta p { font-size:1.125rem;margin:0 0 2rem;opacity:.85; }
.cta-note { color:rgba(255,255,255,.5);font-size:.8125rem;margin-top:.75rem; }

/* Footer */
.lp-footer { background:#111827;color:#e5e7eb;padding:3rem 2rem 1.5rem; }
.footer-content { display:flex;gap:3rem;max-width:1200px;margin:0 auto 2rem;flex-wrap:wrap; }
.footer-brand { display:flex;align-items:flex-start;gap:.75rem;min-width:260px; }
.fb-mark { width:36px;height:36px;background:var(--primary-500);color:#fff;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1rem;flex-shrink:0; }
.fb-name { font-weight:700;font-size:1rem; }
.fb-tagline { color:#9ca3af;font-size:.8125rem;margin:.25rem 0 0; }
.footer-links { display:flex;gap:3rem;flex:1;flex-wrap:wrap; }
.footer-col h4 { font-size:.8125rem;font-weight:600;margin:0 0 .75rem;color:#d1d5db; }
.footer-col a { display:block;color:#9ca3af;text-decoration:none;font-size:.8125rem;margin-bottom:.375rem;transition:color .2s; }
.footer-col a:hover { color:#fff; }
.footer-bottom { border-top:1px solid rgba(255,255,255,.1);padding-top:1.25rem;text-align:center;max-width:1200px;margin:0 auto; }
.footer-bottom p { font-size:.75rem;color:#9ca3af;margin:0 0 .5rem; }
.footer-badges { display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap; }
.footer-badges span { background:rgba(37,99,235,.15);border:1px solid rgba(37,99,235,.3);padding:.25rem .625rem;border-radius:var(--radius-md);font-size:.6875rem;color:var(--primary-500);font-weight:600; }

@media(max-width:1024px){ .hero{grid-template-columns:1fr;gap:2rem;padding:3rem 2rem;} .hero-content{text-align:center;} .hero-subtitle{max-width:100%;} .hero-cta{justify-content:center;} }
@media(max-width:768px){ .hero-title{font-size:2.25rem;} .hero-cta{flex-direction:column;} .cta-primary,.cta-secondary{width:100%;} .stats-preview{grid-template-columns:1fr;} .features-grid,.pricing-grid,.testimonials-grid{grid-template-columns:1fr;} .footer-content{flex-direction:column;gap:2rem;} .footer-links{flex-direction:column;gap:1.5rem;} .final-cta h2{font-size:2rem;} }
</style>
