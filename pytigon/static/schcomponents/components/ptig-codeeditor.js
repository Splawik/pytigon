var BASE_PATH, TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-codeeditor";
TEMPLATE = '<style>\n' +
    '        .button {\n' +
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
    '        }\n' +
    '        .button:disabled { background-color: lightgray; }\n' +
    '        p.function_title {\n' +
    '            background: darkslategray;\n' +
    '            color: gold;\n' +
    '            margin: 0px;\n' +
    '            padding: 0px 45px;\n' +
    '            font-size: 16px;\n' +
    '            font-weight: bold;\n' +
    '            margin-right: 0px;\n' +
    '        }\n' +
    '        h2 { text-align: center; position: absolute; left: 0; right: 0; margin-left: 150px; margin-right: 150px; }\n' +
    '</style>\n' +
    '<div data-bind=\"style-width:width;style-height:height;\" style=\"position:relative;\">\n' +
    '        <slot>\n' +
    '                <div width=\"100%\">\n' +
    '                        <h2>\n' +
    '                                <span class=\"navbar-text mr-auto\" data-bind=\"title\"></span>\n' +
    '                        </h2>\n' +
    '                        <form class=\"form-inline\">\n' +
    '                                <button data-bind=\"disabled:!changed;onclick:on_save\" class=\"button btn btn-primary\" type=\"button\">\n' +
    '                                        Save\n' +
    '                                </button>\n' +
    '                        </form>\n' +
    '                </div>\n' +
    '        </slot>\n' +
    '        <p class=\"function_title\" data-bind=\"function-title;style-visibility:function_title_visibility\"></p>\n' +
    '        <div class=\"vseditor\" name=\"vseditor\" style=\"position:absolute;width:100%;\" data-bind=\"style-top:top;style-bottom:bottom\"></div>\n' +
    '</div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/vs";
stub1_context = (new DefineWebComponent(TAG, true, [], [BASE_PATH + "/editor/editor.main.css"]));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    comp.options["attributes"] = _pyfunc_create_dict("function-title", null, "title", null);
    init = function flx_init (component) {
        var _on_loadjs, function_title_visibility, on_save, state;
        _on_loadjs = (function flx__on_loadjs () {
            var _changed, _process_resize, ed, state, top, value;
            ed = component.root.querySelector("div.vseditor");
            if (_pyfunc_truthy(component.hasAttribute("value"))) {
                value = decodeURIComponent(escape(atob(component.getAttribute("value"))));
            } else {
                value = "";
            }
            component.editor = monaco.editor.create(ed, ({value: value, language: "python", theme: "vs-dark"}));
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
            component.set_state(state);
            component.editor.layout();
            _process_resize = (function flx__process_resize (size_object) {
                if ((!_pyfunc_truthy(component.hasAttribute("height")))) {
                    component.set_state(({height: (((size_object["h"] - size_object["body_offset_y"]) - 7) - ed.offsetTop) + "px"}));
                }
                component.editor.layout();
                return null;
            }).bind(this);

            component.process_resize = _process_resize;
            window.process_resize(component);
            return null;
        }).bind(this);

        require.config(({paths: ({vs: BASE_PATH})}));
        require(["vs/editor/editor.main"], _on_loadjs);
        on_save = (function flx_on_save (event) {
            var _on_ajax, ajax_options, href;
            if (_pyfunc_truthy(component.hasAttribute("href"))) {
                href = component.getAttribute("href");
                ajax_options = ({method: "POST", url: href, dataType: "html", data: ({data: component.editor.getValue()})});
                _on_ajax = (function flx__on_ajax () {
                    component.set_state(({changed: false}));
                    return null;
                }).bind(this);

                (jQuery.ajax(ajax_options).done)(_on_ajax);
            }
            return null;
        }).bind(this);

        if (_pyfunc_truthy((_pyfunc_truthy(component.hasAttribute("function-title"))) && (_pyfunc_truthy(component.getAttribute("function-title"))))) {
            function_title_visibility = "block";
        } else {
            function_title_visibility = "hidden";
        }
        state = ({on_save: on_save, changed: false, function_title_visibility: function_title_visibility});
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0; }
if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
} else { stub1_context.__exit__(null, null, null); }