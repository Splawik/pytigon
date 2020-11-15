// Transcrypt'ed from Python, 2020-11-10 19:12:11
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var TAG = 'insert-object';
export var TEMPLATE = '        <div name=\"insert_element\" class=\"col-5\">\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
export var handle_click = function (app_path, object, context) {
	var vc_component = object.closest ('ptig-codeeditor');
	var ed = vc_component.editor;
	var repeat = 2;
	while (repeat > 0) {
		var pos = ed.getPosition ();
		var text = ed.getValue ();
		var tab = text.py_split ('\n');
		var line = tab [pos.lineNumber - 1];
		if (line.startswith ('@')) {
			if (context ['edit_form'] == 'True') {
				var x = line.py_split (':');
				var href = (((app_path + '/table/PageObjectsConf/action/edit_page_object/?name=') + x [0].__getslice__ (1, null, 1)) + '&page_id=') + str (context ['page_id']);
				window.on_popup_edit_new (href, object [0], null);
			}
			var repeat = 0;
		}
		else {
			if (!(context ['pk'])) {
				alert ('Select new wiki object type or point to existing element to edit proporties');
				break;
			}
			var max = 0;
			for (var l of tab) {
				if (l.startswith ('@' + context ['object_name'])) {
					var x = l.py_split ('_');
					if (len (x) > 1) {
						var xx = x [1].py_split (':');
						try {
							var n = int (xx [0]);
							if (n > max) {
								var max = n;
							}
						}
						catch (__except0__) {
							// pass;
						}
					}
				}
			}
			var range = new monaco.Range (pos.lineNumber, 1, pos.lineNumber, 1);
			var id = dict ([['major', 1], ['minor', 1]]);
			if (context ['edit_form'] == 'True') {
				var edit_form = '_' + str (max + 1);
			}
			else {
				var edit_form = '';
			}
			var text = ('@' + context ['object_name']) + edit_form;
			if (context ['object_inline_editing']) {
				text += ':\n';
			}
			else {
				text += '\n';
			}
			var op = dict ([['identifier', id], ['range', range], ['text', text], ['forceMoveMarkers', true]]);
			ed.executeEdits ('pytigon', [op]);
			ed.setPosition (pos);
			vc_component.state ['on_save'] (null);
			repeat -= 1;
		}
	}
};
var comp = DefineWebComponent (TAG, true);
try {
	comp.__enter__ ();
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var button = component.querySelector ('a.btn');
		button.style.height = '100%';
		var on_click = function () {
			var on_get = function (content) {
				handle_click (component.getAttribute ('app_path'), button, content);
			};
			ajax_json (window.process_href (button.href, window.jQuery (button)), dict ({}), on_get);
			return false;
		};
		button.onclick = on_click;
		var obj = jQuery (component);
		var frame = obj.closest ('.refresh_after_close');
		window.fragment_init (frame);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map