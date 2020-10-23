// Transcrypt'ed from Python, 2020-10-23 23:45:15
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-svg';
export var TEMPLATE = '<div name=\"svgdiv\" data-bind=\"style-width:width;style-height:height\">\n' +
    '        <slot></slot>\n' +
    '</div>\n' +
    '\n' +
    '';
var comp = DefineWebComponent (TAG, true);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ({'width': null, 'height': null});
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var div = component.root.querySelector ('div');
		var state = dict ({});
		state ['onclick'] = window.handle_click;
		var _onmouseover = function (event) {
			print ('onmouseover');
		};
		state ['onmouseover'] = _onmouseover;
		var _onmouseout = function (event) {
			print ('onmouseout');
		};
		state ['onmouseout'] = _onmouseout;
		var _onmousedown = function (event) {
			print ('onmousedown');
		};
		state ['onmousedown'] = _onmousedown;
		var _onmouseup = function (event) {
			print ('onmouseup');
		};
		state ['onmouseup'] = _onmouseup;
		var _onfocusin = function (event) {
			print ('onfocusin');
		};
		state ['onfocusin'] = _onfocusin;
		var _onfocusout = function (event) {
			print ('onfocusout');
		};
		state ['onfocusout'] = _onfocusout;
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