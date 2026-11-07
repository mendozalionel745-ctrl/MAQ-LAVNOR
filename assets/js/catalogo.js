(() => {
  'use strict';
  const search = document.querySelector('#search');
  const type = document.querySelector('#equipment-type');
  const source = document.querySelector('#catalog-source');
  const loadMore = document.querySelector('#load-more');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.equipment-card')];
  const pending = [...document.querySelectorAll('.pending-family')];
  const results = document.querySelector('#results-count');
  const empty = document.querySelector('#no-results');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const params = new URLSearchParams(location.search);
  let category = buttons.some(b => b.dataset.filter === params.get('categoria')) ? params.get('categoria') : 'todos';
  let shownLimit = 12;
  search.value = params.get('buscar') || '';
  if ([...type.options].some(o => o.value === params.get('tipo'))) type.value = params.get('tipo');
  if ([...source.options].some(o => o.value === params.get('origen'))) source.value = params.get('origen');

  function filter(updateUrl = true, resetLimit = true) {
    if (resetLimit) shownLimit = 12;
    const query = normalize(search.value.trim());
    const matches = [];
    let models = 0;
    let lines = 0;
    let pendingCount = 0;
    buttons.forEach(button => {
      const active = button.dataset.filter === category;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    cards.forEach(card => {
      const originMatches = source.value === 'all'
        || (source.value === 'confirmed' && card.dataset.confirmed === 'true')
        || (source.value === 'manufacturer' && card.dataset.confirmed !== 'true' && card.dataset.kind === 'model')
        || (source.value === 'lines' && card.dataset.kind === 'line');
      const visible = (category === 'todos' || category === card.dataset.category)
        && (!type.value || type.value === card.dataset.type)
        && normalize(card.dataset.search).includes(query) && originMatches;
      if (visible) {
        if (card.dataset.kind === 'line') lines++; else models++;
        matches.push(card);
      }
      card.hidden = !visible || matches.length > shownLimit;
    });
    pending.forEach(card => {
      const visible = source.value === 'all'
        && (category === 'todos' || category === card.dataset.category)
        && (!type.value || card.dataset.types.split('|').includes(type.value))
        && normalize(card.dataset.search).includes(query);
      card.hidden = !visible;
      if (visible) pendingCount++;
    });
    const counts = [];
    if (models) counts.push(`${models} ${models === 1 ? 'modelo documentado' : 'modelos documentados'}`);
    if (lines) counts.push(`${lines} ${lines === 1 ? 'línea del fabricante' : 'líneas del fabricante'}`);
    if (pendingCount) counts.push(`${pendingCount} ${pendingCount === 1 ? 'familia pendiente' : 'familias pendientes'}`);
    if (matches.length > shownLimit) counts.push(`Mostrando ${shownLimit} de ${matches.length} productos`);
    results.textContent = counts.join(' · ') || 'Sin coincidencias';
    empty.hidden = matches.length + pendingCount > 0;
    loadMore.hidden = matches.length <= shownLimit;
    loadMore.textContent = `Mostrar ${Math.min(12, Math.max(0, matches.length - shownLimit))} productos más ↓`;
    if (updateUrl) {
      const next = new URLSearchParams();
      if (category !== 'todos') next.set('categoria', category);
      if (search.value.trim()) next.set('buscar', search.value.trim());
      if (type.value) next.set('tipo', type.value);
      if (source.value !== 'all') next.set('origen', source.value);
      history.replaceState(null, '', `${location.pathname}${next.size ? `?${next}` : ''}`);
    }
  }
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filter(); }));
  search.addEventListener('input', () => filter());
  type.addEventListener('change', () => filter());
  source.addEventListener('change', () => filter());
  loadMore.addEventListener('click', () => {
    const previous = new Set(cards.filter(card => !card.hidden));
    shownLimit += 12;
    filter(false, false);
    if (loadMore.hidden) cards.find(card => !card.hidden && !previous.has(card))?.querySelector('h3 a')?.focus({ preventScroll: true });
  });
  document.querySelector('#clear-filters').addEventListener('click', () => {
    category = 'todos'; search.value = ''; type.value = ''; source.value = 'all'; filter(); search.focus();
  });
  window.addEventListener('popstate', () => location.reload());
  filter(false);
})();
