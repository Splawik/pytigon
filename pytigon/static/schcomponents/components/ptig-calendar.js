var BASE_PATH, TAG, TEMPLATE, comp, css_tab, height, init, js_tab, stub1_context, stub2_err, width;
TAG = "ptig-calendar";
TEMPLATE = '        <div name=\"calendar\" style=\"{ width: 100%, height: 100%}\"></div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/jquery_plugins/fullcalendar";
js_tab = [BASE_PATH + "/core/main.min.js", "|", BASE_PATH + "/daygrid/main.min.js"];
css_tab = [BASE_PATH + "/core/main.min.css", BASE_PATH + "/daygrid/main.min.css"];
stub1_context = (new DefineWebComponent(TAG, false, js_tab, css_tab));
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
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var calendar, div, plugins;
        div = component.root.querySelector("div");
        plugins = ["dayGrid"];
        calendar = new FullCalendar.Calendar(div, ({plugins: plugins}));
        calendar.render();
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0; }
if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
} else { stub1_context.__exit__(null, null, null); }