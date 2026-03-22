<template>
  <transition name="modal">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="terms-modal" ref="modalShell" tabindex="-1">
        <div class="tm-header">
          <h2>Terms &amp; Conditions</h2>
          <button class="modal-close" @click="$emit('close')">&times;</button>
        </div>
        <div class="tm-body" @scroll="handleScroll" ref="scrollContainer">
          <div class="terms-content">
            <section><h3>1. Acceptance of Terms</h3><p>By accessing and using THE FINISHER FREE CRM platform ("Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.</p></section>
            <section><h3>2. Use License</h3><p>Permission is granted to temporarily access the Service for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:</p><ul><li>Modify or copy the materials;</li><li>Use the materials for any commercial purpose or for any public display;</li><li>Attempt to reverse engineer any software contained on THE FINISHER's platform;</li><li>Remove any copyright or other proprietary notations from the materials;</li><li>Transfer the materials to another person or "mirror" the materials on any other server.</li></ul></section>
            <section><h3>3. User Account and Data</h3><p>You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to:</p><ul><li>Provide accurate, current, and complete information during registration;</li><li>Maintain and promptly update your account information;</li><li>Keep your password secure and confidential;</li><li>Notify us immediately of any unauthorized use of your account;</li><li>Be responsible for all activities conducted through your account.</li></ul></section>
            <section><h3>4. Privacy, Data Protection & POPIA Compliance</h3><p>We are committed to protecting your privacy in full compliance with the South African Protection of Personal Information Act (POPIA). Your personal information and CRM data are stored securely and will never be shared with third parties without your explicit consent, except as required by law. We implement industry-standard security measures including:</p><ul><li>Encrypted data transmission (HTTPS/TLS);</li><li>Secure password hashing;</li><li>Regular security audits;</li><li>Access controls and authentication;</li><li>Data backup and recovery procedures.</li></ul></section>
            <section><h3>5. Service Plans and Billing</h3><p>THE FINISHER offers multiple service tiers designed to be the most affordable CRM in the world:</p><ul><li><strong>CLASSIC (Free):</strong> Provides unlimited contacts and basic CRM features at no cost forever.</li><li><strong>SPORT (R99/month):</strong> Includes 3 users, email integration, advanced reporting, and priority support.</li><li><strong>LUXURY (R249/month):</strong> Includes 10 users, API access, custom integrations, and advanced analytics.</li><li><strong>PREMIUM (R499/month):</strong> Unlimited users, white-label options, dedicated support, and custom development.</li></ul><p>Paid subscriptions automatically renew unless cancelled at least 24 hours before the renewal date. Refunds are available within 14 days of initial purchase only.</p></section>
            <section><h3>6. Acceptable Use Policy</h3><p>You agree not to use the Service to:</p><ul><li>Violate any laws or regulations;</li><li>Infringe on intellectual property rights;</li><li>Transmit harmful code, viruses, or malware;</li><li>Engage in spamming or unsolicited communications;</li><li>Harass, abuse, or harm other users;</li><li>Attempt to gain unauthorized access to our systems;</li><li>Use automated systems to scrape or collect data.</li></ul></section>
            <section><h3>7. Intellectual Property</h3><p>All content, features, and functionality of the Service, including but not limited to text, graphics, logos, icons, images, audio clips, and software, are the exclusive property of THE FINISHER and are protected by copyright, trademark, and other intellectual property laws.</p></section>
            <section><h3>8. Limitation of Liability</h3><p>THE FINISHER and its affiliates shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use or inability to use the Service.</p><p>In no event shall our total liability exceed the amount paid by you, if any, for accessing the Service during the twelve (12) months prior to the claim.</p></section>
            <section><h3>9. Service Modifications and Termination</h3><p>We reserve the right to:</p><ul><li>Modify, suspend, or discontinue any aspect of the Service at any time;</li><li>Change these Terms &amp; Conditions with notice to users;</li><li>Terminate or suspend accounts that violate these terms;</li><li>Refuse service to anyone for any reason.</li></ul></section>
            <section><h3>10. Disclaimer of Warranties</h3><p>The Service is provided "as is" and "as available" without warranties of any kind, either express or implied, including but not limited to implied warranties of merchantability, fitness for a particular purpose, or non-infringement.</p></section>
            <section><h3>11. Governing Law</h3><p>These Terms &amp; Conditions are governed by and construed in accordance with the laws of the jurisdiction in which THE FINISHER operates.</p></section>
            <section><h3>12. Contact Information</h3><p>If you have any questions about these Terms &amp; Conditions or our POPIA compliance, please contact us at:<br><strong>Email:</strong> thefinishercrm@gmail.com<br><strong>Address:</strong> THE FINISHER CRM Solutions<br><strong>Last Updated:</strong> {{ new Date().toLocaleDateString() }}</p></section>
            <div class="scroll-ind" v-if="!scrolledToBottom"><p>Please scroll down to read all terms</p></div>
          </div>
        </div>
        <div class="tm-footer">
          <button class="btn btn-primary" style="width:100%" :disabled="!scrolledToBottom" @click="handleAccept">
            {{ scrolledToBottom ? 'I Accept the Terms & Conditions' : 'Please Read All Terms First' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'TermsModal',
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      scrolledToBottom: false
    }
  },
  methods: {
    handleScroll() {
      const container = this.$refs.scrollContainer
      if (!container) return

      const scrollTop = container.scrollTop
      const scrollHeight = container.scrollHeight
      const clientHeight = container.clientHeight
      
      
      this.scrolledToBottom = (scrollTop + clientHeight >= scrollHeight - 50)
    },
    handleAccept() {
      if (this.scrolledToBottom) {
        this.$emit('accept')
        this.$emit('close')
      }
    }
  },
  watch: {
    show(newVal) {
      if (!newVal) {
        this.scrolledToBottom = false
        return
      }

      this.scrolledToBottom = false
      this.$nextTick(() => {
        const container = this.$refs.scrollContainer
        if (container) {
          container.scrollTop = 0
        }
        const shell = this.$refs.modalShell
        if (shell && typeof shell.focus === 'function') {
          shell.focus()
        }
      })
    }
  }
}
</script>
<style scoped>
.modal-overlay { position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.8);backdrop-filter:blur(10px);display:flex;align-items:center;justify-content:center;z-index:9999;padding:1rem; }
.terms-modal { background:linear-gradient(135deg, rgba(15,15,15,0.95) 0%, rgba(5,5,5,0.95) 100%);border:1px solid rgba(212, 175, 55, 0.3);border-radius:var(--radius-lg);max-width:680px;width:100%;max-height:90vh;display:flex;flex-direction:column;box-shadow:0 30px 60px rgba(0, 0, 0, 0.9), inset 0 0 0 1px rgba(255, 255, 255, 0.05); }
.tm-header { display:flex;justify-content:space-between;align-items:center;padding:1.25rem 1.5rem;border-bottom:1px solid rgba(212, 175, 55, 0.2); }
.tm-header h2 { font-size:1.125rem;font-weight:700;color:#fff;margin:0; letter-spacing:1px; }
.modal-close { background:none;border:none;font-size:1.5rem;color:#9ca3af;cursor:pointer;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius-sm); transition:all 0.3s; }
.modal-close:hover { background:rgba(212, 175, 55, 0.1);color:#D4AF37; }
.tm-body { flex:1;overflow-y:auto;padding:1.5rem; }
.terms-content section { margin-bottom:1.5rem; }
.terms-content h3 { font-size:.875rem; font-weight:600; color:#D4AF37; margin:0 0 .5rem; text-transform:uppercase; letter-spacing:1px; }
.terms-content p { font-size:.8125rem; color:#d1d5db; line-height:1.6; margin:0 0 .5rem; }
.terms-content ul { margin:.25rem 0 .5rem; padding-left:1.25rem; font-size:.8125rem; color:#d1d5db; line-height:1.7; }
.terms-content li { margin:.25rem 0; }
.scroll-ind { position:sticky;bottom:0;background:rgba(212, 175, 55, 0.05);backdrop-filter:blur(10px);border:1px solid rgba(212, 175, 55, 0.2);padding:.75rem;text-align:center;border-radius:var(--radius-md);margin-top:.75rem; }
.scroll-ind p { margin:0;font-size:.8125rem;font-weight:600;color:#D4AF37;animation:pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.6} }
.tm-footer { padding:1rem 1.5rem;border-top:1px solid rgba(212, 175, 55, 0.2); }
.modal-enter-active,.modal-leave-active { transition:opacity .3s; }
.modal-enter-from,.modal-leave-to { opacity:0; }
</style>
