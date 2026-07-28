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
  // 2. Background Particles (full-page canvas)
  // ───────────────────────────────────────────
  const bgCanvas = document.getElementById('bg-particles');
  if (bgCanvas) {
    const ctx = bgCanvas.getContext('2d');
    let animationId;
    let mouseX = 0, mouseY = 0;

    function resizeBgCanvas() {
      bgCanvas.width = window.innerWidth;
      bgCanvas.height = window.innerHeight;
    }

    resizeBgCanvas();
    window.addEventListener('resize', resizeBgCanvas);

    class BgParticle {
      constructor() {
        this.reset();
      }

      reset() {
        this.x = Math.random() * bgCanvas.width;
        this.y = Math.random() * bgCanvas.height;
        this.size = Math.random() * 5 + 2;
        this.speedX = (Math.random() - 0.5) * 0.5;
        this.speedY = (Math.random() - 0.5) * 0.5;
        this.opacity = Math.random() * 0.3 + 0.18;
        const isDark = html.getAttribute('data-theme') === 'dark';
        const indigo = isDark ? '129, 140, 248' : '79, 70, 186';
        const cyan = isDark ? '34, 211, 238' : '8, 145, 178';
        this.color = Math.random() > 0.5
          ? `rgba(${indigo}, ${this.opacity})`
          : `rgba(${cyan}, ${this.opacity})`;
        this.shape = Math.random() > 0.5 ? 'circle' : 'rounded-rect';
        this.rotation = 0;
        this.rotationSpeed = (Math.random() - 0.5) * 0.008;
        this.life = 0;
        this.maxLife = 500 + Math.random() * 300;
      }

      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.rotation += this.rotationSpeed;
        this.life++;

        if (this.x < -50) this.x = bgCanvas.width + 50;
        if (this.x > bgCanvas.width + 50) this.x = -50;
        if (this.y < -50) this.y = bgCanvas.height + 50;
        if (this.y > bgCanvas.height + 50) this.y = -50;

        if (this.life > this.maxLife) this.reset();
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.opacity;

        if (this.shape === 'circle') {
          ctx.beginPath();
          ctx.arc(0, 0, this.size, 0, Math.PI * 2);
          ctx.fillStyle = this.color;
          ctx.fill();
        } else {
          const w = this.size * 1.5;
          const h = this.size * 0.9;
          const r = 1.5;
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

    const particleCount = Math.min(60, Math.floor(bgCanvas.width / 25));
    const particles = Array.from({ length: particleCount }, () => new BgParticle());

    function animateBg() {
      ctx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);
      particles.forEach(p => { p.update(); p.draw(); });
      animationId = requestAnimationFrame(animateBg);
    }

    animateBg();

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
  // 6. Back to Top
  // ───────────────────────────────────────────
  const backToTop = document.getElementById('back-to-top');

  if (backToTop) {
    const threshold = 400;
    let ticking = false;

    function onScroll() {
      backToTop.classList.toggle('visible', window.scrollY > threshold);
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => { onScroll(); ticking = false; });
        ticking = true;
      }
    });

    onScroll();

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ───────────────────────────────────────────
  // 7. HTMX Loading State
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
