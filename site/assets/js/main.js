/* Sparks OT — shared JS */

(function () {
  'use strict';

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Sticky header ---------------------------------------- */
  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Hamburger nav ---------------------------------------- */
  const toggle = document.querySelector('.nav-toggle');
  const navList = document.getElementById('nav-menu');

  if (toggle && navList) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      navList.classList.toggle('is-open', !open);
    });

    // close on outside click
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !navList.contains(e.target)) {
        toggle.setAttribute('aria-expanded', 'false');
        navList.classList.remove('is-open');
      }
    });

    // close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        toggle.setAttribute('aria-expanded', 'false');
        navList.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  /* ---- Mark active nav link --------------------------------- */
  const path = window.location.pathname.replace(/\/$/, '') || '/index';
  document.querySelectorAll('.nav-link').forEach((link) => {
    const href = link.getAttribute('href').replace(/\/$/, '');
    const matchHome = (href === '/' || href === '/index.html') &&
                      (path === '' || path.endsWith('index') || path === '/');
    const matchPage = href !== '/' && path.endsWith(href.replace(/^\//, '').replace('.html', ''));
    if (matchHome || matchPage) {
      link.setAttribute('aria-current', 'page');
    }
  });

  /* ---- Scroll-reveal (IntersectionObserver) ----------------- */
  if (!prefersReduced && 'IntersectionObserver' in window) {
    const revealObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('[data-reveal]').forEach((el) => revealObs.observe(el));
  } else {
    // Reduced motion: make everything visible immediately
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-visible'));
  }

  /* ---- Testimonial carousel --------------------------------- */
  const carousel = document.getElementById('testimonial-carousel');
  if (carousel) {
    const track  = carousel.querySelector('.carousel-track');
    const slides = carousel.querySelectorAll('.testimonial');
    const dotsEl = carousel.querySelector('.carousel-dots');
    const prevBtn = carousel.querySelector('.carousel-btn.prev');
    const nextBtn = carousel.querySelector('.carousel-btn.next');

    if (!track || slides.length === 0) return;

    let current = 0;
    let timer;

    // Build dots
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot' + (i === 0 ? ' is-active' : '');
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', `Testimonial ${i + 1} of ${slides.length}`);
      dot.setAttribute('aria-selected', String(i === 0));
      dot.addEventListener('click', () => goTo(i));
      dotsEl.appendChild(dot);
    });

    function goTo(index) {
      const dots = dotsEl.querySelectorAll('.carousel-dot');
      dots[current].classList.remove('is-active');
      dots[current].setAttribute('aria-selected', 'false');
      current = (index + slides.length) % slides.length;
      track.style.transform = `translateX(-${current * 100}%)`;
      dots[current].classList.add('is-active');
      dots[current].setAttribute('aria-selected', 'true');
      resetTimer();
    }

    prevBtn && prevBtn.addEventListener('click', () => goTo(current - 1));
    nextBtn && nextBtn.addEventListener('click', () => goTo(current + 1));

    // Auto-advance (skip if reduced motion)
    function startTimer() {
      if (prefersReduced) return;
      timer = setInterval(() => goTo(current + 1), 6000);
    }

    function resetTimer() {
      clearInterval(timer);
      startTimer();
    }

    // Pause on hover/focus
    carousel.addEventListener('mouseenter', () => clearInterval(timer));
    carousel.addEventListener('mouseleave', startTimer);
    carousel.addEventListener('focusin',    () => clearInterval(timer));
    carousel.addEventListener('focusout',   startTimer);

    // Keyboard navigation on track
    track.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft')  goTo(current - 1);
      if (e.key === 'ArrowRight') goTo(current + 1);
    });

    startTimer();
  }

  /* ---- Contact form (Formspree) ----------------------------- */
  const form = document.getElementById('contact-form');
  if (form) {
    const status = document.getElementById('form-status');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const submitBtn = form.querySelector('[type="submit"]');

      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';

      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: data,
          headers: { Accept: 'application/json' },
        });

        if (res.ok) {
          form.reset();
          status.className = 'form-status success';
          status.textContent = "Thanks — we'll be in touch soon!";
        } else {
          throw new Error('Server error');
        }
      } catch {
        status.className = 'form-status error';
        status.textContent = 'Something went wrong. Please email us directly at korrie@sparksot.com';
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send message';
        status.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  }
})();
