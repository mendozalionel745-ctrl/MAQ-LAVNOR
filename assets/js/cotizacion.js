(() => {
  'use strict';
  const config = window.MAQ_CONFIG || {};
  const form = document.querySelector('#quote-form');
  const selection = document.querySelector('#equipment');
  const params = new URLSearchParams(location.search);
  const requested = params.get('equipo') || params.get('tipo');
  if ([...selection.options].some(option => option.value === requested)) selection.value = requested;
  const selectionLabel = document.querySelector('#selected-equipment');
  const selectionState = document.createElement('span');
  selectionState.className = 'selection-state';
  selectionLabel.after(selectionState);
  const result = document.querySelector('#quote-result');
  const message = document.querySelector('#quote-message');
  const feedback = document.querySelector('#copy-status');
  const whatsapp = /^\d{10,15}$/.test(config.whatsapp || '') ? config.whatsapp : '';
  const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(config.email || '') ? config.email : '';
  const configured = Boolean(whatsapp || email);
  document.querySelector('#prepare-quote').disabled = false;

  function updateSelection() {
    selectionLabel.textContent = selection.selectedOptions[0].textContent;
    selectionState.textContent = selection.selectedOptions[0].dataset.status || 'Disponibilidad y configuración sujetas a consulta';
  }
  updateSelection();
  selection.addEventListener('change', updateSelection);
  for (const [key, value] of [['whatsapp', whatsapp ? `+${whatsapp}` : 'Pendiente de completar'], ['email', email || 'Pendiente de completar'], ['address', config.address || 'Pendiente de completar']]) {
    document.querySelector(`[data-contact="${key}"]`).textContent = value;
  }
  if (configured) {
    document.querySelector('#contact-state-title').textContent = 'El envío se completa en el canal elegido';
    document.querySelector('#contact-state').textContent = 'Prepararemos un mensaje para abrir en tu canal de contacto. El envío se completa en esa aplicación.';
  }
  form.addEventListener('input', () => { result.hidden = true; feedback.textContent = ''; });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const fields = new FormData(form);
    const lines = [
      'SOLICITUD DE COTIZACIÓN · MAQ LAVNOR',
      `Equipo / tipo: ${selection.selectedOptions[0].textContent}`,
      `Estado en catálogo: ${selectionState.textContent}`,
      `Contacto: ${fields.get('name').trim()}`,
      `Empresa: ${fields.get('company').trim() || 'No indicada'}`,
      `Correo: ${fields.get('email').trim() || 'No indicado'}`,
      `Teléfono: ${fields.get('phone').trim() || 'No indicado'}`,
      `Ubicación del proyecto: ${fields.get('location').trim()}`,
      `Plazo o fechas: ${fields.get('period').trim()}`,
      `Detalle: ${fields.get('details').trim() || 'Sin detalles adicionales'}`
    ];
    message.value = lines.join('\n');
    const waLink = document.querySelector('#send-whatsapp');
    const mailLink = document.querySelector('#send-email');
    waLink.hidden = !whatsapp;
    mailLink.hidden = !email;
    if (whatsapp) waLink.href = `https://wa.me/${whatsapp}?text=${encodeURIComponent(message.value)}`;
    if (email) mailLink.href = `mailto:${email}?subject=${encodeURIComponent(`Cotización · ${selection.selectedOptions[0].textContent}`)}&body=${encodeURIComponent(message.value)}`;
    document.querySelector('#result-state').textContent = configured
      ? 'Mensaje preparado. Ábrelo en el canal elegido y completa allí el envío. No se ha enviado desde esta web.'
      : 'Consulta preparada en este dispositivo. No se ha enviado: los canales comerciales están pendientes de configurar.';
    result.hidden = false;
    result.focus();
    result.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'center' });
  });
  document.querySelector('#copy-quote').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(message.value);
      feedback.textContent = 'Texto copiado. No se ha enviado ninguna solicitud.';
    } catch {
      message.focus(); message.select();
      feedback.textContent = 'Seleccionamos el texto. Usa Copiar en tu dispositivo.';
    }
  });
  document.querySelector('#download-quote').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([message.value], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url; link.download = 'consulta-maq-lavnor.txt'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    feedback.textContent = 'Descarga preparada. No se ha enviado ninguna solicitud.';
  });
})();
