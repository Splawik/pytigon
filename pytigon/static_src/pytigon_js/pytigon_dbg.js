

var DELETE_FOOTER, EDIT_FOOTER, ERROR_FOOTER, INFO_FOOTER, INLINE, INLINE_BASE, INLINE_DELETE, INLINE_DELETE_BASE, INLINE_EDIT, INLINE_ERROR, INLINE_INFO, MODAL, MODAL_BASE, MODAL_DELETE, MODAL_DELETE_BASE, MODAL_EDIT, MODAL_ERROR, MODAL_INFO;
MODAL = "\n    <div class=\"dialog-data\"></div>\n";
MODAL_BASE = "\n<div class=\"dialog-form modal\" role=\"dialog\" title=\"{title}\">\n    <div class=\"modal-dialog\" role=\"document\">\n        <div class=\"modal-content ajax-region\" data-region=\"error\">\n            <div class=\"modal-header\">\n                <h5 class=\"modal-title\" id=\"ModalLabel\">{title}</h5>\n                <button type=\"button\" class=\"close\" data-dismiss='modal' aria-label=\"Close\">\n                    <span aria-hidden=\"true\">&times;</span>\n                </button>\n            </div>\n            <div class=\"modal-body\">\n                <div class=\"container-fluid\">\n                    <div class=\"dialog-data ajax-frame\" data-region=\"error\"></div>\n                </div>\n            </div>\n            <div class=\"modal-footer\">\n                {{modal_footer}}\n            </div>\n        </div>\n    </div>\n</div>\n";
MODAL_DELETE_BASE = "\n<div class=\"dialog-form modal\" role=\"dialog\" title=\"{title}\">\n    <div class=\"modal-dialog\" role=\"document\">\n        <div class=\"modal-header\">\n            <h5 class=\"modal-title\" id=\"ModalLabel\">{title}</h5>\n            <button type=\"button\" class=\"close\" data-dismiss='modal' aria-label=\"Close\">\n                <span aria-hidden=\"true\">&times;</span>\n            </button>\n        </div>\n        <div class=\"modal-body\">\n            <div class=\"container-fluid\">\n                <div class=\"dialog-data ajax-frame\" data-region=\"error\"></div>\n            </div>\n        </div>\n        <div class=\"modal-footer\">\n            {{modal_footer}}\n        </div>\n    </div>\n</div>\n";
EDIT_FOOTER = " \n<button type=\"button\" class=\"btn btn-secondary btn-close\" data-dismiss='modal'>Cancel</button>\n<button type=\"button\" class=\"btn btn-primary\" target=\"refresh_frame\">OK</button>\n";
INFO_FOOTER = "\n<button type = \"button\" class =\"btn btn-secondary btn-close\" data-dismiss='modal'>Close</button>\n";
DELETE_FOOTER = "\n<button type=\"button\" class=\"btn btn-secondary btn-close\" data-dismiss='modal'>Cancel</button>\n<button type=\"button\" class=\"btn btn-danger\" target=\"refresh_frame\">OK</button>\n";
ERROR_FOOTER = "\n<button type=\"button\" class=\"btn btn-secondary btn-close\" data-dismiss='modal'>Close</button>\n";
MODAL_EDIT = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", EDIT_FOOTER);
MODAL_INFO = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", INFO_FOOTER);
MODAL_DELETE = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", DELETE_FOOTER);
MODAL_ERROR = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", ERROR_FOOTER);
INLINE = "\n    <div class=\"dialog-data\"></div>\n";
INLINE_BASE = "\n<div style='position:relative'>\n    <div class='dark_background'></div>\n    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>\n        <div class=\"modal-content ajax-region\" data-region=\"error\">\n            <div class='modal-content'>\n                <div class='modal-header'>\n                    <h4 class='modal-title'>{title}</h4>\n                    <button type='button' class='btn btn-outline-secondary minimize' onclick='popup_minimize(this)' style='diplay:none;'> \n                        <span class='fa fa-window-minimize'></span> \n                    </button> \n                    <button type='button' class='btn btn-outline-secondary maximize' onclick='popup_maximize(this);return false;'> \n                        <span class='fa fa-window-maximize'></span> \n                    </button> \n                    <button type='button' class='close btn-raised btn-close' aria-label='Close'><span aria-hidden='true'>&times;</span></button>\n                </div>\n                <div class='modal-body'>\n                    <div class='dialog-data'></div>\n                </div>\n                <div class='modal-footer'>\n                    {{modal_footer}}\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n";
INLINE_DELETE_BASE = "\n<div style='position:relative'>\n    <div class='dark_background'></div>\n    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>\n        <div class='modal-content'>\n            <div class='modal-header'>\n                <h4 class='modal-title'>{title}</h4>\n                <button type='button' class='btn btn-outline-secondary minimize' onclick='popup_minimize(this)' style='diplay:none;'> \n                    <span class='fa fa-window-minimize'></span> \n                </button> \n                <button type='button' class='btn btn-outline-secondary maximize' onclick='popup_maximize(this);return false;'> \n                    <span class='fa fa-window-maximize'></span> \n                </button> \n                <button type='button' class='close btn-raised btn-close' aria-label='Close'><span aria-hidden='true'>&times;</span></button>\n            </div>\n            <div class='modal-body'>\n                <div class='dialog-data'></div>\n            </div>\n            <div class='modal-footer'>\n                {{modal_footer}}\n            </div>\n        </div>\n    </div>\n</div>\n";
INLINE_EDIT = _pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", EDIT_FOOTER), "data-dismiss='modal'", "");
INLINE_INFO = _pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", INFO_FOOTER), "data-dismiss='modal'", "");
INLINE_DELETE = _pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", DELETE_FOOTER), "data-dismiss='modal'", "");
INLINE_ERROR = _pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", ERROR_FOOTER), "data-dismiss='modal'", "");

var LOADED_FILES, Loading, TEMPLATES, _OPERATOR, _req_post, ajax_get, ajax_json, ajax_post, ajax_submit, animate_combo, can_popup, corect_href, download_binary_file, get_elem_from_string, get_page, get_table_type, get_template, history_push_state, is_hidden, is_visible, load_css, load_js, load_many_js, on_load_js, process_resize, remove_element, remove_page_from_href, save_as, send_to_dom, super_insert, super_query_selector;
LOADED_FILES = ({});
Loading = function () {
    _pyfunc_op_instantiate(this, arguments);
}
Loading.prototype._base_class = Object;
Loading.prototype.__name__ = "Loading";

Loading.prototype.__init__ = function (element) {
    var loading_indicator;
    this.load_type = null;
    this.element = element;
    if (_pyfunc_truthy(element)) {
        if (_pyfunc_truthy(element.classList.contains("ladda-button"))) {
            this.load_type = "ladda";
            this.ladda = null;
        }
    }
    if ((!_pyfunc_truthy(this.load_type))) {
        loading_indicator = document.getElementById("loading-indicator");
        if (_pyfunc_truthy(loading_indicator)) {
            this.load_type = "global";
            this.loading_indicator = loading_indicator;
        }
    }
    return null;
};

Loading.prototype.create = function () {
    if (_pyfunc_op_equals(this.load_type, "ladda")) {
        this.ladda = window.Ladda.create(this.element);
    }
    return null;
};

Loading.prototype.start = function () {
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.start();
    } else if (_pyfunc_op_equals(this.load_type, "global")) {
        this.loading_indicator.style.display = "block";
    }
    return null;
};

Loading.prototype.set_progress = function (progress) {
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.setProgress(progress);
    }
    return null;
};

Loading.prototype.stop = function () {
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.stop();
    } else if (_pyfunc_op_equals(this.load_type, "global")) {
        this.loading_indicator.style.display = "none";
    }
    return null;
};

Loading.prototype.remove = function () {
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.remove();
        this.ladda = null;
    }
    return null;
};


save_as = function flx_save_as (blob, file_name) {
    var _, anchor_elem, url;
    url = window.URL.createObjectURL(blob);
    anchor_elem = document.createElement("a");
    anchor_elem.style = "display: none";
    anchor_elem.href = url;
    anchor_elem.download = file_name;
    document.body.appendChild(anchor_elem);
    anchor_elem.click();
    document.body.removeChild(anchor_elem);
    _ = (function flx__ () {
        window.URL.revokeObjectURL(url);
        return null;
    }).bind(this);

    setTimeout(_, 1000);
    return null;
};

download_binary_file = function flx_download_binary_file (buf, content_disposition) {
    var file_name, pos, stub1_seq, stub2_itr, var_list;
    file_name = "temp.dat";
    var_list = _pymeth_split.call(content_disposition, ";");
    stub1_seq = var_list;
    if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
    for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
        pos = stub1_seq[stub2_itr];
        if (_pyfunc_op_contains("filename", pos)) {
            file_name = _pymeth_split.call(pos, "=")[1];
            break;
        }
    }
    save_as(buf, file_name);
    return null;
};

ajax_get = function flx_ajax_get (url, complete, process_req) {
    var _onload, process_blob, req;
    process_req = (process_req === undefined) ? null: process_req;
    req = new XMLHttpRequest();
    if (_pyfunc_truthy(process_req)) {
        process_req(req);
    }
    process_blob = false;
    try {
        req.responseType = "blob";
        process_blob = true;
    } catch(err_2) {
        {
        }
    }
    _onload = (function flx__onload () {
        var _on_reader_load, disp, reader;
        if (_pyfunc_truthy(process_blob)) {
            disp = req.getResponseHeader("Content-Disposition");
            if ((_pyfunc_truthy(disp) && _pyfunc_op_contains("attachment", disp))) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                reader = new FileReader();
                _on_reader_load = (function flx__on_reader_load () {
                    if ((((!_pyfunc_op_equals(req.status, 200))) && ((!_pyfunc_op_equals(req.status, 0))))) {
                        console.log(reader.result);
                        (window.open().document.write)(reader.result);
                        complete("Error - details on new page");
                    } else {
                        complete(reader.result);
                    }
                    return null;
                }).bind(this);

                reader.onload = _on_reader_load;
                reader.readAsText(req.response);
            }
        } else if ((((!_pyfunc_op_equals(req.status, 200))) && ((!_pyfunc_op_equals(req.status, 0))))) {
            console.log(req.response);
            (window.open().document.write)(req.response);
            complete("Error - details on new page");
        } else {
            complete(req.response);
        }
        return null;
    }).bind(this);

    req.onload = _onload;
    req.open("GET", url, true);
    req.send(null);
    return null;
};

window.ajax_get = ajax_get;
_req_post = function flx__req_post (req, url, data, complete, content_type) {
    var _onload, process_blob;
    process_blob = false;
    try {
        req.responseType = "blob";
        process_blob = true;
    } catch(err_2) {
        {
        }
    }
    _onload = (function flx__onload (event) {
        var _on_reader_load, disp, reader;
        if (_pyfunc_truthy(process_blob)) {
            disp = req.getResponseHeader("Content-Disposition");
            if ((_pyfunc_truthy(disp) && _pyfunc_op_contains("attachment", disp))) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                reader = new FileReader();
                _on_reader_load = (function flx__on_reader_load () {
                    if ((((!_pyfunc_op_equals(req.status, 200))) && ((!_pyfunc_op_equals(req.status, 0))))) {
                        console.log(reader.result);
                        (window.open().document.write)(reader.result);
                        complete("Error - details on new page");
                    }
                    complete(reader.result);
                    return null;
                }).bind(this);

                reader.onload = _on_reader_load;
                reader.readAsText(req.response);
            }
        } else {
            if ((((!_pyfunc_op_equals(req.status, 200))) && ((!_pyfunc_op_equals(req.status, 0))))) {
                console.log(req.response);
                (window.open().document.write)(req.response);
                complete("Error - details on new page");
            }
            complete(req.response);
        }
        return null;
    }).bind(this);

    req.onload = _onload;
    req.open("POST", url, true);
    req.setRequestHeader("X-CSRFToken", _pymeth_get.call(Cookies, "csrftoken"));
    if (_pyfunc_truthy(content_type)) {
    } else {
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    }
    req.send(data);
    return null;
};

ajax_post = function flx_ajax_post (url, data, complete, process_req) {
    var req;
    process_req = (process_req === undefined) ? null: process_req;
    req = new XMLHttpRequest();
    if (_pyfunc_truthy(process_req)) {
        process_req(req);
    }
    _req_post(req, url, data, complete);
    return null;
};

window.ajax_post = ajax_post;
ajax_json = function flx_ajax_json (url, data, complete, process_req) {
    var _complete, data2;
    process_req = (process_req === undefined) ? null: process_req;
    _complete = (function flx__complete (data_in) {
        var _data;
        _data = JSON.parse(data_in);
        complete(_data);
        return null;
    }).bind(this);

    data2 = JSON.stringify(data);
    ajax_post(url, data2, _complete, process_req);
    return null;
};

window.ajax_json = ajax_json;
ajax_submit = function flx_ajax_submit (_form, complete, data_filter, process_req) {
    var _progressHandlingFunction, content_type, data, form, req;
    data_filter = (data_filter === undefined) ? null: data_filter;
    process_req = (process_req === undefined) ? null: process_req;
    content_type = null;
    req = new XMLHttpRequest();
    form = jQuery(_form);
    if (_pyfunc_truthy(process_req)) {
        process_req(req);
    }
    if (((_pymeth_find.call(form, "[type='file']").length) > 0)) {
        data = new FormData(form[0]);
        if (_pyfunc_truthy(data_filter)) {
            data = data_filter(data);
        }
        content_type = "multipart/form-data; boundary=...";
        if ((!(_pyfunc_op_equals((_pymeth_find.call(form, "#progress").length), 1)))) {
            _pymeth_append.call(_pymeth_find.call(form, "div.inline-form-body"), "<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>");
        } else {
            (jQuery("#progress").width)("0%");
        }
        _progressHandlingFunction = function (e) {
            if (_pyfunc_truthy(e.lengthComputable)) {
                (jQuery("#progress").width)(("" + (parseInt(_pyfunc_op_mult(100, e.loaded) / e.total))) + "%");
            }
            return null;
        };

        req.upload.addEventListener("progress", _progressHandlingFunction, false);
    } else {
        data = form.serialize();
        if (_pyfunc_truthy(data_filter)) {
            data = data_filter(data);
        }
    }
    _req_post(req, corect_href(form.attr("action")), data, complete, content_type);
    return null;
};

