const CACHE_NAME = "langues-en-partage-v1";
const CORE_ASSETS = [
  "./",
  "./index.html",
  "./apprendre.html",
  "./lexique.html",
  "./corpus.html",
  "./styles.css",
  "./corpus.css",
  "./lexique.js",
  "./corpus.js",
  "./apprendre.css",
  "./apprendre.js",
  "./manifest.webmanifest",
  "./assets/app-icon.svg",
  "./data/soninke-lexicon.jsonl",
  "./data/soninke-samples.jsonl",
  "./data/audio-manifest.json",
  "./data/trilingual-lexicon.json",
  "./data/wolof-fr-dictionary.json",
  "./data/soninke-learning-corpus.json",
  "./data/language-sources.json",
  "./data/learning-curriculum.json"
];
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())
  );
});
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key.startsWith("langues-en-partage-") && key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (request.mode === "navigate" || url.pathname.includes("/data/")) {
    event.respondWith(
      fetch(request).then(response => {
        if (!response.ok) return response;
        return caches.open(CACHE_NAME).then(cache => cache.put(request, response.clone())).then(() => response);
      }).catch(() => caches.match(request).then(cached => cached || (request.mode === "navigate" ? caches.match("./apprendre.html").then(page => page || new Response("Offline page unavailable", { status: 503 })) : new Response("Offline resource unavailable", { status: 503 }))))
    );
    return;
  }
  const updatePromise = caches.open(CACHE_NAME).then(cache => fetch(request).then(response => {
    if (!response.ok) return response;
    return cache.put(request, response.clone()).then(() => response);
  }));
  event.waitUntil(updatePromise.catch(() => {}));
  event.respondWith(
    caches.match(request).then(cached => cached || updatePromise.catch(() => new Response("Offline resource unavailable", { status: 503 })))
  );
});