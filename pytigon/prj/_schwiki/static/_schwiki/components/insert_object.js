var PARAM_INDENT, TAG, TEMPLATE, comp, get_current_line, get_editor, get_editor_component, init, is_special_line, join_parameters, set_current_line, stub4_context, stub5_err, trim_line, wiki_object_to_editor;
TAG = "insert-object";
TEMPLATE = '        <div name=\"insert_element\">\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
PARAM_INDENT = 120;
trim_line = function flx_trim_line (line) {
    var key, param, ret, stub1_seq, value, x;
    x = _pymeth_split.call(line, "#", 1);
    if ((x.length > 1)) {
        param = JSON.parse(x[1]);
        ret = ({});
        stub1_seq = param;
        for (key in stub1_seq) {
            if (!stub1_seq.hasOwnProperty(key)){ continue; }
            value = stub1_seq[key];
            if ((!(((_pyfunc_op_equals(jQuery.type(value), "string"))) && (value.length > 1024)))) {
                ret[key] = value;
            }
        }
        return (x[0] + "#") + (_pymeth_replace.call(JSON.stringify(ret), "\n", "\\n"));
    }
    return line;
};

join_parameters = function flx_join_parameters (param, line) {
    var key, old_param, param2, stub2_seq, stub3_itr, x;
    x = _pymeth_split.call(line, "#", 1);
    if ((x.length > 1)) {
        try {
            param2 = JSON.parse(param);
            old_param = JSON.parse(x[1]);
            stub2_seq = old_param;
            if ((typeof stub2_seq === "object") && (!Array.isArray(stub2_seq))) { stub2_seq = Object.keys(stub2_seq);}
            for (stub3_itr = 0; stub3_itr < stub2_seq.length; stub3_itr += 1) {
                key = stub2_seq[stub3_itr];
                if ((((!_pyfunc_op_contains(key, param2))) || _pyfunc_op_equals(param2[key], null))) {
                    param2[key] = old_param[key];
                }
            }
            return _pymeth_replace.call(JSON.stringify(param2), "\n", "\\n");
        } catch(err_3) {
            {
            }
        }
    }
    return param;
};

get_editor_component = function flx_get_editor_component (object) {
    return object.closest("ptig-codeeditor");
};

get_editor = function flx_get_editor (object) {
    var vc_component;
    vc_component = get_editor_component(object);
    return vc_component.editor;
};

is_special_line = function flx_is_special_line (line) {
    if ((_pyfunc_op_equals((_pymeth_strip.call(line).slice(0,1)), "%"))) {
        return true;
    } else {
        return false;
    }
    return null;
};

get_current_line = function flx_get_current_line (editor) {
    return (editor.getModel().getLineContent)(editor.getPosition().lineNumber);
};

set_current_line = function flx_set_current_line (editor, text, overwrite) {
    var current_line, id, line_number, op, range, text2;
    line_number = editor.getPosition().lineNumber;
    current_line = get_current_line(editor);
    if (_pyfunc_truthy(overwrite)) {
        range = new monaco.Range(line_number, 1, line_number, current_line.length + 1);
        text2 = text;
    } else {
        range = new monaco.Range(line_number, 1, line_number, 1);
        text2 = text + "\n";
    }
    id = ({major: 1, minor: 1});
    op = ({identifier: id, range: range, text: text2, forceMoveMarkers: true});
    editor.executeEdits("pytigon", [op]);
    if (_pyfunc_truthy(_pymeth_endswith.call(text, ":"))) {
        editor.setPosition(({lineNumber: line_number, column: text.length + 1}));
    } else {
        editor.setPosition(({lineNumber: line_number, column: 1}));
    }
    editor.focus();
    return null;
};

wiki_object_to_editor = function flx_wiki_object_to_editor (editor, object_name, is_inline_content, param) {
    var current_line, indent, line, overwrite, x;
    current_line = get_current_line(editor);
    if ((current_line.length >= (64 * 1024))) {
        param = join_parameters(param, current_line);
    }
    x = _pymeth_lstrip.call(current_line);
    if (((x.length == 0) || is_special_line(current_line))) {
        overwrite = true;
    } else {
        overwrite = false;
    }
    indent = current_line.length - x.length;
    line = (_pyfunc_op_mult(indent, " ") + "% ") + object_name;
    if (_pyfunc_truthy(is_inline_content)) {
        line += ":";
    }
    if (_pyfunc_truthy(param)) {
        if ((line.length < PARAM_INDENT)) {
            line = _pyfunc_op_add(line, _pyfunc_op_mult((PARAM_INDENT - line.length), " "));
        }
        line += "#";
        line = _pyfunc_op_add(line, param);
    }
    set_current_line(editor, line, overwrite);
    return null;
};