window.ajax_submit = ajax_submit;
load_css = function flx_load_css (path, on_load) {
    var _onload, req;
    on_load = (on_load === undefined) ? null: on_load;
    if ((!(_pyfunc_truthy(LOADED_FILES) && _pyfunc_op_contains(path, LOADED_FILES)))) {
        LOADED_FILES[path] = null;
        req = new XMLHttpRequest();
        _onload = (function flx__onload () {
            if (_pyfunc_truthy(on_load)) {
                on_load(req);
            } else {
                (((jQuery("<style type=\"text/css\"></style>").html)(req.responseText)).appendTo)("head");
            }
            return null;
        }).bind(this);

        req.onload = _onload;
        req.open("GET", path, true);
        req.send("");
    }
    return null;
};

window.load_css = load_css;
on_load_js = function flx_on_load_js (path) {
    var fun, functions, stub3_seq, stub4_itr;
    if ((_pyfunc_truthy(LOADED_FILES) && _pyfunc_op_contains(path, LOADED_FILES))) {
        functions = LOADED_FILES[path];
        if (_pyfunc_truthy(functions)) {
            stub3_seq = functions;
            if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
            for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                fun = stub3_seq[stub4_itr];
                fun();
            }
        }
        LOADED_FILES[path] = null;
    }
    return null;
};

load_js = function flx_load_js (path, fun) {
    var _onload, req;
    if ((_pyfunc_truthy(LOADED_FILES) && _pyfunc_op_contains(path, LOADED_FILES))) {
        if (_pyfunc_truthy(LOADED_FILES[path])) {
            (LOADED_FILES[path].push)(fun);
        } else {
            fun();
        }
    } else {
        LOADED_FILES[path] = [fun];
        req = new XMLHttpRequest();
        _onload = (function flx__onload () {
            var _define, _require, _requirejs, script;
            _requirejs = window.requirejs;
            _require = window.require;
            _define = window.define;
            window.requirejs = null;
            window.require = null;
            window.define = null;
            script = document.createElement("script");
            script.text = req.responseText;
            (document.head.appendChild(script).parentNode.removeChild)(script);
            window.requirejs = _requirejs;
            window.require = _require;
            window.define = _define;
            on_load_js(path);
            return null;
        }).bind(this);

        req.onload = _onload;
        req.open("GET", path, true);
        req.send("");
    }
    return null;
};

window.load_js = load_js;
load_many_js = function flx_load_many_js (paths, fun) {
    var _fun, counter, next_step, path, stub5_seq, stub6_itr;
    counter = 1;
    next_step = null;
    _fun = (function flx__fun () {
        counter = counter - 1;
        if (_pyfunc_op_equals(counter, 0)) {
            if ((!_pyfunc_op_equals(next_step, null))) {
                load_many_js(next_step, fun);
            } else {
                fun();
            }
        }
        return null;
    }).bind(this);

    stub5_seq = paths;
    if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
    for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
        path = stub5_seq[stub6_itr];
        if ((path.length > 0)) {
            if ((!_pyfunc_op_equals(next_step, null))) {
                _pymeth_append.call(next_step, path);
            } else if (_pyfunc_op_equals(path, "|")) {
                next_step = [];
            } else {
                counter = counter + 1;
                load_js(path, _fun);
            }
        }
    }
    _fun();
    return null;
};

window.load_many_js = load_many_js;
history_push_state = function flx_history_push_state (title, url, data) {
    var data2, url2;
    data = (data === undefined) ? null: data;
    url2 = _pymeth_split.call(url, "?")[0];
    if (_pyfunc_truthy(data)) {
        data2 = [LZString.compress(data[0]), data[1]];
    } else {
        data2 = title;
    }
    window.history.pushState(data2, title, url2);
    return null;
};

window.history_push_state = history_push_state;
get_elem_from_string = function flx_get_elem_from_string (html, selectors) {
    var element, temp;
    selectors = (selectors === undefined) ? null: selectors;
    temp = document.createElement("div");
    temp.innerHTML = html;
    if (_pyfunc_truthy(selectors)) {
        element = temp.querySelector(selectors);
        return element;
    } else {
        return temp;
    }
    return null;
};

window.get_elem_from_string = get_elem_from_string;
animate_combo = function flx_animate_combo (button, obj1, obj2, obj1_style_off, obj1_style_on, obj2_style_off, obj2_style_on, speed, end) {
    var _animate, end2;
    end = (end === undefined) ? null: end;
    if (_pyfunc_truthy(end)) {
        end2 = end;
    } else {
        end2 = (function flx_end2 () {
            return null;
        }).bind(this);

    }
    _animate = (function flx__animate () {
        if (_pyfunc_truthy(button.hasClass("on"))) {
            button.removeClass("on");
            obj1.animate(obj1_style_off, speed);
            obj2.animate(obj2_style_off, speed, "swing", end2);
        } else {
            button.addClass("on");
            obj1.animate(obj1_style_on, speed);
            obj2.animate(obj2_style_on, speed, "swing", end2);
        }
        return null;
    }).bind(this);

    button.click(_animate);
    return null;
};

window.animate_combo = animate_combo;
window.icons = ({time: "fa fa-clock-o", date: "fa fa-calendar", up: "fa fa-chevron-up", down: "fa fa-chevron-down", previous: "fa fa-chevron-left", next: "fa fa-chevron-right", today: "fa fa-calendar-check-o", clear: "fa fa-trash", close: "fa fa-times", paginationSwitchDown: "fa-chevron-down", paginationSwitchUp: "fa-chevron-up", refresh: "fa-refresh", toggle: "fa-list-alt", columns: "fa-th", detailOpen: "fa-plus", detailClose: "fa-minus"});
is_hidden = function flx_is_hidden (el) {
    var style;
    style = window.getComputedStyle(el);
    return _pyfunc_op_equals(style.display, "none");
};

window.is_hidden = is_hidden;
is_visible = function flx_is_visible (el) {
    return !_pyfunc_truthy(is_hidden(el));
};

window.is_visible = is_visible;
TEMPLATES = ({MODAL_EDIT: MODAL_EDIT, MODAL_INFO: MODAL_INFO, MODAL_DELETE: MODAL_DELETE, MODAL_ERROR: MODAL_ERROR, INLINE_EDIT: INLINE_EDIT, INLINE_INFO: INLINE_INFO, INLINE_DELETE: INLINE_DELETE, INLINE_ERROR: INLINE_ERROR});
get_template = function flx_get_template (template_name, param) {
    if (_pyfunc_op_contains(template_name, TEMPLATES)) {
        return _pymeth_format.call(TEMPLATES[template_name], param);
    }
    return null;
};

super_query_selector = function flx_super_query_selector (element, selector) {
    var e, pos, stub7_seq, stub8_itr, x;
    x = _pymeth_split.call(selector, "/");
    e = element;
    stub7_seq = x;
    if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
    for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
        pos = stub7_seq[stub8_itr];
        if (_pyfunc_op_equals(pos, "..")) {
            e = e.parentElement;
        } else if (_pyfunc_op_equals(pos, ".")) {
        } else if (_pymeth_startswith.call(pos, "^")) {
            e = e.closest(pos.slice(1));
        } else {
            e = e.querySelector(pos);
        }
        if ((!_pyfunc_truthy(e))) {
            return null;
        }
    }
    return e;
};

window.super_query_selector = super_query_selector;
super_insert = function flx_super_insert (base_element, insert_selector, inserted_element) {
    var c, element, selector2, stub10_itr, stub9_seq, x;
    if ((_pyfunc_truthy(insert_selector) && _pyfunc_op_contains(":", insert_selector))) {
        x = _pymeth_split.call(insert_selector, ":");
        if (_pyfunc_truthy(x[0])) {
            element = super_query_selector(base_element, x[0]);
        } else {
            element = base_element;
        }
        selector2 = x[1];
    } else {
        if (_pyfunc_truthy(insert_selector)) {
            element = super_query_selector(base_element, insert_selector);
        } else {
            element = base_element;
        }
        selector2 = null;
    }
    if ((!_pyfunc_truthy(element))) {
        return null;
    }
    if (_pyfunc_op_contains(selector2, ["overwrite", ">"])) {
        element.innerHTML = "";
        element.appendChild(inserted_element);
    } else if (_pyfunc_op_contains(selector2, ["append_first", "<<"])) {
        element.insertBefore(inserted_element, element.firstChild);
    } else if (_pyfunc_op_contains(selector2, ["append", ">>"])) {
        element.appendChild(inserted_element);
    } else if ((_pyfunc_op_contains(selector2, ["after", ")"]))) {
        element.parentElement.insertBefore(inserted_element, element.nextSibling);
    } else if (_pyfunc_op_contains(selector2, ["before", "("])) {
        element.parentElement.insertBefore(inserted_element, element);
    } else if (_pyfunc_op_equals(selector2, "class")) {
        stub9_seq = inserted_element.classList;
        if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
        for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
            c = stub9_seq[stub10_itr];
            element.classList.add(c);
        }
    } else if (_pyfunc_hasattr(element, selector2)) {
        _pyfunc_getattr(element, selector2)(inserted_element);
    } else {
        element.appendChild(inserted_element);
    }
    return element;
};

window.super_insert = super_insert;
_OPERATOR = [">>", "<<", ">", "(", ")"];
send_to_dom = function flx_send_to_dom (html_text, base_elem) {
    var html, insert_selector, inserted_element, operator, stub11_seq, stub12_itr, x;
    stub11_seq = _OPERATOR;
    if ((typeof stub11_seq === "object") && (!Array.isArray(stub11_seq))) { stub11_seq = Object.keys(stub11_seq);}
    for (stub12_itr = 0; stub12_itr < stub11_seq.length; stub12_itr += 1) {
        operator = stub11_seq[stub12_itr];
        if ((_pyfunc_op_contains(("===" + operator), html_text))) {
            x = _pymeth_split.call(html_text, ("===" + operator));
            html = x[0];
            insert_selector = (x[1] + ":") + operator;
            inserted_element = get_elem_from_string(html, null);
            return super_insert(base_elem, insert_selector, inserted_element);
        }
    }
    return null;
};

window.send_to_dom = send_to_dom;
remove_element = function flx_remove_element (element) {
    var _on_remove, _on_remove_aside, element2, elements, stub13_seq, stub14_itr;
    if (_pyfunc_truthy(element)) {
        _on_remove = (function flx__on_remove (index, value) {
            value.on_remove();
            return null;
        }).bind(this);

        if ((Object.prototype.toString.call(element).slice(8,-1).toLowerCase() === 'string')) {
            elements = Array.prototype.slice.call(document.querySelectorAll(element));
        } else {
            elements = [element];
        }
        stub13_seq = elements;
        if ((typeof stub13_seq === "object") && (!Array.isArray(stub13_seq))) { stub13_seq = Object.keys(stub13_seq);}
        for (stub14_itr = 0; stub14_itr < stub13_seq.length; stub14_itr += 1) {
            element2 = stub13_seq[stub14_itr];
            jQuery.each(_pymeth_find.call(jQuery(element2), ".call_on_remove"), _on_remove);
            _on_remove_aside = (function flx__on_remove_aside (index, value) {
                var dialog;
                dialog = value.firstElementChild;
                if ((_pyfunc_truthy(dialog) && (_pyfunc_truthy(dialog.hasAttribute("modal"))))) {
                    (jQuery(dialog).modal)("hide");
                } else {
                    aside.remove();
                }
                return null;
            }).bind(this);

            jQuery.each(_pymeth_find.call(jQuery(element2), ".plug"), _on_remove_aside);
            element2.remove();
        }
    }
    return null;
};

window.remove_element = remove_element;
process_resize = function flx_process_resize (target_element) {
    var body_rect, elem, elem_rect, elements, elements1, elements2, elements3, h, param, parent_rect, size_desc, size_style, stub15_seq, stub16_itr, stub17_seq, stub18_itr;
    param = ({});
    param["w"] = window.innerWidth;
    param["h"] = window.innerHeight;
    body_rect = document.body.getBoundingClientRect();
    elements1 = Array.prototype.slice.call(target_element.querySelectorAll(".flexible_size"));
    elements2 = Array.prototype.slice.call(target_element.querySelectorAll(".flexible_size_round2"));
    elements3 = [];
    if (_pyfunc_truthy((_pyfunc_truthy(target_element.classList.contains("flexible_size"))) || target_element.classList.contains("flexible_size_round2"))) {
        _pymeth_append.call(elements3, target_element);
    }
    stub17_seq = [elements1, elements2, elements3];
    if ((typeof stub17_seq === "object") && (!Array.isArray(stub17_seq))) { stub17_seq = Object.keys(stub17_seq);}
    for (stub18_itr = 0; stub18_itr < stub17_seq.length; stub18_itr += 1) {
        elements = stub17_seq[stub18_itr];
        stub15_seq = elements;
        if ((typeof stub15_seq === "object") && (!Array.isArray(stub15_seq))) { stub15_seq = Object.keys(stub15_seq);}
        for (stub16_itr = 0; stub16_itr < stub15_seq.length; stub16_itr += 1) {
            elem = stub15_seq[stub16_itr];
            elem_rect = elem.getBoundingClientRect();
            if (_pyfunc_truthy(elem.parentElement)) {
                parent_rect = elem.getBoundingClientRect();
                param["parent_offset_x"] = elem_rect.top - parent_rect.top;
                param["parent_offset_y"] = elem_rect.left - parent_rect.left;
            } else {
                param["parent_offset_y"] = 0;
                param["parent_offset_x"] = 0;
            }
            param["body_offset_y"] = elem_rect.top - body_rect.top;
            param["body_offset_x"] = elem_rect.left - body_rect.left;
            if (_pyfunc_hasattr(elem, "process_resize")) {
                elem.process_resize(param);
            } else {
                size_desc = elem.hasAttribute("data-size");
                if (_pyfunc_truthy(size_desc)) {
                    size_style = _pymeth_format.call(size_desc, param);
                    elem.style.cssText = size_style;
                } else {
                    h = ((param["h"] - param["body_offset_y"]) - 5) + "px";
                    elem.style.height = h;
                    elem.setAttribute("height", h);
                }
            }
        }
    }
    return null;
};

