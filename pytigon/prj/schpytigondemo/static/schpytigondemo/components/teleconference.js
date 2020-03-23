// Transcrypt'ed from Python, 2020-03-23 19:23:11
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var TEMPLATE = '  <div class=\"container\">\n' +
    '        <div class=\"row\">\n' +
    '            <div class=\"col-md-12 my-3\">\n' +
    '                <h2>Room</h2>\n' +
    '                <input v-model=\"roomId\">\n' +
    '            </div>\n' +
    '        </div>\n' +
    '        <div class=\"row\">\n' +
    '            <div class=\"col-md-12\">\n' +
    '                <div class=\"f\">\n' +
    '                    <ptig-webrtc ref=\"webrtc\" width=\"100%\" :roomId=\"roomId\" :src=\"src\" v-on:joined-room=\"logEvent\" v-on:left-room=\"logEvent\" v-on:open-room=\"logEvent\" v-on:share-started=\"logEvent\" v-on:share-stopped=\"logEvent\" @error=\"onError\" />\n' +
    '                </div>\n' +
    '                <div class=\"row\">\n' +
    '                    <div class=\"col-md-12 my-3\">\n' +
    '                        <button type=\"button\" class=\"btn btn-primary\" @click=\"onJoin\">Join</button>\n' +
    '                        <button type=\"button\" class=\"btn btn-primary\" @click=\"onLeave\">Leave</button>\n' +
    '                        <button type=\"button\" class=\"btn btn-primary\" @click=\"onCapture\">Capture Photo</button>\n' +
    '                        <button type=\"button\" class=\"btn btn-primary\" @click=\"onShareScreen\">Share Screen</button>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '            </div>\n' +
    '        </div>\n' +
    '        <div class=\"row\">\n' +
    '            <div class=\"col-md-12\">\n' +
    '                <h2>Captured Image</h2>\n' +
    '                <figure class=\"figure\">\n' +
    '                    <img :src=\"img\" class=\"img-responsive\" />\n' +
    '                </figure>\n' +
    '            </div>\n' +
    '        </div>\n' +
    '    </div>\n' +
    '\n' +
    '';
export var _room = function (resolve, reject) {
	var data = function () {
		var d = dict ({'img': null, 'roomId': 'public-room', 'src': window.BASE_PATH + 'schsimplecontrolsdemo/teleconference/socket.io/'});
		return d;
	};
	var onCapture = function () {
		this.img = this.$refs.webrtc.capture ();
	};
	var onJoin = function () {
		this.$refs.webrtc.join ();
	};
	var onLeave = function () {
		this.$refs.webrtc.leave ();
	};
	var onShareScreen = function () {
		this.img = this.$refs.webrtc.shareScreen ();
	};
	var onError = function (error, stream) {
		console.log ('On Error Event', error, stream);
	};
	var logEvent = function (event) {
		console.log ('Event : ', event);
	};
	var methods = dict ({'onCapture': onCapture, 'onJoin': onJoin, 'onLeave': onLeave, 'onShareScreen': onShareScreen, 'onError': onError, 'logEvent': logEvent});
	resolve (dict ({'data': data, 'template': TEMPLATE, 'methods': methods}));
};
Vue.component ('room', _room);

//# sourceMappingURL=input.map