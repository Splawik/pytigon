var TAG, TEMPLATE, comp, stub1_context, stub2_err, v;
TAG = "ptig-margin-left";
TEMPLATE = '        <div>\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    v = function flx_v (component, old_value, new_value) {
        var div, margin, parent, width, x;
        if ((new_value < 0)) {
            x = 0;
        } else if ((x > 1)) {
            x = 1;
        } else {
            x = new_value;
        }
        parent = component.parentElement.parentElement;
        width = parent.offsetWidth;
        margin = (_pyfunc_op_mult(width, _pyfunc_float(x))) / 4;
        div = component.root.querySelector("div");
        div.style.marginLeft = _pyfunc_str(margin) + "px";
        return null;
    };

    comp.options["attributes"] = ({v: v});
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}