// Transcrypt'ed from Python, 2020-11-26 18:34:21
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {init_table} from '../../pytigon_js/pytigon_js.tbl.js';
import {animate_combo, get_table_type} from '../../pytigon_js/pytigon_js.tools.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
var comp = DefineWebComponent ('sys-sidebarmenu', false);
try {
	comp.__enter__ ();
	var init = comp.fun ('init') (function (component) {
		var _on_resize = function () {
			window.process_resize (document.body);
		};
		var client_type = component.getAttribute ('type');
		var sidebar_menu = component.querySelector ('.sidebar-menu');
		if (client_type && client_type == 'smartfon') {
			jQuery.sidebarMenu (sidebar_menu);
			var obj1_off = dict ([['width', '256px']]);
			var obj1_on = dict ([['width', '0px']]);
			var obj2_off = dict ([['margin-left', '256px'], ['margin-right', '-256px']]);
			var obj2_on = dict ([['margin-left', '0px'], ['margin-right', '0px']]);
			var obj1 = jQuery ('#menu');
			var obj2 = jQuery ('#panel');
			animate_combo (jQuery ('.sidebar-toggle'), obj1, obj2, obj1_off, obj1_on, obj2_off, obj2_on, 'fast', _on_resize);
		}
		else {
			jQuery.sidebarMenu (sidebar_menu);
			var obj1_off = dict ([['width', '256px']]);
			var obj1_on = dict ([['width', '0px']]);
			var obj2_off = dict ([['margin-left', '256px']]);
			var obj2_on = dict ([['margin-left', '0px']]);
			var obj1 = jQuery ('#menu');
			var obj2 = jQuery ('#panel');
			animate_combo (jQuery ('.sidebar-toggle'), obj1, obj2, obj1_off, obj1_on, obj2_off, obj2_on, 'fast', _on_resize);
		}
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}
var comp = DefineWebComponent ('sys-perfectscrollbar', false);
try {
	comp.__enter__ ();
	var init = comp.fun ('init') (function (component) {
		window.PS = new PerfectScrollbar ('#menu');
		var _on_resize = function () {
			window.PS.update ();
		};
		jQuery (window).resize (_on_resize);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}
var comp = DefineWebComponent ('sys-datatable', false);
try {
	comp.__enter__ ();
	var init = comp.fun ('init') (function (component) {
		var table_type = get_table_type (jQuery (component));
		var tbl = component.querySelector ('.tabsort');
		if (tbl) {
			init_table (jQuery (tbl), table_type);
			var onchange = function () {
				jQuery (tbl).bootstrapTable ('refresh');
			};
			component.onchange = onchange;
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