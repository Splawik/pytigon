var __name__ = '__main__';
var _codeeditor = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/ace/src-min';
	var _on_loadjs = function () {
		var props = list (['width', 'height', 'value', 'title', 'href']);
		var template = '                <div>\n' +
    '                        <div class=\"inline\" v-bind:style=\"style_inline\">\n' +
    '                                        <button v-bind:disabled=\"!changed\" v-on:click=\"save\" class=\"btn btn-sm btn-primary\" v-bind:style=\"style_btn\">\n' +
    '                                                <span class=\"fa fa-floppy-o\" />\n' +
    '                                        </button>\n' +
    '                        </div>\n' +
    '                        <div class=\"inline inline_title\" v-bind:style=\"style_title\">\n' +
    '                                <strong>{{ title }}</strong>\n' +
    '                        </div>\n' +
    '                        <div class=\"ceditor\" name=\"ceditor\"></div>\n' +
    '                </div>\n' +
    '\n' +
    '';
		var data = function () {
			return dict ({'style_inline': dict ({'display': 'inline-block'}), 'style_btn': dict ({'margin-left': '0px'}), 'style_title': dict ({'ma rgin-left': '10px'}), 'changed': false});
		};
		var mounted = function () {
			var self = this;
			ace.config.set ('basePath', base_path);
			var editor = ace.edit (jQuery (this.$el).find ('div.ceditor') [0]);
			var rect = editor.container.getBoundingClientRect ();
			editor.container.style.position = 'absolute';
			editor.container.style.top = (rect.top + 2) + 'px';
			editor.container.style.right = '5px';
			editor.container.style.bottom = '5px';
			editor.container.style.left = '5px';
			editor.setTheme ('ace/theme/textmate');
			editor.getSession ().setMode ('ace/mode/python');
			editor.setOptions (dict ({'minLines': 32}));
			var _on_input = function (e) {
				var f = jQuery (':focus');
				if (f.length > 0) {
					var tag = f.get (0).nodeName.toLowerCase ();
				}
				else {
					tag == '';
				}
				if (tag == 'textarea') {
					self.changed = true;
				}
				else {
					var _on_timeout = function () {
						editor.focus ();
					};
					setTimeout (_on_timeout, 0);
				}
			};
			editor.on ('input', _on_input);
			if (self.value) {
				editor.getSession ().setValue (atob (self.value));
			}
			self.editor = editor;
		};
		var save = function () {
			if (this.href) {
				var ajax_options = dict ({'method': 'POST', 'url': this.href, 'dataType': 'html', 'data': dict ({'data': self.editor.getValue ()})});
				var _on_ajax = function () {
					self.changed = false;
				};
				jQuery.ajax (ajax_options).done (_on_ajax);
			}
		};
		var methods = dict ({'save': save});
		resolve (dict ({'props': props, 'template': template, 'mounted': mounted, 'data': data, 'methods': methods}));
	};
	load_js (base_path + '/ace.js', _on_loadjs);
};
Vue.component ('sch-codeeditor', _codeeditor);
