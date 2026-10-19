import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const root = process.cwd();
const read = (path) => readFileSync(resolve(root, path), "utf8");
const failures = [];
const pass = (message) => console.log(`PASS ${message}`);
const fail = (message) => failures.push(message);
const parseJSON = (path) => {
  try { return JSON.parse(read(path)); }
  catch (error) { fail(`${path}: JSON invalide (${error.message})`); return null; }
};

for (const path of ["apprendre.html", "apprendre.css", "apprendre.js", "data/trilingual-lexicon.json", "data/wolof-fr-dictionary.json", "data/language-sources.json", "data/learning-curriculum.json"]) {
  if (existsSync(resolve(root, path))) pass(`fichier requis présent : ${path}`);
  else fail(`fichier requis manquant : ${path}`);
}
const html = read("apprendre.html");
const js = read("apprendre.js");
const schema = parseJSON("data/trilingual-lexicon.json");
const sources = parseJSON("data/language-sources.json");
const curriculum = parseJSON("data/learning-curriculum.json");
const manifest = parseJSON("data/audio-manifest.json");
const wolofDictionary = parseJSON("data/wolof-fr-dictionary.json");
const lines = read("data/soninke-lexicon.jsonl").split(/\r?\n/).filter((line) => line.trim());
const languageCodes = ["soninke", "wolof", "fr", "en"];

for (const code of languageCodes) {
  if (schema?.languages?.some((language) => language.code === code)) pass(`langue de lancement enregistrée : ${code}`);
  else fail(`langue de lancement manquante : ${code}`);
  if (curriculum?.languages?.includes(code)) pass(`parcours pédagogique prévu : ${code}`);
  else fail(`parcours pédagogique manquant : ${code}`);
}
for (const code of ["pulaar", "bambara", "serere"]) {
  if (schema?.futureLanguages?.includes(code)) pass(`langue future prévue : ${code}`);
  else fail(`langue future manquante : ${code}`);
}
if (Array.isArray(schema?.entries)) {
  const ids = new Set();
  for (const [index, entry] of schema.entries.entries()) {
    if (!entry.id || ids.has(entry.id)) fail(`fiche multilingue ${index + 1}: identifiant absent ou dupliqué`);
    ids.add(entry.id);
    for (const lang of languageCodes) {
      if (!entry[lang] || typeof entry[lang] !== "object") fail(`fiche ${entry.id}: bloc de langue manquant ${lang}`);
      else if (typeof entry[lang].word !== "string") fail(`fiche ${entry.id}: champ word absent pour ${lang}`);
    }
    if (!String(entry.source || "").startsWith("https://")) fail(`fiche ${entry.id}: source URL obligatoire`);
    if (!entry.status || !entry.pronunciationStatus || !entry.translationStatus) fail(`fiche ${entry.id}: statuts distincts obligatoires`);
  }
  if (ids.size === schema.entries.length) pass(`${schema.entries.length} fiches multilingues sourcées, identifiants uniques`);
} else fail("schema.entries doit être un tableau");

if (Array.isArray(wolofDictionary?.entries) && wolofDictionary.entryCount === wolofDictionary.entries.length && wolofDictionary.entryCount >= 500) {
  const wolofIds = new Set();
  let sourceErrors = 0;
  for (const entry of wolofDictionary.entries) {
    if (!entry.id || wolofIds.has(entry.id)) sourceErrors++;
    wolofIds.add(entry.id);
    if (!String(entry.source || "").startsWith("https://")) sourceErrors++;
    if (!entry.fr?.word || !entry.wolof?.word) sourceErrors++;
  }
  if (!sourceErrors) pass(`dictionnaire Jàngileen importé : ${wolofDictionary.entryCount} fiches sourcées et identifiants uniques`);
  else fail(`dictionnaire Jàngileen : ${sourceErrors} anomalies dans les sources, mots ou identifiants`);
} else fail("dictionnaire Jàngileen incomplet : au moins 500 fiches et un compteur cohérent sont attendus");
if (Array.isArray(sources?.sources) && sources.sources.length >= 5) pass("catalogue des sources documenté");
else fail("catalogue des sources absent ou incomplet");
if (sources?.policy?.includes("licensing")) pass("règle de licence avant import présente");
else fail("la politique de licence avant import doit être documentée");
if (Array.isArray(curriculum?.learningStages) && curriculum.learningStages.length >= 5) pass("parcours pédagogique structuré");
else fail("parcours pédagogique trop incomplet");
for (const required of ['id="from"', 'id="to"', 'id="search"', 'id="results"', 'id="entry-form"', 'id="export-json"', 'id="export-csv"', 'id="ressources"', 'id="parcours"']) {
  if (html.includes(required)) pass(`interface contient ${required}`);
  else fail(`interface ne contient pas ${required}`);
}
for (const required of ["speechSynthesis", "data/soninke-lexicon.jsonl", "data/audio-manifest.json", "data/trilingual-lexicon.json", "localStorage", "pronunciationStatus", "translationStatus", "path-action"]) {
  if (js.includes(required)) pass(`comportement attendu présent : ${required}`);
  else fail(`comportement attendu absent : ${required}`);
}
if (lines.length === 577) pass("577 entrées soninké lisibles par le prototype");
else fail(`577 entrées soninké attendues, ${lines.length} trouvées`);
if (manifest?.entryCount === 577 && manifest?.audioCount === 576 && manifest?.missingAudioIds?.includes("snk-00308")) {
  pass("manifeste audio cohérent : 577 entrées, 576 WAV, une absence explicitée");
} else fail("compteurs du manifeste audio inattendus");
if (manifest?.entries?.length === 577) {
  const ids = new Set(manifest.entries.map((entry) => entry.id));
  if (ids.size === 577) pass("identifiants du manifeste audio uniques");
  else fail("identifiants du manifeste audio dupliqués");
  const missing = manifest.entries.filter((entry) => entry.audioAvailable && !existsSync(resolve(root, entry.audioPath)));
  if (!missing.length) pass("tous les chemins audio déclarés disponibles existent dans le dépôt");
  else fail(`fichiers audio manquants malgré leur disponibilité déclarée : ${missing.slice(0, 5).map((entry) => entry.id).join(", ")}`);
}
if (failures.length) {
  console.error("\nÉCHECS:");
  for (const message of failures) console.error(`- ${message}`);
  process.exitCode = 1;
} else {
  console.log("\nValidation statique multilingue réussie. Elle ne remplace pas les tests Safari/iPhone, la vérification audio manuelle ou une validation linguistique humaine.");
}
