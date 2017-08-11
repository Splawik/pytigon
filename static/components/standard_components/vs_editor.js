var _vseditor = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/vs';
	var _on_loadjs0 = function () {
		var _on_loadjs = function () {
			var props = list (['width', 'height', 'value', 'title', 'href']);
			var template = '\n            <div>\n                <div class="inline" v-bind:style="style_inline">\n                        <button v-bind:disabled="!changed" v-on:click="save" class="btn btn-sm btn-primary" v-bind:style="style_btn">\n                            <span class="fa fa-floppy-o" />\n                        </button>\n                </div>\n                <div class="inline inline_title" v-bind:style="style_title">\n                    <strong>{{ title }}</strong>\n                </div>\n                <div class="vseditor" name="vseditor"></div>\n            </div>    \n            ';
			var data = function () {
				return dict ({'style_inline': dict ({'display': 'inline-block'}), 'style_btn': dict ({'margin-left': '0px'}), 'style_title': dict ({'ma rgin-left': '10px'}), 'changed': false});
			};
			var mounted = function () {
				var self = this;
				var _next = function () {
					var ed = jQuery (self.$el).find ('div.vseditor');
					var rect = ed [0].getBoundingClientRect ();
					ed.css (dict ({'position': 'absolute', 'top': (rect.top + 2) + 'px', 'bottom': '30px', 'left': '5px', 'right': '25px'}));
					self.editor = monaco.editor.create (ed [0], dict ({'value': atob (self.value), 'language': 'python'}));
					var _changed = function (event) {
						self.changed = true;
					};
					self.editor.onDidChangeModelContent (_changed);
				};
				Vue.nextTick (_next);
			};
			var save = function () {
				if (this.href) {
					var ajax_options = dict ({'method': 'POST', 'url': this.href, 'dataType': 'html', 'data': dict ({'data': self.editor.getValue ()})});
					var _on_ajax = function () {
						this.changed = false;
					};
					jQuery.ajax (ajax_options).done (_on_ajax);
				}
			};
			var methods = dict ({'save': save});
			resolve (dict ({'props': props, 'template': template, 'mounted': mounted, 'data': data, 'methods': methods}));
		};
		require.config (dict ({'paths': dict ({'vs': base_path})}));
		require (list (['vs/editor/editor.main']), _on_loadjs);
	};
	load_many_js ((((base_path + '/../../system/require.js') + ';') + base_path) + '/loader.js', _on_loadjs0);
};
Vue.component ('sch-vseditor', _vseditor);
__pragma__ ('<all>')
	__all__._vseditor = _vseditor;
__pragma__ ('</all>')
