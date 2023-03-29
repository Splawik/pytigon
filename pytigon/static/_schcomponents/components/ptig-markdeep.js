var BASE_PATH, TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-markdeep";
TEMPLATE = '        <div name=\"markdeep style=visibility:hidden\">\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/markdeep";
window.markdeepOptions = ({mode: "script"});
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/markdeep.min.js"], [BASE_PATH + "/whitepaper.css", BASE_PATH + "/diagram.css"]));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var div, ret, txt;
        div = component.root.querySelector("div");
        txt = component.childNodes[0].nodeValue;
        ret = _pymeth_format.call(window.markdeep, txt);
        div.innerHTML = ret;
        div.visibility = "visible";
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0; }
if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
} else { stub1_context.__exit__(null, null, null); }