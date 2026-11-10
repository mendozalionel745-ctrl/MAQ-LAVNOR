(() => {
  'use strict';
  const button = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#main-navigation');
  function closeMenu() {
    button?.setAttribute('aria-expanded', 'false');
    button?.setAttribute('aria-label', 'Abrir menú');
    navigation?.classList.remove('is-open');
  }
  button?.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    navigation.classList.toggle('is-open', open);
  });
  navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button?.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      button.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!navigation?.contains(event.target) && !button?.contains(event.target)) closeMenu();
  });
  matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);

  // El contenido queda visible si JavaScript o IntersectionObserver no están disponibles.
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  if (!motion.matches && 'IntersectionObserver' in window) {
    const targets = document.querySelectorAll('.section-heading,.about-presentation,.purpose-grid article,.reasons-grid article,.values-layout,.logistics-copy,.peru-visual,.delivery-gallery figure,.company-preview-copy');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    targets.forEach(target => {
      target.classList.add('reveal');
      observer.observe(target);
    });
    motion.addEventListener('change', () => {
      if (motion.matches) {
        targets.forEach(target => target.classList.add('is-revealed'));
        observer.disconnect();
      }
    });
  }
})();
