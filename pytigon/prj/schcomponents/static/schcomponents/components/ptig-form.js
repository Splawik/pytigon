// Transcrypt'ed from Python, 2020-11-11 11:06:21
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-form';
var comp = DefineWebComponent (TAG, false);
try {
	comp.__enter__ ();
	var init = comp.fun ('init') (function (component) {
		var _onchange = function (new_value) {
			var on_complete = function (data) {
				var on_data = function (key) {
					if (__in__ ('__', key)) {
						var x = key.py_split ('__');
						var obj = component.root.querySelector (x [0]);
						obj [x [1]] (data [key]);
					}
					else {
						var obj = component.root.querySelector (key);
						obj.innerHTML = data [key];
					}
				};
				Object.keys (data).forEach (on_data);
			};
			var data = dict ([['name', this.getAttribute ('name')], ['new_value', this.value]]);
			var on_field = function (key) {
				data [key] = component.fields [key].value;
			};
			Object.keys (component.fields).forEach (on_field);
			ajax_json (component.getAttribute ('src'), data, on_complete);
		};
		component.fields = dict ({});
		component.figures = dict ({});
		for (var py_selector of tuple (['input', 'select', 'textarea'])) {
			var tab_inp = component.root.querySelectorAll (py_selector);
			for (var inp of tab_inp) {
				inp.addEventListener ('change', _onchange);
				var py_name = inp.getAttribute ('name');
				component.fields [py_name] = inp;
			}
		}
		var tab_inp = component.root.querySelectorAll ('.plotly');
		for (var inp of tab_inp) {
			for (var event of tuple (['click', 'hover', 'unhover', 'relayout', 'selected', 'legendclick'])) {
				inp.on ('plotly_' + event_name, _onchange);
				var py_name = inp.getAttribute ('name');
				component.figures [py_name] = inp;
			}
		}
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map