var _summertextarea = function (resolve, reject) {
	var TEMPLATE = '        <div class=\"summertextareabase border rounded\" v-bind:height=\"height\">\n' +
    '                <textarea class=\"summernotearea\" v-bind:name=\"name\" v-bind:id=\"id\"></textarea>\n' +
    '        </div>\n' +
    '\n' +
    '';
	var base_path = window.BASE_PATH + 'static/bootstrap_plugins/summernote';
	var _on_loadjs = function () {
		var props = list (['width', 'height', 'value', 'name', 'id']);
		var data = function () {
			return dict ({});
		};
		var mounted = function () {
			var self = this;
			var _next = function () {
				var ed = jQuery (self.$el).find ('textarea.summernotearea');
				if (self.height) {
					var h = self.height;
				}
				else {
					var h = 150;
				}
				var options = dict ({'height': 150, 'toolbar': list ([list (['undo', list (['undo'])]), list (['redo', list (['redo'])]), list (['style', list (['bold', 'italic', 'underline', 'clear'])]), list (['color', list (['color'])]), list (['picture', list (['picture'])])]), 'codemirror': dict ({'theme': 'monokai'}), 'icons': dict ({'align': 'fa fa-align-left', 'alignCenter': 'note-icon-align-center', 'alignJustify': 'note-icon-align-justify', 'alignLeft': 'note-icon-align-left', 'alignRight': 'note-icon-align-right', 'rowBelow': 'note-icon-row-below', 'colBefore': 'note-icon-col-before', 'colAfter': 'note-icon-col-after', 'rowAbove': 'note-icon-row-above', 'rowRemove': 'note-icon-row-remove', 'colRemove': 'note-icon-col-remove', 'indent': 'note-icon-align-indent', 'outdent': 'note-icon-align-outdent', 'arrowsAlt': 'note-icon-arrows-alt', 'bold': 'fa fa-bold', 'caret': 'note-icon-caret', 'circle': 'note-icon-circle', 'close': 'note-icon-close', 'code': 'note-icon-code', 'eraser': 'fa fa-eraser', 'font': 'fa fa-font', 'frame': 'note-icon-frame', 'italic': 'fa fa-italic', 'link': 'note-icon-link', 'unlink': 'note-icon-chain-broken', 'magic': 'note-icon-magic', 'menuCheck': 'note-icon-menu-check', 'minus': 'note-icon-minus', 'orderedlist': 'note-icon-orderedlist', 'pencil': 'note-icon-pencil', 'picture': 'fa fa-file-image-o', 'question': 'note-icon-question', 'redo': 'fa fa-repeat', 'square': 'note-icon-square', 'strikethrough': 'note-icon-strikethrough', 'subscript': 'note-icon-subscript', 'superscript': 'note-icon-superscript', 'table': 'note-icon-table', 'textHeight': 'note-icon-text-height', 'trash': 'note-icon-trash', 'underline': 'fa fa-underline', 'undo': 'fa fa-undo', 'unorderedlist': 'note-icon-unorderedlist', 'video': 'note-icon-video'})});
				ed.summernote (options);
				var value = decodeURIComponent (escape (atob (self.value)));
				ed.summernote ('code', value);
				var color_button = jQuery (self.$el).find ('.note-current-color-button');
				color_button.data ('value', dict ({'backColor': 'white'}));
				var recent_color = color_button.find ('.note-recent-color');
				recent_color.css (dict ({'background-color': 'white'}));
			};
			Vue.nextTick (_next);
		};
		var methods = dict ({});
		resolve (dict ({'props': props, 'template': TEMPLATE, 'mounted': mounted, 'data': data, 'methods': methods}));
	};
	load_js (base_path + '/summernote-bs4.min.js', _on_loadjs);
	load_css (base_path + '/summernote-bs4.css');
	load_css (window.BASE_PATH + 'static/app/standard_components/summernote_add.css');
};
Vue.component ('summertextarea', _summertextarea);
