var TAG, TEMPLATE, comp, get_current_line, get_editor, get_editor_component, handle_click, init, is_special_line, set_current_line, stub3_context, stub4_err;
TAG = "insert-object";
TEMPLATE = '        <div name=\"insert_element\">\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
get_editor_component = function flx_get_editor_component (object) {
    return object.closest("ptig-codeeditor");
};

get_editor = function flx_get_editor (object) {
    var vc_component;
    vc_component = get_editor_component(object);
    return vc_component.editor;
};

get_current_line = function flx_get_current_line (editor) {
    return (editor.getModel().getLineContent)(editor.getPosition().lineNumber);
};

set_current_line = function flx_set_current_line (editor, text) {
    var current_line, id, line_number, op, range;
    line_number = editor.getPosition().lineNumber;
    current_line = get_current_line(editor);
    range = new monaco.Range(line_number, 1, line_number, current_line.length + 1);
    id = ({major: 1, minor: 1});
    op = ({identifier: id, range: range, text: text, forceMoveMarkers: true});
    editor.executeEdits("pytigon", [op]);
    editor.setPosition(({lineNumber: line_number, column: 1}));
    editor.focus();
    return null;
};

is_special_line = function flx_is_special_line (line) {
    if ((_pyfunc_op_equals((_pymeth_strip.call(line).slice(0,1)), "%"))) {
        return true;
    } else {
        return false;
    }
    return null;
};

handle_click = function flx_handle_click (app_path, object, context) {
    var _on_get, ed, edit_form, href, id, l, line, max, n, op, pos, range, repeat, stub1_seq, stub2_itr, tab, text, x, xx;
    ed = get_editor();
    repeat = 2;
    while (repeat > 0) {
        pos = ed.getPosition();
        text = ed.getValue();
        tab = _pymeth_split.call(text, "\n");
        line = tab[pos.lineNumber - 1];
        if (_pymeth_startswith.call(line, "@")) {
            if (_pyfunc_op_equals(context["edit_form"], true)) {
                x = _pymeth_split.call(line, ":");
                href = (((app_path + "table/PageObjectsConf/action/edit_page_object/?name=") + (x[0].slice(1))) + "&page_id=") + _pyfunc_str(context["page_id"]);
                _on_get = (function flx__on_get (content) {
                    window.on_popup_edit_new(object, window.get_elem_from_string(content), href);
                    return null;
                }).bind(this);

                ajax_get(href, _on_get);
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
            if (_pyfunc_op_equals(context["edit_form"], true)) {
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
        var on_insert, on_properties, state;
        on_insert = (function flx_on_insert (event) {
            var _complete, button_name, data, ed, ed_component, href, line, spec;
            button_name = event.target.getAttribute("name");
            ed_component = get_editor_component(event.target);
            ed = ed_component.editor;
            line = get_current_line(ed);
            spec = is_special_line(line);
            set_current_line(ed, "$$$");
            if (_pyfunc_truthy(ed_component.hasAttribute("href"))) {
                href = ed_component.getAttribute("href");
                _complete = (function flx__complete (data_in) {
                    alert(data_in);
                    return null;
                }).bind(this);

                data = JSON.stringify(({line: line, status: "new_row"}));
                ajax_post(href, data, _complete, null);
            }
            return null;
        }).bind(this);

        on_properties = (function flx_on_properties (event) {
            return null;
        }).bind(this);

        state = ({on_insert: on_insert, on_properties: on_properties});
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub4_err=err_0; }
if (stub4_err) { if (!stub3_context.__exit__(stub4_err.name || "error", stub4_err, null)) { throw stub4_err; }
} else { stub3_context.__exit__(null, null, null); }
export {get_editor_component, get_editor, get_current_line, set_current_line, is_special_line, handle_click};