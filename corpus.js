(() => {
  "use strict";
  const DATA_URL = "data/soninke-samples.jsonl";
  const STORAGE_KEY = "soninke-tts-libre.corpus-reviews.v1";
  const search = document.getElementById("corpus-search");
  const filter = document.getElementById("review-filter");
  const results = document.getElementById("corpus-results");
  const count = document.getElementById("result-count");
  const message = document.getElementById("corpus-message");
  let entries = [];
  let reviews = readReviews();

  function readReviews() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      return value && typeof value === "object" && !Array.isArray(value) ? value : {};
    } catch { return {}; }
  }
  function saveReviews() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(reviews));
      message.textContent = "Validation enregistrée sur cet appareil.";
    } catch {
      message.textContent = "Enregistrement impossible : exportez les validations pour les conserver.";
    }
  }
  function safeText(value) { return String(value ?? ""); }
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function currentReview(id) {
    return reviews[id] || { status: "not_reviewed", note: "", reviewerRole: "", reviewedAt: null };
  }
  function render() {
    const term = search.value.trim().toLocaleLowerCase();
    const wanted = filter.value;
    const filtered = entries.filter(entry => {
      const review = currentReview(entry.id);
      const haystack = [entry.soninke, entry.french, entry.id].join(" ").toLocaleLowerCase();
      return (!term || haystack.includes(term)) && (wanted === "all" || review.status === wanted);
    });
    results.replaceChildren();
    count.textContent = filtered.length + " / " + entries.length + " phrases";
    if (!filtered.length) {
      results.append(el("p", "empty-results", "Aucune phrase ne correspond à cette recherche."));
      return;
    }
    filtered.forEach(entry => {
      const review = currentReview(entry.id);
      const card = el("article", "corpus-card");
      const top = el("div", "corpus-card-top");
      top.append(el("span", "phrase-index", "SOURCE " + entry.source_phrase_id));
      const badgeLabels = { not_reviewed: "À vérifier", confirmed: "Confirmée par un locuteur", correction: "À corriger" };
      top.append(el("span", "eval-badge " + (review.status === "confirmed" ? "correct" : review.status === "correction" ? "needs_correction" : ""), badgeLabels[review.status] || badgeLabels.not_reviewed));
      card.append(top);
      card.append(el("h2", "corpus-soninke", entry.soninke));
      const frenchLabel = el("p", "corpus-field-label", "Traduction fournie par la source");
      card.append(frenchLabel, el("p", "corpus-french", entry.french));
      const source = el("p", "corpus-source");
      const sourceLink = el("a", "", "Voir la phrase source");
      sourceLink.href = entry.source;
      sourceLink.target = "_blank";
      sourceLink.rel = "noopener noreferrer";
      source.append(sourceLink, document.createTextNode(" · Licence CC BY 4.0 · Attribution : " + entry.attribution));
      card.append(source);
      card.append(el("p", "corpus-caveat", "Non revérifiée indépendamment dans ce projet. Vérifier la variété, le sens et la prononciation avec un locuteur."));
      const form = el("div", "corpus-review-form");
      const statusLabel = el("label", "field-label", "Résultat de la vérification");
      const status = el("select", "status-select");
      status.setAttribute("aria-label", "Résultat de la vérification pour " + entry.soninke);
      [["not_reviewed","À vérifier"],["confirmed","Confirmée par un locuteur"],["correction","À corriger"]].forEach(([value,label]) => {
        const option = el("option","",label); option.value = value; status.append(option);
      });
      status.value = review.status;
      statusLabel.append(status);
      const noteLabel = el("label", "field-label", "Remarque de validation");
      const note = el("textarea", "notes-input");
      note.rows = 2;
      note.placeholder = "Variante, correction proposée, sens confirmé…";
      note.value = safeText(review.note);
      noteLabel.append(note);
      const roleLabel = el("label", "field-label", "Validateur (rôle, facultatif)");
      const role = el("input", "status-select");
      role.type = "text";
      role.maxLength = 100;
      role.placeholder = "Ex. locuteur natif, enseignant";
      role.value = safeText(review.reviewerRole);
      roleLabel.append(role);
      const save = el("button", "button button-primary", "Enregistrer la validation");
      save.type = "button";
      save.addEventListener("click", () => {
        reviews[entry.id] = {
          status: status.value,
          note: note.value.trim(),
          reviewerRole: role.value.trim(),
          reviewedAt: new Date().toISOString()
        };
        saveReviews();
        render();
      });
      form.append(statusLabel, noteLabel, roleLabel, save);
      card.append(form);
      results.append(card);
    });
  }
  search.addEventListener("input", render);
  filter.addEventListener("change", render);
  document.getElementById("export-reviews").addEventListener("click", () => {
    const payload = {
      schemaVersion: 1,
      project: "Soninké TTS Libre",
      exportedAt: new Date().toISOString(),
      note: "Métadonnées de validation locales uniquement ; ne constitue pas une validation TTS.",
      sourceLicense: "CC BY 4.0",
      sourceAttribution: "noah-medra (ORCID 0009-0003-6018-9802), snk_engine, 2026",
      records: entries.map(entry => ({ ...entry, validation: currentReview(entry.id) }))
    };
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json;charset=utf-8" }));
    const link = el("a"); link.href = url; link.download = "soninke-corpus-reviews.json";
    document.body.append(link); link.click(); link.remove(); URL.revokeObjectURL(url);
  });
  document.getElementById("clear-reviews").addEventListener("click", () => {
    if (!window.confirm("Effacer les validations du corpus enregistrées sur cet appareil ?")) return;
    reviews = {};
    try { localStorage.removeItem(STORAGE_KEY); } catch {}
    message.textContent = "Validations locales effacées.";
    render();
  });
  fetch(DATA_URL)
    .then(response => { if (!response.ok) throw new Error("HTTP " + response.status); return response.text(); })
    .then(text => {
      entries = text.split(/\r?\n/).filter(line => line.trim()).map(line => JSON.parse(line));
      if (!entries.length) throw new Error("corpus vide");
      render();
    })
    .catch(() => {
      count.textContent = "Corpus indisponible";
      message.textContent = "Impossible de charger le corpus. Ouvrez cette page depuis le site publié ou servez le dépôt via HTTP(S) ; l’ouverture directe du fichier peut bloquer fetch().";
    });
})();