stub4_context = (new DefineWebComponent(TAG, true));
comp = stub4_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _init_OK, href, on_insert, on_properties, update_or_insert;
        href = component.getAttribute("href");
        _init_OK = (function flx__init_OK () {
            var button_OK, change, ed_component, modal_dialog, on_ok, save;
            ed_component = get_editor_component(component);
            save = ed_component.state["save"];
            change = ed_component.state["save"];
            on_ok = (function flx_on_ok (event) {
                var changed, div, on_saved;
                div = component.closest(".modal-content");
                div.style.opacity = "50%";
                on_saved = (function flx_on_saved () {
                    refresh_ajax_frame(div, "page", null, null, null);
                    return null;
                }).bind(this);

                changed = ed_component.state["changed"];
                if (_pyfunc_truthy(changed)) {
                    save(on_saved);
                } else {
                    on_saved();
                }
                return null;
            }).bind(this);

            modal_dialog = component.closest("div.modal-dialog");
            button_OK = modal_dialog.querySelector("div.modal-footer > button.btn-primary");
            button_OK.setAttribute("target", "none");
            button_OK.onclick = on_ok;
            return null;
        }).bind(this);

        setTimeout(_init_OK, 1);
        update_or_insert = (function flx_update_or_insert (event, insert) {
            var _complete, button, data, ed, ed_component, inline, line, object_name, show_form, spec, status;
            button = event.currentTarget;
            ed_component = get_editor_component(button);
            ed = ed_component.editor;
            if (_pyfunc_truthy(insert)) {
                object_name = button.getAttribute("name");
                show_form = false;
                if ((_pyfunc_op_equals(button.getAttribute("show_form"), "1"))) {
                    show_form = true;
                }
                inline = false;
                if ((_pyfunc_op_equals(button.getAttribute("inline"), "1"))) {
                    inline = true;
                }
                status = "new_object";
                line = null;
            } else {
                line = get_current_line(ed);
                spec = is_special_line(line);
                if (_pyfunc_truthy((_pyfunc_truthy(is_special_line(line))) && _pyfunc_op_contains("#", line))) {
                    object_name = _pymeth_strip.call(((_pymeth_strip.call(((_pymeth_split.call(line, "#")[0]))).slice(1))));
                    inline = false;
                    if (_pyfunc_truthy(_pymeth_endswith.call(object_name, ":"))) {
                        object_name = object_name.slice(0,-1);
                        inline = true;
                    }
                    show_form = true;
                    status = "edit_object";
                    if ((line.length >= (64 * 1024))) {
                        line = trim_line(line);
                    }
                } else {
                    return null;
                }
            }
            if (_pyfunc_op_equals(show_form, true)) {
                _complete = (function flx__complete (content) {
                    var on_loadeddata;
                    on_loadeddata = (function flx_on_loadeddata (event) {
                        var x;
                        console.log("on_loadeddata:" + " " + event.data);
                        x = JSON.parse(event.data);
                        if (_pyfunc_op_contains("line", x)) {
                            wiki_object_to_editor(ed, object_name, inline, x["line"]);
                        }
                        return null;
                    }).bind(this);

                    _pyfunc_setattr(component, "onloadeddata", on_loadeddata);
                    window.on_popup_edit_new(button, window.get_elem_from_string(content), href);
                    return null;
                }).bind(this);

                data = JSON.stringify(({status: status, line: line, object_name: object_name}));
                ajax_post(href, data, _complete, null);
            } else {
                wiki_object_to_editor(ed, object_name, inline, null);
            }
            return null;
        }).bind(this);

        on_insert = (function flx_on_insert (event) {
            update_or_insert(event, true);
            return null;
        }).bind(this);

        on_properties = (function flx_on_properties (event) {
            update_or_insert(event, false);
            return null;
        }).bind(this);

        component.set_state(({on_insert: on_insert, on_properties: on_properties}));
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub5_err=err_0; }
if (stub5_err) { if (!stub4_context.__exit__(stub5_err.name || "error", stub5_err, null)) { throw stub5_err; }
} else { stub4_context.__exit__(null, null, null); }
export {trim_line, join_parameters, get_editor_component, get_editor, is_special_line, get_current_line, set_current_line, wiki_object_to_editor};