// Transcrypt'ed from Python, 2020-02-20 20:45:11
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins';
export var ptig_spreadsheet = function () {
	var props = ['width', 'height'];
	var template = "<div name='spreadsheetdiv' v-bind:style='{ width: width, height: height }' ></div>";
	var mounted = function () {
		var self = this;
		var columns = [dict ({'type': 'text', 'title': 'Column A', 'width': 120}), dict ({'type': 'text', 'title': 'Column B', 'width': 120}), dict ({'type': 'text', 'title': 'Column C', 'width': 120})];
		var data = [['1', '2', '3']];
		self.jtable = jexcel (this.$el, dict ({'data': data, 'columns': columns, 'minDimensions': [10, 10]}));
	};
	return dict ({'props': props, 'template': template, 'mounted': mounted});
};
register_vue_component ('ptig-spreadsheet', ptig_spreadsheet, [BASE_PATH + '/jexcel/jexcel.js', BASE_PATH + '/jsuites/jsuites.js'], [BASE_PATH + '/jsuites/jsuites.css', BASE_PATH + '/jexcel/jexcel.css']);

//# sourceMappingURL=input.map