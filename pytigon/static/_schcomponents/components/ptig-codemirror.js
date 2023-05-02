var BASE_PATH, TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-codemirror";
TEMPLATE = '        <div name=\"codemirror\"></div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
stub1_context = (new DefineWebComponent(TAG, false, [BASE_PATH + "/codemirror.bundle.js"]));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var editor;
        editor = window.init_editor(component.root);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}