var _pivot = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/jquery_plugins/pivottable';
	var _on_loadjs = function () {
		var props = list (['width', 'height']);
		var template = "<div name='pivotdiv' v-bind:style='{ width: width, height: height} ></div>";
		var mounted = function () {
			var data = list ([dict ({'color': 'blue', 'shape': 'circle'}), dict ({'color': 'red', 'shape': 'triangle'})]);
			var options = dict ({'rows': list (['color']), 'cols': list (['shape'])});
			var pivottable = jQuery (this.$el).pivotUI (data, options);
			this.pivottable = pivottable;
		};
		resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
	};
	load_many_js ((((base_path + '/pivot.js') + ';') + base_path) + '/../jquery.ui/jquery-ui.min.js', _on_loadjs);
	load_css (base_path + '/pivot.css');
};
Vue.component ('sch-pivottable', _pivot);
