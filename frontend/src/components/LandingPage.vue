<template>
  <div class="landing-page" @mousemove="handleMouseMove" ref="container">
    <nav class="exclusive-nav">
      <div class="nav-brand">THE FINISHER</div>
      <div class="nav-links">
        <button class="nav-btn" @click="$router.push('/login')">Member Login</button>
      </div>
    </nav>

    <div class="center-stage">
      <div class="card-container">
        <div class="black-card" :style="cardStyle">
          <div class="card-glare" :style="glareStyle"></div>
          <div class="card-content">
            <div class="card-logo">F</div>
            <div class="card-title">THE FINISHER</div>
            <div class="card-subtitle">LUXURY EDITION</div>
          </div>
        </div>
      </div>
      
      <h1 class="headline">Your Pipeline. Elevated.</h1>
      <p class="subheadline">The most exclusive CRM engine built for generational wealth.</p>
      
      <button class="request-btn" @click="$router.push('/register')">Request Access</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      mouseX: 0,
      mouseY: 0,
      containerWidth: 0,
      containerHeight: 0,
    }
  },
  computed: {
    cardStyle() {
      if (this.containerWidth === 0) return {}
      const centerX = this.containerWidth / 2
      const centerY = this.containerHeight / 2
      const rotateY = ((this.mouseX - centerX) / centerX) * 15
      const rotateX = -((this.mouseY - centerY) / centerY) * 15
      return {
        transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
      }
    },
    glareStyle() {
      if (this.containerWidth === 0) return { opacity: 0 }
      const percentX = (this.mouseX / this.containerWidth) * 100
      const percentY = (this.mouseY / this.containerHeight) * 100
      return {
        background: `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(212, 175, 55, 0.4) 0%, transparent 60%)`,
        opacity: 1
      }
    }
  },
  mounted() {
    this.updateDimensions()
    window.addEventListener('resize', this.updateDimensions)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateDimensions)
  },
  methods: {
    updateDimensions() {
      if (this.$refs.container) {
        this.containerWidth = this.$refs.container.offsetWidth
        this.containerHeight = this.$refs.container.offsetHeight
        this.mouseX = this.containerWidth / 2
        this.mouseY = this.containerHeight / 2
      }
    },
    handleMouseMove(e) {
      requestAnimationFrame(() => {
        this.mouseX = e.clientX
        this.mouseY = e.clientY
      })
    }
  }
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}

.exclusive-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 4rem;
  position: relative;
  z-index: 10;
}

.nav-brand {
  font-size: 0.875rem;
  font-weight: 800;
  letter-spacing: 4px;
  color: #D4AF37;
}

.nav-btn {
  background: transparent;
  border: none;
  color: #9ca3af;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-btn:hover {
  color: #D4AF37;
}

.center-stage {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 10;
  padding: 2rem;
}

.card-container {
  perspective: 1000px;
  margin-bottom: 4rem;
}

.black-card {
  width: 340px;
  height: 215px;
  background: linear-gradient(135deg, #111418 0%, #000000 100%);
  border-radius: 16px;
  border: 1px solid rgba(212, 175, 55, 0.3);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.9), inset 0 0 0 1px rgba(255, 255, 255, 0.05);
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-glare {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none;
  z-index: 2;
  mix-blend-mode: screen;
  transition: opacity 0.3s;
}

.card-content {
  position: relative;
  z-index: 3;
  text-align: center;
  transform: translateZ(30px);
}

.card-logo {
  font-size: 3.5rem;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1px rgba(212, 175, 55, 0.8);
  margin-bottom: 1rem;
  line-height: 1;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: 6px;
  color: #D4AF37;
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 4px;
  color: #6b7280;
}

.headline {
  font-size: 4.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 1rem;
  background: linear-gradient(to right, #ffffff, #9ca3af);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
  text-align: center;
}

.subheadline {
  font-size: 1.25rem;
  color: #6b7280;
  margin: 0 0 3rem;
  text-align: center;
  max-width: 600px;
}

.request-btn {
  background: rgba(15, 15, 15, 0.6);
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: #D4AF37;
  padding: 1rem 3rem;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 3px;
  border-radius: 4px;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.request-btn:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: #D4AF37;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.2), inset 0 0 10px rgba(212, 175, 55, 0.1);
  transform: translateY(-2px);
  color: #ffffff;
}

@media(max-width: 768px) {
  .headline { font-size: 2.5rem; }
  .subheadline { font-size: 1rem; padding: 0 1rem; }
  .exclusive-nav { padding: 1.5rem 2rem; }
  .black-card { width: 280px; height: 180px; }
}
</style>
