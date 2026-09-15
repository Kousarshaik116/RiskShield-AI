document.querySelectorAll('form[data-loading]').forEach(form => {
  form.addEventListener('submit', () => {
    const button = form.querySelector('button[type="submit"]');
    button.dataset.original = button.innerHTML;
    button.disabled = true;
    button.textContent = form.dataset.loading;
    form.setAttribute('aria-busy', 'true');
  });
});
window.addEventListener('pageshow', () => {
  document.querySelectorAll('form[data-loading]').forEach(form => {
    const button = form.querySelector('button[type="submit"]');
    if (button.dataset.original) button.innerHTML = button.dataset.original;
    button.disabled = false;
    form.removeAttribute('aria-busy');
  });
});