window.process_resize = process_resize;
get_page = function flx_get_page (elem) {
    if (_pyfunc_truthy(elem.hasClass(".tab-pane"))) {
        return elem;
    } else {
        return elem.closest(".tab-pane");
    }
    return null;
};

get_table_type = function flx_get_table_type (elem) {
    var ret, tabsort;
    tabsort = _pymeth_find.call(elem, ".tabsort");
    if ((tabsort.length == 0)) {
        tabsort = _pymeth_find.call(get_page(elem), ".tabsort");
    }
    if ((tabsort.length > 0)) {
        ret = tabsort.attr("table_type");
        if (_pyfunc_truthy(ret)) {
            return ret;
        }
    }
    return "";
};

can_popup = function flx_can_popup () {
    if (((jQuery(".modal-open").length) > 0)) {
        return false;
    } else {
        return true;
    }
    return null;
};

corect_href = function flx_corect_href (href, only_table) {
    only_table = (only_table === undefined) ? false: only_table;
    if ((!_pyfunc_truthy(href))) {
        return href;
    }
    if (_pyfunc_truthy(only_table)) {
        if (_pyfunc_op_contains("only_table", href)) {
            return href;
        }
    } else if (_pyfunc_op_contains("only_content", href)) {
        return href;
    }
    if (_pyfunc_truthy(only_table)) {
        if (_pyfunc_op_contains("?", href)) {
            return href + "&only_table=1";
        } else {
            return href + "?only_table=1";
        }
    } else if (_pyfunc_op_contains("?", href)) {
        return href + "&only_content=1";
    } else {
        return href + "?only_content=1";
    }
    return null;
};

remove_page_from_href = function flx_remove_page_from_href (href) {
    var pos, stub19_seq, stub20_itr, x, x2, x3;
    x = _pymeth_split.call(href, "?");
    if ((x.length > 1)) {
        x2 = _pymeth_split.call(x[1], "&");
        if ((x2.length > 1)) {
            x3 = [];
            stub19_seq = x2;
            if ((typeof stub19_seq === "object") && (!Array.isArray(stub19_seq))) { stub19_seq = Object.keys(stub19_seq);}
            for (stub20_itr = 0; stub20_itr < stub19_seq.length; stub20_itr += 1) {
                pos = stub19_seq[stub20_itr];
                if ((!_pyfunc_op_contains("page=", pos))) {
                    _pymeth_append.call(x3, pos);
                }
            }
            return (x[0] + "?") + _pymeth_join.call("", x3);
        } else if (_pyfunc_op_contains("page=", x2[0])) {
            return x2;
        } else {
            return href;
        }
    }
    return href;
};

export {Loading, save_as, download_binary_file, ajax_get, ajax_post, ajax_json, ajax_submit, load_css, on_load_js, load_js, load_many_js, history_push_state, get_elem_from_string, animate_combo, is_hidden, is_visible, get_template, super_query_selector, super_insert, send_to_dom, remove_element, process_resize, get_page, get_table_type, can_popup, corect_href, remove_page_from_href};

var DefineWebComponent, GlobalBus, set_state;
set_state = function flx_set_state (component, state) {
    var c, cls, data_selector, element_selector, key, mod_fun, node, nodes, old_value, spec, state_actions, stub1_seq, stub2_itr, stub3_seq, stub4_itr, stub5_seq, stub6_itr, stub7_seq, stub8_itr, value, value2, x, x2, xx;
    spec = ["!", "?", "*", "0", "+", "-", "%"];
    if (_pyfunc_truthy(component.options.hasOwnProperty("state_actions"))) {
        state_actions = component.options["state_actions"];
    } else {
        state_actions = [];
    }
    stub7_seq = Object.keys(state);
    if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
    for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
        key = stub7_seq[stub8_itr];
        value = state[key];
        if ((!_pyfunc_op_equals(component.root, null))) {
            stub5_seq = [component.root, component];
            if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
            for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
                c = stub5_seq[stub6_itr];
                nodes = Array.prototype.slice.call(c.querySelectorAll((("[data-bind*=\"") + key) + ("\"]")));
                stub3_seq = nodes;
                if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                    node = stub3_seq[stub4_itr];
                    xx = node.getAttribute("data-bind");
                    stub1_seq = _pymeth_split.call(xx, ";");
                    if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
                    for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
                        x = stub1_seq[stub2_itr];
                        if ((!_pyfunc_truthy(_pymeth_endswith.call(_pymeth_lower.call(x), _pymeth_lower.call(key))))) {
                            continue;
                        }
                        mod_fun = null;
                        if (_pyfunc_op_contains(":", x)) {
                            x2 = _pymeth_split.call(x, ":", 1);
                            element_selector = x2[0];
                            data_selector = x2[1];
                            if (_pyfunc_op_contains(data_selector[0], spec)) {
                                mod_fun = data_selector[0];
                                data_selector = data_selector.slice(1);
                            }
                            if ((!_pyfunc_truthy(element_selector))) {
                                element_selector = data_selector;
                            }
                        } else {
                            element_selector = "";
                            data_selector = x;
                            if (_pyfunc_op_contains(data_selector[0], spec)) {
                                mod_fun = data_selector[0];
                                data_selector = data_selector.slice(1);
                            }
                        }
                        value2 = value;
                        if (_pyfunc_truthy(mod_fun)) {
                            if (_pyfunc_op_equals(mod_fun, "!")) {
                                value2 = !_pyfunc_truthy(value);
                            } else if (_pyfunc_op_equals(mod_fun, "?")) {
                                if (_pyfunc_truthy(value)) {
                                    value2 = true;
                                } else {
                                    value2 = false;
                                }
                            } else if (_pyfunc_op_equals(mod_fun, "*")) {
                                value2 = _pyfunc_str(value);
                            } else if (_pyfunc_op_equals(mod_fun, "+")) {
                                value2 = _pyfunc_float(value);
                            } else if (_pyfunc_op_equals(mod_fun, "-")) {
                                value2 = _pyfunc_op_mult((-1), _pyfunc_float(value));
                            } else if (_pyfunc_op_equals(mod_fun, "%")) {
                                value2 = _pyfunc_float(value) / 100;
                            }
                        }
                        if (_pyfunc_truthy(element_selector)) {
                            if (_pymeth_startswith.call(element_selector, "style-")) {
                                node.style[element_selector.slice(6)] = value2;
                            } else if (_pymeth_startswith.call(element_selector, "attr-")) {
                                old_value = node.getAttribute(element_selector.slice(5), "");
                                node.setAttribute(element_selector.slice(5), value2);
                            } else if (_pymeth_startswith.call(element_selector, "class-")) {
                                cls = element_selector.slice(6);
                                if (_pyfunc_truthy(value2)) {
                                    node.classList.add(cls);
                                } else {
                                    _pymeth_remove.call(node.classList, cls);
                                }
                            } else {
                                node[element_selector] = value2;
                            }
                        } else {
                            node.innerHTML = value2;
                        }
                    }
                }
            }
        }
        if (_pyfunc_op_contains(key, state_actions)) {
            if (_pyfunc_op_contains(key, component.state)) {
                state_actions[key](component, component.state[key], value);
            } else {
                state_actions[key](component, null, value);
            }
        }
        component.state[key] = value;
    }
    return null;
};

DefineWebComponent = function () {
    _pyfunc_op_instantiate(this, arguments);
}
DefineWebComponent.prototype._base_class = Object;
DefineWebComponent.prototype.__name__ = "DefineWebComponent";

DefineWebComponent.prototype.__init__ = function (tag, shadow, js, css) {
    shadow = (shadow === undefined) ? false: shadow;
    js = (js === undefined) ? null: js;
    css = (css === undefined) ? null: css;
    this.tag = tag;
    this.shadow = shadow;
    this.options = ({});
    this.js = js;
    this.css = css;
    return null;
};

DefineWebComponent.prototype.make_component = function () {
    var _component, _init, css, init, stub10_itr, stub9_seq;
    if ((_pyfunc_truthy(this.js) && (_pyfunc_truthy(this.options.hasOwnProperty("init"))))) {
        init = this.options["init"];
        _component = this;
        _init = (function flx__init (component) {
            var _on_loadjs;
            _on_loadjs = (function flx__on_loadjs () {
                init(component);
                return null;
            }).bind(this);

            load_many_js(_component.js, _on_loadjs);
            return null;
        }).bind(this);

        this.options["init"] = _init;
    }
    if (_pyfunc_truthy(this.css)) {
        stub9_seq = this.css;
        if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
        for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
            css = stub9_seq[stub10_itr];
            if (_pyfunc_truthy(this.shadow)) {
                if (_pyfunc_truthy(this.options.hasOwnProperty("template"))) {
                    this.options["template"] = ((("<style>@import \"") + css) + ("\"</style>\n")) + this.options["template"];
                } else {
                    this.options["template"] = (("<style>@import \"") + css) + ("\"</style>\n");
                }
            } else {
                load_css(css);
            }
        }
    }
    if ((!_pyfunc_truthy(this.options.hasOwnProperty("set_state")))) {
        this.options["set_state"] = set_state;
    }
    define_custom_element(this.tag, this.shadow, this.options);
    return null;
};

DefineWebComponent.prototype.fun = function (name) {
    var decorator;
    decorator = (function flx_decorator (funct) {
        self.options[name] = funct;
        return funct;
    }).bind(this);

    return decorator;
};

DefineWebComponent.prototype.__enter__ = function () {
    return this;
};

DefineWebComponent.prototype.__exit__ = function (type, value, traceback) {
    this.make_component();
    return null;
};


window.DefineWebComponent = DefineWebComponent;
GlobalBus = function () {
    _pyfunc_op_instantiate(this, arguments);
}
GlobalBus.prototype._base_class = Object;
GlobalBus.prototype.__name__ = "GlobalBus";

GlobalBus.prototype.__init__ = function () {
    this.components = [];
    this.state = ({});
    return null;
};

GlobalBus.prototype.set_state = function (state) {
    var key, state2, stub11_seq, value;
    if (_pyfunc_truthy(state)) {
        state2 = _pyfunc_dict(state);
        stub11_seq = state2;
        for (key in stub11_seq) {
            if (!stub11_seq.hasOwnProperty(key)){ continue; }
            value = stub11_seq[key];
            if ((!(_pyfunc_op_contains(key, this.state) && ((!_pyfunc_op_equals(this.state[key], value)))))) {
                this.state[key] = value;
                this.emit(key, value);
            }
        }
    }
    return null;
};

GlobalBus.prototype.emit = function (name, value) {
    var component, stub12_seq, stub13_itr;
    stub12_seq = this.components;
    if ((typeof stub12_seq === "object") && (!Array.isArray(stub12_seq))) { stub12_seq = Object.keys(stub12_seq);}
    for (stub13_itr = 0; stub13_itr < stub12_seq.length; stub13_itr += 1) {
        component = stub12_seq[stub13_itr];
        if (_pyfunc_truthy(component)) {
            if (_pyfunc_hasattr(component, "set_external_state")) {
                component.set_external_state(_pyfunc_create_dict(name, value));
            }
        }
    }
    return null;
};

GlobalBus.prototype.register = function (component) {
    var key, stub14_seq, value;
    if ((!_pyfunc_op_contains(component, this.components))) {
        _pymeth_append.call(this.components, component);
        stub14_seq = this.state;
        for (key in stub14_seq) {
            if (!stub14_seq.hasOwnProperty(key)){ continue; }
            value = stub14_seq[key];
            this.emit(key, value);
        }
    }
    return null;
};

GlobalBus.prototype.unregister = function (component) {
    if (_pyfunc_op_contains(component, this.components)) {
        _pymeth_remove.call(this.components, component);
    }
    return null;
};


window.GlobalBus = GlobalBus;
export {set_state, DefineWebComponent, GlobalBus};

var MOUNT_INIT_FUN, ajax_load, data_type, datatable_init, datetime_init, get_ajax_frame, get_ajax_link, get_ajax_region, label_floating_init, mount_html, moveelement_init, refresh_ajax_frame, register_mount_fun, select2_init, selectpicker_init;
data_type = function flx_data_type (data_or_html) {
    var meta_list, pos, stub1_seq, stub2_itr;
    if (_pyfunc_truthy(data_or_html)) {
        if ((Object.prototype.toString.call(data_or_html).slice(8,-1).toLowerCase() === 'string')) {
            if (_pyfunc_op_contains("$$RETURN_OK", data_or_html)) {
                return "$$RETURN_OK";
            } else if (_pyfunc_op_contains("$$RETURN_NEW_ROW_OK", data_or_html)) {
                return "$$RETURN_NEW_ROW_OK";
            } else if (_pyfunc_op_contains("$$RETURN_UPDATE_ROW_OK", data_or_html)) {
                return "$$RETURN_UPDATE_ROW_OK";
            } else if (_pyfunc_op_contains("$$RETURN_REFRESH_PARENT", data_or_html)) {
                return "$$RETURN_REFRESH_PARENT";
            } else if (_pyfunc_op_contains("$$RETURN_REFRESH", data_or_html)) {
                return "$$RETURN_REFRESH";
            } else if (_pyfunc_op_contains("$$RETURN_CANCEL", data_or_html)) {
                return "$$RETURN_CANCEL";
            } else if (_pyfunc_op_contains("$$RETURN_RELOAD", data_or_html)) {
                return "$$RETURN_RELOAD";
            } else if (_pyfunc_op_contains("$$RETURN_ERROR", data_or_html)) {
                return "$$RETURN_ERROR";
            }
        } else {
            meta_list = Array.prototype.slice.call(data_or_html.querySelectorAll("meta"));
            stub1_seq = meta_list;
            if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
            for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
                pos = stub1_seq[stub2_itr];
                if (_pyfunc_truthy(pos.hasAttribute("name"))) {
                    if ((_pyfunc_op_equals((_pymeth_upper.call(pos.getAttribute("name"))), "RETURN"))) {
                        if (_pyfunc_truthy(pos.hasAttribute("content"))) {
                            return _pymeth_upper.call(pos.getAttribute("content"));
                        }
                    }
                }
            }
        }
    }
    return "$$RETURN_HTML";
};

