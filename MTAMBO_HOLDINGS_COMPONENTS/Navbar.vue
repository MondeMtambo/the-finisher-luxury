<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand" @click="$router.push('/')">
        <span class="brand-icon">🏢</span>
        <div class="brand-text">
          <h1>MTAMBO HOLDINGS</h1>
          <p class="tagline">Getting It Done Before Someone Else Does</p>
        </div>
      </div>
      
      <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
        <span>☰</span>
      </button>

      <div class="nav-links" :class="{ 'mobile-open': mobileMenuOpen }">
        <router-link to="/" @click="mobileMenuOpen = false">Home</router-link>
        <router-link to="/about" @click="mobileMenuOpen = false">About Us</router-link>
        <router-link to="/services" @click="mobileMenuOpen = false">Services</router-link>
        <router-link to="/systems" @click="mobileMenuOpen = false">Systems</router-link>
        <router-link to="/careers" @click="mobileMenuOpen = false">Careers</router-link>
        <router-link to="/contact" @click="mobileMenuOpen = false">Contact</router-link>
        <a href="https://thefinisher.co.za" target="_blank" class="cta-link">Launch THE FINISHER</a>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      mobileMenuOpen: false
    }
  }
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #0a1628 0%, #1a2942 100%);
  color: white;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border-bottom: 3px solid #FFD700;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.nav-brand:hover {
  transform: scale(1.02);
}

.brand-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 4px 8px rgba(255, 215, 0, 0.4));
}

.brand-text h1 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #FFD700;
  letter-spacing: 1px;
  margin: 0;
  line-height: 1;
}

.tagline {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0.25rem 0 0 0;
  font-style: italic;
  letter-spacing: 0.5px;
}

.mobile-toggle {
  display: none;
  background: none;
  border: 2px solid #FFD700;
  color: #FFD700;
  font-size: 1.8rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.mobile-toggle:hover {
  background: rgba(255, 215, 0, 0.1);
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  color: #e2e8f0;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  position: relative;
}

.nav-links a:hover {
  color: #FFD700;
  background: rgba(255, 215, 0, 0.1);
}

.nav-links a.router-link-active {
  color: #FFD700;
  background: rgba(255, 215, 0, 0.15);
}

.cta-link {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #0a1628 !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: 25px;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
  border: none;
}

.cta-link:hover {
  background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
}

@media (max-width: 968px) {
  .mobile-toggle {
    display: block;
  }

  .nav-links {
    position: fixed;
    top: 80px;
    right: -100%;
    width: 300px;
    height: calc(100vh - 80px);
    background: linear-gradient(180deg, #0a1628 0%, #1a2942 100%);
    flex-direction: column;
    padding: 2rem;
    gap: 1rem;
    transition: right 0.4s ease;
    box-shadow: -4px 0 20px rgba(0, 0, 0, 0.5);
    border-left: 3px solid #FFD700;
  }

  .nav-links.mobile-open {
    right: 0;
  }

  .nav-links a {
    width: 100%;
    text-align: center;
    padding: 1rem;
    font-size: 1.1rem;
  }

  .cta-link {
    width: 100%;
  }

  .brand-text h1 {
    font-size: 1.2rem;
  }

  .tagline {
    font-size: 0.65rem;
  }
}

@media (max-width: 600px) {
  .nav-container {
    padding: 0.75rem 1rem;
  }

  .brand-icon {
    font-size: 2rem;
  }

  .brand-text h1 {
    font-size: 1rem;
  }

  .tagline {
    display: none;
  }
}
</style>
