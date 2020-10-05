// Transcrypt'ed from Python, 2020-10-05 20:44:36
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-task';
export var TEMPLATE = '<div name=\'task\'><slot></slot></div>\n' +
    '\n' +
    '';
var comp = DefineWebComponent (TAG, true);
try {
	comp.__enter__ ();
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		component.timer = null;
		component.websocket = null;
		var address = location.hostname;
		if (location.port) {
			address += ':' + location.port;
		}
		if (component.hasAttribute ('websocket_href')) {
			address += component.getAttribute ('websocket_href');
		}
		if (location.protocol != 'https:') {
			var address = 'ws://' + address;
		}
		else {
			var address = 'wss://' + address;
		}
		component.websocket = new WebSocket (address);
		var on_timer = function () {
			if (component.websocket) {
				component.websocket.send (JSON.stringify (dict ({'ping': 1})));
			}
		};
		component.timer = setInterval (on_timer, 10000);
		var _on_websocket_open = function () {
			var div = component.shadowRoot.querySelector ('div');
			var _on_message = function (evt) {
				var jdata = JSON.parse (evt.data);
				var status = jdata ['status'];
				if (status == 'pong') {
					console.log ('pong');
				}
				else if (status == 'start') {
					var task_status = jQuery (div).find ('[name="task_status"]');
					if (task_status.length > 0) {
						task_status.addClass ('task_started');
					}
				}
				else if (status == 'stop') {
					var task_status = jQuery (div).find ('[name="task_status"]');
					if (task_status.length > 0) {
						task_status.removeClass ('task_started');
						task_status.addClass ('task_finished');
					}
					var task_end_info = jQuery (div).find ('[name="task_end_info"]');
					if (task_end_info.length > 0) {
						task_end_info.show ();
					}
				}
				else if (status == 'event') {
					var html = jdata ['data'];
					window.send_to_dom (html, div);
				}
				else {
					console.log (evt.data);
				}
			};
			component.websocket.onmessage = _on_message;
			if (component.hasAttribute ('task_href')) {
				var _complete = function () {
					console.log ('task started');
				};
				ajax_get (component.getAttribute ('task_href'), _complete);
			}
			if (component.hasAttribute ('task_id')) {
				component.websocket.send (JSON.stringify (dict ({'id': component.getAttribute ('task_id')})));
			}
		};
		component.websocket.onopen = _on_websocket_open;
	});
	var disconnectedCallback = comp.fun ('disconnectedCallback') (function (component) {
		window.clearInterval (component.timer);
		component.timer = null;
		var _on_close = function () {
			component.websocket = null;
		};
		component.websocket.onclose = _on_close;
		if (component.websocket) {
			component.websocket.close ();
			component.websocket = null;
		}
		print ('disconnectedCallbaack()');
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map