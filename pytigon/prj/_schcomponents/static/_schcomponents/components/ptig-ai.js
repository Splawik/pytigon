var TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-ai";
TEMPLATE = '<div name=\"ai-chat\" class=\"ai-chat\">\n' +
    '        <div class=\"container\">\n' +
    '                <div class=\"row\">\n' +
    '                        <div class=\"col content\">\n' +
    '                                <p></p>\n' +
    '                        </div>\n' +
    '                </div>\n' +
    '                <div class=\"row\">\n' +
    '                        <div class=\"d-flex\">\n' +
    '                                <textarea name=\"txt\" class=\"class=p-1 form-control flex-grow-1 txt\" rows=\"4\"></textarea>\n' +
    '                                <div class=\"p-1\">\n' +
    '                                        <button type=\"button\" class=\"btn btn-primary h-100\" data-bind=\"onclick:onclickok\">\n' +
    '                                                >\n' +
    '                                        </button>\n' +
    '                                </div>\n' +
    '                                <div class=\"p-1\">\n' +
    '                                        <button type=\"button\" class=\"btn btn-danger h-100\" data-bind=\"onclick:onclickcancel\">\n' +
    '                                                |\n' +
    '                                        </button>\n' +
    '                                </div>\n' +
    '                        </div>\n' +
    '                </div>\n' +
    '        </div>\n' +
    '</div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, false));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _on_websocket_open, _onclick_cancel, _onclick_ok, address, content_p, div, state, txt;
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
        div = component;
        content_p = div.querySelector("div.content > p");
        txt = div.querySelector("textarea.txt");
        _on_websocket_open = (function flx__on_websocket_open () {
            var _on_message;
            _on_message = (function flx__on_message (evt) {
                var html, jdata, status;
                jdata = JSON.parse(evt.data);
                if (_pyfunc_op_contains("status", jdata)) {
                    status = jdata["status"];
                } else {
                    status = "data";
                }
                if (_pyfunc_op_equals(status, "data")) {
                    html = jdata["content"];
                    if (_pyfunc_op_contains("---", html)) {
                        txt.disabled = false;
                        txt.focus();
                    } else {
                        content_p.insertAdjacentHTML("beforeend", _pymeth_replace.call(html, "\n", "<br />"));
                    }
                } else {
                    console.log(evt.data);
                }
                return null;
            }).bind(this);

            component.websocket.onmessage = _on_message;
            return null;
        }).bind(this);

        component.websocket.onopen = _on_websocket_open;
        _onclick_ok = (function flx__onclick_ok (event) {
            if (_pyfunc_truthy(component.websocket)) {
                component.websocket.send(JSON.stringify(({id: 1, content: txt.value})));
            }
            content_p.insertAdjacentHTML("beforeend", ("</p><div class='alert alert-info' role='alert'>" + txt.value) + "</div><p>");
            txt.value = "";
            txt.disabled = true;
            return null;
        }).bind(this);

        _onclick_cancel = (function flx__onclick_cancel (event) {
            if (_pyfunc_truthy(component.websocket)) {
                component.websocket.close();
                component.websocket = new WebSocket(address);
                component.websocket.onopen = _on_websocket_open;
                txt.disabled = false;
                txt.focus();
            }
            return null;
        }).bind(this);

        state = ({});
        state["onclickok"] = _onclick_ok;
        state["onclickcancel"] = _onclick_cancel;
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}