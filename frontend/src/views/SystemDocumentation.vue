<template>
  <div class="doc-page-container">
    <!-- Executive Top Header -->
    <header class="doc-hero">
      <div class="doc-hero-content">
        <div class="brand-crest">
          <span class="crest-dot"></span>
          <span>MTAMBO HOLDINGS DIRECTORATE &bull; OFFICIAL DOCUMENTATION</span>
        </div>
        <h1 class="hero-title">The Finisher Luxury — Executive Operating Manual</h1>
        <p class="hero-sub">
          The definitive guide to sovereign client data isolation, high-ticket deal velocity, automated PayFast split settlements, and statutory tender compliance.
        </p>
        <div class="hero-actions">
          <button type="button" class="btn btn-gold" @click="launchVideoTutorial">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Watch 4K Video Masterclass
          </button>
          <router-link to="/dashboard" class="btn btn-outline-luxury">
            ← Return to Dashboard
          </router-link>
        </div>
      </div>
    </header>

    <!-- Main Layout: Sidebar Navigation + Content Body -->
    <div class="doc-layout">
      <!-- Sticky Quick-Navigation Index -->
      <aside class="doc-toc-sidebar">
        <div class="toc-card">
          <span class="toc-badge">TABLE OF CONTENTS</span>
          <nav class="toc-nav">
            <a 
              v-for="item in tocItems" 
              :key="item.id" 
              :href="`#${item.id}`" 
              :class="['toc-link', { active: activeSection === item.id }]"
              @click.prevent="scrollToSection(item.id)"
            >
              <span class="toc-num">{{ item.num }}</span>
              <span class="toc-title">{{ item.title }}</span>
            </a>
          </nav>
        </div>
      </aside>

      <!-- Documentation Articles -->
      <main class="doc-content">
        <!-- 01: System Architecture -->
        <section id="architecture" class="doc-section card">
          <div class="section-tag">CHAPTER 01</div>
          <h2>System Architecture &amp; Sovereign Data Isolation</h2>
          <p class="lead-text">
            THE FINISHER LUXURY is built on a zero-trust multi-tenant architecture engineered to meet South Africa's strictest POPIA (Protection of Personal Information Act) Section 19 regulations.
          </p>
          <div class="spec-callout">
            <div class="callout-icon">🛡️</div>
            <div class="callout-body">
              <strong>Cryptographic Tenant Boundary</strong>
              <p>Every organization operates within an isolated cryptographic boundary. Client records, deals, and financial telemetry are strictly quarantined so that no data leakage can ever occur between accounts.</p>
            </div>
          </div>
          <div class="screenshot-preview">
            <img src="/screenshots/01_executive_dashboard.png" alt="Executive Dashboard" class="doc-img" />
            <span class="img-caption">Figure 1.1: Live executive telemetry with isolated tenant partition</span>
          </div>
        </section>

        <!-- 02: Dashboard & Velocity -->
        <section id="dashboard" class="doc-section card">
          <div class="section-tag">CHAPTER 02</div>
          <h2>Executive Command Center &amp; Deal Velocity</h2>
          <p>
            Your Dashboard provides real-time financial telemetry over high-ticket opportunities. Rather than cluttered vanity metrics, the interface surfaces the four metrics that govern enterprise survival:
          </p>
          <ul class="doc-list">
            <li><strong>Total Pipeline Value:</strong> Aggregate gross value of all active opportunities in South African Rands (ZAR).</li>
            <li><strong>Pipeline Win Rate:</strong> Rolling historical conversion percentage from qualified opportunity to Closed Won.</li>
            <li><strong>Average Deal Size:</strong> Average contract value per enterprise engagement, allowing you to gauge whether sales capacity is scaling.</li>
            <li><strong>Velocity Telemetry:</strong> Average days required to transition an inquiry through quotation to signed contract.</li>
          </ul>
          <div class="pro-tip-block">
            <strong>💡 BILLIONAIRE OPERATOR TIP:</strong>
            <p>Monitor deal velocity daily. When deal velocity accelerates, your cost of capital drops, allowing you to self-fund rapid commercial growth.</p>
          </div>
        </section>

        <!-- 03: Contacts & Human Stakeholders -->
        <section id="contacts" class="doc-section card">
          <div class="section-tag">CHAPTER 03</div>
          <h2>VIP Corporate Contacts &amp; Decision Makers</h2>
          <p>
            Enterprise software often fails because it treats companies like nameless logos. In The Finisher, <strong>every deal begins with a verified human counterpart</strong>.
          </p>
          <div class="step-guide">
            <div class="step-row">
              <span class="badge-num">1</span>
              <div>
                <strong>Capture Human Sponsor First:</strong>
                <p>Navigate to <em>Clients &amp; Contacts</em> and capture the executive sponsor's full legal name, direct corporate email, and direct mobile number.</p>
              </div>
            </div>
            <div class="step-row">
              <span class="badge-num">2</span>
              <div>
                <strong>Assign Corporate Designations:</strong>
                <p>Categorize contacts by signing authority (CEO, CFO, Procurement Director, Legal Counsel) to streamline stakeholder approval loops.</p>
              </div>
            </div>
          </div>
          <div class="screenshot-preview">
            <img src="/screenshots/02_clients_contacts.png" alt="Corporate B2B Contacts" class="doc-img" />
            <span class="img-caption">Figure 3.1: Clean, verified corporate stakeholder directory</span>
          </div>
        </section>

        <!-- 04: CIPC Businesses -->
        <section id="companies" class="doc-section card">
          <div class="section-tag">CHAPTER 04</div>
          <h2>Corporate Business Directory &amp; CIPC Verification</h2>
          <p>
            Ghost records and duplicate profiles corrupt commercial forecasts. The Finisher enforces statutory data discipline by attaching every business entity to its official South African Companies and Intellectual Property Commission (CIPC) registration number.
          </p>
          <div class="feature-bullets">
            <div class="bullet-card">
              <h4>Official Trading Name (T/A)</h4>
              <p>Maintains distinction between the legal statutory entity name and public trading names for audit clarity.</p>
            </div>
            <div class="bullet-card">
              <h4>Audited Physical Addresses</h4>
              <p>Ensures headquarters and jurisdictional service addresses are recorded for commercial contract enforceability.</p>
            </div>
          </div>
          <div class="screenshot-preview">
            <img src="/screenshots/03_companies_directory.png" alt="CIPC Business Directory" class="doc-img" />
            <span class="img-caption">Figure 4.1: CIPC-verified corporate business records</span>
          </div>
        </section>

        <!-- 05: Deals Pipeline -->
        <section id="deals" class="doc-section card">
          <div class="section-tag">CHAPTER 05</div>
          <h2>High-Ticket Deals &amp; Advisory Timers</h2>
          <p>
            The Deal Pipeline visualizes commercial opportunities across six standardized stages: <strong>Lead, Qualified, Proposal, Negotiation, Closed Won, and Closed Lost</strong>.
          </p>
          <div class="screenshot-preview">
            <img src="/screenshots/04_deals_pipeline.png" alt="Deal Pipeline" class="doc-img" />
            <span class="img-caption">Figure 5.1: Multi-stage Kanban pipeline with advisory timers</span>
          </div>
          <h3>Integrated Billable Advisory Timers</h3>
          <p>
            High-ticket sales often require dozens of executive advisory hours. The Finisher embeds real-time time tracking directly inside every deal card. Click the play button to start tracking consulting time, and stop it when meetings conclude. Accumulated hours appear automatically on client quotations.
          </p>
        </section>

        <!-- 06: PayFast Splits -->
        <section id="splits" class="doc-section card">
          <div class="section-tag">CHAPTER 06</div>
          <h2>PayFast Split Payments &amp; Platform Tollbooth</h2>
          <p>
            The Finisher features integrated PayFast Split Payments. When enterprise clients settle an invoice, funds are divided instantaneously at the payment gateway:
          </p>
          <div class="spec-callout">
            <div class="callout-icon">💳</div>
            <div class="callout-body">
              <strong>Automated Gateway Settlement (Instant Disbursal)</strong>
              <p>Your commercial bank account receives net proceeds directly from PayFast. The platform facilitation slice is settled simultaneously, with zero manual reconciliation required.</p>
            </div>
          </div>
          <div class="screenshot-preview">
            <img src="/screenshots/05_payfast_integrations.png" alt="PayFast Integrations" class="doc-img" />
            <span class="img-caption">Figure 6.1: Live PayFast split settlement and webhook handshakes</span>
          </div>
        </section>

        <!-- 07: Tender Pack -->
        <section id="compliance" class="doc-section card">
          <div class="section-tag">CHAPTER 07</div>
          <h2>Statutory Tender &amp; SEDA Funding Bank Pack</h2>
          <p>
            When pitching for government tenders or applying for commercial bank expansion loans, credit committees require verifiable past performance. 
          </p>
          <p>
            Under <em>Reports</em>, The Finisher compiles your 12-month deal ledger into an official, bank-ready PDF dossier featuring:
          </p>
          <ul class="doc-list">
            <li><strong>National Treasury CSD Formatting:</strong> Ready for upload to the Central Supplier Database.</li>
            <li><strong>POPIA Section 19 Compliance Certificate:</strong> Demonstrating certified cryptographic data protection.</li>
            <li><strong>Tamper-Proof SHA-256 Audit Seal:</strong> Allowing bank adjudicators to verify the integrity of the document via QR code.</li>
          </ul>
          <div class="screenshot-preview">
            <img src="/screenshots/06_tender_compliance_pack.png" alt="Tender Pack" class="doc-img" />
            <span class="img-caption">Figure 7.1: Statutory Tender & SEDA Funding Compliance Pack</span>
          </div>
        </section>

        <!-- 08: Team Governance -->
        <section id="governance" class="doc-section card">
          <div class="section-tag">CHAPTER 08</div>
          <h2>Role-Based Access Control (RBAC) &amp; Team Governance</h2>
          <p>
            Enterprise security demands that employees only access data strictly necessary for their function. The Finisher implements zero-trust role-based permissions:
          </p>
          <table class="role-table">
            <thead>
              <tr>
                <th>Role</th>
                <th>Clearance Level</th>
                <th>Permitted Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Owner / Superuser</strong></td>
                <td><span class="badge-gold">Sovereign Root</span></td>
                <td>Full system configuration, PayFast merchant keys, tenant management.</td>
              </tr>
              <tr>
                <td><strong>Executive Admin</strong></td>
                <td><span class="badge-blue">Level 1 Executive</span></td>
                <td>Pipeline management, contract approval, compliance exports, staff onboarding.</td>
              </tr>
              <tr>
                <td><strong>Commercial Sales</strong></td>
                <td><span class="badge-amber">Level 2 Sales</span></td>
                <td>Contact capture, deal negotiations, quote dispatch, advisory timers.</td>
              </tr>
              <tr>
                <td><strong>Compliance / Legal</strong></td>
                <td><span class="badge-purple">Level 2 Audit</span></td>
                <td>POPIA logs review, CIPC record audits, statutory report generation.</td>
              </tr>
            </tbody>
          </table>
          <div class="screenshot-preview">
            <img src="/screenshots/09_employee_directory.png" alt="Employee Directory" class="doc-img" />
            <span class="img-caption">Figure 8.1: Role-based employee security directory</span>
          </div>
        </section>

        <!-- 09: Standard Operating Protocol -->
        <section id="sop" class="doc-section card">
          <div class="section-tag">CHAPTER 09</div>
          <h2>Executive 5-Step Operating Protocol (SOP)</h2>
          <p>
            To ensure zero operational error, every member of your commercial team must execute engagements in the following sequence:
          </p>
          <div class="timeline-sop">
            <div class="sop-step">
              <span class="sop-num">1</span>
              <div>
                <h4>Capture Contact</h4>
                <p>Record the executive decision-maker under Contacts before initiating any company creation.</p>
              </div>
            </div>
            <div class="sop-step">
              <span class="sop-num">2</span>
              <div>
                <h4>Establish CIPC Company Record</h4>
                <p>Register the formal entity with valid registration number, link the contact, and confirm headquarters.</p>
              </div>
            </div>
            <div class="sop-step">
              <span class="sop-num">3</span>
              <div>
                <h4>Initialize Deal Opportunity</h4>
                <p>Open the deal in the pipeline, attach valuation, select estimated closure date, and start tracking advisory time.</p>
              </div>
            </div>
            <div class="sop-step">
              <span class="sop-num">4</span>
              <div>
                <h4>Issue Formal PDF Quotation</h4>
                <p>Generate and transmit an audited commercial proposal directly through the CRM's high-entropy email engine.</p>
              </div>
            </div>
            <div class="sop-step">
              <span class="sop-num">5</span>
              <div>
                <h4>Execute PayFast Settlement</h4>
                <p>Client pays via Instant EFT or Card; webhook automatically shifts deal to Closed Won and disburses funds.</p>
              </div>
            </div>
          </div>
          <div class="screenshot-preview">
            <img src="/screenshots/07_help_and_enablement.png" alt="Help Center SOP" class="doc-img" />
            <span class="img-caption">Figure 9.1: Institutional Help & Enablement SOP portal</span>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SystemDocumentation',
  data() {
    return {
      activeSection: 'architecture',
      tocItems: [
        { id: 'architecture', num: '01', title: 'System Architecture' },
        { id: 'dashboard', num: '02', title: 'Executive Dashboard' },
        { id: 'contacts', num: '03', title: 'VIP Contacts' },
        { id: 'companies', num: '04', title: 'CIPC Businesses' },
        { id: 'deals', num: '05', title: 'Deals & Pipeline' },
        { id: 'splits', num: '06', title: 'PayFast Splits' },
        { id: 'compliance', num: '07', title: 'Tender Bank Pack' },
        { id: 'governance', num: '08', title: 'Team Governance' },
        { id: 'sop', num: '09', title: '5-Step Protocol' }
      ]
    }
  },
  methods: {
    launchVideoTutorial() {
      window.dispatchEvent(new CustomEvent('open-system-tutorial'))
    },
    scrollToSection(sectionId) {
      this.activeSection = sectionId
      const el = document.getElementById(sectionId)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }
  }
}
</script>

