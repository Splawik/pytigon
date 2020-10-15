// Transcrypt'ed from Python, 2020-10-15 19:12:26
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-imask';
export var TEMPLATE = '        <slot></slot>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins';
export var decimal_separator = function () {
	return 1.1.toLocaleString () [1];
};
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/imask/imask.js']);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ({});
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var input = component.querySelector ('input');
		var options = dict ({});
		var mask = component.getAttribute ('mask');
		var _mask = mask.lower ();
		if (_mask == 'number' || _mask == 'monay') {
			options ['mask'] = window.Number;
			if (_mask == 'monay') {
				options ['scale'] = 2;
				options ['radix'] = decimal_separator ();
			}
			if (component.hasAttribute ('scale')) {
				options ['scale'] = int (component.getAttribute ('scale'));
			}
			if (component.hasAttribute ('signed')) {
				options ['signed'] = true;
			}
			if (component.hasAttribute ('thousands-separator')) {
				if (component.getAttribute ('thousands-separator')) {
					options ['thousandsSeparator'] = component.getAttribute ('thousands-separator');
				}
				else {
					options ['thousandsSeparator'] = ' ';
				}
			}
			if (component.hasAttribute ('pad-fractional-zeros')) {
				options ['padFractionalZeros'] = true;
			}
			if (component.hasAttribute ('normalize-zeros')) {
				options ['normalizeZeros'] = true;
			}
			if (component.hasAttribute ('radix')) {
				if (component.getAttribute ('radix')) {
					options ['radix'] = component.getAttribute ('radix');
				}
				else {
					options ['radix'] = decimal_separator ();
				}
			}
			if (component.hasAttribute ('map-to-radix')) {
				options ['mapToRadix'] = component.getAttribute ('map-to-radix');
			}
		}
		else if (_mask == 'range') {
			options ['mask'] = IMask.MaskedRange;
			if (component.hasAttribute ('from')) {
				options ['from'] = int (component.getAttribute ('from'));
			}
			if (component.hasAttribute ('to')) {
				options ['to'] = int (component.getAttribute ('to'));
			}
			if (component.hasAttribute ('max-length')) {
				options ['maxLength'] = int (component.getAttribute ('max-length'));
			}
		}
		else if (_mask == 'enum') {
			options ['mask'] = IMask.MaskedEnum;
			options ['enum'] = component.getAttribute ('enum').py_split (';');
		}
		else if (_mask == 'date') {
			options ['mask'] = window.Date;
			if (component.hasAttribute ('pattern')) {
				options ['pattern'] = component.getAttribute ('pattern');
			}
			else {
				options ['pattern'] = 'Y-m-000';
				options ['blocks'] = dict ({'d': dict ({'mask': window.IMask.MaskedRange, 'from': 1, 'to': 12, 'maxLength': 2}), 'm': dict ({'mask': window.IMask.MaskedRange, 'from': 1, 'to': 12, 'maxLength': 2}), 'Y': dict ({'mask': window.IMask.MaskedRange, 'from': 1900, 'to': 9999})});
			}
		}
		else {
			options ['mask'] = mask;
		}
		var imask = IMask (input, options);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map