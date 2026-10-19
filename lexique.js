(() => {
  "use strict";
  const DATA_URL = "data/soninke-lexicon.jsonl";
  const PAGE_SIZE = 50;
  const search = document.getElementById("lexicon-search");
  const filter = document.getElementById("lexicon-filter");
  const results = document.getElementById("lexicon-results");
  const count = document.getElementById("lexicon-count");
  const message = document.getElementById("lexicon-message");
  const pageIndicator = document.getElementById("page-indicator");
  const previous = document.getElementById("previous-page");
  const next = document.getElementById("next-page");
  let entries = [];
  let audioById = new Map();
  let page = 0;

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = String(text ?? "");
    return node;
  }
  function render() {
    const term = search.value.trim().toLocaleLowerCase();
    const wanted = filter.value;
    const filtered = entries.filter(entry => {
      const matchesTerm = !term || [entry.word, entry.id].join(" ").toLocaleLowerCase().includes(term);
      const matchesStatus = wanted === "all" || (wanted === "validated" ? entry.pronunciationValidated === true : entry.pronunciationValidated !== true);
      return matchesTerm && matchesStatus;
    });
    const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    page = Math.min(page, pageCount - 1);
    const visible = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
    results.replaceChildren();
    count.textContent = filtered.length + " / " + entries.length + " entrées";
    pageIndicator.textContent = "Page " + (page + 1) + " / " + pageCount;
    previous.disabled = page <= 0;
    next.disabled = page >= pageCount - 1;
    if (!visible.length) {
      results.append(el("p", "empty-results", "Aucun mot ne correspond à cette recherche."));
      return;
    }
    visible.forEach(entry => {
      const card = el("article", "corpus-card");
      const top = el("div", "corpus-card-top");
      top.append(el("span", "phrase-index", entry.id));
      top.append(el("span", "eval-badge " + (entry.pronunciationValidated ? "correct" : "needs_correction"),
        entry.pronunciationValidated === true ? "Prononciation validée" : (entry.technicalStatus === "generation_error" || entry.audioStatus === "generation_error" ? "Erreur technique — validation en attente" : "En attente de validation linguistique")));
      card.append(top);
      card.append(el("h2", "corpus-soninke", entry.word));
      const audioInfo = audioById.get(entry.id);
      if (audioInfo && audioInfo.audioAvailable && audioInfo.audioPath) {
        const audio = el("audio", "lexicon-audio-player");
        audio.controls = true;
        audio.preload = "none";
        audio.src = audioInfo.audioPath;
        audio.setAttribute("aria-label", "Écouter la prononciation de " + entry.word);
        card.append(audio);
        card.append(el("p", "corpus-field-label", "Audio disponible" + (audioInfo.durationSeconds ? " · " + audioInfo.durationSeconds.toFixed(2).replace(".", ",") + " s" : "")));
      } else {
        card.append(el("p", "corpus-caveat", "Audio indisponible pour cette entrée ; aucun fichier n’a été inventé."));
      }
      const details = entry.audioStatus === "audio_present_reused"
        ? "Statut audio du manifeste : audio existant réutilisé"
        : entry.audioStatus === "generated"
          ? "Statut audio du manifeste : audio généré"
          : "Statut audio du manifeste : génération en erreur";
      card.append(el("p", "corpus-field-label", details));
      if (entry.validationNote) card.append(el("p", "corpus-caveat", entry.validationNote));
      const source = el("p", "corpus-source");
      if (/^https:\/\//.test(entry.source)) {
        const link = el("a", "", "Consulter la source");
        link.href = entry.source;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        source.append(link);
      } else {
        source.append(document.createTextNode("Provenance : " + entry.source));
      }
      source.append(document.createTextNode(" · Licence " + entry.license + " · " + entry.attribution));
      card.append(source);
      results.append(card);
    });
  }
  search.addEventListener("input", () => { page = 0; render(); });
  filter.addEventListener("change", () => { page = 0; render(); });
  previous.addEventListener("click", () => { if (page > 0) { page--; render(); window.scrollTo({top: 0, behavior: "auto"}); } });
  next.addEventListener("click", () => { page++; render(); window.scrollTo({top: 0, behavior: "auto"}); });
  Promise.all([
    fetch(DATA_URL).then(response => { if (!response.ok) throw new Error("Lexique HTTP " + response.status); return response.text(); }),
    fetch("data/audio-manifest.json").then(response => { if (!response.ok) throw new Error("Manifeste audio HTTP " + response.status); return response.json(); })
  ])
    .then(([text, audioData]) => {
      entries = text.split(/\\r?\\n/).filter(line => line.trim()).map(line => JSON.parse(line));
      if (!entries.length) throw new Error("lexique vide");
      audioById = new Map((audioData.entries || []).map(item => [item.id, item]));
      render();
    })
    .catch(error => {
      count.textContent = "Lexique indisponible";
      message.textContent = "Impossible de charger le lexique et son manifeste audio. " + error.message;
    });
})();