<style scoped>
.doc-page-container {
  padding: 1.5rem 2rem 4rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Hero Header */
.doc-hero {
  background: linear-gradient(180deg, #131724 0%, #0c0f1a 100%);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 16px;
  padding: 2.5rem 3rem;
  margin-bottom: 2rem;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5);
}

.brand-crest {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #d4af37;
  margin-bottom: 0.75rem;
}

.crest-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #d4af37;
  box-shadow: 0 0 8px #d4af37;
}

.hero-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 0.75rem;
  letter-spacing: -0.5px;
}

.hero-sub {
  font-size: 1.05rem;
  color: #94a3b8;
  max-width: 800px;
  line-height: 1.6;
  margin: 0 0 1.5rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

/* Layout */
.doc-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2rem;
  align-items: flex-start;
}

/* Sticky Sidebar */
.doc-toc-sidebar {
  position: sticky;
  top: 90px;
}

.toc-card {
  background: #0f1320;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1.25rem 1rem;
}

.toc-badge {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 1.2px;
  color: #d4af37;
  display: block;
  margin-bottom: 1rem;
  padding-left: 8px;
}

.toc-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toc-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 6px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.82rem;
  transition: all 0.2s;
}

.toc-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
}

.toc-link.active {
  background: rgba(212, 175, 55, 0.12);
  color: #d4af37;
  font-weight: 700;
}

