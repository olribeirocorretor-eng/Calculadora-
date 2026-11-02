/* Service worker da calculadora SINDMUNICIPAIS.
 * Ao alterar index.html ou outros arquivos do app, aumente VERSAO
 * para que os aparelhos baixem a versão nova. */
const VERSAO = 'v3';
const CACHE_APP = `sindmunicipais-app-${VERSAO}`;
const CACHE_FONTES = 'sindmunicipais-fontes';

const ARQUIVOS_APP = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/maskable-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_APP)
      .then((cache) => cache.addAll(ARQUIVOS_APP))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((nomes) => Promise.all(
        nomes
          .filter((nome) => nome.startsWith('sindmunicipais-app-') && nome !== CACHE_APP)
          .map((nome) => caches.delete(nome))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // A calculadora comemorativa (pasta registro/) tem o próprio service worker.
  if (url.pathname.startsWith(new URL('./registro/', self.registration.scope).pathname)) return;

  // Página: tenta a rede primeiro (para pegar atualizações) e usa o cache sem internet.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((resposta) => {
          const copia = resposta.clone();
          caches.open(CACHE_APP).then((cache) => cache.put('./index.html', copia));
          return resposta;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Fonte Archivo (Google Fonts): usa o cache e atualiza em segundo plano.
  if (url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com') {
    event.respondWith(
      caches.open(CACHE_FONTES).then((cache) =>
        cache.match(request).then((emCache) => {
          const daRede = fetch(request)
            .then((resposta) => {
              if (resposta.ok || resposta.type === 'opaque') cache.put(request, resposta.clone());
              return resposta;
            })
            .catch(() => emCache);
          return emCache || daRede;
        })
      )
    );
    return;
  }

  // Demais arquivos do próprio site: cache primeiro, rede como reserva.
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(request).then((emCache) => emCache || fetch(request).then((resposta) => {
        if (resposta.ok) {
          const copia = resposta.clone();
          caches.open(CACHE_APP).then((cache) => cache.put(request, copia));
        }
        return resposta;
      }))
    );
  }
});
