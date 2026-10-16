import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = process.cwd();
const read = (path) => readFileSync(resolve(root, path), "utf8");
const failures = [];
const pass = (message) => console.log(`PASS ${message}`);
const fail = (message) => failures.push(message);

const requiredPhrases = ["Daga yige", "Li tao", "Daga goli"];
const app = read("app.js");
const index = read("index.html");
const readme = read("README.md");
const corpusHtml = read("corpus.html");
const corpusJs = read("corpus.js");
const plan = read("docs/PLAN-STT-TTS.md");
const checklist = read("docs/TESTING-CHECKLIST.md");
const candidates = read("docs/MODEL-CANDIDATES.md");
const lines = read("data/soninke-samples.jsonl").split(/\r?\n/).filter((line) => line.trim());

for (const phrase of requiredPhrases) {
  if (app.includes(phrase)) pass(`phrase initiale conservée dans le modèle applicatif: ${phrase}`);
  else fail(`phrase initiale absente ou modifiée: ${phrase}`);
}

const ids = new Set();
const requiredFields = ["id", "soninke", "french", "source", "license", "attribution", "project_status"];
for (const [index, line] of lines.entries()) {
  let item;
  try {
    item = JSON.parse(line);
  } catch (error) {
    fail(`JSONL ligne ${index + 1} invalide: ${error.message}`);
    continue;
  }
  for (const field of requiredFields) {
    if (typeof item[field] !== "string" || !item[field].trim()) {
      fail(`ligne JSONL ${index + 1}: champ obligatoire manquant ${field}`);
    }
  }
  if (item.id) {
    if (ids.has(item.id)) fail(`identifiant JSONL dupliqué: ${item.id}`);
    ids.add(item.id);
  }
  if (item.source && !/^https:\/\//.test(item.source)) {
    fail(`ligne JSONL ${index + 1}: source HTTPS attendue`);
  }
}
if (lines.length === 5 && ids.size === 5) pass("5 exemples JSONL valides, identifiants uniques");
else fail(`nombre d'exemples inattendu: ${lines.length} lignes, ${ids.size} identifiants uniques (5 attendus)`);

for (const [label, ok] of [
  ["lien vers le corpus depuis l'accueil", index.includes('href="corpus.html"')],
  ["recherche et export présents dans l'interface corpus", /corpus-search/.test(corpusHtml) && /export/.test(corpusJs)],
  ["plan STT/TTS référencé depuis le README", readme.includes("docs/PLAN-STT-TTS.md")],
  ["checklist mobile référencée depuis le README", readme.includes("docs/TESTING-CHECKLIST.md") && checklist.includes("Page de recherche du corpus")],
  ["inventaire des candidats référencé et prudent sur les modèles", readme.includes("docs/MODEL-CANDIDATES.md") && candidates.includes("pas encore validé") && candidates.includes("wav2vec2-bloom-speech-snk")],
  ["limites du TTS documentées dans le plan", plan.includes("Aucun TTS") && plan.includes("audio vérifié")],
]) {
  if (ok) pass(label);
  else fail(label);
}

if (failures.length) {
  console.error("\nÉCHECS:");
  for (const message of failures) console.error(`- ${message}`);
  process.exitCode = 1;
} else {
  console.log("\nValidation statique réussie. Cela ne remplace pas un test navigateur, un test audio ou une validation linguistique humaine.");
}
