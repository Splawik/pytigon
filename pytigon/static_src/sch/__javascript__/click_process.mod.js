	__nest__ (
		__all__,
		'click_process', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'click_process';
					var corect_href = __init__ (__world__.tools).corect_href;
					var ajax_get = __init__ (__world__.tools).ajax_get;
					var mount_html = __init__ (__world__.tools).mount_html;
					var refresh_fragment = __init__ (__world__.popup).refresh_fragment;
					var get_menu = __init__ (__world__.tabmenu).get_menu;
					var get_value = function (elem, py_name) {
						if (elem.length > 0) {
							var x = elem.closest ('.refr_object');
							if (x.length > 0) {
								var x2 = x.find (sprintf ("[name='%s']", py_name));
								if (x2.length > 0) {
									return x2.val ();
								}
							}
						}
						return '[[ERROR]]';
					};
					var process_href = function (href, elem) {
						var ret = list ([]);
						if (__in__ ('[[', href) && __in__ (']]', href)) {
							var x1 = href.py_split ('[[');
							var process = false;
							var __iterable0__ = x1;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var pos = __iterable0__ [__index0__];
								if (process) {
									if (__in__ (']]', pos)) {
										var x2 = pos.py_split (']]', 1);
										var value = get_value (elem, x2 [0]);
										if (value && value != 'None') {
											ret.append (value + x2 [1]);
										}
										else {
											ret.append (x2 [1]);
										}
									}
									else {
										ret.append (pos);
									}
									var process = false;
								}
								else {
									ret.append (pos);
									var process = true;
								}
							}
							return ''.join (ret);
						}
						else {
							return href;
						}
					};
					var process_on_click = function (event_tab, elem) {
						if (typeof elem == 'undefined' || (elem != null && elem .hasOwnProperty ("__kwargtrans__"))) {;
							var elem = null;
						};
						var _on_click = function (e) {
							var target = jQuery (e.currentTarget).attr ('target');
							if (target == '_blank' || target == '_parent') {
								return true;
							}
							var src_obj = jQuery (this);
							if (__in__ ('xlink:href', e.currentTarget.attributes)) {
								var href = jQuery (this).attr ('xlink:href');
							}
							else {
								var href = jQuery (this).attr ('href');
							}
							if (href && __in__ ('#', href)) {
								return true;
							}
							if (!(href)) {
								return true;
							}
							var href = process_href (href, src_obj);
							var __iterable0__ = event_tab;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var pos = __iterable0__ [__index0__];
								if (pos [0] == '*' || pos [0] == target) {
									if (pos [1] == '*' || src_obj.hasClass (pos [1])) {
										if (pos [3]) {
											var url = corect_href (href, true);
										}
										else if (pos [2]) {
											var url = corect_href (href, false);
										}
										else {
											var url = href;
										}
										e.preventDefault ();
										pos [4] (url, this, e);
										return true;
									}
								}
							}
							e.preventDefault ();
							var href2 = corect_href (href);
							var _on_data = function (data) {
								if (data && __in__ ('_parent_refr', data) || __in__ (target, tuple (['refresh_obj', 'refresh_page']))) {
									if (target == 'refresh_obj') {
										if (!(refresh_fragment (src_obj, null, true))) {
											refresh_fragment (src_obj);
										}
									}
									else {
										refresh_fragment (src_obj);
									}
								}
								else {
									if (window.APPLICATION_TEMPLATE == 'modern') {
										if (window.ACTIVE_PAGE) {
											mount_html (window.ACTIVE_PAGE.page, data);
										}
										else {
											mount_html (jQuery ('#wiki_start'), data);
											return ;
										}
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
							ajax_get (href2, _on_data);
						};
						if (elem) {
							elem.on ('click', 'a', _on_click);
						}
						else {
							jQuery ('#tabs2_content').on ('click', 'a', _on_click);
							jQuery ('#dialog-form-modal').on ('click', 'a', _on_click);
							jQuery ('#body_body').on ('click', 'a', _on_click);
							jQuery ('#wiki_start').on ('click', 'a', _on_click);
						}
					};
					__pragma__ ('<use>' +
						'popup' +
						'tabmenu' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.ajax_get = ajax_get;
						__all__.corect_href = corect_href;
						__all__.get_menu = get_menu;
						__all__.get_value = get_value;
						__all__.mount_html = mount_html;
						__all__.process_href = process_href;
						__all__.process_on_click = process_on_click;
						__all__.refresh_fragment = refresh_fragment;
					__pragma__ ('</all>')
				}
			}
		}
	);
