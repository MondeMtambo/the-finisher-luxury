<template>
  <div class="help-page">
    <div class="page-header">
      <div>
        <h1>Help &amp; Enablement</h1>
        <p class="page-subtitle">Everything you need to master THE FINISHER — from first contact capture to winning the deal.</p>
      </div>
    </div>

    <div class="card" style="padding:1.5rem">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
        <div>
          <h2 style="font-size:1rem;font-weight:600;color:var(--gray-900);margin:0">Guided Tutorial</h2>
          <p style="font-size:.8125rem;color:var(--gray-500);margin:.25rem 0 0">Interactive walkthrough of the CRM workflow</p>
        </div>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap">
          <button type="button" @click="launchTutorial" class="btn btn-primary">Launch Tutorial</button>
          <button type="button" @click="skipTutorial" class="btn btn-secondary">Skip Tutorial</button>
        </div>
      </div>
      <p v-if="tutorialStatus === 'completed'" style="margin:.75rem 0 0;font-size:.8125rem;color:var(--green-500)">Tutorial marked as completed. You can relaunch anytime.</p>
      <p v-else-if="tutorialStatus === 'skipped'" style="margin:.75rem 0 0;font-size:.8125rem;color:var(--gray-500)">Tutorial will stay hidden until you relaunch it.</p>
    </div>

    <div class="card" style="padding:1.5rem">
      <h2 style="font-size:1rem;font-weight:600;color:var(--gray-900);margin:0 0 1rem">Guided Walkthrough</h2>
      <ol class="walk-list">
        <li><strong>Register a client tenant:</strong> Complete the registration form and confirm the welcome email.</li>
        <li><strong>Capture a contact:</strong> In Contacts, record the client champion and manually capture their company name.</li>
        <li><strong>Create the company profile:</strong> Once a contact exists, formalise the company record with full business details.</li>
        <li><strong>Link contact to company:</strong> Edit the contact and assign the newly created company.</li>
        <li><strong>Build the first deal:</strong> With contacts and companies ready, log the opportunity, stage, and value.</li>
      </ol>
      <p style="font-size:.8125rem;color:var(--primary-500);font-weight:600;margin:.75rem 0 0">Tip: The tutorial will highlight each screen and you can hit Skip All anytime.</p>
    </div>

    <div class="card" style="padding:1.5rem">
      <h2 style="font-size:1rem;font-weight:600;color:var(--gray-900);margin:0 0 1rem">Frequently Asked Questions</h2>
      <div v-for="question in faqs" :key="question.q" class="faq-item">
        <h3>{{ question.q }}</h3>
        <p v-for="(line, idx) in question.a" :key="idx">{{ line }}</p>
      </div>
    </div>

    <div class="card" style="padding:1.5rem">
      <h2 style="font-size:1rem;font-weight:600;color:var(--gray-900);margin:0 0 .25rem">Contact Support</h2>
      <p style="font-size:.8125rem;color:var(--gray-500);margin:0 0 1.25rem">Need help? Our dedicated support team is here to assist you.</p>
      <div class="support-grid">
        <div class="sc" v-for="s in supportCards" :key="s.title">
          <div class="sc-icon" :class="s.color"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path :d="s.icon"/></svg></div>
          <h3>{{ s.title }}</h3>
          <p>{{ s.desc }}</p>
          <a :href="s.href" class="btn btn-sm btn-secondary">{{ s.linkText }}</a>
        </div>
      </div>
      <div class="support-footer">
        <p><strong>THE FINISHER LUXURY CRM</strong></p>
        <p style="color:var(--gray-500);font-size:.8125rem">2026 MTAMBO HOLDINGS - Premium Luxury Edition</p>
        <p style="color:var(--gray-500);font-size:.75rem;margin-top:.25rem">Average response time: 24-48 hours</p>
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
      faqs: [
        {
          q: 'How do I create a contact?',
          a: [
            'Navigate to Contacts and click "Add Contact".',
            'Capture first name, last name, email, phone, and the company name manually.',
            'Optionally assign the contact to a company once it exists.'
          ]
        },
        {
          q: 'Why can’t I open Companies first?',
          a: [
            'THE FINISHER enforces data discipline — capture at least one contact before formalising a company.',
            'This ensures every company record has a human counterpart for support and password recovery.'
          ]
        },
        {
          q: 'How do I log a deal?',
          a: [
            'Create or link a contact to a company.',
            'Open Deals, choose the company, then the linked contact, add value and stage, and save.'
          ]
        },
        {
          q: 'Can I revisit the tutorial?',
          a: [
            'Yes. Use the "Launch Guided Tutorial" button above. The tutorial can be replayed anytime.'
          ]
        }
      ],
      tutorialStatus: localStorage.getItem(TUTORIAL_KEY) || 'pending',
      supportCards: [
        { title: 'Email Support', desc: 'Get detailed help via email', href: 'mailto:support@thefinishersport.co.za', linkText: 'Email Us', icon: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z M22 6l-10 7L2 6', color: 'blue' },
        { title: 'Legal & Licensing', desc: 'Legal inquiries and licensing', href: 'mailto:legal@mtamboholdings.co.za', linkText: 'Contact Legal', icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', color: 'gray' },
        { title: 'Enablement Desk', desc: 'Custom dashboards & integrations', href: 'mailto:support@thefinisher.co.za', linkText: 'Get Help', icon: 'M22 10v6M2 10l10-5 10 5-10 5z M6 12v5c6 3 12 0 12 0v-5', color: 'green' },
        { title: 'Report a Bug', desc: 'Found an issue? Let us know!', href: 'mailto:support@thefinishersport.co.za?subject=Bug Report', linkText: 'Report Bug', icon: 'M8 2v4 M16 2v4 M3 10h18 M12 14v4 M8 14l-2 4 M16 14l2 4', color: 'red' }
      ]
    }
  },
  methods: {
    launchTutorial() {
      localStorage.setItem(TUTORIAL_KEY, 'completed')
      this.tutorialStatus = 'completed'
      this.$emit('launch-tutorial')
      toast.success('Tutorial Launched', 'Tutorial will start from the dashboard. Return to the dashboard to follow the guided steps.')
    },
    skipTutorial() {
      localStorage.setItem(TUTORIAL_KEY, 'skipped')
      this.tutorialStatus = 'skipped'
      toast.info('Tutorial Skipped', 'You can relaunch it anytime from this Help Centre.')
    }
  }
}
</script>
<style scoped>
.help-page { max-width:900px; margin:0 auto; display:flex; flex-direction:column; gap:1.25rem; }
.walk-list { margin:0; padding-left:1.5rem; display:flex; flex-direction:column; gap:.75rem; font-size:.8125rem; color:var(--gray-700); line-height:1.6; }
.walk-list strong { color:var(--gray-900); }
.faq-item + .faq-item { margin-top:1rem; border-top:1px solid var(--gray-100); padding-top:1rem; }
.faq-item h3 { font-size:.875rem; font-weight:600; color:var(--gray-900); margin:0 0 .375rem; }
.faq-item p { font-size:.8125rem; color:var(--gray-600); margin:.125rem 0; line-height:1.5; }
.support-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1rem; margin-bottom:1.5rem; }
.sc { background:var(--gray-50); border:1px solid var(--border-color); border-radius:var(--radius-md); padding:1.25rem; text-align:center; transition:border-color .2s; }
.sc:hover { border-color:var(--primary-500); }
.sc-icon { width:40px; height:40px; border-radius:var(--radius-md); display:flex; align-items:center; justify-content:center; margin:0 auto .75rem; }
.sc-icon.blue { background:#eff6ff; color:var(--primary-500); }
.sc-icon.gray { background:var(--gray-100); color:var(--gray-600); }
.sc-icon.green { background:#ecfdf5; color:var(--green-500); }
.sc-icon.red { background:#fef2f2; color:var(--red-500); }
.sc h3 { font-size:.875rem; font-weight:600; color:var(--gray-900); margin:0 0 .25rem; }
.sc p { font-size:.75rem; color:var(--gray-500); margin:0 0 .75rem; }
.support-footer { border-top:1px solid var(--border-color); padding-top:1rem; text-align:center; }
.support-footer p { margin:.25rem 0; }
@media(max-width:600px){ .support-grid{grid-template-columns:1fr;} }
</style>
