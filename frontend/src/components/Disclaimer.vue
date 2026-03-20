<template>
  <section class="disclaimer-page">
    <div class="page-header">
      <h1>Disclaimer, Privacy Notice &amp; Copyright Protection</h1>
      <p class="page-subtitle"><strong>Company:</strong> MTAMBO HOLDINGS &bull; <strong>Product:</strong> THE FINISHER LUXURY CRM - PREMIUM EDITION</p>
      <p style="font-size:.75rem;color:var(--gray-400)">Effective date: 2 November 2026</p>
    </div>

    <div class="card copyright-card">
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
    </div>

    <div class="card"><h2>Purpose</h2><p>This page explains how MTAMBO HOLDINGS ("we", "us") processes personal information when you use THE FINISHER LUXURY CRM (the "Service"). It also provides important legal disclosures, including your rights under the South African Protection of Personal Information Act, 2013 (POPIA).</p></div>

    <div class="card-grid">
      <div class="card"><h2>What we collect</h2><ul><li>Account and authentication data (username, hashed password, optional profile details).</li><li>Content you (our client) choose to store in the CRM, e.g., contacts, companies, deals, notes.</li><li>Technical and usage data (logs, device/browser metadata, IP address) for security and diagnostics.</li></ul></div>
      <div class="card"><h2>How we use data</h2><ul><li>Provide, secure, and maintain the Service (authentication, storage, backups, availability).</li><li>Improve features and performance (aggregated analytics, troubleshooting, quality assurance).</li><li>Comply with legal obligations and enforce terms, prevent fraud and abuse.</li></ul></div>
    </div>

    <div class="card"><h2>POPIA: Key principles</h2><ul>
      <li><strong>Lawfulness, fairness, transparency:</strong> Processing occurs on a valid legal basis and with clear notices.</li>
      <li><strong>Purpose limitation:</strong> Data is used for specified, explicit, and legitimate purposes only.</li>
      <li><strong>Data minimisation:</strong> We collect only what is necessary for the Service.</li>
      <li><strong>Accuracy:</strong> You control and must keep CRM data accurate and up to date.</li>
      <li><strong>Storage limitation:</strong> Data is kept only as long as needed for the purposes stated.</li>
      <li><strong>Security safeguards:</strong> Reasonable technical and organisational measures are applied to protect data.</li>
      <li><strong>Data subject rights:</strong> Access, correction, deletion, objection, and complaint rights are respected.</li>
    </ul><p class="note">Under POPIA, MTAMBO HOLDINGS is generally the <em>Operator</em> for client CRM content, and the client is the <em>Responsible Party</em>.</p></div>

    <div class="card-grid">
      <div class="card"><h2>Client responsibilities</h2><ul><li>Obtain and document lawful basis/consent from your contacts where required.</li><li>Only upload data you are authorised to process; delete data when no longer necessary.</li><li>Respond to data subject requests (access/correction/deletion) for your CRM records.</li><li>Keep credentials secure and manage user access appropriately.</li></ul></div>
      <div class="card"><h2>Sharing and transfers</h2><ul><li>We do not sell personal information.</li><li>Service providers (e.g., hosting, email) may process data under written agreements with safeguards.</li><li>Cross-border transfers (if any) follow applicable adequacy or safeguard mechanisms.</li></ul></div>
    </div>

    <div class="card-grid">
      <div class="card"><h2>Security</h2><ul><li>Encrypted transport (HTTPS) and industry-standard hashing for passwords.</li><li>Access controls, logging, and monitoring for suspicious activity.</li><li>Least-privilege and need-to-know principles for operator access.</li></ul></div>
      <div class="card"><h2>Retention</h2><ul><li>We retain personal data only as long as necessary to provide the Service and meet legal obligations.</li><li>Clients may delete their CRM records at any time; backups are purged on a rolling schedule.</li></ul></div>
    </div>

    <div class="card"><h2>Your rights</h2><ul><li>Request access to your personal information.</li><li>Request correction or deletion (subject to legal/contractual limits).</li><li>Object to certain processing and withdraw consent where relied upon.</li><li>Lodge a complaint with the Information Regulator (South Africa).</li></ul><p class="note">For CRM records owned by a client, please contact that client as the Responsible Party.</p></div>

    <div class="card"><h2>Contact &amp; Legal Inquiries</h2><p>For privacy, legal queries, or licensing inquiries, contact MTAMBO HOLDINGS at <strong>legal@mtamboholdings.co.za</strong><br><strong>Address:</strong> MTAMBO HOLDINGS, South Africa<br><strong>Product Support:</strong> support@thefinishersport.co.za<br>We will respond within a reasonable timeframe.</p></div>

    <div class="legal-footer">
      <p><strong>&copy; 2026 MTAMBO HOLDINGS. All rights reserved.</strong></p>
      <p>THE FINISHER LUXURY CRM - PREMIUM LUXURY EDITION</p>
      <p>Protected by South African and International Copyright Laws</p>
      <p class="warn-footer">Unauthorized use, reproduction, or distribution is strictly prohibited and subject to legal prosecution.</p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Disclaimer'
}
</script>
<style scoped>
.disclaimer-page { max-width:960px; margin:0 auto; display:flex; flex-direction:column; gap:1.25rem; }
.card h2 { font-size:1rem; font-weight:600; color:var(--gray-900); margin:0 0 .75rem; }
.card ul { margin:.5rem 0 0; padding-left:1.25rem; font-size:.8125rem; color:var(--gray-600); line-height:1.7; }
.card li { margin:.25rem 0; }
.card p { font-size:.8125rem; color:var(--gray-600); line-height:1.6; margin:.25rem 0; }
.card strong { color:var(--gray-900); }
.card-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:1rem; }
.note { margin-top:.75rem; font-size:.8125rem; color:var(--gray-500); font-style:italic; }
.copyright-card { border:2px solid var(--primary-500); }
.copyright-card h2 { color:var(--primary-500); }
.warn-box { background:#fef2f2; border-left:4px solid var(--red-500); padding:.75rem 1rem; margin-top:1rem; border-radius:var(--radius-sm); font-size:.8125rem; font-weight:600; color:var(--red-500); }
.legal-footer { background:var(--gray-900); color:#fff; padding:1.5rem; border-radius:var(--radius-lg); text-align:center; }
.legal-footer p { margin:.25rem 0; font-size:.8125rem; }
.warn-footer { color:var(--amber-500); font-weight:700; font-size:.75rem; margin-top:.5rem; }
@media(max-width:600px){ .card-grid{grid-template-columns:1fr;} }
</style>
