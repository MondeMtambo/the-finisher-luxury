<template>
  <div class="upgrade-page">
    <div class="card" style="padding:2rem">
      <h1 style="font-size:1.5rem;font-weight:700;color:var(--gray-900);margin:0 0 .5rem">{{ planCopy.title }}</h1>
      <p style="font-size:.875rem;color:var(--gray-600);margin:0 0 1rem">{{ planCopy.subtitle }}</p>
      <div v-if="planCopy.price" class="price-badge">{{ planCopy.price }}</div>
      <p v-else style="font-size:.8125rem;color:var(--gray-500);font-weight:600">Contact sales for tailored pricing</p>
    </div>

    <div class="card" style="padding:1.5rem">
      <h2 style="font-size:1rem;font-weight:600;color:var(--gray-900);margin:0 0 1rem">What unlocks with {{ planCopy.label }}?</h2>
      <ul class="feature-list">
        <li v-for="feature in planCopy.features" :key="feature">{{ feature }}</li>
      </ul>
      <div class="coming-soon">
        <span class="badge badge-blue" style="margin-bottom:.5rem">Coming Soon</span>
        <p style="font-size:.8125rem;color:var(--gray-600);margin:0">Upgrade flows are finalising. Your workspace will receive the new experience shortly.</p>
      </div>
    </div>

    <div style="display:flex;gap:.75rem;flex-wrap:wrap">
      <button type="button" class="btn btn-primary" @click="contactSales">Contact Sales</button>
      <button type="button" class="btn btn-secondary" @click="goBack">Back to Dashboard</button>
    </div>
  </div>
</template>

<script>
const PLAN_LIBRARY = {
  sport: {
    label: 'SPORT',
    title: 'SPORT Tier Upgrade',
    subtitle: 'Step into the professional lane with team collaboration and performance dashboards.',
    price: 'R99/month',
    features: [
      'Up to 2 workspace users',
      'Advanced performance dashboards',
      'Automated task playbooks',
      'Priority support with 4-hour SLA'
    ]
  },
  luxury: {
    label: 'LUXURY',
    title: 'LUXURY Tier Upgrade',
    subtitle: 'Precision CRM for growth teams that demand analytics depth.',
    price: 'R299/month',
    features: [
      'Up to 10 workspace users',
      'Advanced analytics and KPI scoreboards',
      'API access and third-party integrations',
      'White-glove onboarding sessions'
    ]
  },
  premium: {
    label: 'PREMIUM',
    title: 'PREMIUM Tier Upgrade',
    subtitle: 'Unleash unlimited scale with white-labelling and automation engines.',
    price: 'R499/month',
    features: [
      'Unlimited workspace users',
      'White-label theming and branding',
      'Automation and workflow studio',
      'Dedicated success partner'
    ]
  },
  enterprise: {
    label: 'LEGENDS',
    title: 'LEGENDS Enterprise Edition',
    subtitle: 'Custom revenue architecture for elite programmes and sports-luxury experiences.',
    price: '',
    features: [
      'Unlimited capacity with bespoke infrastructure',
      'Sales point experience design and custom UI builds',
      'On-premise or hybrid deployment options',
      'Embedded analyst squad for campaign execution'
    ]
  }
}

export default {
  name: 'UpgradePage',
  computed: {
    planKey() {
      return (this.$route.params.plan || '').toLowerCase()
    },
    planCopy() {
      return PLAN_LIBRARY[this.planKey] || {
        label: 'THE FINISHER',
        title: 'Upgrade Centre',
        subtitle: 'Select a plan from the dashboard upgrade buttons to see tailored benefits.',
        price: '',
        features: [
          'Unlimited contacts remain free forever',
          'Advanced tiers unlock analytics, automation, and design services',
          'Dedicated enablement engineers on standby'
        ]
      }
    }
  },
  methods: {
    goBack() {
  this.$router.push('/dashboard')
    },
    contactSales() {
      window.location.href = 'mailto:sales@thefinisher.co.za?subject=Upgrade%20Enquiry'
    }
  }
}
</script>
<style scoped>
.upgrade-page { max-width:720px; margin:0 auto; display:flex; flex-direction:column; gap:1.25rem; }
.price-badge { display:inline-block; background:var(--primary-500); color:#fff; padding:.375rem 1rem; border-radius:var(--radius-md); font-weight:700; font-size:.9375rem; }
.feature-list { margin:0; padding-left:1.5rem; display:flex; flex-direction:column; gap:.5rem; font-size:.8125rem; color:var(--gray-700); line-height:1.6; }
.coming-soon { margin-top:1.25rem; background:var(--gray-50); border:1px dashed var(--border-color); border-radius:var(--radius-md); padding:1rem; }
</style>
