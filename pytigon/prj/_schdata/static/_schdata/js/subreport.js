// Transcrypt'ed from Python, 2020-06-10 23:23:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var subreport_dragstart = function (ev) {
	ev.dataTransfer.setData ('text', ev.target.getAttribute ('name'));
};
window.subreport_dragstart = subreport_dragstart;
export var subreport_drop = function (ev, base_path) {
	ev.preventDefault ();
	if (ev.target.tagName == 'LABEL') {
		var target = ev.target;
	}
	else {
		var target = ev.target.parentElement;
	}
	var data = ev.dataTransfer.getData ('text');
	var data2 = target.getAttribute ('name');
	if (data2 != data) {
		var href = ((((base_path + 'schreports/table/Report/') + data) + '/') + data2) + '/action/move_to/';
		ajax_get (href, standard_on_data (jQuery (target), href));
	}
};
window.subreport_drop = subreport_drop;
export var subreport_ondragenter = function (ev) {
	if (ev.target.tagName == 'LABEL') {
		jQuery (ev.target).addClass ('bg-success');
	}
};
window.subreport_ondragenter = subreport_ondragenter;
export var subreport_ondragleave = function (ev) {
	if (ev.target.tagName == 'LABEL') {
		jQuery (ev.target).removeClass ('bg-success');
	}
};
window.subreport_ondragleave = subreport_ondragleave;
export var subreport_ondragover = function (ev) {
	if (ev.target.tagName == 'LABEL') {
		ev.preventDefault ();
	}
};
window.subreport_ondragover = subreport_ondragover;

//# sourceMappingURL=input.map