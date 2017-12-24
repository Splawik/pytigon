var __name__ = '__main__';
var _plotly = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins';
	var _on_loadjs = function () {
		var props = list (['width', 'height']);
		var template = "<div name='plotlydiv' v-bind:style='{ width: width, height: height} ></div>";
		var mounted = function () {
			var data = list ([dict ({'values': list ([19, 26, 55]), 'labels': list (['Residential', 'Non-Residential', 'Utility']), 'type': 'pie'})]);
			var layout = dict ({'height': 400, 'width': 500});
			var plot = Plotly.newPlot (this.$el, data, layout, dict ({'displayModeBar': true, 'showLink': false, 'displaylogo': false, 'scrollZoom': true, 'modeBarButtonsToRemove': list (['sendDataToCloud'])}));
			this.plot = plot;
		};
		resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
	};
	load_js (base_path + '/plotly-latest.min.js', _on_loadjs);
};
Vue.component ('sch-plotly', _plotly);
