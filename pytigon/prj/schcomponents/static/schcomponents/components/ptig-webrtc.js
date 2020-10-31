// Transcrypt'ed from Python, 2020-10-31 08:54:46
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../pytigon_js/org.transcrypt.__runtime__.js';
import {DefineWebComponent} from '../../pytigon_js/pytigon_js.component.js';
var __name__ = '__main__';
export var TAG = 'ptig-webrtc';
export var TEMPLATE = '        <div class=\"container bs-docs-container\">\n' +
    '                <div class=\"row\">\n' +
    '                        <div class=\"videos\">\n' +
    '                                <div class=\"col-md-9\">\n' +
    '                                        <h2>Remote</h2>\n' +
    '                                        <video class=\"webrtc_remote\" autoplay></video>\n' +
    '                                </div>\n' +
    '                                <div class=\"col-md-3\">\n' +
    '                                        <h2>Local</h2>\n' +
    '                                        <video class=\"webrtc_local call_on_remove\" autoplay muted></video>\n' +
    '                                </div>\n' +
    '                        </div>\n' +
    '                </div>\n' +
    '                <div class=\"well\">\n' +
    '                                <p class=\"webrtc_traceback bg-info\"></p>\n' +
    '                                <p class=\"webrtc_streaming bg-info\"></p>\n' +
    '                </div>\n' +
    '        </div>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/schcomponents/components';