MOUNT_INIT_FUN = [];
register_mount_fun = function flx_register_mount_fun (fun) {
    _pymeth_append.call(MOUNT_INIT_FUN, fun);
    return null;
};

window.register_mount_fun = register_mount_fun;
mount_html = function flx_mount_html (dest_elem, data_or_html, link) {
    var _on_remove, evt, fun, stub3_seq, stub4_itr;
    link = (link === undefined) ? null: link;
    if (_pyfunc_truthy((_pyfunc_truthy(_pyfunc_getattr(dest_elem, "onloadeddata"))) && _pyfunc_truthy(dest_elem.onloadeddata))) {
        evt = document.createEvent("HTMLEvents");
        evt.initEvent("loadeddata", false, true);
        evt.data = data_or_html;
        evt.data_source = link;
        dest_elem.dispatchEvent(evt);
        return null;
    }
    if ((!_pyfunc_op_equals(data_or_html, null))) {
        _on_remove = (function flx__on_remove (index, value) {
            value.on_remove();
            return null;
        }).bind(this);

        jQuery.each(_pymeth_find.call(jQuery(dest_elem), ".call_on_remove"), _on_remove);
        if ((Object.prototype.toString.call(data_or_html).slice(8,-1).toLowerCase() === 'string')) {
            dest_elem.innerHTML = data_or_html;
        } else {
            dest_elem.innerHTML = "";
            dest_elem.appendChild(data_or_html);
        }
    }
    if (_pyfunc_truthy(MOUNT_INIT_FUN)) {
        stub3_seq = MOUNT_INIT_FUN;
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            fun = stub3_seq[stub4_itr];
            fun(dest_elem);
        }
    }
    return null;
};

window.mount_html = mount_html;
datetime_init = function flx_datetime_init (dest_elem) {
    var d, format;
    format = ({singleDatePicker: true, showDropdowns: true, buttonClasses: "btn", applyClass: "btn-success align-top", cancelClass: "btn-danger btn-sm align-top", timePicker24Hour: true, autoApply: true, locale: ({format: "YYYY-MM-DD", separator: "-", applyLabel: "&nbsp; OK &nbsp;", cancelLabel: "<i class='fa fa-close'></i>"})});
    d = _pymeth_find.call(jQuery(dest_elem), "div.form-group .datefield input");
    d.daterangepicker(format);
    format["locale"]["format"] = "YYYY-MM-DD HH:mm";
    format["timePicker"] = true;
    format["timePickerIncrement"] = 30;
    d = _pymeth_find.call(jQuery(dest_elem), "div.form-group .datetimefield input");
    d.daterangepicker(format);
    return null;
};

register_mount_fun(datetime_init);
selectpicker_init = function flx_selectpicker_init (dest_elem) {
    ((_pymeth_find.call(jQuery(dest_elem), ".selectpicker")).selectpicker)();
    return null;
};

register_mount_fun(selectpicker_init);
moveelement_init = function flx_moveelement_init (dest_elem) {
    var _on_remove, data_position, elem2, obj, objs, parent, stub7_seq, stub8_itr;
    objs = Array.prototype.slice.call(dest_elem.querySelectorAll(".move-element"));
    if (_pyfunc_truthy(objs)) {
        stub7_seq = objs;
        if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
        for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
            obj = stub7_seq[stub8_itr];
            if (_pyfunc_truthy(obj.hasAttribute("data-position"))) {
                _pymeth_remove.call(obj.classList, "move-element");
                data_position = obj.getAttribute("data-position");
                parent = obj.parentElement;
                elem2 = super_insert(dest_elem, obj.getAttribute("data-position"), obj);
                if (_pyfunc_truthy(_pymeth_endswith.call(data_position, ":class"))) {
                    _on_remove = (function flx__on_remove () {
                        var c, stub5_seq, stub6_itr;
                        stub5_seq = obj.classList;
                        if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
                        for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
                            c = stub5_seq[stub6_itr];
                            _pymeth_remove.call(elem2.classList, c);
                        }
                        return null;
                    }).bind(this);

                } else {
                    _on_remove = (function flx__on_remove () {
                        obj.remove();
                        return null;
                    }).bind(this);

                }
                parent.on_remove = _on_remove;
                parent.classList.add("call_on_remove");
            }
        }
    }
    return null;
};

register_mount_fun(moveelement_init);
label_floating_init = function flx_label_floating_init (dest_elem) {
    var _on_blur;
    _on_blur = function (e) {
        var test;
        if ((_pyfunc_op_equals(e["type"], "focus") || (this.value.length > 0))) {
            test = true;
        } else {
            test = false;
        }
        (((jQuery(this).parents)(".form-group")).toggleClass)("focused", test);
        return null;
    };

    ((((_pymeth_find.call(jQuery(dest_elem), ".label-floating .form-control")).on)("focus blur", _on_blur)).trigger)("blur");
    return null;
};

register_mount_fun(label_floating_init);
select2_init = function flx_select2_init (dest_elem) {
    var _onloadeddata, control, controls, init_select2_ctrl, set_select2_value, stub10_itr, stub9_seq;
    ((_pymeth_find.call(jQuery(dest_elem), ".django-select2:not(.select2-full-width)")).djangoSelect2)(({width: "calc(100% - 48px)", minimumInputLength: 1}));
    ((_pymeth_find.call(jQuery(dest_elem), ".django-select2.select2-full-width")).djangoSelect2)(({width: "calc(100%)", minimumInputLength: 1}));
    set_select2_value = (function flx_set_select2_value (sel2, id, text) {
        _pymeth_append.call(sel2, (jQuery("<option>", ({value: id, text: text}))));
        sel2.val(id.toString());
        sel2.trigger("change");
        return null;
    }).bind(this);

    controls = Array.prototype.slice.call(dest_elem.querySelectorAll(".django-select2"));
    if (_pyfunc_truthy(controls)) {
        stub9_seq = controls;
        if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
        for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
            control = stub9_seq[stub10_itr];
            _onloadeddata = function (event) {
                var id, src_elem, text;
                if (_pyfunc_hasattr(event, "data_source")) {
                    src_elem = event.data_source;
                    if (_pyfunc_truthy(src_elem)) {
                        id = src_elem.getAttribute("data-id");
                        text = src_elem.getAttribute("data-text");
                        set_select2_value(jQuery(control), id, text);
                    }
                }
                return null;
            };

            control.onloadeddata = _onloadeddata;
            control.classList.add("ajax-frame");
            control.setAttribute("data-region", "get_row");
        }
    }
    init_select2_ctrl = (function flx_init_select2_ctrl () {
        var id, sel2, src, text;
        sel2 = jQuery(this);
        src = sel2.closest(".input-group");
        if ((src.length == 1)) {
            if (_pyfunc_truthy((src[0].hasAttribute)("item_id"))) {
                id = src.attr("item_id");
                if (_pyfunc_truthy(id)) {
                    text = src.attr("item_str");
                    set_select2_value(sel2, id, text);
                }
            }
        }
        return null;
    }).bind(this);

    ((_pymeth_find.call(jQuery(dest_elem), ".django-select2")).each)(init_select2_ctrl);
    return null;
};

register_mount_fun(select2_init);
datatable_init = function flx_datatable_init (dest_elem) {
    var table_type, tbl;
    table_type = get_table_type(jQuery(dest_elem));
    tbl = _pymeth_find.call(jQuery(dest_elem), ".tabsort");
    if ((tbl.length > 0)) {
        init_table(tbl, table_type);
    }
    ((_pymeth_find.call(jQuery(dest_elem), ".tree")).treegrid)();
    return null;
};

register_mount_fun(datatable_init);
register_mount_fun(process_resize);
get_ajax_region = function flx_get_ajax_region (element, region_name) {
    var ret;
    region_name = (region_name === undefined) ? null: region_name;
    if (((_pyfunc_truthy(element.classList.contains("ajax-region"))) && ((((!_pyfunc_truthy(region_name))) || (_pyfunc_op_equals(element.getAttribute("data-region"), region_name)))))) {
        return element;
    } else if (_pyfunc_truthy(region_name)) {
        ret = element.closest(".ajax-region");
        while (ret) {
            if ((_pyfunc_op_equals(ret.getAttribute("data-region"), region_name))) {
                return ret;
            }
            ret = ret.parentElement;
            if (_pyfunc_truthy(ret)) {
                ret = ret.closest(".ajax-region");
            }
        }
        if (_pyfunc_truthy(region_name)) {
            return get_ajax_region(element, null);
        } else {
            return null;
        }
    } else {
        return element.closest(".ajax-region");
    }
    return null;
};

window.get_ajax_region = get_ajax_region;
get_ajax_link = function flx_get_ajax_link (element, region_name) {
    var link, region;
    region_name = (region_name === undefined) ? null: region_name;
    if (((_pyfunc_truthy(element.classList.contains("ajax-link"))) && ((((!_pyfunc_truthy(region_name))) || (_pyfunc_op_equals(element.getAttribute("data-region"), region_name)))))) {
        return element;
    }
    region = get_ajax_region(element, region_name);
    if (_pyfunc_truthy(region)) {
        if (_pyfunc_truthy(region.classList.contains("ajax-link"))) {
            return region;
        } else if (_pyfunc_truthy(region_name)) {
            link = region.querySelector((".ajax-link[data-region='" + region_name) + "']");
            if (_pyfunc_truthy(link)) {
                return link;
            }
        } else {
            return region.querySelector(".ajax-link");
        }
    }
    if (_pyfunc_truthy(region_name)) {
        return get_ajax_link(element, null);
    } else {
        return null;
    }
    return null;
};

window.get_ajax_link = get_ajax_link;
get_ajax_frame = function flx_get_ajax_frame (element, region_name) {
    var frame, region;
    region_name = (region_name === undefined) ? null: region_name;
    region = get_ajax_region(element, region_name);
    if (_pyfunc_truthy(region)) {
        if (((_pyfunc_truthy(region.classList.contains("ajax-frame"))) && ((((!_pyfunc_truthy(region_name))) || (_pyfunc_op_equals(region.getAttribute("data-region"), region_name)))))) {
            return region;
        } else if (_pyfunc_truthy(region_name)) {
            frame = region.querySelector((".ajax-frame[data-region='" + region_name) + "']");
            if (_pyfunc_truthy(frame)) {
                return frame;
            }
        } else {
            return region.querySelector(".ajax-frame");
        }
    }
    if (_pyfunc_truthy(region_name)) {
        return get_ajax_frame(element, null);
    } else {
        return null;
    }
    return null;
};

window.get_ajax_frame = get_ajax_frame;
refresh_ajax_frame = function flx_refresh_ajax_frame (element, region_name, data_element, callback, callback_on_error) {
    var _callback, data, frame, link, loading, post, region, url;
    region_name = (region_name === undefined) ? null: region_name;
    data_element = (data_element === undefined) ? null: data_element;
    callback = (callback === undefined) ? null: callback;
    callback_on_error = (callback_on_error === undefined) ? null: callback_on_error;
    region = get_ajax_region(element, region_name);
    frame = get_ajax_frame(element, region_name);
    if ((!_pyfunc_truthy(frame))) {
        return null;
    }
    link = get_ajax_link(element, region_name);
    loading = new Loading(element);
    _callback = (function flx__callback (data) {
        var dt;
        loading.stop();
        loading.remove();
        dt = data_type(data);
        if ((((!_pyfunc_op_equals(dt, "$$RETURN_ERROR"))) && (_pyfunc_truthy(_pyfunc_getattr(frame, "onloadeddata"))) && _pyfunc_truthy(frame.onloadeddata))) {
            mount_html(frame, data, link);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_OK", "$$RETURN_REFRESH"])) {
            return refresh_ajax_frame(element, region_name, null, callback, callback_on_error);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_NEW_ROW_OK", "$$RETURN_UPDATE_ROW_OK", "$$RETURN_REFRESH_PARENT"])) {
            return refresh_ajax_frame(region.parentElement, region_name, null, callback, callback_on_error);
        } else if (_pyfunc_op_equals(dt, "$$RETURN_RELOAD")) {
            if (_pyfunc_op_equals(region_name, "error")) {
                mount_html(frame, data, link);
            } else {
                return refresh_ajax_frame(element, "error", data, callback, callback_on_error);
            }
        } else if (_pyfunc_op_equals(dt, "$$RETURN_CANCEL")) {
        } else if (_pyfunc_op_equals(dt, "$$RETURN_ERROR")) {
            if ((Object.prototype.toString.call(data).slice(8,-1).toLowerCase() === 'string')) {
                (window.open().document.write)(data);
            } else {
                (window.open().document.write)(data.innerHTML);
            }
        } else {
            mount_html(frame, data, link);
        }
        if (_pyfunc_op_contains(dt, ["$$RETURN_ERROR", "$$RETURN_RELOAD"])) {
            if (_pyfunc_truthy(callback_on_error)) {
                callback_on_error();
            }
        } else if (_pyfunc_truthy(callback)) {
            callback();
        }
        return null;
    }).bind(this);

    if (_pyfunc_truthy(data_element)) {
        _callback(data_element);
        return null;
    }
    url = null;
    post = false;
    if (_pyfunc_truthy(link.hasAttribute("href"))) {
        url = link.getAttribute("href");
    } else if (_pyfunc_truthy(link.hasAttribute("action"))) {
        url = link.getAttribute("action");
        post = true;
    } else if (_pyfunc_truthy(link.hasAttribute("src"))) {
        url = link.getAttribute("src");
    }
    if (_pyfunc_truthy(url)) {
        if (((_pyfunc_truthy(link.hasAttribute("data-region"))) && ((_pyfunc_op_equals(link.getAttribute("data-region"), "table"))))) {
            url = corect_href(url, true);
        } else {
            url = corect_href(url);
        }
        loading.create();
        loading.start();
        if (_pyfunc_truthy(post)) {
            if ((_pyfunc_op_equals(_pymeth_lower.call(link.tagName), "form"))) {
                ajax_submit(jQuery(link), _callback);
            } else {
                data = (jQuery(link).serialize)();
                ajax_post(url, data, _callback);
            }
        } else {
            ajax_get(url, _callback);
        }
    } else {
        _callback(null);
    }
    return null;
};

