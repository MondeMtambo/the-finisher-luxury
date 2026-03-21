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
.landing-page { min-height:100vh; background:#0B0C10; font-family:'Inter',system-ui,sans-serif; color: #fff; }

/* Hero */
.hero { display:grid;grid-template-columns:1fr 1fr;gap:4rem;max-width:1200px;margin:0 auto;padding:6rem 2rem;align-items:center; }
.hero-badge { display:inline-block;background:rgba(212, 175, 55, 0.15);color:#D4AF37;padding:.375rem 1rem;border-radius:var(--radius-md);font-weight:700;font-size:.75rem;letter-spacing:.04em;margin-bottom:1.5rem; border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 0 10px rgba(212, 175, 55, 0.2); }
.hero-title { font-size:3.5rem;font-weight:800;color:#fff;line-height:1.15;margin:0 0 1.25rem; background: linear-gradient(to right, #fff, #D4AF37); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-subtitle { font-size:1.125rem;color:#9ca3af;line-height:1.6;margin:0 0 2rem;max-width:540px; }
.hero-cta { display:flex;gap:1rem;margin-bottom:.75rem; }
.cta-primary { background:linear-gradient(135deg, #D4AF37 0%, #B49015 100%);color:#000;border:none;padding:.875rem 2rem;border-radius:var(--radius-md);font-size:1rem;font-weight:700;cursor:pointer;transition:all .3s; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4); }
.cta-primary:hover { transform:translateY(-2px);box-shadow:0 6px 20px rgba(212, 175, 55, 0.6); }
.cta-primary.large { font-size:1.125rem;padding:1.25rem 3rem; }
.cta-secondary { background:transparent;color:#D4AF37;border:1px solid #D4AF37;padding:.875rem 2rem;border-radius:var(--radius-md);font-size:1rem;font-weight:600;cursor:pointer;transition:all .3s; text-transform: uppercase; letter-spacing: 1px; }
.cta-secondary:hover { background:rgba(212, 175, 55, 0.1); box-shadow: 0 0 15px rgba(212, 175, 55, 0.2); }
.hero-note { color:#6b7280;font-size:.8125rem; }
.hero-image { display:flex;justify-content:center;align-items:center; position: relative; }
.hero-image::before { content: ''; position: absolute; width: 150%; height: 150%; background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, transparent 60%); z-index: 0; }
.mockup-browser { width:100%;max-width:460px;background:#111418;border-radius:var(--radius-lg);box-shadow:0 25px 50px -12px rgba(0,0,0,0.7);overflow:hidden;border:1px solid rgba(212, 175, 55, 0.3); z-index: 1; position: relative; }
.browser-bar { background:#1A1D24;padding:.625rem .75rem;display:flex;gap:.375rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
.dot { width:10px;height:10px;border-radius:50%; }
.dot.red{background:#ef4444;} .dot.yellow{background:#f59e0b;} .dot.green{background:#22c55e;}
.browser-content { padding:1.5rem;background:#111418; }
.stats-preview { display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem; }
.stat-box { background:rgba(255,255,255,0.03);padding:1.25rem;border-radius:var(--radius-md);text-align:center;box-shadow:0 4px 6px rgba(0,0,0,0.3);border:1px solid rgba(212, 175, 55, 0.1); border-top: 2px solid #D4AF37; }
.stat-value { font-size:1.5rem;font-weight:800;color:#fff; }
.stat-label { font-size:.75rem;color:#9ca3af;margin-top:.125rem; text-transform: uppercase; letter-spacing: 1px; }

/* Features */
.features-section { background:#0D0F12;padding:6rem 2rem; border-top: 1px solid rgba(212, 175, 55, 0.1); border-bottom: 1px solid rgba(212, 175, 55, 0.1); }
.section-title { text-align:center;font-size:2.5rem;font-weight:800;color:#fff;margin:0 0 .5rem; background: linear-gradient(to right, #D4AF37, #fff); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.section-subtitle { text-align:center;font-size:1.125rem;color:#9ca3af;margin:0 0 4rem; }
.features-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem;max-width:1200px;margin:0 auto; }
.feature-card { background:rgba(255,255,255,0.02);padding:2.5rem;border-radius:var(--radius-lg);border:1px solid rgba(255,255,255,0.05);transition:all .3s; position: relative; overflow: hidden; }
.feature-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #D4AF37, transparent); opacity: 0; transition: opacity 0.3s; }
.feature-card:hover { border-color:rgba(212, 175, 55, 0.3);box-shadow:0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(212, 175, 55, 0.05);transform:translateY(-5px); background:rgba(255,255,255,0.04); }
.feature-card:hover::before { opacity: 1; }
.feature-icon { width:56px;height:56px;background:rgba(212, 175, 55, 0.1);color:#D4AF37;border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:1.5rem; border: 1px solid rgba(212, 175, 55, 0.2); }
.feature-card h3 { font-size:1.25rem;font-weight:700;color:#fff;margin:0 0 .75rem; }
.feature-card p { color:#9ca3af;line-height:1.7;margin:0;font-size:.9375rem; }

/* Pricing */
.pricing-section { padding:6rem 2rem; background: radial-gradient(circle at center, #111418 0%, #0B0C10 100%); }
.pricing-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:2rem;max-width:1100px;margin:0 auto; align-items: center; }
.pricing-card { background:#111418;padding:2.5rem;border-radius:var(--radius-lg);border:1px solid rgba(255,255,255,0.1);position:relative;transition:all .3s; }
.pricing-card:hover { transform:translateY(-5px);box-shadow:0 20px 40px rgba(0,0,0,0.6); border-color: rgba(212, 175, 55, 0.3); }
.pricing-card.featured { border-color:#D4AF37;box-shadow:0 0 30px rgba(212, 175, 55, 0.15); transform: scale(1.05); background: #161A20; }
.pricing-card.featured:hover { transform: scale(1.05) translateY(-5px); box-shadow:0 15px 40px rgba(212, 175, 55, 0.2); }
.pricing-pop { position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg, #D4AF37, #B49015);color:#000;padding:.25rem 1.25rem;border-radius:20px;font-size:.75rem;font-weight:800;letter-spacing:1px; box-shadow: 0 4px 10px rgba(212,175,55,0.3); }
.pricing-tier { font-size:.875rem;font-weight:800;color:#D4AF37;text-transform:uppercase;letter-spacing:2px;margin-bottom:.5rem; }
.pricing-price { font-size:3rem;font-weight:800;color:#fff;margin-bottom:.25rem; }
.pricing-period { color:#6b7280;font-size:.875rem;margin-bottom:2rem; text-transform: uppercase; letter-spacing: 1px; }
.pricing-features { list-style:none;padding:0;margin:0 0 2rem; }
.pricing-features li { padding:.75rem 0;color:#d1d5db;border-bottom:1px solid rgba(255,255,255,0.05);font-size:.875rem; }
.pricing-features li::before { content:''; display:inline-block; width:16px; height:16px; margin-right:.75rem; vertical-align:middle; background:#D4AF37; mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M13.5 4.5l-7 7L3 8' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E"); -webkit-mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M13.5 4.5l-7 7L3 8' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E"); }
.pricing-features li.disabled { color:#6b7280; }
.pricing-features li.disabled::before { background:#4b5563; mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 8h8' stroke='%23fff' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E"); -webkit-mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 8h8' stroke='%23fff' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E"); }
.btn { width:100%;padding:1rem; border-radius: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; transition: all 0.3s; }
.btn-primary { background: linear-gradient(135deg, #D4AF37, #B49015); color: #000; border: none; }
.btn-primary:hover { box-shadow: 0 0 15px rgba(212,175,55,0.4); transform: translateY(-2px); }
.btn-secondary { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.2); }
.btn-secondary:hover { border-color: #D4AF37; color: #D4AF37; }

/* Testimonials */
.testimonials-section { background:#0D0F12;padding:6rem 2rem; border-top: 1px solid rgba(212, 175, 55, 0.1); border-bottom: 1px solid rgba(212, 175, 55, 0.1); }
.testimonials-grid { display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem;max-width:1200px;margin:0 auto; }
.testimonial-card { background:rgba(255,255,255,0.02);padding:2.5rem;border-radius:var(--radius-lg);border:1px solid rgba(255,255,255,0.05); }
.stars { display:flex;gap:.25rem;margin-bottom:1rem; }
.stars svg { fill: #D4AF37; }
.t-text { font-size:1.0625rem;color:#d1d5db;line-height:1.7;font-style:italic;margin:0 0 1.5rem; }
.t-author { display:flex;flex-direction:column; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem; }
.t-author strong { color:#fff;font-weight:700;font-size:1rem; margin-bottom: 0.25rem; }
.t-author span { color:#D4AF37;font-size:.8125rem; text-transform: uppercase; letter-spacing: 1px; }

/* Final CTA  */
.final-cta { background:linear-gradient(to bottom, #111418, #000);color:#fff;padding:8rem 2rem;text-align:center; position: relative; overflow: hidden; }
.final-cta::before { content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 800px; height: 1px; background: linear-gradient(90deg, transparent, #D4AF37, transparent); }
.final-cta h2 { font-size:3.5rem;font-weight:800;margin:0 0 1rem; background: linear-gradient(to right, #fff, #D4AF37); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.final-cta p { font-size:1.25rem;margin:0 0 3rem;color:#9ca3af; }
.cta-note { color:rgba(255,255,255,.4);font-size:.8125rem;margin-top:1.5rem; text-transform: uppercase; letter-spacing: 1px; }

/* Footer */
.lp-footer { background:#000;color:#9ca3af;padding:4rem 2rem 2rem; border-top: 1px solid rgba(212, 175, 55, 0.2); }
.footer-content { display:flex;gap:4rem;max-width:1200px;margin:0 auto 3rem;flex-wrap:wrap; }
.footer-brand { display:flex;align-items:flex-start;gap:1rem;min-width:280px; }
.fb-mark { width:40px;height:40px;background:linear-gradient(135deg, #D4AF37, #B49015);color:#000;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.25rem;flex-shrink:0; }
.fb-name { font-weight:800;font-size:1.125rem; color:#fff; letter-spacing: 1px; }
.fb-tagline { color:#6b7280;font-size:.875rem;margin:.5rem 0 0; line-height: 1.5; }
.footer-links { display:flex;gap:4rem;flex:1;flex-wrap:wrap; }
.footer-col h4 { font-size:.875rem;font-weight:700;margin:0 0 1.25rem;color:#fff; text-transform: uppercase; letter-spacing: 1px; }
.footer-col a { display:block;color:#9ca3af;text-decoration:none;font-size:.875rem;margin-bottom:.75rem;transition:all .2s; }
.footer-col a:hover { color:#D4AF37; padding-left: 5px; }
.footer-bottom { border-top:1px solid rgba(255,255,255,.05);padding-top:2rem;text-align:center;max-width:1200px;margin:0 auto; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.footer-bottom p { font-size:.8125rem;color:#6b7280;margin:0; }
.footer-badges { display:flex;gap:1rem;justify-content:center;flex-wrap:wrap; }
.footer-badges span { background:rgba(212, 175, 55, 0.05);border:1px solid rgba(212, 175, 55, 0.2);padding:.375rem .75rem;border-radius:20px;font-size:.6875rem;color:#D4AF37;font-weight:700; text-transform: uppercase; letter-spacing: 1px; }

@media(max-width:1024px){ .hero{grid-template-columns:1fr;gap:3rem;padding:4rem 2rem;} .hero-content{text-align:center;} .hero-subtitle{max-width:100%;} .hero-cta{justify-content:center;} .pricing-card.featured{transform:none;} .pricing-card.featured:hover{transform:translateY(-5px);} }
@media(max-width:768px){ .hero-title{font-size:2.5rem;} .hero-cta{flex-direction:column;} .cta-primary,.cta-secondary{width:100%;} .stats-preview{grid-template-columns:1fr;} .features-grid,.pricing-grid,.testimonials-grid{grid-template-columns:1fr;} .footer-content{flex-direction:column;gap:2.5rem;} .footer-links{flex-direction:column;gap:2rem;} .final-cta h2{font-size:2.5rem;} }
</style>
