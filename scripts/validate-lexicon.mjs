import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const file = resolve(process.cwd(), "data/soninke-lexicon.jsonl");
const lines = readFileSync(file, "utf8").split(/\r?\n/).filter((line) => line.trim());
const failures = [];
const ids = new Set();
const words = new Set();
const allowedAudioStatuses = new Set(["audio_present_reused", "generated", "generation_error"]);
const requiredStrings = ["id", "word", "source", "license", "attribution"];
const pass = (message) => console.log(`PASS ${message}`);
const fail = (message) => failures.push(message);

for (const [index, line] of lines.entries()) {
  let entry;
  try {
    entry = JSON.parse(line);
  } catch (error) {
    fail(`ligne ${index + 1}: JSON invalide (${error.message})`);
    continue;
  }
  for (const field of requiredStrings) {
    if (typeof entry[field] !== "string" || !entry[field].trim()) {
      fail(`ligne ${index + 1}: champ obligatoire manquant ou vide: ${field}`);
    }
  }
  if (entry.id) {
    if (ids.has(entry.id)) fail(`identifiant dupliqué: ${entry.id}`);
    ids.add(entry.id);
  }
  if (entry.word) {
    if (words.has(entry.word)) fail(`mot dupliqué: ${entry.word}`);
    words.add(entry.word);
  }
  if (entry.source && !/^https:\/\//.test(entry.source) && !entry.source.startsWith("phrase de test fournie par le référent")) {
    fail(`ligne ${index + 1}: source HTTPS ou provenance de test documentée attendue`);
  }
  if (!allowedAudioStatuses.has(entry.audioStatus)) {
    fail(`ligne ${index + 1}: audioStatus non autorisé: ${entry.audioStatus}`);
  }
  if (entry.pronunciationValidated !== true || entry.validationStatus !== "validated") {
    fail(`ligne ${index + 1}: statut linguistique attendu = validé / validated`);
  }
  if (typeof entry.validationNote !== "string" || !entry.validationNote.includes("Validation linguistique confirmée par le référent linguistique soninké du projet")) {
    fail(`ligne ${index + 1}: attestation du référent linguistique manquante`);
  }
}

if (lines.length === 577) pass("577 entrées présentes");
else fail(`577 entrées attendues, ${lines.length} trouvées`);
if (ids.size === lines.length) pass("identifiants uniques");
else fail(`identifiants uniques: ${ids.size} pour ${lines.length} lignes`);
if (words.size === lines.length) pass("mots uniques");
else fail(`mots uniques: ${words.size} pour ${lines.length} lignes`);
if (failures.length) {
  console.error("\nÉCHECS:");
  for (const message of failures) console.error(`- ${message}`);
  process.exitCode = 1;
} else {
  console.log("Validation lexique réussie : structure et attestation du référent linguistique présentes pour chaque entrée. Le contrôle automatique ne réévalue pas lui-même la prononciation.");
}
