var __name__ = '__main__';
var TEMPLATE = '        <div class=\"card\" v-bind:style=\"{ width: \'22rem\', float:\'left\', margin: \'0.2rem\' }\">\n' +
    '                <div class=\"card-header\" v-bind:style=\"{ height: \'3rem\' }\">\n' +
    '                        {{title}}\n' +
    '                        <button v-if=\"copybutton\" v-on:click=\"$emit(\'copy\')\" v-bind:style=\"{ float: \'right\' }\"> = &gt</button>\n' +
    '                </div>\n' +
    '                <div class=\"card-block\">\n' +
    '                        <div>Grupa asortymentowa:</div>\n' +
    '                        <select v-model=\"category1value\" v-on:change=\"changetab1(0)\" v-bind:style=\"{ width: \'300px\', paddingRight: \'20px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\">\n' +
    '                                <option v-for=\"v in get_unique_values_from_list(category1array, 0)\" v-bind:value=\"v\">{{v}}</option>\n' +
    '                        </select>\n' +
    '                        <div>Grupa cennikowa:</div>\n' +
    '                        <select v-model=\"category2value\" v-on:change=\"changetab2(1)\" v-bind:style=\"{ width: \'300px\', paddingRight: \'20px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\">\n' +
    '                                <option v-for=\"v in get_unique_values_from_list(category2array,1)\" v-bind:value=\"v\">{{v}}</option>\n' +
    '                        </select>\n' +
    '                        <div>Nazwa produktu:</div>\n' +
    '                        <select v-model=\"category3value\" v-on:change=\"changetab3(2)\" v-bind:style=\"{ width: \'300px\', paddingRight: \'20px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\">\n' +
    '                                <option v-for=\"v in get_unique_values_from_list(category3array,2)\" v-bind:value=\"v\">{{v}}</option>\n' +
    '                        </select>\n' +
    '                        <div>Lokalizacja:</div>\n' +
    '                        <select v-model=\"lokalizacja\" v-bind:style=\"{ width: \'300px\', paddingRight: \'20px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\">\n' +
    '                                <option v-for=\"v in mag\" v-bind:value=\"v[0]\">{{v[1]}}{{v}}</option>\n' +
    '                        </select>\n' +
    '                        <div v-bind:style=\"{ width: \'75px\', float: \'left\' }\">\n' +
    '                                Ilość/sam:\n' +
    '                                <input v-model=\"il_na_sam\" v-bind:style=\"{ width: \'60px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\" />\n' +
    '                        </div>\n' +
    '                        <div v-bind:style=\"{ width: \'75px\', float: \'left\' }\">\n' +
    '                                Cena lb:\n' +
    '                                <input v-model=\"cena\" v-bind:style=\"{ width: \'60px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\" />\n' +
    '                        </div>\n' +
    '                        <div v-bind:style=\"{ width: \'75px\', float: \'left\' }\">\n' +
    '                                Koszt sam.:\n' +
    '                                <input v-model=\"koszt\" v-bind:style=\"{ width: \'60px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\" />\n' +
    '                        </div>\n' +
    '                        <div v-bind:style=\"{ width: \'75px\', float: \'left\' }\">\n' +
    '                                Liczba sam.:\n' +
    '                                <input v-model=\"liczba_sam\" v-bind:style=\"{ width: \'60px\', marginBottom: \'0.4rem\', fontSize: \'12px\' }\" />\n' +
    '                        </div>\n' +
    '                        <span>\n' +
    '                                <calculation v-bind:rec=\"ret\" v-bind:lokalizacja=\"lokalizacja\" v-bind:il_na_sam=\"il_na_sam\" v-bind:cena=\"cena\" v-bind:koszt=\"koszt\" v-bind:liczba_sam=\"liczba_sam\"></calculation>\n' +
    '                        </span>\n' +
    '                </div>\n' +
    '        </div>\n' +
    '\n' +
    '';
