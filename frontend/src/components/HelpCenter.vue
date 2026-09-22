<template>
  <div class="help-page">
    <!-- Header -->
    <div class="help-header">
      <div class="header-left">
        <div class="brand-crest-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>MTAMBO HOLDINGS DIRECTORATE</span>
        </div>
        <h1 class="page-title">Help &amp; Enterprise Enablement</h1>
        <p class="page-subtitle">Master THE FINISHER LUXURY ecosystem — from high-ticket contact onboarding to automated split settlements.</p>
      </div>
      <div class="header-actions">
        <button type="button" @click="launchTutorial" class="btn btn-gold">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          Launch Interactive Tour
        </button>
        <button type="button" @click="skipTutorial" class="btn btn-outline-luxury">
          Dismiss Tour
        </button>
      </div>
    </div>

    <!-- Tour Status Notice -->
    <div v-if="tutorialStatus === 'completed'" class="status-pill status-completed">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
      <span>Interactive system tour completed. You can relaunch it at any time to train new executive staff.</span>
    </div>
    <div v-else-if="tutorialStatus === 'skipped'" class="status-pill status-skipped">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span>Interactive tour is currently dismissed. Click "Launch Interactive Tour" whenever you are ready.</span>
    </div>

    <!-- Official Compliance & Documentation Hub Links -->
    <div class="docs-quick-grid">
      <router-link to="/documentation" class="doc-card featured-doc-card">
        <div class="doc-icon">📖</div>
        <div class="doc-info">
          <h4>Operating Manual &amp; Docs</h4>
          <p>Complete step-by-step masterclass &amp; visual guide</p>
        </div>
        <span class="doc-arrow">&rarr;</span>
      </router-link>
      <router-link to="/popia-compliance" class="doc-card">
        <div class="doc-icon">⚖️</div>
        <div class="doc-info">
          <h4>POPIA Section 19</h4>
          <p>Bank-grade audited compliance safeguards</p>
        </div>
        <span class="doc-arrow">&rarr;</span>
      </router-link>
      <router-link to="/api-docs" class="doc-card">
        <div class="doc-icon">⚙️</div>
        <div class="doc-info">
          <h4>Enterprise API Docs</h4>
          <p>REST endpoints, webhooks &amp; tokens</p>
        </div>
        <span class="doc-arrow">&rarr;</span>
      </router-link>
      <router-link to="/privacy-policy" class="doc-card">
        <div class="doc-info">
          <h4>Privacy Policy</h4>
          <p>Zero operational data leakage protocols</p>
        </div>
        <span class="doc-arrow">&rarr;</span>
      </router-link>
      <router-link to="/terms-of-service" class="doc-card">
        <div class="doc-icon">📜</div>
        <div class="doc-info">
          <h4>Terms of Service</h4>
          <p>Enterprise SaaS licensing agreement</p>
        </div>
        <span class="doc-arrow">&rarr;</span>
      </router-link>
    </div>

    <!-- Guided 5-Step Workflow -->
    <div class="luxury-card">
      <div class="card-head">
        <div class="head-title-wrap">
          <span class="card-badge">STANDARD OPERATING PROTOCOL</span>
          <h2>Executive 5-Step Workflow</h2>
        </div>
        <span class="card-note">Data Discipline Standard</span>
      </div>

      <div class="workflow-timeline">
        <div class="timeline-step">
          <div class="step-badge">1</div>
          <div class="step-content">
            <h3>Register Client Tenant</h3>
            <p>Establish the corporate workspace entity, configure tenant settings, and confirm master administrative credentials.</p>
          </div>
        </div>

        <div class="timeline-step">
          <div class="step-badge">2</div>
          <div class="step-content">
            <h3>Capture High-Ticket Contact</h3>
            <p>Under <strong>Clients &amp; Contacts</strong>, capture the primary stakeholder (executive sponsor, phone, and company name).</p>
          </div>
        </div>

        <div class="timeline-step">
          <div class="step-badge">3</div>
          <div class="step-content">
            <h3>Formalize Corporate Company Profile</h3>
            <p>Once a human counterpart exists, establish the corporate entity record with registration numbers, industry, and address.</p>
          </div>
        </div>

        <div class="timeline-step">
          <div class="step-badge">4</div>
          <div class="step-content">
            <h3>Link Stakeholders to Company Record</h3>
            <p>Associate team members, signatories, and decision-makers to maintain an audited commercial contact dossier.</p>
          </div>
        </div>

        <div class="timeline-step">
          <div class="step-badge">5</div>
          <div class="step-content">
            <h3>Launch Deal Pipeline &amp; Split Settlement</h3>
            <p>Open <strong>Deals</strong>, assign valuation, dispatch certified PDF quotes, and process commercial settlements with automated tollbooth splits.</p>
          </div>
        </div>
      </div>

      <div class="pro-tip-box">
        <div class="tip-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        </div>
        <div class="tip-body">
          <strong>Executive Pro-Tip:</strong> The Finisher CRM enforces human-first data architecture. Always capture at least one human contact before formalizing an enterprise company to prevent ghost records.
        </div>
      </div>
    </div>

    <!-- Interactive FAQs -->
    <div class="luxury-card">
      <div class="card-head">
        <div class="head-title-wrap">
          <span class="card-badge">KNOWLEDGE BASE</span>
          <h2>Frequently Asked Questions</h2>
        </div>
        <span class="card-note">Clear Executive Answers</span>
      </div>

      <div class="faq-accordion">
        <div 
          v-for="(faq, index) in faqs" 
          :key="faq.q" 
          class="faq-item"
          :class="{ 'is-open': openFaqIndex === index }"
        >
          <div class="faq-question" @click="toggleFaq(index)">
            <div class="faq-q-left">
              <span class="faq-bullet">Q:</span>
              <h3>{{ faq.q }}</h3>
            </div>
            <span class="faq-chevron">{{ openFaqIndex === index ? '−' : '+' }}</span>
          </div>
          <div v-if="openFaqIndex === index" class="faq-answer">
            <p v-for="(line, idx) in faq.a" :key="idx">{{ line }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Support Cards -->
    <div class="luxury-card">
      <div class="card-head">
        <div class="head-title-wrap">
          <span class="card-badge">DIRECT ASSISTANCE</span>
          <h2>Executive Concierge &amp; Support</h2>
        </div>
        <span class="card-note">Dedicated 24/7 Desk</span>
      </div>
      <p class="section-intro">Need customized platform assistance, white-label setup, or custom API integration? Our senior engineering team is standing by.</p>

      <div class="support-grid">
        <div class="sc" v-for="s in supportCards" :key="s.title">
          <div class="sc-icon" :class="s.color">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path :d="s.icon"/></svg>
          </div>
          <h3>{{ s.title }}</h3>
          <p>{{ s.desc }}</p>
          <a :href="s.href" class="sc-btn">{{ s.linkText }} &rarr;</a>
        </div>
      </div>

      <div class="support-footer">
        <div class="footer-crest">MTAMBO HOLDINGS GROUP</div>
        <p class="footer-title">THE FINISHER LUXURY CRM &middot; JSE &amp; POPIA CERTIFIED PLATFORM</p>
        <p class="footer-sub">Cryptographically Secured Client Data &middot; South African Commercial Gateway</p>
      </div>
    </div>
  </div>
</template>

<script>
import toast from '../utils/toast'

const TUTORIAL_KEY = 'thefinisher_tutorial_state'

export default {
  name: 'HelpCenter',
  data() {
    return {
      openFaqIndex: 0,
      faqs: [
        {
          q: 'How do I create a new client contact?',
          a: [
            'Navigate to "Clients" in the main sidebar and click "Create Contact".',
            'Capture their first name, last name, corporate email address, and direct phone number.',
            'Once saved, this contact can be attached to formal company dossiers and deal opportunities.'
          ]
        },
        {
          q: 'Why does the system require a contact before creating a company?',
          a: [
            'THE FINISHER enforces rigorous data discipline: every corporate account must have a verified human decision-maker.',
            'This guarantees zero orphan records and ensures all quotes, invoices, and password recovery emails reach real people.'
          ]
        },
        {
          q: 'How does PayFast Split Payments work for my deals?',
          a: [
            'Under Integrations Hub, configure your own PayFast Merchant ID.',
            'When your client pays an invoice through the CRM, PayFast automatically splits the payment at the gateway.',
            'Your business receives 98% net proceeds directly into your merchant bank account, while the CRM facilitaton tollbooth (2%) is routed to Mtambo Holdings.'
          ]
        },
        {
          q: 'How do I enable White-Label Custom Branding for my organization?',
          a: [
            'Navigate to "Settings" in the main sidebar and locate the "Corporate White-Label Branding" module.',
            'Activate the white-label license (R199/month) via PayFast.',
            'Once activated, you can upload your corporate logo and letterhead, removing all standard system watermarks.'
          ]
        },
        {
          q: 'Can I replay the Interactive System Tour anytime?',
          a: [
            'Yes. Simply click the golden "Launch Interactive Tour" button at the top of this page.',
            'The step-by-step tutorial will guide you across your live dashboard and workspaces.'
          ]
        }
      ],
      tutorialStatus: localStorage.getItem(TUTORIAL_KEY) || 'pending',
      supportCards: [
        { 
          title: 'Executive Concierge', 
          desc: 'High-priority enterprise assistance and SLA escalations.', 
          href: 'mailto:support@thefinishercrm.tech', 
          linkText: 'Email Concierge', 
          icon: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z M22 6l-10 7L2 6', 
          color: 'gold' 
        },
        { 
          title: 'Legal & POPIA Directorate', 
          desc: 'Data privacy, cryptographic validation, and compliance inquiries.', 
          href: 'mailto:legal@mtamboholdings.co.za', 
          linkText: 'Contact Directorate', 
          icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', 
          color: 'gold' 
        },
        { 
          title: 'Integration Desk', 
          desc: 'Webhook endpoints, API tokens, and PayFast multi-merchant setups.', 
          href: 'mailto:support@thefinishercrm.tech?subject=Integration%20Setup', 
          linkText: 'Integration Setup', 
          icon: 'M22 10v6M2 10l10-5 10 5-10 5z M6 12v5c6 3 12 0 12 0v-5', 
          color: 'gold' 
        },
        { 
          title: 'Direct Telemetry Desk', 
          desc: 'Found a visual bug or workflow issue? Alert the engineering team.', 
          href: 'mailto:support@thefinishercrm.tech?subject=Bug%20Report', 
          linkText: 'Report Issue', 
          icon: 'M8 2v4 M16 2v4 M3 10h18 M12 14v4 M8 14l-2 4 M16 14l2 4', 
          color: 'gold' 
        }
      ]
    }
  },
  methods: {
    toggleFaq(index) {
      this.openFaqIndex = this.openFaqIndex === index ? null : index
    },
    launchTutorial() {
      localStorage.setItem(TUTORIAL_KEY, 'completed')
      this.tutorialStatus = 'completed'
      this.$emit('launch-tutorial')
      toast.success('Interactive Tour Launched', 'Tour initialized. Returning to Dashboard to guide you through your workspace.')
      setTimeout(() => {
        this.$router.push('/dashboard')
      }, 1000)
    },
    skipTutorial() {
      localStorage.setItem(TUTORIAL_KEY, 'skipped')
      this.tutorialStatus = 'skipped'
      toast.info('Tour Dismissed', 'You can relaunch the interactive guide at any time from this page.')
    }
  }
}
</script>

<style scoped>
.help-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.5rem 2rem 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header */
.help-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.brand-crest-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.725rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #d4af37;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary, #ffffff);
  margin: 0 0 0.35rem;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-size: 0.9rem;
  color: var(--text-muted, #94a3b8);
  margin: 0;
  line-height: 1.5;
  max-width: 650px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* Buttons */
.btn-gold {
  background: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
  color: #ffffff;
  border: none;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.65rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 14px rgba(212, 175, 55, 0.3);
  transition: all 0.2s ease;
}

.btn-gold:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.45);
}

