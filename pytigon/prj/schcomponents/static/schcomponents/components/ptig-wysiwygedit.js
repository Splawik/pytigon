// Transcrypt'ed from Python, 2020-12-01 20:03:42
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-wysiwygedit';
export var TEMPLATE = '        <slot></slot>\n' +
    '        <div class=\"editorframe\">\n' +
    '                <div class=\"editor-container\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/quill';
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/shadowquill.js'], [BASE_PATH + '/quill.snow.css']);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ([['width', null], ['height', null], ['name', null]]);
	comp.options ['template'] = TEMPLATE;
	var constructor = comp.fun ('constructor') (function (component) {
		component.textarea = component.querySelector ('textarea');
		if (component.textarea) {
			component.textarea.style.display = 'none';
		}
		var toolbar_div = component.querySelector ("div[slot='toolbar']");
		if (toolbar_div) {
			component.toolbar = window.JSON.parse (toolbar_div.innerHTML);
		}
		else {
			component.toolbar = null;
		}
	});
	var init = comp.fun ('init') (function (component) {
		var editor_div = component.root.querySelector ('div.editor-container');
		var editor_options = dict ([['modules', dict ([['syntax', false]])], ['theme', 'snow']]);
		if (component.toolbar) {
			editor_options ['modules'] ['toolbar'] = component.toolbar;
		}
		var editor = new Quill (editor_div, editor_options);
		component.editor = editor;
		var sync = function () {
			if (component.textarea.childNodes.length > 0) {
				jQuery (component.textarea).text (editor_div.children [0].innerHTML);
			}
			else {
				jQuery (component.textarea).text ('');
			}
		};
		var on_change = function () {
			component.set_state (dict ([['changed', true]]));
		};
		if (component.textarea) {
			editor.setContents ([]);
			if (component.textarea.childNodes.length > 0) {
				editor.clipboard.dangerouslyPasteHTML (0, component.textarea.childNodes [0].nodeValue);
			}
			editor.on ('text-change', sync);
		}
		else {
			editor.on ('text-change', on_change);
		}
		var on_save = function (event) {
			if (event.currentTarget.hasAttribute ('href')) {
				var href = event.currentTarget.getAttribute ('href');
				var ajax_options = dict ([['method', 'POST'], ['url', href], ['dataType', 'html'], ['data', dict ([['data', editor_div.children [0].innerHTML]])]]);
				var _on_ajax = function () {
					component.set_state (dict ([['changed', false]]));
				};
				jQuery.ajax (ajax_options).done (_on_ajax);
			}
		};
		var state = dict ([['on_save', on_save], ['changed', false]]);
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