// Transcrypt'ed from Python, 2020-09-20 21:40:06
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var _vseditor = function (resolve, reject) {
	var del_TEMPLATE = '        <div class=\"vseditorbase\">\n' +
    '                <button v-bind:disabled=\"!changed\" v-on:click=\"save\" class=\"btn btn-sm btn-primary\" style=\"position: absolute; z-index: 999;\">\n' +
    '                        <span class=\"fa fa-floppy-o\"></span>\n' +
    '                </button>\n' +
    '                <div style=\"width:100%; position:absolute; top:10px; text-align:center\">\n' +
    '                        <h5>{{ title }}</h5>\n' +
    '                </div>\n' +
    '                <div class=\"vseditor\" name=\"vseditor\" style=\"position: absolute; top:50px; left:5px; right:5px; bottom:1px; overflow: hidden;\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
	var TEMPLATE = '        <div class=\"vseditorbase\" v-bind:style=\"{ width: width, height: height }\">\n' +
    '                <nav class=\"navbar navbar-light bg-light\">\n' +
    '                        <span class=\"navbar-text mr-auto\">\n' +
    '                                {{ title }}\n' +
    '                        </span>\n' +
    '                        <form class=\"form-inline row col-sm-6 col-md-6 col-lg-6\">\n' +
    '                                <div class=\"row col-sm-10 col-md-10 col-lg-10\">\n' +
    '                                        <slot></slot>\n' +
    '                                </div>\n' +
    '                                <button v-bind:disabled=\"!changed\" v-on:click=\"save\" class=\"btn btn-primary col-sm-2 col-md-2 col-lg-2\" type=\"button\">\n' +
    '                                        <span class=\"fa fa-floppy-o\"></span>\n' +
    '                                        Save\n' +
    '                                </button>\n' +
    '                        </form>\n' +
    '                </nav>\n' +
    '                <div class=\"vseditor\" name=\"vseditor\" style=\"width:100%;height:100%;\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/vs';
	var _on_loadjs = function () {
		var props = ['width', 'height', 'value', 'title', 'href'];
		var data = function () {
			return dict ({'changed': false, 'calc_height': 100});
		};
		var mounted = function () {
			var self = this;
			var _next = function () {
				var ed = jQuery (self.$el).find ('div.vseditor');
				var value = decodeURIComponent (escape (atob (self.value)));
				self.editor = monaco.editor.create (ed [0], dict ({'value': value, 'language': 'python', 'theme': 'vs-dark'}));
				ed.data ('editor', self.editor);
				ed.data ('vue-editor', self);
				var _changed = function (event) {
					self.changed = true;
				};
				self.editor.onDidChangeModelContent (_changed);
				var _on_resize = function (event) {
					var parent_dy = ed [0].parentElement.offsetHeight;
					var y = ed [0].offsetTop;
					if (parent_dy - y > 0) {
						ed.height (parent_dy - y);
					}
					if (ed.width () > 10 && ed.height () > 10) {
						self.editor.layout ();
					}
				};
				window.register_resize_fun (_on_resize, 1);
				window.process_resize ();
			};
			if (window.hasOwnProperty ('MOUNTED_COMPONENTS')) {
				window.MOUNTED_COMPONENTS++;
			}
			Vue.nextTick (_next);
		};
		var save = function (event) {
			var self = this;
			if (this.href) {
				var ajax_options = dict ({'method': 'POST', 'url': this.href, 'dataType': 'html', 'data': dict ({'data': this.editor.getValue ()})});
				var _on_ajax = function () {
					self.changed = false;
				};
				jQuery.ajax (ajax_options).done (_on_ajax);
			}
		};
		var methods = dict ({'save': save});
		resolve (dict ({'props': props, 'template': TEMPLATE, 'mounted': mounted, 'data': data, 'methods': methods}));
	};
	require.config (dict ({'paths': dict ({'vs': base_path})}));
	require (['vs/editor/editor.main'], _on_loadjs);
};
Vue.component ('ptig-codeeditor', _vseditor);

//# sourceMappingURL=input.map