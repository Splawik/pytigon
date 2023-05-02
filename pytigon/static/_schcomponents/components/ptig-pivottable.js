var BASE_PATH, TAG, comp, height, init, stub1_context, stub2_err, width;
TAG = "ptig-pivottable";
BASE_PATH = window.BASE_PATH + "static/jquery_plugins/pivottable";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/pivot.js", BASE_PATH + "/../jquery.ui/jquery-ui.min.js"], [BASE_PATH + "/pivot.min.css"]));
comp = stub1_context.__enter__();
try {
    width = function flx_width (component, old_value, new_value) {
        component.style.width = new_value;
        return null;
    };

    height = function flx_height (component, old_value, new_value) {
        component.style.height = new_value;
        return null;
    };

    comp.options["attributes"] = ({width: width, height: height});
    comp.options["template"] = "<style></style>";
    init = function flx_init (component) {
        var data, options;
        data = [({color: "blue", shape: "circle"}), ({color: "red", shape: "triangle"})];
        options = ({rows: ["color"], cols: ["shape"]});
        component["pivottable"] = (jQuery(component.root).pivotUI)(data, options);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}