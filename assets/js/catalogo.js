(() => {
  'use strict';
  const search = document.querySelector('#search');
  const type = document.querySelector('#equipment-type');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.equipment-card')];
  const pending = [...document.querySelectorAll('.pending-family')];
  const results = document.querySelector('#results-count');
  const empty = document.querySelector('#no-results');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const params = new URLSearchParams(location.search);
  let category = buttons.some(button => button.dataset.filter === params.get('categoria')) ? params.get('categoria') : 'todos';
  search.value = params.get('buscar') || '';
  if ([...type.options].some(option => option.value === params.get('tipo'))) type.value = params.get('tipo');

  function filter(updateUrl = true) {
    const query = normalize(search.value.trim());
    let count = 0;
    let pendingCount = 0;
    buttons.forEach(button => {
      const active = button.dataset.filter === category;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    cards.forEach(card => {
      const visible = (category === 'todos' || category === card.dataset.category)
        && (!type.value || type.value === card.dataset.type)
        && normalize(card.dataset.search).includes(query);
      card.hidden = !visible;
      if (visible) count++;
    });
    pending.forEach(card => {
      const visible = (category === 'todos' || category === card.dataset.category)
        && (!type.value || card.dataset.types.split('|').includes(type.value))
        && normalize(card.dataset.search).includes(query);
      card.hidden = !visible;
      if (visible) pendingCount++;
    });
    results.textContent = `${count} ${count === 1 ? 'equipo con ficha técnica' : 'equipos con ficha técnica'}${pendingCount ? ` · ${pendingCount} ${pendingCount === 1 ? 'familia pendiente de documentación' : 'familias pendientes de documentación'}` : ''}`;
    empty.hidden = count + pendingCount > 0;
    if (updateUrl) {
      const next = new URLSearchParams();
      if (category !== 'todos') next.set('categoria', category);
      if (search.value.trim()) next.set('buscar', search.value.trim());
      if (type.value) next.set('tipo', type.value);
      history.replaceState(null, '', `${location.pathname}${next.size ? `?${next}` : ''}`);
    }
  }
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filter(); }));
  search.addEventListener('input', () => filter());
  type.addEventListener('change', () => filter());
  document.querySelector('#clear-filters').addEventListener('click', () => {
    category = 'todos'; search.value = ''; type.value = ''; filter(); search.focus();
  });
  window.addEventListener('popstate', () => location.reload());
  filter(false);
})();
