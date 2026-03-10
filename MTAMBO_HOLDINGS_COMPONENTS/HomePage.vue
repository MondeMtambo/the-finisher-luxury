<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="clan-badge">
          <span class="badge-text">Nhlangothi • Gomazane • Vezi • Masilela</span>
        </div>
        <h1 class="hero-title">
          We Don't Just Build<br/>
          <span class="highlight">We Finish</span>
        </h1>
        <p class="hero-subtitle">
          Like the steadfast Gomazane and the vigilant Vezi, Mtambo Holdings delivers cutting-edge digital solutions before the need becomes urgent. We finish what others start, and we start what others fear to finish.
        </p>
        <div class="hero-stats">
          <div class="stat">
            <div class="stat-number">5+</div>
            <div class="stat-label">Years Experience</div>
          </div>
          <div class="stat">
            <div class="stat-number">50+</div>
            <div class="stat-label">Projects Completed</div>
          </div>
          <div class="stat">
            <div class="stat-number">100%</div>
            <div class="stat-label">Client Satisfaction</div>
          </div>
        </div>
        <div class="hero-cta">
          <button class="btn-primary" @click="$router.push('/services')">Explore Services</button>
          <button class="btn-secondary" @click="$router.push('/systems')">View Systems</button>
        </div>
      </div>
      <div class="hero-image">
        <div class="floating-card card-1">
          <div class="card-icon">💻</div>
          <div class="card-text">Web Development</div>
        </div>
        <div class="floating-card card-2">
          <div class="card-icon">🎨</div>
          <div class="card-text">Graphic Design</div>
        </div>
        <div class="floating-card card-3">
          <div class="card-icon">⚙️</div>
          <div class="card-text">Systems Engineering</div>
        </div>
        <div class="floating-card card-4">
          <div class="card-icon">🏆</div>
          <div class="card-text">THE FINISHER CRM</div>
        </div>
      </div>
    </section>

    <!-- Vision Section -->
    <section class="vision-section">
      <div class="vision-content">
        <h2 class="section-title">Our Vision</h2>
        <div class="vision-text">
          <span class="vision-quote">"Getting It Done Before Someone Else Does"</span>
          <p>
            We are the Nhlangothi—the spear that cuts through complexity. The Masilela—those who don't disappear when challenges arise. 
            With the agility of Nyong'eluhlaza and the leadership of Jiyane, we transform visions into finished realities.
          </p>
        </div>
      </div>
    </section>

    <!-- Services Preview -->
    <section class="services-preview">
      <h2 class="section-title">What We Do</h2>
      <div class="services-grid">
        <div class="service-card">
          <div class="service-icon">🎨</div>
          <h3>Graphic Design</h3>
          <p>Stunning visuals that capture your brand's essence</p>
        </div>
        <div class="service-card">
          <div class="service-icon">💻</div>
          <h3>Web Development</h3>
          <p>Modern, responsive websites built with cutting-edge tech</p>
        </div>
        <div class="service-card">
          <div class="service-icon">⚙️</div>
          <h3>Systems Engineering</h3>
          <p>C++, JavaScript, Python—we speak every language</p>
        </div>
        <div class="service-card highlight-card">
          <div class="service-icon">🏆</div>
          <h3>THE FINISHER CRM</h3>
          <p>Our flagship product for sales & customer management</p>
          <button class="card-btn" @click="$router.push('/systems')">Learn More</button>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <h2>Ready to Finish Strong?</h2>
      <p>Let's build something extraordinary together</p>
      <button class="btn-primary large" @click="$router.push('/contact')">Get In Touch</button>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  min-height: 90vh;
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 50%, #0a1628 100%);
  color: white;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 4rem 6rem;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.clan-badge {
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  display: inline-block;
  margin-bottom: 2rem;
}

.badge-text {
  color: #FFD700;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 1px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: #f8fafc;
}

.highlight {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #cbd5e1;
  margin-bottom: 2rem;
  max-width: 600px;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  margin: 3rem 0;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: #FFD700;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hero-cta {
  display: flex;
  gap: 1.5rem;
  margin-top: 2rem;
}

.btn-primary {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #0a1628;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(255, 215, 0, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(255, 215, 0, 0.6);
}

.btn-secondary {
  background: transparent;
  color: #FFD700;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  border: 2px solid #FFD700;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateY(-3px);
}

/* Floating Cards */
.hero-image {
  position: relative;
  height: 600px;
}

.floating-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 215, 0, 0.3);
  padding: 1.5rem 2rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: float 6s ease-in-out infinite;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.card-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 40%;
  right: 10%;
  animation-delay: 1.5s;
}

.card-3 {
  bottom: 30%;
  left: 5%;
  animation-delay: 3s;
}

.card-4 {
  bottom: 10%;
  right: 15%;
  animation-delay: 4.5s;
  background: rgba(255, 215, 0, 0.1);
  border: 2px solid #FFD700;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.card-icon {
  font-size: 2rem;
}

.card-text {
  font-weight: 600;
  color: #e2e8f0;
  font-size: 1rem;
}

/* Vision Section */
.vision-section {
  padding: 6rem 6rem;
  background: #f8fafc;
  text-align: center;
}

.section-title {
  font-size: 3rem;
  font-weight: 900;
  color: #0a1628;
  margin-bottom: 2rem;
}

.vision-content {
  max-width: 900px;
  margin: 0 auto;
}

.vision-quote {
  font-size: 2rem;
  font-weight: 700;
  color: #FFD700;
  font-style: italic;
  display: block;
  margin-bottom: 2rem;
}

.vision-text p {
  font-size: 1.2rem;
  line-height: 1.9;
  color: #475569;
}

/* Services Preview */
.services-preview {
  padding: 6rem 6rem;
  background: white;
  text-align: center;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.service-card {
  background: #f8fafc;
  padding: 2.5rem;
  border-radius: 20px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.service-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: #FFD700;
}

.service-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.service-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0a1628;
  margin-bottom: 1rem;
}

.service-card p {
  color: #64748b;
  line-height: 1.6;
}

.highlight-card {
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 100%);
  border: 2px solid #FFD700;
}

.highlight-card h3,
.highlight-card p {
  color: white;
}

.card-btn {
  margin-top: 1.5rem;
  background: #FFD700;
  color: #0a1628;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-btn:hover {
  background: #FFA500;
  transform: scale(1.05);
}

/* CTA Section */
.cta-section {
  padding: 6rem 6rem;
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 100%);
  text-align: center;
  color: white;
}

.cta-section h2 {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 1rem;
}

.cta-section p {
  font-size: 1.3rem;
  color: #cbd5e1;
  margin-bottom: 2.5rem;
}

.btn-primary.large {
  font-size: 1.3rem;
  padding: 1.25rem 3rem;
}

/* Responsive */
@media (max-width: 968px) {
  .hero {
    grid-template-columns: 1fr;
    padding: 3rem 2rem;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    margin: 0 auto 2rem;
  }

  .hero-stats {
    justify-content: center;
    flex-wrap: wrap;
    gap: 2rem;
  }

  .hero-cta {
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero-image {
    display: none;
  }

  .services-preview,
  .vision-section,
  .cta-section {
    padding: 4rem 2rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .services-grid {
    grid-template-columns: 1fr;
  }
}
</style>
