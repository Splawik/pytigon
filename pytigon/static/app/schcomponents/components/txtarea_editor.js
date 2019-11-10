// Transcrypt'ed from Python, 2019-11-10 13:56:04
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '.././../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var mounted = function () {
	var txtarea = jQuery (this.$el);
	txtarea.addClass ('vue');
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/ace/src-min';
	var _on_loadjs = function () {
		ace.config.set ('basePath', base_path);
		var a = jQuery ('<div></div>');
		txtarea.after (a);
		var editor = ace.edit (a [0]);
		editor.setOptions (dict ({'maxLines': 32}));
		editor.setTheme ('ace/theme/textmate');
		editor.getSession ().setMode ('ace/mode/markdown');
		editor.getSession ().setValue (txtarea.val ());
		txtarea.hide ();
		var _on_change = function () {
			txtarea.val (editor.getSession ().getValue ());
		};
		editor.getSession ().on ('change', _on_change);
		if (window.hasOwnProperty ('MOUNTED_COMPONENTS')) {
			window.MOUNTED_COMPONENTS++;
		}
	};
	load_js (base_path + '/ace.js', _on_loadjs);
};
export var target = jQuery ('body') [0];
export var process_mutations = function (mutations) {
	var _process_mutation = function (mutation) {
		var newNodes = mutation.addedNodes;
		if (newNodes != null) {
			var nodes = jQuery (newNodes);
			var _process_node = function () {
				var node = jQuery (this);
				var txtarray = node.find ('textarea.ceditor');
				if (txtarray.length > 0 && !(txtarray.hasClass ('vue'))) {
					var _process_txt = function () {
						var vm = new Vue (dict ({'el': this, 'mounted': mounted}));
					};
					txtarray.each (_process_txt);
				}
			};
			nodes.each (_process_node);
		}
	};
	mutations.forEach (_process_mutation);
};
export var observer = new MutationObserver (process_mutations);
export var config = dict ({'attributes': false, 'childList': true, 'characterData': true, 'subtree': true});
observer.observe (target, config);

//# sourceMappingURL=input.map