CACHE_NAME = 'PYTIGON_';

// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();

var filesToCache = [
    '/offline/',
    '/static/css/django-pwa-app.css',
    '/static/images/pytigon.png',
];


// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                var files_to_cache = [];
                var l = location.pathname.split('/')
                if (l.length>2) {
                    for(item of filesToCache) {
                        files_to_cache.push("/"+l[1]+item)
                    }
                }
                else {
                    files_to_cache = filesToCache;
                }
                return cache.addAll(files_to_cache);
            })
    )
});


// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});
