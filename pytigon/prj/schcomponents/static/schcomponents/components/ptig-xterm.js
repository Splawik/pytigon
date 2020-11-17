// Transcrypt'ed from Python, 2020-11-17 21:52:43
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-xterm';
export var TEMPLATE = '        <div name=\"xterm\" data-bind=\"style-width:width;style-height:height\"></div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/xterm';
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/xterm.js', BASE_PATH + '/fit.js'], [BASE_PATH + '/xterm.css']);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ([['width', null], ['height', null]]);
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var div = component.root.querySelector ('div');
		Terminal.applyAddon (fit);
		var address = location.hostname;
		if (location.port) {
			address += ':' + location.port;
		}
		address += component.getAttribute ('href');
		if (location.protocol != 'https:') {
			var address = 'ws://' + address;
		}
		else {
			var address = 'wss://' + address;
		}
		var websocket = new WebSocket (address);
		component.websocket = websocket;
		var term = new Terminal ();
		term.open (div);
		term.setOption ('fontFamily', 'monospace');
		term.setOption ('fontSize', 14);
		term.setOption ('lineHeight', 1.1);
		term.setOption ('theme', dict ([['background', '#222d32']]));
		component.term = term;
		var on_timer = function () {
			if (websocket) {
				websocket.send (JSON.stringify (dict ([['ping', 1]])));
			}
		};
		var timer = setInterval (on_timer, 10000);
		component.timer = timer;
		var _on_websocket_open = function () {
			var _fit_to_screen = function () {
				term.fit ();
				var s = JSON.stringify (dict ([['resize', dict ([['cols', term.cols], ['rows', term.rows]])]]));
				websocket.send (s);
			};
			var _on_key = function (key, ev) {
				var txt = JSON.stringify (dict ([['input', key]]));
				websocket.send (txt);
			};
			var _on_message = function (evt) {
				if (evt.data == 'pong') {
					// pass;
				}
				else {
					term.write (evt.data);
				}
			};
			term.on ('key', _on_key);
			websocket.onmessage = _on_message;
			jQuery (window).resize (_fit_to_screen);
			_fit_to_screen ();
		};
		websocket.onopen = _on_websocket_open;
	});
	var disconnectedCallback = comp.fun ('disconnectedCallback') (function (component) {
		window.clearInterval (component.timer);
		component.timer = null;
		var _on_close = function () {
			component.term.dispose ();
			component.term = null;
		};
		component.websocket.onclose = _on_close;
		if (component.websocket) {
			component.websocket.close ();
			component.websocket = null;
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