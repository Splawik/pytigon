var TAG, TEMPLATE, comp, disconnectedCallback, init, stub1_context, stub2_err;
TAG = "ptig-time";
TEMPLATE = '        <slot></slot>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _on_time;
        _on_time = (function flx__on_time () {
            var d, t;
            d = new Date();
            t = _pymeth_replace.call(d.toISOString(), "T", " ");
            component.set_state(({time: t.slice(11,19), date: t.slice(0,10), datetime: t.slice(0,19), time_short: t.slice(11,16), datetimeshort: t.slice(0,16)}));
            return null;
        }).bind(this);

        component.timer = setInterval(_on_time, 250);
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