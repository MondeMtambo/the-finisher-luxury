<template>
  <div class="systems-page">
    <!-- Hero -->
    <section class="systems-hero">
      <h1>Our Systems</h1>
      <p>Enterprise-grade solutions built to finish strong</p>
    </section>

    <!-- THE FINISHER Showcase -->
    <section class="finisher-showcase">
      <div class="showcase-header">
        <div class="finisher-logo">
          <span class="logo-icon">🏆</span>
          <h2>THE FINISHER</h2>
          <p class="logo-subtitle">SPORT EDITION</p>
        </div>
        <p class="showcase-desc">
          The CRM built for South African champions. Don't just chase leads—finish every relationship strong. 
          Manage contacts, close deals, empower your team—all in one powerful platform.
        </p>
      </div>

      <!-- Pricing Comparison -->
      <div class="pricing-grid">
        <!-- FREE Tier -->
        <div class="pricing-card">
          <div class="tier-badge free">CLASSIC</div>
          <div class="price">
            <span class="currency">R</span>
            <span class="amount">0</span>
          </div>
          <p class="period">Forever Free</p>
          
          <ul class="features-list">
            <li>✅ 1 User</li>
            <li>✅ Unlimited Contacts</li>
            <li>✅ Unlimited Companies</li>
            <li>✅ Unlimited Deals</li>
            <li>✅ Ticket Management</li>
            <li>✅ Basic Reports</li>
            <li>✅ Mobile Responsive</li>
            <li>❌ Advanced Analytics</li>
            <li>❌ API Access</li>
          </ul>

          <a href="https://thefinisher.co.za/register" target="_blank" class="btn-tier">
            Get Started Free
          </a>
        </div>

        <!-- SPORT Tier -->
        <div class="pricing-card featured">
          <div class="featured-badge">🏆 MOST POPULAR</div>
          <div class="tier-badge sport">SPORT</div>
          <div class="price">
            <span class="currency">R</span>
            <span class="amount">99</span>
          </div>
          <p class="period">per month</p>
          
          <ul class="features-list">
            <li>✅ 2 Users</li>
            <li>✅ Everything in CLASSIC</li>
            <li>✅ Company Auto-Create</li>
            <li>✅ Advanced Reporting</li>
            <li>✅ Performance Analytics</li>
            <li>✅ Priority Support</li>
            <li>✅ Role-Based Access</li>
            <li>✅ Notifications System</li>
            <li>❌ API Access</li>
          </ul>

          <a href="https://thefinisher.co.za/register" target="_blank" class="btn-tier primary">
            Start Now
          </a>
        </div>

        <!-- LUXURY Tier -->
        <div class="pricing-card">
          <div class="tier-badge luxury">LUXURY</div>
          <div class="price">
            <span class="currency">R</span>
            <span class="amount">249</span>
          </div>
          <p class="period">per month</p>
          
          <ul class="features-list">
            <li>✅ 10 Users</li>
            <li>✅ Everything in SPORT</li>
            <li>✅ API Access</li>
            <li>✅ Custom Integrations</li>
            <li>✅ Dedicated Support</li>
            <li>✅ Training Sessions</li>
            <li>✅ Advanced Permissions</li>
            <li>✅ Data Export</li>
            <li>✅ Webhooks</li>
          </ul>

          <a href="https://thefinisher.co.za/register" target="_blank" class="btn-tier">
            Get Started
          </a>
        </div>

        <!-- PREMIUM Tier -->
        <div class="pricing-card">
          <div class="tier-badge premium">PREMIUM</div>
          <div class="price">
            <span class="currency">R</span>
            <span class="amount">499</span>
          </div>
          <p class="period">per month</p>
          
          <ul class="features-list">
            <li>✅ Unlimited Users</li>
            <li>✅ Everything in LUXURY</li>
            <li>✅ White-Label Option</li>
            <li>✅ Custom Development</li>
            <li>✅ SLA Guarantee</li>
            <li>✅ Dedicated Account Manager</li>
            <li>✅ On-Site Training</li>
            <li>✅ Priority Features</li>
            <li>✅ Custom Integrations</li>
          </ul>

          <a href="https://thefinisher.co.za/register" target="_blank" class="btn-tier">
            Contact Sales
          </a>
        </div>
      </div>

      <!-- Features Grid -->
      <div class="features-grid">
        <h3>Key Features</h3>
        <div class="features-showcase">
          <div class="feature-item">
            <div class="feature-icon">📇</div>
            <h4>Smart Contact Management</h4>
            <p>Auto-create companies from email domains. Track unlimited contacts with self-employed handling.</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🎯</div>
            <h4>Deal Pipeline Tracking</h4>
            <p>Visualize your sales pipeline. Track time spent on deals. Never miss a follow-up.</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🎟️</div>
            <h4>Ticketing System</h4>
            <p>Internal ticket management. Assign, track, and resolve with priority levels.</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📊</div>
            <h4>Performance Analytics</h4>
            <p>Real-time dashboards. Admin oversight with detailed metrics. Know who's crushing it.</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">👥</div>
            <h4>Role-Based Access</h4>
            <p>Company admins, employees, system staff. Everyone sees exactly what they need.</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🔔</div>
            <h4>Smart Notifications</h4>
            <p>Stay in the loop with scoped notifications. Never miss an important update.</p>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="finisher-cta">
        <h2>Ready to Finish Strong?</h2>
        <p>Join South African businesses closing more deals with THE FINISHER</p>
        <div class="cta-buttons">
          <a href="https://thefinisher.co.za" target="_blank" class="btn-launch">
            Launch THE FINISHER →
          </a>
          <button class="btn-demo" @click="$router.push('/contact')">
            Request Demo
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'SystemsPage'
}
</script>

