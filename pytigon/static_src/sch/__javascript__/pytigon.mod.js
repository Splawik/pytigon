	(function () {
		var __name__ = '__main__';
		var Page = __init__ (__world__.page).Page;
		var TabMenuItem = __init__ (__world__.tabmenuitem).TabMenuItem;
		var get_menu = __init__ (__world__.tabmenu).get_menu;
		var on_get_tbl_value = __init__ (__world__.popup).on_get_tbl_value;
		var on_new_tbl_value = __init__ (__world__.popup).on_new_tbl_value;
		var on_get_row = __init__ (__world__.popup).on_get_row;
		var on_popup_edit_new = __init__ (__world__.popup).on_popup_edit_new;
		var on_popup_inline = __init__ (__world__.popup).on_popup_inline;
		var on_popup_info = __init__ (__world__.popup).on_popup_info;
		var on_popup_delete = __init__ (__world__.popup).on_popup_delete;
		var on_cancel_inline = __init__ (__world__.popup).on_cancel_inline;
		var refresh_fragment = __init__ (__world__.popup).refresh_fragment;
		var on_edit_ok = __init__ (__world__.popup).on_edit_ok;
		var on_delete_ok = __init__ (__world__.popup).on_delete_ok;
		var ret_ok = __init__ (__world__.popup).ret_ok;
		var refresh_current_object = __init__ (__world__.popup).refresh_current_object;
		var refresh_current_page = __init__ (__world__.popup).refresh_current_page;
		var refresh_current_app = __init__ (__world__.popup).refresh_current_app;
		var only_get = __init__ (__world__.popup).only_get;
		var init_table = __init__ (__world__.tbl).init_table;
		var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
		var can_popup = __init__ (__world__.tools).can_popup;
		var corect_href = __init__ (__world__.tools).corect_href;
		var get_table_type = __init__ (__world__.tools).get_table_type;
		var handle_class_click = __init__ (__world__.tools).handle_class_click;
		var ajax_get = __init__ (__world__.tools).ajax_get;
		var ajax_post = __init__ (__world__.tools).ajax_post;
		var ajax_load = __init__ (__world__.tools).ajax_load;
		var ajax_submit = __init__ (__world__.tools).ajax_submit;
		var load_css = __init__ (__world__.tools).load_css;
		var load_js = __init__ (__world__.tools).load_js;
		var load_many_js = __init__ (__world__.tools).load_many_js;
		var history_push_state = __init__ (__world__.tools).history_push_state;
		var mount_html = __init__ (__world__.tools).mount_html;
		var register_fragment_init_fun = __init__ (__world__.tools).register_fragment_init_fun;
		var register_mount_fun = __init__ (__world__.tools).register_mount_fun;
		var remove_page_from_href = __init__ (__world__.tools).remove_page_from_href;
		var get_and_run_script = __init__ (__world__.tools).get_and_run_script;
		var service_worker_and_indexedDB_test = __init__ (__world__.offline).service_worker_and_indexedDB_test;
		var install_service_worker = __init__ (__world__.offline).install_service_worker;
		var sync_and_run = __init__ (__world__.db).sync_and_run;
		var img_field = __init__ (__world__.widget).img_field;
		var process_on_click = __init__ (__world__.click_process).process_on_click;
		window.PS = null;
		window.MOUNTED_COMPONENTS = 0;
		var app_init = function (prj_name, application_template, menu_id, lang, base_path, base_fragment_init, component_init, offline_support, start_page, gen_time) {
			moment.locale (lang);
			window.ACTIVE_PAGE = null;
			window.PRJ_NAME = prj_name;
			window.APPLICATION_TEMPLATE = application_template;
			window.MENU = null;
			window.PUSH_STATE = true;
			if (base_path) {
				window.BASE_PATH = base_path;
			}
			else {
				window.BASE_PATH = '';
			}
			window.WAIT_ICON = null;
			window.WAIT_ICON2 = false;
			window.MENU_ID = 0;
			window.BASE_FRAGMENT_INIT = base_fragment_init;
			window.COUNTER = 1;
			window.EDIT_RET_FUNCTION = null;
			window.RET_CONTROL = null;
			window.COMPONENT_INIT = component_init;
			window.LANG = lang;
			window.GEN_TIME = gen_time;
			if (offline_support) {
				if (navigator.onLine && service_worker_and_indexedDB_test ()) {
					install_service_worker ();
				}
			}
			var _on_sync = function (status) {
				if (status == 'OK-refresh') {
					location.reload ();
				}
			};
			sync_and_run ('sys', _on_sync);
			jQuery (window).resize (datatable_onresize);
			var _on_submit = function (e) {
				var self = jQuery (this);
				if (jQuery (this).hasClass ('DialogForm')) {
					e.preventDefault ();
					on_edit_ok (false, jQuery (this));
					return ;
				}
				if (jQuery (this).attr ('target') == '_blank') {
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				if (jQuery (this).attr ('target') == '_self') {
					return true;
				}
				if (jQuery (this).attr ('target') == 'refresh_obj') {
					if (refresh_fragment (jQuery (this), null, true, null, true)) {
						return false;
					}
				}
				var data = jQuery (this).serialize ();
				if (data && __in__ ('pdf=on', data)) {
					jQuery (this).attr ('target', '_blank');
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				if (data && __in__ ('odf=on', data)) {
					jQuery (this).attr ('target', '_blank');
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				e.preventDefault ();
				var submit_button = jQuery (this).find ('button[type="submit"]');
				if (submit_button.length > 0) {
					submit_button.attr ('data-style', 'zoom-out');
					submit_button.attr ('data-spinner-color', '#FF0000');
					window.WAIT_ICON = Ladda.create (submit_button [0]);
					window.WAIT_ICON.start ();
				}
				else {
					window.WAIT_ICON2 = true;
					jQuery ('#loading-indicator').show ();
				}
				var href = jQuery (this).attr ('action');
				if (href) {
					jQuery (this).attr ('action', corect_href (remove_page_from_href (href)));
				}
				var _on_submit2 = function (data) {
					if (window.ACTIVE_PAGE) {
						mount_html (window.ACTIVE_PAGE.page, data);
					}
					else {
						_on_menu_href (self, self.attr ('title'), null, data);
					}
					if (window.WAIT_ICON) {
						window.WAIT_ICON.stop ();
					}
					if (window.WAIT_ICON2) {
						jQuery ('#loading-indicator').hide ();
						window.WAIT_ICON2 = false;
					}
				};
				ajax_submit (jQuery (this), _on_submit2);
			};
			jQuery ('#tabs2_content').on ('submit', 'form', _on_submit);
			jQuery ('#dialog-form-modal').on ('submit', 'form', _on_submit);
			jQuery ('#search').on ('submit', 'form', _on_submit);
			if (jQuery ('#menu').length > 0) {
				window.PS = new PerfectScrollbar ('#menu');
				var _on_resize = function () {
					window.PS.update ();
				};
				jQuery (window).resize (_on_resize);
			}
			var _on_key = function (e) {
				if (e.which == 13) {
					var elem = jQuery (e.target);
					if (elem.prop ('tagName') != 'TEXTAREA') {
						var form = elem.closest ('form');
						if (form.length > 0) {
							if (form.hasClass ('DialogForm')) {
								e.preventDefault ();
								on_edit_ok (false, form);
								return ;
							}
						}
					}
				}
			};
			jQuery (document).keypress (_on_key);
			process_on_click (EVENT_TAB);
			if (can_popup ()) {
				var _local_fun = function () {
					if (window.APPLICATION_TEMPLATE != 'traditional') {
						var pos = jQuery ('.menu-href.btn-warning');
						if (pos.length > 0) {
							var elem = jQuery ('#a_' + pos.closest ('div.tab-pane').attr ('id'));
							elem.tab ('show');
						}
						else {
							var elem = jQuery ('.first_pos');
							elem.tab ('show');
						}
					}
					else {
						var id = int (menu_id) + 1;
						var elem = jQuery (('#tabs a:eq(' + id) + ')');
						elem.tab ('show');
					}
					var _on_menu_click = function (e) {
						if (window.APPLICATION_TEMPLATE != 'traditional') {
							e.preventDefault ();
							var toggler = jQuery ('#topmenu').find ('.navbar-toggler');
							if (toggler && toggler.is (':visible')) {
								var obj = this;
								var _on_collapse = function () {
									_on_menu_href (obj);
									jQuery ('#navbar-ex1-collapse').off ('hidden.bs.collapse', _on_collapse);
								};
								jQuery ('#navbar-ex1-collapse').on ('hidden.bs.collapse', _on_collapse);
								jQuery ('#navbar-ex1-collapse').collapse ('hide');
							}
							else {
								_on_menu_href (this);
							}
						}
					};
					jQuery ('body').on ('click', 'a.menu-href', _on_menu_click);
					var _on_logout_click = function () {
						window.location = jQuery (this).attr ('action');
					};
					jQuery ('#logout').on ('click', _on_logout_click);
					var _on_sysmenu_click = function () {
						window.location = jQuery (this).attr ('action');
					};
					jQuery ('.system_menu').on ('click', _on_sysmenu_click);
					var _on_tabs_click = function (e) {
						e.preventDefault ();
						jQuery (this).tab ('show');
					};
					jQuery ('#tabs a').click (_on_tabs_click);
					var _on_resize = function (e) {
						datatable_onresize ();
					};
					jQuery ('#tabs2').on ('shown.bs.tab', _on_resize);
					var _on_timeout = function (e) {
						window.setTimeout (datatable_onresize, 300);
					};
					jQuery ('body').on ('expanded.pushMenu collapsed.pushMenu', _on_timeout);
				};
				jQuery (_local_fun);
			}
			var _init_start_wiki_page = function () {
				if (start_page && start_page != 'None' && window.location.pathname == base_path) {
					var _on_load = function (responseText, status, response) {
						// pass;
					};
					ajax_load (jQuery ('#wiki_start'), (base_path + start_page) + '?only_content&schtml=1', _on_load);
				}
			};
			window.init_start_wiki_page = _init_start_wiki_page;
			_init_start_wiki_page ();
		};
		var _on_menu_href = function (elem, title, url, txt) {
			if (typeof title == 'undefined' || (title != null && title .hasOwnProperty ("__kwargtrans__"))) {;
				var title = null;
			};
			if (typeof url == 'undefined' || (url != null && url .hasOwnProperty ("__kwargtrans__"))) {;
				var url = null;
			};
			if (typeof txt == 'undefined' || (txt != null && txt .hasOwnProperty ("__kwargtrans__"))) {;
				var txt = null;
			};
			if (window.APPLICATION_TEMPLATE != 'traditional') {
				if (!(title)) {
					var title = jQuery.trim (jQuery (elem).text ());
				}
				if (txt) {
					var value = jQuery (('<div>' + txt) + '</div>').find ('head').find ('title').text ();
					if (value) {
						var title = value;
					}
				}
				var menu = get_menu ();
				var classname = jQuery (elem).attr ('class');
				if (classname && __in__ ('btn', classname)) {
					if (window.WAIT_ICON) {
						window.WAIT_ICON.stop ();
					}
					jQuery (elem).attr ('data-style', 'zoom-out');
					jQuery (elem).attr ('data-spinner-color', '#FF0000');
					window.WAIT_ICON = Ladda.create (elem);
				}
				else {
					window.WAIT_ICON = null;
				}
				if (window.APPLICATION_TEMPLATE == 'modern' && menu.is_open (title)) {
					menu.activate (title);
				}
				else {
					if (url) {
						var href = url;
					}
					else {
						var href = jQuery (elem).attr ('href');
					}
					var href2 = corect_href (href);
					var _on_new_win = function (data) {
						jQuery ('#wiki_start').hide ();
						if (window.APPLICATION_TEMPLATE == 'modern') {
							var id = menu.new_page (title, data, href2);
						}
						else {
							mount_html (jQuery ('#body_body'), data);
							window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
							window.ACTIVE_PAGE.set_href (href2);
							if (window.PUSH_STATE) {
								var id = jQuery (elem).attr ('id');
								if (!(id)) {
									var id = 'menu_id_' + window.MENU_ID;
									window.MENU_ID = window.MENU_ID + 1;
									jQuery (elem).attr ('id', id);
								}
								history_push_state (title, href, list ([data, id]));
							}
						}
						if (window.WAIT_ICON) {
							window.WAIT_ICON.stop ();
							window.WAIT_ICON = null;
						}
						if (window.WAIT_ICON2) {
							jQuery ('#loading-indicator').hide ();
							window.WAIT_ICON2 = false;
						}
					};
					if (window.APPLICATION_TEMPLATE == 'standard' && classname && __in__ ('btn', classname)) {
						jQuery ('a.menu-href').removeClass ('btn-warning');
						jQuery (elem).addClass ('btn-warning');
					}
					if (txt) {
						_on_new_win (txt);
					}
					else {
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						else {
							window.WAIT_ICON2 = true;
							jQuery ('#loading-indicator').show ();
						}
						ajax_get (href2, _on_new_win);
						jQuery ('.navbar-ex1-collapse').collapse ('hide');
					}
				}
				jQuery ('.auto-hide').trigger ('click');
				return false;
			}
		};
		var _on_error = function (request, settings) {
			if (window.WAIT_ICON) {
				window.WAIT_ICON.stop ();
				window.WAIT_ICON = null;
			}
			if (window.WAIT_ICON2) {
				jQuery ('#loading-indicator').hide ();
				window.WAIT_ICON2 = false;
			}
			if (settings.status == 200) {
				return ;
			}
			if (settings.responseText) {
				var start = settings.responseText.indexOf ('<body>');
				var end = settings.responseText.lastIndexOf ('</body>');
				if (start > 0 && end > 0) {
					mount_html (jQuery ('#dialog-data-error'), settings.responseText.substring (start + 6, end - 1));
					jQuery ('#dialog-form-error').modal ();
				}
				else {
					mount_html (jQuery ('#dialog-data-error'), settings.responseText);
					jQuery ('#dialog-form-error').modal ();
				}
			}
		};
		var jquery_ready = function () {
			jQuery (document).ajaxError (_on_error);
			var _on_hide = function (e) {
				mount_html (jQuery (this).find ('div.dialog-data'), "<div class='alert alert-info' role='alert'>Sending data - please wait</div>", false, false);
			};
			jQuery ('div.dialog-form').on ('hide.bs.modal', _on_hide);
			var _local_fun = function () {
				console.log ('collapsed');
			};
			jQuery ('.navbar-ex1-collapse').on ('hidden.bs.collapse', _local_fun);
			if (window.APPLICATION_TEMPLATE == 'traditional') {
				window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
			}
			else if (window.APPLICATION_TEMPLATE == 'modern') {
				var txt = jQuery ('.page').html ();
				var txt2 = jQuery.trim (txt);
				if (txt2) {
					var txt = jQuery.trim (jQuery ('.page') [0].outerHTML);
					jQuery ('.page').remove ();
					var menu = get_menu ();
					menu.new_page (jQuery ('title').text (), txt, window.location.href);
				}
			}
			else {
				window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
				if (window.APPLICATION_TEMPLATE == 'to_print') {
					new Vue (dict ({'el': '#body_body'}));
				}
			}
		};
		var on_new_tab = function (url, elem, e) {
			var title = jQuery (e.currentTarget).attr ('title');
			var url2 = url.py_split ('?') [0];
			if (!(title)) {
				if (len (url2) > 16) {
					var title = '...' + url2.__getslice__ (-(13), null, 1);
				}
				else {
					var title = url2;
				}
			}
			return _on_menu_href (elem, title, url);
		};
		var EVENT_TAB = list ([tuple (['*', 'get_tbl_value', true, false, on_get_tbl_value]), tuple (['*', 'new_tbl_value', true, false, on_new_tbl_value]), tuple (['*', 'get_row', true, false, on_get_row]), tuple (['popup_edit', '*', true, false, on_popup_edit_new]), tuple (['popup_info', '*', true, false, on_popup_info]), tuple (['popup_delete', '*', true, false, on_popup_delete]), tuple (['inline', '*', true, false, on_popup_inline]), tuple (['_top', '*', true, false, on_new_tab]), tuple (['_top2', '*', true, false, on_new_tab]), tuple (['refresh_obj', '*', true, false, refresh_current_object]), tuple (['refresh_page', '*', true, false, refresh_current_page]), tuple (['refresh_app', '*', false, false, refresh_current_app]), tuple (['run_script', '*', false, false, get_and_run_script]), tuple (['null', '*', false, false, only_get])]);
		var standard_on_data = function (src_obj, href) {
			var _standard_on_data = function (data) {
				if (data && __in__ ('_parent_refr', data)) {
					refresh_fragment (src_obj);
				}
				else {
					if (window.APPLICATION_TEMPLATE == 'modern') {
						mount_html (window.ACTIVE_PAGE.page, data);
						window.ACTIVE_PAGE.set_href (href);
					}
					else {
						mount_html (jQuery ('#body_body'), data);
					}
					window.ACTIVE_PAGE.set_href (href);
					get_menu ().get_active_item ().url = href;
					if (window.PUSH_STATE) {
						history_push_state ('title', href);
					}
				}
			};
			return _standard_on_data;
		};
		window.standard_on_data = standard_on_data;
		var _on_popstate = function (e) {
			if (e.state) {
				window.PUSH_STATE = false;
				if (window.APPLICATION_TEMPLATE == 'modern') {
					var menu = get_menu ().activate (e.state, false);
				}
				else {
					var x = e.state;
					mount_html (jQuery ('#body_body'), LZString.decompress (x [0]));
					window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
					window.ACTIVE_PAGE.set_href (document.location);
					if (window.APPLICATION_TEMPLATE == 'standard') {
						jQuery ('a.menu-href').removeClass ('btn-warning');
						jQuery ('#' + x [1]).addClass ('btn-warning');
					}
				}
				window.PUSH_STATE = true;
			}
			else if (window.APPLICATION_TEMPLATE == 'modern') {
				// pass;
			}
			else {
				mount_html (jQuery ('#body_body'), '', false, false);
				window.ACTIVE_PAGE = null;
				if (window.APPLICATION_TEMPLATE == 'standard') {
					jQuery ('a.menu-href').removeClass ('btn-warning');
				}
			}
		};
		window.addEventListener ('popstate', _on_popstate, false);
		__pragma__ ('<use>' +
			'click_process' +
			'db' +
			'offline' +
			'page' +
			'popup' +
			'tabmenu' +
			'tabmenuitem' +
			'tbl' +
			'tools' +
			'widget' +
		'</use>')
		__pragma__ ('<all>')
			__all__.EVENT_TAB = EVENT_TAB;
			__all__.Page = Page;
			__all__.TabMenuItem = TabMenuItem;
			__all__.__name__ = __name__;
			__all__._on_error = _on_error;
			__all__._on_menu_href = _on_menu_href;
			__all__._on_popstate = _on_popstate;
			__all__.ajax_get = ajax_get;
			__all__.ajax_load = ajax_load;
			__all__.ajax_post = ajax_post;
			__all__.ajax_submit = ajax_submit;
			__all__.app_init = app_init;
			__all__.can_popup = can_popup;
			__all__.corect_href = corect_href;
			__all__.datatable_onresize = datatable_onresize;
			__all__.get_and_run_script = get_and_run_script;
			__all__.get_menu = get_menu;
			__all__.get_table_type = get_table_type;
			__all__.handle_class_click = handle_class_click;
			__all__.history_push_state = history_push_state;
			__all__.img_field = img_field;
			__all__.init_table = init_table;
			__all__.install_service_worker = install_service_worker;
			__all__.jquery_ready = jquery_ready;
			__all__.load_css = load_css;
			__all__.load_js = load_js;
			__all__.load_many_js = load_many_js;
			__all__.mount_html = mount_html;
			__all__.on_cancel_inline = on_cancel_inline;
			__all__.on_delete_ok = on_delete_ok;
			__all__.on_edit_ok = on_edit_ok;
			__all__.on_get_row = on_get_row;
			__all__.on_get_tbl_value = on_get_tbl_value;
			__all__.on_new_tab = on_new_tab;
			__all__.on_new_tbl_value = on_new_tbl_value;
			__all__.on_popup_delete = on_popup_delete;
			__all__.on_popup_edit_new = on_popup_edit_new;
			__all__.on_popup_info = on_popup_info;
			__all__.on_popup_inline = on_popup_inline;
			__all__.only_get = only_get;
			__all__.process_on_click = process_on_click;
			__all__.refresh_current_app = refresh_current_app;
			__all__.refresh_current_object = refresh_current_object;
			__all__.refresh_current_page = refresh_current_page;
			__all__.refresh_fragment = refresh_fragment;
			__all__.register_fragment_init_fun = register_fragment_init_fun;
			__all__.register_mount_fun = register_mount_fun;
			__all__.remove_page_from_href = remove_page_from_href;
			__all__.ret_ok = ret_ok;
			__all__.service_worker_and_indexedDB_test = service_worker_and_indexedDB_test;
			__all__.standard_on_data = standard_on_data;
			__all__.sync_and_run = sync_and_run;
		__pragma__ ('</all>')
	}) ();