export var get_configuration = function (server, username, password) {
	var ret = { iceServers: [ {"urls": "stun:" + server, "username": username, "credential": password }, {"urls":"turn:" + server, "username": username, "credential": password } ] };
	print (ret);
	return ret;
};
export var init_webrtc = function (url, host, room, local, remote, traceback, streaming) {
	if (host) {
		var initiator = false;
	}
	else {
		var initiator = true;
	}
	var pc = null;
	var ws = new WebSocket (url.py_replace ('http', 'ws').py_replace ('https', 'wss'));
	var PeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection;
	var IceCandidate = window.RTCIceCandidate || window.RTCIceCandidate;
	var SessionDescription = window.RTCSessionDescription || window.RTCSessionDescription;
	navigator.getUserMedia = navigator.getUserMedia || navigator.mediaDevices.getUserMedia || navigator.webkitGetUserMedia;
	var timer = null;
	var connected = false;
	var _on_remove = function () {
		console.log ('close on remove');
		if (pc) {
			pc.close ();
		}
		pc = null;
		ws.close ();
		ws = null;
		if (timer) {
			window.clearInterval (timer);
			timer = null;
		}
	};
	local.on_remove = _on_remove;
	var _success = function (stream) {
		var server = 'pytigon.cloud';
		var username = 'auto';
		var password = 'anawa';
		var ws_onmessage = ws.onmessage;
		var on_timer = function () {
			if (ws) {
				ws.send (JSON.stringify (dict ({'ping': 1})));
			}
			if (pc && !(host) && !(connected)) {
				createOffer ();
			}
		};
		timer = setInterval (on_timer, 10000);
		var init_pc = function () {
			pc = new PeerConnection (get_configuration (server, username, password));
			var _onaddremotestream = function (event) {
				remote.srcObject = event.stream;
				remote.play ();
				logStreaming (true);
			};
			pc.onaddstream = _onaddremotestream;
			var _onremovestream = function (event) {
				print ('onremovestream:');
				print (event);
			};
			pc.onremovestream = _onremovestream;
			var _onicecandidate = function (event) {
				if (event.candidate) {
					ws.send (JSON.stringify (event.candidate));
				}
			};
			pc.addEventListener ('icecandidate', _onicecandidate);
		};
		init_pc ();
		var log_video_loaded = function (event) {
			var video = event.target;
			print (video.id);
			print (video.videoWidth);
			print (video.videoHeight);
		};
		var log_resized_video = function (event) {
			log_video_loaded (event);
		};
		local.addEventListener ('loadedmetadata', log_video_loaded);
		remote.addEventListener ('loadedmetadata', log_video_loaded);
		remote.addEventListener ('onresize', log_resized_video);
		var _onmessage = function (event) {
			var signal = JSON.parse (event.data);
			if (signal.sdp) {
				if (initiator) {
					receiveAnswer (signal);
				}
				else {
					receiveOffer (signal);
				}
			}
			else if (signal.candidate) {
				pc.addIceCandidate (new IceCandidate (signal));
			}
			else if (signal.destroy) {
				if (pc) {
					pc.close ();
				}
				init_pc ();
				pc.addStream (stream);
				connected = false;
			}
			else {
				ws_onmessage (event);
			}
		};
		ws.onmessage = _onmessage;
		if (stream) {
			pc.addStream (stream);
			local.srcObject = stream;
			local.play ();
		}
		if (initiator) {
			createOffer ();
		}
		else {
			log ('Waiting for guest connection..');
		}
		logStreaming (false);
	};
	var _fail = function () {
		var argi = tuple ([].slice.apply (arguments).slice (0));
		traceback.innerHTML = Array.prototype.join.call (argi, ' ');
		traceback.setAttribute ('class', 'bg-danger');
	};
	var initialize = function () {
		var constraints = dict ({'audio': true, 'video': true});
		navigator.getUserMedia (constraints, _success, _fail);
	};
	var _socketCallback = function (event) {
		var signal = JSON.parse (event.data);
		if (signal.status) {
			if (signal.status == 'connected') {
				if (host) {
					ws.send (JSON.stringify (dict ({'init_consumer': 1, 'room': room, 'host': host})));
				}
				else {
					ws.send (JSON.stringify (dict ({'init_consumer': 1, 'room': room})));
				}
			}
			else if (signal.status == 'initiated') {
				initialize ();
			}
		}
	};
	ws.onmessage = _socketCallback;
	var createOffer = function () {
		log ('Creating offer. Please wait.');
		var _create_offer = function (offer) {
			log ('Success offer');
			var set_description = function () {
				log ('Sending to remote..');
				ws.send (JSON.stringify (offer));
			};
			pc.setLocalDescription (offer, set_description, _fail);
		};
		pc.createOffer (_create_offer, _fail);
	};
	var receiveOffer = function (offer) {
		log ('Received offer.');
		var set_remote_description = function () {
			log ('Creating response');
			var create_answer = function (answer) {
				log ('Created response');
				var set_local_description = function () {
					log ('Sent response');
					ws.send (JSON.stringify (answer));
					var connected = true;
				};
				pc.setLocalDescription (answer, set_local_description, _fail);
			};
			pc.createAnswer (create_answer, _fail);
		};
		pc.setRemoteDescription (new SessionDescription (offer), set_remote_description, _fail);
	};
	var receiveAnswer = function (answer) {
		log ('received answer');
		pc.setRemoteDescription (new SessionDescription (answer));
		connected = true;
	};
	var log = function () {
		var argi = tuple ([].slice.apply (arguments).slice (0));
		traceback.innerHTML = Array.prototype.join.call (argi, ' ');
		console.log.apply (console, argi);
	};
	var logStreaming = function (is_streaming) {
		if (is_streaming) {
			streaming.innerHTML = '[streaming]';
		}
		else {
			streaming.innerHTML = '[.]';
		}
	};
};
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/adapter-latest.js']);
try {
	comp.__enter__ ();
	comp.options ['template'] = TEMPLATE;
	var init = comp.fun ('init') (function (component) {
		var remote = component.root.querySelector ('.webrtc_remote');
		var local = component.root.querySelector ('.webrtc_local');
		var traceback = component.root.querySelector ('.webrtc_traceback');
		var streaming = component.root.querySelector ('webrtc_streaming');
		var url = window.location;
		var src = ((url.protocol + '//') + url.host) + component.getAttribute ('src');
		init_webrtc (src, component.getAttribute ('host'), component.getAttribute ('roomId'), local, remote, traceback, streaming);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map