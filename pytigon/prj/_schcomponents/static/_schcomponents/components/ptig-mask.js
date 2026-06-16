var TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-mask";
TEMPLATE = '        <slot></slot>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true, []));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var input;
        input = component.querySelector("input");
        ((new Inputmask()).mask)(input);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}