.toc-num {
  font-size: 0.7rem;
  font-family: monospace;
  color: #d4af37;
}

/* Content Area */
.doc-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.doc-section {
  background: #0f1320;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 2.25rem 2.5rem;
}

.section-tag {
  font-size: 0.7rem;
  font-weight: 800;
  color: #d4af37;
  letter-spacing: 1.2px;
  margin-bottom: 0.5rem;
}

.doc-section h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 1rem;
}

.lead-text {
  font-size: 1.02rem;
  color: #cbd5e1;
  line-height: 1.6;
}

.doc-section p {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 1.25rem;
}

.spec-callout {
  display: flex;
  gap: 14px;
  background: rgba(212, 175, 55, 0.06);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 10px;
  padding: 1.25rem;
  margin: 1.25rem 0;
}

.callout-icon {
  font-size: 1.5rem;
}

.callout-body strong {
  display: block;
  font-size: 0.9rem;
  color: #d4af37;
  margin-bottom: 4px;
}

.callout-body p {
  margin: 0;
  font-size: 0.85rem;
  color: #e2e8f0;
}

.screenshot-preview {
  margin: 1.5rem 0 0.5rem;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: #070910;
}

.doc-img {
  width: 100%;
  display: block;
  object-fit: contain;
}

.img-caption {
  display: block;
  padding: 8px 14px;
  font-size: 0.75rem;
  color: #64748b;
  background: #090c15;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.pro-tip-block {
  background: rgba(16, 185, 129, 0.08);
  border: 1px dashed rgba(16, 185, 129, 0.35);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin: 1.25rem 0;
}

