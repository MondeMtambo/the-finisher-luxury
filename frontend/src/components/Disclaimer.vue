<template>
  <div class="doc-page">
    <div class="doc-container">
      <button class="back-btn" @click="$router.push('/')">← Back to Home</button>

      <h1>Disclaimer &amp; Privacy Notice</h1>
      <p class="subtitle"><strong>Company:</strong> MTAMBO HOLDINGS &bull; <strong>Product:</strong> THE FINISHER LUXURY CRM</p>
      <p class="last-updated">Effective date: 2 November 2026</p>

      <section class="copyright-section">
        <h2>Copyright &amp; Intellectual Property Protection</h2>
        <p><strong>&copy; 2026 MTAMBO HOLDINGS. All Rights Reserved.</strong><br>THE FINISHER LUXURY CRM is proprietary software owned exclusively by MTAMBO HOLDINGS. This application, including all source code, design elements, user interfaces, features, documentation, and associated materials, is protected by South African and international copyright laws.</p>
        <ul>
          <li><strong>No Reproduction:</strong> Unauthorized copying, reproduction, modification, or distribution of any part of this software is strictly prohibited.</li>
          <li><strong>No Reverse Engineering:</strong> Users are prohibited from decompiling, disassembling, or reverse engineering the software.</li>
          <li><strong>Trademark Protection:</strong> "THE FINISHER LUXURY", the logo, and related marks are trademarks of MTAMBO HOLDINGS.</li>
          <li><strong>Legal Action:</strong> Violations will result in immediate legal action including civil and criminal prosecution to the fullest extent of the law.</li>
          <li><strong>Licensing:</strong> Use of this software is granted solely under explicit license agreement. Unauthorized commercial use is forbidden.</li>
        </ul>
        <div class="warn-box"><strong>PLAGIARISM WARNING:</strong> Any attempt to copy, steal, clone, or pass off this software as your own work will be met with swift legal action. We actively monitor for unauthorized use and maintain detailed audit trails.</div>
      </section>

      <section>
        <h2>Purpose</h2>
        <p>This page explains how MTAMBO HOLDINGS ("we", "us") processes personal information when you use THE FINISHER LUXURY CRM (the "Service"). It also provides important legal disclosures, including your rights under the South African Protection of Personal Information Act, 2013 (POPIA).</p>
      </section>

      <section>
        <h2>What we collect &amp; How we use data</h2>
        <ul>
          <li>Account and authentication data (username, hashed password, optional profile details).</li>
          <li>Content you (our client) choose to store in the CRM, e.g., contacts, companies, deals, notes.</li>
          <li>Technical and usage data (logs, device/browser metadata, IP address) for security and diagnostics.</li>
          <li>Provide, secure, and maintain the Service (authentication, storage, backups, availability).</li>
          <li>Improve features and performance (aggregated analytics, troubleshooting, quality assurance).</li>
          <li>Comply with legal obligations and enforce terms, prevent fraud and abuse.</li>
        </ul>
      </section>

      <section>
        <h2>POPIA: Key principles</h2>
        <ul>
          <li><strong>Lawfulness, fairness, transparency:</strong> Processing occurs on a valid legal basis and with clear notices.</li>
          <li><strong>Purpose limitation:</strong> Data is used for specified, explicit, and legitimate purposes only.</li>
          <li><strong>Data minimisation:</strong> We collect only what is necessary for the Service.</li>
          <li><strong>Accuracy:</strong> You control and must keep CRM data accurate and up to date.</li>
          <li><strong>Storage limitation:</strong> Data is kept only as long as needed for the purposes stated.</li>
          <li><strong>Security safeguards:</strong> Reasonable technical and organisational measures are applied to protect data.</li>
          <li><strong>Data subject rights:</strong> Access, correction, deletion, objection, and complaint rights are respected.</li>
        </ul>
        <p class="note">Under POPIA, MTAMBO HOLDINGS is generally the <em>Operator</em> for client CRM content, and the client is the <em>Responsible Party</em>.</p>
      </section>

      <section>
        <h2>Client responsibilities &amp; Sharing</h2>
        <ul>
          <li>Obtain and document lawful basis/consent from your contacts where required.</li>
          <li>Only upload data you are authorised to process; delete data when no longer necessary.</li>
          <li>Respond to data subject requests (access/correction/deletion) for your CRM records.</li>
          <li>We do not sell personal information.</li>
          <li>Service providers (e.g., hosting, email) may process data under written agreements with safeguards.</li>
        </ul>
      </section>

      <section>
        <h2>Security &amp; Retention</h2>
        <ul>
          <li>Encrypted transport (HTTPS) and industry-standard hashing for passwords.</li>
          <li>Access controls, logging, and monitoring for suspicious activity.</li>
          <li>We retain personal data only as long as necessary to provide the Service and meet legal obligations.</li>
          <li>Clients may delete their CRM records at any time; backups are purged on a rolling schedule.</li>
        </ul>
      </section>

      <section>
        <h2>Your rights</h2>
        <ul>
          <li>Request access to your personal information.</li>
          <li>Request correction or deletion (subject to legal/contractual limits).</li>
          <li>Object to certain processing and withdraw consent where relied upon.</li>
          <li>Lodge a complaint with the Information Regulator (South Africa).</li>
        </ul>
        <p class="note">For CRM records owned by a client, please contact that client as the Responsible Party.</p>
      </section>

      <section>
        <h2>Contact &amp; Legal Inquiries</h2>
        <p>For privacy, legal queries, or licensing inquiries, contact MTAMBO HOLDINGS at <strong>legal@mtamboholdings.co.za</strong><br>
        <strong>Address:</strong> MTAMBO HOLDINGS, South Africa<br>
        <strong>Product Support:</strong> support@thefinisher.co.za</p>
      </section>

      <div class="legal-footer">
        <p><strong>&copy; 2026 MTAMBO HOLDINGS. All rights reserved.</strong></p>
        <p>THE FINISHER LUXURY CRM - PREMIUM LUXURY EDITION</p>
        <p>Protected by South African and International Copyright Laws</p>
        <p class="warn-footer">Unauthorized use, reproduction, or distribution is strictly prohibited and subject to legal prosecution.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Disclaimer'
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
  transition: all 0.3s ease;
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

.subtitle {
  color: #d1d5db;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
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

.copyright-section h2 {
  color: #ffffff;
}

.warn-box {
  background: rgba(239, 68, 68, 0.1);
  border-left: 4px solid #ef4444;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ef4444;
}

.legal-footer {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  text-align: center;
}

.legal-footer p {
  margin: 0.5rem 0;
  font-size: 0.875rem;
  color: #9ca3af;
}

.warn-footer {
  color: #D4AF37 !important;
  font-weight: 700;
  font-size: 0.75rem !important;
  margin-top: 1rem !important;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.note {
  font-size: 0.875rem;
  color: #9ca3af;
  font-style: italic;
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
