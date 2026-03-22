<template>
  <div class="doc-page">
    <div class="doc-container">
      <button class="back-btn" @click="$router.push('/')">← Back to Home</button>
      
      <h1>Terms of Service</h1>
      <p class="last-updated">Last Updated: March 22, 2026</p>

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
        <p><strong>Legal / Privacy:</strong> legal@thefinisher.co.za</p>
        <p><strong>Data Protection / DPO:</strong> privacy@thefinisher.co.za</p>
        <p><strong>Support:</strong> support@thefinisher.co.za</p>
        <p><strong>Phone:</strong> +27 (0)10 123 4567</p>
      </section>

      <section>
        <h2>13. POPIA Compliance</h2>
        <p>We process personal information in accordance with the Protection of Personal Information Act (POPIA) (Act No. 4 of 2013). THE FINISHER LUXURY is committed to protecting the privacy and personal information of our users and customers. We will only collect, use, retain and disclose personal information where there is a lawful basis for doing so and for purposes set out in these Terms and our Privacy Policy.</p>
        <p>Data subjects have rights under POPIA, including the right to access, correct, request deletion of, or object to certain processing of their personal information. To exercise these rights or to contact our Data Protection Officer, please email <strong>privacy@thefinisher.co.za</strong> or <strong>legal@thefinisher.co.za</strong>. We will respond to privacy requests in accordance with applicable law.</p>
        <p>We retain personal information only for as long as necessary to fulfil the purposes for which it was collected or to comply with legal obligations. We implement reasonable technical and organisational measures to protect personal information against loss, unauthorized access, disclosure, or other unlawful processing.</p>
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
  background: #000000;
  color: #ffffff;
  padding: 2rem;
  font-family: 'Inter', system-ui, sans-serif;
}

.doc-container {
  max-width: 900px;
  margin: 0 auto;
  background: linear-gradient(135deg, rgba(15,15,15,0.8) 0%, rgba(5,5,5,0.9) 100%);
  backdrop-filter: blur(20px);
  padding: 3rem;
  border-radius: 16px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.9), inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}

.back-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
  color: #9ca3af;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 0.8125rem;
}

.back-btn:hover {
  border-color: #ffffff;
  color: #ffffff;
  transform: translateX(-4px);
}

h1 {
  font-size: 2.5rem;
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-weight: 800;
  letter-spacing: 1px;
}

.last-updated {
  color: #9ca3af;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

section {
  margin: 2rem 0;
}

h2 {
  font-size: 1.5rem;
  color: #D4AF37;
  margin: 2rem 0 1rem 0;
  font-weight: 700;
  letter-spacing: 1px;
}

h3 {
  font-size: 1.1rem;
  color: #B49015;
  margin: 1.5rem 0 0.75rem 0;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

p {
  line-height: 1.8;
  margin: 1rem 0;
  color: #d1d5db;
}

ul {
  margin: 1rem 0;
  padding-left: 2rem;
}

li {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #d1d5db;
}

strong {
  color: #ffffff;
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
