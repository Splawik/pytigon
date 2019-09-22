	__nest__ (
		__all__,
		'tabmenu', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tabmenu';
					var Page = __init__ (__world__.page).Page;
					var TabMenuItem = __init__ (__world__.tabmenuitem).TabMenuItem;
					var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
					var history_push_state = __init__ (__world__.tools).history_push_state;
					var mount_html = __init__ (__world__.tools).mount_html;
					var TabMenu = __class__ ('TabMenu', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.id = 0;
							self.titles = dict ({});
							self.active_item = null;
						});},
						get get_active_item () {return __get__ (this, function (self) {
							return self.active_item;
						});},
						get is_open () {return __get__ (this, function (self, title) {
							if (self.titles && __in__ (title, self.titles) && self.titles [title]) {
								return true;
							}
							else {
								return false;
							}
						});},
						get activate () {return __get__ (this, function (self, title, push_state) {
							if (typeof push_state == 'undefined' || (push_state != null && push_state .hasOwnProperty ("__kwargtrans__"))) {;
								var push_state = true;
							};
							var menu_item = self.titles [title];
							jQuery (sprintf ('#li_%s a', menu_item.id)).tab ('show');
							if (push_state && window.PUSH_STATE) {
								history_push_state (menu_item.title, menu_item.url);
							}
							datatable_onresize ();
						});},
						get new_page () {return __get__ (this, function (self, title_alternate, data, href) {
							var _id = 'tab' + self.id;
							var tmp = jQuery (data).find ('header').find ('title').text ();
							var title = jQuery.trim (tmp);
							if (!(title)) {
								var title = title_alternate;
							}
							var title2 = jQuery.trim (title);
							var menu_item = TabMenuItem (_id, title2, href, data);
							self.titles [title2] = menu_item;
							var menu_pos = vsprintf ("<li id='li_%s' class ='nav-item'><a href='#%s' class='nav-link bg-info' data-toggle='tab' role='tab' title='%s'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-outline-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", list ([_id, _id, title2, title2, _id]));
							var append_left = jQuery ('#tabs2').hasClass ('append-left');
							if (append_left) {
								jQuery ('#tabs2').prepend (menu_pos);
							}
							else {
								jQuery ('#tabs2').append (menu_pos);
							}
							jQuery ('#tabs2_content').append (sprintf ("<div class='tab-pane container-fluid refr_target refr_object win-content page' id='%s'></div>", _id));
							window.ACTIVE_PAGE = Page (_id, jQuery ('#' + _id));
							self.active_item = menu_item;
							if (window.PUSH_STATE) {
								history_push_state (title2, href);
							}
							var _on_show_tab = function (e) {
								window.ACTIVE_PAGE = Page (_id, jQuery ('#' + _id), menu_item);
								var menu = get_menu ();
								menu_item = menu.titles [jQuery.trim (e.target.text)];
								self.active_item = menu_item;
								if (window.PUSH_STATE) {
									history_push_state (menu_item.title, menu_item.url);
								}
							};
							if (append_left) {
								jQuery ('#tabs2 a:first').on ('shown.bs.tab', _on_show_tab);
								jQuery ('#tabs2 a:first').tab ('show');
							}
							else {
								jQuery ('#tabs2 a:last').on ('shown.bs.tab', _on_show_tab);
								jQuery ('#tabs2 a:last').tab ('show');
							}
							mount_html (jQuery ('#' + _id), data);
							var _on_button_click = function (event) {
								get_menu ().remove_page (jQuery (this).attr ('id').py_replace ('button_', ''));
							};
							jQuery (sprintf ('#button_%s', _id)).click (_on_button_click);
							var scripts = jQuery (('#' + _id) + ' script');
							var _local_fun = function (index, element) {
								eval (this.innerHTML);
							};
							scripts.each (_local_fun);
							self.id++;
							return _id;
						});},
						get remove_page () {return __get__ (this, function (self, id) {
							var _on_remove = function (index, value) {
								value.on_remove ();
							};
							jQuery.each (jQuery ('#' + id).find ('.call_on_remove'), _on_remove);
							var _local_fun = function (index, value) {
								if (value && value.id == id) {
									self.titles [index] = null;
								}
							};
							jQuery.each (self.titles, _local_fun);
							jQuery (sprintf ('#li_%s', id)).remove ();
							jQuery (sprintf ('#%s', id)).remove ();
							var last_a = jQuery ('#tabs2 a:last');
							if (last_a.length > 0) {
								last_a.tab ('show');
							}
							else {
								window.ACTIVE_PAGE = null;
								if (window.PUSH_STATE) {
									history_push_state ('', window.BASE_PATH);
								}
								if (jQuery ('#wiki_start').find ('.content').length == 0) {
									window.init_start_wiki_page ();
								}
								jQuery ('#wiki_start').show ();
							}
						});}
					});
					var get_menu = function () {
						if (!(window.MENU)) {
							window.MENU = TabMenu ();
						}
						return window.MENU;
					};
					__pragma__ ('<use>' +
						'page' +
						'tabmenuitem' +
						'tbl' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.Page = Page;
						__all__.TabMenu = TabMenu;
						__all__.TabMenuItem = TabMenuItem;
						__all__.__name__ = __name__;
						__all__.datatable_onresize = datatable_onresize;
						__all__.get_menu = get_menu;
						__all__.history_push_state = history_push_state;
						__all__.mount_html = mount_html;
					__pragma__ ('</all>')
				}
			}
		}
	);