<style scoped>
.systems-page {
  min-height: 100vh;
  background: #f8fafc;
}

.systems-hero {
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 100%);
  color: white;
  padding: 6rem 2rem 4rem;
  text-align: center;
}

.systems-hero h1 {
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.systems-hero p {
  font-size: 1.5rem;
  color: #cbd5e1;
}

/* Showcase */
.finisher-showcase {
  max-width: 1400px;
  margin: -2rem auto 4rem;
  padding: 0 2rem;
}

.showcase-header {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-bottom: 4rem;
}

.finisher-logo {
  margin-bottom: 2rem;
}

.logo-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.finisher-logo h2 {
  font-size: 3rem;
  font-weight: 900;
  color: #0a1628;
  margin-bottom: 0.5rem;
}

.logo-subtitle {
  font-size: 1rem;
  color: #FFD700;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.showcase-desc {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #475569;
  max-width: 800px;
  margin: 0 auto;
}

/* Pricing Grid */
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.pricing-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
}

.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border-color: #FFD700;
}

.pricing-card.featured {
  border: 3px solid #FFD700;
  box-shadow: 0 20px 60px rgba(255, 215, 0, 0.2);
  transform: scale(1.05);
}

.featured-badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #0a1628;
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  font-weight: 800;
  font-size: 0.85rem;
  letter-spacing: 1px;
}

.tier-badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  font-weight: 800;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  letter-spacing: 1px;
}

.tier-badge.free {
  background: #e2e8f0;
  color: #475569;
}

.tier-badge.sport {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #0a1628;
}

.tier-badge.luxury {
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: white;
}

.tier-badge.premium {
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 100%);
  color: #FFD700;
  border: 2px solid #FFD700;
}

.price {
  margin: 2rem 0 0.5rem;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.currency {
  font-size: 2rem;
  font-weight: 700;
  color: #64748b;
  margin-right: 0.25rem;
  margin-top: 0.75rem;
}

.amount {
  font-size: 4rem;
  font-weight: 900;
  color: #0a1628;
}

.period {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 2rem;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 2rem 0;
  text-align: left;
}

.features-list li {
  padding: 0.75rem 0;
  color: #475569;
  font-size: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.btn-tier {
  display: block;
  width: 100%;
  padding: 1rem;
  border: 2px solid #0a1628;
  background: white;
  color: #0a1628;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  text-align: center;
}

.btn-tier:hover {
  background: #0a1628;
  color: white;
}

.btn-tier.primary {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  border: none;
  color: #0a1628;
}

.btn-tier.primary:hover {
  background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
  transform: scale(1.02);
}

/* Features Grid */
.features-grid {
  background: white;
  padding: 4rem 3rem;
  border-radius: 20px;
  margin-bottom: 4rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.features-grid h3 {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0a1628;
  text-align: center;
  margin-bottom: 3rem;
}

.features-showcase {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2.5rem;
}

.feature-item {
  text-align: center;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-item h4 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #0a1628;
  margin-bottom: 0.75rem;
}

.feature-item p {
  color: #64748b;
  line-height: 1.6;
}

/* CTA */
.finisher-cta {
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 100%);
  padding: 4rem 3rem;
  border-radius: 20px;
  text-align: center;
  color: white;
}

.finisher-cta h2 {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 1rem;
}

.finisher-cta p {
  font-size: 1.3rem;
  color: #cbd5e1;
  margin-bottom: 2.5rem;
}

.cta-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-launch,
.btn-demo {
  padding: 1.25rem 3rem;
  font-size: 1.1rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-launch {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #0a1628;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-launch:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(255, 215, 0, 0.4);
}

.btn-demo {
  background: transparent;
  color: #FFD700;
  border: 2px solid #FFD700;
}

.btn-demo:hover {
  background: rgba(255, 215, 0, 0.1);
}

@media (max-width: 968px) {
  .systems-hero h1 {
    font-size: 2.5rem;
  }

  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .pricing-card.featured {
    transform: scale(1);
  }

  .features-showcase {
    grid-template-columns: 1fr;
  }

  .cta-buttons {
    flex-direction: column;
  }
}
</style>
