var BASE_PATH, TAG, comp, css_libs, height, init, js_libs, stub1_context, stub2_err, width;
TAG = "ptig-spreadsheet";
BASE_PATH = window.BASE_PATH + "static/_schcomponents/tabulator/";
js_libs = [BASE_PATH + "tabulator.js"];
css_libs = [BASE_PATH + "tabulator.css"];
stub1_context = (new DefineWebComponent(TAG, false, js_libs, css_libs, true));
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
        var tabledata, tabulator;
        tabulator = component.modules[0];
        tabledata = [({id: 1, name: "Oli Bob", progress: 12, gender: "male", rating: 1, col: "red", dob: "19/02/1984", car: 1}), ({id: 2, name: "Mary May", progress: 1, gender: "female", rating: 2, col: "blue", dob: "14/05/1982", car: true}), ({id: 3, name: "Christine Lobowski", progress: 42, gender: "female", rating: 0, col: "green", dob: "22/05/1982", car: "true"}), ({id: 4, name: "Brendon Philips", progress: 100, gender: "male", rating: 1, col: "orange", dob: "01/08/1980"}), ({id: 5, name: "Margret Marmajuke", progress: 16, gender: "female", rating: 5, col: "yellow", dob: "31/01/1999"}), ({id: 6, name: "Frank Harbours", progress: 38, gender: "male", rating: 4, col: "red", dob: "12/05/1966", car: 1})];
        component.table = new tabulator.Tabulator(component, ({data: tabledata, autoColumns: true}));
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}