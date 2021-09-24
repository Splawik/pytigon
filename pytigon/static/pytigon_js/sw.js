CACHE_NAME = 'pytigon';
CACHE_PAGES = [/.*\/static\/.*/i, ]
CACHE_PAGES_ON_START = []

//++//

var on_install = function(event) {
    var init_cache = function() {
        var on_cache_open = function(cache) {
            console.log('Opened cache');
            return cache.addAll(CACHE_PAGES_ON_START);
        };
        caches.open(CACHE_NAME).then(on_cache_open);
    };
    event.waitUntil(init_cache);
};
self.addEventListener('install', on_install);

var on_fetch = function(event) {
    console.log(event.request.url);
    if (event.request.url.startsWith('127.0.0.2')) {
        alert("X1");
    }
    if (event.request.method === 'POST') {
        return;
    }
    var resp = function(response) {
        if (response) {
            return response;
        }
        var fetchRequest = event.request.clone();
        var resp2 = function(response) {
            if (!(response) || response.status != 200 || response.type != 'basic') {
                return response;
            }
            var test = false;
            for (pos of CACHE_PAGES) {
                if (event.request.url.match(pos)) {
                    test = true;
                    break;
                }
            }
            if (test == false) {
                return response;
            }
            var responseToCache = response.clone();
            var on_cache_open = function(cache) {
                cache.put(event.request, responseToCache);
            };
            caches.open(CACHE_NAME).then(on_cache_open);
            return response;
        };
        return fetch(fetchRequest).then(resp2);
    };
    event.respondWith(caches.match(event.request).then(resp))
};
self.addEventListener('fetch', on_fetch);

function run_db_fun(callback_fun, parameters) {
    open_request = indexedDB.open("pytigon_service_db", 1);

    function onupgradeneeded() {
        db = open_request.result
        if (!db.objectStoreNames.contains('pytigon_databases')) {
            db.createObjectStore('pytigon_databases', {
                'keyPath': 'id'
            })
        }
    }
    open_request.onupgradeneeded = onupgradeneeded;

    function onsuccess(event) {
        db = event.target.result;
        callback_fun(db, parameters);
    }
    open_request.onsuccess = onsuccess;
}

function save_to_db(key, value) {
    function _save(db, tab) {
        transaction = db.transaction('pytigon_databases', 'readwrite');
        dbs = transaction.objectStore('pytigon_databases');
        request = dbs.put({
            id: tab[0],
            data: tab[1]
        });

        function onsuccess() {
            console.log("DB saved: ", request.result);
        }
        request.onsuccess = onsuccess;

        function onerror() {
            console.log("DB saved: ", request.result);
        }
        request.onerror = onerror;
    }
    run_db_fun(_save, [key, value]);
}


function get_from_db(key, callback) {
    function _get(db, tab) {
        transaction = db.transaction('pytigon_databases');
        dbs = transaction.objectStore('pytigon_databases');
        request = dbs.get(tab[0]);

        function onsuccess(event) {
            value = event.target.result;
            tab[1](value);
        }
        request.onsuccess = onsuccess;

        function onerror() {
            tab[1](None);
        }
        request.onerror = onerror
    }
    run_db_fun(_get, [key, callback]);
}

function message(event) {
    if (event.data && event.data.type == 'get_state') {
        function _post_message_to_client(clients) {
            if (clients && clients.length) {
                function _callback(data) {
                    clients[0].postMessage({
                        type: 'get_state',
                        data: data
                    });
                }
                get_from_db(event.data.name, _callback);
            }
        }
        self.clients.matchAll({
            'includeUncontrolled': true,
            'type': 'window'
        }).then(_post_message_to_client)
    }
    if (event.data.type == 'set_state') {
        save_to_db(event.data.name, event.data.data);
    }

}

self.addEventListener('message', message)