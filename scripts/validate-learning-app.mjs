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

for (const path of ["apprendre.html", "apprendre.css", "apprendre.js", "data/trilingual-lexicon.json", "data/language-sources.json", "data/learning-curriculum.json"]) {
  if (existsSync(resolve(root, path))) pass(`fichier requis présent : ${path}`);
  else fail(`fichier requis manquant : ${path}`);
}
const html = read("apprendre.html");
const js = read("apprendre.js");
const schema = parseJSON("data/trilingual-lexicon.json");
const sources = parseJSON("data/language-sources.json");
const curriculum = parseJSON("data/learning-curriculum.json");
const manifest = parseJSON("data/audio-manifest.json");
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
if (Array.isArray(schema?.entries)) pass("liste de fiches multilingues initialisée");
else fail("schema.entries doit être un tableau");
if (Array.isArray(sources?.sources) && sources.sources.length >= 5) pass("catalogue des sources documenté");
else fail("catalogue des sources absent ou incomplet");
if (sources?.policy?.includes("licensing")) pass("règle de licence avant import présente");
else fail("la politique de licence avant import doit être documentée");
if (Array.isArray(curriculum?.learningStages) && curriculum.learningStages.length >= 5) pass("parcours pédagogique structuré");
else fail("parcours pédagogique trop incomplet");
for (const required of ['id="from"', 'id="to"', 'id="search"', 'id="results"', 'id="entry-form"', 'id="export-json"', 'id="export-csv"', 'id="ressources"']) {
  if (html.includes(required)) pass(`interface contient ${required}`);
  else fail(`interface ne contient pas ${required}`);
}
for (const required of ["speechSynthesis", "data/soninke-lexicon.jsonl", "data/audio-manifest.json", "data/trilingual-lexicon.json", "localStorage", "pronunciationStatus", "translationStatus"]) {
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
