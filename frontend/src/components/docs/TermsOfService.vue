<template>
  <div class="doc-page">
    <div class="doc-container">
      <button class="back-btn" @click="$router.push('/')">← Back to Home</button>
      
      <h1>Terms of Service</h1>
      <p class="last-updated">Last Updated: January 10, 2026</p>

      <section>
        <h2>1. Acceptance of Terms</h2>
        <p>By accessing and using THE FINISHER LUXURY ("Service"), you agree to be bound by these Terms of Service. If you do not agree, please do not use our service.</p>
      </section>

      <section>
        <h2>2. Service Description</h2>
        <p>THE FINISHER LUXURY is a cloud-based CRM platform designed for South African businesses. We provide contact management, deal tracking, ticketing, and analytics tools.</p>
      </section>

      <section>
        <h2>3. Account Registration</h2>
        <ul>
          <li>You must provide accurate and complete information</li>
          <li>You are responsible for maintaining account security</li>
          <li>You must be 18 years or older to use this service</li>
          <li>One person may not maintain multiple accounts</li>
        </ul>
      </section>

      <section>
        <h2>4. Subscription and Pricing</h2>
        <h3>4.1 Free Tier</h3>
        <p>Our CLASSIC tier is <strong>free forever</strong> for 1 user with core features.</p>

        <h3>4.2 Paid Tiers</h3>
        <ul>
          <li><strong>SPORT:</strong> R99/month for 2 users</li>
          <li><strong>LUXURY:</strong> R249/month for 10 users</li>
          <li><strong>PREMIUM:</strong> R499/month for unlimited users</li>
        </ul>
        <p>Prices are in South African Rand (ZAR) and exclude VAT where applicable.</p>

        <h3>4.3 Billing</h3>
        <ul>
          <li>Monthly subscriptions are billed in advance</li>
          <li>No refunds for partial months</li>
          <li>You may cancel at any time</li>
          <li>Downtime credits may be issued for service disruptions</li>
        </ul>
      </section>

      <section>
        <h2>5. Acceptable Use</h2>
        <p>You agree NOT to:</p>
        <ul>
          <li>Violate any laws or regulations</li>
          <li>Upload malicious code or viruses</li>
          <li>Attempt to breach security measures</li>
          <li>Scrape or reverse-engineer our platform</li>
          <li>Use the service for spam or harassment</li>
          <li>Impersonate others or misrepresent affiliation</li>
        </ul>
      </section>

      <section>
        <h2>6. Data Ownership</h2>
        <ul>
          <li>You retain all rights to your data</li>
          <li>We do not sell or share your data with third parties</li>
          <li>You can export your data at any time</li>
          <li>Upon account deletion, data is removed within 30 days</li>
        </ul>
      </section>

      <section>
        <h2>7. Service Availability</h2>
        <p>We strive for 99.9% uptime but do not guarantee uninterrupted service. Scheduled maintenance will be announced in advance.</p>
      </section>

      <section>
        <h2>8. Limitation of Liability</h2>
        <p>THE FINISHER LUXURY is provided "as is" without warranties. We are not liable for:</p>
        <ul>
          <li>Data loss due to user error</li>
          <li>Business losses or lost profits</li>
          <li>Third-party integrations or services</li>
          <li>Force majeure events</li>
        </ul>
      </section>

      <section>
        <h2>9. Termination</h2>
        <p>We reserve the right to suspend or terminate accounts that violate these terms. Users may cancel their account at any time from the dashboard.</p>
      </section>

      <section>
        <h2>10. Changes to Terms</h2>
        <p>We may update these terms. Continued use after changes constitutes acceptance. Material changes will be communicated via email.</p>
      </section>

      <section>
        <h2>11. Governing Law</h2>
        <p>These terms are governed by the laws of South Africa. Disputes will be resolved in South African courts.</p>
      </section>

      <section>
        <h2>12. Contact</h2>
        <p><strong>Email:</strong> legal@thefinisher.co.za</p>
        <p><strong>Support:</strong> support@thefinisher.co.za</p>
        <p><strong>Phone:</strong> +27 (0)10 123 4567</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TermsOfService'
}
</script>

<style scoped>
.doc-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  padding: 2rem;
}

.doc-container {
  max-width: 900px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.05);
  padding: 3rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.back-btn {
  background: rgba(56, 189, 248, 0.2);
  border: 1px solid rgba(56, 189, 248, 0.4);
  color: #38bdf8;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(56, 189, 248, 0.3);
  transform: translateX(-4px);
}

h1 {
  font-size: 2.5rem;
  color: #f8fafc;
  margin-bottom: 0.5rem;
  font-weight: 800;
}

.last-updated {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

section {
  margin: 2rem 0;
}

h2 {
  font-size: 1.8rem;
  color: #38bdf8;
  margin: 2rem 0 1rem 0;
  font-weight: 700;
}

h3 {
  font-size: 1.3rem;
  color: #93c5fd;
  margin: 1.5rem 0 0.75rem 0;
  font-weight: 600;
}

p {
  line-height: 1.8;
  margin: 1rem 0;
  color: #cbd5e1;
}

ul {
  margin: 1rem 0;
  padding-left: 2rem;
}

li {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #cbd5e1;
}

strong {
  color: #f8fafc;
  font-weight: 700;
}

@media (max-width: 768px) {
  .doc-container {
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>