.btn-outline-luxury {
  background: var(--surface-bg, rgba(255, 255, 255, 0.04));
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.15));
  color: var(--text-secondary, #cbd5e1);
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.65rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-outline-luxury:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.5);
  color: var(--text-primary, #ffffff);
}

/* Status Pills */
.status-pill {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.85rem 1.2rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-completed {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #4ade80;
}

.status-skipped {
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.25);
  color: #facc15;
}

/* Docs Quick Grid */
.docs-quick-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.doc-card {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 1rem 1.2rem;
  background: var(--surface-card, #0f172a);
  border: 1px solid var(--border-gold, rgba(212, 175, 55, 0.2));
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.doc-card:hover {
  border-color: #d4af37;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

.doc-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.doc-info {
  flex: 1;
}

.doc-info h4 {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-primary, #ffffff);
}

.doc-info p {
  margin: 0.15rem 0 0;
  font-size: 0.75rem;
  color: var(--text-muted, #94a3b8);
}

.doc-arrow {
  color: #d4af37;
  font-weight: 700;
  font-size: 1.1rem;
  transition: transform 0.2s ease;
}

.doc-card:hover .doc-arrow {
  transform: translateX(3px);
}

/* Luxury Card Container */
.luxury-card {
  background: var(--surface-card, #0f172a);
  border: 1px solid var(--border-gold, rgba(212, 175, 55, 0.22));
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.06));
}

.card-badge {
  display: inline-block;
  font-size: 0.675rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #d4af37;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.card-head h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary, #ffffff);
  margin: 0;
}

.card-note {
  font-size: 0.75rem;
  color: var(--text-muted, #64748b);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-intro {
  color: var(--text-secondary, #cbd5e1);
  font-size: 0.85rem;
  margin: 0 0 1.25rem;
  line-height: 1.5;
}

/* Workflow Timeline */
.workflow-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-step {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.85rem 1rem;
  background: var(--surface-bg, rgba(255, 255, 255, 0.02));
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.05));
  border-radius: 10px;
  transition: all 0.2s ease;
}

.timeline-step:hover {
  background: rgba(212, 175, 55, 0.04);
  border-color: rgba(212, 175, 55, 0.25);
}

.step-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af37, #b45309);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
}

.step-content {
  flex: 1;
}

.step-content h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary, #ffffff);
  margin: 0 0 0.25rem;
}

.step-content p {
  font-size: 0.825rem;
  color: var(--text-secondary, #cbd5e1);
  margin: 0;
  line-height: 1.5;
}

.pro-tip-box {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding: 0.85rem 1.1rem;
  background: rgba(212, 175, 55, 0.08);
  border-left: 3px solid #d4af37;
  border-radius: 8px;
  color: #fde68a;
  font-size: 0.825rem;
  line-height: 1.5;
}

.tip-icon {
  color: #d4af37;
  flex-shrink: 0;
  margin-top: 2px;
}

/* Accordion FAQs */
.faq-accordion {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.faq-item {
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.07));
  border-radius: 10px;
  background: var(--surface-bg, rgba(255, 255, 255, 0.02));
  overflow: hidden;
  transition: all 0.2s ease;
}

.faq-item.is-open {
  border-color: rgba(212, 175, 55, 0.4);
  background: rgba(212, 175, 55, 0.03);
}

.faq-question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.2rem;
  cursor: pointer;
  user-select: none;
}

