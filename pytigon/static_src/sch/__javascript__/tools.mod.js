	__nest__ (
		__all__,
		'tools', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tools';
					var LOADED_FILES = dict ({});
					var FIRST_INIT = true;
					var FRAGMENT_INIT_FUN = list ([]);
					var register_fragment_init_fun = function (fun) {
						FRAGMENT_INIT_FUN.append (fun);
					};
					var fragment_init = function (elem) {
						if (typeof elem == 'undefined' || (elem != null && elem .hasOwnProperty ("__kwargtrans__"))) {;
							var elem = null;
						};
						if (elem) {
							var elem2 = elem;
						}
						else {
							var elem2 = window.ACTIVE_PAGE.page;
						}
						var format = dict ({'singleDatePicker': true, 'showDropdowns': true, 'buttonClasses': 'btn', 'applyClass': 'btn-success align-top', 'cancelClass': 'btn-danger btn-sm align-top', 'timePicker24Hour': true, 'autoApply': true, 'locale': dict ({'format': 'YYYY-MM-DD', 'separator': '-', 'applyLabel': '&nbsp; OK &nbsp;', 'cancelLabel': "<i class='fa fa-close'></i>"})});
						var d = elem2.find ('div.form-group .datefield input');
						d.daterangepicker (format);
						format ['locale'] ['format'] = 'YYYY-MM-DD HH:mm';
						format ['timePicker'] = true;
						format ['timePickerIncrement'] = 30;
						var d = elem2.find ('div.form-group .datetimefield input');
						d.daterangepicker (format);
						jQuery ('.selectpicker').selectpicker ();
						var _on_blur = function (e) {
							if (e ['type'] == 'focus' || this.value.length > 0) {
								var test = true;
							}
							else {
								var test = false;
							}
							jQuery (this).parents ('.form-group').toggleClass ('focused', test);
						};
						elem2.find ('.label-floating .form-control').on ('focus blur', _on_blur).trigger ('blur');
						var load_inline_frame = function () {
							var frame = jQuery (this);
							frame.append (INLINE_FRAME_HTML);
							var obj2 = frame.find ('div.frame-data-inner');
							if (obj2.length > 0) {
								var url = frame.attr ('href');
								var complete = function (txt) {
									// pass;
								};
								ajax_load (obj2, url, complete);
							}
						};
						elem2.find ('.inline_frame').each (load_inline_frame);
						elem2.find ('.django-select2:not(.select2-full-width)').djangoSelect2 (dict ({'width': 'calc(100% - 48px)'}));
						elem2.find ('.django-select2.select2-full-width').djangoSelect2 (dict ({'width': 'calc(100%)'}));
						var init_select2_ctrl = function () {
							var sel2 = jQuery (this);
							var src = sel2.closest ('.input-group');
							if (src.length == 1) {
								if (src [0].hasAttribute ('item_id')) {
									var id = src.attr ('item_id');
									if (id) {
										var text = src.attr ('item_str');
										sel2.append (jQuery ('<option>', dict ({'value': id, 'text': text})));
										sel2.val (id.toString ());
										sel2.trigger ('change');
									}
								}
							}
						};
						elem2.find ('.django-select2').each (init_select2_ctrl);
						if (window.BASE_FRAGMENT_INIT) {
							window.BASE_FRAGMENT_INIT ();
						}
						var __iterable0__ = FRAGMENT_INIT_FUN;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var fun = __iterable0__ [__index0__];
							fun (elem2);
						}
					};
					var evalJSFromHtml = function (html) {
						var newElement = document.createElement ('div');
						newElement.innerHTML = html;
						var scripts = newElement.getElementsByTagName ('script');
						var eval_fun = function (id, value) {
							eval (value.innerHTML);
						};
						jQuery.each (scripts, eval_fun);
					};
					var evalCSSFromHtml = function (html, elem) {
						var newElement = document.createElement ('div');
						newElement.innerHTML = html;
						var css = newElement.getElementsByTagName ('style');
						while (css.length > 0) {
							var style = css.py_pop ();
							style.attr ('scoped', 'scoped');
							elem.append (style);
						}
					};
					var MOUNT_INIT_FUN = list ([]);
					var register_mount_fun = function (fun) {
						MOUNT_INIT_FUN.append (fun);
					};
					var mount_html = function (elem, html_txt, run_fragment_init, component_init) {
						if (typeof run_fragment_init == 'undefined' || (run_fragment_init != null && run_fragment_init .hasOwnProperty ("__kwargtrans__"))) {;
							var run_fragment_init = true;
						};
						if (typeof component_init == 'undefined' || (component_init != null && component_init .hasOwnProperty ("__kwargtrans__"))) {;
							var component_init = true;
						};
						if (component_init && window.COMPONENT_INIT && len (window.COMPONENT_INIT) > 0) {
							try {
								elem.empty ();
								var res = Vue.compile (('<div>' + html_txt) + '</div>');
								if (elem && elem.length > 0) {
									var vm = new Vue (dict ({'render': res.render, 'staticRenderFns': res.staticRenderFns}));
									var component = vm.$mount ();
									var _append = function (index, value) {
										if (value) {
											elem [0].appendChild (value);
										}
									};
									jQuery.each (component.$el.childNodes, _append);
									evalJSFromHtml (html_txt);
									evalCSSFromHtml (html_txt, elem);
								}
							}
							catch (__except0__) {
								elem.html (html_txt);
							}
						}
						else {
							elem.html (html_txt);
						}
						if (run_fragment_init) {
							fragment_init (elem);
						}
						if (MOUNT_INIT_FUN) {
							var __iterable0__ = MOUNT_INIT_FUN;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var fun = __iterable0__ [__index0__];
								fun (elem);
							}
						}
						if (elem.hasClass ('refr_replace')) {
							var elem_tmp = elem.contents ();
							elem.replaceWith (elem_tmp);
						}
					};
					var save_as = function (blob, file_name) {
						var url = window.URL.createObjectURL (blob);
						var anchor_elem = document.createElement ('a');
						anchor_elem.style = 'display: none';
						anchor_elem.href = url;
						anchor_elem.download = file_name;
						document.body.appendChild (anchor_elem);
						anchor_elem.click ();
						document.body.removeChild (anchor_elem);
						var _ = function () {
							window.URL.revokeObjectURL (url);
						};
						setTimeout (_, 1000);
					};
					var download_binary_file = function (buf, content_disposition) {
						var file_name = 'temp.dat';
						var var_list = content_disposition.py_split (';');
						var __iterable0__ = var_list;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var pos = __iterable0__ [__index0__];
							if (__in__ ('filename', pos)) {
								var file_name = pos.py_split ('=') [1];
								break;
							}
						}
						save_as (buf, file_name);
					};
					var ajax_get = function (url, complete, process_req) {
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var req = new XMLHttpRequest ();
						if (process_req) {
							process_req (req);
						}
						var process_blob = false;
						try {
							req.responseType = 'blob';
							var process_blob = true;
						}
						catch (__except0__) {
							// pass;
						}
						var _onload = function () {
							if (process_blob) {
								var disp = req.getResponseHeader ('Content-Disposition');
								if (disp && __in__ ('attachment', disp)) {
									download_binary_file (req.response, disp);
									complete (null);
								}
								else {
									var reader = new FileReader ();
									var _on_reader_load = function () {
										if (req.status != 200 && req.status != 0) {
											console.log (reader.result);
											window.open ().document.write (reader.result);
											complete ('Error - details on new page');
										}
										else {
											complete (reader.result);
										}
									};
									reader.onload = _on_reader_load;
									reader.readAsText (req.response);
								}
							}
							else if (req.status != 200 && req.status != 0) {
								console.log (req.response);
								window.open ().document.write (req.response);
								complete ('Error - details on new page');
							}
							else {
								complete (req.response);
							}
						};
						req.onload = _onload;
						req.open ('GET', url, true);
						req.send (null);
					};
					window.ajax_get = ajax_get;
					var ajax_load = function (elem, url, complete) {
						var _onload = function (responseText) {
							mount_html (elem, responseText);
							complete (responseText);
						};
						ajax_get (url, _onload);
					};
					window.ajax_load = ajax_load;
					var _req_post = function (req, url, data, complete, content_type) {
						var process_blob = false;
						try {
							req.responseType = 'blob';
							var process_blob = true;
						}
						catch (__except0__) {
							// pass;
						}
						var _onload = function () {
							if (process_blob) {
								var disp = req.getResponseHeader ('Content-Disposition');
								if (disp && __in__ ('attachment', disp)) {
									download_binary_file (req.response, disp);
									complete (null);
								}
								else {
									var reader = new FileReader ();
									var _on_reader_load = function () {
										if (req.status != 200 && req.status != 0) {
											console.log (reader.result);
											window.open ().document.write (reader.result);
											complete ('Error - details on new page');
										}
										complete (reader.result);
									};
									reader.onload = _on_reader_load;
									reader.readAsText (req.response);
								}
							}
							else {
								if (req.status != 200 && req.status != 0) {
									console.log (req.response);
									window.open ().document.write (req.response);
									complete ('Error - details on new page');
								}
								complete (req.response);
							}
						};
						req.onload = _onload;
						req.open ('POST', url, true);
						req.setRequestHeader ('X-CSRFToken', Cookies.get ('csrftoken'));
						if (content_type) {
							// pass;
						}
						else {
							req.setRequestHeader ('Content-type', 'application/x-www-form-urlencoded');
						}
						if (data.length) {
							req.setRequestHeader ('Content-length', data.length);
						}
						req.send (data);
					};
					var ajax_post = function (url, data, complete, process_req) {
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var req = new XMLHttpRequest ();
						if (process_req) {
							process_req (req);
						}
						_req_post (req, url, data, complete);
					};
					window.ajax_post = ajax_post;
					var ajax_json = function (url, data, complete, process_req) {
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var _complete = function (data_in) {
							var _data = JSON.parse (data_in);
							complete (_data);
						};
						var data2 = JSON.stringify (data);
						ajax_post (url, data2, _complete, process_req);
					};
					window.ajax_json = ajax_json;
					var ajax_submit = function (form, complete, data_filter, process_req) {
						if (typeof data_filter == 'undefined' || (data_filter != null && data_filter .hasOwnProperty ("__kwargtrans__"))) {;
							var data_filter = null;
						};
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var content_type = null;
						var req = new XMLHttpRequest ();
						if (process_req) {
							process_req (req);
						}
						if (form.find ("[type='file']").length > 0) {
							var data = new FormData (form [0]);
							if (data_filter) {
								var data = data_filter (data);
							}
							var content_type = 'multipart/form-data; boundary=...';
							if (!(form.find ('#progress').length == 1)) {
								form.find ('div.inline-form-body').append ("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>");
							}
							else {
								jQuery ('#progress').width ('0%');
							}
							var _progressHandlingFunction = function (e) {
								if (e.lengthComputable) {
									jQuery ('#progress').width (('' + parseInt ((100 * e.loaded) / e.total)) + '%');
								}
							};
							req.upload.addEventListener ('progress', _progressHandlingFunction, false);
						}
						else {
							var data = form.serialize ();
							if (data_filter) {
								var data = data_filter (data);
							}
						}
						_req_post (req, corect_href (form.attr ('action')), data, complete, content_type);
					};
					window.ajax_submit = ajax_submit;
					var get_page = function (elem) {
						if (elem.hasClass ('.tab-pane')) {
							return elem;
						}
						else {
							return elem.closest ('.tab-pane');
						}
					};
					var get_table_type = function (elem) {
						var tabsort = elem.find ('.tabsort');
						if (tabsort.length == 0) {
							var tabsort = get_page (elem).find ('.tabsort');
						}
						if (tabsort.length > 0) {
							var ret = tabsort.attr ('table_type');
							if (ret) {
								return ret;
							}
						}
						return '';
					};
					var can_popup = function () {
						if (jQuery ('.modal-open').length > 0) {
							return false;
						}
						else {
							return true;
						}
					};
					var corect_href = function (href, only_table) {
						if (typeof only_table == 'undefined' || (only_table != null && only_table .hasOwnProperty ("__kwargtrans__"))) {;
							var only_table = false;
						};
						if (only_table) {
							if (__in__ ('only_table', href)) {
								return href;
							}
						}
						else if (__in__ ('only_content', href)) {
							return href;
						}
						if (only_table) {
							if (__in__ ('?', href)) {
								return href + '&only_table=1';
							}
							else {
								return href + '?only_table=1';
							}
						}
						else if (__in__ ('?', href)) {
							return href + '&only_content=1';
						}
						else {
							return href + '?only_content=1';
						}
					};
					var remove_page_from_href = function (href) {
						var x = href.py_split ('?');
						if (len (x) > 1) {
							var x2 = x [1].py_split ('&');
							if (len (x2) > 1) {
								var x3 = list ([]);
								var __iterable0__ = x2;
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var pos = __iterable0__ [__index0__];
									if (!(__in__ ('page=', pos))) {
										x3.append (pos);
									}
								}
								return (x [0] + '?') + ''.join (x3);
							}
							else if (__in__ ('page=', x2 [0])) {
								return x2;
							}
							else {
								return href;
							}
						}
						return href;
					};
					var load_css = function (path) {
						if (!(LOADED_FILES && __in__ (path, LOADED_FILES))) {
							LOADED_FILES [path] = null;
							var req = new XMLHttpRequest ();
							var _onload = function () {
								jQuery ('<style type="text/css"></style>').html (req.responseText).appendTo ('head');
							};
							req.onload = _onload;
							req.open ('GET', path, true);
							req.send ('');
						}
					};
					window.load_css = load_css;
					var on_load_js = function (path) {
						if (LOADED_FILES && __in__ (path, LOADED_FILES)) {
							var functions = LOADED_FILES [path];
							if (functions) {
								var __iterable0__ = functions;
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var fun = __iterable0__ [__index0__];
									fun ();
								}
							}
							LOADED_FILES [path] = null;
						}
					};
					var load_js = function (path, fun) {
						if (LOADED_FILES && __in__ (path, LOADED_FILES)) {
							if (LOADED_FILES [path]) {
								LOADED_FILES [path].push (fun);
							}
							else {
								fun ();
							}
						}
						else {
							LOADED_FILES [path] = list ([fun]);
							var req = new XMLHttpRequest ();
							var _onload = function () {
								var script = document.createElement ('script');
								script.text = req.responseText;
								document.head.appendChild (script).parentNode.removeChild (script);
								on_load_js (path);
							};
							req.onload = _onload;
							req.open ('GET', path, true);
							req.send ('');
						}
					};
					window.load_js = load_js;
					var load_many_js = function (paths, fun) {
						var counter = 1;
						var _fun = function () {
							counter = counter - 1;
							if (counter == 0) {
								fun ();
							}
						};
						var __iterable0__ = paths.py_split (';');
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var path = __iterable0__ [__index0__];
							if (path.length > 0) {
								var counter = counter + 1;
								load_js (path, _fun);
							}
						}
						_fun ();
					};
					window.load_many_js = load_many_js;
					var history_push_state = function (title, url, data) {
						if (typeof data == 'undefined' || (data != null && data .hasOwnProperty ("__kwargtrans__"))) {;
							var data = null;
						};
						var url2 = url.py_split ('?') [0];
						if (data) {
							var data2 = list ([LZString.compress (data [0]), data [1]]);
						}
						else {
							var data2 = title;
						}
						window.history.pushState (data2, title, url2);
					};
					window.history_push_state = history_push_state;
					var animate_combo = function (button, obj1, obj2, obj1_style_off, obj1_style_on, obj2_style_off, obj2_style_on, speed, end) {
						if (typeof end == 'undefined' || (end != null && end .hasOwnProperty ("__kwargtrans__"))) {;
							var end = null;
						};
						if (end) {
							var end2 = end;
						}
						else {
							var end2 = function () {
								// pass;
							};
						}
						var _animate = function () {
							if (button.hasClass ('on')) {
								button.removeClass ('on');
								obj1.animate (obj1_style_off, speed);
								obj2.animate (obj2_style_off, speed, 'swing', end2);
							}
							else {
								button.addClass ('on');
								obj1.animate (obj1_style_on, speed);
								obj2.animate (obj2_style_on, speed, 'swing', end2);
							}
						};
						button.click (_animate);
					};
					window.animate_combo = animate_combo;
					window.icons = dict ({'time': 'fa fa-clock-o', 'date': 'fa fa-calendar', 'up': 'fa fa-chevron-up', 'down': 'fa fa-chevron-down', 'previous': 'fa fa-chevron-left', 'next': 'fa fa-chevron-right', 'today': 'fa fa-calendar-check-o', 'clear': 'fa fa-trash', 'close': 'fa fa-times', 'paginationSwitchDown': 'fa-chevron-down', 'paginationSwitchUp': 'fa-chevron-up', 'refresh': 'fa-refresh', 'toggle': 'fa-list-alt', 'columns': 'fa-th', 'detailOpen': 'fa-plus', 'detailClose': 'fa-minus'});
					var get_and_run_script = function (url, elem, e) {
						var _on_load_js = function (html_text) {
							var object = jQuery (elem);
							var x = jQuery (html_text).html ();
							if (x) {
								eval (x);
							}
							var object = null;
						};
						ajax_get (url, _on_load_js);
					};
					__pragma__ ('<all>')
						__all__.FIRST_INIT = FIRST_INIT;
						__all__.FRAGMENT_INIT_FUN = FRAGMENT_INIT_FUN;
						__all__.LOADED_FILES = LOADED_FILES;
						__all__.MOUNT_INIT_FUN = MOUNT_INIT_FUN;
						__all__.__name__ = __name__;
						__all__._req_post = _req_post;
						__all__.ajax_get = ajax_get;
						__all__.ajax_json = ajax_json;
						__all__.ajax_load = ajax_load;
						__all__.ajax_post = ajax_post;
						__all__.ajax_submit = ajax_submit;
						__all__.animate_combo = animate_combo;
						__all__.can_popup = can_popup;
						__all__.corect_href = corect_href;
						__all__.download_binary_file = download_binary_file;
						__all__.evalCSSFromHtml = evalCSSFromHtml;
						__all__.evalJSFromHtml = evalJSFromHtml;
						__all__.fragment_init = fragment_init;
						__all__.get_and_run_script = get_and_run_script;
						__all__.get_page = get_page;
						__all__.get_table_type = get_table_type;
						__all__.history_push_state = history_push_state;
						__all__.load_css = load_css;
						__all__.load_js = load_js;
						__all__.load_many_js = load_many_js;
						__all__.mount_html = mount_html;
						__all__.on_load_js = on_load_js;
						__all__.register_fragment_init_fun = register_fragment_init_fun;
						__all__.register_mount_fun = register_mount_fun;
						__all__.remove_page_from_href = remove_page_from_href;
						__all__.save_as = save_as;
					__pragma__ ('</all>')
				}
			}
		}
	);
