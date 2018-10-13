var __name__ = '__main__';
var _sync_elem = function (resolve, reject) {
	var props = list (['rec']);
	var data = function () {
		return dict ({'status': 0});
	};
	var template = '<div>xxx{{status}}yyy</div>';
	var mounted = function () {
		var vue_obj = this;
		console.log ('X1');
		var on_open_database = function (db) {
			console.log ('X2');
			var complete = function (responseText, table_name) {
				var x = JSON.parse (responseText);
				vue_obj.status = vue_obj.status + 1;
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
	resolve (dict ({'data': data, 'template': template, 'mounted': mounted}));
};
Vue.component ('sync_elem', _sync_elem);
