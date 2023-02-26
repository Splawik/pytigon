var TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "test-options";
TEMPLATE = '        <ul data-bind=\"data\"></ul>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var child, data, stub3_seq, stub4_itr;
        data = "";
        stub3_seq = Array.prototype.slice.call(component.children);
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            child = stub3_seq[stub4_itr];
            data = _pyfunc_op_add(data, ("<li>" + child.innerHTML) + "</li>");
        }
        component.set_state(({data: data}));
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}