window.refresh_ajax_frame = refresh_ajax_frame;
ajax_load = function flx_ajax_load (element, url, complete) {
    var _onload;
    _onload = (function flx__onload (responseText) {
        mount_html(element, responseText, null);
        complete(responseText);
        return null;
    }).bind(this);

    ajax_get(url, _onload);
    return null;
};

window.ajax_load = ajax_load;
export {data_type, register_mount_fun, mount_html, datetime_init, selectpicker_init, moveelement_init, label_floating_init, select2_init, datatable_init, get_ajax_region, get_ajax_link, get_ajax_frame, refresh_ajax_frame, ajax_load};

var INIT_DB_STRUCT, SYNC_STRUCT, _MSIE, _MSIE2, _UA, get_list_from_table, get_table, init_db, init_sync, on_sys_sync, open_database, sync_and_run;
INIT_DB_STRUCT = null;
init_db = function flx_init_db (struct) {
    INIT_DB_STRUCT = struct;
    return null;
};

window.init_db = init_db;
open_database = function flx_open_database (on_open) {
    var _onerror, _onsuccess, _onupgradeneeded, request;
    if ((!_pyfunc_truthy(window.indexedDB))) {
        console.log("Your Browser does not support IndexedDB");
    } else {
        request = window.indexedDB.open(window.PRJ_NAME, 1);
        _onerror = (function flx__onerror (event) {
            console.log("Error opening DB", event);
            return null;
        }).bind(this);

        request.onerror = _onerror;
        _onupgradeneeded = (function flx__onupgradeneeded (event) {
            var db, objectStore, pos, stub1_seq, stub2_itr;
            console.log("Upgrading");
            db = event.target.result;
            objectStore = db.createObjectStore("param", ({keyPath: "key"}));
            if (_pyfunc_truthy(INIT_DB_STRUCT)) {
                stub1_seq = INIT_DB_STRUCT;
                if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
                for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
                    pos = stub1_seq[stub2_itr];
                    objectStore = db.createObjectStore(pos[0], pos[1]);
                }
            }
            return null;
        }).bind(this);

        request.onupgradeneeded = _onupgradeneeded;
        _onsuccess = (function flx__onsuccess (event) {
            var db;
            db = event.target.result;
            on_open(db);
            return null;
        }).bind(this);

        request.onsuccess = _onsuccess;
    }
    return null;
};

window.open_database = open_database;
get_table = function flx_get_table (table_name, on_open, read_only) {
    var _on_open;
    read_only = (read_only === undefined) ? true: read_only;
    _on_open = (function flx__on_open (db) {
        var mode, tabObjectStore, tabTrans;
        if (_pyfunc_op_equals(read_only, true)) {
            mode = "readonly";
        } else {
            mode = "readwrite";
        }
        tabTrans = db.transaction(table_name, mode);
        tabObjectStore = tabTrans.objectStore(table_name);
        on_open(tabTrans, tabObjectStore);
        return null;
    }).bind(this);

    open_database(_on_open);
    return null;
};

window.get_table = get_table;
get_list_from_table = function flx_get_list_from_table (table, on_open_list) {
    var on_open;
    on_open = (function flx_on_open (trans, table) {
        var cursor_request, items, oncomplete, onerror, onsuccess;
        items = [];
        oncomplete = (function flx_oncomplete (evt) {
            on_open_list(items);
            return null;
        }).bind(this);

        trans.oncomplete = oncomplete;
        cursor_request = table.openCursor();
        onerror = (function flx_onerror (error) {
            console.log(error);
            return null;
        }).bind(this);

        cursor_request.onerror = onerror;
        onsuccess = (function flx_onsuccess (evt) {
            var cursor;
            cursor = evt.target.result;
            if (_pyfunc_truthy(cursor)) {
                items.push(cursor.value);
                cursor.continue();
            }
            return null;
        }).bind(this);

        cursor_request.onsuccess = onsuccess;
        return null;
    }).bind(this);

    get_table(table, on_open);
    return null;
};

window.get_list_from_table = get_list_from_table;
on_sys_sync = function flx_on_sys_sync (fun) {
    var _fun;
    _fun = (function flx__fun (cache_deleted) {
        if (_pyfunc_truthy(cache_deleted)) {
            fun("OK-refresh");
        } else {
            fun("OK-no cache");
        }
        return null;
    }).bind(this);

    (caches.delete("PYTIGON_" + window.PRJ_NAME).then)(_fun);
    return null;
};

_UA = window.navigator.userAgent;
_MSIE = _UA.indexOf("MSIE ");
_MSIE2 = _UA.indexOf("Trident/");
if (((_MSIE > 0) || (_MSIE2 > 0))) {
    SYNC_STRUCT = [];
} else {
    SYNC_STRUCT = [["sys", window.BASE_PATH + "schsys/app_time_stamp/", on_sys_sync]];
}
init_sync = function flx_init_sync (sync_struct) {
    var pos, stub3_seq, stub4_itr;
    stub3_seq = sync_struct;
    if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
    for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
        pos = stub3_seq[stub4_itr];
        _pymeth_append.call(SYNC_STRUCT, pos);
    }
    return null;
};

window.init_sync = init_sync;
sync_and_run = function flx_sync_and_run (tbl, fun) {
    var _on_request_init, complete, pos, rec, stub5_seq, stub6_itr;
    rec = null;
    stub5_seq = SYNC_STRUCT;
    if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
    for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
        pos = stub5_seq[stub6_itr];
        if (_pyfunc_op_equals(pos[0], tbl)) {
            rec = pos;
            break;
        }
    }
    if ((!_pyfunc_truthy(rec))) {
        fun("error - no reg function");
        return null;
    }
    if (_pyfunc_truthy(navigator.onLine)) {
        complete = (function flx_complete (responseText) {
            var _on_open_param, time, x;
            _on_open_param = (function flx__on_open_param (trans, db) {
                var _on_param_error, _on_param_success, param_get_request;
                param_get_request = _pymeth_get.call(db, ("time_sync_" + tbl));
                _on_param_error = (function flx__on_param_error (event) {
                    rec[2](fun);
                    db.add(({key: "time_sync_" + tbl, value: time}));
                    return null;
                }).bind(this);

                _on_param_success = (function flx__on_param_success (event) {
                    var _on_add_error, _on_add_success, _on_update, param, param_add_request, param_update_request, time2;
                    param = param_get_request.result;
                    if (_pyfunc_truthy(param)) {
                        time2 = param.value;
                        if ((time2 < time)) {
                            param.value = time;
                            param_update_request = db.put(param);
                            _on_update = (function flx__on_update (event) {
                                rec[2](fun);
                                return null;
                            }).bind(this);

                            param_update_request.onerror = _on_update;
                            param_update_request.onsuccess = _on_update;
                        } else {
                            fun("OK");
                        }
                    } else {
                        param_add_request = db.add(({key: "time_sync_" + tbl, value: time}));
                        _on_add_success = (function flx__on_add_success (event) {
                            rec[2](fun);
                            return null;
                        }).bind(this);

                        _on_add_error = (function flx__on_add_error (event) {
                            rec[2](fun);
                            return null;
                        }).bind(this);

                        param_add_request.onerror = _on_add_error;
                        param_add_request.onsuccess = _on_add_success;
                    }
                    return null;
                }).bind(this);

                param_get_request.onerror = _on_param_error;
                param_get_request.onsuccess = _on_param_success;
                return null;
            }).bind(this);

            if (true) {
                x = JSON.parse(responseText);
                time = x["TIME"];
                get_table("param", _on_open_param, false);
            }
            return null;
        }).bind(this);

        _on_request_init = (function flx__on_request_init (request) {
            var _on_timeout;
            _on_timeout = function (event) {
                fun("timeout");
                return null;
            };

            try {
                request.timeout = 2000;
            } catch(err_4) {
                {
                }
            }
            request.ontimeout = _on_timeout;
            return null;
        }).bind(this);

        ajax_get(rec[1], complete, _on_request_init);
    } else {
        fun("offline");
    }
    return null;
};

window.sync_and_run = sync_and_run;
export {init_db, open_database, get_table, get_list_from_table, on_sys_sync, init_sync, sync_and_run};

var EVENT_CLICK_TAB, EVENT_TAB, REGISTERED_EVENT_TYPES, _chcek_element, _get_click_event_from_tab, _get_title, _get_value, _on_inline, _on_menu_click, _on_popup, on_click_default_action, on_global_event, on_inline, on_inline_delete, on_inline_edit_new, on_inline_error, on_inline_info, on_new_tab, on_popup, on_popup_delete, on_popup_edit_new, on_popup_error, on_popup_info, on_replace_app, on_resize, only_get, process_href, refresh_app, refresh_frame, refresh_page, register_global_event;
EVENT_TAB = [];
REGISTERED_EVENT_TYPES = [];
_chcek_element = function flx__chcek_element (element, selector) {
    var sel, tag, x;
    if ((!_pyfunc_truthy(selector))) {
        return true;
    }
    if (_pyfunc_op_contains(".", selector)) {
        x = _pymeth_split.call(selector, ".");
        tag = x[0];
        sel = x[1];
    } else if (_pymeth_startswith.call(selector, "#")) {
        tag = null;
        sel = selector;
    } else {
        tag = selector;
        sel = null;
    }
    if (_pyfunc_truthy(tag)) {
        if ((!(_pyfunc_op_equals(_pymeth_lower.call(element.tagName), tag)))) {
            return false;
        }
    }
    if (_pyfunc_truthy(sel)) {
        if (_pymeth_startswith.call(sel, "#")) {
            if ((!_pyfunc_op_equals(element.id, sel.slice(1)))) {
                return false;
            }
        } else if ((!_pyfunc_truthy(element.classList.contains(sel)))) {
            return false;
        }
    }
    return true;
};

_get_title = function flx__get_title (element, data_element, url) {
    var title, title_alt, title_element, url2;
    title = element.getAttribute("title");
    if (_pyfunc_truthy(data_element)) {
        title_element = data_element.querySelector("title");
        if (_pyfunc_truthy(title_element)) {
            title_alt = _pymeth_strip.call(title_element.innerHTML);
        } else {
            title_alt = "";
        }
    } else {
        title_alt = "";
    }
    if (_pyfunc_truthy(((!_pyfunc_truthy(title))) && ((!_pyfunc_truthy(title_alt))))) {
        url2 = _pymeth_split.call(url, "?")[0];
        if ((url2.length > 16)) {
            title = "..." + url2.slice(-13);
        } else {
            title = url2;
        }
    } else if ((!_pyfunc_truthy(title))) {
        title = title_alt;
        title_alt = "";
    }
    return [title, title_alt];
};

on_global_event = function flx_on_global_event (event) {
    var element, pos, stub1_seq, stub2_itr;
    stub1_seq = EVENT_TAB;
    if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
    for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
        pos = stub1_seq[stub2_itr];
        if (_pyfunc_op_equals(pos[0], event.type)) {
            element = event.target;
            while (element) {
                if (_pyfunc_truthy(_chcek_element(element, pos[2]))) {
                    return pos[1](event, element);
                }
                element = element.parentElement;
                if ((_pyfunc_truthy(element) && ((_pyfunc_op_equals(_pymeth_lower.call(element.tagName), "body"))))) {
                    break;
                }
            }
        }
    }
    return null;
};

register_global_event = function flx_register_global_event (event_type, fun, selector) {
    if ((!_pyfunc_op_contains(event_type, REGISTERED_EVENT_TYPES))) {
        document.body.addEventListener(event_type, on_global_event);
        _pymeth_append.call(REGISTERED_EVENT_TYPES, event_type);
    }
    _pymeth_append.call(EVENT_TAB, [event_type, fun, selector]);
    return null;
};

window.register_global_event = register_global_event;
_get_value = function flx__get_value (elem, name) {
    var x, x2;
    if ((elem.length > 0)) {
        x = elem.closest(".ajax-region");
        if ((x.length > 0)) {
            x2 = _pymeth_find.call(x, sprintf("[name='%s']", name));
            if ((x2.length > 0)) {
                return x2.val();
            }
        }
    }
    return "[[ERROR]]";
};

process_href = function flx_process_href (href, elem) {
    var pos, process, ret, stub3_seq, stub4_itr, value, x1, x2;
    ret = [];
    if ((_pyfunc_op_contains("[[", href) && _pyfunc_op_contains("]]", href))) {
        x1 = _pymeth_split.call(href, "[[");
        process = false;
        stub3_seq = x1;
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            pos = stub3_seq[stub4_itr];
            if (_pyfunc_truthy(process)) {
                if (_pyfunc_op_contains("]]", pos)) {
                    x2 = _pymeth_split.call(pos, "]]", 1);
                    value = _get_value(elem, x2[0]);
                    if ((_pyfunc_truthy(value) && ((!_pyfunc_op_equals(value, "None"))))) {
                        _pymeth_append.call(ret, _pyfunc_op_add(value, x2[1]));
                    } else {
                        _pymeth_append.call(ret, x2[1]);
                    }
                } else {
                    _pymeth_append.call(ret, pos);
                }
                process = false;
            } else {
                _pymeth_append.call(ret, pos);
                process = true;
            }
        }
        return _pymeth_join.call("", ret);
    } else {
        return href;
    }
    return null;
};

window.process_href = process_href;
_get_click_event_from_tab = function flx__get_click_event_from_tab (target_element, target, href) {
    var pos, stub5_seq, stub6_itr, url;
    stub5_seq = EVENT_CLICK_TAB;
    if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
    for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
        pos = stub5_seq[stub6_itr];
        if ((_pyfunc_op_equals(pos[0], "*") || _pyfunc_op_equals(pos[0], target))) {
            if ((_pyfunc_op_equals(pos[1], "*") || target_element.classList.contains(pos[1]))) {
                if (_pyfunc_truthy(pos[3])) {
                    url = corect_href(href, true);
                } else if (_pyfunc_truthy(pos[2])) {
                    url = corect_href(href, false);
                } else {
                    url = href;
                }
                return [url, pos[4]];
            }
        }
    }
    return [null, null];
};