var TEMPLATE2 = '        <div>\n' +
    '                {{sync}}\n' +
    '                <table class=\"table table-sm\">\n' +
    '                        <tr>\n' +
    '                                <th>Waga ładunku/sam.:</th>\n' +
    '                                <td>{{waga_sam}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Łączna waga ładunku:</th>\n' +
    '                                <td>{{waga}}</td>\n' +
    '                        </tr>\n' +
    '                </table>\n' +
    '                <table class=\"table table-sm\">\n' +
    '                        <tr>\n' +
    '                                <th></th>\n' +
    '                                <th>Jednostkowo</th>\n' +
    '                                <th>Ogółem</th>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Koszt transportu</th>\n' +
    '                                <td>{{koszt_transp_0}}</td>\n' +
    '                                <td>{{koszt_transp_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Surowce</th>\n' +
    '                                <td>{{surowce_0}}</td>\n' +
    '                                <td>{{surowce_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Robocizna</th>\n' +
    '                                <td>{{robocizna_0}}</td>\n' +
    '                                <td>{{robocizna_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Koszty bezpośrednie</th>\n' +
    '                                <td>{{koszty_bezp_0}}</td>\n' +
    '                                <td>{{koszty_bezp_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Koszty magazynów</th>\n' +
    '                                <td>{{koszty_mag_0}}</td>\n' +
    '                                <td>{{koszty_mag_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>KOSZTY 1A</th>\n' +
    '                                <td>{{koszty_1a_0}}</td>\n' +
    '                                <td>{{koszty_1a_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>MARŻA 1A</th>\n' +
    '                                <td>{{marza_1a_0}}</td>\n' +
    '                                <td>{{marza_1a_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Administracja</th>\n' +
    '                                <td>{{administracja_0}}</td>\n' +
    '                                <td>{{administracja_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Amortyzacja</th>\n' +
    '                                <td>{{amortyzacja_0}}</td>\n' +
    '                                <td>{{amortyzacja_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>Koszty łącznie</th>\n' +
    '                                <td>{{koszty_razem_0}}</td>\n' +
    '                                <td>{{koszty_razem_1}}</td>\n' +
    '                        </tr>\n' +
    '                        <tr>\n' +
    '                                <th>MARŻA 2</th>\n' +
    '                                <td>{{marza_2_0}}</td>\n' +
    '                                <td>{{marza_2_1}}</td>\n' +
    '                        </tr>\n' +
    '                </table>\n' +
    '        </div>\n' +
    '\n' +
    '';
var TEMPLATE3 = '        <div>\n' +
    '                <select_elem title=\"Opcja 1\" v-bind:copybutton=\"1\" v-on:copy=\"on_copy(0)\"></select_elem>\n' +
    '                <select_elem title=\"Opcja 2\" v-bind:copybutton=\"1\" v-on:copy=\"on_copy(1)\"></select_elem>\n' +
    '                <select_elem title=\"Opcja 3\" v-bind:copybutton=\"1\" v-on:copy=\"on_copy(2)\"></select_elem>\n' +
    '                <select_elem title=\"Opcja 4\" v-bind:copybutton=\"0\"></select_elem>\n' +
    '        </div>\n' +
    '\n' +
    '';
