	__nest__ (
		__all__,
		'popup', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'popup';
					var can_popup = __init__ (__world__.tools).can_popup;
					var corect_href = __init__ (__world__.tools).corect_href;
					var ajax_load = __init__ (__world__.tools).ajax_load;
					var ajax_get = __init__ (__world__.tools).ajax_get;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var ajax_submit = __init__ (__world__.tools).ajax_submit;
					var handle_class_click = __init__ (__world__.tools).handle_class_click;
					var mount_html = __init__ (__world__.tools).mount_html;
					var get_table_type = __init__ (__world__.tools).get_table_type;
					var register_fragment_init_fun = __init__ (__world__.tools).register_fragment_init_fun;
					var remove_page_from_href = __init__ (__world__.tools).remove_page_from_href;
					var datatable_refresh = __init__ (__world__.tbl).datatable_refresh;
					var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
					var init_table = __init__ (__world__.tbl).init_table;
					var get_menu = __init__ (__world__.tabmenu).get_menu;
					var refresh_fragment = function (data_item_to_refresh, fun, only_table, data, remove_pagination) {
						if (typeof fun == 'undefined' || (fun != null && fun .hasOwnProperty ("__kwargtrans__"))) {;
							var fun = null;
						};
						if (typeof only_table == 'undefined' || (only_table != null && only_table .hasOwnProperty ("__kwargtrans__"))) {;
							var only_table = false;
						};
						if (typeof data == 'undefined' || (data != null && data .hasOwnProperty ("__kwargtrans__"))) {;
							var data = null;
						};
						if (typeof remove_pagination == 'undefined' || (remove_pagination != null && remove_pagination .hasOwnProperty ("__kwargtrans__"))) {;
							var remove_pagination = false;
						};
						var only_table_href = false;
						var refr_block = data_item_to_refresh.closest ('.refr_object');
						if (refr_block.hasClass ('refr_target')) {
							var target = refr_block;
						}
						else {
							var target = refr_block.find ('.refr_target');
							if (target.length > 1) {
								var target = jQuery (target [0]);
							}
						}
						if (only_table) {
							var datatable = target.find ('table[name=tabsort].datatable');
							if (datatable.length > 0) {
								datatable_refresh (datatable);
								target.find ('.inline_dialog').remove ();
								if (fun) {
									fun ();
								}
								return true;
							}
							var datatable = target.find ('table[name=tabsort].tabsort');
							if (datatable.length > 0) {
								var only_table_href = true;
								target.find ('.inline_dialog').remove ();
								var target = datatable.closest ('div.tableframe');
							}
							else {
								return false;
							}
						}
						if (data) {
							mount_html (target, data);
							if (fun) {
								fun ();
							}
						}
						else {
							if (refr_block.hasClass ('refr_source')) {
								var src = refr_block;
							}
							else {
								var src = refr_block.find ('.refr_source');
							}
							if (src.length > 0) {
								var src = jQuery (src [0]);
								var href = src.attr ('href');
								if (remove_pagination) {
									var href = remove_page_from_href (href);
								}
								if (src.prop ('tagName') == 'FORM') {
									var _refr2 = function (data) {
										mount_html (target, data);
										if (fun) {
											fun ();
										}
									};
									ajax_post (corect_href (href, only_table_href), src.serialize (), _refr2);
								}
								else {
									var _on_load = function (responseText) {
										if (fun) {
											fun ();
										}
									};
									ajax_load (target, corect_href (href, only_table_href), _on_load);
								}
							}
							else if (fun) {
								fun ();
							}
						}
						return true;
					};
					var on_popup_inline = function (url, elem, e) {
						var jelem = jQuery (elem);
						if (jelem.hasClass ('edit')) {
							return on_popup_edit_new (url, elem, e);
						}
						if (jelem.hasClass ('delete')) {
							return on_popup_delete (url, elem, e);
						}
						if (jelem.hasClass ('info')) {
							return on_popup_delete (url, elem, e);
						}
						jelem.attr ('data-style', 'zoom-out');
						jelem.attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						jQuery ('body').addClass ('shown_inline_dialog');
						jelem.closest ('table').find ('.inline_dialog').remove ();
						window.COUNTER = window.COUNTER + 1;
						var id = window.COUNTER;
						var href2 = corect_href (jQuery (elem).attr ('href'));
						var new_fragment = jQuery (((((("<tr class='refr_source refr_object inline_dialog hide' id='IDIAL_" + id) + "' href='") + href2) + "'><td colspan='20'>") + INLINE_TABLE_HTML.py_replace ('{{title}}', elem.getAttribute ('title'))) + '</td></tr>');
						new_fragment.insertAfter (jQuery (elem).closest ('tr'));
						var elem2 = new_fragment.find ('.refr_target');
						var _on_load = function (responseText, status, response) {
							new_fragment.removeClass ('hide');
							if (status != 'error') {
								_dialog_loaded (false, elem2);
								on_dialog_load ();
							}
							if (window.WAIT_ICON) {
								window.WAIT_ICON.stop ();
								window.WAIT_ICON = null;
							}
						};
						ajax_load (elem2, href2, _on_load);
						return false;
					};
					var on_popup_in_form = function (elem) {
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						jQuery ('body').addClass ('shown_inline_dialog');
						jQuery (elem).closest ('div.Dialog').find ('.inline_dialog').remove ();
						window.COUNTER = window.COUNTER + 1;
						var id = window.COUNTER;
						var href2 = corect_href (jQuery (elem).attr ('href'));
						var new_fragment = jQuery (((((("<div class='refr_source refr_object inline_dialog hide' id='IDIAL_" + id) + "' href='") + href2) + "'>") + INLINE_TABLE_HTML.py_replace ('{{title}}', elem.getAttribute ('title'))) + '</div>');
						new_fragment.insertAfter (jQuery (elem).closest ('div.form-group'));
						var elem2 = new_fragment.find ('.refr_target');
						var _on_load = function (responseText, status, response) {
							jQuery ('#IDIAL_' + id).hide ();
							jQuery ('#IDIAL_' + id).removeClass ('hide');
							jQuery ('#IDIAL_' + id).show ('slow');
							if (status != 'error') {
								_dialog_loaded (false, elem2);
								on_dialog_load ();
							}
							if (window.WAIT_ICON) {
								window.WAIT_ICON.stop ();
								window.WAIT_ICON = null;
							}
						};
						ajax_load (elem2, href2, _on_load);
						return false;
					};
					var on_popup_edit_new = function (url, elem, e) {
						if (e) {
							var target = jQuery (e.currentTarget).attr ('target');
						}
						else {
							var target = 'popup';
						}
						if (url) {
							var href2 = corect_href (url);
						}
						else {
							var href2 = corect_href (jQuery (elem).attr ('href'));
						}
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (can_popup () && !(target == 'inline') && !(jQuery (elem).hasClass ('inline')) && !(jQuery (elem).attr ('name') && __in__ ('_inline', jQuery (elem).attr ('name')))) {
							jQuery ('#ModalLabel').html (jQuery (elem).attr ('title'));
							var elem2 = jQuery ('div.dialog-data');
							elem2.closest ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load = function (responseText, status, response) {
								_dialog_loaded (true, elem2);
								on_dialog_load ();
							};
							ajax_load (elem2, href2, _on_load);
						}
						else {
							jQuery ('body').addClass ('shown_inline_dialog');
							if (window.WAIT_ICON) {
								window.WAIT_ICON.start ();
							}
							if (jQuery (elem).hasClass ('new-row')) {
								var elem2 = jQuery ((sprintf ("<div class='refr_source refr_object inline_dialog tr hide' href='%s'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</div>');
								var new_position = jQuery (elem).closest ('.refr_object').find ('div.new_row');
								if (new_position.length > 0) {
									elem2.insertAfter (jQuery (new_position [0]));
								}
								else {
									elem2.insertAfter (jQuery (elem).closest ('div.tr'));
								}
							}
							else {
								var in_table = false;
								var __iterable0__ = list ([jQuery (elem).parent (), jQuery (elem).parent ().parent ()]);
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var obj = __iterable0__ [__index0__];
									var __iterable1__ = list (['td_action', 'td_information']);
									for (var __index1__ = 0; __index1__ < len (__iterable1__); __index1__++) {
										var c = __iterable1__ [__index1__];
										if (obj.hasClass (c)) {
											var in_table = true;
											break;
										}
									}
								}
								if (in_table) {
									var elem2 = jQuery ((sprintf ("<tr class='refr_source refr_object inline_dialog hide' href='%s'><td colspan='20'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</td></tr>');
									elem2.insertAfter (jQuery (elem).closest ('tr'));
								}
								else {
									var test = jQuery (elem).closest ('form');
									if (test.length > 0) {
										var elem2 = jQuery ((sprintf ("<div class='refr_source refr_object inline_dialog hide' href='%s'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</div>');
										elem2.insertAfter (jQuery (elem).closest ('div.form-group'));
									}
									else {
										var elem2 = jQuery ((sprintf ("<div class='refr_source refr_object inline_dialog tr hide' href='%s'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</div>');
										var new_position = jQuery (elem).closest ('.refr_object').find ('div.new_row');
										if (new_position.length > 0) {
											elem2.insertAfter (jQuery (new_position [0]));
										}
										else {
											elem2.insertAfter (jQuery (elem).closest ('div.tr'));
										}
									}
								}
							}
							mount_html (elem2.find ('.modal-title'), jQuery (elem).attr ('title'), false, false);
							elem2.attr ('related-object', jQuery (elem).uid ());
							var elem3 = elem2.find ('div.dialog-data-inner');
							var _on_load2 = function (responseText, status, response) {
								elem2.hide ();
								elem2.removeClass ('hide');
								elem2.show ('slow');
								if (status != 'error') {
									_dialog_loaded (false, elem3);
									on_dialog_load ();
								}
								if (window.WAIT_ICON) {
									window.WAIT_ICON.stop ();
									window.WAIT_ICON = null;
								}
							};
							ajax_load (elem3, href2, _on_load2);
						}
						return false;
					};
					window.on_popup_edit_new = on_popup_edit_new;
					var on_popup_info = function (url, elem, e) {
						if (can_popup ()) {
							var _on_load = function (responseText, status, response) {
								jQuery ('div.dialog-form-info').modal ();
							};
							ajax_load (jQuery ('div.dialog-data-info'), jQuery (elem).attr ('href'), _on_load);
						}
						else {
							jQuery ('.inline_dialog').remove ();
							jQuery (("<tr class='refr_object inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML) + '</td></tr>').insertAfter (jQuery (elem).parents ('tr'));
							var _on_load2 = function (responseText, status, response) {
								// pass;
							};
							ajax_load (jQuery ('div.dialog-data-inner'), jQuery (elem).attr ('href'), _on_load2);
						}
						return false;
					};
					var on_popup_delete = function (url, elem, e) {
						if (can_popup ()) {
							jQuery ('div.dialog-data-delete').closest ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load = function (responseText, status, response) {
								jQuery ('div.dialog-form-delete').modal ();
								jQuery ('div.dialog-form-delete').fadeTo ('fast', 1);
							};
							ajax_load (jQuery ('div.dialog-data-delete'), jQuery (elem).attr ('href'), _on_load);
						}
						else {
							jQuery ('.inline_dialog').remove ();
							var elem2 = jQuery (("<tr class='refr_object inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML) + '</td></tr>');
							elem2.insertAfter (jQuery (elem).parents ('tr'));
							elem2.find ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load2 = function () {
								// pass;
							};
							ajax_load (jQuery ('div.dialog-data-inner'), jQuery (elem).attr ('href'), _on_load2);
						}
						return false;
					};
					var on_dialog_load = function () {
						// pass;
					};
					var _dialog_loaded = function (is_modal, elem) {
						var obj = elem.closest ('.refr_object');
						if (obj.length > 0) {
							if (obj [0].hasAttribute ('related-object')) {
								var btn = jQuery ('#' + obj.attr ('related-object'));
							}
							else {
								var btn = obj;
							}
							if (btn.hasClass ('no_cancel')) {
								obj.find ('.btn_cancel').hide ();
								obj.find ('.close').hide ();
							}
							else {
								obj.find ('.btn_cancel').show ();
								obj.find ('.close').show ();
							}
							if (btn.hasClass ('no_close')) {
								obj.find ('.close').hide ();
							}
							else {
								obj.find ('.close').show ();
							}
							if (btn.hasClass ('no_ok')) {
								obj.find ('.btn_ok').hide ();
							}
							else {
								obj.find ('.btn_ok').show ();
							}
						}
						if (is_modal) {
							jQuery ('div.dialog-form').fadeTo ('fast', 1);
							jQuery ('div.dialog-form').find ('.modal-dialog').removeClass ('modal-lg').removeClass ('modal-sm');
							var x = jQuery ('div.dialog-form').find ('div[name=modal-type-ref]');
							if (x.length > 0) {
								jQuery ('div.dialog-form').find ('.modal-dialog').addClass (x.attr ('class'));
							}
							jQuery ('div.dialog-form').modal ();
							jQuery ('div.dialog-form').drags (dict ({'handle': '.modal-header'}));
						}
					};
					var _refresh_win = function (responseText, ok_button) {
						var refr_obj = jQuery (ok_button).closest ('.refr_object');
						var popup_activator = jQuery ('#' + refr_obj.attr ('related-object'));
						if (responseText && __in__ ('RETURN_OK', responseText)) {
							if (refr_obj.hasClass ('modal')) {
								if (jQuery ('div.dialog-form').hasClass ('show')) {
									var dialog = 'div.dialog-form';
								}
								else if (jQuery ('div.dialog-form-delete').hasClass ('show')) {
									var dialog = 'div.dialog-form-delete';
								}
								else {
									var dialog = 'div.dialog-form-info';
								}
								var hide_dialog_form = function () {
									jQuery (dialog).modal ('hide');
								};
								jQuery (dialog).fadeTo ('slow', 0.5);
								if (!(refresh_fragment (popup_activator, hide_dialog_form, true))) {
									refresh_fragment (popup_activator, hide_dialog_form, false);
								}
							}
							else {
								if (refr_obj.hasClass ('inline_dialog')) {
									var inline_dialog = refr_obj;
								}
								else {
									var inline_dialog = refr_obj.find ('.inline_dialog');
								}
								if (inline_dialog.length > 0) {
									inline_dialog.remove ();
								}
								if (!(refresh_fragment (popup_activator, null, true))) {
									return refresh_fragment (popup_activator, null, false);
								}
							}
						}
						else if (refr_obj.hasClass ('modal')) {
							mount_html (jQuery ('div.dialog-data'), responseText);
						}
						else {
							mount_html (ok_button.closest ('.refr_target'), responseText);
						}
					};
					var _refresh_win_and_ret = function (responseText, ok_button) {
						if (responseText && __in__ ('RETURN_OK', responseText)) {
							var related_object = jQuery (ok_button).closest ('.refr_object').attr ('related-object');
							var popup_activator = jQuery ('#' + related_object);
							if (jQuery (ok_button).closest ('.refr_object').hasClass ('show')) {
								jQuery ('div.dialog-form').modal ('hide');
							}
							else {
								jQuery (ok_button).closest ('.refr_object').remove ();
							}
							if (popup_activator && popup_activator.data ('edit_ret_function')) {
								window.RET_CONTROL = popup_activator.data ('ret_control');
								window.EDIT_RET_FUNCTION = popup_activator.data ('edit_ret_function');
								var q = jQuery (('<div>' + responseText) + '</div>').find ('script');
								eval (q.text ());
							}
						}
						else {
							mount_html (jQuery ('div.dialog-data'), responseText);
						}
					};
					var _refresh_win_after_ok = function (responseText, ok_button) {
						var related_object = jQuery (ok_button).closest ('.refr_object').attr ('related-object');
						var popup_activator = jQuery ('#' + related_object);
						if (popup_activator && popup_activator.data ('edit_ret_function')) {
							window.EDIT_RET_FUNCTION = popup_activator.data ('edit_ret_function');
							window.EDIT_RET_FUNCTION (responseText, ok_button);
							window.EDIT_RET_FUNCTION = false;
						}
						else {
							_refresh_win (responseText, ok_button);
						}
					};
					var on_edit_ok = function (button, form) {
						if (form) {
							var f = form;
						}
						else {
							var f = jQuery (button).parent ().parent ().find ('form:first');
						}
						var _fun = function (data) {
							_refresh_win_after_ok (data, f);
						};
						if (f.length > 0) {
							ajax_submit (f, _fun);
						}
						else {
							_refresh_win ('RETURN_OK', jQuery (button));
						}
						return false;
					};
					window.on_edit_ok = on_edit_ok;
					var on_delete_ok = function (form) {
						var _on_data = function (data) {
							_refresh_win (data, form);
						};
						ajax_post (corect_href (form.attr ('action')), form.serialize (), _on_data);
						return false;
					};
					window.on_delete_ok = on_delete_ok;
					var on_cancel_inline = function (elem) {
						var refr = false;
						var inline_dialog = jQuery (elem).closest ('.inline_dialog');
						if (inline_dialog.length > 0) {
							var test = inline_dialog.find ('.refresh_after_close');
							if (test.length > 0) {
								var refr = true;
							}
						}
						jQuery ('body').removeClass ('shown_inline_dialog');
						if (refr) {
							_refresh_win ('RETURN_OK', inline_dialog.parent ());
						}
						else {
							inline_dialog.remove ();
							datatable_onresize ();
						}
					};
					window.on_cancel_inline = on_cancel_inline;
					var ret_ok = function (id, title) {
						var text = title;
						var ret_control = window.RET_CONTROL;
						if (ret_control.find (("option[value='" + id) + "']").length == 0) {
							ret_control.append (jQuery ('<option>', dict ({'value': id, 'text': text})));
						}
						ret_control.val (id.toString ());
						ret_control.trigger ('change');
					};
					var on_get_tbl_value = function (url, elem, e) {
						on_popup_in_form (elem);
					};
					var on_new_tbl_value = function (url, elem, e) {
						window.EDIT_RET_FUNCTION = _refresh_win_and_ret;
						window.RET_CONTROL = jQuery (elem).closest ('.input-group').find ('.django-select2');
						jQuery (elem).data ('edit_ret_function', window.EDIT_RET_FUNCTION);
						jQuery (elem).data ('ret_control', window.RET_CONTROL);
						return on_popup_edit_new (url, elem, e);
					};
					var on_get_row = function (url, elem, e) {
						var id = jQuery (elem).attr ('data-id');
						var text = jQuery (elem).attr ('data-text');
						var ret_control = jQuery (elem).closest ('.refr_source').prev ('.form-group').find ('.django-select2');
						if (ret_control.find (("option[value='" + id) + "']").length == 0) {
							ret_control.append (jQuery ('<option>', dict ({'value': id, 'text': text})));
						}
						ret_control.val (id.toString ());
						ret_control.trigger ('change');
						jQuery (elem).closest ('.refr_source').remove ();
					};
					var _init_subforms = function (elem) {
						var subforms = elem.find ('.subform_frame');
						var _load_subform = function (index, obj) {
							var content = jQuery (this).find ('.subform_content');
							if (content.length > 0) {
								var href = jQuery (this).attr ('href');
								var _finish = function () {
									// pass;
								};
								ajax_load (content, corect_href (href), _finish);
							}
						};
						subforms.each (_load_subform);
					};
					register_fragment_init_fun (_init_subforms);
					var refresh_current_object = function (url, elem, e) {
						var href = url;
						var href2 = corect_href (url);
						var target = 'refresh_obj';
						var src_obj = jQuery (elem);
						var refr_block = src_obj.closest ('.refr_object');
						if (refr_block.hasClass ('refr_source')) {
							var src = refr_block;
						}
						else {
							var src = refr_block.find ('.refr_source');
						}
						if (src.length > 0) {
							src.attr ('href', href2);
							src.attr ('action', href2);
						}
						var _on_data = function (data) {
							if (data && __in__ ('_parent_refr', data) || __in__ (target, tuple (['refresh_obj', 'refresh_page']))) {
								if (target == 'refresh_obj') {
									if (__in__ ('only_table', href)) {
										if (!(refresh_fragment (src_obj, null, true, data))) {
											refresh_fragment (src_obj, null, false, data);
										}
									}
									else {
										refresh_fragment (src_obj, null, false, data);
									}
								}
								else {
									refresh_fragment (src_obj, null, false, data);
								}
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
						if (src_obj.hasClass ('page-link')) {
							ajax_submit (src, _on_data);
						}
						else {
							ajax_get (href2, _on_data);
						}
					};
					var refresh_current_page = function (url, elem, e) {
						// pass;
					};
					var refresh_current_app = function (url, elem, e) {
						// pass;
					};
					var _none = function () {
						// pass;
					};
					var only_get = function (url, elem, e) {
						var href = url;
						var href2 = corect_href (url);
						var target = 'refresh_obj';
						var src_obj = jQuery (elem);
						var refr_block = src_obj.closest ('.refr_object');
						if (refr_block.hasClass ('refr_source')) {
							var src = refr_block;
						}
						else {
							var src = refr_block.find ('.refr_source');
						}
						if (src.length > 0) {
							src.attr ('href', href2);
							src.attr ('action', href2);
						}
						var _on_data = function (data) {
							if (data && __in__ ('_parent_refr', data) && __in__ ('YES', data) || __in__ ('OK', data)) {
								if (!(refresh_fragment (jQuery (elem), null, true))) {
									return refresh_fragment (jQuery (elem), null, false);
								}
							}
						};
						if (src_obj.hasClass ('page-link')) {
							ajax_submit (src, _on_data);
						}
						else {
							ajax_get (href2, _on_data);
						}
					};
					var popup_min_max = function (elm, max) {
						if (typeof max == 'undefined' || (max != null && max .hasOwnProperty ("__kwargtrans__"))) {;
							var max = true;
						};
						var elem = jQuery (elm);
						if (elem.hasClass ('modal-dialog')) {
							var popup = elem;
						}
						else {
							var popup = elem.closest ('.modal-dialog');
						}
						if (popup.length > 0) {
							var minimize = popup.find ('.minimize');
							var maximize = popup.find ('.maximize');
							if (minimize.length > 0) {
								if (max) {
									minimize.show ();
								}
								else {
									minimize.hide ();
								}
							}
							if (maximize.length > 0) {
								if (max) {
									maximize.hide ();
								}
								else {
									maximize.show ();
								}
							}
							if (max) {
								popup.addClass ('modal-fullscreen');
								popup.addClass ('modal-open');
							}
							else {
								popup.removeClass ('modal-fullscreen');
								popup.removeClass ('modal-open');
							}
							jQuery (window).trigger ('resize');
						}
					};
					var popup_minimize = function (elem) {
						return popup_min_max (elem, false);
					};
					window.popup_minimize = popup_minimize;
					var popup_maximize = function (elem) {
						return popup_min_max (elem, true);
					};
					window.popup_maximize = popup_maximize;
					jQuery.fn.modal.Constructor.prototype.enforceFocus = _none;
					__pragma__ ('<use>' +
						'tabmenu' +
						'tbl' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__._dialog_loaded = _dialog_loaded;
						__all__._init_subforms = _init_subforms;
						__all__._none = _none;
						__all__._refresh_win = _refresh_win;
						__all__._refresh_win_after_ok = _refresh_win_after_ok;
						__all__._refresh_win_and_ret = _refresh_win_and_ret;
						__all__.ajax_get = ajax_get;
						__all__.ajax_load = ajax_load;
						__all__.ajax_post = ajax_post;
						__all__.ajax_submit = ajax_submit;
						__all__.can_popup = can_popup;
						__all__.corect_href = corect_href;
						__all__.datatable_onresize = datatable_onresize;
						__all__.datatable_refresh = datatable_refresh;
						__all__.get_menu = get_menu;
						__all__.get_table_type = get_table_type;
						__all__.handle_class_click = handle_class_click;
						__all__.init_table = init_table;
						__all__.mount_html = mount_html;
						__all__.on_cancel_inline = on_cancel_inline;
						__all__.on_delete_ok = on_delete_ok;
						__all__.on_dialog_load = on_dialog_load;
						__all__.on_edit_ok = on_edit_ok;
						__all__.on_get_row = on_get_row;
						__all__.on_get_tbl_value = on_get_tbl_value;
						__all__.on_new_tbl_value = on_new_tbl_value;
						__all__.on_popup_delete = on_popup_delete;
						__all__.on_popup_edit_new = on_popup_edit_new;
						__all__.on_popup_in_form = on_popup_in_form;
						__all__.on_popup_info = on_popup_info;
						__all__.on_popup_inline = on_popup_inline;
						__all__.only_get = only_get;
						__all__.popup_maximize = popup_maximize;
						__all__.popup_min_max = popup_min_max;
						__all__.popup_minimize = popup_minimize;
						__all__.refresh_current_app = refresh_current_app;
						__all__.refresh_current_object = refresh_current_object;
						__all__.refresh_current_page = refresh_current_page;
						__all__.refresh_fragment = refresh_fragment;
						__all__.register_fragment_init_fun = register_fragment_init_fun;
						__all__.remove_page_from_href = remove_page_from_href;
						__all__.ret_ok = ret_ok;
					__pragma__ ('</all>')
				}
			}
		}
	);