on_click_default_action = function flx_on_click_default_action (event, target_element) {
    var _callback2, _get_or_post, callback, href, param, src_obj, stub8_, target, url;
    target = target_element.getAttribute("target");
    if (_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "traditional")) {
        if (_pyfunc_truthy(((!_pyfunc_truthy(target))) || (_pyfunc_truthy(target) && _pyfunc_op_contains(target, ["_self", "_parent", "_top"])))) {
            return false;
        }
    }
    src_obj = jQuery(target_element);
    href = target_element.getAttribute("xlink:href");
    if ((!_pyfunc_truthy(href))) {
        href = target_element.getAttribute("href");
    }
    if ((!_pyfunc_truthy(href))) {
        href = target_element.getAttribute("action");
    }
    if ((!_pyfunc_truthy(href))) {
        href = target_element.getAttribute("src");
    }
    if ((_pyfunc_truthy(href) && _pyfunc_op_contains("#", href))) {
        return true;
    }
    if (_pyfunc_truthy(src_obj.hasClass("editable"))) {
        return true;
    }
    if (_pyfunc_truthy(href)) {
        href = process_href(href, jQuery(target_element));
    }
    if ((_pyfunc_op_equals(_pymeth_lower.call(target_element.tagName), "form"))) {
        if ((_pyfunc_op_equals(target_element.getAttribute("target"), "_blank"))) {
            target_element.setAttribute("enctype", "multipart/form-data");
            target_element.setAttribute("encoding", "multipart/form-data");
            return true;
        }
        if ((_pyfunc_op_equals(target_element.getAttribute("target"), "_self"))) {
            return true;
        }
        if (_pyfunc_truthy(target_element.querySelector("[type='file']"))) {
            param = "file";
        } else {
            param = (jQuery(target_element).serialize)();
        }
        if ((_pyfunc_truthy(param) && _pyfunc_op_contains("pdf=on", param))) {
            target_element.setAttribute("enctype", "multipart/form-data");
            target_element.setAttribute("encoding", "multipart/form-data");
            return true;
        }
        if ((_pyfunc_truthy(target_element) && _pyfunc_op_contains("odf=on", param))) {
            target_element.setAttribute("enctype", "multipart/form-data");
            target_element.setAttribute("encoding", "multipart/form-data");
            return true;
        }
    } else {
        param = null;
        if (_pyfunc_op_equals(target, "_blank")) {
            return null;
        }
    }
    _get_or_post = (function flx__get_or_post (url, callback, data2) {
        var _callback, loading;
        data2 = (data2 === undefined) ? null: data2;
        loading = new Loading(target_element);
        loading.create();
        loading.start();
        _callback = (function flx__callback (data) {
            var data_element, new_callback, new_target, new_target_elem, new_url, stub7_;
            loading.stop();
            loading.remove();
            data_element = get_elem_from_string(data);
            new_target_elem = data_element.querySelector("meta[name='target']");
            if (_pyfunc_truthy(new_target_elem)) {
                new_target = new_target_elem.getAttribute("content");
            } else {
                new_target = null;
            }
            if ((_pyfunc_truthy(new_target) && ((!_pyfunc_op_equals(new_target, target))))) {
                stub7_ = _get_click_event_from_tab(target_element, new_target, url);
                new_callback = stub7_[0];new_url = stub7_[1];
                new_callback(target_element, data_element, new_url, param, event);
            } else {
                callback(target_element, data_element, url, param, event);
            }
            return null;
        }).bind(this);

        if (_pyfunc_truthy(url)) {
            if (_pyfunc_truthy(param)) {
                ajax_post(url, param, _callback);
            } else {
                ajax_get(url, _callback);
            }
        } else {
            _callback(data2);
        }
        return null;
    }).bind(this);

    stub8_ = _get_click_event_from_tab(target_element, target, href);
    url = stub8_[0];callback = stub8_[1];
    if (_pyfunc_truthy(callback)) {
        if (_pyfunc_op_equals(param, "file")) {
            _callback2 = (function flx__callback2 (data2) {
                _get_or_post(null, callback, data2);
                return null;
            }).bind(this);

            ajax_submit(target_element, _callback2, null, null);
        } else if (_pyfunc_truthy(url)) {
            _get_or_post(url, callback, null);
        } else {
            callback(target_element, null, null, null, event);
        }
        event.preventDefault();
        return true;
    }
    return null;
};

_on_menu_click = function flx__on_menu_click (event, target_element) {
    var _on_collapse, toggler;
    if ((!_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "traditional"))) {
        event.preventDefault();
        toggler = document.querySelector("#topmenu .navbar-toggler");
        if ((_pyfunc_truthy(toggler) && (_pyfunc_truthy(is_visible(toggler))))) {
            _on_collapse = function () {
                on_click_default_action(event, target_element);
                (jQuery("#navbar-ex1-collapse").off)("hidden.bs.collapse", _on_collapse);
                return null;
            };

            (jQuery("#navbar-ex1-collapse").on)("hidden.bs.collapse", _on_collapse);
            (jQuery("#navbar-ex1-collapse").collapse)("hide");
        } else {
            on_click_default_action(event, target_element);
        }
    }
    return null;
};

register_global_event("click", _on_menu_click, "a.menu-href");
register_global_event("click", on_click_default_action, "a");
register_global_event("click", on_click_default_action, "button");
register_global_event("submit", on_click_default_action, "form");
_on_inline = function flx__on_inline (target_element, data_element, url, param, event, template_name) {
    var child, content, dialog, dialog_slot, dialog_slot2, inline_position, on_hidden;
    inline_position = target_element.getAttribute("data-inline-position");
    if ((_pyfunc_truthy(inline_position) && (_pyfunc_truthy(_pymeth_endswith.call(((_pymeth_split.call(inline_position, ":")[0])), "tr"))))) {
        dialog_slot = document.createElement("tr");
        child = document.createElement("td");
        child.setAttribute("colspan", "100");
        dialog_slot.appendChild(child);
        dialog_slot2 = child;
    } else {
        dialog_slot = document.createElement("div");
        dialog_slot.classList.add("col-12");
        dialog_slot2 = dialog_slot;
    }
    dialog_slot.classList.add("plug");
    dialog_slot2.innerHTML = get_template(_pymeth_replace.call(template_name, "MODAL", "INLINE"), ({title: _get_title(target_element, data_element, url)[0]}));
    target_element.setAttribute("data-style", "zoom-out");
    target_element.setAttribute("data-spinner-color", "#FF0000");
    content = dialog_slot.querySelector("div.dialog-data");
    content.appendChild(data_element);
    super_insert(target_element, inline_position, dialog_slot);
    mount_html(dialog_slot, null);
    on_hidden = function (event) {
        var obj, region;
        region = get_ajax_region(target_element, target_element.getAttribute("data-region"));
        if (_pyfunc_truthy(region)) {
            obj = region.querySelector(".plug");
            obj.remove();
        }
        return null;
    };

    dialog = jQuery(dialog_slot.firstElementChild);
    if (_pyfunc_truthy(dialog)) {
        dialog.on("click", "button.btn-close", on_hidden);
    }
    return null;
};

on_inline = function flx_on_inline (target_element, data_element, new_url, param, event) {
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE");
};

on_inline_edit_new = function flx_on_inline_edit_new (target_element, data_element, new_url, param, event) {
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_EDIT");
};

on_inline_info = function flx_on_inline_info (target_element, data_element, new_url, param, event) {
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_INFO");
};

on_inline_delete = function flx_on_inline_delete (target_element, data_element, new_url, param, event) {
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_DELETE");
};

on_inline_error = function flx_on_inline_error (target_element, data_element, new_url, param, event) {
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_ERROR");
};

_on_popup = function flx__on_popup (target_element, data_element, url, param, event, template_name) {
    var content, dialog, dialog_slot, on_hidden, region;
    if ((!_pyfunc_truthy(can_popup()))) {
        return _on_inline(target_element, data_element, url, param, event, template_name);
    }
    dialog_slot = document.createElement("aside");
    dialog_slot.setAttribute("class", "plug");
    dialog_slot.innerHTML = get_template(template_name, ({title: _get_title(target_element, data_element, url)[0]}));
    region = get_ajax_region(target_element, target_element.getAttribute("data-region"));
    if ((!_pyfunc_truthy(region))) {
        return null;
    }
    region.appendChild(dialog_slot);
    target_element.setAttribute("data-style", "zoom-out");
    target_element.setAttribute("data-spinner-color", "#FF0000");
    content = dialog_slot.querySelector("div.dialog-data");
    mount_html(content, data_element);
    on_hidden = function (event) {
        var obj;
        obj = region.querySelector(".plug");
        if (_pyfunc_truthy(obj)) {
            obj.remove();
        }
        return null;
    };

    dialog = jQuery(dialog_slot.firstElementChild);
    if (_pyfunc_truthy(dialog)) {
        dialog.on("hidden.bs.modal", on_hidden);
        dialog.drags(({handle: ".modal-header"}));
        dialog.modal(({show: true}));
    }
    return null;
};

on_popup = function flx_on_popup (target_element, data_element, new_url, param, event) {
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL");
};

on_popup_edit_new = function flx_on_popup_edit_new (target_element, data_element, new_url, param, event) {
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_EDIT");
};

on_popup_info = function flx_on_popup_info (target_element, data_element, new_url, param, event) {
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_INFO");
};

on_popup_delete = function flx_on_popup_delete (target_element, data_element, new_url, param, event) {
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_DELETE");
};

on_popup_error = function flx_on_popup_error (target_element, data_element, new_url, param, event) {
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_ERROR");
};

on_new_tab = function flx_on_new_tab (target_element, data_element, new_url, param, event) {
    var data_element2, stub9_, title, title_alt;
    stub9_ = _get_title(target_element, data_element, new_url);
    title = stub9_[0];title_alt = stub9_[1];
    data_element2 = data_element.querySelector("section.body-body");
    if ((!_pyfunc_truthy(data_element2))) {
        data_element2 = data_element;
    }
    return (get_menu().on_menu_href)(target_element, data_element2, title, title_alt, new_url);
};

on_replace_app = function flx_on_replace_app (target_element, data_element, new_url, param, event) {
    if (_pyfunc_truthy(window.PUSH_STATE)) {
        history_push_state("", window.BASE_PATH);
    } else {
        window.location.pathname = window.BASE_PATH;
    }
    window.MENU = null;
    mount_html(document.querySelector("section.body-body"), data_element.querySelector("section.body-body"), false);
    return null;
};

refresh_frame = function flx_refresh_frame (target_element, data_element, new_url, param, event) {
    var _callback, _callback_on_error, aside, data_element2, data_region, dialog, f;
    dialog = null;
    aside = target_element.closest(".plug");
    if (_pyfunc_truthy(aside)) {
        dialog = aside.firstElementChild;
    }
    _callback = (function flx__callback () {
        if (_pyfunc_truthy(aside)) {
            if ((_pyfunc_truthy(dialog) && (_pyfunc_truthy(dialog.classList.contains("modal"))))) {
                (jQuery(dialog).modal)("hide");
            } else {
                aside.remove();
            }
        }
        return null;
    }).bind(this);

    _callback_on_error = (function flx__callback_on_error () {
        if (_pyfunc_truthy(aside)) {
            aside.style.opacity = "100%";
        }
        return null;
    }).bind(this);

    if (_pyfunc_truthy(aside)) {
        aside.style.opacity = "50%";
    }
    f = target_element.getAttribute("data-remote-elem");
    if (_pyfunc_truthy(f)) {
        data_element2 = data_element.querySelector(f);
    } else {
        data_element2 = data_element;
    }
    data_region = target_element.getAttribute("data-region");
    refresh_ajax_frame(target_element, data_region, data_element2, _callback, _callback_on_error);
    return null;
};

refresh_page = function flx_refresh_page (target_element, data_element, new_url, param, event) {
    var data_element2, frame;
    frame = target_element.closest("div.content");
    if ((_pyfunc_truthy(frame) && _pyfunc_truthy(frame.firstElementChild))) {
        if ((Object.prototype.toString.call(data_element).slice(8,-1).toLowerCase() === 'string')) {
            data_element2 = null;
        } else {
            data_element2 = data_element.querySelector("div.content");
        }
        if (_pyfunc_truthy(data_element2)) {
            if (_pyfunc_truthy(data_element2.firstElementChild)) {
                data_element2 = data_element2.firstElementChild;
            }
        }
        if ((!_pyfunc_truthy(data_element2))) {
            data_element2 = data_element;
        }
        mount_html(frame, data_element2);
    }
    return null;
};

refresh_app = function flx_refresh_app (target_element, data_element, new_url, param, event) {
    window.location.href = window.BASE_PATH;
    return null;
};

only_get = function flx_only_get (target_element, data_element, url, param, event) {
    return null;
};

EVENT_CLICK_TAB = [["inline", "*", true, false, on_inline], ["inline_edit", "*", true, false, on_inline_edit_new], ["inline_info", "*", true, false, on_inline_info], ["inline_delete", "*", true, false, on_inline_delete], ["inline_error", "*", true, false, on_inline_error], ["popup", "*", true, false, on_popup], ["popup_edit", "*", true, false, on_popup_edit_new], ["popup_info", "*", true, false, on_popup_info], ["popup_delete", "*", true, false, on_popup_delete], ["popup_error", "*", true, false, on_popup_error], ["_top", "*", false, false, on_replace_app], ["_top2", "*", true, false, on_new_tab], ["_self", "*", true, false, refresh_page], ["_parent", "*", true, false, on_new_tab], ["refresh_frame", "*", true, false, refresh_frame], ["refresh_page", "*", true, false, refresh_page], ["refresh_app", "*", false, false, refresh_app], ["null", "*", false, false, only_get]];
on_resize = function flx_on_resize (event) {
    process_resize(document.body);
    return null;
};

