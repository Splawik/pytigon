// Transcrypt'ed from Python, 2020-10-26 23:06:55
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-codeeditor';
export var TEMPLATE = '<slot>\n' +
    '        <navbar navbar-expand-lg navbar-dark bg-primary>\n' +
    '                <span class=\"navbar-text mr-auto\" data-bind=\"title\"></span>\n' +
    '                <form class=\"form-inline\">\n' +
    '                        <button data-bind=\"disabled:!changed;onclick:on_save\" class=\"btn btn-primary\" type=\"button\">\n' +
    '                                <span class=\"fa fa-floppy-o\"></span>\n' +
    '                                Save\n' +
    '                        </button>\n' +
    '                </form>\n' +
    '        </navbar>\n' +
    '</slot>\n' +
    '<div class=\"vseditor\" name=\"vseditor\" style=\"width:100%;height:calc(100% - 5rem);\"></div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/vs';
var comp = DefineWebComponent (TAG, true, [], [BASE_PATH + '/editor/editor.main.css']);
try {
	comp.__enter__ ();
	comp.options ['template'] = TEMPLATE;
	var width = function (component, old_value, new_value) {
		component.style.width = new_value;
	};
	var height = function (component, old_value, new_value) {
		component.style.height = new_value;
	};
	comp.options ['attributes'] = dict ({'width': width, 'height': height, 'title': null});
	var init = comp.fun ('init') (function (component) {
		var _on_loadjs = function () {
			var ed = component.root.querySelector ('div.vseditor');
			if (component.hasAttribute ('value')) {
				var value = decodeURIComponent (escape (atob (component.getAttribute ('value'))));
			}
			else {
				var value = '';
			}
			component.editor = monaco.editor.create (ed, dict ({'value': value, 'language': 'python', 'theme': 'vs-dark'}));
			var _changed = function (event) {
				component.set_state (dict ({'changed': true}));
			};
			component.editor.onDidChangeModelContent (_changed);
			var _on_resize = function (event) {
				var parent_dy = component.offsetHeight;
				var y = ed.offsetTop;
				if (parent_dy - y > 0) {
					ed.style.height = parent_dy - y;
				}
				if (ed.offsetHeight > 10 && ed.offsetHeight > 10) {
					component.editor.layout ();
				}
			};
			window.register_resize_fun (_on_resize, 1);
			window.process_resize ();
		};
		require.config (dict ({'paths': dict ({'vs': BASE_PATH})}));
		require (['vs/editor/editor.main'], _on_loadjs);
		var on_save = function (event) {
			if (component.hasAttribute ('href')) {
				var href = component.getAttribute ('href');
				var ajax_options = dict ({'method': 'POST', 'url': href, 'dataType': 'html', 'data': dict ({'data': component.editor.getValue ()})});
				var _on_ajax = function () {
					component.set_state (dict ({'changed': false}));
				};
				jQuery.ajax (ajax_options).done (_on_ajax);
			}
		};
		var state = dict ({'on_save': on_save, 'changed': false});
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