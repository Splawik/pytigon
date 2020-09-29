// Transcrypt'ed from Python, 2020-09-29 22:47:40
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var TAG = 'ptig-wysiwygedit';
export var TEMPLATE = '        <div class=\"editorframe\">\n' +
    '                <div class=\"editor-container\">\n' +
    '                        <slot></slot>\n' +
    '                </div>\n' +
    '        </div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/quill';
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/shadowquill.js'], [BASE_PATH + '/quill.snow.css']);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ({'width': null, 'height': null});
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var toolbar_div = component.root.querySelector ('div.toolabar-container');
		var editor_div = component.root.querySelector ('div.editor-container');
		var editor_options = dict ({'modules': dict ({'syntax': false, 'toolbar': [[dict ({'font': []}), dict ({'size': []})], ['bold', 'italic', 'underline', 'strike'], [dict ({'color': []}), dict ({'background': []})], [dict ({'script': 'super'}), dict ({'script': 'sub'})], [dict ({'header': '1'}), dict ({'header': '2'}), 'blockquote', 'code-block'], [dict ({'list': 'ordered'}), dict ({'list': 'bullet'}), dict ({'indent': '-1'}), dict ({'indent': '+1'})], ['direction', dict ({'align': []})], ['link', 'image', 'video', 'formula'], ['clean']]}), 'theme': 'snow'});
		var editor = new Quill (editor_div, editor_options);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map