window.addEventListener("resize", on_resize);
export {on_global_event, register_global_event, process_href, on_click_default_action, on_inline, on_inline_edit_new, on_inline_info, on_inline_delete, on_inline_error, on_popup, on_popup_edit_new, on_popup_info, on_popup_delete, on_popup_error, on_new_tab, on_replace_app, refresh_frame, refresh_page, refresh_app, only_get, on_resize};

var install_service_worker, service_worker_and_indexedDB_test;
install_service_worker = function flx_install_service_worker () {
    var err, reg;
    if (_pyfunc_hasattr(navigator, "serviceWorker")) {
        reg = (function flx_reg (registration) {
            var onstatechange, serviceWorker;
            if (_pyfunc_truthy(registration.installing)) {
                serviceWorker = registration.installing;
            } else if (_pyfunc_truthy(registration.waiting)) {
                serviceWorker = registration.waiting;
            } else if (_pyfunc_truthy(registration.active)) {
                serviceWorker = registration.active;
            }
            if (_pyfunc_truthy(serviceWorker)) {
                console.log(serviceWorker.state);
                onstatechange = function (e) {
                    console.log(e.target.state);
                    return null;
                };

                serviceWorker.addEventListener("statechange", onstatechange);
            }
            return null;
        }).bind(this);

        err = (function flx_err (error) {
            console.log(error);
            return null;
        }).bind(this);

        (((navigator.serviceWorker.register(BASE_PATH + "sw.js").then)(reg)).catch)(err);
    } else {
        console.log("The current browser doesn't support service workers");
    }
    return null;
};

service_worker_and_indexedDB_test = function flx_service_worker_and_indexedDB_test () {
    if ((_pyfunc_hasattr(navigator, "serviceWorker") && _pyfunc_hasattr(window, "indexedDB") && ((_pyfunc_op_equals(location.hostname, "localhost") || _pyfunc_op_equals(location.hostname, "127.0.0.1") || _pyfunc_op_equals(location.hostname, "127.0.0.2") || _pyfunc_op_equals(location.protocol, "https:"))))) {
        return true;
    } else {
        return false;
    }
    return null;
};

export {install_service_worker, service_worker_and_indexedDB_test};

var Page, TabMenu, TabMenuItem, get_menu;
Page = function () {
    _pyfunc_op_instantiate(this, arguments);
}
Page.prototype._base_class = Object;
Page.prototype.__name__ = "Page";

Page.prototype.__init__ = function (id, page) {
    this.id = id;
    this.page = page;
    return null;
};

Page.prototype.set_href = function (href) {
    this.page.attr("_href", href);
    return null;
};

Page.prototype.get_href = function () {
    return this.page.attr("_href");
};


TabMenuItem = function () {
    _pyfunc_op_instantiate(this, arguments);
}
TabMenuItem.prototype._base_class = Object;
TabMenuItem.prototype.__name__ = "TabMenuItem";

TabMenuItem.prototype.__init__ = function (id, title, url, data) {
    data = (data === undefined) ? null: data;
    this.id = id;
    this.title = jQuery.trim(title);
    this.url = url;
    this.data = data;
    return null;
};


TabMenu = function () {
    _pyfunc_op_instantiate(this, arguments);
}
TabMenu.prototype._base_class = Object;
TabMenu.prototype.__name__ = "TabMenu";

TabMenu.prototype.__init__ = function () {
    this.id = 0;
    this.titles = ({});
    this.active_item = null;
    return null;
};

TabMenu.prototype.get_active_item = function () {
    return this.active_item;
};

TabMenu.prototype.is_open = function (title) {
    if ((_pyfunc_truthy(this.titles) && _pyfunc_op_contains(title, this.titles) && _pyfunc_truthy(this.titles[title]))) {
        return true;
    } else {
        return false;
    }
    return null;
};

TabMenu.prototype.activate = function (title, push_state) {
    var menu_item;
    push_state = (push_state === undefined) ? true: push_state;
    menu_item = this.titles[title];
    ((jQuery(sprintf("#li_%s a", menu_item.id))).tab)("show");
    if ((_pyfunc_truthy(push_state) && _pyfunc_truthy(window.PUSH_STATE))) {
        history_push_state(menu_item.title, menu_item.url);
    }
    return null;
};

TabMenu.prototype.register = function (title) {
    this.titles[title] = "$$$";
    return null;
};

TabMenu.prototype.new_page = function (title, data_or_html, href, title_alt) {
    var _id, _local_fun, _on_button_click, _on_show_tab, append_left, menu_item, menu_pos, scripts;
    title_alt = (title_alt === undefined) ? null: title_alt;
    _id = "tab" + this.id;
    menu_item = new TabMenuItem(_id, title, href, data_or_html);
    this.titles[title] = menu_item;
    if ((_pyfunc_truthy(title_alt) && ((!_pyfunc_op_equals(title_alt, title))))) {
        this.titles[title_alt] = menu_item;
    }
    menu_pos = vsprintf("<li id='li_%s' class ='nav-item'><a href='#%s' class='nav-link bg-info' data-toggle='tab' role='tab' title='%s'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-outline-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", [_id, _id, title, title, _id]);
    append_left = (jQuery("#tabs2").hasClass)("append-left");
    if (_pyfunc_truthy(append_left)) {
        (jQuery("#tabs2").prepend)(menu_pos);
    } else {
        _pymeth_append.call(jQuery("#tabs2"), menu_pos);
    }
    _pymeth_append.call(jQuery("#tabs2_content"), sprintf("<div class='tab-pane container-fluid ajax-region ajax-frame win-content page' id='%s'></div>", _id));
    window.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
    this.active_item = menu_item;
    if (_pyfunc_truthy(window.PUSH_STATE)) {
        history_push_state(title, href);
    }
    _on_show_tab = function (e) {
        var menu;
        window.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id), menu_item);
        menu = get_menu();
        menu_item = menu.titles[jQuery.trim(e.target.text)];
        this.active_item = menu_item;
        if (_pyfunc_truthy(window.PUSH_STATE)) {
            history_push_state(menu_item.title, menu_item.url);
        }
        process_resize(document.getElementById(menu_item.id));
        return null;
    };

    if (_pyfunc_truthy(append_left)) {
        (jQuery("#tabs2 a:first").on)("shown.bs.tab", _on_show_tab);
        (jQuery("#tabs2 a:first").tab)("show");
    } else {
        (jQuery("#tabs2 a:last").on)("shown.bs.tab", _on_show_tab);
        (jQuery("#tabs2 a:last").tab)("show");
    }
    mount_html(document.getElementById(_id), data_or_html, null);
    _on_button_click = function (event) {
        (get_menu().remove_page)(_pymeth_replace.call((((jQuery(this).attr)("id"))), "button_", ""));
        return null;
    };

    ((jQuery(sprintf("#button_%s", _id))).click)(_on_button_click);
    scripts = jQuery(("#" + _id) + " script");
    _local_fun = (function flx__local_fun (index, element) {
        eval(this.innerHTML);
        return null;
    }).bind(this);

    scripts.each(_local_fun);
    this.id += 1;
    return _id;
};

TabMenu.prototype.remove_page = function (id) {
    var _local_fun, last_a;
    _local_fun = (function flx__local_fun (index, value) {
        if ((_pyfunc_truthy(value) && _pyfunc_op_equals(value.id, id))) {
            this.titles[index] = null;
        }
        return null;
    }).bind(this);

    jQuery.each(this.titles, _local_fun);
    remove_element(sprintf("#li_%s", id));
    remove_element(sprintf("#%s", id));
    last_a = jQuery("#tabs2 a:last");
    if ((last_a.length > 0)) {
        last_a.tab("show");
    } else {
        window.ACTIVE_PAGE = null;
        if (_pyfunc_truthy(window.PUSH_STATE)) {
            history_push_state("", window.BASE_PATH);
        }
        if ((_pyfunc_op_equals(((_pymeth_find.call(jQuery("#body_desktop"), ".content")).length), 0))) {
            window.init_start_wiki_page();
        }
        (jQuery("#body_desktop").show)();
    }
    return null;
};

TabMenu.prototype.on_menu_href = function (elem, data_or_html, title, title_alt, url) {
    var href, href2;
    title_alt = (title_alt === undefined) ? null: title_alt;
    url = (url === undefined) ? null: url;
    if (_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "modern")) {
        if (_pyfunc_truthy(this.is_open(title))) {
            this.activate(title);
        } else {
            this.register(title);
            if (_pyfunc_truthy(url)) {
                href = url;
            } else {
                href = (jQuery(elem).attr)("href");
            }
            href2 = corect_href(href);
            (jQuery("#body_desktop").hide)();
            this.new_page(title, data_or_html.innerHTML, href2, title_alt);
        }
        (jQuery(".auto-hide").trigger)("click");
        return false;
    } else {
        mount_html(document.querySelector("#body_desktop"), data_or_html, null);
        (jQuery(".auto-hide").trigger)("click");
        return false;
    }
    return null;
};


get_menu = function flx_get_menu () {
    if ((!_pyfunc_truthy(window.MENU))) {
        window.MENU = new TabMenu();
    }
    return window.MENU;
};

export {Page, TabMenuItem, TabMenu, get_menu};

var _is_visible, _rowStyle, datatable_ajax, datatable_refresh, datetable_set_height, init_table, prepare0, prepare_datatable, table_loadeddata;
_is_visible = function flx__is_visible (element) {
    var test;
    test = jQuery(element).is(":visible");
    if (_pyfunc_truthy(test)) {
        return true;
    } else {
        return false;
    }
    return null;
};

datetable_set_height = function flx_datetable_set_height (element) {
    var dy, dy_win, elem, panel, table_offset;
    if (_pyfunc_truthy((jQuery(element).hasClass)("table_get"))) {
        return null;
    }
    if ((!_pyfunc_truthy(_is_visible(element)))) {
        return null;
    }
    elem = (jQuery(element).closest)(".tabsort_panel");
    table_offset = elem.offset().top;
    dy_win = (jQuery(window).height)();
    dy = dy_win - table_offset;
    if ((dy < 200)) {
        dy = 200;
    }
    panel = _pymeth_find.call(elem, ".fixed-table-toolbar");
    if ((!_pyfunc_truthy(_is_visible(panel)))) {
        dy = _pyfunc_op_add(dy, panel.height() - 15);
    }
    (jQuery(element).bootstrapTable)("resetView", ({height: dy - 5}));
    return null;
};

datatable_refresh = function flx_datatable_refresh (table) {
    table.bootstrapTable("refresh");
    return null;
};

_rowStyle = function flx__rowStyle (value, row, index) {
    var c, x;
    x = _pymeth_find.call(((jQuery(("<div>" + value["cid"]) + "</div>"))), "div.td_information");
    if ((x.length > 0)) {
        c = _pymeth_replace.call(((_pymeth_replace.call(x.attr("class"), "td_information", ""))), " ", "");
        if ((c.length > 0)) {
            return ({classes: c});
        }
    }
    return ({});
};

prepare_datatable = function flx_prepare_datatable (table) {
    var _local_fun;
    _local_fun = (function flx__local_fun (index) {
        var l, td, tr;
        td = (jQuery(this).parent)();
        tr = td.parent();
        l = _pymeth_find.call(tr, "td").length;
        ((_pymeth_find.call(tr, "td:gt(0)")).remove)();
        td.attr("colspan", l);
        return null;
    }).bind(this);

    (_pymeth_find.call(table, "div.second_row").each)(_local_fun);
    return null;
};

prepare0 = function flx_prepare0 (table) {
    var refr_block, stub1_seq, stub2_itr, tables;
    refr_block = table.closest(".ajax-frame");
    if (_pyfunc_truthy(refr_block)) {
        tables = Array.prototype.slice.call((refr_block[0].querySelectorAll)("div.fixed-table-header table.tabsort"));
        stub1_seq = tables;
        if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
        for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
            table = stub1_seq[stub2_itr];
            _pymeth_remove.call(table.classList, "flexible_size");
        }
    }
    return null;
};

datatable_ajax = function flx_datatable_ajax (params) {
    var _on_get_data, _on_post_data, d, form, success, url;
    url = params["url"];
    success = params["success"];
    if ((_pyfunc_op_contains("form", _pyfunc_dict(params["data"])))) {
        form = params["data"]["form"];
        delete params["data"]["form"];
        d = jQuery.param(params["data"]);
        url = _pyfunc_op_add(url, "?" + d);
        _on_post_data = (function flx__on_post_data (data) {
            var d2;
            d2 = JSON.parse(data);
            success(d2);
            return null;
        }).bind(this);

        ajax_post(url, form, _on_post_data);
    } else {
        d = jQuery.param(params["data"]);
        url = _pyfunc_op_add(url, "?" + d);
        _on_get_data = (function flx__on_get_data (data) {
            var d2;
            d2 = JSON.parse(data);
            success(d2);
            return null;
        }).bind(this);

        ajax_get(url, _on_get_data);
    }
    return null;
};

