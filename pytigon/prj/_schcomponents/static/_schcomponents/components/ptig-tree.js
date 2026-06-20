var TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-tree";
TEMPLATE = '<div class=\"tree\" data-bind=\"style-width:width;style-height:height\">\n' +
    '        <slot></slot>\n' +
    '</div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var state;
        component.classList.add("tree");
        state = ({});
        state["onclick"] = window.handle_click;
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}