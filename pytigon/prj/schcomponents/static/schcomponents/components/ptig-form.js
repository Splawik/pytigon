var TAG, comp, init, stub1_context, stub2_err;
TAG = "ptig-form";
stub1_context = (new DefineWebComponent(TAG, false));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var _onchange, event, inp, name, selector, stub10_itr, stub3_seq, stub4_itr, stub5_seq, stub6_itr, stub7_seq, stub8_itr, stub9_seq, tab_inp;
        _onchange = function (new_value) {
            var data, on_complete, on_field;
            on_complete = (function flx_on_complete (data) {
                var on_data;
                on_data = (function flx_on_data (key) {
                    var obj, x;
                    if (_pyfunc_op_contains("__", key)) {
                        x = _pymeth_split.call(key, "__");
                        obj = component.root.querySelector(x[0]);
                        (obj[x[1]])(data[key]);
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
        stub5_seq = ["input", "select", "textarea"];
        if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
        for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
            selector = stub5_seq[stub6_itr];
            tab_inp = Array.prototype.slice.call(component.root.querySelectorAll(selector));
            stub3_seq = tab_inp;
            if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
            for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                inp = stub3_seq[stub4_itr];
                inp.addEventListener("change", _onchange);
                name = inp.getAttribute("name");
                component.fields[name] = inp;
            }
        }
        tab_inp = Array.prototype.slice.call(component.root.querySelectorAll(".plotly"));
        stub9_seq = tab_inp;
        if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
        for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
            inp = stub9_seq[stub10_itr];
            stub7_seq = ["click", "hover", "unhover", "relayout", "selected", "legendclick"];
            if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
            for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
                event = stub7_seq[stub8_itr];
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