init_table = function flx_init_table (table, table_type) {
    var _handle_toolbar_expand, _process_resize, btn, init_bootstrap_table, onLoadSuccess, onPostHeader, panel, panel2, queryParams, table_panel;
    if (_pyfunc_op_equals(table_type, "datatable")) {
        onLoadSuccess = (function flx_onLoadSuccess (data) {
            var _pagination;
            prepare_datatable(table);
            _pagination = (function flx__pagination () {
                ((_pymeth_find.call((((jQuery(table).closest)(".fixed-table-container"))), ".fixed-table-pagination ul.pagination a")).addClass)("page-link");
                return null;
            }).bind(this);

            setTimeout(_pagination, 0);
            return false;
        }).bind(this);

        onPostHeader = (function flx_onPostHeader (data) {
            prepare0(table);
            return false;
        }).bind(this);

        queryParams = (function flx_queryParams (p) {
            var refr_block, src;
            refr_block = (jQuery(table).closest)(".ajax-frame");
            src = _pymeth_find.call(refr_block, ".ajax-link");
            if (((src.length > 0) && ((_pyfunc_op_equals(src.prop("tagName"), "FORM"))))) {
                p["form"] = src.serialize();
            }
            return p;
        }).bind(this);

        if (_pyfunc_truthy(table.hasClass("table_get"))) {
            table.bootstrapTable(({onLoadSuccess: onLoadSuccess, onPostHeader: onPostHeader, height: 350, rowStyle: _rowStyle, queryParams: queryParams, ajax: datatable_ajax}));
        } else {
            table.bootstrapTable(({onLoadSuccess: onLoadSuccess, onPostHeader: onPostHeader, rowStyle: _rowStyle, queryParams: queryParams, ajax: datatable_ajax}));
        }
        init_bootstrap_table = function (e, data) {
            var on_hidden_editable;
            (_pymeth_find.call(table, "a.editable").editable)(({step: "any"}));
            on_hidden_editable = function (e, reason) {
                var edit_next, next;
                if ((_pyfunc_op_equals(reason, "save") || _pyfunc_op_equals(reason, "nochange"))) {
                    next = _pymeth_find.call((((((jQuery(this).closest)("tr")).next)())), ".editable");
                    if ((next.length > 0)) {
                        if (_pyfunc_truthy(next.hasClass("autoopen"))) {
                            edit_next = (function flx_edit_next () {
                                next.editable("show");
                                return null;
                            }).bind(this);

                            setTimeout(edit_next, 300);
                        } else {
                            next.focus();
                        }
                    }
                }
                return null;
            };

            (_pymeth_find.call(table, "a.editable").on)("hidden", on_hidden_editable);
            return null;
        };

        table.on("post-body.bs.table", init_bootstrap_table);
        table_panel = (jQuery(table).closest)(".content");
        btn = _pymeth_find.call(table_panel, ".tabsort-toolbar-expand");
        if (_pyfunc_truthy(btn)) {
            _handle_toolbar_expand = function (elem) {
                var panel, panel2;
                panel = _pymeth_find.call(table_panel, ".fixed-table-toolbar");
                panel2 = jQuery(".list_content_header_two_row");
                if (_pyfunc_truthy((jQuery(this).hasClass)("active"))) {
                    panel.show();
                    panel2.show();
                } else {
                    panel.hide();
                    panel2.hide();
                }
                process_resize(document.body);
                return null;
            };

            table_panel.on("click", ".tabsort-toolbar-expand", _handle_toolbar_expand);
            if (_pyfunc_truthy(btn.hasClass("active"))) {
                panel = _pymeth_find.call(table_panel, ".fixed-table-toolbar");
                panel2 = jQuery(".list_content_header_two_row");
                panel.hide();
                panel2.hide();
            }
        }
        _process_resize = (function flx__process_resize (size_object) {
            datetable_set_height(table[0]);
            return null;
        }).bind(this);

        table[0].process_resize = _process_resize;
    }
    return null;
};

table_loadeddata = function flx_table_loadeddata (event) {
    if (_pyfunc_truthy(_pyfunc_getattr(event, "data"))) {
        if ((_pyfunc_truthy(event.data) && _pyfunc_op_contains("$$RETURN_REFRESH_PARENT", event.data))) {
            ((_pymeth_find.call(jQuery(event.target), "table[name=tabsort].datatable")).bootstrapTable)("refresh");
        } else {
            refresh_ajax_frame(event.data_source, "error", event.data);
        }
    } else {
        ((_pymeth_find.call(jQuery(event.target), "table[name=tabsort].datatable")).bootstrapTable)("refresh");
    }
    return null;
};

window.table_loadeddata = table_loadeddata;
export {datetable_set_height, datatable_refresh, prepare_datatable, prepare0, datatable_ajax, init_table, table_loadeddata};

var humanFileSize, img_field;
humanFileSize = function flx_humanFileSize (bytes, si) {
    var thresh, u, units;
    if (_pyfunc_truthy(si)) {
        thresh = 1000;
    } else {
        thresh = 1024;
    }
    if ((Math.abs(bytes) < thresh)) {
        return [bytes + " B", 0];
    }
    if (_pyfunc_truthy(si)) {
        units = ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    } else {
        units = ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];
    }
    u = -1;
    while (true) {
        bytes /= thresh;
        u += 1;
        if ((!(((Math.abs(bytes) >= thresh)) && ((u < (units.length - 1)))))) {
            break;
        }
    }
    return [(bytes.toFixed(1) + " ") + units[u], u + 1];
};

img_field = function flx_img_field (elem) {
    var _onload, ext, file_name, img, level, pos, reader, size, stub1_seq, stub2_itr, stub3_, test, txt, x;
    txt = _pymeth_replace.call((((jQuery(elem).val)())), (new RegExp("^.*[\\\\ /]")), "");
    ((_pymeth_find.call((((jQuery(elem).closest)("label"))), ".upload")).html)(txt);
    if ((_pyfunc_truthy(elem.files) && _pyfunc_truthy(elem.files[0]))) {
        file_name = elem.files[0].name;
        ext = [".jpeg", ".jpg", ".svg", ".gif", ".png"];
        test = false;
        stub1_seq = ext;
        if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
        for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
            pos = stub1_seq[stub2_itr];
            if ((_pyfunc_op_contains(pos, _pymeth_lower.call(file_name)))) {
                test = true;
                break;
            }
        }
        if (_pyfunc_truthy(test)) {
            reader = new FileReader();
            _onload = function (e) {
                var img, x;
                x = _pymeth_find.call((((jQuery(elem).closest)("label"))), ".img");
                if ((x.length > 0)) {
                    x.remove();
                }
                img = jQuery("<img class='img' />");
                img.insertAfter(_pymeth_find.call((((jQuery(elem).closest)("label"))), "input"));
                img.attr("src", e.target.result);
                return null;
            };

            reader.onload = _onload;
            reader.readAsDataURL(elem.files[0]);
        } else {
            x = _pymeth_find.call((((jQuery(elem).closest)("label"))), ".img");
            if ((x.length > 0)) {
                x.remove();
            }
            stub3_ = humanFileSize(elem.files[0].size, true);
            size = stub3_[0];level = stub3_[1];
            ext = (((((elem.files[0].type) + "<br><span class='size_level_") + level) + "'>") + size) + "</span>";
            img = jQuery("<p class='img' />");
            img.insertAfter(_pymeth_find.call((((jQuery(elem).closest)("label"))), "input"));
            img.html(ext);
        }
    }
    return null;
};

window.img_field = img_field;
export {humanFileSize, img_field};

var _on_error, _on_key, _on_popstate, activate_menu, app_init, dom_content_loaded, jquery_ready;
window.PS = null;
window.MOUNTED_COMPONENTS = 0;
window.GLOBAL_BUS = new GlobalBus();
window.START_MENU_ID = null;
_on_key = function (e) {
    var elem, form;
    if (_pyfunc_op_equals(e.which, 13)) {
        elem = jQuery(e.target);
        if ((!_pyfunc_op_equals(elem.prop("tagName"), "TEXTAREA"))) {
            form = elem.closest("form");
            if ((form.length > 0)) {
                if (_pyfunc_truthy(form.hasClass("DialogForm"))) {
                    e.preventDefault();
                    on_edit_ok(false, form);
                    return null;
                }
            }
        }
    }
    return null;
};

register_global_event("keypress", _on_key, null);
dom_content_loaded = function flx_dom_content_loaded () {
    mount_html(document.querySelector("section.body-body"), null);
    return null;
};

app_init = function flx_app_init (prj_name, application_template, menu_id, lang, base_path, base_fragment_init, component_init, offline_support, start_page, gen_time, callback) {
    var _init_start_wiki_page, _on_sync, desktop;
    callback = (callback === undefined) ? null: callback;
    moment.locale(lang);
    window.ACTIVE_PAGE = null;
    window.PRJ_NAME = prj_name;
    window.APPLICATION_TEMPLATE = application_template;
    window.MENU = null;
    window.PUSH_STATE = true;
    if (_pyfunc_truthy(base_path)) {
        window.BASE_PATH = base_path;
    } else {
        window.BASE_PATH = "";
    }
    window.WAIT_ICON = null;
    window.WAIT_ICON2 = false;
    window.START_MENU_ID = menu_id;
    window.BASE_FRAGMENT_INIT = base_fragment_init;
    window.COUNTER = 1;
    window.EDIT_RET_FUNCTION = null;
    window.RET_CONTROL = null;
    window.COMPONENT_INIT = component_init;
    window.LANG = lang;
    window.GEN_TIME = gen_time;
    if (_pyfunc_op_equals(APPLICATION_TEMPLATE, "traditional")) {
        document.addEventListener("DOMContentLoaded", dom_content_loaded);
    }
    if (_pyfunc_truthy(offline_support)) {
        if ((_pyfunc_truthy(navigator.onLine) && (_pyfunc_truthy(service_worker_and_indexedDB_test())))) {
            install_service_worker();
        }
    }
    _on_sync = (function flx__on_sync (status) {
        if (_pyfunc_op_equals(status, "OK-refresh")) {
            location.reload();
        }
        return null;
    }).bind(this);

    sync_and_run("sys", _on_sync);
    _init_start_wiki_page = (function flx__init_start_wiki_page () {
        var _on_load;
        if ((_pyfunc_truthy(start_page) && ((!_pyfunc_op_equals(start_page, "None"))) && _pyfunc_op_equals(window.location.pathname, base_path))) {
            _on_load = (function flx__on_load (responseText, status, response) {
                console.log("_init_strart_wiki_page::_on_load");
                return null;
            }).bind(this);

            ajax_load(document.querySelector("#body_desktop"), _pyfunc_op_add(base_path, start_page) + "?only_content&schtml=1", _on_load);
        }
        return null;
    }).bind(this);

    window.init_start_wiki_page = _init_start_wiki_page;
    _init_start_wiki_page();
    if (_pyfunc_hasattr(window, "init_callback")) {
        window.init_callback();
    }
    jQuery.fn.editable.defaults.mode = "inline";
    jQuery.fn.combodate.defaults["maxYear"] = 2025;
    activate_menu();
    desktop = document.getElementById("body_desktop");
    if (_pyfunc_truthy(desktop)) {
        mount_html(desktop, null, null);
    }
    return null;
};

activate_menu = function flx_activate_menu () {
    var a, a_tab, div, event, href, id_elem, li, menu, pathname, pathname2, stub1_seq, stub2_itr, x;
    pathname = window.location.pathname;
    if (_pymeth_startswith.call(pathname, window.BASE_PATH)) {
        pathname2 = pathname.slice(window.BASE_PATH.length);
    } else {
        pathname2 = pathname;
    }
    if (_pyfunc_truthy(pathname2)) {
        menu = document.querySelector("sys-sidebarmenu");
        a_tab = Array.prototype.slice.call(document.querySelectorAll("a.menu-href"));
        stub1_seq = a_tab;
        if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
        for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
            a = stub1_seq[stub2_itr];
            if (_pyfunc_truthy(a.hasAttribute("href"))) {
                href = _pymeth_split.call(a.getAttribute("href"), "?")[0];
                if ((_pymeth_startswith.call(href, ("/" + pathname2)))) {
                    if (_pyfunc_truthy(menu)) {
                        li = a.closest("li.treeview");
                        if ((_pyfunc_truthy(li) && ((!_pyfunc_truthy(li.classList.contains("active")))))) {
                            a = li.querySelector("a");
                            if (_pyfunc_truthy(a)) {
                                event = document.createEvent("MouseEvents");
                                event.initMouseEvent("click", true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null);
                                a.dispatchEvent(event);
                            }
                        }
                    } else {
                        div = a.closest(".tab-tab");
                        if (_pyfunc_truthy(div)) {
                            id_elem = "a_" + div.id;
                            x = document.getElementById(id_elem);
                            if (_pyfunc_truthy(x)) {
                                (jQuery(x).tab)("show");
                            }
                        }
                    }
                }
            }
        }
    }
    return null;
};

_on_error = function flx__on_error (request, settings) {
    var end, start;
    if (_pyfunc_truthy(window.WAIT_ICON)) {
        window.WAIT_ICON.stop();
        window.WAIT_ICON = null;
    }
    if (_pyfunc_truthy(window.WAIT_ICON2)) {
        (jQuery("#loading-indicator").hide)();
        window.WAIT_ICON2 = false;
    }
    if (_pyfunc_op_equals(settings.status, 200)) {
        return null;
    }
    if (_pyfunc_truthy(settings.responseText)) {
        start = settings.responseText.indexOf("<body>");
        end = settings.responseText.lastIndexOf("</body>");
        if (((start > 0) && (end > 0))) {
            mount_html(jQuery("#dialog-data-error"), settings.responseText.substring(start + 6, end - 1));
            (jQuery("#dialog-form-error").modal)();
        } else {
            mount_html(jQuery("#dialog-data-error"), settings.responseText);
            (jQuery("#dialog-form-error").modal)();
        }
    }
    return null;
};

jquery_ready = function flx_jquery_ready () {
    return null;
};

_on_popstate = function (e) {
    var menu, x;
    if (_pyfunc_truthy(e.state)) {
        window.PUSH_STATE = false;
        if (_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "modern")) {
            menu = (get_menu().activate)(e.state, false);
        } else {
            x = e.state;
            mount_html(jQuery("#body_desktop"), LZString.decompress(x[0]));
            window.ACTIVE_PAGE = new Page(0, jQuery("#body_desktop"));
            window.ACTIVE_PAGE.set_href(document.location);
            if (_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "standard")) {
                (jQuery("a.menu-href").removeClass)("btn-warning");
                (jQuery("#" + x[1]).addClass)("btn-warning");
            }
        }
        window.PUSH_STATE = true;
    } else if (_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "modern")) {
    } else {
        mount_html(jQuery("#body_desktop"), "", false, false);
        window.ACTIVE_PAGE = null;
        if (_pyfunc_op_equals(window.APPLICATION_TEMPLATE, "standard")) {
            (jQuery("a.menu-href").removeClass)("btn-warning");
        }
    }
    return null;
};

window.addEventListener("popstate", _on_popstate, false);
export {dom_content_loaded, app_init, activate_menu, jquery_ready};

