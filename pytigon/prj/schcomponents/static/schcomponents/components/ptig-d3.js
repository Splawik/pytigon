// Transcrypt'ed from Python, 2020-07-06 18:13:45
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins';
export var ptig_d3 = function () {
	var props = ['width', 'height'];
	var template = "<div name='d3div' v-bind:style='{ width: width, height: height}' ></div>";
	var mounted = function () {
		var sampleSVG = d3.select (this.$el).append ('svg').attr ('width', 100).attr ('height', 100);
		var _on_mouseover = function () {
			d3.select (this).style ('fill', 'aliceblue');
		};
		var _on_mouseout = function () {
			d3.select (this).style ('fill', 'white');
		};
		sampleSVG.append ('circle').style ('stroke', 'gray').style ('fill', 'white').attr ('r', 40).attr ('cx', 50).attr ('cy', 50).on ('mouseover', _on_mouseover).on ('mouseout', _on_mouseout);
	};
	return dict ({'props': props, 'template': template, 'mounted': mounted});
};
register_vue_component ('ptig-d3', ptig_d3, [BASE_PATH + '/d3/d3.v3.min.js']);

//# sourceMappingURL=input.map