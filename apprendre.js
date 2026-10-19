(() => {
"use strict";
const $=id=>document.getElementById(id);
let LANGS={soninke:{label:"Soninké",code:"SNK",speech:""},wolof:{label:"Wolof",code:"WOL",speech:"wo-SN"},fr:{label:"Français",code:"FR",speech:"fr-FR"},en:{label:"English",code:"EN",speech:"en-US"}};
const CAT={greeting:"Salutations","daily-life":"Vie quotidienne",family:"Famille",travel:"Voyage",food:"Alimentation",grammar:"Grammaire",other:"Autre"};
const POS={noun:"nom",verb:"verbe",adjective:"adjectif",adverb:"adverbe",preposition:"préposition",pronoun:"pronom",article:"article",conjunction:"conjonction",other:"non précisé"};
const KEY="soninke-tts-libre-learning-v1";let entries=[],local=[];
const sameSource=(a,b)=>{try{return decodeURIComponent(a)===decodeURIComponent(b)}catch(_){return a===b}};
const val=(e,l,k)=>String(e&&e[l]&&e[l][k]||"").trim();
const norm=e=>({...e,id:e.id||"local-"+(typeof crypto!=="undefined"&&crypto.randomUUID?crypto.randomUUID():Date.now()+"-"+Math.random()),category:e.category||"other",grammar_category:e.grammar_category||"",source:e.source||"",sourceName:e.sourceName||"",license:e.license||"",sourceExamples:Array.isArray(e.sourceExamples)?e.sourceExamples:[],origin:e.origin||"community",status:e.status||"draft",pronunciationStatus:e.pronunciationStatus||"unverified",translationStatus:e.translationStatus||"unverified"});
function configureLanguages(definitions){
 const active=(definitions||[]).filter(item=>item&&item.code&&item.name);
 if(!active.length)return;
 const next={};
 active.forEach(item=>{next[item.code]={label:item.name,code:item.code.toUpperCase(),speech:item.speechLocale||""}});
 LANGS=next;
 ["from","to","entry-language"].forEach(id=>{
  const select=$(id),previous=select.value;
  select.replaceChildren();
  active.forEach(item=>{const option=document.createElement("option");option.value=item.code;option.textContent=item.name;select.append(option)});
  if(active.some(item=>item.code===previous))select.value=previous;
  else select.value=id==="from"?(active.some(item=>item.code==="soninke")?"soninke":active[0].code):id==="to"?(active.some(item=>item.code==="fr")?"fr":active[0].code):active[0].code;
 });
 const fields=$("translation-fields");fields.replaceChildren();
 active.forEach(item=>{
  const label=document.createElement("label");label.textContent="Traduction en "+item.name;
  const input=document.createElement("input");input.id="entry-"+item.code;input.maxLength=180;input.placeholder="Facultatif";
  label.append(input);fields.append(label);
 });
}
function loadLocal(){try{const x=JSON.parse(localStorage.getItem(KEY)||"[]");return Array.isArray(x)?x:[]}catch(_){return[]}}
function voiceAvailable(language){if(!("speechSynthesis"in window))return false;const prefix=language.split("-")[0].toLowerCase();return speechSynthesis.getVoices().some(voice=>voice.lang.toLowerCase().startsWith(prefix))}
function render(){const from=$("from").value,to=$("to").value,q=$("search").value.trim().toLocaleLowerCase(),cat=$("category").value,grammar=$("grammar-filter").value;const shown=entries.filter(e=>(!q||Object.keys(LANGS).flatMap(l=>["word","definition","example"].map(k=>val(e,l,k))).concat(e.source||"",(e.sourceExamples||[]).flatMap(x=>[x.translationClass,x.originalClass])).join(" ").toLocaleLowerCase().includes(q))&&(!cat||e.category===cat)&&(!grammar||e.grammar_category===grammar)&&val(e,from,"word"));$("entry-count").textContent=shown.length+" fiches";$("results").replaceChildren();$("empty").hidden=shown.length!==0;$("status").textContent=shown.length?"Les statuts de validation et les sources sont conservés séparément.":"Aucun résultat. Essayez une autre recherche ou ajoutez une fiche.";shown.slice(0,100).forEach(e=>{const c=document.createElement("article");c.className="word-card";const top=document.createElement("div");top.className="card-top";const tag=document.createElement("span");tag.className="tag";tag.textContent=LANGS[from].label;const state=document.createElement("span");state.className="state";state.textContent=e.status==="validated"?"Fiche validée":"À vérifier / compléter";top.append(tag,state);c.append(top);const h=document.createElement("h3");h.textContent=val(e,from,"word")||"Mot non renseigné";c.append(h);const t=document.createElement("p");t.className="translation";t.textContent=val(e,to,"word")||"Traduction à compléter";c.append(t);const d=val(e,to,"definition")||val(e,from,"definition");if(d){const p=document.createElement("p");p.className="detail";p.textContent=d;c.append(p)}const ex=val(e,to,"example")||val(e,from,"example");if(ex){const p=document.createElement("p");p.className="example";p.textContent=ex;c.append(p)}(e.sourceExamples||[]).filter(x=>x.translationClass||x.originalClass).forEach(x=>{const p=document.createElement("p");p.className="example";p.textContent="Exemple source à vérifier (langues non attribuées) : "+[x.translationClass,x.originalClass].filter(Boolean).join(" ⇄ ");c.append(p)});const row=document.createElement("div");row.className="audio-row";[...new Set([from,to])].forEach(l=>{const b=document.createElement("button");b.type="button";b.className="audio-button";const url=(e[l]||{}).audio_url;if(url){b.textContent="▶ Écouter "+LANGS[l].label;b.onclick=()=>{const a=new Audio(url);a.play().catch(()=>{$("status").textContent="Lecture impossible : vérifiez le fichier audio.";})}}else if(LANGS[l].speech&&val(e,l,"word")&&"speechSynthesis"in window){if(voiceAvailable(LANGS[l].speech)){b.textContent="🔊 Voix "+LANGS[l].label;b.onclick=()=>{const voice=speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().startsWith(LANGS[l].speech.split("-")[0].toLowerCase()));if(!voice){$("status").textContent="Aucune voix compatible installée pour "+LANGS[l].label+".";return}speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(val(e,l,"word"));u.lang=LANGS[l].speech;u.voice=voice;speechSynthesis.speak(u);$("status").textContent="Voix de synthèse du navigateur ; ce n’est pas un enregistrement natif."}}else{b.textContent="Voix "+LANGS[l].label+" indisponible";b.disabled=true}}else{b.textContent="Audio "+LANGS[l].label+" à ajouter";b.disabled=true}row.append(b)});c.append(row);const m=document.createElement("p");m.className="meta";m.textContent=(CAT[e.category]||"Autre")+(e.grammar_category?" · grammaire : "+(POS[e.grammar_category]||e.grammar_category):"")+" · audio : "+e.pronunciationStatus+" · traduction : "+e.translationStatus+(e.sourceName?" · "+e.sourceName:"")+(e.source?" · source : "+e.source:"");c.append(m);$("results").append(c)});if(shown.length>100)$("status").textContent+=" Affichage limité aux 100 premières fiches."}
let sentenceEntries=[];
function renderSentences(){
 const query=$("sentence-search").value.trim().toLocaleLowerCase(),level=$("sentence-level").value;
 const shown=sentenceEntries.filter(e=>(!query||((e.snk||"")+" "+(e.fr||"")).toLocaleLowerCase().includes(query))&&(!level||e.niveau===level));
 $("sentence-count").textContent=shown.length+" phrases";
 $("sentence-results").replaceChildren();
 $("sentence-status").textContent=shown.length?"Corpus soninké–français sourcé · licence CC BY 4.0 · exemples à consulter avec leur contexte.":"Aucun résultat dans ce corpus.";
 shown.slice(0,40).forEach(e=>{
  const card=document.createElement("article");card.className="sentence-card";
  const top=document.createElement("div");top.className="card-top";
  const tag=document.createElement("span");tag.className="tag";tag.textContent=e.niveau==="paragraphe"?"Lecture":"Phrase";
  const state=document.createElement("span");state.className="state";state.textContent="Source documentée";
  top.append(tag,state);card.append(top);
  const sh=document.createElement("h3");sh.textContent="Soninké";card.append(sh);
  const snk=document.createElement("p");snk.className="sentence-soninke";snk.textContent=e.snk||"";card.append(snk);
  const fh=document.createElement("h4");fh.textContent="Français";card.append(fh);
  const fr=document.createElement("p");fr.className="sentence-french";fr.textContent=e.fr||"";card.append(fr);
  const row=document.createElement("div");row.className="audio-row";
  const native=document.createElement("button");native.type="button";native.className="audio-button";native.textContent="Audio soninké à enregistrer";native.disabled=true;row.append(native);
  const french=document.createElement("button");french.type="button";french.className="audio-button";
  if(voiceAvailable("fr-FR")){french.textContent="🔊 Prononcer le français (synthèse)";french.onclick=()=>{const voice=speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().startsWith("fr"));if(!voice){$("sentence-status").textContent="Aucune voix française installée dans ce navigateur.";return}speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(e.fr||"");utterance.lang="fr-FR";utterance.voice=voice;speechSynthesis.speak(utterance);$("sentence-status").textContent="Synthèse vocale du français, pas un enregistrement natif."}}else{french.textContent="Voix française indisponible";french.disabled=true}
  row.append(french);card.append(row);
  const meta=document.createElement("p");meta.className="meta";meta.textContent=(e.source||"Source documentée")+" · attribution CC BY 4.0 · graphie d’origine conservée";card.append(meta);
  const link=document.createElement("a");link.href=e.sourceUrl;link.target="_blank";link.rel="noopener noreferrer";link.className="source-link";link.textContent="Voir le fichier source ↗";card.append(link);
  $("sentence-results").append(card);
 });
 if(shown.length>40)$("sentence-status").textContent+=" Affichage limité aux 40 premiers résultats ; affinez la recherche.";
}
function openForm(){$("add-panel").hidden=false;$("entry-word").focus();$("add-panel").scrollIntoView({behavior:"smooth"})}
function exportFile(name,content,type){const u=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement("a");a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)}
function exportJSON(){exportFile("langues-en-partage.json",JSON.stringify({schemaVersion:1,languages:Object.keys(LANGS),entries},null,2),"application/json;charset=utf-8")}
function exportCSV(){const cols=["id","soninke.word","soninke.audio_url","wolof.word","wolof.audio_url","fr.word","fr.definition","fr.example","en.word","en.definition","en.example","category","source","status","pronunciationStatus","translationStatus"];const quote=x=>'"'+String(x??"").replace(/"/g,'""')+'"';const rows=[cols.join(","),...entries.map(e=>cols.map(k=>{let v=e;k.split(".").forEach(p=>v=v&&v[p]);return quote(v)}).join(","))];exportFile("langues-en-partage.csv","\uFEFF"+rows.join("\r\n"),"text/csv;charset=utf-8")}
$("search").addEventListener("input",render);["from","to","category","grammar-filter"].forEach(id=>$(id).addEventListener("change",render));$("clear").onclick=()=>{$("search").value="";render()};$("show-add").onclick=openForm;$("show-add-bottom").onclick=openForm;$("close-add").onclick=()=>$("add-panel").hidden=true;$("export-json").onclick=exportJSON;$("export-csv").onclick=exportCSV;
  document.querySelectorAll(".path-action").forEach(button => button.addEventListener("click", () => { $("category").value = button.dataset.category || ""; $("search").value = ""; render(); $("explorer").scrollIntoView({behavior:"smooth", block:"start"}); }));

$("entry-form").addEventListener("submit",ev=>{ev.preventDefault();const l=$("entry-language").value,w=$("entry-word").value.trim();if(!w)return;const translations={};Object.keys(LANGS).forEach(code=>{const input=$("entry-"+code);translations[code]={word:input?input.value.trim():""}});translations[l].word=w;const e=norm({...translations,category:$("entry-category").value,source:$("entry-source").value.trim(),status:"draft",origin:"community"});const ex=$("entry-example").value.trim();if(ex)e[l].example=ex;local.push(e);entries.push(e);try{localStorage.setItem(KEY,JSON.stringify(local))}catch(_){}$("entry-form").reset();$("add-panel").hidden=true;$("from").value=l;$("search").value=w;render();$("status").textContent="Fiche enregistrée dans ce navigateur. Exportez le JSON/CSV pour partager la contribution."});
local=loadLocal();
$("sentence-search").addEventListener("input",renderSentences);
$("sentence-level").addEventListener("change",renderSentences);
fetch("data/soninke-learning-corpus.json").then(response=>{if(!response.ok)throw Error("corpus "+response.status);return response.json()}).then(data=>{sentenceEntries=Array.isArray(data.entries)?data.entries:[];renderSentences()}).catch(error=>{$("sentence-count").textContent="Corpus indisponible";$("sentence-status").textContent="Le corpus de phrases n’a pas pu être chargé ("+error.message+"). Le lexique reste utilisable."});

if("speechSynthesis"in window)speechSynthesis.addEventListener("voiceschanged",render);
Promise.all([fetch("data/soninke-lexicon.jsonl").then(r=>{if(!r.ok)throw Error("lexique "+r.status);return r.text()}),fetch("data/audio-manifest.json").then(r=>{if(!r.ok)throw Error("audio "+r.status);return r.json()}),fetch("data/trilingual-lexicon.json").then(r=>{if(!r.ok)throw Error("schéma "+r.status);return r.json()}),fetch("data/wolof-fr-dictionary.json").then(r=>{if(!r.ok)throw Error("dictionnaire wolof "+r.status);return r.json()})]).then(([txt,manifest,tri,wolofDictionary])=>{configureLanguages(tri.languages||[]);const audio=new Map((manifest.entries||[]).map(x=>[x.id,x]));entries=txt.split(/\r?\n/).filter(x=>x.trim()).map(line=>{const x=JSON.parse(line),a=audio.get(x.id);return norm({id:x.id,soninke:{word:x.word,audio_url:a&&a.audioAvailable?a.audioPath:""},source:x.source||"",status:"draft",pronunciationStatus:x.pronunciationValidated?"attested-in-project":"unverified",translationStatus:"unverified"})});const mergeEntry=x=>{const e=norm(x),i=entries.findIndex(y=>y.id===e.id||(e.origin==="external-dictionary"&&y.origin==="external-dictionary-seed"&&sameSource(y.source,e.source)));if(i>=0)entries[i]=e;else entries.push(e)};(tri.entries||[]).forEach(mergeEntry);(wolofDictionary.entries||[]).forEach(mergeEntry);local.forEach(x=>{const i=entries.findIndex(y=>y.id===x.id);if(i>=0)entries[i]=x;else entries.push(x)});render()}).catch(err=>{entries=local;render();$("status").textContent="Le lexique complet n’a pas pu être chargé ("+err.message+"). L’ajout local et l’export restent disponibles."});
})();