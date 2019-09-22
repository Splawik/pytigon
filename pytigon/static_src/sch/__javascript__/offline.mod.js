	__nest__ (
		__all__,
		'offline', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'offline';
					var install_service_worker = function () {
						if (hasattr (navigator, 'serviceWorker')) {
							var reg = function (registration) {
								if (registration.installing) {
									var serviceWorker = registration.installing;
								}
								else if (registration.waiting) {
									var serviceWorker = registration.waiting;
								}
								else if (registration.active) {
									var serviceWorker = registration.active;
								}
								if (serviceWorker) {
									console.log (serviceWorker.state);
									var onstatechange = function (e) {
										console.log (e.target.state);
									};
									serviceWorker.addEventListener ('statechange', onstatechange);
								}
							};
							var err = function (error) {
								console.log (error);
							};
							navigator.serviceWorker.register (BASE_PATH + 'sw.js').then (reg).catch (err);
						}
						else {
							console.log ("The current browser doesn't support service workers");
						}
					};
					var service_worker_and_indexedDB_test = function () {
						if (hasattr (navigator, 'serviceWorker') && hasattr (window, 'indexedDB') && (location.hostname == 'localhost' || location.hostname == '127.0.0.1' || location.protocol == 'https:')) {
							return true;
						}
						else {
							return false;
						}
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.install_service_worker = install_service_worker;
						__all__.service_worker_and_indexedDB_test = service_worker_and_indexedDB_test;
					__pragma__ ('</all>')
				}
			}
		}
	);
