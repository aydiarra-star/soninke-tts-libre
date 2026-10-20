(() => {
  const toast = document.getElementById('toast');
  let toastTimer;
  function notify(message, kind = '') {
    if (!toast) return;
    toast.textContent = message;
    toast.className = 'toast show' + (kind ? ' ' + kind : '');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toast.className = 'toast'; }, 3000);
  }

  const search = document.getElementById('globalSearch');
  const cards = [...document.querySelectorAll('.language-card')];
  const empty = document.getElementById('emptySearch');
  function filterLanguages() {
    const q = (search?.value || '').trim().toLocaleLowerCase('fr');
    let visible = 0;
    cards.forEach(card => {
      const text = (card.innerText + ' ' + (card.dataset.search || '')).toLocaleLowerCase('fr');
      const match = !q || text.includes(q);
      card.hidden = !match;
      if (match) visible++;
    });
    if (empty) empty.hidden = visible !== 0;
  }
  search?.addEventListener('input', filterLanguages);
  search?.addEventListener('keydown', event => {
    if (event.key === 'Escape') { search.value = ''; filterLanguages(); search.blur(); }
  });
  document.addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault(); search?.focus();
    }
  });

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      document.querySelectorAll('.nav-link').forEach(item => item.classList.remove('active'));
      link.classList.add('active');
      document.getElementById('sidebar')?.classList.remove('open');
    });
  });

  document.querySelectorAll('[data-start]').forEach(button => {
    button.addEventListener('click', () => {
      const language = button.dataset.start;
      notify('Parcours ' + language + ' sélectionné. Les leçons seront reliées à tes contenus validés.');
    });
  });

  document.getElementById('lessonButton')?.addEventListener('click', () => {
    notify('Leçon « Saluer avec le sourire » sélectionnée. Audio et exercices seront ajoutés avec les ressources validées.');
  });
  document.getElementById('audioButton')?.addEventListener('click', () => {
    notify('Aucun fichier audio n’est encore relié à cette maquette.', 'error');
  });
  document.getElementById('coachButton')?.addEventListener('click', () => {
    notify('Le coach IA est une maquette visuelle : aucune conversation n’est encore connectée.');
  });
  document.getElementById('notifyButton')?.addEventListener('click', () => {
    notify('Tu es à jour : aucune nouvelle notification.');
  });

  const periodButton = document.getElementById('periodButton');
  const periods = ['Cette semaine⌄', 'Ce mois-ci⌄', 'Tout le parcours⌄'];
  let period = 0;
  periodButton?.addEventListener('click', () => {
    period = (period + 1) % periods.length;
    periodButton.textContent = periods[period];
    notify('Vue « ' + periods[period].replace('⌄', '') + ' » : les statistiques affichées restent des données de démonstration.');
  });

  const menuToggle = document.getElementById('menuToggle');
  menuToggle?.addEventListener('click', () => document.getElementById('sidebar')?.classList.toggle('open'));
  document.addEventListener('click', event => {
    const sidebar = document.getElementById('sidebar');
    if (sidebar?.classList.contains('open') && !sidebar.contains(event.target) && !menuToggle?.contains(event.target)) {
      sidebar.classList.remove('open');
    }
  });
})();