var TAG, TEMPLATE, comp, disconnectedCallback, init, stub1_context, stub2_err;
TAG = "ptig-task";
TEMPLATE = '<div name=\'task\'><slot></slot></div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, false));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var _on_websocket_open, address, on_timer;
        component.timer = null;
        component.websocket = null;
        address = location.hostname;
        if (_pyfunc_truthy(location.port)) {
            address = _pyfunc_op_add(address, ":" + location.port);
        }
        if (_pyfunc_truthy(component.hasAttribute("websocket_href"))) {
            address = _pyfunc_op_add(address, component.getAttribute("websocket_href"));
        }
        if ((!_pyfunc_op_equals(location.protocol, "https:"))) {
            address = "ws://" + address;
        } else {
            address = "wss://" + address;
        }
        component.websocket = new WebSocket(address);
        on_timer = (function flx_on_timer () {
            if (_pyfunc_truthy(component.websocket)) {
                component.websocket.send(JSON.stringify(({ping: 1})));
            }
            return null;
        }).bind(this);

        component.timer = setInterval(on_timer, 10000);
        _on_websocket_open = (function flx__on_websocket_open () {
            var _complete, _on_message, div;
            div = component;
            _on_message = (function flx__on_message (evt) {
                var html, jdata, status, task_end_info, task_status;
                jdata = JSON.parse(evt.data);
                status = jdata["status"];
                if (_pyfunc_op_equals(status, "pong")) {
                    console.log("pong");
                } else if (_pyfunc_op_equals(status, "start")) {
                    task_status = _pymeth_find.call(jQuery(div), ("[name=\"task_status\"]"));
                    if ((task_status.length > 0)) {
                        task_status.addClass("task_started");
                    }
                } else if (_pyfunc_op_equals(status, "stop")) {
                    task_status = _pymeth_find.call(jQuery(div), ("[name=\"task_status\"]"));
                    if ((task_status.length > 0)) {
                        task_status.removeClass("task_started");
                        task_status.addClass("task_finished");
                    }
                    task_end_info = _pymeth_find.call(jQuery(div), ("[name=\"task_end_info\"]"));
                    if ((task_end_info.length > 0)) {
                        task_end_info.show();
                    }
                } else if (_pyfunc_op_equals(status, "event")) {
                    html = jdata["data"];
                    window.send_to_dom(html, div);
                } else {
                    console.log(evt.data);
                }
                return null;
            }).bind(this);

            component.websocket.onmessage = _on_message;
            if (_pyfunc_truthy(component.hasAttribute("task_href"))) {
                _complete = (function flx__complete () {
                    console.log("task started");
                    return null;
                }).bind(this);

                ajax_get(component.getAttribute("task_href"), _complete);
            }
            if (_pyfunc_truthy(component.hasAttribute("task_id"))) {
                component.websocket.send(JSON.stringify(({id: component.getAttribute("task_id")})));
            }
            return null;
        }).bind(this);

        component.websocket.onopen = _on_websocket_open;
        return null;
    };

    comp.options["init"] = init;
    disconnectedCallback = function flx_disconnectedCallback (component) {
        var _on_close;
        window.clearInterval(component.timer);
        component.timer = null;
        _on_close = (function flx__on_close () {
            component.websocket = null;
            return null;
        }).bind(this);

        component.websocket.onclose = _on_close;
        if (_pyfunc_truthy(component.websocket)) {
            component.websocket.close();
            component.websocket = null;
        }
        console.log("disconnectedCallbaack()");
        return null;
    };

    comp.options["disconnectedCallback"] = disconnectedCallback;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}