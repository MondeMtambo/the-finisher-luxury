<template>
  <div class="doc-page">
    <div class="doc-container">
      <button class="back-btn" @click="$router.push('/')">← Back to Home</button>
      
      <h1>POPIA Compliance Statement</h1>
      <p class="last-updated">Last Updated: January 10, 2026</p>

      <section>
        <h2>Our Commitment to POPIA</h2>
        <p>THE FINISHER LUXURY is fully compliant with South Africa's Protection of Personal Information Act (POPIA, Act 4 of 2013). We are committed to protecting your personal information and respecting your privacy rights.</p>
      </section>

      <section>
        <h2>Information Officer</h2>
        <p><strong>Name:</strong> Monde Mtambo</p>
        <p><strong>Email:</strong> thefinishercrm@gmail.com</p>
        <p><strong>Phone:</strong> +27 (0)10 123 4567</p>
        <p>Our Information Officer is responsible for ensuring POPIA compliance across all operations.</p>
      </section>

      <section>
        <h2>POPIA Principles We Follow</h2>
        
        <h3>1. Accountability</h3>
        <p>We take full responsibility for personal information under our control and have implemented appropriate policies and procedures.</p>

        <h3>2. Processing Limitation</h3>
        <p>We only process personal information that is:</p>
        <ul>
          <li>Necessary for our CRM service delivery</li>
          <li>Collected with your consent</li>
          <li>Processed lawfully and transparently</li>
        </ul>

        <h3>3. Purpose Specification</h3>
        <p>We collect data solely for:</p>
        <ul>
          <li>Providing CRM services</li>
          <li>Account management</li>
          <li>Customer support</li>
          <li>Service improvements</li>
          <li>Legal compliance</li>
        </ul>

        <h3>4. Further Processing Limitation</h3>
        <p>We do not use your data for purposes beyond what was originally specified without obtaining fresh consent.</p>

        <h3>5. Information Quality</h3>
        <p>We ensure your personal information is:</p>
        <ul>
          <li>Complete and accurate</li>
          <li>Not misleading</li>
          <li>Updated where necessary</li>
        </ul>

        <h3>6. Openness</h3>
        <p>We maintain full transparency about:</p>
        <ul>
          <li>What data we collect</li>
          <li>How we process it</li>
          <li>Who has access to it</li>
          <li>Your rights regarding your data</li>
        </ul>

        <h3>7. Security Safeguards</h3>
        <p>We implement robust security measures:</p>
        <ul>
          <li>Encryption at rest and in transit</li>
          <li>Access controls and authentication</li>
          <li>Regular security audits</li>
          <li>Staff training on data protection</li>
          <li>Incident response procedures</li>
        </ul>

        <h3>8. Data Subject Participation</h3>
        <p>You have the right to:</p>
        <ul>
          <li>Request confirmation of what data we hold</li>
          <li>Access your personal information</li>
          <li>Correct or update your data</li>
          <li>Object to processing</li>
          <li>Request data deletion</li>
          <li>Data portability</li>
        </ul>
      </section>

      <section>
        <h2>Data Breach Procedures</h2>
        <p>In the unlikely event of a data breach, we will:</p>
        <ul>
          <li>Notify the Information Regulator within 72 hours</li>
          <li>Inform affected data subjects promptly</li>
          <li>Take immediate remedial action</li>
          <li>Conduct a thorough investigation</li>
          <li>Implement additional safeguards</li>
        </ul>
      </section>

      <section>
        <h2>Third-Party Processors</h2>
        <p>We only work with processors who:</p>
        <ul>
          <li>Are POPIA-compliant or equivalent (GDPR)</li>
          <li>Have signed data processing agreements</li>
          <li>Implement adequate security measures</li>
          <li>Do not process data for their own purposes</li>
        </ul>
      </section>

      <section>
        <h2>Children's Privacy</h2>
        <p>Our service is not directed at children under 18. We do not knowingly collect personal information from minors without parental consent.</p>
      </section>

      <section>
        <h2>Cross-Border Data Transfers</h2>
        <p>Data is primarily hosted in South Africa. If cross-border transfers occur, we ensure:</p>
        <ul>
          <li>Adequate levels of protection</li>
          <li>Compliance with POPIA Section 72</li>
          <li>Contractual safeguards with processors</li>
        </ul>
      </section>

      <section>
        <h2>Filing a Complaint</h2>
        <p>If you believe we have violated your privacy rights:</p>
        <p><strong>Contact us first:</strong> thefinishercrm@gmail.com</p>
        <p><strong>Or lodge a complaint with:</strong></p>
        <p>
          Information Regulator (South Africa)<br>
          Email: inforeg@justice.gov.za<br>
          Website: www.justice.gov.za/inforeg
        </p>
      </section>

      <section>
        <h2>Policy Updates</h2>
        <p>We review this policy annually. Material changes will be communicated via email and require fresh consent where necessary.</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PopiaCompliance'
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
