	__nest__ (
		__all__,
		'tbl', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tbl';
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var register_fragment_init_fun = __init__ (__world__.tools).register_fragment_init_fun;
					var get_table_type = __init__ (__world__.tools).get_table_type;
					var load_js = __init__ (__world__.tools).load_js;
					var mount_html = __init__ (__world__.tools).mount_html;
					var datetable_set_height = function () {
						if (jQuery (this).hasClass ('table_get')) {
							return ;
						}
						if (!(jQuery (this).is (':visible'))) {
							return ;
						}
						var elem = jQuery (this).closest ('.tabsort_panel');
						var table_offset = elem.offset ().top;
						var dy_win = jQuery (window).height ();
						var dy = dy_win - table_offset;
						if (dy < 200) {
							var dy = 200;
						}
						var panel = elem.find ('.fixed-table-toolbar');
						if (!(panel.is (':visible'))) {
							dy += panel.height () - 15;
						}
						jQuery (this).bootstrapTable ('resetView', dict ({'height': dy - 5}));
					};
					var datatable_refresh = function (table) {
						table.bootstrapTable ('refresh');
					};
					var _rowStyle = function (value, row, index) {
						var x = jQuery (('<div>' + value ['cid']) + '</div>').find ('div.td_information');
						if (x.length > 0) {
							var c = x.attr ('class').py_replace ('td_information', '');
							if (c.length > 0) {
								return dict ({'classes': c});
							}
						}
						return dict ({});
					};
					var prepare_datatable = function (table) {
						var _local_fun = function (index) {
							var td = jQuery (this).parent ();
							var tr = td.parent ();
							var l = tr.find ('td').length;
							tr.find ('td:gt(0)').remove ();
							td.attr ('colspan', l);
						};
						table.find ('div.second_row').each (_local_fun);
					};
					var datatable_ajax = function (params) {
						var url = params ['url'];
						var success = params ['success'];
						if (__in__ ('form', dict (params ['data']))) {
							var form = params ['data'] ['form'];
							delete params ['data'] ['form'];
							var d = jQuery.param (params ['data']);
							url += '?' + d;
							var _on_post_data = function (data) {
								var d2 = JSON.parse (data);
								success (d2);
							};
							ajax_post (url, form, _on_post_data);
						}
						else {
							var d = jQuery.param (params ['data']);
							url += '?' + d;
							var _on_get_data = function (data) {
								var d2 = JSON.parse (data);
								success (d2);
							};
							ajax_get (url, _on_get_data);
						}
					};
					var init_table = function (table, table_type) {
						if (table_type == 'datatable') {
							var onLoadSuccess = function (data) {
								prepare_datatable (table);
								var _pagination = function () {
									jQuery (table).closest ('.fixed-table-container').find ('.fixed-table-pagination ul.pagination a').addClass ('page-link');
									datatable_onresize ();
								};
								setTimeout (_pagination, 0);
								return false;
							};
							var queryParams = function (p) {
								var refr_block = jQuery (table).closest ('.refr_object');
								var src = refr_block.find ('.refr_source');
								if (src.length > 0 && src.prop ('tagName') == 'FORM') {
									p ['form'] = src.serialize ();
								}
								return p;
							};
							if (table.hasClass ('table_get')) {
								table.bootstrapTable (dict ({'onLoadSuccess': onLoadSuccess, 'height': 350, 'rowStyle': _rowStyle, 'queryParams': queryParams, 'ajax': datatable_ajax}));
							}
							else {
								table.bootstrapTable (dict ({'onLoadSuccess': onLoadSuccess, 'rowStyle': _rowStyle, 'queryParams': queryParams, 'ajax': datatable_ajax}));
							}
							var table_panel = jQuery (table).closest ('.content');
							var btn = table_panel.find ('.tabsort-toolbar-expand');
							if (btn) {
								var _handle_toolbar_expand = function (elem) {
									var panel = table_panel.find ('.fixed-table-toolbar');
									if (jQuery (this).hasClass ('active')) {
										panel.show ();
										datatable_onresize ();
									}
									else {
										panel.hide ();
										datatable_onresize ();
									}
								};
								table_panel.on ('click', '.tabsort-toolbar-expand', _handle_toolbar_expand);
								if (btn.hasClass ('active')) {
									var panel = table_panel.find ('.fixed-table-toolbar');
									panel.hide ();
									datatable_onresize ();
								}
							}
						}
					};
					var content_set_height = function () {
						if (!(jQuery (this).is (':visible'))) {
							return ;
						}
						if (jQuery (this).closest ('.tabsort').length > 0) {
							return ;
						}
						if (jQuery (this).closest ('#dialog-form-modal').length > 0) {
							return ;
						}
						var content_offset = jQuery (this).offset ().top;
						var dy_win = jQuery (window).height ();
						var dy = (dy_win - content_offset) - 30;
						if (dy < 200) {
							var dy = 200;
						}
						jQuery (this).height (dy);
					};
					var datatable_onresize = function () {
						jQuery ('.datatable:not(.table_get)').each (datetable_set_height);
						jQuery ('.content').each (content_set_height);
					};
					window.datatable_onresize = datatable_onresize;
					var _on_fragment_init = function (elem) {
						datatable_onresize ();
						var table_type = get_table_type (elem);
						var tbl = elem.find ('.tabsort');
						if (tbl.length > 0) {
							init_table (tbl, table_type);
						}
					};
					register_fragment_init_fun (_on_fragment_init);
					__pragma__ ('<use>' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__._on_fragment_init = _on_fragment_init;
						__all__._rowStyle = _rowStyle;
						__all__.ajax_post = ajax_post;
						__all__.content_set_height = content_set_height;
						__all__.datatable_ajax = datatable_ajax;
						__all__.datatable_onresize = datatable_onresize;
						__all__.datatable_refresh = datatable_refresh;
						__all__.datetable_set_height = datetable_set_height;
						__all__.get_table_type = get_table_type;
						__all__.init_table = init_table;
						__all__.load_js = load_js;
						__all__.mount_html = mount_html;
						__all__.prepare_datatable = prepare_datatable;
						__all__.register_fragment_init_fun = register_fragment_init_fun;
					__pragma__ ('</all>')
				}
			}
		}
	);
