// Transcrypt'ed from Python, 2020-11-28 12:14:30
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-scroll-action';
export var TEMPLATE = '        <div>\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
var comp = DefineWebComponent (TAG, true);
try {
	comp.__enter__ ();
	comp.options ['template'] = TEMPLATE;
	var get_screen_cordinates = function (obj) {
		var x = obj.offsetLeft;
		var y = obj.offsetTop;
		while (obj.offsetParent) {
			var x = x + obj.offsetParent.offsetLeft;
			var y = y + obj.offsetParent.offsetTop;
			if (obj == document.getElementsByTagName ('body') [0]) {
				break;
			}
			else {
				var obj = obj.offsetParent;
			}
		}
		return tuple ([x, y]);
	};
	var init = comp.fun ('init') (function (component) {
		var div = component.root.querySelector ('div');
		var offset_to_parent = jQuery (div).offset ().top - jQuery (component.parentNode).offset ().top;
		var handle_scroll = function (event) {
			var window_dy = component.parentNode.offsetHeight;
			var div_y1 = offset_to_parent - component.parentNode.scrollTop;
			var div_y2 = div_y1 + div.offsetHeight;
			if (component.hasAttribute ('y')) {
				var window_y = window_dy - int ((int (component.getAttribute ('y').py_replace ('%', '')) * window_dy) / 100);
			}
			else {
				var window_y = int (window_dy / 2);
			}
			if (component.hasAttribute ('dy')) {
				var active_zone_dy = int ((int (component.getAttribute ('dy').py_replace ('%', '')) * (div_y2 - div_y1)) / 100);
			}
			else {
				var active_zone_dy = int ((div_y2 - div_y1) / 2);
			}
			if (div_y1 > window_dy) {
				var offset_top = 0;
			}
			else if (div_y1 < 0) {
				var offset_top = 1;
			}
			else {
				var offset_top = 1 - div_y1 / window_dy;
			}
			if (div_y2 > window_dy) {
				var offset_bottom = 0;
			}
			else if (div_y2 < 0) {
				var offset_bottom = 1;
			}
			else {
				var offset_bottom = 1 - div_y2 / window_dy;
			}
			if (offset_top > 0 && offset_top < 1) {
				var top_is_visible = true;
			}
			else {
				var top_is_visible = false;
			}
			if (offset_bottom > 0 && offset_bottom < 1) {
				var bottom_is_visible = true;
			}
			else {
				var bottom_is_visible = false;
			}
			var v = (2 * (window_y - (div_y1 + div_y2) / 2)) / active_zone_dy;
			component.set_state (dict ([['offset_top', offset_top], ['offset_bottom', offset_bottom], ['top_is_visible', top_is_visible], ['bottom_is_visible', bottom_is_visible], ['v', v]]));
		};
		if (component.parentNode) {
			component.parentNode.addEventListener ('scroll', handle_scroll);
		}
	});
	var disconnectedCallback = comp.fun ('disconnectedCallback') (function (component) {
		window.removeEventListener ('scroll', component.handle_scroll);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map