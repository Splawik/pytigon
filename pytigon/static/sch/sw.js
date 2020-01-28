CACHE_NAME = 'pytigon';
CACHE_PAGES =
[ /.*\/static\/.*/i,
]
CACHE_PAGES_ON_START = []

//++//

var on_install = function (event) {
        var init_cache = function () {
                var on_cache_open = function (cache) {
                        console.log ('Opened cache');
                        return cache.addAll (CACHE_PAGES_ON_START);
                };
                caches.open (CACHE_NAME).then (on_cache_open);
        };
        event.waitUntil (init_cache);
};
self.addEventListener ('install', on_install);

var on_fetch = function (event) {
    console.log(event.request.url);
    if (event.request.url.startsWith('127.0.0.2')) {
        alert("X1");
    }
    if (event.request.method === 'POST') {
      return;
    }
    var resp = function (response) {
                if (response) {
                        return response;
                }
                var fetchRequest = event.request.clone ();
                var resp2 = function (response) {
                        if (!(response) || response.status != 200 || response.type != 'basic') {
                                return response;
                        }
                        var test = false;
                        for(pos of CACHE_PAGES ) {
                            if (event.request.url.match(pos)) {
                                test = true;
                                break;
                            }
                        }
                        if(test==false) {
                            return response;
                        }
                        var responseToCache = response.clone ();
                        var on_cache_open = function (cache) {
                                cache.put (event.request, responseToCache);
                        };
                        caches.open (CACHE_NAME).then (on_cache_open);
                        return response;
                };
                return fetch (fetchRequest).then (resp2);
        };
    event.respondWith(caches.match(event.request).then(resp))
};
self.addEventListener ('fetch', on_fetch);

