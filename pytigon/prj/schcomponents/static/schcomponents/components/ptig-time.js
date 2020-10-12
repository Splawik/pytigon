// Transcrypt'ed from Python, 2020-10-12 20:48:51
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-time';
export var TEMPLATE = '        <p data-bind=\"time\"></p>\n' +
    '\n' +
    '';
var comp = DefineWebComponent (TAG, true);
try {
	comp.__enter__ ();
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var _on_time = function () {
			var d = new Date ();
			component.set_state (dict ({'time': d.toISOString ().py_replace ('T', ' ').__getslice__ (0, 19, 1)}));
		};
		component.timer = setInterval (_on_time, 1000);
	});
	var disconnectedCallback = comp.fun ('disconnectedCallback') (function (component) {
		if (component.timer) {
			clearTimeout (component.timer);
			component.timer = null;
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