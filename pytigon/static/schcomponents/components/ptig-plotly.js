// Transcrypt'ed from Python, 2020-11-26 18:34:20
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-plotly';
export var TEMPLATE = '        <div name=\"plotlydiv\" data-bind:style-width:width;style-height:height></div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins';
export var BASE_PLOTLY_PATH = window.BASE_PATH + 'schreports/plot_service/';
export var from_dict = function (d, py_name) {
	if (__in__ (py_name, d)) {
		return d [py_name];
	}
	else {
		return dict ({});
	}
};
export var transform_event_data = function (data) {
	var ret = dict ({});
	if (__in__ ('destination', data)) {
		ret ['destination'] = data ['destination'];
	}
	if (__in__ ('event_name', data)) {
		ret ['event_name'] = data ['event_name'];
	}
	if (__in__ ('points', data)) {
		var pp = [];
		for (var point of data ['points']) {
			var p = dict ({});
			for (var key of ['curveNumber', 'pointNumber', 'x', 'y', 'z', 'lat', 'lon']) {
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
export var process_response_data = function (component, data) {
	if (__in__ ('redirect', data) && data ['redirect']) {
		data ['redirect'] = false;
		window.GLOBAL_BUS.emit (new set (['plotly', data]));
	}
	else if (__in__ ('function', data)) {
		var fun = data ['function'];
		var el = component.div;
		var layout = from_dict (data, 'layout');
		if (component.width) {
			layout ['width'] = component.width;
		}
		if (component.height) {
			layout ['height'] = component.height;
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
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/plotly/plotly.min.js', BASE_PATH + '/d3/d3.v3.min.js'], [BASE_PATH + '/plotly/plotly.css']);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ([['width', null], ['height', null]]);
	comp.options ['template'] = TEMPLATE;
	var on_plotly = function (component, data) {
		if (__in__ ('destination', data) && data ['destination'] == ('plotly/' + component.getAttribute ('plotly-name')) + '/') {
			process_response_data (component, data);
		}
	};
	comp.options ['global_state_actions'] = dict ([['plotly', on_plotly]]);
	var init = comp.fun ('init') (function (component) {
		var div = component.root.querySelector ('div');
		component.div = div;
		var plotly_name = component.getAttribute ('plotly-name');
		var url = (BASE_PLOTLY_PATH + plotly_name) + '/';
		if (component.hasAttribute ('param')) {
			url += '?param=' + component.getAttribute (param);
		}
		var data = null;
		var layout = null;
		var config = null;
		var events = null;
		var on_loaded = function () {
			if (component.hasAttribute ('width')) {
				layout ['width'] = component.getAttribute ('widht');
			}
			if (component.hasAttribute ('height')) {
				layout ['height'] = component.getAttribute ('height');
			}
			var plot = Plotly.newPlot (div, data, layout, config);
			component.plot = plot;
			if (events) {
				for (var pos of events) {
					if (__in__ ('=>', pos)) {
						var x = pos.py_split ('=>');
						var _callback = function (data1) {
							data1 ['destination'] = x [1];
							data1 ['event_name'] = x [0];
							window.GLOBAL_BUS.emit (new set (['plotly', data1]));
						};
						div.on ('plotly_' + x [0], _callback);
					}
					else {
						var make_callback = function (event_name) {
							var _callback = function (data2) {
								data2 ['event_name'] = event_name;
								var _on_server_response = function (server_data) {
									server_data ['event_name'] = event_name;
									process_response_data (component, server_data);
								};
								ajax_json (url, dict ([['name', component.getAttribute ('plotly-name')], ['action', 'on_event'], ['event_name', event_name], ['data', transform_event_data (data2)]]), _on_server_response);
							};
							return _callback;
						};
						div.on ('plotly_' + pos, make_callback (pos));
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
		ajax_json (url, dict ([['name', plotly_name], ['action', 'get_data']]), on_data_loaded);
		ajax_json (url, dict ([['name', plotly_name], ['action', 'get_layout']]), on_layout_loaded);
		ajax_json (url, dict ([['name', plotly_name], ['action', 'get_config']]), on_config_loaded);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map