// Transcrypt'ed from Python, 2020-12-16 10:22:55
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
import {JSONPath} from '../../vanillajs_plugins/jsonpath_plus/index-es.min.js';
export var TAG = 'ptig-select2';
export var TEMPLATE = '        <div class=\"ajax-region\" style=\"position:relative;\" data-bind=\"style-padding-right:padding;style-width:width\" data-region=\"get_row\">\n' +
    '                <select style=\"width:100%;\" data-bind=\":multiple\"></select>\n' +
    '                <a type=\"button\" target=\"popup_info\" name=\"get_tbl_value\" class=\"btn btn-secondary btn-flat foreignkey_button get_tbl_value\" data-inline-position=\"^div.ajax-region:append\" style=\"position:absolute;right:2px\" data-bind=\"style-visibility:visibility;:href\">\n' +
    '                        <span class=\"fa-table fa\"></span>\n' +
    '                </a>\n' +
    '        </div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/jquery_plugins/select2';
var comp = DefineWebComponent (TAG, false);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ([['width', null], ['multiple', null], ['href', null], ['target', null]]);
	var constructor = comp.fun ('constructor') (function (component) {
		component.style.display = 'none';
	});
	var init = comp.fun ('init') (function (component) {
		var elem = document.createElement ('div');
		elem.innerHTML = TEMPLATE;
		var select = elem.querySelector ('select');
		var options = dict ({});
		var graphql = component.querySelector ('graphql');
		if (graphql) {
			var query = graphql.innerHTML;
			var data = function (params) {
				if (params.term) {
					return dict ([['query', query.py_replace ('$$$', params.term)]]);
				}
				else {
					return dict ([['query', query.py_replace ('$$$', '')]]);
				}
			};
			var process_results = function (data) {
				var tmp = JSONPath (dict ([['path', '$..node'], ['json', data]]));
				for (var pos of tmp) {
					pos ['id'] = atob (pos ['id']).py_split (':') [1];
				}
				return dict ([['results', tmp]]);
			};
			var ajax_options = dict ({});
			ajax_options ['processResults'] = process_results;
			ajax_options ['data'] = data;
			ajax_options ['type'] = 'post';
			ajax_options ['dataType'] = 'json';
			ajax_options ['delay'] = 250;
			ajax_options ['cache'] = true;
			ajax_options ['url'] = window.BASE_PATH + 'graphql/';
			options ['ajax'] = ajax_options;
		}
		else {
			var data = [];
			var append_to = function (parent, children) {
				var append = function (item, index) {
					if (item.tagName.lower () == 'optgroup') {
						var tmp = [];
						append_to (tmp, item.children);
						parent.append (dict ([['text', item.innerHTML], ['children', tmp]]));
					}
					else if (item.tagName.lower () == 'option') {
						if (item.hasAttribute ('value')) {
							parent.append (dict ([['id', item.getAttribute ('value')], ['text', item.innerHTML]]));
						}
					}
				};
				children.forEach (append);
			};
			append_to (data, component.children);
			options ['data'] = data;
		}
		component.innerHTML = '';
		component.appendChild (elem);
		jQuery (select).select2 (options);
		var _set_select2_value = function (sel2, id, text) {
			sel2.append (jQuery ('<option>', dict ([['value', id], ['text', text]])));
			sel2.val (id.toString ());
			sel2.trigger ('change');
		};
		var _onloadeddata = function (event) {
			if (hasattr (event, 'data_source')) {
				var src_elem = event.data_source;
				if (src_elem) {
					var id = src_elem.getAttribute ('data-id');
					var text = src_elem.getAttribute ('data-text');
					_set_select2_value (jQuery (select), id, text);
				}
			}
		};
		select.onloadeddata = _onloadeddata;
		select.classList.add ('ajax-frame');
		select.setAttribute ('data-region', 'get_row');
		component.style.display = 'block';
		if (component.hasAttribute ('href')) {
			var state = dict ([['padding', '52px'], ['visibility', 'visible']]);
		}
		else {
			var state = dict ([['padding', '2px'], ['visibility', 'hidden']]);
		}
		state ['onclick'] = window.handle_click;
		component.set_state (state);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map