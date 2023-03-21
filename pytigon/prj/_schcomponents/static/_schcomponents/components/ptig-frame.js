var TAG, TEMPLATE, comp, disconnectedCallback, init, stub1_context, stub2_err;
TAG = "ptig-frame";
TEMPLATE = '        <div></div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, false));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _on_time, div, timeout;
        timeout = _pyfunc_int(component.getAttribute("timeout"));
        div = component.root.querySelector("div");
        _on_time = (function flx__on_time () {
            var on_load;
            on_load = (function flx_on_load (data) {
                div.innerHTML = data;
                return null;
            }).bind(this);

            ajax_get(component.getAttribute("src"), on_load);
            return null;
        }).bind(this);

        component.timer = setInterval(_on_time, _pyfunc_op_mult(timeout, 1000));
        _on_time();
        return null;
    };

    comp.options["init"] = init;
    disconnectedCallback = function flx_disconnectedCallback (component) {
        if (_pyfunc_truthy(component.timer)) {
            clearTimeout(component.timer);
            component.timer = null;
        }
        return null;
    };

    comp.options["disconnectedCallback"] = disconnectedCallback;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}