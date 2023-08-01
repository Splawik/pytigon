var BASE_PATH, TAG, comp, css_libs, height, init, js_libs, stub1_context, stub2_err, width;
TAG = "ptig-spreadsheet";
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
js_libs = [BASE_PATH + "/jsuites/jsuites.js", BASE_PATH + "/jexcel/jexcel.js"];
css_libs = [BASE_PATH + "/jsuites/jsuites.css", BASE_PATH + "/jexcel/jexcel.css"];
stub1_context = (new DefineWebComponent(TAG, false, js_libs, css_libs));
comp = stub1_context.__enter__();
try {
    width = function flx_width (component, old_value, new_value) {
        component.root.style.width = new_value;
        return null;
    };

    height = function flx_height (component, old_value, new_value) {
        component.root.style.height = new_value;
        return null;
    };

    comp.options["attributes"] = ({width: width, height: height});
    comp.options["template"] = "";
    init = function flx_init (component) {
        var columns, data;
        columns = [({type: "text", title: "Column A", width: 120}), ({type: "text", title: "Column B", width: 120}), ({type: "text", title: "Column C", width: 120})];
        data = [["1", "2", "3"]];
        component.jtable = jspreadsheet(component, ({data: data, columns: columns, minDimensions: [10, 10]}));
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}