var TAG, TEMPLATE, comp, handle_click, init, stub3_context, stub4_err;
TAG = "insert-object";
TEMPLATE = '        <div name=\"insert_element\" class=\"col-5\">\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
handle_click = function flx_handle_click (app_path, object, context) {
    var ed, edit_form, href, id, l, line, max, n, op, pos, range, repeat, stub1_seq, stub2_itr, tab, text, vc_component, x, xx;
    vc_component = object.closest("ptig-codeeditor");
    ed = vc_component.editor;
    repeat = 2;
    while (repeat > 0) {
        pos = ed.getPosition();
        text = ed.getValue();
        tab = _pymeth_split.call(text, "\n");
        line = tab[pos.lineNumber - 1];
        if (_pymeth_startswith.call(line, "@")) {
            if (_pyfunc_op_equals(context["edit_form"], "True")) {
                x = _pymeth_split.call(line, ":");
                href = (((app_path + "/table/PageObjectsConf/action/edit_page_object/?name=") + (x[0].slice(1))) + "&page_id=") + _pyfunc_str(context["page_id"]);
                window.on_popup_edit_new(href, object[0], null);
            }
            repeat = 0;
        } else {
            if ((!_pyfunc_truthy(context["pk"]))) {
                alert("Select new wiki object type or point to existing element to edit proporties");
                break;
            }
            max = 0;
            stub1_seq = tab;
            if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
            for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
                l = stub1_seq[stub2_itr];
                if ((_pymeth_startswith.call(l, ("@" + context["object_name"])))) {
                    x = _pymeth_split.call(l, "_");
                    if ((x.length > 1)) {
                        xx = _pymeth_split.call(x[1], ":");
                        try {
                            n = _pyfunc_int(xx[0]);
                            if ((n > max)) {
                                max = n;
                            }
                        } catch(err_7) {
                            {
                            }
                        }
                    }
                }
            }
            range = new monaco.Range(pos.lineNumber, 1, pos.lineNumber, 1);
            id = ({major: 1, minor: 1});
            if (_pyfunc_op_equals(context["edit_form"], "True")) {
                edit_form = "_" + (_pyfunc_str((max + 1)));
            } else {
                edit_form = "";
            }
            text = ("@" + context["object_name"]) + edit_form;
            if (_pyfunc_truthy(context["object_inline_editing"])) {
                text += ":\n";
            } else {
                text += "\n";
            }
            op = ({identifier: id, range: range, text: text, forceMoveMarkers: true});
            ed.executeEdits("pytigon", [op]);
            ed.setPosition(pos);
            vc_component.state["on_save"](null);
            repeat -= 1;
        }
    }
    return null;
};

stub3_context = (new DefineWebComponent(TAG, true));
comp = stub3_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var button, on_click;
        button = component.querySelector("a.btn");
        button.style.height = "100%";
        on_click = (function flx_on_click () {
            var on_get;
            on_get = (function flx_on_get (content) {
                handle_click(component.getAttribute("app_path"), button, content);
                return null;
            }).bind(this);

            ajax_json(window.process_href(button.href, window.jQuery(button)), ({}), on_get);
            return false;
        }).bind(this);

        button.onclick = on_click;
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub4_err=err_0; }
if (stub4_err) { if (!stub3_context.__exit__(stub4_err.name || "error", stub4_err, null)) { throw stub4_err; }
} else { stub3_context.__exit__(null, null, null); }
export {handle_click};