var TAG, comp, get_select_values, init, stub3_context, stub4_err;
TAG = "ptig-form";
get_select_values = function flx_get_select_values (select) {
    var opt, opt_id, result, stub1_seq, stub2_itr;
    result = [];
    stub1_seq = select.options;
    if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
    for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
        opt_id = stub1_seq[stub2_itr];
        opt = select.options[opt_id];
        if (_pyfunc_truthy(opt.selected)) {
            _pymeth_append.call(result, (_pyfunc_truthy(opt.value) || opt.text));
        }
    }
    return result;
};

stub3_context = (new DefineWebComponent(TAG, false));
comp = stub3_context.__enter__();
try {
    init = function flx_init (component) {
        var _onchange, event, inp, name, selector, stub10_seq, stub11_itr, stub12_seq, stub13_itr, stub6_seq, stub7_itr, stub8_seq, stub9_itr, tab_inp;
        _onchange = function (new_value) {
            var data, on_complete, on_field, value;
            on_complete = (function flx_on_complete (data) {
                var on_data;
                on_data = (function flx_on_data (key) {
                    var key2, obj, stub5_seq, value2, x;
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
                        stub5_seq = data[key];
                        for (key2 in stub5_seq) {
                            if (!stub5_seq.hasOwnProperty(key2)){ continue; }
                            value2 = stub5_seq[key2];
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

            if (_pyfunc_truthy(this.hasAttribute("multiple"))) {
                value = get_select_values(this);
            } else {
                value = this.value;
            }
            data = ({name: this.getAttribute("name"), new_value: value});
            on_field = (function flx_on_field (key) {
                if (_pyfunc_truthy((component.fields[key].hasAttribute)("multiple"))) {
                    data[key] = get_select_values(component.fields[key]);
                } else {
                    data[key] = component.fields[key].value;
                }
                return null;
            }).bind(this);

            (Object.keys(component.fields).forEach)(on_field);
            ajax_json(component.getAttribute("src"), data, on_complete);
            return null;
        };

        component.fields = ({});
        component.figures = ({});
        stub8_seq = ["input", "select", "textarea"];
        if ((typeof stub8_seq === "object") && (!Array.isArray(stub8_seq))) { stub8_seq = Object.keys(stub8_seq);}
        for (stub9_itr = 0; stub9_itr < stub8_seq.length; stub9_itr += 1) {
            selector = stub8_seq[stub9_itr];
            tab_inp = Array.prototype.slice.call(component.root.querySelectorAll(selector));
            stub6_seq = tab_inp;
            if ((typeof stub6_seq === "object") && (!Array.isArray(stub6_seq))) { stub6_seq = Object.keys(stub6_seq);}
            for (stub7_itr = 0; stub7_itr < stub6_seq.length; stub7_itr += 1) {
                inp = stub6_seq[stub7_itr];
                inp.addEventListener("change", _onchange);
                name = inp.getAttribute("name");
                component.fields[name] = inp;
            }
        }
        tab_inp = Array.prototype.slice.call(component.root.querySelectorAll(".plotly"));
        stub12_seq = tab_inp;
        if ((typeof stub12_seq === "object") && (!Array.isArray(stub12_seq))) { stub12_seq = Object.keys(stub12_seq);}
        for (stub13_itr = 0; stub13_itr < stub12_seq.length; stub13_itr += 1) {
            inp = stub12_seq[stub13_itr];
            stub10_seq = ["click", "hover", "unhover", "relayout", "selected", "legendclick"];
            if ((typeof stub10_seq === "object") && (!Array.isArray(stub10_seq))) { stub10_seq = Object.keys(stub10_seq);}
            for (stub11_itr = 0; stub11_itr < stub10_seq.length; stub11_itr += 1) {
                event = stub10_seq[stub11_itr];
                inp.on("plotly_" + event_name, _onchange);
                name = inp.getAttribute("name");
                component.figures[name] = inp;
            }
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub4_err=err_0;
} finally {
    if (stub4_err) { if (!stub3_context.__exit__(stub4_err.name || "error", stub4_err, null)) { throw stub4_err; }
    } else { stub3_context.__exit__(null, null, null); }
}
export {get_select_values};