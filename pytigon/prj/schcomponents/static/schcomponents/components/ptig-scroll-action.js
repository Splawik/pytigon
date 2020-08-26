// Transcrypt'ed from Python, 2020-08-26 20:00:50
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var get_screen_cordinates = function (obj) {
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
export var ptig_scroll_action = function () {
	var template = '<div><slot v-bind=\"{ offset_top, offset_bottom, top_is_visible, bottom_is_visible, v }\"></slot></div>\n' +
    '\n' +
    '';
	var data = function () {
		return dict ({'offset_top': 0, 'offset_bottom': 0, 'top_is_visible': false, 'bottom_is_visible': false, 'v': 0});
	};
	var created = function () {
		window.addEventListener ('scroll', this.handle_scroll);
	};
	var destroyed = function () {
		window.removeEventListener ('scroll', this.handle_scroll);
	};
	var handle_scroll = function (event) {
		var rect = this.$el.getBoundingClientRect ();
		var y1 = rect.top;
		var y2 = rect.bottom;
		var dy = screen.height;
		if (y1 > dy) {
			this.offset_top = 0;
		}
		else if (y1 < 0) {
			this.offset_top = 1;
		}
		else {
			this.offset_top = 1 - y1 / dy;
		}
		if (y2 > dy) {
			this.offset_bottom = 0;
		}
		else if (y2 < 0) {
			this.offset_bottom = 1;
		}
		else {
			this.offset_bottom = 1 - y2 / dy;
		}
		if (this.offset_top > 0 && this.offset_top < 1) {
			this.top_is_visible = true;
		}
		else {
			this.top_is_visible = false;
		}
		if (this.offset_bottom > 0 && this.offset_bottom < 1) {
			this.bottom_is_visible = true;
		}
		else {
			this.bottom_is_visible = false;
		}
		this.v = (this.offset_top + this.offset_bottom) / 2;
	};
	var methods = dict ({'handle_scroll': handle_scroll});
	return dict ({'data': data, 'created': created, 'template': template, 'methods': methods, 'destroyed': destroyed});
};
Vue.component ('ptig-scroll-action', ptig_scroll_action ());

//# sourceMappingURL=input.map