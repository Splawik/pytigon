var BASE_PATH, TAG, TEMPLATE, comp, disconnectedCallback, init, init2, stub1_context, stub2_err;
TAG = "ptig-xterm";
TEMPLATE = '        <div name=\"xterm\" data-bind=\"style-width:width;style-height:height\"></div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/xterm";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/xterm.js", BASE_PATH + "/fit.js"], [BASE_PATH + "/xterm.css"]));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null});
    comp.options["template"] = TEMPLATE;
    init2 = function flx_init2 (component) {
        var _on_websocket_open, address, div, on_timer, term, timer, websocket;
        div = component.root.querySelector("div");
        Terminal.applyAddon(fit);
        address = location.hostname;
        if (_pyfunc_truthy(location.port)) {
            address = _pyfunc_op_add(address, ":" + location.port);
        }
        address = _pyfunc_op_add(address, component.getAttribute("href"));
        if ((!_pyfunc_op_equals(location.protocol, "https:"))) {
            address = "ws://" + address;
        } else {
            address = "wss://" + address;
        }
        websocket = new WebSocket(address);
        component.websocket = websocket;
        term = new Terminal();
        term.open(div);
        term.setOption("fontFamily", "monospace");
        term.setOption("fontSize", 14);
        term.setOption("lineHeight", 1.1);
        term.setOption("theme", ({background: "#222d32"}));
        component.term = term;
        on_timer = (function flx_on_timer () {
            if (_pyfunc_truthy(websocket)) {
                websocket.send(JSON.stringify(({ping: 1})));
            }
            return null;
        }).bind(this);

        timer = setInterval(on_timer, 10000);
        component.timer = timer;
        _on_websocket_open = (function flx__on_websocket_open () {
            var _fit_to_screen, _on_key, _on_message, _process_resize;
            _fit_to_screen = (function flx__fit_to_screen () {
                var s;
                try {
                    term.fit();
                } catch(err_5) {
                    {
                    }
                }
                s = JSON.stringify(({resize: ({cols: term.cols, rows: term.rows})}));
                websocket.send(s);
                return null;
            }).bind(this);

            _on_key = (function flx__on_key (key, ev) {
                var txt;
                txt = JSON.stringify(({input: key}));
                websocket.send(txt);
                return null;
            }).bind(this);

            _on_message = (function flx__on_message (evt) {
                if (_pyfunc_op_equals(evt.data, "pong")) {
                } else {
                    term.write(evt.data);
                }
                return null;
            }).bind(this);

            term.on("key", _on_key);
            websocket.onmessage = _on_message;
            _process_resize = (function flx__process_resize (size_object) {
                component.set_state(({height: ((size_object["h"] - size_object["body_offset_y"]) - 3) + "px"}));
                _fit_to_screen();
                return null;
            }).bind(this);

            component.process_resize = _process_resize;
            window.process_resize(component);
            return null;
        }).bind(this);

        websocket.onopen = _on_websocket_open;
        return null;
    };

    init = function flx_init (component) {
        setTimeout(init2, 1, component);
        return null;
    };

    comp.options["init"] = init;
    disconnectedCallback = function flx_disconnectedCallback (component) {
        var _on_close;
        window.clearInterval(component.timer);
        component.timer = null;
        _on_close = (function flx__on_close () {
            component.term.dispose();
            component.term = null;
            return null;
        }).bind(this);

        component.websocket.onclose = _on_close;
        if (_pyfunc_truthy(component.websocket)) {
            component.websocket.close();
            component.websocket = null;
        }
        return null;
    };

    comp.options["disconnectedCallback"] = disconnectedCallback;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}