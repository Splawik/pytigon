var __name__ = '__main__';
var sync_tables = function (after_sync_fun) {
	var on_open_database = function (db) {
		var complete = function (responseText, table_name) {
			var lp = 0;
			var x = JSON.parse (responseText);
			console.log ('Success opening DB');
			var tabObjectStore = db.transaction (table_name, 'readwrite').objectStore (table_name);
			var clear_request = tabObjectStore.clear ();
			var _clearsuccess = function (event) {
				var __iterable0__ = x;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var pos = __iterable0__ [__index0__];
					if (table_name == 'kar') {
						var obj = dict ({'symkar': pos [4], 'path': pos [0], 'pathopis': pos [1], 'grupa': pos [2], 'opisgrupy': pos [3], 'opikar': pos [5]});
					}
					if (table_name == 'mag') {
						var obj = dict ({'mag': pos [0], 'opismag': pos [1], 'symodd': pos [2]});
					}
					if (table_name == 'tkw') {
						var obj = dict ({'symkary': pos [0], 'sur': pos [1], 'rob': pos [2], 'adm': pos [3], 'zmien': pos [4], 'amort': pos [5], 'kosztmag': pos [6]});
					}
					if (table_name == 'przel') {
						var obj = dict ({'symkar': pos [0], 'waga': pos [1], 'mprzel': pos [2]});
					}
					tabObjectStore.add (obj);
				}
				lp++;
				if (lp == 4) {
					after_sync_fun ();
				}
			};
			clear_request.onsuccess = _clearsuccess;
		};
		var _complete = function (table_name) {
			var _complete2 = function (responseText) {
				return complete (responseText, table_name);
			};
			return _complete2;
		};
		ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/0/', _complete ('kar'));
		ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/1/', _complete ('mag'));
		ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/2/', _complete ('tkw'));
		ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/3/', _complete ('przel'));
	};
	open_database (on_open_database);
};
