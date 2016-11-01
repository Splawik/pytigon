
		var __symbols__ = ['__esv5__'];
		var _d3 = function (resolve, reject) {
			var base_path = window.BASE_PATH + 'static/vanillajs_plugins';
			var _on_loadjs = function () {
				var props = list (['width', 'height']);
				var template = "<div name='d3div' v-bind:style='{ width: width, height: height}' ></div>";
				var mounted = function () {
					var sampleSVG = d3.select (this.$el).append ('svg').attr ('width', 100).attr ('height', 100);
					var _on_mouseover = function () {
						d3.select (this).style ('fill', 'aliceblue');
					};
					var _on_mouseout = function () {
						d3.select (this).style ('fill', 'white');
					};
					sampleSVG.append ('circle').style ('stroke', 'gray').style ('fill', 'white').attr ('r', 40).attr ('cx', 50).attr ('cy', 50).on ('mouseover', _on_mouseover).on ('mouseout', _on_mouseout);
				};
				resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
			};
			load_js (base_path + '/plotly-latest.min.js', _on_loadjs);
		};
		Vue.component ('sch-d3', _d3);
		__pragma__ ('<all>')
			__all__._d3 = _d3;
		__pragma__ ('</all>')
	