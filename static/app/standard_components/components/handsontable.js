var _handsontable = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/jquery_plugins';
	var _on_loadjs = function () {
		var props = list (['width', 'height']);
		var template = "<div name='handsontablediv' v-bind:style='{ width: width, height: height }' ></div>";
		var mounted = function () {
			var self = this;
			var data = list ([list (['Column A', 'Column B', 'Column C']), list (['1', '2', '3'])]);
			var htable = new window.Handsontable (this.$el, dict ({'data': data}));
			self.htable = htable;
		};
		resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
	};
	load_js (base_path + '/handsontable.full.js', _on_loadjs);
	load_css (base_path + '/handsontable.full.css');
};
Vue.component ('sch-handsontable', _handsontable);
