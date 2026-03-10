<template>
  <div class="doc-page">
    <div class="doc-container">
      <button class="back-btn" @click="$router.push('/')">← Back to Home</button>
      
      <h1>Privacy Policy</h1>
      <p class="last-updated">Last Updated: January 10, 2026</p>

      <section>
        <h2>1. Introduction</h2>
        <p>THE FINISHER LUXURY ("we", "our", "us") respects your privacy and is committed to protecting your personal data. This privacy policy explains how we collect, use, and safeguard your information in compliance with South Africa's Protection of Personal Information Act (POPIA).</p>
      </section>

      <section>
        <h2>2. Information We Collect</h2>
        <h3>2.1 Personal Information</h3>
        <ul>
          <li>Name, email address, phone number</li>
          <li>Company name and business details</li>
          <li>Job title and department</li>
          <li>Profile picture (optional)</li>
        </ul>

        <h3>2.2 Usage Data</h3>
        <ul>
          <li>Login times and activity logs</li>
          <li>CRM interactions (contacts, deals, tickets)</li>
          <li>Performance metrics</li>
          <li>Browser type and IP address</li>
        </ul>
      </section>

      <section>
        <h2>3. How We Use Your Data</h2>
        <ul>
          <li>To provide and maintain our CRM service</li>
          <li>To manage your account and subscription</li>
          <li>To send service updates and notifications</li>
          <li>To improve our platform and user experience</li>
          <li>To comply with legal obligations</li>
        </ul>
      </section>

      <section>
        <h2>4. Data Security</h2>
        <p>We implement industry-standard security measures:</p>
        <ul>
          <li>Encrypted data transmission (HTTPS/TLS)</li>
          <li>Secure password hashing</li>
          <li>Regular security audits</li>
          <li>Access controls and authentication</li>
          <li>Secure cloud infrastructure</li>
        </ul>
      </section>

      <section>
        <h2>5. Your POPIA Rights</h2>
        <p>Under POPIA, you have the right to:</p>
        <ul>
          <li>Access your personal information</li>
          <li>Correct inaccurate data</li>
          <li>Delete your account and data</li>
          <li>Object to data processing</li>
          <li>Data portability</li>
          <li>Lodge a complaint with the Information Regulator</li>
        </ul>
      </section>

      <section>
        <h2>6. Data Retention</h2>
        <p>We retain your data for as long as your account is active. Upon deletion request, we remove all personal data within 30 days, except where retention is required by law.</p>
      </section>

      <section>
        <h2>7. Third-Party Services</h2>
        <p>We may share data with trusted service providers:</p>
        <ul>
          <li>Cloud hosting providers (AWS/Railway)</li>
          <li>Payment processors (for paid tiers)</li>
          <li>Email service providers</li>
        </ul>
        <p>All third parties are contractually bound to protect your data.</p>
      </section>

      <section>
        <h2>8. Contact Us</h2>
        <p>For privacy concerns or to exercise your POPIA rights:</p>
        <p><strong>Email:</strong> privacy@thefinisher.co.za</p>
        <p><strong>Phone:</strong> +27 (0)10 123 4567</p>
        <p><strong>Address:</strong> Johannesburg, South Africa</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrivacyPolicy'
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
