// Transcrypt'ed from Python, 2020-04-05 15:24:00
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var BASE_PATH = window.BASE_PATH + 'static/bootstrap_plugins/summernote';
export var ptig_wysiwygedit = function () {
	var template = '        <div class=\"summertextareabase border rounded\" v-bind:height=\"height\">\n' +
    '                <textarea class=\"summernotearea\" v-bind:name=\"name\" v-bind:id=\"id\">\n' +
    '                        <p style=\"text-align:left;color:black; background:white;\"></p>\n' +
    '                </textarea>\n' +
    '        </div>\n' +
    '\n' +
    '';
	var props = ['width', 'height', 'value', 'name', 'id'];
	var data = function () {
		return dict ({});
	};
	var mounted = function () {
		var self = this;
		var _next = function () {
			var ed = jQuery (self.$el).find ('textarea.summernotearea');
			if (self.height) {
				var h = self.height;
			}
			else {
				var h = 150;
			}
			var options = dict ({'height': 150, 'toolbar': [['undo', ['undo']], ['redo', ['redo']], ['style', ['bold', 'italic', 'underline', 'clear']], ['color', ['color']], ['picture', ['picture']]], 'codemirror': dict ({'theme': 'readable'}), 'icons': dict ({'align': 'fa fa-align-left', 'alignCenter': 'note-icon-align-center', 'alignJustify': 'note-icon-align-justify', 'alignLeft': 'note-icon-align-left', 'alignRight': 'note-icon-align-right', 'rowBelow': 'note-icon-row-below', 'colBefore': 'note-icon-col-before', 'colAfter': 'note-icon-col-after', 'rowAbove': 'note-icon-row-above', 'rowRemove': 'note-icon-row-remove', 'colRemove': 'note-icon-col-remove', 'indent': 'note-icon-align-indent', 'outdent': 'note-icon-align-outdent', 'arrowsAlt': 'note-icon-arrows-alt', 'bold': 'fa fa-bold', 'caret': 'note-icon-caret', 'circle': 'note-icon-circle', 'close': 'note-icon-close', 'code': 'note-icon-code', 'eraser': 'fa fa-eraser', 'font': 'fa fa-font', 'frame': 'note-icon-frame', 'italic': 'fa fa-italic', 'link': 'note-icon-link', 'unlink': 'note-icon-chain-broken', 'magic': 'note-icon-magic', 'menuCheck': 'note-icon-menu-check', 'minus': 'note-icon-minus', 'orderedlist': 'note-icon-orderedlist', 'pencil': 'note-icon-pencil', 'picture': 'fa fa-file-image-o', 'question': 'note-icon-question', 'redo': 'fa fa-repeat', 'square': 'note-icon-square', 'strikethrough': 'note-icon-strikethrough', 'subscript': 'note-icon-subscript', 'superscript': 'note-icon-superscript', 'table': 'note-icon-table', 'textHeight': 'note-icon-text-height', 'trash': 'note-icon-trash', 'underline': 'fa fa-underline', 'undo': 'fa fa-undo', 'unorderedlist': 'note-icon-unorderedlist', 'video': 'note-icon-video'})});
			ed.summernote (options);
			var value = decodeURIComponent (escape (atob (self.value)));
			ed.summernote ('code', value);
		};
		Vue.nextTick (_next);
	};
	var methods = dict ({});
	return dict ({'props': props, 'template': template, 'mounted': mounted, 'data': data, 'methods': methods});
};
register_vue_component ('ptig-wysiwygedit', ptig_wysiwygedit, [BASE_PATH + '/summernote-bs4.min.js'], [BASE_PATH + '/summernote-bs4.css', window.BASE_PATH + 'static/schcomponents/summernote_add.css']);

//# sourceMappingURL=input.map