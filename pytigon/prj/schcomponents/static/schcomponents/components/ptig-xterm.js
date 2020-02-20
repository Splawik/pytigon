// Transcrypt'ed from Python, 2020-02-20 20:45:11
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/xterm';
export var ptig_xterm = function () {
	var props = ['width', 'height', 'x', 'y', 'href'];
	var template = "<div class = 'call_on_remove' name='xterm' v-bind:style='{ width: width, height: height}' ></div>";
	Terminal.applyAddon (fit);
	var mounted = function () {
		var self = this;
		var _next = function () {
			var address = location.hostname;
			if (location.port) {
				address += ':' + location.port;
			}
			address += self.href;
			if (location.protocol != 'https:') {
				var address = 'ws://' + address;
			}
			else {
				var address = 'wss://' + address;
			}
			var websocket = new WebSocket (address);
			var term = new Terminal ();
			term.open (self.$el);
			term.setOption ('fontFamily', 'monospace');
			term.setOption ('fontSize', 14);
			term.setOption ('lineHeight', 1.1);
			self.term = term;
			var on_remove = function () {
				var _on_close = function () {
					websocket = null;
					term.dispose ();
					term = null;
				};
				websocket.onclose = _on_close;
				if (websocket) {
					websocket.close ();
					websocket = null;
				}
			};
			self.$el.on_remove = on_remove;
			var _on_websocket_open = function () {
				var _fit_to_screen = function () {
					term.fit ();
					var s = JSON.stringify (dict ({'resize': dict ({'cols': term.cols, 'rows': term.rows})}));
					websocket.send (s);
				};
				var _on_key = function (key, ev) {
					var txt = JSON.stringify (dict ({'input': key}));
					websocket.send (txt);
				};
				var _on_message = function (evt) {
					term.write (evt.data);
				};
				term.on ('key', _on_key);
				websocket.onmessage = _on_message;
				jQuery (window).resize (_fit_to_screen);
				_fit_to_screen ();
			};
			websocket.onopen = _on_websocket_open;
		};
		Vue.nextTick (_next);
	};
	return dict ({'props': props, 'template': template, 'mounted': mounted});
};
register_vue_component ('ptig-xterm', ptig_xterm, [BASE_PATH + '/xterm.js', BASE_PATH + '/fit.js'], [BASE_PATH + '/xterm.css']);

//# sourceMappingURL=input.map