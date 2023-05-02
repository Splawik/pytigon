var BASE_PATH, TAG, TEMPLATE, comp, get_configuration, init, init_webrtc, stub1_context, stub2_err;
TAG = "ptig-webrtc";
TEMPLATE = '        <div class=\"container bs-docs-container\">\n' +
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
BASE_PATH = window.BASE_PATH + "static/schcomponents/components";
get_configuration = function flx_get_configuration (server, username, password) {
    var ret;
    ret = __pragma__("js", "{}", "{ iceServers: [ {\"urls\": \"stun:\" + server, \"username\": username, \"credential\": password }, {\"urls\":\"turn:\" + server, \"username\": username, \"credential\": password } ] };");
    console.log(ret);
    return ret;
};

init_webrtc = function flx_init_webrtc (url, host, room, local, remote, traceback, streaming) {
    var IceCandidate, PeerConnection, SessionDescription, _fail, _on_remove, _socketCallback, _success, connected, createOffer, initialize, initiator, log, logStreaming, pc, receiveAnswer, receiveOffer, timer, ws;
    if (_pyfunc_truthy(host)) {
        initiator = false;
    } else {
        initiator = true;
    }
    pc = null;
    ws = new WebSocket(_pymeth_replace.call(_pymeth_replace.call(url, "http", "ws"), "https", "wss"));
    PeerConnection = _pyfunc_truthy(window.RTCPeerConnection) || window.webkitRTCPeerConnection;
    IceCandidate = _pyfunc_truthy(window.RTCIceCandidate) || window.RTCIceCandidate;
    SessionDescription = _pyfunc_truthy(window.RTCSessionDescription) || window.RTCSessionDescription;
    navigator.getUserMedia = _pyfunc_truthy(navigator.getUserMedia) || _pyfunc_truthy(navigator.mediaDevices.getUserMedia) || navigator.webkitGetUserMedia;
    timer = null;
    connected = false;
    _on_remove = (function flx__on_remove () {
        console.log("close on remove");
        if (_pyfunc_truthy(pc)) {
            pc.close();
        }
        pc = null;
        ws.close();
        ws = null;
        if (_pyfunc_truthy(timer)) {
            window.clearInterval(timer);
            timer = null;
        }
        return null;
    }).bind(this);

    local.on_remove = _on_remove;
    _success = (function flx__success (stream) {
        var _onmessage, init_pc, log_resized_video, log_video_loaded, on_timer, password, server, username, ws_onmessage;
        server = "pytigon.cloud";
        username = "auto";
        password = "anawa";
        ws_onmessage = ws.onmessage;
        on_timer = (function flx_on_timer () {
            if (_pyfunc_truthy(ws)) {
                ws.send(JSON.stringify(({ping: 1})));
            }
            if ((_pyfunc_truthy(pc) && ((!_pyfunc_truthy(host))) && ((!_pyfunc_truthy(connected))))) {
                createOffer();
            }
            return null;
        }).bind(this);

        timer = setInterval(on_timer, 10000);
        init_pc = (function flx_init_pc () {
            var _onaddremotestream, _onicecandidate, _onremovestream;
            pc = new PeerConnection(get_configuration(server, username, password));
            _onaddremotestream = (function flx__onaddremotestream (event) {
                remote.srcObject = event.stream;
                remote.play();
                logStreaming(true);
                return null;
            }).bind(this);

            pc.onaddstream = _onaddremotestream;
            _onremovestream = (function flx__onremovestream (event) {
                console.log("onremovestream:");
                console.log(event);
                return null;
            }).bind(this);

            pc.onremovestream = _onremovestream;
            _onicecandidate = (function flx__onicecandidate (event) {
                if (_pyfunc_truthy(event.candidate)) {
                    ws.send(JSON.stringify(event.candidate));
                }
                return null;
            }).bind(this);

            pc.addEventListener("icecandidate", _onicecandidate);
            return null;
        }).bind(this);

        init_pc();
        log_video_loaded = (function flx_log_video_loaded (event) {
            var video;
            video = event.target;
            console.log(video.id);
            console.log(video.videoWidth);
            console.log(video.videoHeight);
            return null;
        }).bind(this);

        log_resized_video = (function flx_log_resized_video (event) {
            log_video_loaded(event);
            return null;
        }).bind(this);

        local.addEventListener("loadedmetadata", log_video_loaded);
        remote.addEventListener("loadedmetadata", log_video_loaded);
        remote.addEventListener("onresize", log_resized_video);
        _onmessage = (function flx__onmessage (event) {
            var signal;
            signal = JSON.parse(event.data);
            if (_pyfunc_truthy(signal.sdp)) {
                if (_pyfunc_truthy(initiator)) {
                    receiveAnswer(signal);
                } else {
                    receiveOffer(signal);
                }
            } else if (_pyfunc_truthy(signal.candidate)) {
                pc.addIceCandidate(new IceCandidate(signal));
            } else if (_pyfunc_truthy(signal.destroy)) {
                if (_pyfunc_truthy(pc)) {
                    pc.close();
                }
                init_pc();
                pc.addStream(stream);
                connected = false;
            } else {
                ws_onmessage(event);
            }
            return null;
        }).bind(this);

        ws.onmessage = _onmessage;
        if (_pyfunc_truthy(stream)) {
            pc.addStream(stream);
            local.srcObject = stream;
            local.play();
        }
        if (_pyfunc_truthy(initiator)) {
            createOffer();
        } else {
            log("Waiting for guest connection..");
        }
        logStreaming(false);
        return null;
    }).bind(this);

    _fail = (function flx__fail () {
        var argi;
        argi = Array.prototype.slice.call(arguments);
        traceback.innerHTML = Array.prototype.join.call(argi, " ");
        traceback.setAttribute("class", "bg-danger");
        return null;
    }).bind(this);

    initialize = (function flx_initialize () {
        var constraints;
        constraints = ({audio: true, video: true});
        navigator.getUserMedia(constraints, _success, _fail);
        return null;
    }).bind(this);

    _socketCallback = (function flx__socketCallback (event) {
        var signal;
        signal = JSON.parse(event.data);
        if (_pyfunc_truthy(signal.status)) {
            if (_pyfunc_op_equals(signal.status, "connected")) {
                if (_pyfunc_truthy(host)) {
                    ws.send(JSON.stringify(({init_consumer: 1, room: room, host: host})));
                } else {
                    ws.send(JSON.stringify(({init_consumer: 1, room: room})));
                }
            } else if (_pyfunc_op_equals(signal.status, "initiated")) {
                initialize();
            }
        }
        return null;
    }).bind(this);

    ws.onmessage = _socketCallback;
    createOffer = (function flx_createOffer () {
        var _create_offer;
        log("Creating offer. Please wait.");
        _create_offer = (function flx__create_offer (offer) {
            var set_description;
            log("Success offer");
            set_description = (function flx_set_description () {
                log("Sending to remote..");
                ws.send(JSON.stringify(offer));
                return null;
            }).bind(this);

            pc.setLocalDescription(offer, set_description, _fail);
            return null;
        }).bind(this);

        pc.createOffer(_create_offer, _fail);
        return null;
    }).bind(this);

    receiveOffer = (function flx_receiveOffer (offer) {
        var set_remote_description;
        log("Received offer.");
        set_remote_description = (function flx_set_remote_description () {
            var create_answer;
            log("Creating response");
            create_answer = (function flx_create_answer (answer) {
                var set_local_description;
                log("Created response");
                set_local_description = (function flx_set_local_description () {
                    var connected;
                    log("Sent response");
                    ws.send(JSON.stringify(answer));
                    connected = true;
                    return null;
                }).bind(this);

                pc.setLocalDescription(answer, set_local_description, _fail);
                return null;
            }).bind(this);

            pc.createAnswer(create_answer, _fail);
            return null;
        }).bind(this);

        pc.setRemoteDescription(new SessionDescription(offer), set_remote_description, _fail);
        return null;
    }).bind(this);

    receiveAnswer = (function flx_receiveAnswer (answer) {
        log("received answer");
        pc.setRemoteDescription(new SessionDescription(answer));
        connected = true;
        return null;
    }).bind(this);

    log = (function flx_log () {
        var argi;
        argi = Array.prototype.slice.call(arguments);
        traceback.innerHTML = Array.prototype.join.call(argi, " ");
        console.log.apply(console, argi);
        return null;
    }).bind(this);

    logStreaming = (function flx_logStreaming (is_streaming) {
        if (_pyfunc_truthy(is_streaming)) {
            streaming.innerHTML = "[streaming]";
        } else {
            streaming.innerHTML = "[.]";
        }
        return null;
    }).bind(this);

    return null;
};

stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/adapter-latest.js"]));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var local, remote, src, streaming, traceback, url;
        remote = component.root.querySelector(".webrtc_remote");
        local = component.root.querySelector(".webrtc_local");
        traceback = component.root.querySelector(".webrtc_traceback");
        streaming = component.root.querySelector("webrtc_streaming");
        url = window.location;
        src = ((url.protocol + "//") + url.host) + component.getAttribute("src");
        init_webrtc(src, component.getAttribute("host"), component.getAttribute("roomId"), local, remote, traceback, streaming);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}
export {get_configuration, init_webrtc};