var float_from_str = function (parm) {
	return parseFloat (parm);
};
var _calculation = function (resolve, reject) {
	var props = list (['rec', 'lokalizacja', 'il_na_sam', 'cena', 'koszt', 'liczba_sam']);
	var data = function () {
		return dict ({'waga': '', 'waga_sam': '', 'koszt_transp_0': '', 'koszt_transp_1': '', 'surowce_0': '', 'surowce_1': '', 'robocizna_0': '', 'robocizna_1': '', 'koszty_bezp_0': '', 'koszty_bezp_1': '', 'koszty_mag_0': '', 'koszty_mag_1': '', 'koszty_1a_0': '', 'koszty_1a_1': '', 'marza_1a_0': '', 'marza_1a_1': '', 'administracja_0': '', 'administracja_1': '', 'amortyzacja_0': '', 'amortyzacja_1': '', 'koszty_razem_0': '', 'koszty_razem_1': '', 'marza_2_0': '', 'marza_2_1': ''});
	};
	var sync = function () {
		if (len (this.rec) > 0 && this.lokalizacja != '' && this.il_na_sam != '' && this.cena != '' && this.koszt != '' && this.liczba_sam != '') {
			var symkar = this.rec [0] [3];
			var cur_date = new Date ();
			var cur_year = cur_date.getFullYear ();
			var symkar2 = (((str (cur_year) + '/') + this.lokalizacja) + '/') + symkar;
			var vue_obj = this;
			var _on_open_przel = function (tabTrans, przel_tab) {
				var przel_get_request = przel_tab.get (symkar);
				var _on_przel_error = function (event) {
					console.log ('Brak przelicznika');
				};
				var _on_przel_success = function (event) {
					var przel = przel_get_request.result;
					var _on_open_tkw = function (tabTrans2, tkw_tab) {
						var tkw_get_request = tkw_tab.get (symkar2);
						var _on_tkw_error = function (event) {
							console.log ('Brak TKW');
						};
						var _on_tkw_success = function (event) {
							var tkw = tkw_get_request.result;
							var il_na_sam = parseFloat (vue_obj.il_na_sam);
							var cena = parseFloat (vue_obj.cena);
							var koszt_sam = parseFloat (vue_obj.koszt);
							var liczba_sam = parseFloat (vue_obj.liczba_sam);
							var prz = przel.mprzel;
							vue_obj.waga = ((il_na_sam * przel.waga) * liczba_sam).toFixed (2);
							vue_obj.waga_sam = (il_na_sam * przel.waga).toFixed (2);
							if (tkw && przel) {
								vue_obj.koszt_transp_0 = (koszt_sam / il_na_sam).toFixed (2);
								vue_obj.koszt_transp_1 = (koszt_sam * liczba_sam).toFixed (2);
								vue_obj.surowce_0 = (prz * tkw.sur).toFixed (2);
								vue_obj.surowce_1 = (((prz * tkw.sur) * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.robocizna_0 = (prz * tkw.rob).toFixed (2);
								vue_obj.robocizna_1 = (((prz * tkw.rob) * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.koszty_bezp_0 = (prz * tkw.zmien).toFixed (2);
								vue_obj.koszty_bezp_1 = (((prz * tkw.zmien) * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.koszty_mag_0 = (prz * tkw.kosztmag).toFixed (2);
								vue_obj.koszty_mag_1 = (((prz * tkw.kosztmag) * il_na_sam) * liczba_sam).toFixed (2);
								var koszty_1a = koszt_sam / il_na_sam + prz * (((tkw.sur + tkw.rob) + tkw.zmien) + tkw.kosztmag);
								vue_obj.koszty_1a_0 = koszty_1a.toFixed (2);
								vue_obj.koszty_1a_1 = ((koszty_1a * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.marza_1a_0 = (cena - koszty_1a).toFixed (2);
								vue_obj.marza_1a_1 = (((cena - koszty_1a) * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.administracja_0 = (prz * tkw.adm).toFixed (2);
								vue_obj.administracja_1 = (((prz * tkw.adm) * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.amortyzacja_0 = (prz * tkw.amort).toFixed (2);
								vue_obj.amortyzacja_1 = (((prz * tkw.amort) * il_na_sam) * liczba_sam).toFixed (2);
								var koszty_razem = koszty_1a + prz * (tkw.adm + tkw.amort);
								vue_obj.koszty_razem_0 = koszty_razem.toFixed (2);
								vue_obj.koszty_razem_1 = ((koszty_razem * il_na_sam) * liczba_sam).toFixed (2);
								vue_obj.marza_2_0 = (cena - koszty_razem).toFixed (2);
								vue_obj.marza_2_1 = (((cena - koszty_razem) * il_na_sam) * liczba_sam).toFixed (2);
							}
							else {
								vue_obj.koszt_transp_0 = 'B/D';
								vue_obj.koszt_transp_1 = 'B/D';
								vue_obj.surowce_0 = 'B/D';
								vue_obj.surowce_1 = 'B/D';
								vue_obj.robocizna_0 = 'B/D';
								vue_obj.robocizna_1 = 'B/D';
								vue_obj.koszty_bezp_0 = 'B/D';
								vue_obj.koszty_bezp_1 = 'B/D';
								vue_obj.koszty_mag_0 = 'B/D';
								vue_obj.koszty_mag_1 = 'B/D';
								vue_obj.koszty_1a_0 = 'B/D';
								vue_obj.koszty_1a_1 = 'B/D';
								vue_obj.marza_1a_0 = 'B/D';
								vue_obj.marza_1a_1 = 'B/D';
								vue_obj.administracja_0 = 'B/D';
								vue_obj.administracja_1 = 'B/D';
								vue_obj.amortyzacja_0 = 'B/D';
								vue_obj.amortyzacja_1 = 'B/D';
								vue_obj.koszty_razem_0 = 'B/D';
								vue_obj.koszty_razem_1 = 'B/D';
								vue_obj.marza_2_0 = 'B/D';
								vue_obj.marza_2_1 = 'B/D';
							}
						};
						tkw_get_request.onerror = _on_tkw_error;
						tkw_get_request.onsuccess = _on_tkw_success;
					};
					get_table ('tkw', _on_open_tkw);
				};
				przel_get_request.onerror = _on_przel_error;
				przel_get_request.onsuccess = _on_przel_success;
			};
			get_table ('przel', _on_open_przel);
			return '1';
		}
		else {
			this.waga = '';
			this.waga_sam = '';
			this.koszt_transp_0 = '';
			this.koszt_transp_1 = '';
			this.surowce_0 = '';
			this.surowce_1 = '';
			this.robocizna_0 = '';
			this.robocizna_1 = '';
			this.koszty_bezp_0 = '';
			this.koszty_bezp_1 = '';
			this.koszty_mag_0 = '';
			this.koszty_mag_1 = '';
			this.koszty_1a_0 = '';
			this.koszty_1a_1 = '';
			this.marza_1a_0 = '';
			this.marza_1a_1 = '';
			this.administracja_0 = '';
			this.administracja_1 = '';
			this.amortyzacja_0 = '';
			this.amortyzacja_1 = '';
			this.koszty_razem_0 = '';
			this.koszty_razem_1 = '';
			this.marza_2_0 = '';
			this.marza_2_1 = '';
			return '0';
		}
	};
	var computed = dict ({'sync': sync});
	var template = TEMPLATE2;
	resolve (dict ({'props': props, 'data': data, 'computed': computed, 'template': template}));
};
Vue.component ('calculation', _calculation);
var _select_elem = function (resolve, reject) {
	var props = list (['lp', 'category1id', 'category2id', 'category3id', 'title', 'copybutton']);
	var data = function () {
		return dict ({'category1value': '', 'category2value': '', 'category2array': list ([]), 'category3value': '', 'category3array': list ([]), 'ret': list ([]), 'il_na_sam': '', 'cena': '', 'koszt': '', 'liczba_sam': '', 'category1array': list ([]), 'mag': list ([]), 'lokalizacja': ''});
	};
	var methods = function () {
		var changetab1 = function (id) {
			this.category2array = list ([]);
			this.category2value = '';
			this.category3value = '';
			this.ret = list ([]);
			var __iterable0__ = this.category1array;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var pos = __iterable0__ [__index0__];
				if (pos [id] == this.category1value) {
					this.category2array.push (pos);
				}
			}
		};
		var changetab2 = function (id) {
			this.category3array = list ([]);
			this.category3value = '';
			this.ret = list ([]);
			var __iterable0__ = this.category2array;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var pos = __iterable0__ [__index0__];
				if (pos [id] == this.category2value) {
					this.category3array.push (pos);
				}
			}
		};
		var changetab3 = function (id) {
			this.ret = list ([]);
			var __iterable0__ = this.category3array;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var pos = __iterable0__ [__index0__];
				if (pos [id] == this.category3value) {
					this.ret.push (pos);
				}
			}
		};
		var get_unique_values_from_list = function (lst, list_id) {
			var ret = list ([]);
			var __iterable0__ = lst;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var pos = __iterable0__ [__index0__];
				if (!(__in__ (pos [list_id], ret))) {
					ret.push (pos [list_id]);
				}
			}
			return ret;
		};
		return dict ({'changetab1': changetab1, 'changetab2': changetab2, 'changetab3': changetab3, 'get_unique_values_from_list': get_unique_values_from_list, 'copy': copy});
	};
	var template = TEMPLATE;
	var mounted = function () {
		var vue_obj = this;
		var on_open_kar = function (py_items) {
			vue_obj.category1array = list ([]);
			var __iterable0__ = py_items;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var item = __iterable0__ [__index0__];
				vue_obj.category1array.append (list ([item.pathopis, item.opisgrupy, item.opikar, item.symkar]));
			}
		};
		get_list_from_table ('kar', on_open_kar);
		var on_open_mag = function (py_items) {
			vue_obj.mag = list ([]);
			var __iterable0__ = py_items;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var item = __iterable0__ [__index0__];
				vue_obj.mag.append (list ([item.mag, item.opismag]));
			}
		};
		get_list_from_table ('mag', on_open_mag);
	};
	resolve (dict ({'props': props, 'data': data, 'methods': methods (), 'template': template, 'mounted': mounted}));
};
Vue.component ('select_elem', _select_elem);
var _select_contener = function (resolve, reject) {
	var on_copy = function (id) {
		var source = this.$children [id];
		var dest = this.$children [id + 1];
		dest.category1value = source.category1value;
		dest.changetab1 (0);
		dest.category2value = source.category2value;
		dest.changetab2 (1);
		dest.category3value = source.category3value;
		dest.changetab3 (2);
		dest.lokalizacja = source.lokalizacja;
		dest.il_na_sam = source.il_na_sam;
		dest.cena = source.cena;
		dest.koszt = source.koszt;
		dest.liczba_sam = source.liczba_sam;
		console.log ('COPY!!!');
		console.log (event);
	};
	var _resolve = function () {
		resolve (dict ({'template': TEMPLATE3, 'methods': dict ({'on_copy': on_copy})}));
	};
	sync_and_run ('alltab', _resolve);
};
Vue.component ('select_contener', _select_contener);
