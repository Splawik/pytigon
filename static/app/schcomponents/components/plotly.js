var __name__ = '__main__';
var from_dict = function (d, py_name) {
	if (__in__ (py_name, d)) {
		return d [py_name];
	}
	else {
		return dict ({});
	}
};
var transform_event_data = function (data) {
	var ret = dict ({});
	if (__in__ ('destination', data)) {
		ret ['destination'] = data ['destination'];
	}
	if (__in__ ('event_name', data)) {
		ret ['event_name'] = data ['event_name'];
	}
	if (__in__ ('points', data)) {
		var pp = list ([]);
		var __iterable0__ = data ['points'];
		for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
			var point = __iterable0__ [__index0__];
			var p = dict ({});
			var __iterable1__ = list (['curveNumber', 'pointNumber', 'x', 'y', 'z', 'lat', 'lon']);
			for (var __index1__ = 0; __index1__ < len (__iterable1__); __index1__++) {
				var key = __iterable1__ [__index1__];
				if (point.hasOwnProperty (key)) {
					p [key] = point [key];
				}
			}
			pp.append (p);
		}
		ret ['points'] = pp;
	}
	return ret;
};
var _plotly = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins';
	var base_plotly_path = window.BASE_PATH + 'schreports/plot_service/';
	var _on_loadjs = function () {
		var props = list (['width', 'height', 'plotlyName', 'param']);
		var template = "<div name='plotlydiv' v-bind:style='{ width: width, height: height} ></div>";
		var process_response_data = function (this_obj, data) {
			if (__in__ ('redirect', data) && data ['redirect']) {
				data ['redirect'] = false;
				global_vue_bus.$emit ('plotly', data);
			}
			else if (__in__ ('function', data)) {
				var fun = data ['function'];
				var el = this_obj.$el;
				var layout = from_dict (data, 'layout');
				if (this_obj.width) {
					layout ['width'] = this_obj.width;
				}
				if (this_obj.height) {
					layout ['height'] = this_obj.height;
				}
				if (fun == 'newPlot') {
					Plotly.newPlot (el, from_dict (data, 'data'), layout, from_dict (data, 'config'));
				}
				else if (fun == 'react') {
					Plotly.react (el, from_dict (data, 'data'), layout, from_dict (data, 'config'));
				}
				else if (fun == 'restyle') {
					if (__in__ ('traceIndices', data)) {
						Plotly.restyle (el, from_dict (data, 'update'), from_dict (data, 'traceIndices'));
					}
					else {
						Plotly.restyle (el, from_dict (data, 'update'));
					}
				}
				else if (fun == 'relayout') {
					Plotly.relayout (el, from_dict (data, 'update'));
				}
				else if (fun == 'update') {
					if (__in__ ('traceIndices', data)) {
						Plotly.restyle (el, from_dict (data, 'data'), from_dict (data, 'layout'), from_dict (data, 'traceIndices'));
					}
					else {
						Plotly.restyle (el, from_dict (data, 'data'), from_dict (data, 'layout'));
					}
				}
				else if (fun == 'addTraces') {
					if (__in__ ('id', data)) {
						Plotly.addTraces (el, from_dict (data, 'traces'), data ['id']);
					}
					else {
						Plotly.addTraces (el, from_dict (data, 'traces'));
					}
				}
				else if (fun == 'deleteTraces') {
					Plotly.deleteTraces (el, from_dict (data, 'traceIndices'));
				}
				else if (fun == 'moveTraces') {
					if (__in__ ('id', data)) {
						Plotly.moveTraces (el, from_dict (data, 'traceIndices'), data ['id']);
					}
					else {
						Plotly.moveTraces (el, from_dict (data, 'traceIndices'));
					}
				}
				else if (fun == 'extendTraces') {
					Plotly.extendTraces (el, from_dict (data, 'traces'), from_dict (data, 'traceIndices'));
				}
				else if (fun == 'prependTraces') {
					Plotly.prependTraces (el, from_dict (data, 'traces'), from_dict (data, 'traceIndices'));
				}
				else if (fun == 'addFrames') {
					// pass;
				}
				else if (fun == 'animate') {
					// pass;
				}
			}
		};
		var mounted = function () {
			var url = (base_plotly_path + this.plotlyName) + '/';
			if (this.param) {
				url += '?param=' + this.param;
			}
			var this_obj = this;
			var data = null;
			var layout = null;
			var config = null;
			var events = null;
			var on_loaded = function () {
				if (this_obj.width) {
					layout ['width'] = this_obj.width;
				}
				if (this_obj.height) {
					layout ['height'] = this_obj.height;
				}
				var plot = Plotly.newPlot (this_obj.$el, data, layout, config);
				this_obj.plot = plot;
				var el = this_obj.$el;
				if (window.hasOwnProperty ('MOUNTED_COMPONENTS')) {
					window.MOUNTED_COMPONENTS++;
				}
				if (events) {
					var __iterable0__ = events;
					for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
						var pos = __iterable0__ [__index0__];
						if (__in__ ('=>', pos)) {
							var x = pos.py_split ('=>');
							var _callback = function (data1) {
								data1 ['destination'] = x [1];
								data1 ['event_name'] = x [0];
								global_vue_bus.$emit ('plotly', data1);
							};
							el.on ('plotly_' + x [0], _callback);
						}
						else {
							var make_callback = function (event_name) {
								var _callback = function (data2) {
									data2 ['event_name'] = event_name;
									var _on_server_response = function (server_data) {
										server_data ['event_name'] = event_name;
										process_response_data (this_obj, server_data);
									};
									ajax_json (url, dict ({'name': this_obj.plotlyName, 'action': 'on_event', 'event_name': event_name, 'data': transform_event_data (data2)}), _on_server_response);
								};
								return _callback;
							};
							el.on ('plotly_' + pos, make_callback (pos));
						}
					}
				}
			};
			var on_data_loaded = function (_data) {
				data = _data ['data'];
				if (__in__ ('events', _data)) {
					events = _data ['events'];
				}
				if (layout != null && config != null) {
					on_loaded ();
				}
			};
			var on_layout_loaded = function (_data) {
				layout = _data;
				if (data != null && config != null) {
					on_loaded ();
				}
			};
			var on_config_loaded = function (_data) {
				config = _data;
				if (data != null && layout != null) {
					on_loaded ();
				}
			};
			ajax_json (url, dict ({'name': this_obj.plotlyName, 'action': 'get_data'}), on_data_loaded);
			ajax_json (url, dict ({'name': this_obj.plotlyName, 'action': 'get_layout'}), on_layout_loaded);
			ajax_json (url, dict ({'name': this_obj.plotlyName, 'action': 'get_config'}), on_config_loaded);
		};
		var created = function () {
			var this_obj = this;
			var on_event = function (data) {
				if (__in__ ('destination', data) && data ['destination'] == ('plotly/' + this_obj.plotlyName) + '/') {
					process_response_data (this_obj, data);
				}
			};
			global_vue_bus.$on ('plotly', on_event);
		};
		resolve (dict ({'props': props, 'template': template, 'created': created, 'mounted': mounted}));
	};
	load_js (base_path + '/plotly-latest.min.js', _on_loadjs);
};
Vue.component ('sch-plotly', _plotly);
