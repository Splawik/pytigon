	__nest__ (
		__all__,
		'db', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'db';
					var INIT_DB_STRUCT = null;
					var init_db = function (struct) {
						INIT_DB_STRUCT = struct;
					};
					window.init_db = init_db;
					var open_database = function (on_open) {
						if (!(window.indexedDB)) {
							console.log ('Your Browser does not support IndexedDB');
						}
						else {
							var request = window.indexedDB.open (window.PRJ_NAME, 1);
							var _onerror = function (event) {
								console.log ('Error opening DB', event);
							};
							request.onerror = _onerror;
							var _onupgradeneeded = function (event) {
								console.log ('Upgrading');
								var db = event.target.result;
								var objectStore = db.createObjectStore ('param', dict ({'keyPath': 'key'}));
								if (INIT_DB_STRUCT) {
									var __iterable0__ = INIT_DB_STRUCT;
									for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
										var pos = __iterable0__ [__index0__];
										var objectStore = db.createObjectStore (pos [0], pos [1]);
									}
								}
							};
							request.onupgradeneeded = _onupgradeneeded;
							var _onsuccess = function (event) {
								var db = event.target.result;
								on_open (db);
							};
							request.onsuccess = _onsuccess;
						}
					};
					window.open_database = open_database;
					var get_table = function (table_name, on_open, read_only) {
						if (typeof read_only == 'undefined' || (read_only != null && read_only .hasOwnProperty ("__kwargtrans__"))) {;
							var read_only = true;
						};
						var _on_open = function (db) {
							if (read_only == true) {
								var mode = 'readonly';
							}
							else {
								var mode = 'readwrite';
							}
							var tabTrans = db.transaction (table_name, mode);
							var tabObjectStore = tabTrans.objectStore (table_name);
							on_open (tabTrans, tabObjectStore);
						};
						open_database (_on_open);
					};
					window.get_table = get_table;
					var get_list_from_table = function (table, on_open_list) {
						var on_open = function (trans, table) {
							var py_items = list ([]);
							var oncomplete = function (evt) {
								on_open_list (py_items);
							};
							trans.oncomplete = oncomplete;
							var cursor_request = table.openCursor ();
							var onerror = function (error) {
								console.log (error);
							};
							cursor_request.onerror = onerror;
							var onsuccess = function (evt) {
								var cursor = evt.target.result;
								if (cursor) {
									py_items.push (cursor.value);
									cursor.continue ();
								}
							};
							cursor_request.onsuccess = onsuccess;
						};
						get_table (table, on_open);
					};
					window.get_list_from_table = get_list_from_table;
					var on_sys_sync = function (fun) {
						var _fun = function (cache_deleted) {
							if (cache_deleted) {
								fun ('OK-refresh');
							}
							else {
								fun ('OK-no cache');
							}
						};
						caches.delete ('PYTIGON_' + window.PRJ_NAME).then (_fun);
					};
					var _UA = window.navigator.userAgent;
					var _MSIE = _UA.indexOf ('MSIE ');
					var _MSIE2 = _UA.indexOf ('Trident/');
					if (_MSIE > 0 || _MSIE2 > 0) {
						var SYNC_STRUCT = list ([]);
					}
					else {
						var SYNC_STRUCT = list ([list (['sys', window.BASE_PATH + 'schsys/app_time_stamp/', on_sys_sync])]);
					}
					var init_sync = function (sync_struct) {
						var __iterable0__ = sync_struct;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var pos = __iterable0__ [__index0__];
							SYNC_STRUCT.append (pos);
						}
					};
					window.init_sync = init_sync;
					var sync_and_run = function (tbl, fun) {
						var rec = null;
						var __iterable0__ = SYNC_STRUCT;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var pos = __iterable0__ [__index0__];
							if (pos [0] == tbl) {
								var rec = pos;
								break;
							}
						}
						if (!(rec)) {
							fun ('error - no reg function');
							return ;
						}
						if (navigator.onLine) {
							var complete = function (responseText) {
								var _on_open_param = function (trans, db) {
									var param_get_request = db.get ('time_sync_' + tbl);
									var _on_param_error = function (event) {
										rec [2] (fun);
										db.add (dict ({'key': 'time_sync_' + tbl, 'value': time}));
									};
									var _on_param_success = function (event) {
										var param = param_get_request.result;
										if (param) {
											var time2 = param.value;
											if (time2 < time) {
												param.value = time;
												var param_update_request = db.put (param);
												var _on_update = function (event) {
													rec [2] (fun);
												};
												param_update_request.onerror = _on_update;
												param_update_request.onsuccess = _on_update;
											}
											else {
												fun ('OK');
											}
										}
										else {
											var param_add_request = db.add (dict ({'key': 'time_sync_' + tbl, 'value': time}));
											var _on_add_success = function (event) {
												rec [2] (fun);
											};
											var _on_add_error = function (event) {
												rec [2] (fun);
											};
											param_add_request.onerror = _on_add_error;
											param_add_request.onsuccess = _on_add_success;
										}
									};
									param_get_request.onerror = _on_param_error;
									param_get_request.onsuccess = _on_param_success;
								};
								try {
									var x = JSON.parse (responseText);
									var time = x ['TIME'];
									get_table ('param', _on_open_param, false);
								}
								catch (__except0__) {
									console.log (responseText);
									window.open ().document.write (responseText);
								}
							};
							var _on_request_init = function (request) {
								var _on_timeout = function (event) {
									fun ('timeout');
								};
								try {
									request.timeout = 2000;
								}
								catch (__except0__) {
									// pass;
								}
								request.ontimeout = _on_timeout;
							};
							ajax_get (rec [1], complete, _on_request_init);
						}
						else {
							fun ('offline');
						}
					};
					window.sync_and_run = sync_and_run;
					__pragma__ ('<all>')
						__all__.INIT_DB_STRUCT = INIT_DB_STRUCT;
						__all__.SYNC_STRUCT = SYNC_STRUCT;
						__all__._MSIE = _MSIE;
						__all__._MSIE2 = _MSIE2;
						__all__._UA = _UA;
						__all__.__name__ = __name__;
						__all__.get_list_from_table = get_list_from_table;
						__all__.get_table = get_table;
						__all__.init_db = init_db;
						__all__.init_sync = init_sync;
						__all__.on_sys_sync = on_sys_sync;
						__all__.open_database = open_database;
						__all__.sync_and_run = sync_and_run;
					__pragma__ ('</all>')
				}
			}
		}
	);
