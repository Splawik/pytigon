var TAG, comp, init, stub1_context, stub2_err;
TAG = "ptig-form";
stub1_context = (new DefineWebComponent(TAG, false));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var _onchange, event, inp, name, selector, stub10_seq, stub11_itr, stub4_seq, stub5_itr, stub6_seq, stub7_itr, stub8_seq, stub9_itr, tab_inp;
        _onchange = function (new_value) {
            var data, on_complete, on_field;
            on_complete = (function flx_on_complete (data) {
                var on_data;
                on_data = (function flx_on_data (key) {
                    var key2, obj, stub3_seq, value2, x;
                    if (_pyfunc_op_contains("__", key)) {
                        x = _pymeth_split.call(key, "__");
                        obj = component.root.querySelector(x[0]);
                        if (_pyfunc_op_equals(x[1], "value")) {
                            obj.value = data[key];
                        } else {
                            (obj[x[1]])(data[key]);
                        }
                    } else if (_pyfunc_op_equals(key, "refresh_ajax_frame")) {
                        refresh_ajax_frame(component, data[key]);
                    } else if (_pyfunc_op_equals(key, "set_state")) {
                        GLOBAL_BUS.set_state(data[key]);
                    } else if (_pyfunc_op_equals(key, "send_event")) {
                        stub3_seq = data[key];
                        for (key2 in stub3_seq) {
                            if (!stub3_seq.hasOwnProperty(key2)){ continue; }
                            value2 = stub3_seq[key2];
                            GLOBAL_BUS.send_event(key2, value2);
                        }
                    } else if (_pyfunc_op_equals(key, "none")) {
                    } else {
                        obj = component.root.querySelector(key);
                        obj.innerHTML = data[key];
                    }
                    return null;
                }).bind(this);

                (Object.keys(data).forEach)(on_data);
                return null;
            }).bind(this);

            data = ({name: this.getAttribute("name"), new_value: this.value});
            on_field = (function flx_on_field (key) {
                data[key] = component.fields[key].value;
                return null;
            }).bind(this);

            (Object.keys(component.fields).forEach)(on_field);
            ajax_json(component.getAttribute("src"), data, on_complete);
            return null;
        };

        component.fields = ({});
        component.figures = ({});
        stub6_seq = ["input", "select", "textarea"];
        if ((typeof stub6_seq === "object") && (!Array.isArray(stub6_seq))) { stub6_seq = Object.keys(stub6_seq);}
        for (stub7_itr = 0; stub7_itr < stub6_seq.length; stub7_itr += 1) {
            selector = stub6_seq[stub7_itr];
            tab_inp = Array.prototype.slice.call(component.root.querySelectorAll(selector));
            stub4_seq = tab_inp;
            if ((typeof stub4_seq === "object") && (!Array.isArray(stub4_seq))) { stub4_seq = Object.keys(stub4_seq);}
            for (stub5_itr = 0; stub5_itr < stub4_seq.length; stub5_itr += 1) {
                inp = stub4_seq[stub5_itr];
                inp.addEventListener("change", _onchange);
                name = inp.getAttribute("name");
                component.fields[name] = inp;
            }
        }
        tab_inp = Array.prototype.slice.call(component.root.querySelectorAll(".plotly"));
        stub10_seq = tab_inp;
        if ((typeof stub10_seq === "object") && (!Array.isArray(stub10_seq))) { stub10_seq = Object.keys(stub10_seq);}
        for (stub11_itr = 0; stub11_itr < stub10_seq.length; stub11_itr += 1) {
            inp = stub10_seq[stub11_itr];
            stub8_seq = ["click", "hover", "unhover", "relayout", "selected", "legendclick"];
            if ((typeof stub8_seq === "object") && (!Array.isArray(stub8_seq))) { stub8_seq = Object.keys(stub8_seq);}
            for (stub9_itr = 0; stub9_itr < stub8_seq.length; stub9_itr += 1) {
                event = stub8_seq[stub9_itr];
                inp.on("plotly_" + event_name, _onchange);
                name = inp.getAttribute("name");
                component.figures[name] = inp;
            }
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}