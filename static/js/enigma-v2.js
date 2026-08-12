(() => {
  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-mobile-menu]');
  const body = document.body;

  const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 12);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    menu?.classList.toggle('open', !open);
    body.classList.toggle('menu-open', !open);
  });

  menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    toggle?.setAttribute('aria-expanded', 'false');
    menu.classList.remove('open');
    body.classList.remove('menu-open');
  }));

  const reveals = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });
    reveals.forEach(el => observer.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('is-visible'));
  }

  document.querySelectorAll('.toast-close').forEach(btn => {
    btn.addEventListener('click', () => btn.closest('.toast')?.remove());
  });

  document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('input', () => {
      if (input.value && !input.value.startsWith('+') && /^\d/.test(input.value)) {
        input.value = '+' + input.value;
      }
    });
  });
})();