.pro-tip-block strong {
  display: block;
  font-size: 0.78rem;
  color: #10b981;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.pro-tip-block p {
  margin: 0;
  color: #e2e8f0;
  font-size: 0.85rem;
}

.doc-list {
  padding-left: 1.5rem;
  color: #94a3b8;
  margin-bottom: 1.25rem;
}

.doc-list li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.doc-list strong {
  color: #ffffff;
}

/* Step Guides */
.step-guide {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1.25rem 0;
}

.step-row {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 1rem;
}

.badge-num {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #d4af37;
  color: #0b0f19;
  font-weight: 800;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-row strong {
  color: #ffffff;
  font-size: 0.88rem;
  display: block;
  margin-bottom: 4px;
}

.step-row p {
  margin: 0;
  font-size: 0.82rem;
}

/* Feature Bullets */
.feature-bullets {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1.25rem 0;
}

.bullet-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 1rem;
}

.bullet-card h4 {
  margin: 0 0 6px;
  font-size: 0.88rem;
  color: #d4af37;
}

.bullet-card p {
  margin: 0;
  font-size: 0.8rem;
}

/* Role Table */
.role-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25rem 0;
  font-size: 0.85rem;
}

.role-table th {
  text-align: left;
  padding: 10px 12px;
  background: #151926;
  color: #cbd5e1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.role-table td {
  padding: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #94a3b8;
}

.badge-gold { background: rgba(212, 175, 55, 0.15); color: #d4af37; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; }
.badge-blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; }
.badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; }
.badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; }

/* SOP Timeline */
.timeline-sop {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 1.5rem 0;
}

.sop-step {
  display: flex;
  gap: 14px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 1rem;
}

.sop-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #d4af37;
  color: #0b0f19;
  font-weight: 800;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sop-step h4 {
  margin: 0 0 4px;
  font-size: 0.88rem;
  color: #ffffff;
}

.sop-step p {
  margin: 0;
  font-size: 0.82rem;
}

/* Buttons */
.btn-gold {
  background: linear-gradient(135deg, #d4af37 0%, #b8972f 100%);
  color: #0b0f19;
  font-weight: 800;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  font-size: 0.88rem;
}

.btn-outline-luxury {
  background: transparent;
  color: #d4af37;
  border: 1px solid rgba(212, 175, 55, 0.4);
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  font-size: 0.88rem;
  display: inline-flex;
  align-items: center;
}

@media (max-width: 900px) {
  .doc-layout {
    grid-template-columns: 1fr;
  }
  .doc-toc-sidebar {
    display: none;
  }
}
</style>