.faq-q-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.faq-bullet {
  color: #d4af37;
  font-weight: 800;
  font-size: 0.95rem;
}

.faq-question h3 {
  font-size: 0.925rem;
  font-weight: 600;
  color: var(--text-primary, #ffffff);
  margin: 0;
}

.faq-chevron {
  color: #d4af37;
  font-size: 1.25rem;
  font-weight: 700;
}

.faq-answer {
  padding: 0.25rem 1.2rem 1.1rem 2.4rem;
  color: var(--text-secondary, #cbd5e1);
  font-size: 0.85rem;
  line-height: 1.6;
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.04));
}

.faq-answer p {
  margin: 0.35rem 0;
}

/* Support Grid */
.support-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.sc {
  background: var(--surface-bg, rgba(255, 255, 255, 0.02));
  border: 1px solid var(--border-gold, rgba(212, 175, 55, 0.2));
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
}

.sc:hover {
  border-color: #d4af37;
  transform: translateY(-2px);
  background: rgba(212, 175, 55, 0.04);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.sc-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #d4af37;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.85rem;
}

.sc h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary, #ffffff);
  margin: 0 0 0.35rem;
}

.sc p {
  font-size: 0.8rem;
  color: var(--text-muted, #94a3b8);
  margin: 0 0 1rem;
  line-height: 1.45;
  flex: 1;
}

.sc-btn {
  display: inline-block;
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid #d4af37;
  color: #d4af37;
  font-weight: 700;
  font-size: 0.8rem;
  padding: 0.45rem 0.9rem;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.15s ease;
}

.sc-btn:hover {
  background: #d4af37;
  color: #000000;
}

/* Support Footer */
.support-footer {
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  padding-top: 1.25rem;
  text-align: center;
}

.footer-crest {
  font-size: 0.725rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: #d4af37;
}

.footer-title {
  font-size: 0.825rem;
  font-weight: 700;
  color: var(--text-primary, #ffffff);
  margin: 0.25rem 0;
}

.footer-sub {
  font-size: 0.75rem;
  color: var(--text-muted, #64748b);
  margin: 0;
}

@media (max-width: 768px) {
  .help-page { padding: 1rem; }
  .help-header { flex-direction: column; align-items: stretch; }
  .header-actions { width: 100%; }
  .header-actions button { flex: 1; }
  .support-grid { grid-template-columns: 1fr; }
}
</style>
