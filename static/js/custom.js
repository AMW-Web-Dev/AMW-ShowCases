/* ══════════════════════════════════════════════════
   AMW Portfolio — Custom JavaScript
   ══════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ───────────────────────────────────────────
  // 1. Dark/Light Mode Toggle
  // ───────────────────────────────────────────
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;
  const STORAGE_KEY = 'amw-portfolio-theme';

  function getPreferredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    if (themeToggle) {
      themeToggle.innerHTML = theme === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-fill"></i>';
      themeToggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    }
    // Also update Bootstrap navbar class
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      navbar.classList.toggle('navbar-dark', theme === 'dark');
      navbar.classList.toggle('navbar-light', theme === 'light');
    }
  }

  // Apply saved theme immediately (before paint if possible)
  const initialTheme = getPreferredTheme();
  setTheme(initialTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // Listen for system preference changes
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      setTheme(e.matches ? 'light' : 'dark');
    }
  });

  // ───────────────────────────────────────────
  // 2. Hero Particles (Canvas)
  // ───────────────────────────────────────────
  const heroCanvas = document.getElementById('hero-particles');
  if (heroCanvas) {
    const ctx = heroCanvas.getContext('2d');
    let animationId;
    let mouseX = 0, mouseY = 0;

    function resizeCanvas() {
      heroCanvas.width = heroCanvas.offsetWidth;
      heroCanvas.height = heroCanvas.offsetHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Particle class — geometric shapes, not dots
    class GeoParticle {
      constructor() {
        this.reset();
      }

      reset() {
        this.x = Math.random() * heroCanvas.width;
        this.y = Math.random() * heroCanvas.height;
        this.size = Math.random() * 6 + 2;
        this.speedX = (Math.random() - 0.5) * 0.5;
        this.speedY = (Math.random() - 0.5) * 0.5;
        this.opacity = Math.random() * 0.4 + 0.1;
        this.shape = Math.random() > 0.5 ? 'circle' : 'rounded-rect';
        this.color = Math.random() > 0.6
          ? `rgba(129, 140, 248, ${this.opacity})`   // indigo
          : `rgba(34, 211, 238, ${this.opacity})`;     // cyan
        this.rotation = 0;
        this.rotationSpeed = (Math.random() - 0.5) * 0.01;
        this.life = 0;
        this.maxLife = 300 + Math.random() * 200;
      }

      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.rotation += this.rotationSpeed;
        this.life++;

        // Mouse parallax
        const dx = mouseX - this.x;
        const dy = mouseY - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 200) {
          const force = (200 - dist) / 200 * 0.3;
          this.x -= dx * force * 0.01;
          this.y -= dy * force * 0.01;
        }

        // Wrap around edges with padding
        if (this.x < -50) this.x = heroCanvas.width + 50;
        if (this.x > heroCanvas.width + 50) this.x = -50;
        if (this.y < -50) this.y = heroCanvas.height + 50;
        if (this.y > heroCanvas.height + 50) this.y = -50;

        if (this.life > this.maxLife) this.reset();
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.opacity * (1 - this.life / this.maxLife * 0.5);

        if (this.shape === 'circle') {
          ctx.beginPath();
          ctx.arc(0, 0, this.size, 0, Math.PI * 2);
          ctx.fillStyle = this.color;
          ctx.fill();
        } else {
          const w = this.size * 1.5;
          const h = this.size;
          const r = 2;
          ctx.beginPath();
          ctx.moveTo(-w / 2 + r, -h / 2);
          ctx.lineTo(w / 2 - r, -h / 2);
          ctx.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r);
          ctx.lineTo(w / 2, h / 2 - r);
          ctx.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2);
          ctx.lineTo(-w / 2 + r, h / 2);
          ctx.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r);
          ctx.lineTo(-w / 2, -h / 2 + r);
          ctx.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
          ctx.closePath();
          ctx.fillStyle = this.color;
          ctx.fill();
        }

        ctx.restore();
      }
    }

    // Connection lines between nearby particles
    function drawConnections(particles) {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(129, 140, 248, ${0.06 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }
    }

    // Create particles
    const particleCount = Math.min(60, Math.floor(heroCanvas.width / 20));
    const particles = Array.from({ length: particleCount }, () => new GeoParticle());

    // Track mouse for parallax
    heroCanvas.addEventListener('mousemove', (e) => {
      const rect = heroCanvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    heroCanvas.addEventListener('mouseleave', () => {
      mouseX = -9999;
      mouseY = -9999;
    });

    function animateParticles() {
      ctx.clearRect(0, 0, heroCanvas.width, heroCanvas.height);

      particles.forEach(p => {
        p.update();
        p.draw();
      });

      drawConnections(particles);
      animationId = requestAnimationFrame(animateParticles);
    }

    animateParticles();

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
      if (animationId) cancelAnimationFrame(animationId);
    });
  }

  // ───────────────────────────────────────────
  // 3. Scroll Reveal Animations
  // ───────────────────────────────────────────
  const revealElements = document.querySelectorAll('.reveal');

  if (revealElements.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          // Staggered delay
          setTimeout(() => {
            entry.target.classList.add('active');
          }, index * 100);
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -50px 0px',
    });

    revealElements.forEach(el => observer.observe(el));
  }

  // ───────────────────────────────────────────
  // 4. Active Nav Link Highlight
  // ───────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
      link.classList.add('active');
    }
  });

  // ───────────────────────────────────────────
  // 5. Smooth Anchor Scroll
  // ───────────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ───────────────────────────────────────────
  // 6. HTMX Loading State
  // ───────────────────────────────────────────
  if (typeof htmx !== 'undefined') {
    document.body.addEventListener('htmx:beforeRequest', (e) => {
      const target = e.detail.target;
      if (target) target.classList.add('loading');
    });

    document.body.addEventListener('htmx:afterRequest', (e) => {
      const target = e.detail.target;
      if (target) target.classList.remove('loading');
    });
  }
});
