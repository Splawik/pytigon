var BASE_PATH, TAG, TEMPLATE, comp, height, init, stub1_context, stub2_err, width;
TAG = "ptig-codeeditor";
TEMPLATE = '<style>\n' +
    '        .codeeditor-button {\n' +
    '            background-color: #008CBA;\n' +
    '            border: none;\n' +
    '            color: white;\n' +
    '            padding: 11px 32px;\n' +
    '            text-align: center;\n' +
    '            text-decoration: none;\n' +
    '            display: inline-block;\n' +
    '            font-size: 16px;\n' +
    '            margin: 2px 0px;\n' +
    '            cursor: pointer;\n' +
    '            height: 3rem;\n' +
    '        }\n' +
    '        button.codeeditor-button:disabled { background-color: lightgray; }\n' +
    '        p.function_title {\n' +
    '            background: darkslategray;\n' +
    '            color: gold;\n' +
    '            margin: 0px;\n' +
    '            padding: 0px 45px;\n' +
    '            font-size: 16px;\n' +
    '            font-weight: bold;\n' +
    '            margin-right: 0px;\n' +
    '        }\n' +
    '        h2 { text-align: center; paddin:0; margin:0; }\n' +
    '        .bar { height: 3rem; border-spacing: 0px; }\n' +
    '        .vseditor { top: 3.5rem; left:0; right:0; bottom:0; border-width: 1px; border-style: dotted; }\n' +
    '        button.codeeditor-button svg { width: 24px; height: 24px; }\n' +
    '        .td_width { width: 6rem; }\n' +
    '</style>\n' +
    '<div data-bind=\"style-width:width;style-height:height;\" style=\"position:relative;overflow: hidden;\">\n' +
    '        <slot>\n' +
    '                <table class=\"bar\" width=\"100%\">\n' +
    '                        <tr>\n' +
    '                                <td class=\"td_width\">\n' +
    '                                        <form class=\"form-inline\">\n' +
    '                                                <button data-bind=\"disabled:!changed;onclick:on_save\" class=\"codeeditor-button btn btn-primary\" type=\"button\">\n' +
    '                                                        <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"feather feather-save\"><path d=\"M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z\"></path><polyline points=\"17 21 17 13 7 13 7 21\"></polyline><polyline points=\"7 3 7 8 15 8\"></polyline></svg>\n' +
    '                                                </button>\n' +
    '                                        </form>\n' +
    '                                </td>\n' +
    '                                <td>\n' +
    '                                        <h2>\n' +
    '                                                <span class=\"navbar-text mr-auto\" data-bind=\"title\"></span>\n' +
    '                                        </h2>\n' +
    '                                </td>\n' +
    '                                <td class=\"td_width\">\n' +
    '                                        &nbsp;\n' +
    '                                </td>\n' +
    '                        </tr>\n' +
    '                </table>\n' +
    '        </slot>\n' +
    '        <p class=\"function_title\" data-bind=\"function-title;style-visibility:function_title_visibility\"></p>\n' +
    '        <div class=\"vseditor\" name=\"vseditor\" style=\"position:absolute;\" data-bind=\"style-top:top\"></div>\n' +
    '</div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/vs";
stub1_context = (new DefineWebComponent(TAG, true, [], [BASE_PATH + "/editor/editor.main.css"]));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    width = function flx_width (component, old_value, new_value) {
        var div;
        if (_pyfunc_hasattr(component, "editor")) {
            div = component.root.querySelector("div");
            div.style.width = new_value;
            component.editor.layout();
        }
        return null;
    };

    height = function flx_height (component, old_value, new_value) {
        var div;
        if (_pyfunc_hasattr(component, "editor")) {
            div = component.root.querySelector("div");
            div.style.height = new_value;
            component.editor.layout();
        }
        return null;
    };

    comp.options["attributes"] = _pyfunc_create_dict("width", width, "height", height, "function-title", null, "title", null);
    init = function flx_init (component) {
        var _on_loadjs, function_title_visibility, on_save, save, state;
        _on_loadjs = (function flx__on_loadjs () {
            var _changed, ed, state, theme, top, value;
            ed = component.root.querySelector("div.vseditor");
            if (_pyfunc_truthy(component.hasAttribute("value"))) {
                value = decodeURIComponent(escape(atob(component.getAttribute("value"))));
            } else {
                value = "";
            }
            if (_pyfunc_truthy(component.hasAttribute("theme"))) {
                theme = component.getAttribute("theme");
            } else {
                theme = "vs";
            }
            component.editor = monaco.editor.create(ed, ({value: value, language: "python", theme: theme, wordWrap: "off", wordWrapMinified: false}));
            _changed = (function flx__changed (event) {
                component.set_state(({changed: true}));
                return null;
            }).bind(this);

            component.editor.onDidChangeModelContent(_changed);
            top = ed.offsetTop;
            state = ({top: top + "px", bottom: 0});
            if (_pyfunc_truthy(component.hasAttribute("width"))) {
                state["width"] = component.getAttribute("width");
            }
            if (_pyfunc_truthy(component.hasAttribute("height"))) {
                state["height"] = component.getAttribute("height");
            }
            if (_pyfunc_truthy(component.hasAttribute("offset"))) {
                state["top"] = component.getAttribute("offset");
            } else {
                state["top"] = "3.5rem";
            }
            component.set_state(state);
            component.editor.layout();
            return null;
        }).bind(this);

        require.config(({paths: ({vs: BASE_PATH})}));
        require(["vs/editor/editor.main"], _on_loadjs);
        save = (function flx_save (callback) {
            var ajax_options, href;
            if (_pyfunc_truthy(component.hasAttribute("href"))) {
                href = component.getAttribute("href");
                ajax_options = ({method: "POST", url: href, dataType: "html", data: ({data: component.editor.getValue()})});
                (jQuery.ajax(ajax_options).done)(callback);
            }
            return null;
        }).bind(this);

        on_save = (function flx_on_save (event) {
            var _on_ajax;
            _on_ajax = (function flx__on_ajax () {
                component.set_state(({changed: false}));
                return null;
            }).bind(this);

            save(_on_ajax);
            return null;
        }).bind(this);

        if (_pyfunc_truthy((_pyfunc_truthy(component.hasAttribute("function-title"))) && (_pyfunc_truthy(component.getAttribute("function-title"))))) {
            function_title_visibility = "block";
        } else {
            function_title_visibility = "hidden";
        }
        state = ({on_save: on_save, save: save, changed: false, function_title_visibility: function_title_visibility});
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}