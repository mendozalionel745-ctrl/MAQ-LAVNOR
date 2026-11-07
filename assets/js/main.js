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
})();
