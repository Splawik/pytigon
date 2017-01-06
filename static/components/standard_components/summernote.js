
		var _htmleditor = function (resolve, reject) {
			var base_path = window.BASE_PATH + 'static/bootstrap_plugins/summernote';
			var _on_loadjs = function () {
				var props = list (['width', 'height', 'value', 'title', 'href']);
				var template = '\n        <div>\n            <div class="inline" v-bind:style="style_inline">\n                    <button v-bind:disabled="!changed" v-on:click="save" class="btn btn-sm btn-primary" v-bind:style="style_btn">\n                        <span class="fa fa-floppy-o" />\n                    </button>\n            </div>\n            <div class="inline inline_title" v-bind:style="style_title">\n                <strong>{{ title }}</strong>\n            </div>\n            <div class="htmleditor" name="htmleditor"></div>\n        </div>    \n        ';
				var data = function () {
					return dict ({'style_inline': dict ({'display': 'inline-block'}), 'style_btn': dict ({'margin-left': '0px'}), 'style_title': dict ({'ma rgin-left': '10px'}), 'changed': false});
				};
				var mounted = function () {
					var self = this;
					var editor = jQuery (this.$el).find ('div.htmleditor');
					var rect = editor [0].getBoundingClientRect ();
					editor.css (dict ({'position': 'absolute', 'top': (rect.top + 2) + 'px', 'bottom': '5px', 'left': '5px', 'right': '5px'}));
					if (self.value) {
						editor.html (atob (self.value));
					}
					editor.summernote ();
					self.editor = editor;
				};
				var save = function () {
					var self = this;
					if (this.href) {
						var ajax_options = dict ({'method': 'POST', 'url': this.href, 'dataType': 'html', 'data': dict ({'data': self.editor.summernote ('code')})});
						var _on_ajax = function () {
							self.changed = false;
						};
						jQuery.ajax (ajax_options).done (_on_ajax);
					}
				};
				var methods = dict ({'save': save});
				resolve (dict ({'props': props, 'template': template, 'mounted': mounted, 'data': data, 'methods': methods}));
			};
			load_js (base_path + '/summernote.min.js', _on_loadjs);
			load_css (base_path + '/summernote.css');
		};
		Vue.component ('sch-htmleditor', _htmleditor);
		__pragma__ ('<all>')
			__all__._htmleditor = _htmleditor;
		__pragma__ ('</all>')
	