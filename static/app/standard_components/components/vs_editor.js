var _vseditor = function (resolve, reject) {
	var TEMPLATE = '        <div class=\"vseditorbase\">\n' +
    '                <button v-bind:disabled=\"!changed\" v-on:click=\"save\" class=\"btn btn-sm btn-primary\" style=\"position: absolute; z-index: 999;\">\n' +
    '                        <span class=\"fa fa-floppy-o\"></span>\n' +
    '                </button>\n' +
    '                <div style=\"width:100%; position:absolute; top:10px; text-align:center\">\n' +
    '                        <h5>{{ title }}</h5>\n' +
    '                </div>\n' +
    '                <div class=\"vseditor\" name=\"vseditor\" style=\"position: absolute; top:50px; left:5px; right:15px; bottom:10px;\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/vs';
	var _on_loadjs0 = function () {
		var _on_loadjs = function () {
			var props = list (['width', 'height', 'value', 'title', 'href']);
			var data = function () {
				return dict ({'changed': false});
			};
			var mounted = function () {
				var self = this;
				var _next = function () {
					var ed = jQuery (self.$el).find ('div.vseditor');
					var value = decodeURIComponent (escape (atob (self.value)));
					self.editor = monaco.editor.create (ed [0], dict ({'value': value, 'language': 'python', 'theme': 'vs-dark'}));
					var _changed = function (event) {
						self.changed = true;
					};
					self.editor.onDidChangeModelContent (_changed);
					var _on_resize = function (event) {
						self.editor.layout ();
					};
					jQuery (window).resize (_on_resize);
				};
				Vue.nextTick (_next);
			};
			var save = function (event) {
				var self = this;
				if (this.href) {
					var ajax_options = dict ({'method': 'POST', 'url': this.href, 'dataType': 'html', 'data': dict ({'data': this.editor.getValue ()})});
					var _on_ajax = function () {
						self.changed = false;
					};
					jQuery.ajax (ajax_options).done (_on_ajax);
				}
			};
			var methods = dict ({'save': save});
			resolve (dict ({'props': props, 'template': TEMPLATE, 'mounted': mounted, 'data': data, 'methods': methods}));
		};
		require.config (dict ({'paths': dict ({'vs': base_path})}));
		require (list (['vs/editor/editor.main']), _on_loadjs);
	};
	console.log ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
	load_many_js ((((base_path + '/../../system/require.js') + ';') + base_path) + '/loader.js', _on_loadjs0);
};
Vue.component ('sch-vseditor', _vseditor);
