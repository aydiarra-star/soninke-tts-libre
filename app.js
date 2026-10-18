(() => {
  "use strict";
  const STORAGE_KEY = "soninke-tts-libre.validation.v1";
  const PHRASES = [
    { id: "p1", text: "Daga yige" },
    { id: "p2", text: "Li tao" },
    { id: "p3", text: "Daga goli" }
  ];
  const labels = {
    not_evaluated: "Non évaluée",
    correct: "Prononciation correcte",
    needs_correction: "À corriger"
  };
  let data = loadData();
  const cards = [...document.querySelectorAll(".phrase-card")];
  const globalMessage = document.getElementById("global-message");
  const objectUrls = new Map();

  function emptyRecord(phrase) {
    return { id: phrase.id, text: phrase.text, status: "not_evaluated", notes: "", audioFileName: "", updatedAt: null };
  }
  function loadData() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      return Object.fromEntries(PHRASES.map(p => {
        const old = saved[p.id] || {};
        return [p.id, { ...emptyRecord(p), ...old, id: p.id, text: p.text }];
      }));
    } catch {
      return Object.fromEntries(PHRASES.map(p => [p.id, emptyRecord(p)]));
    }
  }
  function persist(id) {
    data[id].updatedAt = new Date().toISOString();
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      const card = document.querySelector('[data-phrase-id="' + id + '"]');
      card.querySelector(".save-state").textContent = "Annotation enregistrée sur cet appareil.";
      globalMessage.textContent = "";
    } catch {
      globalMessage.textContent = "Le navigateur n’a pas pu enregistrer localement. Exportez vos annotations pour les conserver.";
    }
    renderProgress();
  }
  function renderProgress() {
    const evaluated = PHRASES.filter(p => data[p.id].status !== "not_evaluated").length;
    document.getElementById("progress-count").textContent = evaluated + " / " + PHRASES.length + " évaluées";
  }
  function renderCard(card) {
    const id = card.dataset.phraseId;
    const record = data[id];
    card.querySelector(".status-select").value = record.status;
    card.querySelector(".notes-input").value = record.notes || "";
    card.querySelector("[data-badge]").textContent = labels[record.status] || labels.not_evaluated;
    card.querySelector("[data-badge]").className = "eval-badge " + record.status;
    const player = card.querySelector(".audio-player");
    if (record.audioFileName) {
      card.querySelector(".audio-help").textContent = "Fichier sélectionné : " + record.audioFileName;
    }
  }
  cards.forEach(card => {
    const id = card.dataset.phraseId;
    const status = card.querySelector(".status-select");
    const notes = card.querySelector(".notes-input");
    const fileInput = card.querySelector(".audio-input");
    const player = card.querySelector(".audio-player");
    const help = document.getElementById("audio-help-" + id);
    card.querySelector("[data-badge]").textContent = labels[data[id].status];
    card.querySelector("[data-badge]").className = "eval-badge " + data[id].status;
    status.value = data[id].status;
    notes.value = data[id].notes || "";
    fileInput.addEventListener("change", () => {
      const file = fileInput.files && fileInput.files[0];
      if (!file) return;
      if (!file.type.startsWith("audio/")) {
        help.textContent = "Veuillez sélectionner un fichier audio.";
        fileInput.value = "";
        return;
      }
      if (objectUrls.has(id)) URL.revokeObjectURL(objectUrls.get(id));
      const url = URL.createObjectURL(file);
      objectUrls.set(id, url);
      player.src = url;
      player.hidden = false;
      data[id].audioFileName = file.name;
      help.textContent = "Fichier prêt à écouter : " + file.name + ". Il reste sur cet appareil.";
      persist(id);
    });
    status.addEventListener("change", () => {
      data[id].status = status.value;
      card.querySelector("[data-badge]").textContent = labels[status.value];
      card.querySelector("[data-badge]").className = "eval-badge " + status.value;
      persist(id);
    });
    notes.addEventListener("input", () => {
      data[id].notes = notes.value;
      persist(id);
    });
  });

  function recordsForExport() {
    return PHRASES.map(p => ({
      ...data[p.id],
      audioFileName: data[p.id].audioFileName || "",
      audioIncluded: false,
      audioNote: data[p.id].audioFileName ? "Fichier audio non inclus dans l’export ; conserver séparément." : "Aucun audio sélectionné"
    }));
  }
  function download(name, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = name;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }
  document.getElementById("export-json").addEventListener("click", () => {
    download("soninke-tts-validations.json", JSON.stringify({
      schemaVersion: 1,
      project: "Soninké TTS Libre",
      exportedAt: new Date().toISOString(),
      note: "Métadonnées uniquement. Aucun audio ni traduction n’est inclus.",
      records: recordsForExport()
    }, null, 2), "application/json;charset=utf-8");
  });
  document.getElementById("export-csv").addEventListener("click", () => {
    const rows = recordsForExport();
    const columns = ["id", "text", "status", "notes", "audioFileName", "audioIncluded", "updatedAt"];
    const quote = value => '"' + String(value ?? "").replace(/"/g, '""') + '"';
    const csv = [columns.map(quote).join(","), ...rows.map(r => columns.map(c => quote(r[c])).join(","))].join("\r\n");
    download("soninke-tts-validations.csv", "\uFEFF" + csv, "text/csv;charset=utf-8");
  });
  document.getElementById("clear-data").addEventListener("click", () => {
    if (!window.confirm("Effacer les annotations enregistrées dans ce navigateur ? Cette action ne peut pas être annulée.")) return;
    try { localStorage.removeItem(STORAGE_KEY); } catch {}
    data = Object.fromEntries(PHRASES.map(p => [p.id, emptyRecord(p)]));
    cards.forEach(card => {
      const id = card.dataset.phraseId;
      card.querySelector(".status-select").value = "not_evaluated";
      card.querySelector(".notes-input").value = "";
      card.querySelector("[data-badge]").textContent = labels.not_evaluated;
      card.querySelector("[data-badge]").className = "eval-badge not_evaluated";
      card.querySelector(".save-state").textContent = "";
      card.querySelector(".audio-input").value = "";
      const player = card.querySelector(".audio-player");
      player.pause(); player.removeAttribute("src"); player.load(); player.hidden = true;
      document.getElementById("audio-help-" + id).textContent = "Le fichier reste sur votre appareil ; il n’est pas envoyé au serveur.";
      if (objectUrls.has(id)) { URL.revokeObjectURL(objectUrls.get(id)); objectUrls.delete(id); }
    });
    renderProgress();
    globalMessage.textContent = "Annotations locales effacées.";
  });
  renderProgress();
})();