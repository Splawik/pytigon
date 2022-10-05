var BASE_PATH, TAG, comp, init, stub1_context, stub2_err;
TAG = "ptig-script";
BASE_PATH = window.BASE_PATH + "static/";
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var finish, src;
        src = component.getAttribute("src");
        finish = (function flx_finish () {
            return null;
        }).bind(this);

        window.load_js(src, finish);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}