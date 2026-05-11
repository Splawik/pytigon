

var DELETE_FOOTER, EDIT_FOOTER, ERROR_FOOTER, INFO_FOOTER, INLINE, INLINE_BASE, INLINE_DELETE, INLINE_DELETE_BASE, INLINE_EDIT, INLINE_ERROR, INLINE_INFO, MODAL, MODAL_BASE, MODAL_DELETE, MODAL_DELETE_BASE, MODAL_EDIT, MODAL_ERROR, MODAL_INFO, _CANCEL, _CLOSE, _COPY_TO_CLIP;
"\nHTML template resources for modal and inline dialogs.\n\nDefines base HTML templates for various dialog types (modal and inline)\nused throughout the application. Each template type has a corresponding\nfooter with action buttons (OK, Cancel, Close, Copy to clipboard).\n\nTemplate types:\n    MODAL, MODAL_EDIT, MODAL_INFO, MODAL_DELETE, MODAL_ERROR\n    INLINE, INLINE_EDIT, INLINE_INFO, INLINE_DELETE, INLINE_ERROR\n";
if (_pyfunc_hasattr(window, "gettext")) {
    _CANCEL = gettext("Cancel");
    _CLOSE = gettext("Close");
    _COPY_TO_CLIP = gettext("Copy to clipboard");
} else {
    _CANCEL = "Cancel";
    _CLOSE = "Close";
    _COPY_TO_CLIP = "Copy to clipboard";
}
MODAL = "\n    <div class=\"dialog-data\"></div>\n";
MODAL_BASE = _pymeth_replace.call((("\n<div class=\"dialog-form modal\" role=\"dialog\" title=\"{title}\">\n    <div class=\"ajax-region modal-dialog\" role=\"document\" data-region='(page)(page-content)'>\n        <div class=\"modal-content ajax-region\" data-region=\"error\">\n            <div class=\"modal-header\">\n                <h5 class=\"modal-title\" id=\"ModalLabel\">{title}</h5>\n                <button type=\"button\" class=\"close btn-close\" data-dismiss='modal' data-bs-dismiss='modal' aria-label=\"Close\"></button>\n            </div>\n            <div class=\"modal-body\">\n                <div class=\"container-fluid ajax-frame ajax-link win-content form-and-details\" data-region='page' href='{href}'>\n                    <div class=\"form-without-details d-flex flex-grow-1 flex-column\">\n                        <div class=\"dialog-data ajax-frame\" data-region=\"error\"></div>\n                    </div>\n                </div>\n            </div>\n            <div class=\"modal-footer\">\n                {{modal_footer}}\n            </div>\n        </div>\n    </div>\n</div>\n")), "Close", _CLOSE);
MODAL_DELETE_BASE = _pymeth_replace.call((("\n<div class=\"dialog-form modal\" role=\"dialog\" title=\"{title}\">\n    <div class=\"ajax-region modal-dialog\" role=\"document\" data-region='(page)(page-content)'>\n        <div class=\"modal-header\">\n            <h5 class=\"modal-title\" id=\"ModalLabel\">{title}</h5>\n            <button type=\"button\" class=\"close btn-close\" data-dismiss='modal' data-bs-dismiss='modal' aria-label=\"Close\"></button>\n        </div>\n        <div class=\"modal-body\">\n            <div class=\"container-fluid\">\n                <div class=\"dialog-data ajax-frame\" data-region=\"error\"></div>\n            </div>\n        </div>\n        <div class=\"modal-footer\">\n            {{modal_footer}}\n        </div>\n    </div>\n</div>\n")), "Close", _CLOSE);
EDIT_FOOTER = _pymeth_replace.call((" \n<button type=\"button\" class=\"btn btn-secondary ptig-btn-close\" data-dismiss='modal' data-bs-dismiss='modal'>Cancel</button>\n<button type=\"button\" class=\"btn btn-primary\" data-region=\"page-content\" target=\"close_frame\">OK</button>\n"), "Cancel", _CANCEL);
INFO_FOOTER = _pymeth_replace.call(((_pymeth_replace.call(("\n<button type = \"button\" class =\"btn btn-info copy_to_clipboard\">Copy to clipboard</button>\n<button type = \"button\" class =\"btn btn-secondary ptig-btn-close\" data-dismiss='modal' data-bs-dismiss='modal'>Close</button>\n"), "Copy to clipboard", _COPY_TO_CLIP))), "Close", _CLOSE);
DELETE_FOOTER = _pymeth_replace.call(("\n<button type=\"button\" class=\"btn btn-secondary ptig-btn-close\" data-dismiss='modal' data-bs-dismiss='modal'>Cancel</button>\n<button type=\"button\" class=\"btn btn-danger\" data-region=\"page-content\" target=\"close_frame\">OK</button>\n"), "Cancel", _CANCEL);
ERROR_FOOTER = _pymeth_replace.call(("\n<button type=\"button\" class=\"btn btn-secondary ptig-btn-close\" data-dismiss='modal' data-bs-dismiss='modal'>Close</button>\n"), "Close", _CLOSE);
MODAL_EDIT = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", EDIT_FOOTER);
MODAL_INFO = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", INFO_FOOTER);
MODAL_DELETE = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", DELETE_FOOTER);
MODAL_ERROR = _pymeth_replace.call(MODAL_BASE, "{{modal_footer}}", ERROR_FOOTER);
INLINE = "\n    <div class=\"dialog-data\"></div>\n";
INLINE_BASE = _pymeth_replace.call((("\n<div class='inline-dialog-frame'>\n    <div class='dark_background'></div>\n    <div class='ajax-region modal-dialog modal-dialog-inline' role='document' data-region='(page)(page-content)'>\n        <div class=\"modal-content ajax-region inline-content\" data-region=\"error\">\n            <div class='modal-content2 d-flex flex-column' style='min-height: 50vh;'>\n                <div class='modal-header'>\n                    <h4 class='modal-title'>{title}</h4>\n                    <div class='dialog-buttons>\n                        <button type='button' class='btn btn-light btn-transparent minimize' onclick='inline_minimize(this)' style='display:none;'> \n                            <span class='fa fa-window-minimize'></span> \n                        </button> \n                        <button type='button' class='btn btn-light btn-transparent maximize' onclick='inline_maximize(this);return false;'> \n                            <span class='fa fa-window-maximize'></span> \n                        </button> \n                        <button type='button' class='close btn btn-light btn-transparent shadow-none ptig-btn-close' aria-label='Close'>\n                            <span class='fa fa-times'></span>\n                        </button>\n                    </div>\n                </div>\n                <div class='modal-body ajax-frame ajax-link d-flex flex-column win-content table-and-details' data-region='page' href='{href}'>\n                    <div class=\"table-without-details d-flex flex-grow-1 flex-column\">\n                        <div class='dialog-data ajax-frame d-flex flex-column flex-grow-1' data-region='error'></div>\n                    </div>\n                </div>\n                <div class='modal-footer'>\n                    {{modal_footer}}\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n")), "Close", _CLOSE);
INLINE_DELETE_BASE = _pymeth_replace.call("\n<div style='position:relative;z-index:1001;'>\n    <div class='dark_background'></div>\n    <div class='ajax-region modal-dialog modal-dialog-inline' role='document' data-region='(page)(page-content)'>\n        <div class='modal-content'>\n            <div class='modal-header'>\n                <h4 class='modal-title'>{title}</h4>\n                <div>\n                    <button type='button' class='btn btn-light btn-transparent minimize' onclick='inline_minimize(this)' style='display:none;'> \n                        <span class='fa fa-window-minimize'></span> \n                    </button> \n                    <button type='button' class='btn btn-light btn-transparent maximize' onclick='inline_maximize(this);return false;'> \n                        <span class='fa fa-window-maximize'></span> \n                    </button> \n                    <button type='button' class='close btn-close shadow-none ptig-btn-close' aria-label='Close'></button>\n                </div>\n            </div>\n            <div class='modal-body'>\n                <div class='dialog-data ajax-frame' data-region='error'></div>\n            </div>\n            <div class='modal-footer'>\n                {{modal_footer}}\n            </div>\n        </div>\n    </div>\n</div>\n", "Close", _CLOSE);
INLINE_EDIT = _pymeth_replace.call(((_pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", EDIT_FOOTER), "data-dismiss='modal'", ""))), "data-bs-dismiss='modal'", "");
INLINE_INFO = _pymeth_replace.call(((_pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", INFO_FOOTER), "data-dismiss='modal'", ""))), "data-bs-dismiss='modal'", "");
INLINE_DELETE = _pymeth_replace.call(((_pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", DELETE_FOOTER), "data-dismiss='modal'", ""))), "data-bs-dismiss='modal'", "");
INLINE_ERROR = _pymeth_replace.call(((_pymeth_replace.call(_pymeth_replace.call(INLINE_BASE, "{{modal_footer}}", ERROR_FOOTER), "data-dismiss='modal'", ""))), "data-bs-dismiss='modal'", "");

var LOADED_FILES, Loading, TEMPLATES, _OPERATOR, _req_post, add_param2url, ajax_get, ajax_json, ajax_post, ajax_submit, animate_combo, can_popup, correct_href, download_binary_file, element_get_url, element_set_url, frontend_view, get_elem_from_string, get_page, get_table_type, get_template, history_push_state, inline_maximize, inline_minimize, is_hidden, is_visible, join_urls, load_css, load_js, load_many_js, on_load_js, process_resize, remove_element, remove_page_from_href, save_as, send_to_dom, standard_error_handler, super_insert, super_query_selector;
"\nUtility functions and helper classes for the Pytigon client-side framework.\n\nProvides:\n- Loading indicators (Ladda buttons and global spinner).\n- AJAX communication (GET, POST, JSON, form submit, file upload).\n- Dynamic JS/CSS loading with dependency tracking.\n- DOM manipulation helpers (query, insert, remove, resize).\n- URL manipulation (correct_href, join_urls, history push state).\n- Template rendering and dialog positioning.\n- File download and error handling.\n";
LOADED_FILES = ({});
Loading = function () {
    // Manage loading indicators for AJAX operations.
    // 
    //     Supports two modes:
    //     - 'ladda': Ladda button animation on the triggering element.
    //     - 'global': A global loading-indicator element.
    // 
    //     Usage::
    // 
    //         loading = Loading(element)
    //         loading.create()
    //         loading.start()
    //         # ... async operation ...
    //         loading.stop()
    //         loading.remove()
    _pyfunc_op_instantiate(this, arguments);
}
Loading.prototype._base_class = Object;
Loading.prototype.__name__ = "Loading";

Loading.prototype.__init__ = function (element) {
    var loading_indicator;
    // Initialize the loading manager for a given element.
    // 
    //         Detects whether to use Ladda (if the element has .ladda-button)
    //         or the global loading indicator.
    // 
    //         Args:
    //             element: The DOM element that triggered the operation.
    this.load_type = null;
    if ((_pyfunc_hasattr(element, "data") && (_pyfunc_truthy(_pyfunc_getattr(element, "data"))))) {
        this.element = _pyfunc_getattr(element, "data");
    } else {
        this.element = element;
    }
    if (_pyfunc_truthy(this.element)) {
        if (_pyfunc_truthy(this.element.classList.contains("ladda-button"))) {
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
    // Create the Ladda instance if in ladda mode.
    if (_pyfunc_op_equals(this.load_type, "ladda")) {
        this.ladda = window.Ladda.create(this.element);
    }
    return null;
};

Loading.prototype.start = function () {
    // Start the loading animation.
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.start();
    } else if (_pyfunc_op_equals(this.load_type, "global")) {
        this.loading_indicator.style.display = "block";
    }
    return null;
};

Loading.prototype.set_progress = function (progress) {
    // Update the Ladda progress bar.
    // 
    //         Args:
    //             progress: Progress value between 0 and 1.
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.setProgress(progress);
    }
    return null;
};

Loading.prototype.stop = function () {
    // Stop the loading animation.
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.stop();
    } else if (_pyfunc_op_equals(this.load_type, "global")) {
        this.loading_indicator.style.display = "none";
    }
    return null;
};

Loading.prototype.remove = function () {
    // Remove the Ladda instance and clean up.
    if ((_pyfunc_op_equals(this.load_type, "ladda") && _pyfunc_truthy(this.ladda))) {
        this.ladda.remove();
        this.ladda = null;
    }
    return null;
};


save_as = function flx_save_as (blob, file_name) {
    var _, anchor_elem, url;
    // Trigger a file download in the browser.
    // 
    //     Creates a temporary anchor element with a blob URL, clicks it,
    //     and cleans up after a short delay.
    // 
    //     Args:
    //         blob: Blob or File object to download.
    //         file_name: Suggested file name for the download.
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

standard_error_handler = function flx_standard_error_handler (req) {
    var _on_reader_load, reader;
    // Display a standard error dialog for failed AJAX requests.
    // 
    //     For 500 errors: opens the response in a new window.
    //     For other errors: shows a SweetAlert2 error dialog.
    // 
    //     Args:
    //         req: The XMLHttpRequest object with .status and .response.
    if ((!_pyfunc_op_equals(req.status, 200))) {
        reader = new FileReader();
        _on_reader_load = (function flx__on_reader_load () {
            if (_pyfunc_op_equals(req.status, 500)) {
                console.log(reader.result);
                (window.open().document.write)(reader.result);
            } else {
                Swal.fire(({icon: "error", title: _pymeth_format.call("Error: {:d}", req.status), text: reader.result}));
            }
            return null;
        }).bind(this);

        reader.onload = _on_reader_load;
        reader.readAsText(req.response);
    }
    return null;
};

window.standard_error_handler = standard_error_handler;
download_binary_file = function flx_download_binary_file (buf, content_disposition) {
    var file_name, pos, stub1_seq, stub2_itr, var_list;
    // Download a binary file from a server response.
    // 
    //     Parses the Content-Disposition header to extract the filename.
    // 
    //     Args:
    //         buf: Binary blob data.
    //         content_disposition: Content-Disposition header string.
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

frontend_view = function flx_frontend_view (url, complete, callback_on_error, param) {
    var _callback, param2, url2, x;
    callback_on_error = (callback_on_error === undefined) ? null: callback_on_error;
    param = (param === undefined) ? null: param;
    // Render a frontend view (.fview) URL.
    // 
    //     Loads the corresponding .js module, invokes its request function
    //     with parameters, and optionally renders a Nunjucks template.
    // 
    //     Args:
    //         url: The .fview URL to process.
    //         complete: Callback receiving the rendered result.
    //         callback_on_error: Optional error callback.
    //         param: Optional parameters for the view.
    url2 = window.process_href(_pymeth_replace.call(url, ".fview", ".js"), null);
    param2 = param;
    if (_pyfunc_truthy(param)) {
        param2 = window.getParamsFromEncodedParams(param);
    } else if (_pyfunc_op_contains("?", url)) {
        param2 = window.getParamsFromUrl(url);
    }
    _callback = (function flx__callback (module) {
        var _callback2, r;
        _callback2 = (function flx__callback2 (context) {
            var _callback3, template;
            if ((((_pyfunc_op_equals(jQuery.type(context), "object"))) && _pyfunc_truthy(context["template"]))) {
                _callback3 = (function flx__callback3 (template_str) {
                    var res;
                    res = window.nunjucks.renderString(template_str, context);
                    complete(res);
                    return null;
                }).bind(this);

                template = context["template"];
                if (_pyfunc_op_equals(template, ".")) {
                    template = _pymeth_replace.call(url, ".fview", ".html");
                }
                ajax_get(template, _callback3);
            } else {
                complete(context);
            }
            return null;
        }).bind(this);

        if (((_pyfunc_truthy(window.hasOwnProperty("cordova"))) || _pyfunc_op_equals(location.protocol, "file:"))) {
            r = eval(_pymeth_replace.call(module, "export", ""));
            r(param2, _callback2);
        } else {
            module["request"](param2, _callback2);
        }
        return null;
    }).bind(this);

    if (((_pyfunc_truthy(window.hasOwnProperty("cordova"))) || _pyfunc_op_equals(location.protocol, "file:"))) {
        ajax_get(url2, _callback, callback_on_error);
    } else {
        x = window.dynamic_import(url2, _callback);
    }
    return null;
};

ajax_get = function flx_ajax_get (url, complete, callback_on_error, process_req) {
    var _onload, process_blob, req;
    callback_on_error = (callback_on_error === undefined) ? null: callback_on_error;
    process_req = (process_req === undefined) ? null: process_req;
    // Perform an AJAX GET request.
    // 
    //     Handles .fview URLs via frontend_view, binary downloads, redirects,
    //     and standard text responses.
    // 
    //     Args:
    //         url: The URL to fetch.
    //         complete: Callback receiving the response text.
    //         callback_on_error: Optional error callback.
    //         process_req: Optional callback to configure the XHR before send.
    // 
    //     Returns:
    //         The XMLHttpRequest object.
    if (_pyfunc_op_contains(".fview", url)) {
        return frontend_view(url, complete, callback_on_error, null);
    }
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
        if ((!_pyfunc_op_equals(req.status, 200))) {
            if (_pyfunc_truthy(callback_on_error)) {
                callback_on_error(req);
            } else {
                standard_error_handler(req);
            }
            return null;
        }
        if ((!_pyfunc_truthy(req.response))) {
            complete(req.responseText);
        } else if (_pyfunc_truthy(process_blob)) {
            disp = req.getResponseHeader("Content-Disposition");
            if ((_pyfunc_truthy(disp) && _pyfunc_op_contains("attachment", disp))) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                reader = new FileReader();
                _on_reader_load = (function flx__on_reader_load () {
                    var _complete2, url2data;
                    if ((((!_pyfunc_op_equals(req.status, 200))) && ((!_pyfunc_op_equals(req.status, 0))))) {
                        console.log(reader.result);
                        (window.open().document.write)(reader.result);
                        complete("Error - details on new page");
                    } else {
                        if (_pyfunc_op_equals(disp, "redirect")) {
                            url2data = _pymeth_split.call(reader.result, "|");
                            _complete2 = (function flx__complete2 (data) {
                                var _callback_next, element, next_href, next_target, query;
                                element = complete(data);
                                if (_pyfunc_truthy(element)) {
                                    next_href = url2data[1];
                                    next_target = url2data[2];
                                    query = url2data[3];
                                    element = element.querySelector(query);
                                    _callback_next = (function flx__callback_next (data) {
                                        var s, t;
                                        if (_pymeth_startswith.call(next_target, "inline")) {
                                            t = _pymeth_replace.call(next_target, "inline", "");
                                            if (_pyfunc_op_equals(t, "_info")) {
                                                s = "INLINE_INFO";
                                            } else if (_pyfunc_op_equals(t, "_delete")) {
                                                s = "INLINE_DELETE";
                                            } else if (_pyfunc_op_equals(t, "_edit")) {
                                                s = "INLINE_EDIT";
                                            } else {
                                                s = "INLINE";
                                            }
                                            return window._on_inline(element, get_elem_from_string(data), next_href, ({}), null, s);
                                        } else if (_pymeth_startswith.call(next_target, "popup")) {
                                            t = _pymeth_replace.call(next_target, "popup", "");
                                            if (_pyfunc_op_equals(t, "_info")) {
                                                s = "MODAL_INFO";
                                            } else if (_pyfunc_op_equals(t, "_delete")) {
                                                s = "MODAL_DELETE";
                                            } else if (_pyfunc_op_equals(t, "_edit")) {
                                                s = "MODAL_EDIT";
                                            } else {
                                                s = "MODAL";
                                            }
                                            return window._on_popup(element, get_elem_from_string(data), next_href, ({}), null, s);
                                        } else {
                                            return window.on_new_tab(element, get_elem_from_string(data), next_href, ({}), null);
                                        }
                                        return null;
                                    }).bind(this);

                                    ajax_get(next_href, _callback_next);
                                }
                                return element;
                            }).bind(this);

                            return ajax_get(url2data[0], _complete2);
                        }
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
    return req;
};

window.ajax_get = ajax_get;
_req_post = function flx__req_post (req, url, data, complete, callback_on_error, content_type) {
    var _onload, process_blob;
    callback_on_error = (callback_on_error === undefined) ? null: callback_on_error;
    content_type = (content_type === undefined) ? null: content_type;
    // Internal POST request handler.
    // 
    //     Handles .fview URLs, blob responses, and standard text responses.
    if (_pyfunc_op_contains(".fview", url)) {
        return frontend_view(url, complete, callback_on_error, data);
    }
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
        if ((!_pyfunc_op_contains(req.status, [200, 500]))) {
            if (_pyfunc_truthy(callback_on_error)) {
                callback_on_error(req);
            } else {
                standard_error_handler(req);
            }
            return null;
        }
        if ((!_pyfunc_truthy(req.response))) {
            complete(req.responseText);
        } else if (_pyfunc_truthy(process_blob)) {
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
        if ((!_pyfunc_op_equals(content_type, "pass"))) {
            req.setRequestHeader("Content-Type", content_type);
        }
    } else {
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    }
    req.send(data);
    return req;
};

ajax_post = function flx_ajax_post (url, data, complete, callback_on_error, process_req, content_type) {
    var req;
    process_req = (process_req === undefined) ? null: process_req;
    content_type = (content_type === undefined) ? null: content_type;
    // Perform an AJAX POST request.
    // 
    //     Args:
    //         url: The URL to post to.
    //         data: Form data string or FormData object.
    //         complete: Callback receiving the response text.
    //         callback_on_error: Error callback.
    //         process_req: Optional callback to configure the XHR before send.
    //         content_type: Content-Type header value, or 'pass' to skip.
    // 
    //     Returns:
    //         The XMLHttpRequest object.
    req = new XMLHttpRequest();
    if (_pyfunc_truthy(process_req)) {
        process_req(req);
    }
    _req_post(req, url, data, complete, callback_on_error, content_type);
    return req;
};

window.ajax_post = ajax_post;
ajax_json = function flx_ajax_json (url, data, complete, callback_on_error, process_req) {
    var _complete, data2;
    process_req = (process_req === undefined) ? null: process_req;
    // Perform an AJAX POST with JSON content type.
    // 
    //     Stringifies the data object and sends it as application/json.
    // 
    //     Args:
    //         url: The URL to post to.
    //         data: Data object to stringify and send.
    //         complete: Callback receiving the parsed JSON response.
    //         callback_on_error: Error callback.
    //         process_req: Optional XHR configuration callback.
    _complete = (function flx__complete (data_in) {
        var _data;
        try {
            _data = JSON.parse(data_in);
        } catch(err_3) {
            {
                _data = data_in;
            }
        }
        complete(_data);
        return null;
    }).bind(this);

    data2 = JSON.stringify(data);
    return ajax_post(url, data2, _complete, callback_on_error, null, "application/json");
};

window.ajax_json = ajax_json;
ajax_submit = function flx_ajax_submit (_form, complete, callback_on_error, data_filter, process_req, url) {
    var _progressHandlingFunction, content_type, data, form, pair, req, stub3_seq, stub4_itr;
    callback_on_error = (callback_on_error === undefined) ? null: callback_on_error;
    data_filter = (data_filter === undefined) ? null: data_filter;
    process_req = (process_req === undefined) ? null: process_req;
    url = (url === undefined) ? null: url;
    // Submit a form via AJAX with automatic file upload detection.
    // 
    //     If the form contains file inputs, uses FormData with progress tracking.
    //     Otherwise, serializes the form data.
    // 
    //     Args:
    //         _form: The form DOM element.
    //         complete: Callback receiving the response.
    //         callback_on_error: Error callback.
    //         data_filter: Optional function to transform form data before send.
    //         process_req: Optional XHR configuration callback.
    //         url: Optional override URL (falls back to form action).
    content_type = null;
    req = new XMLHttpRequest();
    form = jQuery(_form);
    if (_pyfunc_truthy(process_req)) {
        process_req(req);
    }
    if (((_pymeth_find.call(form, "[type='file']").length) > 0)) {
        _form.setAttribute("enctype", "multipart/form-data");
        data = new FormData(_form);
        if (_pyfunc_truthy(data_filter)) {
            data = data_filter(data);
        }
        content_type = "pass";
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
        stub3_seq = data.entries();
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            pair = stub3_seq[stub4_itr];
            console.log(((pair[0] + ": ") + pair[1]));
        }
    } else {
        data = form.serialize();
        if (_pyfunc_truthy(data_filter)) {
            data = data_filter(data);
        }
    }
    if (_pyfunc_truthy(url)) {
        return _req_post(req, url, data, complete, callback_on_error, content_type);
    } else {
        return _req_post(req, correct_href(form.attr("action"), [_form[0]]), data, complete, callback_on_error, content_type);
    }
    return null;
};

window.ajax_submit = ajax_submit;
load_css = function flx_load_css (path, on_load) {
    var _onload, req;
    on_load = (on_load === undefined) ? null: on_load;
    // Dynamically load a CSS file.
    // 
    //     Prevents duplicate loads by tracking loaded files. If no on_load
    //     callback is provided, injects a <style> tag into <head>.
    // 
    //     Args:
    //         path: URL of the CSS file.
    //         on_load: Optional callback receiving the XHR on load.
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
    var fun, functions, stub5_seq, stub6_itr;
    // Execute callbacks registered for a loaded JS file.
    // 
    //     Args:
    //         path: URL of the JS file that was loaded.
    if ((_pyfunc_truthy(LOADED_FILES) && _pyfunc_op_contains(path, LOADED_FILES))) {
        functions = LOADED_FILES[path];
        if (_pyfunc_truthy(functions)) {
            stub5_seq = functions;
            if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
            for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
                fun = stub5_seq[stub6_itr];
                fun();
            }
        }
        LOADED_FILES[path] = null;
    }
    return null;
};

load_js = function flx_load_js (path, fun) {
    var _onload, req;
    // Dynamically load a JavaScript file and execute a callback.
    // 
    //     Supports deduplication: if already loading, queues the callback.
    //     If already loaded, executes immediately.
    // 
    //     Args:
    //         path: URL of the JS file to load.
    //         fun: Callback to execute after the script loads.
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
    var _fun, counter, next_step, path, stub7_seq, stub8_itr;
    // Load multiple JS files in order, executing a callback when all done.
    // 
    //     Supports the '|' separator to create loading groups: files before '|'
    //     are loaded before those after.
    // 
    //     Args:
    //         paths: List of JS file URLs. May contain '|' as a stage separator.
    //         fun: Callback executed after all files are loaded.
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

    stub7_seq = paths;
    if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
    for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
        path = stub7_seq[stub8_itr];
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
    // Push a state entry to the browser history.
    // 
    //     Converts the URL to a subpage query parameter format.
    // 
    //     Args:
    //         title: History entry title.
    //         url: URL for the history entry.
    //         data: Optional data tuple [html_content, element_id] for state restoration.
    if ((((!_pyfunc_truthy(url))) || _pyfunc_op_equals(url, "/"))) {
        url2 = url;
    } else {
        url2 = "?subpage=" + ((new URL(url, "http://127.0.0.1")).pathname);
    }
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
    // Create a DOM element from an HTML string.
    // 
    //     Wraps the HTML in a temporary div.ajax-temp-item.
    // 
    //     Args:
    //         html: HTML string to parse.
    //         selectors: Optional CSS selector to extract a specific child.
    // 
    //     Returns:
    //         A DOM element or the temporary container if multiple children.
    temp = document.createElement("div");
    temp.classList.add("ajax-temp-item");
    temp.innerHTML = html;
    if (_pyfunc_truthy(selectors)) {
        element = temp.querySelector(selectors);
        return element;
    } else if ((temp.childNodes.length == 1)) {
        return temp.childNodes[0];
    } else {
        return temp;
    }
    return null;
};

window.get_elem_from_string = get_elem_from_string;
animate_combo = function flx_animate_combo (button, obj1, obj2, obj1_style_off, obj1_style_on, obj2_style_off, obj2_style_on, speed, end) {
    var _animate, end2;
    end = (end === undefined) ? null: end;
    // Toggle animation between two states for paired elements.
    // 
    //     When the button is clicked, toggles between 'on' and 'off' states,
    //     animating obj1 and obj2 with CSS transitions.
    // 
    //     Args:
    //         button: jQuery button element that toggles the state.
    //         obj1: First jQuery element to animate.
    //         obj2: Second jQuery element to animate.
    //         obj1_style_off: CSS properties for obj1 when button is OFF.
    //         obj1_style_on: CSS properties for obj1 when button is ON.
    //         obj2_style_off: CSS properties for obj2 when button is OFF.
    //         obj2_style_on: CSS properties for obj2 when button is ON.
    //         speed: Animation duration or None for instant.
    //         end: Optional callback after animation completes.
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
            if (_pyfunc_truthy(speed)) {
                obj1.animate(obj1_style_off, speed);
            } else {
                obj1.css(obj1_style_off);
            }
            obj1.removeClass("off");
            obj1.addClass("on");
            if (_pyfunc_truthy(speed)) {
                obj2.animate(obj2_style_off, speed, "linear", end2);
            } else {
                obj2.css(obj2_style_off);
                end2();
            }
            obj2.removeClass("on");
            obj2.addClass("off");
        } else {
            button.addClass("on");
            if (_pyfunc_truthy(speed)) {
                obj1.animate(obj1_style_on, speed);
            } else {
                obj1.css(obj1_style_on);
            }
            obj1.removeClass("on");
            obj1.addClass("off");
            if (_pyfunc_truthy(speed)) {
                obj2.animate(obj2_style_on, speed, "linear", end2);
            } else {
                obj2.css(obj2_style_on);
                end2();
            }
            obj2.removeClass("off");
            obj2.addClass("on");
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
    // Check if an element is hidden via computed style.
    // 
    //     Args:
    //         el: DOM element.
    // 
    //     Returns:
    //         bool: True if display:none.
    style = window.getComputedStyle(el);
    return _pyfunc_op_equals(style.display, "none");
};

window.is_hidden = is_hidden;
is_visible = function flx_is_visible (el) {
    // Check if an element is visible.
    // 
    //     Args:
    //         el: DOM element.
    // 
    //     Returns:
    //         bool: True if not hidden.
    return !_pyfunc_truthy(is_hidden(el));
};

window.is_visible = is_visible;
TEMPLATES = ({MODAL_EDIT: MODAL_EDIT, MODAL_INFO: MODAL_INFO, MODAL_DELETE: MODAL_DELETE, MODAL_ERROR: MODAL_ERROR, INLINE_EDIT: INLINE_EDIT, INLINE_INFO: INLINE_INFO, INLINE_DELETE: INLINE_DELETE, INLINE_ERROR: INLINE_ERROR});
get_template = function flx_get_template (template_name, param) {
    var ret;
    // Get a rendered template string with parameter substitution.
    // 
    //     Replaces {title} and {href} placeholders in the template.
    // 
    //     Args:
    //         template_name: Key into the TEMPLATES dict.
    //         param: Dict with 'title' and optionally 'href' keys.
    // 
    //     Returns:
    //         str: The rendered template, or None if template not found.
    if (_pyfunc_op_contains(template_name, TEMPLATES)) {
        ret = _pymeth_replace.call(TEMPLATES[template_name], "{title}", param["title"]);
        if (_pyfunc_op_contains("href", param)) {
            ret = _pymeth_replace.call(ret, "{href}", param["href"]);
        }
        return ret;
    }
    return null;
};

super_query_selector = function flx_super_query_selector (element, selector) {
    var e, pos, stub10_itr, stub9_seq, x;
    // Enhanced query selector with path-like syntax.
    // 
    //     Supports special path segments:
    //     - '..' : parent element
    //     - '.'  : current element (no-op)
    //     - '^selector' : closest ancestor matching selector
    //     - 'selector' : querySelector
    // 
    //     Multiple segments are separated by '/'.
    // 
    //     Args:
    //         element: Starting DOM element.
    //         selector: Path string (e.g. '../div.content/^.modal').
    // 
    //     Returns:
    //         The matched element or None.
    x = _pymeth_split.call(selector, "/");
    e = element;
    stub9_seq = x;
    if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
    for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
        pos = stub9_seq[stub10_itr];
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
    var c, element, selector2, stub11_seq, stub12_itr, x;
    // Insert an element relative to a target using a position selector.
    // 
    //     Selector format: 'path:position' where position is one of:
    //     - 'overwrite' / '>' : replace content
    //     - 'append_first' / '<<' : insert as first child
    //     - 'append' / '>>' : append as last child
    //     - 'after' / ')' : insert after target
    //     - 'before' / '(' : insert before target
    //     - 'class' : copy classes from inserted to target
    // 
    //     Args:
    //         base_element: Starting DOM element.
    //         insert_selector: Position selector string.
    //         inserted_element: Element to insert.
    // 
    //     Returns:
    //         The target element or None if not found.
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
        stub11_seq = Array.prototype.slice.call(inserted_element.classList);
        if ((typeof stub11_seq === "object") && (!Array.isArray(stub11_seq))) { stub11_seq = Object.keys(stub11_seq);}
        for (stub12_itr = 0; stub12_itr < stub11_seq.length; stub12_itr += 1) {
            c = stub11_seq[stub12_itr];
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
    var html, insert_selector, inserted_element, operator, stub13_seq, stub14_itr, x;
    // Parse HTML text and insert it into the DOM based on position markers.
    // 
    //     If the HTML contains ===operator followed by a selector, inserts
    //     the parsed content at the specified position relative to base_elem.
    // 
    //     Args:
    //         html_text: HTML string possibly containing ===operator markers.
    //         base_elem: Base element for relative insertion.
    // 
    //     Returns:
    //         The result of super_insert, or None if no operator found.
    stub13_seq = _OPERATOR;
    if ((typeof stub13_seq === "object") && (!Array.isArray(stub13_seq))) { stub13_seq = Object.keys(stub13_seq);}
    for (stub14_itr = 0; stub14_itr < stub13_seq.length; stub14_itr += 1) {
        operator = stub13_seq[stub14_itr];
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
    var _on_remove, _on_remove_aside, element2, elements, stub15_seq, stub16_itr;
    // Remove an element from the DOM with cleanup callbacks.
    // 
    //     Handles:
    //     - .call_on_remove callbacks before removal.
    //     - .plug elements with modal dialogs (hides modals first).
    //     - String selectors (removes all matches).
    // 
    //     Args:
    //         element: DOM element, or CSS selector string.
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
        stub15_seq = elements;
        if ((typeof stub15_seq === "object") && (!Array.isArray(stub15_seq))) { stub15_seq = Object.keys(stub15_seq);}
        for (stub16_itr = 0; stub16_itr < stub15_seq.length; stub16_itr += 1) {
            element2 = stub15_seq[stub16_itr];
            jQuery.each(_pymeth_find.call(jQuery(element2), ".call_on_remove"), _on_remove);
            _on_remove_aside = (function flx__on_remove_aside (index, value) {
                var d, dialog;
                dialog = value.firstElementChild;
                if ((_pyfunc_truthy(dialog) && (_pyfunc_truthy(dialog.hasAttribute("modal"))))) {
                    if (_pyfunc_truthy(window.hasOwnProperty("bootstrap"))) {
                        d = new bootstrap.Modal(dialog);
                        d.hide();
                    } else {
                        (jQuery(dialog).modal)("hide");
                    }
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
    var body_rect, elem, elem_rect, elements, elements1, elements2, elements3, h, param, parent_rect, size_desc, size_style, stub17_seq, stub18_itr, stub19_seq, stub20_itr;
    // Process resize events for flexible_size elements.
    // 
    //     Calculates viewport dimensions and element offsets, then triggers
    //     size adjustments on elements with .flexible_size or
    //     .flexible_size_round2 classes, either via their process_resize
    //     callback or by applying data-size attribute formatting.
    // 
    //     Args:
    //         target_element: Root element to scan for resizable children.
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
    stub19_seq = [elements1, elements2, elements3];
    if ((typeof stub19_seq === "object") && (!Array.isArray(stub19_seq))) { stub19_seq = Object.keys(stub19_seq);}
    for (stub20_itr = 0; stub20_itr < stub19_seq.length; stub20_itr += 1) {
        elements = stub19_seq[stub20_itr];
        stub17_seq = elements;
        if ((typeof stub17_seq === "object") && (!Array.isArray(stub17_seq))) { stub17_seq = Object.keys(stub17_seq);}
        for (stub18_itr = 0; stub18_itr < stub17_seq.length; stub18_itr += 1) {
            elem = stub17_seq[stub18_itr];
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
    // Get the closest .tab-pane ancestor of an element.
    // 
    //     Args:
    //         elem: jQuery element.
    // 
    //     Returns:
    //         jQuery element matching .tab-pane.
    if (_pyfunc_truthy(elem.hasClass(".tab-pane"))) {
        return elem;
    } else {
        return elem.closest(".tab-pane");
    }
    return null;
};

get_table_type = function flx_get_table_type (elem) {
    var ret, tabsort;
    // Detect the table_type attribute from a .tabsort element.
    // 
    //     Searches within the element and its parent page.
    // 
    //     Args:
    //         elem: jQuery element.
    // 
    //     Returns:
    //         str: The table_type value, or empty string.
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

window.get_table_type = get_table_type;
can_popup = function flx_can_popup () {
    // Check if a modal popup can be opened (no existing modal is open).
    // 
    //     Returns:
    //         bool: True if no .modal-open element exists.
    if (((jQuery(".modal-open").length) > 0)) {
        return false;
    } else {
        return true;
    }
    return null;
};

correct_href = function flx_correct_href (href, elements) {
    var element, only_content, only_table, stub21_seq, stub22_itr, stub23_seq, stub24_itr, stub25_seq, stub26_itr;
    elements = (elements === undefined) ? null: elements;
    // Add fragment parameters to a URL based on element context.
    // 
    //     Automatically appends:
    //     - 'fragment=table-content' for table region elements.
    //     - 'fragment=page-content' for other elements.
    //     - Custom get-param attributes from elements.
    // 
    //     Args:
    //         href: The URL to modify.
    //         elements: Tuple of DOM elements providing context.
    // 
    //     Returns:
    //         str: The modified URL.
    if ((!_pyfunc_truthy(href))) {
        return href;
    }
    if (_pyfunc_op_contains("fragment=", href)) {
        return href;
    }
    only_table = false;
    if ((!_pyfunc_op_equals(elements, null))) {
        stub21_seq = elements;
        if ((typeof stub21_seq === "object") && (!Array.isArray(stub21_seq))) { stub21_seq = Object.keys(stub21_seq);}
        for (stub22_itr = 0; stub22_itr < stub21_seq.length; stub22_itr += 1) {
            element = stub21_seq[stub22_itr];
            if ((((!_pyfunc_op_equals(element, null))) && (_pyfunc_truthy(element.hasAttribute("data-region"))) && ((_pyfunc_op_contains("table", (_pymeth_lower.call(element.getAttribute("data-region")))))))) {
                only_table = true;
            }
        }
    }
    if (_pyfunc_truthy(only_table)) {
        if (_pyfunc_op_contains("?", href)) {
            href += "&fragment=table-content";
        } else {
            href += "?fragment=table-content";
        }
    } else {
        only_content = true;
        if ((!_pyfunc_op_equals(elements, null))) {
            stub23_seq = elements;
            if ((typeof stub23_seq === "object") && (!Array.isArray(stub23_seq))) { stub23_seq = Object.keys(stub23_seq);}
            for (stub24_itr = 0; stub24_itr < stub23_seq.length; stub24_itr += 1) {
                element = stub23_seq[stub24_itr];
                if ((((!_pyfunc_op_equals(element, null))) && (_pyfunc_truthy(element.hasAttribute("target"))) && ((_pyfunc_op_contains((_pymeth_lower.call(element.getAttribute("target"))), ["_top", "_blank"]))))) {
                    only_content = false;
                }
            }
        }
        if (_pyfunc_truthy(only_content)) {
            if (_pyfunc_op_contains("?", href)) {
                href += "&fragment=page-content";
            } else {
                href += "?fragment=page-content";
            }
        }
    }
    if ((!_pyfunc_op_equals(elements, null))) {
        stub25_seq = elements;
        if ((typeof stub25_seq === "object") && (!Array.isArray(stub25_seq))) { stub25_seq = Object.keys(stub25_seq);}
        for (stub26_itr = 0; stub26_itr < stub25_seq.length; stub26_itr += 1) {
            element = stub25_seq[stub26_itr];
            if ((_pyfunc_truthy(element) && (_pyfunc_truthy(element.hasAttribute("get-param"))) && (_pyfunc_truthy(element.getAttribute("get-param"))))) {
                if ((!(_pyfunc_op_contains(element.getAttribute("get-param"), href)))) {
                    if (_pyfunc_op_contains("?", href)) {
                        href = _pyfunc_op_add(href, "&" + element.getAttribute("get-param"));
                    } else {
                        href = _pyfunc_op_add(href, "?" + element.getAttribute("get-param"));
                    }
                }
            }
        }
    }
    return href;
};

remove_page_from_href = function flx_remove_page_from_href (href) {
    var pos, stub27_seq, stub28_itr, x, x2, x3;
    // Remove 'page=' parameter from a URL.
    // 
    //     Args:
    //         href: URL string.
    // 
    //     Returns:
    //         str: URL without page parameters.
    x = _pymeth_split.call(href, "?");
    if ((x.length > 1)) {
        x2 = _pymeth_split.call(x[1], "&");
        if ((x2.length > 1)) {
            x3 = [];
            stub27_seq = x2;
            if ((typeof stub27_seq === "object") && (!Array.isArray(stub27_seq))) { stub27_seq = Object.keys(stub27_seq);}
            for (stub28_itr = 0; stub28_itr < stub27_seq.length; stub28_itr += 1) {
                pos = stub27_seq[stub28_itr];
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

inline_maximize = function flx_inline_maximize (elem) {
    var b_max, b_min, dialog;
    // Maximize an inline dialog (add .maximized class, toggle buttons).
    dialog = elem.closest("div.modal-content");
    if ((!_pyfunc_truthy(dialog.classList.contains("maximized")))) {
        dialog.classList.add("maximized");
    }
    b_min = dialog.querySelector("button.minimize");
    b_max = dialog.querySelector("button.maximize");
    b_min.style.display = "inline-block";
    b_max.style.display = "none";
    return null;
};

window.inline_maximize = inline_maximize;
inline_minimize = function flx_inline_minimize (elem) {
    var b_max, b_min, dialog;
    // Minimize an inline dialog (remove .maximized class, toggle buttons).
    dialog = elem.closest("div.modal-content");
    if (_pyfunc_truthy(dialog.classList.contains("maximized"))) {
        _pymeth_remove.call(dialog.classList, "maximized");
    }
    b_min = dialog.querySelector("button.minimize");
    b_max = dialog.querySelector("button.maximize");
    b_min.style.display = "none";
    b_max.style.display = "inline-block";
    return null;
};

window.inline_minimize = inline_minimize;
element_get_url = function flx_element_get_url (element) {
    var attr, stub29_seq, stub30_itr;
    // Get the URL from an element's href, action, or src attribute.
    // 
    //     Args:
    //         element: DOM element.
    // 
    //     Returns:
    //         str: The first found URL attribute value, or None.
    stub29_seq = ["href", "action", "src"];
    if ((typeof stub29_seq === "object") && (!Array.isArray(stub29_seq))) { stub29_seq = Object.keys(stub29_seq);}
    for (stub30_itr = 0; stub30_itr < stub29_seq.length; stub30_itr += 1) {
        attr = stub29_seq[stub30_itr];
        if (_pyfunc_truthy(element.hasAttribute(attr))) {
            return element.getAttribute(attr);
        }
    }
    return null;
};

window.element_get_url = element_get_url;
element_set_url = function flx_element_set_url (element, url) {
    var attr, stub31_seq, stub32_itr;
    // Set the URL on an element's href, action, or src attribute.
    // 
    //     Only sets the first matching attribute.
    // 
    //     Args:
    //         element: DOM element.
    //         url: URL value to set.
    stub31_seq = ["href", "action", "src"];
    if ((typeof stub31_seq === "object") && (!Array.isArray(stub31_seq))) { stub31_seq = Object.keys(stub31_seq);}
    for (stub32_itr = 0; stub32_itr < stub31_seq.length; stub32_itr += 1) {
        attr = stub31_seq[stub32_itr];
        if (_pyfunc_truthy(element.hasAttribute(attr))) {
            element.setAttribute(attr, url);
            return null;
        }
    }
    return null;
};

window.element_set_url = element_set_url;
join_urls = function flx_join_urls (url1, url2) {
    var d, item, key, stub33_, stub34_seq, stub35_itr, stub36_, stub37_seq, stub38_itr, stub39_seq, url1base, value, x, xx, y, z;
    // Merge two URLs, combining their query parameters.
    // 
    //     url2's parameters override url1's for same keys.
    // 
    //     Args:
    //         url1: Base URL.
    //         url2: URL with parameters to merge.
    // 
    //     Returns:
    //         str: Combined URL.
    d = ({});
    if ((!_pyfunc_op_contains("?", url2))) {
        return url1;
    }
    if (_pyfunc_op_contains("?", url1)) {
        stub33_ = _pymeth_split.call(url1, "?", 1);
        url1base = stub33_[0];x = stub33_[1];
        stub34_seq = _pymeth_split.call(x, "&");
        if ((typeof stub34_seq === "object") && (!Array.isArray(stub34_seq))) { stub34_seq = Object.keys(stub34_seq);}
        for (stub35_itr = 0; stub35_itr < stub34_seq.length; stub35_itr += 1) {
            item = stub34_seq[stub35_itr];
            y = _pymeth_split.call(item, "=", 1);
            if ((y.length > 1)) {
                d[y[0]] = y[1];
            } else {
                d[y[0]] = "";
            }
        }
    } else {
        url1base = url1;
    }
    stub36_ = _pymeth_split.call(url2, "?", 1);
    z = stub36_[0];xx = stub36_[1];
    stub37_seq = _pymeth_split.call(xx, "&");
    if ((typeof stub37_seq === "object") && (!Array.isArray(stub37_seq))) { stub37_seq = Object.keys(stub37_seq);}
    for (stub38_itr = 0; stub38_itr < stub37_seq.length; stub38_itr += 1) {
        item = stub37_seq[stub38_itr];
        y = _pymeth_split.call(item, "=", 1);
        if ((y.length > 1)) {
            d[y[0]] = y[1];
        } else {
            d[y[0]] = "";
        }
    }
    url1base += "?";
    stub39_seq = d;
    for (key in stub39_seq) {
        if (!stub39_seq.hasOwnProperty(key)){ continue; }
        value = stub39_seq[key];
        url1base = _pyfunc_op_add(url1base, ((key + "=") + value) + "&");
    }
    return url1base.slice(0,-1);
};

window.join_urls = join_urls;
add_param2url = function flx_add_param2url (url, param) {
    // Append a query parameter to a URL.
    // 
    //     Args:
    //         url: Base URL.
    //         param: Parameter string (e.g. 'key=value').
    // 
    //     Returns:
    //         str: URL with appended parameter.
    if (_pyfunc_op_contains("?", url)) {
        return (url + "&") + param;
    } else {
        return (url + "?") + param;
    }
    return null;
};

window.add_param2url = add_param2url;
export {Loading, save_as, standard_error_handler, download_binary_file, frontend_view, ajax_get, ajax_post, ajax_json, ajax_submit, load_css, on_load_js, load_js, load_many_js, history_push_state, get_elem_from_string, animate_combo, is_hidden, is_visible, get_template, super_query_selector, super_insert, send_to_dom, remove_element, process_resize, get_page, get_table_type, can_popup, correct_href, remove_page_from_href, inline_maximize, inline_minimize, element_get_url, element_set_url, join_urls, add_param2url};

var DefineWebComponent, GlobalBus, set_state;
"\nWeb Component definition and state management module.\n\nProvides:\n- set_state: data-binding engine for reactive state updates in components.\n- DefineWebComponent: declarative custom element builder with shadow DOM,\n  JS/CSS loading, and lifecycle management.\n- GlobalBus: pub/sub event bus for cross-component communication.\n";
set_state = function flx_set_state (component, state) {
    var c, cls, data_selector, element_selector, key, mod_fun, node, nodes, spec, state_actions, stub1_seq, stub2_itr, stub3_seq, stub4_itr, stub5_seq, stub6_itr, stub7_seq, stub8_itr, value, value2, x, x2, xx;
    // Apply reactive state updates to a component's DOM bindings.
    // 
    //     Processes `data-bind` attributes on elements within the component,
    //     applying state values using optional modifiers:
    // 
    //     Modifier prefixes (applied to the data_selector portion):
    //         !  - boolean NOT
    //         ?  - boolean cast (truthy → True, falsy → False)
    //         *  - string cast
    //         +  - float cast (positive)
    //         -  - float cast (negated)
    //         %  - float cast (divided by 100)
    // 
    //     Element selector prefixes:
    //         style-  - set CSS style property
    //         attr-   - set HTML attribute
    //         class-  - toggle CSS class based on value truthiness
    //         (none)  - set innerHTML
    // 
    //     Args:
    //         component: The component instance (must have .root, .options, .state).
    //         state: Dict of key-value pairs to apply.
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
    // Declarative builder for custom HTML elements (Web Components).
    // 
    //     Supports:
    //     - Shadow DOM rendering with CSS imports.
    //     - Lazy loading of JavaScript dependencies.
    //     - Automatic state binding via set_state.
    //     - Decorator-style option registration via the `fun()` method.
    //     - Context manager protocol for clean definition syntax.
    // 
    //     Usage::
    // 
    //         with DefineWebComponent("my-element", shadow=True, js=[...], css=[...]) as comp:
    //             @comp.fun("init")
    //             def init(component):
    //                 # initialization code
    //                 pass
    // 
    //     Attributes:
    //         tag: Custom element tag name.
    //         shadow: Whether to use Shadow DOM.
    //         options: Dict of component lifecycle callbacks and settings.
    //         js: List of JS file URLs to load before init.
    //         css: List of CSS file URLs to load.
    _pyfunc_op_instantiate(this, arguments);
}
DefineWebComponent.prototype._base_class = Object;
DefineWebComponent.prototype.__name__ = "DefineWebComponent";

DefineWebComponent.prototype.__init__ = function (tag, shadow, js, css) {
    shadow = (shadow === undefined) ? false: shadow;
    js = (js === undefined) ? null: js;
    css = (css === undefined) ? null: css;
    // Initialize the component definition.
    // 
    //         Args:
    //             tag: Custom element tag name (e.g. 'my-component').
    //             shadow: Enable Shadow DOM (default False).
    //             js: List of JavaScript file URLs to load.
    //             css: List of CSS file URLs to load.
    this.tag = tag;
    this.shadow = shadow;
    this.options = ({});
    this.js = js;
    this.css = css;
    return null;
};

DefineWebComponent.prototype.make_component = function () {
    var _component, _init, css, init, stub10_itr, stub9_seq;
    // Build and register the custom element with the browser.
    // 
    //         Wraps the init callback to load JS dependencies first, injects
    //         CSS into the template (for shadow DOM) or loads via link (light DOM),
    //         and registers the custom element via define_custom_element.
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
    // Decorator to register a lifecycle callback.
    // 
    //         Usage::
    // 
    //             @comp.fun("init")
    //             def my_init(component):
    //                 pass
    // 
    //         Args:
    //             name: The option key to set (e.g. 'init', 'set_state').
    // 
    //         Returns:
    //             A decorator function that registers the decorated function.
    decorator = (function flx_decorator (funct) {
        self.options[name] = funct;
        return funct;
    }).bind(this);

    return decorator;
};

DefineWebComponent.prototype.__enter__ = function () {
    // Context manager entry - returns self for decorator usage.
    return this;
};

DefineWebComponent.prototype.__exit__ = function (type, value, traceback) {
    // Context manager exit - triggers component registration.
    this.make_component();
    return null;
};


window.DefineWebComponent = DefineWebComponent;
GlobalBus = function () {
    // Simple pub/sub event bus for communication between web components.
    // 
    //     Components register themselves with the bus and receive state updates
    //     via set_external_state. The bus can also emit named events to all
    //     registered components via handle_event.
    // 
    //     Usage::
    // 
    //         bus = GlobalBus()
    //         bus.register(my_component)
    //         bus.set_state({"theme": "dark"})
    //         bus.send_event("refresh", None)
    _pyfunc_op_instantiate(this, arguments);
}
GlobalBus.prototype._base_class = Object;
GlobalBus.prototype.__name__ = "GlobalBus";

GlobalBus.prototype.__init__ = function () {
    // Initialize an empty component registry and state dict.
    this.components = [];
    this.state = ({});
    return null;
};

GlobalBus.prototype.set_state = function (state) {
    var key, state2, stub11_seq, value;
    // Broadcast state changes to all registered components.
    // 
    //         Only emits values that have actually changed from the last known state.
    // 
    //         Args:
    //             state: Dict of key-value pairs to broadcast.
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

GlobalBus.prototype.send_event = function (name, value) {
    var component, stub12_seq, stub13_itr;
    // Send a named event to all registered components.
    // 
    //         Components that implement handle_event(name, value) will receive it.
    // 
    //         Args:
    //             name: Event name.
    //             value: Event payload.
    stub12_seq = this.components;
    if ((typeof stub12_seq === "object") && (!Array.isArray(stub12_seq))) { stub12_seq = Object.keys(stub12_seq);}
    for (stub13_itr = 0; stub13_itr < stub12_seq.length; stub13_itr += 1) {
        component = stub12_seq[stub13_itr];
        if (_pyfunc_truthy(component)) {
            if (_pyfunc_hasattr(component, "handle_event")) {
                component.handle_event(name, value);
            }
        }
    }
    return null;
};

GlobalBus.prototype.emit = function (name, value) {
    var component, stub14_seq, stub15_itr;
    // Emit a state change to all registered components.
    // 
    //         Components that implement set_external_state({name: value}) will
    //         receive the update.
    // 
    //         Args:
    //             name: State key name.
    //             value: New state value.
    stub14_seq = this.components;
    if ((typeof stub14_seq === "object") && (!Array.isArray(stub14_seq))) { stub14_seq = Object.keys(stub14_seq);}
    for (stub15_itr = 0; stub15_itr < stub14_seq.length; stub15_itr += 1) {
        component = stub14_seq[stub15_itr];
        if (_pyfunc_truthy(component)) {
            if (_pyfunc_hasattr(component, "set_external_state")) {
                component.set_external_state(_pyfunc_create_dict(name, value));
            }
        }
    }
    return null;
};

GlobalBus.prototype.register = function (component) {
    var key, stub16_seq, value;
    // Register a component to receive state updates.
    // 
    //         Upon registration, the component immediately receives all current
    //         state values.
    // 
    //         Args:
    //             component: Component instance to register.
    if ((!_pyfunc_op_contains(component, this.components))) {
        _pymeth_append.call(this.components, component);
        if (_pyfunc_hasattr(component, "set_external_state")) {
            stub16_seq = this.state;
            for (key in stub16_seq) {
                if (!stub16_seq.hasOwnProperty(key)){ continue; }
                value = stub16_seq[key];
                component.set_external_state(_pyfunc_create_dict(key, value));
            }
        }
    }
    return null;
};

GlobalBus.prototype.unregister = function (component) {
    // Remove a component from the bus.
    // 
    //         Args:
    //             component: Component instance to unregister.
    if (_pyfunc_op_contains(component, this.components)) {
        _pymeth_remove.call(this.components, component);
    }
    return null;
};


window.GlobalBus = GlobalBus;
export {set_state, DefineWebComponent, GlobalBus};

var MOUNT_INIT_FUN, _get_region_element_closest, _get_region_elements_inside, _on_shown_bs_tab, _refresh_page, _valid_region_element, ajax_load, auto_frame_init, auto_refresh_tab, create_onloadeddata, data_type, datatable_init, get_ajax_frame, get_ajax_link, get_ajax_region, get_click_on_focus_fun, get_refresh_on_focus_fun, init_select2_ctrl, mount_html, moveelement_init, on_focus_action, refresh_ajax_frame, register_mount_fun, select2_init, select_combo_init, selectpicker_init, set_select2_value;
"\nAJAX region management and HTML mounting module.\n\nProvides the core DOM manipulation and AJAX content loading layer:\n- data_type: Detects server response type markers for routing.\n- mount_html: Renders HTML content into a target element with morph support.\n- register_mount_fun: Plugin system for post-mount initialization hooks.\n- Select2, SelectPicker, DataTable initialization hooks.\n- AJAX region/link/frame element lookup helpers.\n- refresh_ajax_frame: Core function for AJAX-based content updates.\n\nDependencies (pscript cross-module):\n    pytigon_js.tools: Loading, correct_href, ajax_get, ajax_post,\n                      get_table_type, super_insert\n    pytigon_js.tbl: init_table\n";
data_type = function flx_data_type (data_or_html) {
    var meta_list, pos, stub1_seq, stub2_itr;
    // Detect the server response type from markers in the response.
    // 
    //     Checks for special `$$RETURN_*` markers in string responses or
    //     `<meta name="RETURN" content="...">` tags in HTML responses.
    // 
    //     Args:
    //         data_or_html: String or DOM element containing server response.
    // 
    //     Returns:
    //         str: One of the `$$RETURN_*` constants, or `$$RETURN_HTML` if
    //              no special marker is found.
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
            } else if (_pyfunc_op_contains("$$RETURN_RELOAD_PAGE", data_or_html)) {
                return "$$RETURN_RELOAD_PAGE";
            } else if (_pyfunc_op_contains("$$RETURN_REFRESH", data_or_html)) {
                return "$$RETURN_REFRESH";
            } else if (_pyfunc_op_contains("$$RETURN_CANCEL", data_or_html)) {
                return "$$RETURN_CANCEL";
            } else if (_pyfunc_op_contains("$$RETURN_RELOAD", data_or_html)) {
                return "$$RETURN_RELOAD";
            } else if (_pyfunc_op_contains("$$RETURN_ERROR", data_or_html)) {
                return "$$RETURN_ERROR";
            } else if (_pyfunc_op_contains("$$RETURN_REFRESH_AUTO_FRAME", data_or_html)) {
                return "$$RETURN_REFRESH_AUTO_FRAME";
            } else if (_pyfunc_op_contains("$$RETURN_HTML_ERROR", data_or_html)) {
                return "$$RETURN_HTML_ERROR";
            } else if (_pyfunc_op_contains("$$RETURN_JSON", data_or_html)) {
                return "$$RETURN_JSON";
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
    // Register a callback to run after every mount_html operation.
    // 
    //     The callback receives the destination element that was just mounted.
    // 
    //     Args:
    //         fun: Callback function(dest_elem) invoked after each mount.
    _pymeth_append.call(MOUNT_INIT_FUN, fun);
    return null;
};

window.register_mount_fun = register_mount_fun;
mount_html = function flx_mount_html (dest_elem, data_or_html, link) {
    var _on_remove, attr, elem2, evt, fun, item, obj, replace, stub3_seq, stub4_itr, stub5_seq, stub6_itr, stub7_seq, stub8_itr;
    link = (link === undefined) ? null: link;
    // Mount HTML content into a destination element.
    // 
    //     This is the central DOM update function. It supports:
    //     - 'loadeddata' event delegation for elements with onloadeddata handlers.
    //     - 'data-link' attribute redirection (.. = replace parent).
    //     - Idiomorph-based DOM morphing for smooth transitions.
    //     - 'call_on_remove' cleanup callbacks.
    //     - 'ajax-temp-item' container unwrapping.
    //     - Post-mount initialization hooks (MOUNT_INIT_FUN).
    // 
    //     Args:
    //         dest_elem: Target DOM element to receive content.
    //         data_or_html: HTML string or DOM element to mount.
    //         link: Optional source element for data-source tracking.
    // 
    //     Returns:
    //         The destination element after mounting, or None if dest_elem is None.
    replace = false;
    if (_pyfunc_op_equals(dest_elem, null)) {
        return null;
    }
    if ((_pyfunc_hasattr(dest_elem, "onloadeddata") && (_pyfunc_truthy(_pyfunc_getattr(dest_elem, "onloadeddata"))) && _pyfunc_truthy(dest_elem.onloadeddata))) {
        evt = document.createEvent("HTMLEvents");
        evt.initEvent("loadeddata", false, true);
        evt.data = data_or_html;
        evt.data_source = link;
        dest_elem.dispatchEvent(evt);
        return dest_elem;
    }
    if (_pyfunc_truthy(dest_elem.hasAttribute("data-link"))) {
        attr = dest_elem.getAttribute("data-link");
        if (_pyfunc_op_equals(attr, "..")) {
            replace = true;
        } else {
            obj = window.super_query_selector(dest_elem, dest_elem.getAttribute("data-link"));
            if (_pyfunc_truthy(obj)) {
                dest_elem = obj;
            }
        }
    }
    if ((!_pyfunc_op_equals(data_or_html, null))) {
        _on_remove = (function flx__on_remove (index, value) {
            // Invoke on_remove callback on elements marked for cleanup.
            value.on_remove();
            return null;
        }).bind(this);

        jQuery.each(_pymeth_find.call(jQuery(dest_elem), ".call_on_remove"), _on_remove);
        if ((dest_elem.children.length > 0)) {
            elem2 = dest_elem.cloneNode();
            if ((_pyfunc_op_equals(jQuery.type(data_or_html), "string"))) {
                window.IN_MORPH_PROCESS = true;
                elem2.innerHTML = data_or_html;
                window.IN_MORPH_PROCESS = false;
                if (_pyfunc_truthy(replace)) {
                    if ((elem2.children.length > 0)) {
                        elem2 = elem2.children[0];
                    }
                }
            } else if ((((_pyfunc_op_equals(_pymeth_lower.call(data_or_html.tagName), "div"))) && (_pyfunc_truthy(data_or_html.classList.contains("ajax-temp-item"))))) {
                stub3_seq = Array.prototype.slice.call(data_or_html.children);
                if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                    item = stub3_seq[stub4_itr];
                    if (_pyfunc_truthy(replace)) {
                        elem2.replaceWith(item);
                        break;
                    } else {
                        elem2.appendChild(item);
                    }
                }
            } else if (_pyfunc_truthy(replace)) {
                elem2.replaceWith(data_or_html);
            } else {
                elem2.appendChild(data_or_html);
            }
            Idiomorph.morph(dest_elem, elem2);
        } else if ((_pyfunc_op_equals(jQuery.type(data_or_html), "string"))) {
            dest_elem.innerHTML = data_or_html;
            if (_pyfunc_truthy(replace)) {
                if ((dest_elem.children.length > 0)) {
                    dest_elem.replaceWith(dest_elem.children[0]);
                }
            }
        } else if ((((_pyfunc_op_equals(_pymeth_lower.call(data_or_html.tagName), "div"))) && (_pyfunc_truthy(data_or_html.classList.contains("ajax-temp-item"))))) {
            stub5_seq = Array.prototype.slice.call(data_or_html.children);
            if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
            for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
                item = stub5_seq[stub6_itr];
                if (_pyfunc_truthy(replace)) {
                    dest_elem.replaceWith(item);
                    break;
                } else {
                    dest_elem.appendChild(item);
                }
            }
        } else if (_pyfunc_truthy(replace)) {
            dest_elem.replaceWith(data_or_html);
        } else {
            dest_elem.appendChild(data_or_html);
        }
    }
    if (_pyfunc_truthy(MOUNT_INIT_FUN)) {
        stub7_seq = MOUNT_INIT_FUN;
        if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
        for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
            fun = stub7_seq[stub8_itr];
            fun(dest_elem);
        }
    }
    return dest_elem;
};

window.mount_html = mount_html;
selectpicker_init = function flx_selectpicker_init (dest_elem) {
    // Initialize Bootstrap SelectPicker widgets in mounted content.
    if (_pyfunc_hasattr(jQuery.fn, "selectpicker")) {
        ((_pymeth_find.call(jQuery(dest_elem), ".selectpicker")).selectpicker)();
    }
    return null;
};

register_mount_fun(selectpicker_init);
auto_frame_init = function flx_auto_frame_init (dest_elem) {
    var elem, frame_list, stub10_itr, stub9_seq;
    // Auto-refresh all .auto-frame elements in mounted content.
    frame_list = Array.prototype.slice.call(dest_elem.querySelectorAll(".auto-frame"));
    stub9_seq = frame_list;
    if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
    for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
        elem = stub9_seq[stub10_itr];
        refresh_ajax_frame(elem);
    }
    return null;
};

register_mount_fun(auto_frame_init);
_on_shown_bs_tab = function flx__on_shown_bs_tab (event) {
    var auto_refresh_target, div, frame, item, item_list, stub11_seq, stub12_itr, target;
    // Handle Bootstrap tab shown event for auto-refresh tabs.
    // 
    //     When a tab is shown, refreshes the associated frame or specific
    //     targets within it based on auto-refresh-target attribute.
    if (_pyfunc_truthy(event.target.hasAttribute("data-bs-target"))) {
        target = event.target.getAttribute("data-bs-target");
        div = event.target.closest("div.auto-refresh");
        frame = div.querySelector(target);
        if (_pyfunc_truthy(frame.hasAttribute("auto-refresh-target"))) {
            auto_refresh_target = frame.getAttribute("auto-refresh-target");
            item_list = Array.prototype.slice.call(frame.querySelectorAll(auto_refresh_target));
            stub11_seq = item_list;
            if ((typeof stub11_seq === "object") && (!Array.isArray(stub11_seq))) { stub11_seq = Object.keys(stub11_seq);}
            for (stub12_itr = 0; stub12_itr < stub11_seq.length; stub12_itr += 1) {
                item = stub11_seq[stub12_itr];
                window.refresh_ajax_frame(item);
            }
        } else {
            refresh_ajax_frame(frame);
        }
    }
    return null;
};

auto_refresh_tab = function flx_auto_refresh_tab (dest_elem) {
    var elem, item_list, stub13_seq, stub14_itr;
    // Bind auto-refresh behavior to tabs in .auto-refresh containers.
    item_list = Array.prototype.slice.call(dest_elem.querySelectorAll("div.auto-refresh button"));
    stub13_seq = item_list;
    if ((typeof stub13_seq === "object") && (!Array.isArray(stub13_seq))) { stub13_seq = Object.keys(stub13_seq);}
    for (stub14_itr = 0; stub14_itr < stub13_seq.length; stub14_itr += 1) {
        elem = stub13_seq[stub14_itr];
        elem.addEventListener("shown.bs.tab", _on_shown_bs_tab);
    }
    return null;
};

register_mount_fun(auto_refresh_tab);
get_click_on_focus_fun = function flx_get_click_on_focus_fun (element) {
    var _click;
    // Create a visibilitychange handler that clicks the element.
    // 
    //     Args:
    //         element: DOM element to click when page becomes visible.
    // 
    //     Returns:
    //         Callback for the visibilitychange event.
    _click = (function flx__click (event) {
        if ((!_pyfunc_truthy(document.hidden))) {
            element.click();
        }
        return null;
    }).bind(this);

    return _click;
};

get_refresh_on_focus_fun = function flx_get_refresh_on_focus_fun (element) {
    var _refresh;
    // Create a visibilitychange handler that refreshes the element.
    // 
    //     Args:
    //         element: DOM element to refresh when page becomes visible.
    // 
    //     Returns:
    //         Callback for the visibilitychange event.
    _refresh = (function flx__refresh (event) {
        if ((!_pyfunc_truthy(document.hidden))) {
            refresh_ajax_frame(element);
        }
        return null;
    }).bind(this);

    return _refresh;
};

on_focus_action = function flx_on_focus_action (dest_elem) {
    var elem, fun, item_list, stub15_seq, stub16_itr;
    // Bind visibilitychange-based actions to .on-focus-action elements.
    // 
    //     Supports two modes:
    //     - .on-focus-action-click: clicks the element when page becomes visible.
    //     - .on-focus-action-refresh: refreshes the element when page becomes visible.
    item_list = Array.prototype.slice.call(dest_elem.querySelectorAll(".on-focus-action"));
    stub15_seq = item_list;
    if ((typeof stub15_seq === "object") && (!Array.isArray(stub15_seq))) { stub15_seq = Object.keys(stub15_seq);}
    for (stub16_itr = 0; stub16_itr < stub15_seq.length; stub16_itr += 1) {
        elem = stub15_seq[stub16_itr];
        fun = null;
        if (_pyfunc_truthy(elem.classList.contains("on-focus-action-click"))) {
            fun = get_click_on_focus_fun(elem);
        } else if (_pyfunc_truthy(elem.classList.contains("on-focus-action-refresh"))) {
            fun = get_refresh_on_focus_fun(elem);
        }
        if (_pyfunc_truthy(fun)) {
            window.addEventListener("visibilitychange", fun);
        }
    }
    return null;
};

register_mount_fun(on_focus_action);
moveelement_init = function flx_moveelement_init (dest_elem) {
    var _on_remove, data_position, elem2, obj, objs, parent, stub19_seq, stub20_itr;
    // Process .move-element directives: move elements to target positions.
    // 
    //     Elements with class 'move-element' and 'data-position' attribute are
    //     moved to the specified DOM location via super_insert. Registers cleanup
    //     callbacks for proper element removal.
    objs = Array.prototype.slice.call(dest_elem.querySelectorAll(".move-element"));
    if (_pyfunc_truthy(objs)) {
        stub19_seq = objs;
        if ((typeof stub19_seq === "object") && (!Array.isArray(stub19_seq))) { stub19_seq = Object.keys(stub19_seq);}
        for (stub20_itr = 0; stub20_itr < stub19_seq.length; stub20_itr += 1) {
            obj = stub19_seq[stub20_itr];
            if (_pyfunc_truthy(obj.hasAttribute("data-position"))) {
                _pymeth_remove.call(obj.classList, "move-element");
                data_position = obj.getAttribute("data-position");
                parent = obj.parentElement;
                elem2 = super_insert(dest_elem, obj.getAttribute("data-position"), obj);
                if ((!_pyfunc_truthy(elem2))) {
                    continue;
                }
                if (_pyfunc_truthy(_pymeth_endswith.call(data_position, ":class"))) {
                    _on_remove = (function flx__on_remove () {
                        var c, stub17_seq, stub18_itr;
                        // Remove classes from target when source is removed.
                        stub17_seq = Array.prototype.slice.call(obj.classList);
                        if ((typeof stub17_seq === "object") && (!Array.isArray(stub17_seq))) { stub17_seq = Object.keys(stub17_seq);}
                        for (stub18_itr = 0; stub18_itr < stub17_seq.length; stub18_itr += 1) {
                            c = stub17_seq[stub18_itr];
                            _pymeth_remove.call(elem2.classList, c);
                        }
                        return null;
                    }).bind(this);

                } else {
                    _on_remove = (function flx__on_remove () {
                        // Remove the original element when source is removed.
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
set_select2_value = function flx_set_select2_value (sel2, id, text) {
    // Set the value and display text of a Select2 widget.
    // 
    //     Args:
    //         sel2: jQuery Select2 element.
    //         id: Option value to select.
    //         text: Display text for the option.
    _pymeth_append.call(sel2, (jQuery("<option>", ({value: id, text: text}))));
    sel2.val(id.toString());
    sel2.trigger("change");
    return null;
};

create_onloadeddata = function flx_create_onloadeddata (control) {
    var _onloadeddata;
    // Create a loadeddata event handler for a Select2 control.
    // 
    //     When the control receives a loadeddata event with data_source,
    //     extracts data-id and data-text attributes to set the Select2 value.
    // 
    //     Args:
    //         control: The Select2 DOM element.
    // 
    //     Returns:
    //         Event handler function for the 'loadeddata' event.
    _onloadeddata = function (event) {
        var id, src_elem, text;
        if (_pyfunc_hasattr(event, "data_source")) {
            src_elem = event.data_source;
            if (_pyfunc_truthy(src_elem)) {
                id = src_elem.getAttribute("data-id");
                text = src_elem.getAttribute("data-text");
                if ((_pyfunc_truthy(id) && _pyfunc_truthy(text))) {
                    set_select2_value(jQuery(control), id, text);
                }
            }
        }
        return null;
    };

    return _onloadeddata;
};

init_select2_ctrl = function () {
    var id, sel2, src, text;
    // Initialize a single Select2 control with existing data from parent.
    // 
    //     Looks for item_id/item_str attributes on the parent .input-group
    //     and sets the Select2 value accordingly.
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
};

select2_init = function flx_select2_init (dest_elem) {
    var control, controls, modal, stub21_seq, stub22_itr;
    // Initialize Django Select2 widgets in mounted content.
    // 
    //     Configures Select2 with proper dropdown parents (especially for modals)
    //     and wires up loadeddata handlers for dynamic value updates.
    controls = Array.prototype.slice.call(dest_elem.querySelectorAll(".django-select2"));
    if (_pyfunc_truthy(controls)) {
        stub21_seq = controls;
        if ((typeof stub21_seq === "object") && (!Array.isArray(stub21_seq))) { stub21_seq = Object.keys(stub21_seq);}
        for (stub22_itr = 0; stub22_itr < stub21_seq.length; stub22_itr += 1) {
            control = stub21_seq[stub22_itr];
            modal = control.closest(".modal");
            if (_pyfunc_truthy(modal)) {
                (jQuery(control).djangoSelect2)(({minimumInputLength: 0, placeholder: "Select an option", dropdownParent: jQuery(modal)}));
            } else {
                (jQuery(control).djangoSelect2)(({minimumInputLength: 0, placeholder: "Select an option"}));
            }
            control.onloadeddata = create_onloadeddata(control);
            control.classList.add("ajax-frame");
            control.setAttribute("data-region", "get_row");
        }
    }
    ((_pymeth_find.call(jQuery(dest_elem), ".django-select2")).each)(init_select2_ctrl);
    return null;
};

register_mount_fun(select2_init);
select_combo_init = function flx_select_combo_init (dest_elem) {
    var elem, on_change, on_change_element, select_ctrl_list, stub23_seq, stub24_itr;
    // Initialize cascading select combos (.select_combo class).
    // 
    //     When a select with data-rel-name changes, finds the associated element
    //     by name and loads its options via AJAX from its src attribute.
    //     Supports loadeddata event delegation for custom handlers.
    select_ctrl_list = Array.prototype.slice.call(dest_elem.querySelectorAll(".select_combo"));
    on_change_element = (function flx_on_change_element (element) {
        var _onload, evt, next_element, next_elements, region, src;
        // Handle cascading update for a changed select element.
        region = element.closest(".ajax-region");
        if ((!_pyfunc_op_equals(region, null))) {
            next_elements = document.getElementsByName(element.getAttribute("data-rel-name"));
            if ((next_elements.length > 0)) {
                next_element = next_elements[0];
                if (_pyfunc_truthy(next_element.hasAttribute("src"))) {
                    src = next_element.getAttribute("src");
                    if (_pyfunc_truthy(element.value)) {
                        src = process_href(src, jQuery(element));
                        _onload = (function flx__onload (responseText) {
                            var evt;
                            if ((_pyfunc_hasattr(next_element, "onloadeddata") && (_pyfunc_truthy(_pyfunc_getattr(next_element, "onloadeddata"))) && _pyfunc_truthy(next_element.onloadeddata))) {
                                evt = document.createEvent("HTMLEvents");
                                evt.initEvent("loadeddata", false, true);
                                evt.data = responseText;
                                evt.data_source = src;
                                next_element.dispatchEvent(evt);
                            } else {
                                next_element.innerHTML = responseText;
                                on_change_element(next_element);
                            }
                            return null;
                        }).bind(this);

                        ajax_get(src, _onload);
                    } else if ((_pyfunc_hasattr(next_element, "onloadeddata") && (_pyfunc_truthy(_pyfunc_getattr(next_element, "onloadeddata"))) && _pyfunc_truthy(next_element.onloadeddata))) {
                        evt = document.createEvent("HTMLEvents");
                        evt.initEvent("loadeddata", false, true);
                        evt.data = "";
                        evt.data_source = src;
                        next_element.dispatchEvent(evt);
                    } else {
                        next_element.innerHTML = "<option disabled selected value></option>";
                        on_change_element(next_element);
                    }
                }
            }
        }
        return null;
    }).bind(this);

    on_change = (function flx_on_change (event) {
        var element;
        element = event.target;
        return on_change_element(element);
    }).bind(this);

    stub23_seq = select_ctrl_list;
    if ((typeof stub23_seq === "object") && (!Array.isArray(stub23_seq))) { stub23_seq = Object.keys(stub23_seq);}
    for (stub24_itr = 0; stub24_itr < stub23_seq.length; stub24_itr += 1) {
        elem = stub23_seq[stub24_itr];
        if (_pyfunc_truthy(elem.hasAttribute("data-rel-name"))) {
            elem.addEventListener("change", on_change);
        }
    }
    return null;
};

register_mount_fun(select_combo_init);
datatable_init = function flx_datatable_init (dest_elem) {
    var table_type, tbl;
    // Initialize DataTables and treegrid widgets in mounted content.
    // 
    //     Detects the table type and initializes Bootstrap Table and treegrid
    //     components as appropriate.
    table_type = get_table_type(jQuery(dest_elem));
    tbl = _pymeth_find.call(jQuery(dest_elem), ".tabsort");
    if ((tbl.length > 0)) {
        init_table(tbl, table_type);
    }
    if (_pyfunc_hasattr(jQuery.fn, "treegrid")) {
        ((_pymeth_find.call(jQuery(dest_elem), ".tree")).treegrid)();
    }
    return null;
};

register_mount_fun(datatable_init);
register_mount_fun(process_resize);
_valid_region_element = function flx__valid_region_element (element, class_name, region_name) {
    var x;
    region_name = (region_name === undefined) ? null: region_name;
    // Check if an element belongs to the specified region scope.
    // 
    //     An element is valid if it has no region_name requirement, or if its
    //     data-region attribute contains the region_name (possibly with a
    //     parenthesized scope qualifier).
    // 
    //     Args:
    //         element: DOM element to check.
    //         class_name: The CSS class type ('ajax-region', 'ajax-link', etc.).
    //         region_name: Optional region name to match.
    // 
    //     Returns:
    //         bool: True if the element is valid for the given region.
    if ((!_pyfunc_truthy(region_name))) {
        return true;
    }
    if (_pyfunc_truthy(element.hasAttribute("data-region"))) {
        x = element.getAttribute("data-region");
        if (_pyfunc_op_equals(region_name, x)) {
            return true;
        }
        if ((_pyfunc_op_contains((("(" + region_name) + ")"), x))) {
            return true;
        }
        if ((_pyfunc_op_contains((((("(" + class_name) + ":") + region_name) + ")"), x))) {
            return true;
        }
    }
    return false;
};

_get_region_elements_inside = function flx__get_region_elements_inside (element, class_name, region_name) {
    var item, item_list, ret, stub25_seq, stub26_itr;
    region_name = (region_name === undefined) ? null: region_name;
    // Find all elements with a given class inside a container.
    // 
    //     Args:
    //         element: Container DOM element.
    //         class_name: CSS class to query (e.g. 'ajax-link').
    //         region_name: Optional region scope filter.
    // 
    //     Returns:
    //         list: Matching DOM elements.
    item_list = Array.prototype.slice.call(element.querySelectorAll("." + class_name));
    ret = [];
    stub25_seq = item_list;
    if ((typeof stub25_seq === "object") && (!Array.isArray(stub25_seq))) { stub25_seq = Object.keys(stub25_seq);}
    for (stub26_itr = 0; stub26_itr < stub25_seq.length; stub26_itr += 1) {
        item = stub25_seq[stub26_itr];
        if (_pyfunc_truthy(item.classList.contains(class_name))) {
            if (_pyfunc_truthy(_valid_region_element(item, class_name, region_name))) {
                _pymeth_append.call(ret, item);
            }
        } else if ((!_pyfunc_truthy(region_name))) {
            _pymeth_append.call(ret, item);
        }
    }
    return ret;
};

_get_region_element_closest = function flx__get_region_element_closest (element, class_name, region_name) {
    var item;
    region_name = (region_name === undefined) ? null: region_name;
    // Find the closest ancestor matching class_name and optional region.
    // 
    //     Args:
    //         element: Starting DOM element.
    //         class_name: CSS class to match.
    //         region_name: Optional region scope filter.
    // 
    //     Returns:
    //         Matching ancestor element or None.
    item = element.closest("." + class_name);
    if ((!_pyfunc_truthy(region_name))) {
        return item;
    }
    while (item) {
        if (_pyfunc_truthy(_valid_region_element(item, class_name, region_name))) {
            return item;
        }
        item = item.parentElement;
        if ((!_pyfunc_op_equals(item, null))) {
            item = item.closest("." + class_name);
        }
    }
    return null;
};

get_ajax_region = function flx_get_ajax_region (element, region_name, strict_mode) {
    var ret;
    region_name = (region_name === undefined) ? null: region_name;
    strict_mode = (strict_mode === undefined) ? false: strict_mode;
    // Find the nearest .ajax-region ancestor matching the region name.
    // 
    //     Args:
    //         element: Starting DOM element.
    //         region_name: Optional region name to match (from data-region attr).
    //         strict_mode: If True, returns None instead of falling back to
    //             the closest region without name matching.
    // 
    //     Returns:
    //         The matching .ajax-region element or None.
    if (_pyfunc_truthy((_pyfunc_truthy(element.classList.contains("ajax-region"))) && (_pyfunc_truthy(_valid_region_element(element, "ajax-region", region_name))))) {
        return element;
    } else if (_pyfunc_truthy(region_name)) {
        ret = element.closest(".ajax-region");
        while (ret) {
            if (_pyfunc_truthy(_valid_region_element(ret, "ajax-region", region_name))) {
                return ret;
            }
            ret = ret.parentElement;
            if ((!_pyfunc_op_equals(ret, null))) {
                ret = ret.closest(".ajax-region");
            }
        }
        if ((_pyfunc_truthy(region_name) && ((!_pyfunc_truthy(strict_mode))))) {
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
get_ajax_link = function flx_get_ajax_link (element, region_name, strict_mode) {
    var link, link_list, region, stub27_seq, stub28_itr;
    region_name = (region_name === undefined) ? null: region_name;
    strict_mode = (strict_mode === undefined) ? false: strict_mode;
    // Find the .ajax-link element for a given region scope.
    // 
    //     Searches for elements that provide the URL for AJAX operations within
    //     a region. Priority: direct class match > single child > closest child.
    // 
    //     Args:
    //         element: Starting DOM element.
    //         region_name: Optional region name scope.
    //         strict_mode: If True, don't fall back to un-scoped lookup.
    // 
    //     Returns:
    //         The matching .ajax-link element or None.
    if (_pyfunc_truthy((_pyfunc_truthy(element.classList.contains("ajax-link"))) && (_pyfunc_truthy(_valid_region_element(element, "ajax-link", region_name))))) {
        return element;
    }
    region = get_ajax_region(element, region_name, strict_mode);
    if ((!_pyfunc_op_equals(region, null))) {
        if (_pyfunc_truthy((_pyfunc_truthy(region.classList.contains("ajax-link"))) && (_pyfunc_truthy(_valid_region_element(region, "ajax-link", region_name))))) {
            return region;
        } else if (_pyfunc_truthy(region_name)) {
            link_list = _get_region_elements_inside(region, "ajax-link", region_name);
            if ((link_list.length == 1)) {
                return link_list[0];
            }
            stub27_seq = link_list;
            if ((typeof stub27_seq === "object") && (!Array.isArray(stub27_seq))) { stub27_seq = Object.keys(stub27_seq);}
            for (stub28_itr = 0; stub28_itr < stub27_seq.length; stub28_itr += 1) {
                link = stub27_seq[stub28_itr];
                if ((_pyfunc_op_equals(_get_region_element_closest(link, "ajax-region", region_name), region))) {
                    return link;
                }
            }
            if ((link_list.length > 0)) {
                return link_list[0];
            }
        } else {
            return region.querySelector(".ajax-link");
        }
    }
    if ((_pyfunc_truthy(region_name) && ((!_pyfunc_truthy(strict_mode))))) {
        return get_ajax_link(element, null);
    } else {
        return null;
    }
    return null;
};

window.get_ajax_link = get_ajax_link;
get_ajax_frame = function flx_get_ajax_frame (element, region_name, strict_mode) {
    var f, frame_list, region, stub29_seq, stub30_itr;
    region_name = (region_name === undefined) ? null: region_name;
    strict_mode = (strict_mode === undefined) ? false: strict_mode;
    // Find the .ajax-frame element for a given region scope.
    // 
    //     Similar to get_ajax_link but for frame elements (content containers).
    // 
    //     Args:
    //         element: Starting DOM element.
    //         region_name: Optional region name scope.
    //         strict_mode: If True, don't fall back to un-scoped lookup.
    // 
    //     Returns:
    //         The matching .ajax-frame element or None.
    region = get_ajax_region(element, region_name, strict_mode);
    if ((!_pyfunc_op_equals(region, null))) {
        if (_pyfunc_truthy((_pyfunc_truthy(region.classList.contains("ajax-frame"))) && (_pyfunc_truthy(_valid_region_element(region, "ajax-frame", region_name))))) {
            return region;
        } else if (_pyfunc_truthy(region_name)) {
            frame_list = _get_region_elements_inside(region, "ajax-frame", region_name);
            if ((frame_list.length == 1)) {
                return frame_list[0];
            }
            stub29_seq = frame_list;
            if ((typeof stub29_seq === "object") && (!Array.isArray(stub29_seq))) { stub29_seq = Object.keys(stub29_seq);}
            for (stub30_itr = 0; stub30_itr < stub29_seq.length; stub30_itr += 1) {
                f = stub29_seq[stub30_itr];
                if ((_pyfunc_op_equals(_get_region_element_closest(f, "ajax-region", region_name), region))) {
                    return f;
                }
            }
            if ((frame_list.length > 0)) {
                return frame_list[0];
            }
        } else {
            return region.querySelector(".ajax-frame");
        }
    }
    if ((_pyfunc_truthy(region_name) && ((!_pyfunc_truthy(strict_mode))))) {
        return get_ajax_frame(element, null);
    } else {
        return null;
    }
    return null;
};

window.get_ajax_frame = get_ajax_frame;
_refresh_page = function flx__refresh_page (target_element, data_element) {
    var data_element2, frame;
    // Refresh the content of a full page section.
    // 
    //     Replaces the content inside div.content with new data.
    // 
    //     Args:
    //         target_element: Element within the page to refresh.
    //         data_element: New content (string or DOM element).
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

refresh_ajax_frame = function flx_refresh_ajax_frame (element, region_name, data_element, callback, callback_on_error, data_if_none) {
    var _callback, _callback_on_error, data, frame, link, loading, post, region, url;
    region_name = (region_name === undefined) ? null: region_name;
    data_element = (data_element === undefined) ? null: data_element;
    callback = (callback === undefined) ? null: callback;
    callback_on_error = (callback_on_error === undefined) ? null: callback_on_error;
    data_if_none = (data_if_none === undefined) ? null: data_if_none;
    // Refresh an AJAX frame with content from the server or provided data.
    // 
    //     This is the central function for AJAX-based content updates. It:
    //     1. Locates the region, frame, and link elements.
    //     2. If data_element is provided, uses it directly.
    //     3. Otherwise, fetches the URL from the link element via GET or POST.
    //     4. Processes the response based on its data_type marker.
    //     5. Handles special markers: REFRESH, RELOAD, CANCEL, ERROR, JSON, etc.
    // 
    //     Args:
    //         element: Starting element for region/link/frame lookup.
    //         region_name: Optional region scope name.
    //         data_element: Pre-fetched content to mount (skips AJAX if provided).
    //         callback: Success callback invoked after content is mounted.
    //         callback_on_error: Error callback for failed requests.
    //         data_if_none: Content to use if the URL contains unresolved [[placeholders]].
    // 
    //     Returns:
    //         The result of mount_html, or None.
    region = get_ajax_region(element, region_name);
    frame = get_ajax_frame(element, region_name);
    if (_pyfunc_op_equals(frame, null)) {
        return null;
    }
    link = get_ajax_link(element, region_name);
    url = null;
    loading = new Loading(element);
    _callback = (function flx__callback (data) {
        var dt, elem, evt, options, plug, ret, txt;
        // Process the AJAX response and route based on data_type.
        ret = null;
        loading.stop();
        loading.remove();
        dt = data_type(data);
        if ((((!_pyfunc_op_equals(dt, "$$RETURN_ERROR"))) && _pyfunc_truthy(element) && (_pyfunc_truthy(element.hasAttribute("rettype"))))) {
            dt = "$$" + element.getAttribute("rettype");
        }
        if ((((!_pyfunc_op_equals(dt, "$$RETURN_ERROR"))) && (_pyfunc_truthy(_pyfunc_getattr(frame, "onloadeddata"))) && _pyfunc_truthy(frame.onloadeddata))) {
            ret = mount_html(frame, data, link);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_REFRESH"])) {
            return refresh_ajax_frame(region, region_name, null, callback, callback_on_error);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_REFRESH_PARENT"])) {
            return refresh_ajax_frame(region.parentElement, region_name, null, callback, callback_on_error);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_RELOAD_PAGE"])) {
            return _refresh_page(region, data);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_OK", "$$RETURN_NEW_ROW_OK", "$$RETURN_UPDATE_ROW_OK"])) {
            plug = region.closest(".plug");
            if (_pyfunc_truthy(plug)) {
                elem = region.closest(".plug").parentElement;
            } else {
                elem = element;
            }
            if (_pyfunc_truthy(callback)) {
                callback();
            }
            return refresh_ajax_frame(elem, "", null, null, callback_on_error, data);
        } else if (_pyfunc_op_equals(dt, "$$RETURN_RELOAD")) {
            if (_pyfunc_op_equals(region_name, "error")) {
                ret = mount_html(frame, data, link);
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
        } else if (_pyfunc_op_equals(dt, "$$RETURN_REFRESH_AUTO_FRAME")) {
            auto_frame_init(frame);
        } else if (_pyfunc_op_equals(dt, "$$RETURN_HTML_ERROR")) {
            if ((Object.prototype.toString.call(data).slice(8,-1).toLowerCase() === 'string')) {
                txt = data;
            } else {
                txt = data.innerHTML;
            }
            options = ({title: "Error!", html: txt, icon: "error", buttonsStyling: false, showCancelButton: false, customClass: ({confirmButton: "btn btn-primary btn-lg"})});
            Swal.fire(options);
        } else if (_pyfunc_op_equals(dt, "$$RETURN_JSON")) {
            frame = get_ajax_frame(region, "json");
            callback();
            if (_pyfunc_truthy(frame)) {
                if ((_pyfunc_hasattr(frame, "onloadeddata") && (_pyfunc_truthy(_pyfunc_getattr(frame, "onloadeddata"))) && _pyfunc_truthy(frame.onloadeddata))) {
                    evt = document.createEvent("HTMLEvents");
                    evt.initEvent("loadeddata", false, true);
                    evt.data = data;
                    evt.data_source = link;
                    frame.dispatchEvent(evt);
                    return null;
                }
            }
            return null;
        } else {
            ret = mount_html(frame, data, link);
        }
        if (_pyfunc_op_contains(dt, ["$$RETURN_ERROR", "$$RETURN_RELOAD", "$$RETURN_HTML_ERROR"])) {
            if (_pyfunc_truthy(callback_on_error)) {
                callback_on_error();
            }
        } else if (_pyfunc_truthy(callback)) {
            callback();
        }
        return ret;
    }).bind(this);

    _callback_on_error = (function flx__callback_on_error (req) {
        // Handle AJAX request failure.
        loading.stop();
        loading.remove();
        window.standard_error_handler(req);
        return null;
    }).bind(this);

    if (_pyfunc_truthy(data_element)) {
        return _callback(data_element);
    }
    post = false;
    if ((!_pyfunc_op_equals(link, null))) {
        if (_pyfunc_truthy(link.hasAttribute("href"))) {
            url = link.getAttribute("href");
        } else if (_pyfunc_truthy(link.hasAttribute("action"))) {
            url = link.getAttribute("action");
            post = true;
        } else if (_pyfunc_truthy(link.hasAttribute("src"))) {
            url = link.getAttribute("src");
        }
    }
    if (_pyfunc_truthy(url)) {
        url = correct_href(url, [element, link]);
        url = process_href(url, jQuery(link.parentElement));
        if ((_pyfunc_op_contains("[[", url) && _pyfunc_op_contains("]]", url))) {
            _callback(data_if_none);
            return null;
        }
        loading.create();
        loading.start();
        if (_pyfunc_truthy(post)) {
            if ((_pyfunc_op_equals(_pymeth_lower.call(link.tagName), "form"))) {
                ajax_submit(link, _callback, _callback_on_error, null, null, url);
            } else {
                data = (jQuery(link).serialize)();
                ajax_post(url, data, _callback, _callback_on_error);
            }
        } else {
            ajax_get(url, _callback, _callback_on_error);
        }
        return null;
    } else {
        return _callback(data_if_none);
    }
    return null;
};

window.refresh_ajax_frame = refresh_ajax_frame;
ajax_load = function flx_ajax_load (element, url, complete) {
    var _onload;
    // Load content from a URL and mount it into the specified element.
    // 
    //     Simple wrapper around ajax_get + mount_html.
    // 
    //     Args:
    //         element: Target DOM element for the loaded content.
    //         url: URL to fetch content from.
    //         complete: Callback invoked with the response text after mounting.
    _onload = (function flx__onload (responseText) {
        mount_html(element, responseText, null);
        complete(responseText);
        return null;
    }).bind(this);

    ajax_get(url, _onload);
    return null;
};

window.ajax_load = ajax_load;
export {data_type, register_mount_fun, mount_html, selectpicker_init, auto_frame_init, auto_refresh_tab, get_click_on_focus_fun, get_refresh_on_focus_fun, on_focus_action, moveelement_init, set_select2_value, create_onloadeddata, init_select2_ctrl, select2_init, select_combo_init, datatable_init, get_ajax_region, get_ajax_link, get_ajax_frame, refresh_ajax_frame, ajax_load};

var INIT_DB_STRUCT, SYNC_STRUCT, _MSIE, _MSIE2, _UA, get_list_from_table, get_table, init_db, init_sync, on_sys_sync, open_database, sync_and_run;
"\nIndexedDB database layer and server synchronization module.\n\nProvides:\n- IndexedDB initialization and table management.\n- Generic CRUD helpers (open, get_table, get_list_from_table).\n- Time-stamp based synchronization between server and local IndexedDB.\n- Support for configurable sync structures (multiple tables).\n";
INIT_DB_STRUCT = null;
init_db = function flx_init_db (struct) {
    // Initialize the database schema definition.
    // 
    //     Called before open_database to define which object stores to create.
    // 
    //     Args:
    //         struct: List of (store_name, options) tuples for IndexedDB object stores.
    INIT_DB_STRUCT = struct;
    return null;
};

window.init_db = init_db;
open_database = function flx_open_database (on_open) {
    var _onerror, _onsuccess, _onupgradeneeded, request;
    // Open (or create) the IndexedDB database for the current project.
    // 
    //     The database name is derived from window.PRJ_NAME. On first creation,
    //     creates a 'param' key-value store plus any stores defined via init_db().
    // 
    //     Args:
    //         on_open: Callback invoked with the opened database instance on success.
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
    // Open a specific object store within the IndexedDB database.
    // 
    //     Args:
    //         table_name: Name of the object store to open.
    //         on_open: Callback receiving (transaction, objectStore).
    //         read_only: If True, opens in readonly mode; otherwise readwrite.
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
    // Retrieve all records from an object store as a list.
    // 
    //     Opens a cursor and iterates through all records, collecting them
    //     into an array.
    // 
    //     Args:
    //         table: Name of the object store.
    //         on_open_list: Callback receiving the list of all stored items.
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
    // Built-in system sync handler: clears PYTIGON cache and reports status.
    // 
    //     Args:
    //         fun: Callback receiving status string:
    //             'OK-refresh' if cache was deleted,
    //             'OK-no cache' if no cache existed.
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
    // Register additional synchronization entries.
    // 
    //     Each entry defines a table name, a server URL for timestamp checking,
    //     and a sync function to execute when the server has newer data.
    // 
    //     Args:
    //         sync_struct: List of sync entries to append to SYNC_STRUCT.
    //             Each entry: [table_name, url, sync_function]
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
    // Synchronize a specific table with the server and invoke callback.
    // 
    //     Fetches a timestamp from the server, compares it with the locally stored
    //     timestamp in IndexedDB, and runs the registered sync function if the
    //     server has newer data.
    // 
    //     Args:
    //         tbl: Table name to synchronize (must be registered in SYNC_STRUCT).
    //         fun: Callback receiving status:
    //             'OK' - already in sync,
    //             'OK-refresh' / 'OK-no cache' - from sync function,
    //             'offline' - no network connection,
    //             'timeout' - request timed out,
    //             'error - no reg function' - table not registered.
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
            // Process the server timestamp response.
            _on_open_param = (function flx__on_open_param (trans, db) {
                var _on_param_error, _on_param_success, param_get_request;
                // Check local timestamp against server timestamp in IndexedDB.
                param_get_request = _pymeth_get.call(db, ("time_sync_" + tbl));
                _on_param_error = (function flx__on_param_error (event) {
                    // No local timestamp yet - store and trigger sync.
                    rec[2](fun);
                    db.add(({key: "time_sync_" + tbl, value: time}));
                    return null;
                }).bind(this);

                _on_param_success = (function flx__on_param_success (event) {
                    var _on_add_error, _on_add_success, _on_update, param, param_add_request, param_update_request, time2;
                    // Compare timestamps and update if server is newer.
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

            x = JSON.parse(responseText);
            time = x["TIME"];
            get_table("param", _on_open_param, false);
            return null;
        }).bind(this);

        _on_request_init = (function flx__on_request_init (request) {
            var _on_timeout;
            // Configure a 2-second timeout for the sync request.
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

var EVENT_CLICK_TAB, EVENT_TAB, REGISTERED_EVENT_TYPES, _check_element, _get_click_event_from_tab, _get_scrolled_parent, _get_title, _get_value, _on_close_subpage, _on_inline, _on_menu_click, _on_popup, _on_subframe, close_frame, create_event_handler, on_click_default_action, on_close_subframe, on_close_subframe_and_refresh, on_close_subpage, on_close_subpage_and_refresh, on_global_event, on_inline, on_inline_delete, on_inline_edit_new, on_inline_error, on_inline_info, on_message, on_new_tab, on_popup, on_popup_delete, on_popup_edit_new, on_popup_error, on_popup_info, on_replace_app, on_resize, on_subframe, on_subpage, only_get, process_href, refresh_app, refresh_frame, refresh_page, register_global_event;
"\nEvent handling and navigation target routing module.\n\nThis is the core event system that handles:\n- Global event delegation (click, submit, keypress) with selector matching.\n- URL processing with template placeholder substitution ([[variable]]).\n- Navigation target dispatching: inline, popup, tab, subpage, subframe, etc.\n- Dialog creation and lifecycle management (modal/inline).\n- History-based close/back navigation for subpages and subframes.\n\nThe EVENT_CLICK_TAB table maps target names to handler functions:\n    Target types: inline, inline_edit, inline_info, inline_delete,\n    popup, popup_edit, popup_info, popup_delete, popup_error,\n    _top, _self, _parent, page, subpage, subframe,\n    refresh_frame, close_frame, refresh_page, refresh_app, message, null\n\nDependencies (pscript cross-module):\n    pytigon_js.tabmenu: get_menu\n    pytigon_js.tools: Loading, is_visible, correct_href, ajax_get,\n                      get_template, super_insert, remove_element,\n                      process_resize, can_popup, get_elem_from_string\n    pytigon_js.ajax_region: get_ajax_region, refresh_ajax_frame, mount_html\n";
EVENT_TAB = [];
REGISTERED_EVENT_TYPES = [];
_check_element = function flx__check_element (element, selector) {
    var sel, tag, x;
    // Check if an element matches a CSS-like selector.
    // 
    //     Supports tag.class, #id, and plain tag selectors.
    // 
    //     Args:
    //         element: DOM element to test.
    //         selector: Selector string (e.g. 'a.menu-href', '#myid', 'button').
    // 
    //     Returns:
    //         bool: True if the element matches the selector.
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
    // Extract a title from element attributes or response data.
    // 
    //     Priority: element's title attribute > data's <title> tag > truncated URL.
    // 
    //     Args:
    //         element: Source DOM element.
    //         data_element: Response data element (may contain <title>).
    //         url: Fallback URL for generating title.
    // 
    //     Returns:
    //         tuple: (title, title_alt) where title_alt is the alternate title
    //                from the data element (empty string if none).
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

on_global_event = function (event) {
    var element, pos, stub1_seq, stub2_itr;
    // Global event dispatcher - routes events to registered handlers.
    // 
    //     Walks up the DOM tree from the event target, checking each element
    //     against registered selectors. Stops at the body element.
    // 
    //     Args:
    //         self: The event target element.
    //         event: The DOM event object.
    stub1_seq = EVENT_TAB;
    if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
    for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
        pos = stub1_seq[stub2_itr];
        if (_pyfunc_op_equals(pos[0], event.type)) {
            element = event.target;
            while (element) {
                if (_pyfunc_truthy(_check_element(element, pos[2]))) {
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
    // Register a global event handler with optional CSS selector filter.
    // 
    //     On first registration for an event type, adds a single event listener
    //     to document.body that dispatches to all registered handlers.
    // 
    //     Args:
    //         event_type: DOM event name (e.g. 'click', 'submit', 'keypress').
    //         fun: Handler function(event, element).
    //         selector: CSS-like selector to filter target elements, or None.
    if ((!_pyfunc_op_contains(event_type, REGISTERED_EVENT_TYPES))) {
        document.body.addEventListener(event_type, on_global_event);
        _pymeth_append.call(REGISTERED_EVENT_TYPES, event_type);
    }
    _pymeth_append.call(EVENT_TAB, [event_type, fun, selector]);
    return null;
};

window.register_global_event = register_global_event;
_get_value = function flx__get_value (elem, name) {
    var stub3_seq, stub4_itr, x, x1, x2, x3, xx;
    // Resolve a template variable to its value.
    // 
    //     Variables starting with '$' reference window properties.
    //     Other variables are looked up in form inputs within the current
    //     region, page, or document scope.
    // 
    //     Args:
    //         elem: jQuery element providing context for the lookup.
    //         name: Variable name (with optional '$' prefix for window scope).
    // 
    //     Returns:
    //         The resolved value, or '[[ERROR]]' if not found.
    if (_pymeth_startswith.call(name, "$")) {
        name = name.slice(1);
        if (_pyfunc_hasattr(window, name)) {
            return _pyfunc_getattr(window, name);
        }
    } else if ((elem.length > 0)) {
        x1 = elem.closest(".ajax-region");
        x2 = elem.closest(".page");
        x3 = jQuery(document);
        stub3_seq = [x1, x2, x3];
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            x = stub3_seq[stub4_itr];
            if ((x.length > 0)) {
                xx = _pymeth_find.call(x, sprintf("[name='%s']", name));
                if ((xx.length > 0)) {
                    return xx.val();
                }
            }
        }
    }
    return "[[ERROR]]";
};

process_href = function flx_process_href (href, elem) {
    var pos, process, ret, stub5_seq, stub6_itr, value, x1, x2;
    // Replace [[variable]] placeholders in a URL with actual values.
    // 
    //     Placeholders are resolved via _get_value. If a value is None,
    //     the placeholder is replaced with an empty string.
    // 
    //     Args:
    //         href: URL string possibly containing [[...]] placeholders.
    //         elem: jQuery element providing context for value resolution.
    // 
    //     Returns:
    //         str: The processed URL with placeholders replaced.
    ret = [];
    if ((_pyfunc_op_contains("[[", href) && _pyfunc_op_contains("]]", href))) {
        x1 = _pymeth_split.call(href, "[[");
        process = false;
        stub5_seq = x1;
        if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
        for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
            pos = stub5_seq[stub6_itr];
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
    var pos, stub7_seq, stub8_itr, url;
    // Look up the handler for a given target type in EVENT_CLICK_TAB.
    // 
    //     Args:
    //         target_element: The clicked DOM element.
    //         target: Target name (e.g. 'inline', 'popup', '_top').
    //         href: The URL being navigated to.
    // 
    //     Returns:
    //         tuple: (url, callback) or (None, None) if no match found.
    stub7_seq = EVENT_CLICK_TAB;
    if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
    for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
        pos = stub7_seq[stub8_itr];
        if ((_pyfunc_op_equals(pos[0], "*") || _pyfunc_op_equals(pos[0], target))) {
            if ((_pyfunc_op_equals(pos[1], "*") || target_element.classList.contains(pos[1]))) {
                url = correct_href(href, [target_element]);
                return [url, pos[4]];
            }
        }
    }
    return [null, null];
};

on_click_default_action = function flx_on_click_default_action (event, target_element) {
    var _callback2, _get_or_post, callback, href, obj, param, ret, src_obj, stub10_, target, tmp_url1, tmp_url2, url;
    // Handle click/submit events and route to the appropriate action.
    // 
    //     This is the main event handler for navigation. It:
    //     1. Resolves data-link indirection.
    //     2. Extracts href/action/src from the target element.
    //     3. Determines the target type and finds the matching handler.
    //     4. For forms: detects file uploads, PDF/ODF generation.
    //     5. Executes GET/POST AJAX requests with loading indicators.
    //     6. Routes responses through the target handler callbacks.
    // 
    //     Args:
    //         event: The DOM event object.
    //         target_element: The clicked/submitted element.
    // 
    //     Returns:
    //         True if the event was handled (prevent default navigation),
    //         None for _blank target (allow default).
    if (_pyfunc_truthy(target_element.hasAttribute("data-link"))) {
        obj = super_query_selector(target_element, target_element.getAttribute("data-link"));
        if (_pyfunc_truthy(obj)) {
            tmp_url1 = window.element_get_url(obj);
            tmp_url2 = window.element_get_url(target_element);
            if ((((!_pyfunc_op_equals(tmp_url1, null))) && _pyfunc_truthy(tmp_url2))) {
                element_set_url(obj, join_urls(tmp_url1, tmp_url2));
            }
            _pyfunc_setattr(obj, "data", target_element);
            ret = on_click_default_action(event, obj);
            _pyfunc_setattr(obj, "data", null);
            return ret;
        }
    }
    target = target_element.getAttribute("target");
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
        var _callback, _callback_on_error, loading, req;
        data2 = (data2 === undefined) ? null: data2;
        // Execute the AJAX request and route the response.
        req = null;
        loading = new Loading(target_element);
        loading.create();
        loading.start();
        _callback = (function flx__callback (data) {
            var data_element, element, new_callback, new_target, new_target_elem, new_url, stub9_;
            // Process the AJAX response and dispatch to the handler.
            element = null;
            loading.stop();
            loading.remove();
            data_element = get_elem_from_string(data);
            if ((_pyfunc_op_equals(data_element.nodeName, "META") && (_pyfunc_truthy(data_element.hasAttribute("name"))) && ((_pyfunc_op_equals(data_element.getAttribute("name"), "target"))))) {
                new_target_elem = data_element;
            } else {
                new_target_elem = data_element.querySelector("meta[name='target']");
            }
            if (_pyfunc_truthy(new_target_elem)) {
                new_target = new_target_elem.getAttribute("content");
            } else {
                new_target = null;
            }
            if ((_pyfunc_truthy(new_target) && ((!_pyfunc_op_equals(new_target, target))))) {
                stub9_ = _get_click_event_from_tab(target_element, new_target, url);
                new_url = stub9_[0];new_callback = stub9_[1];
                element = new_callback(target_element, data_element, new_url, param, event);
            } else {
                element = callback(target_element, data_element, url, param, event);
            }
            return element;
        }).bind(this);

        _callback_on_error = (function flx__callback_on_error (req) {
            // Handle AJAX errors.
            loading.stop();
            loading.remove();
            window.standard_error_handler(req);
            return null;
        }).bind(this);

        if (_pyfunc_truthy(url)) {
            if (_pyfunc_truthy(param)) {
                req = ajax_post(url, param, _callback, _callback_on_error);
            } else {
                req = ajax_get(url, _callback, _callback_on_error);
            }
        } else {
            _callback(data2);
        }
        return null;
    }).bind(this);

    stub10_ = _get_click_event_from_tab(target_element, target, href);
    url = stub10_[0];callback = stub10_[1];
    if (_pyfunc_truthy(callback)) {
        if (_pyfunc_op_equals(param, "file")) {
            _callback2 = (function flx__callback2 (data2) {
                _get_or_post(null, callback, data2);
                return null;
            }).bind(this);

            ajax_submit(target_element, _callback2, null, null, null);
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
    // Handle menu link clicks with mobile collapse support.
    // 
    //     If the navbar toggler is visible (mobile view), collapses the menu
    //     first and then processes the click after the collapse animation.
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
    return null;
};

register_global_event("click", _on_menu_click, "a.menu-href");
register_global_event("click", on_click_default_action, "a");
register_global_event("click", on_click_default_action, "button");
register_global_event("submit", on_click_default_action, "form");
create_event_handler = function flx_create_event_handler (href, target, position) {
    var _handler;
    target = (target === undefined) ? "inline_info": target;
    position = (position === undefined) ? "div.page.active": position;
    // Create a synthetic click event handler for programmatic navigation.
    // 
    //     Creates a temporary <a> element, attaches it to the DOM, simulates
    //     a click, and returns a handler function.
    // 
    //     Args:
    //         href: URL to navigate to.
    //         target: Target type (default 'inline_info').
    //         position: CSS selector for where to attach the temporary element.
    // 
    //     Returns:
    //         A handler function that triggers the navigation when called.
    _handler = (function flx__handler (event) {
        var a;
        a = document.createElement("a");
        a.setAttribute("href", href);
        a.setAttribute("target", target);
        (document.querySelector(position).appendChild)(a);
        on_click_default_action(event.originalEvent, a);
        return false;
    }).bind(this);

    return _handler;
};

window.create_event_handler = create_event_handler;
_get_scrolled_parent = function flx__get_scrolled_parent (node) {
    // Find the nearest scrollable ancestor of a node.
    // 
    //     Args:
    //         node: Starting DOM node.
    // 
    //     Returns:
    //         The first ancestor with scrollHeight > clientHeight, or None.
    if (_pyfunc_op_equals(node, null)) {
        return null;
    }
    if ((node.scrollHeight > node.clientHeight)) {
        return node;
    } else {
        return _get_scrolled_parent(node.parentNode);
    }
    return null;
};

_on_inline = function flx__on_inline (target_element, data_element, url, param, event, template_name) {
    var _on_click, bottom, btn, child, content, dialog, dialog_slot, dialog_slot2, dy, height, inline_position, item, on_hidden, plug, rect1, rect2, scroll_frame, stub11_seq, stub12_itr, sy, top, top2, txt, viewportOffset;
    // Create an inline (non-modal) dialog within the page flow.
    // 
    //     Inline dialogs are embedded in the page rather than floating as modals.
    //     They can be positioned after a table row (tr), in a div slot, or within
    //     a plug container.
    // 
    //     Features:
    //     - Auto-scrolling to keep the dialog visible.
    //     - Copy-to-clipboard support for INFO dialogs.
    //     - Maximize/minimize via CSS classes.
    //     - After-close refresh callbacks.
    // 
    //     Args:
    //         target_element: The element that triggered the dialog.
    //         data_element: The content to display.
    //         url: Source URL (may contain after_close= parameter).
    //         param: Request parameters.
    //         event: The triggering DOM event.
    //         template_name: Template key (INLINE, INLINE_EDIT, INLINE_INFO, ...).
    // 
    //     Returns:
    //         The created dialog slot DOM element.
    inline_position = target_element.getAttribute("data-inline-position");
    if ((_pyfunc_truthy(inline_position) && (_pyfunc_truthy(_pymeth_endswith.call(((_pymeth_split.call(inline_position, ":")[0])), "tr"))))) {
        dialog_slot = document.createElement("tr");
        child = document.createElement("td");
        child.setAttribute("colspan", "100");
        dialog_slot.appendChild(child);
        dialog_slot2 = child;
    } else {
        dialog_slot = document.createElement("div");
        dialog_slot.classList.add("dialog-slot");
        dialog_slot.classList.add("col-12");
        dialog_slot2 = dialog_slot;
    }
    dialog_slot.classList.add("plug");
    dialog_slot2.innerHTML = get_template(_pymeth_replace.call(template_name, "MODAL", "INLINE"), ({title: _get_title(target_element, data_element, url)[0], href: url}));
    target_element.setAttribute("data-style", "zoom-out");
    target_element.setAttribute("data-spinner-color", "#FF0000");
    content = dialog_slot.querySelector("div.dialog-data");
    if ((((_pyfunc_op_equals(_pymeth_lower.call(data_element.tagName), "div"))) && (_pyfunc_truthy(data_element.classList.contains("ajax-temp-item"))))) {
        stub11_seq = Array.prototype.slice.call(data_element.childNodes);
        if ((typeof stub11_seq === "object") && (!Array.isArray(stub11_seq))) { stub11_seq = Object.keys(stub11_seq);}
        for (stub12_itr = 0; stub12_itr < stub11_seq.length; stub12_itr += 1) {
            item = stub11_seq[stub12_itr];
            content.appendChild(item);
        }
    } else {
        content.appendChild(data_element);
    }
    super_insert(target_element, inline_position, dialog_slot);
    mount_html(dialog_slot, null);
    if (_pyfunc_truthy(data_element.classList.contains("maximized"))) {
        inline_maximize(data_element);
    }
    on_hidden = function (event) {
        var obj, region, x;
        // Clean up the dialog when closed.
        region = get_ajax_region(target_element, target_element.getAttribute("data-region"));
        if (_pyfunc_truthy(region)) {
            obj = region.querySelector(".plug");
            obj.remove();
            if (_pyfunc_op_contains("after_close=", url)) {
                x = _pymeth_split.call(url, "after_close=")[1];
                if (_pymeth_startswith.call(x, "refresh")) {
                    window.refresh_ajax_frame(region);
                }
            }
        }
        return false;
    };

    dialog = dialog_slot.firstElementChild;
    if ((!_pyfunc_op_equals(dialog, null))) {
        (jQuery(dialog).on)("click", "button.ptig-btn-close", on_hidden);
    }
    plug = dialog.closest("aside.plug");
    if ((!_pyfunc_op_equals(plug, null))) {
        viewportOffset = dialog.getBoundingClientRect();
        top = viewportOffset.top;
        bottom = _pyfunc_op_add(top, viewportOffset.height);
        height = window.innerHeight;
        if ((bottom > height)) {
            if ((height > viewportOffset.height)) {
                top2 = (height - viewportOffset.height) / 2;
            } else {
                top2 = 0;
            }
            dy = top - top2;
            scroll_frame = plug.firstElementChild;
            sy = scroll_frame.scrollTop;
            scroll_frame.scrollTop = _pyfunc_op_add(dy, sy);
        }
    } else {
        plug = dialog.closest(".plug");
        if ((!_pyfunc_op_equals(plug, null))) {
            scroll_frame = _get_scrolled_parent(plug);
            if ((!_pyfunc_op_equals(scroll_frame, null))) {
                rect1 = dialog.getBoundingClientRect();
                rect2 = scroll_frame.getBoundingClientRect();
                sy = scroll_frame.scrollTop;
                if ((rect1.top > rect2.top)) {
                    if ((rect1.height < rect2.height)) {
                        if ((_pyfunc_op_add(rect1.top, rect1.height) > _pyfunc_op_add(rect2.top, rect2.height))) {
                            scroll_frame.scrollTop = _pyfunc_op_add(_pyfunc_int(sy), (_pyfunc_op_add(rect1.top, rect1.height) - _pyfunc_op_add(rect2.top, rect2.height)));
                        }
                    } else {
                        scroll_frame.scrollTop = _pyfunc_op_add(_pyfunc_int(sy), (rect1.top - rect2.top));
                    }
                } else {
                    scroll_frame.scrollTop = _pyfunc_op_add(_pyfunc_int(sy), (rect1.top - rect2.top));
                }
            }
        }
    }
    if (_pyfunc_op_contains("INFO", template_name)) {
        txt = dialog_slot.querySelector("textarea.copy_to_clipboard");
        btn = dialog_slot.querySelector("button.copy_to_clipboard");
        if (_pyfunc_truthy(btn)) {
            if ((_pyfunc_truthy(txt) && _pyfunc_truthy(txt.value))) {
                btn.style.display = "block";
                _on_click = (function flx__on_click () {
                    txt.select();
                    document.execCommand("copy");
                    return null;
                }).bind(this);

                btn.addEventListener("click", _on_click);
            } else {
                btn.style.display = "none";
            }
        }
    }
    return dialog_slot;
};

window._on_inline = _on_inline;
on_inline = function flx_on_inline (target_element, data_element, new_url, param, event) {
    // Create an inline dialog with INLINE template.
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE");
};

window.on_inline = on_inline;
on_inline_edit_new = function flx_on_inline_edit_new (target_element, data_element, new_url, param, event) {
    // Create an inline edit dialog.
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_EDIT");
};

window.on_inline_edit_new = on_inline_edit_new;
on_inline_info = function flx_on_inline_info (target_element, data_element, new_url, param, event) {
    // Create an inline info dialog with copy-to-clipboard.
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_INFO");
};

window.on_inline_info = on_inline_info;
window.on_inline_inf = on_inline_info;
on_inline_delete = function flx_on_inline_delete (target_element, data_element, new_url, param, event) {
    // Create an inline delete confirmation dialog.
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_DELETE");
};

window.on_inline_delete = on_inline_delete;
on_inline_error = function flx_on_inline_error (target_element, data_element, new_url, param, event) {
    // Create an inline error dialog.
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE_ERROR");
};

window.on_inline_error = on_inline_error;
_on_popup = function flx__on_popup (target_element, data_element, url, param, event, template_name) {
    var _on_click, btn, content, dialog, dialog_slot, on_hidden, region, txt;
    // Create a Bootstrap modal popup dialog.
    // 
    //     Falls back to inline mode if a modal is already open (to avoid
    //     stacking modals).
    // 
    //     Features:
    //     - Bootstrap 5 Modal with backdrop support.
    //     - Draggable via jQuery drags plugin.
    //     - Copy-to-clipboard for INFO dialogs.
    //     - After-close refresh callbacks.
    // 
    //     Args:
    //         target_element: The element that triggered the popup.
    //         data_element: The content to display.
    //         url: Source URL (may contain after_close= parameter).
    //         param: Request parameters.
    //         event: The triggering DOM event.
    //         template_name: Template key (MODAL, MODAL_EDIT, MODAL_INFO, ...).
    // 
    //     Returns:
    //         The created dialog content element.
    if ((!_pyfunc_truthy(can_popup()))) {
        return _on_inline(target_element, data_element, url, param, event, template_name);
    }
    dialog_slot = document.createElement("aside");
    dialog_slot.setAttribute("class", "plug");
    dialog_slot.innerHTML = get_template(template_name, ({title: _get_title(target_element, data_element, url)[0], href: url}));
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
        var obj, x;
        // Clean up the popup when hidden.
        obj = region.querySelector(".plug");
        if (_pyfunc_truthy(obj)) {
            obj.remove();
        }
        if (_pyfunc_op_contains("after_close=", url)) {
            x = _pymeth_split.call(url, "after_close=")[1];
            if (_pymeth_startswith.call(x, "refresh")) {
                window.refresh_ajax_frame(region);
            }
        }
        return false;
    };

    if (_pyfunc_truthy(window.hasOwnProperty("bootstrap"))) {
        dialog_slot.firstElementChild.addEventListener("hidden.bs.modal", on_hidden);
        dialog = new window.bootstrap.Modal(dialog_slot.firstElementChild, ({backdrop: false}));
        if (_pyfunc_truthy(dialog)) {
            dialog.show();
            (jQuery(dialog_slot).drags)(({handle: ".modal-header"}));
        }
    } else {
        dialog = jQuery(dialog_slot.firstElementChild);
        if (_pyfunc_truthy(dialog)) {
            dialog.on("hidden.bs.modal", on_hidden);
            dialog.drags(({handle: ".modal-header"}));
            dialog.modal(({show: true, backdrop: false}));
        }
    }
    if (_pyfunc_op_contains("INFO", template_name)) {
        txt = dialog_slot.querySelector("textarea.copy_to_clipboard");
        btn = dialog_slot.querySelector("button.copy_to_clipboard");
        if (_pyfunc_truthy(btn)) {
            if ((_pyfunc_truthy(txt) && _pyfunc_truthy(txt.value))) {
                btn.style.display = "block";
                _on_click = (function flx__on_click () {
                    txt.select();
                    document.execCommand("copy");
                    return null;
                }).bind(this);

                btn.addEventListener("click", _on_click);
            } else {
                btn.style.display = "none";
            }
        }
    }
    return content;
};

window._on_popup = _on_popup;
on_popup = function flx_on_popup (target_element, data_element, new_url, param, event) {
    // Create a modal popup dialog.
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL");
};

window.on_popup = on_popup;
on_popup_edit_new = function flx_on_popup_edit_new (target_element, data_element, new_url, param, event) {
    // Create a modal edit popup dialog.
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_EDIT");
};

window.on_popup_edit_new = on_popup_edit_new;
on_popup_info = function flx_on_popup_info (target_element, data_element, new_url, param, event) {
    // Create a modal info popup dialog.
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_INFO");
};

window.on_popup_info = on_popup_info;
on_popup_delete = function flx_on_popup_delete (target_element, data_element, new_url, param, event) {
    // Create a modal delete confirmation popup.
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_DELETE");
};

window.on_popup_delete = on_popup_delete;
on_popup_error = function flx_on_popup_error (target_element, data_element, new_url, param, event) {
    // Create a modal error popup.
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_ERROR");
};

window.on_popup_error = on_popup_error;
on_new_tab = function flx_on_new_tab (target_element, data_element, new_url, param, event) {
    var data_element2, stub13_, title, title_alt;
    // Open content in a new application tab (or activate existing).
    // 
    //     Extracts the title from the response and delegates to the menu system.
    stub13_ = _get_title(target_element, data_element, new_url);
    title = stub13_[0];title_alt = stub13_[1];
    data_element2 = data_element.querySelector("section.body-body");
    if ((!_pyfunc_truthy(data_element2))) {
        data_element2 = data_element;
    }
    return (get_menu().on_menu_href)(target_element, data_element2, title, title_alt, new_url);
};

window.on_new_tab = on_new_tab;
on_replace_app = function flx_on_replace_app (target_element, data_element, new_url, param, event) {
    var obj, objects, stub14_seq, stub15_itr, subpage, subpages, wrapper;
    // Replace the entire application content (for _top targets).
    // 
    //     Clears the current content wrapper, mounts new content from the
    //     response's body-body section, reinitializes the start page, and
    //     re-activates the menu. Preserves subpage navigation if present.
    subpages = ((new URLSearchParams(window.location.search)).getAll)("subpage");
    if (_pyfunc_truthy(subpages)) {
        subpage = subpages[0];
    } else {
        subpage = null;
    }
    if (_pyfunc_truthy(window.PUSH_STATE)) {
        history_push_state("", window.BASE_PATH);
    } else {
        window.location.pathname = window.BASE_PATH;
    }
    window.MENU = null;
    wrapper = document.querySelector("div.content-wrapper");
    if (_pyfunc_truthy(wrapper)) {
        wrapper.innerHTML = "";
    }
    mount_html(wrapper, data_element.querySelector("section.body-body"), false);
    window.init_start_page();
    window.activate_menu();
    if (_pyfunc_truthy(subpage)) {
        objects = Array.prototype.slice.call(document.querySelectorAll("a"));
        stub14_seq = objects;
        if ((typeof stub14_seq === "object") && (!Array.isArray(stub14_seq))) { stub14_seq = Object.keys(stub14_seq);}
        for (stub15_itr = 0; stub15_itr < stub14_seq.length; stub15_itr += 1) {
            obj = stub14_seq[stub15_itr];
            if ((_pyfunc_truthy(obj.href) && (_pyfunc_truthy(obj.classList.contains("menu-href"))))) {
                if (_pyfunc_op_contains(subpage, obj.href)) {
                    obj.click();
                    break;
                }
            }
        }
    }
    return wrapper;
};

_on_subframe = function flx__on_subframe (frame_element, target_element, data_element, url, param, event) {
    var stack_slot;
    // Push new content onto the subframe stack.
    // 
    //     Saves the current frame content into a hidden stack-slot and
    //     replaces it with new data.
    stack_slot = document.createElement("div");
    stack_slot.style.display = "none";
    stack_slot.classList.add("stack-slot");
    while (frame_element.childNodes.length > 0) {
        stack_slot.appendChild(frame_element.childNodes[0]);
    }
    mount_html(frame_element, data_element);
    frame_element.prepend(stack_slot);
    return null;
};

on_subpage = function flx_on_subpage (target_element, data_element, new_url, param, event) {
    var page;
    // Navigate to a subpage within the current page.
    page = target_element.closest(".page");
    return _on_subframe(page, target_element, data_element, new_url, param, event);
};

window.on_subpage = on_subpage;
on_subframe = function flx_on_subframe (target_element, data_element, new_url, param, event) {
    var frame;
    // Navigate to a subframe (within an ajax-frame or data-link target).
    if (_pyfunc_truthy(target_element.hasAttribute("data-link"))) {
        frame = super_query_selector(target_element, target_element.getAttribute("data-link"));
    } else {
        frame = target_element.closest(".ajax-frame");
    }
    return _on_subframe(frame, target_element, data_element, new_url, param, event);
};

window.on_subframe = on_subframe;
_on_close_subpage = function flx__on_close_subpage (page, target_element, data_element, new_url, param, event) {
    var _on_remove, child, count, stack_slot, temp_slot;
    // Pop the subpage/subframe stack, restoring previous content.
    // 
    //     Removes 'count' levels of stack-slots from the page.
    if (_pyfunc_truthy(target_element.hasAttribute("subpage-count"))) {
        count = _pyfunc_int(target_element.getAttribute("subpage-count"));
    } else {
        count = 1;
    }
    temp_slot = document.createElement("div");
    if ((page.childNodes.length > 0)) {
        child = page.childNodes[0];
        if (_pyfunc_truthy(((!_pyfunc_truthy(child))) || ((!_pyfunc_hasattr(child, "classList"))) || (!_pyfunc_truthy(child.classList.contains("stack-slot"))))) {
            return null;
        }
        temp_slot.appendChild(child);
    }
    _on_remove = (function flx__on_remove (index, value) {
        value.on_remove();
        return null;
    }).bind(this);

    jQuery.each(_pymeth_find.call(jQuery(page), ".call_on_remove"), _on_remove);
    stack_slot = temp_slot.childNodes[0];
    while (count > 1) {
        child = stack_slot.childNodes[0];
        if (_pyfunc_truthy(((!_pyfunc_truthy(child))) || ((!_pyfunc_hasattr(child, "classList"))) || (!_pyfunc_truthy(child.classList.contains("stack-slot"))))) {
            break;
        }
        stack_slot = child;
        count -= 1;
    }
    page.innerHTML = "";
    while (stack_slot.childNodes.length > 0) {
        page.appendChild(stack_slot.childNodes[0]);
    }
    return page;
};

on_close_subpage = function flx_on_close_subpage (target_element, data_element, new_url, param, event) {
    var page;
    // Close the current subpage and restore the previous one.
    page = target_element.closest(".page");
    return _on_close_subpage(page, target_element, data_element, new_url, param, event);
};

on_close_subpage_and_refresh = function flx_on_close_subpage_and_refresh (target_element, data_element, new_url, param, event) {
    var page, ret;
    // Close subpage and refresh the parent frame.
    page = target_element.closest(".page");
    ret = on_close_subpage(target_element, data_element, new_url, param, event);
    window.refresh_ajax_frame(page);
    return ret;
};

on_close_subframe = function flx_on_close_subframe (target_element, data_element, new_url, param, event) {
    var frame;
    // Close the current subframe and restore previous content.
    if (_pyfunc_truthy(target_element.hasAttribute("data-link"))) {
        frame = super_query_selector(target_element, target_element.getAttribute("data-link"));
    } else {
        frame = target_element.closest(".ajax-frame");
    }
    return _on_close_subpage(frame, target_element, data_element, new_url, param, event);
};

on_close_subframe_and_refresh = function flx_on_close_subframe_and_refresh (target_element, data_element, new_url, param, event) {
    var frame, ret;
    // Close subframe and refresh the parent.
    if (_pyfunc_truthy(target_element.hasAttribute("data-link"))) {
        frame = super_query_selector(target_element, target_element.getAttribute("data-link"));
    } else {
        frame = target_element.closest(".ajax-frame");
    }
    ret = on_close_subframe(target_element, data_element, new_url, param, event);
    window.refresh_ajax_frame(frame);
    return ret;
};

close_frame = function flx_close_frame (target_element, data_element, new_url, param, event, data_region) {
    var _callback, _callback_on_error, aside, data_element2, data_region2, dialog, f, region;
    data_region = (data_region === undefined) ? null: data_region;
    // Close a dialog/frame and optionally refresh the parent region.
    // 
    //     Handles both modal (Bootstrap) and inline plug dismissal,
    //     with opacity feedback during the close operation.
    // 
    //     Args:
    //         target_element: The element that triggered the close.
    //         data_element: Response data to mount after close.
    //         data_region: Optional region name override.
    f = target_element.getAttribute("data-link");
    if (_pyfunc_truthy(f)) {
        data_element2 = super_query_selector(data_element, f);
    } else {
        data_element2 = data_element;
    }
    if (_pyfunc_truthy(data_region)) {
        data_region2 = data_region;
    } else {
        data_region2 = target_element.getAttribute("data-region");
    }
    region = get_ajax_region(get_ajax_region(target_element, "page").parentElement, data_region2);
    dialog = null;
    aside = target_element.closest(".plug");
    if ((_pyfunc_truthy(aside) && (_pyfunc_truthy(region.contains(aside))))) {
        dialog = aside.firstElementChild;
    } else {
        aside = null;
    }
    _callback = (function flx__callback () {
        // After successful refresh, dismiss the dialog.
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
        // On error, restore dialog opacity.
        if (_pyfunc_truthy(aside)) {
            aside.style.opacity = "100%";
        }
        return null;
    }).bind(this);

    if (_pyfunc_truthy(aside)) {
        aside.style.opacity = "50%";
    }
    return refresh_ajax_frame(target_element, data_region2, data_element2, _callback, _callback_on_error);
};

refresh_frame = function flx_refresh_frame (target_element, data_element, new_url, param, event, data_region) {
    var data_element2, data_region2, f;
    data_region = (data_region === undefined) ? null: data_region;
    // Refresh a frame with new content.
    // 
    //     Args:
    //         target_element: Element to use for region lookup.
    //         data_element: New content to mount.
    //         data_region: Optional region name for the frame to refresh.
    f = target_element.getAttribute("data-link");
    if (_pyfunc_truthy(f)) {
        data_element2 = super_query_selector(data_element, f);
    } else {
        data_element2 = data_element;
    }
    if (_pyfunc_truthy(data_region)) {
        data_region2 = data_region;
    } else {
        data_region2 = target_element.getAttribute("data-region");
    }
    return refresh_ajax_frame(target_element, data_region2, data_element2);
};

refresh_page = function flx_refresh_page (target_element, data_element, new_url, param, event) {
    // Refresh the page-content region of the current page.
    return refresh_frame(target_element, data_element, new_url, param, event, "page-content");
};

refresh_app = function flx_refresh_app (target_element, data_element, new_url, param, event) {
    // Reload the entire application by navigating to the base path.
    window.location.href = window.BASE_PATH;
    return null;
};

only_get = function flx_only_get (target_element, data_element, url, param, event) {
    // No-op handler for background GET requests (no UI update).
    return null;
};

on_message = function flx_on_message (target_element, data_element, new_url, param, event) {
    var options;
    // Display a SweetAlert2 message dialog.
    // 
    //     Reads icon, title, text, footer, and timer from data attributes
    //     on either the target_element or the data_element.
    options = ({icon: "success", title: "Information", text: "success"});
    if (_pyfunc_truthy(target_element.hasAttribute("data-icon"))) {
        options["icon"] = target_element.getAttribute("data-icon");
    } else if (_pyfunc_truthy(data_element.hasAttribute("data-icon"))) {
        options["icon"] = data_element.getAttribute("data-icon");
    }
    if (_pyfunc_truthy(target_element.hasAttribute("data-title"))) {
        options["title"] = target_element.getAttribute("data-title");
    } else if (_pyfunc_truthy(data_element.hasAttribute("data-title"))) {
        options["title"] = data_element.getAttribute("data-title");
    }
    if (_pyfunc_truthy(target_element.hasAttribute("data-text"))) {
        options["text"] = target_element.getAttribute("data-text");
    } else if (_pyfunc_truthy(data_element.hasAttribute("data-text"))) {
        options["text"] = data_element.getAttribute("data-text");
    }
    if (_pyfunc_truthy(target_element.hasAttribute("data-footer"))) {
        options["footer"] = target_element.getAttribute("data-footer");
    } else if (_pyfunc_truthy(data_element.hasAttribute("data-footer"))) {
        options["footer"] = data_element.getAttribute("data-footer");
    }
    if (_pyfunc_truthy(target_element.hasAttribute("data-timer"))) {
        options["timer"] = target_element.getAttribute("data-timer");
    } else if (_pyfunc_truthy(data_element.hasAttribute("data-timer"))) {
        options["timer"] = data_element.getAttribute("data-timer");
    }
    Swal.fire(options);
    return null;
};

EVENT_CLICK_TAB = [["inline", "*", true, false, on_inline], ["inline_edit", "*", true, false, on_inline_edit_new], ["inline_info", "*", true, false, on_inline_info], ["inline_delete", "*", true, false, on_inline_delete], ["inline_error", "*", true, false, on_inline_error], ["popup", "*", true, false, on_popup], ["popup_edit", "*", true, false, on_popup_edit_new], ["popup_info", "*", true, false, on_popup_info], ["popup_delete", "*", true, false, on_popup_delete], ["popup_error", "*", true, false, on_popup_error], ["_top", "*", false, false, on_replace_app], ["_top2", "*", true, false, on_new_tab], ["_self", "*", true, false, refresh_page], ["_parent", "*", true, false, on_new_tab], ["page", "*", true, false, on_new_tab], ["refresh_frame", "*", true, false, refresh_frame], ["close_frame", "*", true, false, close_frame], ["refresh_page", "*", true, false, refresh_page], ["refresh_app", "*", false, false, refresh_app], ["message", "*", false, false, on_message], ["subpage", "*", true, false, on_subpage], ["subframe", "*", true, false, on_subframe], ["*", "close-subpage", true, false, on_close_subpage], ["*", "close-subpage-and-refresh", true, false, on_close_subpage_and_refresh], ["*", "close-subframe", true, false, on_close_subframe], ["*", "close-subframe-and-refresh", true, false, on_close_subframe_and_refresh], ["null", "*", false, false, only_get]];
on_resize = function (event) {
    // Global window resize handler - triggers process_resize on body.
    process_resize(document.body);
    return null;
};

window.addEventListener("resize", on_resize);
export {on_global_event, register_global_event, process_href, on_click_default_action, create_event_handler, on_inline, on_inline_edit_new, on_inline_info, on_inline_delete, on_inline_error, on_popup, on_popup_edit_new, on_popup_info, on_popup_delete, on_popup_error, on_new_tab, on_replace_app, on_subpage, on_subframe, on_close_subpage, on_close_subpage_and_refresh, on_close_subframe, on_close_subframe_and_refresh, close_frame, refresh_frame, refresh_page, refresh_app, only_get, on_message, on_resize};

var install_service_worker, service_worker_and_indexedDB_test;
"\nOffline support module for PWA (Progressive Web Application) functionality.\n\nProvides service worker installation and browser capability detection\nfor offline operation with IndexedDB.\n";
install_service_worker = function flx_install_service_worker () {
    var err, reg;
    // Register the service worker for offline support and PWA capabilities.
    // 
    //     Attempts to register 'sw.js' as a service worker. Logs the worker state
    //     and listens for state changes. Falls back gracefully if service workers
    //     are not supported by the browser.
    if (_pyfunc_hasattr(navigator, "serviceWorker")) {
        reg = (function flx_reg (registration) {
            var onstatechange, serviceWorker;
            // Callback invoked after successful service worker registration.
            // 
            //             Determines the active service worker instance (installing, waiting,
            //             or active) and sets up a state change listener for debugging.
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
                    // Log state transitions of the service worker.
                    console.log(e.target.state);
                    return null;
                };

                serviceWorker.addEventListener("statechange", onstatechange);
            }
            return null;
        }).bind(this);

        err = (function flx_err (error) {
            // Log service worker registration errors.
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
    // Check whether the browser supports both service workers and IndexedDB.
    // 
    //     Also verifies the connection is over HTTPS or localhost (required for
    //     service worker registration by the Secure Contexts spec).
    // 
    //     Returns:
    //         bool: True if offline support is available, False otherwise.
    if ((_pyfunc_hasattr(navigator, "serviceWorker") && _pyfunc_hasattr(window, "indexedDB") && ((_pyfunc_op_equals(location.hostname, "localhost") || _pyfunc_op_equals(location.hostname, "127.0.0.1") || _pyfunc_op_equals(location.hostname, "127.0.0.2") || _pyfunc_op_equals(location.protocol, "https:"))))) {
        return true;
    } else {
        return false;
    }
    return null;
};

export {install_service_worker, service_worker_and_indexedDB_test};

var Page, TabMenu, TabMenuItem, get_menu;
"\nTab-based navigation menu system.\n\nProvides a multi-tab page management system that creates and manages\nBootstrap tab panels for navigation. Supports:\n- Creating new tabs with dynamic content loading.\n- Activating existing tabs by title.\n- Removing tabs and cleaning up associated DOM elements.\n- Push state history integration for back/forward navigation.\n- Different behavior based on APPLICATION_TEMPLATE setting.\n\nClasses:\n    Page: Represents an active page/tab in the UI.\n    TabMenuItem: Metadata for a single menu tab item.\n    TabMenu: Core tab management engine.\n";
Page = function () {
    // Represents an active page (tab pane) in the UI.
    // 
    //     Associates a tab DOM element with its identifier and tracks
    //     the current href for history management.
    // 
    //     Attributes:
    //         id: Unique tab identifier (string).
    //         page: jQuery-wrapped tab pane DOM element.
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
    // Store the href associated with this page for history.
    this.page.attr("_href", href);
    return null;
};

Page.prototype.get_href = function () {
    // Retrieve the stored href for this page.
    return this.page.attr("_href");
};


TabMenuItem = function () {
    // Metadata for a single tab in the menu system.
    // 
    //     Attributes:
    //         id: Unique DOM identifier for the tab (string).
    //         title: Display title of the tab (trimmed).
    //         url: Navigation URL associated with the tab.
    //         data: Optional content data for the tab.
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
    // Core manager for the Bootstrap-based tab navigation system.
    // 
    //     Creates and manages tab elements in the #tabs2 container, handling
    //     tab creation, activation, removal, and browser history integration.
    // 
    //     The menu behavior differs by APPLICATION_TEMPLATE:
    //         - 'modern': Uses the full tab system with history push state.
    //         - Other: Uses simpler body_desktop content replacement.
    _pyfunc_op_instantiate(this, arguments);
}
TabMenu.prototype._base_class = Object;
TabMenu.prototype.__name__ = "TabMenu";

TabMenu.prototype.__init__ = function () {
    // Initialize the tab menu with an empty state.
    this.id = 0;
    this.titles = ({});
    this.active_item = null;
    return null;
};

TabMenu.prototype.get_active_item = function () {
    // Return the currently active TabMenuItem, or None.
    return this.active_item;
};

TabMenu.prototype.is_open = function (title) {
    // Check whether a tab with the given title is currently open.
    // 
    //         Args:
    //             title: Tab title to check.
    // 
    //         Returns:
    //             bool: True if the tab exists and is open.
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
    // Activate an existing tab by its title.
    // 
    //         Shows the tab panel and optionally pushes a history state entry.
    // 
    //         Args:
    //             title: Title of the tab to activate.
    //             push_state: If True (and window.PUSH_STATE is True), push
    //                 a history entry for back/forward navigation.
    menu_item = this.titles[title];
    ((jQuery(sprintf("#li_%s a", menu_item.id))).tab)("show");
    if ((_pyfunc_truthy(push_state) && _pyfunc_truthy(window.PUSH_STATE))) {
        history_push_state(menu_item.title, menu_item.url);
    }
    return null;
};

TabMenu.prototype.register = function (title) {
    // Pre-register a tab title (marks it as reserved with '$$$').
    // 
    //         Args:
    //             title: Title to reserve in the tab registry.
    this.titles[title] = "$$$";
    return null;
};

TabMenu.prototype.new_page = function (title, data_or_html, href, title_alt) {
    var _id, _local_fun, _on_button_click, _on_show_tab, append_left, menu_item, menu_pos, scripts;
    title_alt = (title_alt === undefined) ? null: title_alt;
    // Create a new tab page with content.
    // 
    //         Builds the tab navigation element (#tabs2 li), the tab content
    //         pane (#tabs2_content div), mounts the provided HTML content,
    //         and binds tab events (show, close button, inline scripts).
    // 
    //         Args:
    //             title: Display title for the new tab.
    //             data_or_html: HTML content or DOM element to mount in the tab.
    //             href: URL associated with the tab (for history and reloading).
    //             title_alt: Alternative title for lookup (optional).
    // 
    //         Returns:
    //             str: The generated tab DOM id.
    _id = "tab" + this.id;
    menu_item = new TabMenuItem(_id, title, href, data_or_html);
    this.titles[title] = menu_item;
    if ((_pyfunc_truthy(title_alt) && ((!_pyfunc_op_equals(title_alt, title))))) {
        this.titles[title_alt] = menu_item;
    }
    menu_pos = vsprintf("<li id='li_%s' class ='nav-item'><a href='#%s' class='nav-link bg-info' data-toggle='tab' data-bs-toggle='tab' role='tab' title='%s'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-outline-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", [_id, _id, title, title, _id]);
    append_left = (jQuery("#tabs2").hasClass)("append-left");
    if (_pyfunc_truthy(append_left)) {
        (jQuery("#tabs2").prepend)(menu_pos);
    } else {
        _pymeth_append.call(jQuery("#tabs2"), menu_pos);
    }
    _pymeth_append.call(jQuery("#tabs2_content"), sprintf("<div class='tab-pane container-fluid ajax-region ajax-frame ajax-link win-content content page' id='%s' data-region='page' href='%s'></div>", _id, href));
    window.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
    this.active_item = menu_item;
    if (_pyfunc_truthy(window.PUSH_STATE)) {
        history_push_state(title, href);
    }
    _on_show_tab = function (e) {
        var menu;
        // Handle tab shown event: update active page and push history.
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
        // Handle close button click on the tab.
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
    // Remove a tab by its DOM id.
    // 
    //         Cleans up both the navigation element (#li_<id>) and the content
    //         pane (#<id>). Activates the last remaining tab or restores the
    //         body_desktop if no tabs remain.
    // 
    //         Args:
    //             id: The tab DOM id to remove (without '#' prefix).
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
            window.init_start_page();
        }
        (jQuery("#body_desktop").show)();
    }
    return null;
};

TabMenu.prototype.on_menu_href = function (elem, data_or_html, title, title_alt, url) {
    var href, href2;
    title_alt = (title_alt === undefined) ? null: title_alt;
    url = (url === undefined) ? null: url;
    // Handle a menu link click: either activate an existing tab or create a new one.
    // 
    //         Behavior depends on APPLICATION_TEMPLATE:
    //         - 'modern': Uses the full tab system.
    //         - Other: Replaces body_desktop content directly.
    // 
    //         Valid APPLICATION_TEMPLATE values:
    //             'standard', 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
    // 
    //         Args:
    //             elem: The clicked DOM element.
    //             data_or_html: HTML content to display.
    //             title: Title for the tab/page.
    //             title_alt: Alternative title for lookup.
    //             url: Navigation URL (falls back to elem's href if not provided).
    // 
    //         Returns:
    //             bool: False to prevent default navigation.
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
            href2 = correct_href(href);
            (jQuery("#body_desktop").hide)();
            this.new_page(title, data_or_html, href2, title_alt);
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
    // Get or create the singleton TabMenu instance.
    // 
    //     Returns:
    //         TabMenu: The global menu instance stored in window.MENU.
    if ((!_pyfunc_truthy(window.MENU))) {
        window.MENU = new TabMenu();
    }
    return window.MENU;
};

export {Page, TabMenuItem, TabMenu, get_menu};

var _is_visible, _rowStyle, datatable_action, datatable_ajax, datatable_buttons, datatable_refresh, datetable_set_height, init_table, loading_template, old_datetable_set_height, on_check_toggle_visibility, prepare0, prepare_datatable, table_loadeddata;
"\nBootstrap Table integration and data table management module.\n\nProvides initialization and lifecycle management for Bootstrap Table\nwidgets including:\n- Table height management and responsive sizing.\n- AJAX data loading with server-side pagination/sorting.\n- Row selection, checkboxes, and inline editing.\n- Table action dropdowns and toolbar expand/collapse.\n- Data change event handling (loadeddata) for table refresh.\n- Visual feedback for row-level operations.\n\nDependencies (pscript cross-module):\n    pytigon_js.tools: ajax_post, ajax_get, get_table_type, load_js\n    pytigon_js.ajax_region: refresh_ajax_frame\n";
_is_visible = function flx__is_visible (element) {
    var test;
    // Check if an element is visible using jQuery's :visible selector.
    test = jQuery(element).is(":visible");
    if (_pyfunc_truthy(test)) {
        return true;
    } else {
        return false;
    }
    return null;
};

old_datetable_set_height = function flx_old_datetable_set_height (element) {
    var details, details_height, dy, dy_win, dydy, elem, panel, table_offset;
    // Legacy table height calculation based on window/viewport offsets.
    // 
    //     Used for tables with the 'table_get' class.
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
    if (((_pyfunc_truthy((elem[0].hasAttribute)("table-details"))) && ((_pyfunc_op_equals(((elem[0].getAttribute)("table-details")), "1"))))) {
        details = super_query_selector(elem[0], "^.table-and-details/.row-details");
        details_height = details.clientHeight;
        dydy = _pyfunc_op_mult(details_height, dy_win) / 100;
    }
    dy -= dydy;
    if ((dy < 200)) {
        dy = 200;
    }
    panel = _pymeth_find.call(elem, ".fixed-table-toolbar");
    if ((!_pyfunc_truthy(_is_visible(panel)))) {
        dy = _pyfunc_op_add(dy, panel.outerHeight() + 5);
    }
    (jQuery(element).bootstrapTable)("resetView", ({height: dy - 5}));
    return null;
};

datetable_set_height = function flx_datetable_set_height (element) {
    var dy, elem, panel;
    // Calculate table height based on parent container height.
    // 
    //     Modern approach: uses the parent's height instead of window offsets.
    if ((!_pyfunc_truthy(_is_visible(element)))) {
        return null;
    }
    elem = (jQuery(element).closest)(".tabsort_panel");
    dy = (elem.parent().height)();
    if ((dy < 200)) {
        dy = 200;
    }
    panel = _pymeth_find.call(elem, ".fixed-table-toolbar");
    if ((!_pyfunc_truthy(_is_visible(panel)))) {
        dy = _pyfunc_op_add(dy, panel.outerHeight() + 5);
    }
    (jQuery(element).bootstrapTable)("resetView", ({height: dy - 10}));
    return null;
};

datatable_refresh = function flx_datatable_refresh (element) {
    var region;
    // Refresh a Bootstrap Table - either directly or via parent region.
    // 
    //     If the element itself has the .tabsort class, refreshes it directly.
    //     Otherwise, looks for the nearest 'table' region and refreshes tables within.
    if (_pyfunc_truthy(element.classList.contains("tabsort"))) {
        (jQuery(element).bootstrapTable)("refresh", ({silent: true}));
    } else {
        region = get_ajax_region(element, "table");
        if ((!_pyfunc_op_equals(region, null))) {
            ((_pymeth_find.call(jQuery(region), "table[name=tabsort].datatable")).bootstrapTable)("refresh", ({silent: true}));
        }
    }
    return null;
};

window.datatable_refresh = datatable_refresh;
_rowStyle = function flx__rowStyle (value, row, index) {
    var c, x;
    // Extract row CSS class from the cid (cell identifier) column.
    // 
    //     Looks for a div.td_information within the cid column and extracts
    //     additional CSS classes for row-level styling.
    // 
    //     Args:
    //         value: Row data object.
    //         row: Full row data.
    //         index: Row index.
    // 
    //     Returns:
    //         dict: {'classes': css_class} if found, otherwise {}.
    x = _pymeth_find.call(((jQuery(("<div class='cid'>" + value["cid"]) + "</div>"))), "div.td_information");
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
    // Post-render cleanup: merge second_row cells and auto-select if needed.
    // 
    //     - Merges div.second_row cells by removing siblings and setting colspan.
    //     - Triggers auto-select checkbox if data-autoselect attribute is set.
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
    if (_pyfunc_truthy((table[0].hasAttribute)("data-autoselect"))) {
        (((((table[0].closest)(".bootstrap-table")).querySelector)("[name='select']")).click)();
    }
    return null;
};

prepare0 = function flx_prepare0 (table) {
    var refr_block, stub1_seq, stub2_itr, tables;
    // Remove 'flexible_size' class from header tables within the frame.
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
    // Custom AJAX handler for Bootstrap Table server-side processing.
    // 
    //     For tables within a form: serializes the form data and sends a POST.
    //     Otherwise: sends a GET with query parameters.
    // 
    //     Args:
    //         params: Bootstrap Table AJAX parameters dict with url, data, success keys.
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
    var _handle_toolbar_expand, _on_column_resize_stop, _process_resize, btn, icons, init_bootstrap_table, onCheck, onLoadSuccess, onPostHeader, onRefresh, panel, panel2, queryParams, table_panel;
    // Initialize a Bootstrap Table with full configuration.
    // 
    //     Sets up:
    //     - Checkbox columns (visible for .multiple-select, hidden otherwise).
    //     - Row ID column.
    //     - AJAX data loading.
    //     - Row click handling and row-active region updates.
    //     - Toolbar expand/collapse.
    //     - Resize handling.
    //     - Inline editing with auto-advance.
    // 
    //     Args:
    //         table: jQuery-wrapped table element.
    //         table_type: Table type string (e.g. 'datatable').
    if (_pyfunc_op_equals(table_type, "datatable")) {
        if (_pyfunc_truthy(table.hasClass("multiple-select"))) {
            ((_pymeth_find.call(((_pymeth_find.call(jQuery(table), "tr:first"))), "th:first")).before)("<th data-field='state' data-checkbox='true' data-visible='true'></th>");
        } else {
            ((_pymeth_find.call(((_pymeth_find.call(jQuery(table), "tr:first"))), "th:first")).before)("<th data-field='state' data-checkbox='true' data-visible='false'></th>");
        }
        ((_pymeth_find.call(((_pymeth_find.call(jQuery(table), "tr:first"))), "th:last")).after)("<th data-field='id' data-visible='false'>ID</th>");
        onLoadSuccess = (function flx_onLoadSuccess (data) {
            var _pagination;
            // After loading data: prepare table and add pagination styling.
            prepare_datatable(table);
            _pagination = (function flx__pagination () {
                ((_pymeth_find.call((((jQuery(table).closest)(".fixed-table-container"))), ".fixed-table-pagination ul.pagination a")).addClass)("page-link");
                return null;
            }).bind(this);

            setTimeout(_pagination, 0);
            return false;
        }).bind(this);

        onPostHeader = (function flx_onPostHeader (data) {
            // After header render: remove flexible_size from header tables.
            prepare0(table);
            return false;
        }).bind(this);

        onCheck = (function flx_onCheck (row, elem) {
            var row_active_divs, stub3_seq, stub4_itr, x, x2;
            // Handle row checkbox: update table_row_pk input and refresh active areas.
            if ((elem.length > 0)) {
                x = (elem[0].closest)(".ajax-region[data-region='page'");
                if (_pyfunc_truthy(x)) {
                    x2 = x.querySelector("input[name='table_row_pk']");
                    if (_pyfunc_truthy(x2)) {
                        x2.value = row.id;
                        row_active_divs = Array.prototype.slice.call(x.querySelectorAll(".table-row-active"));
                        stub3_seq = row_active_divs;
                        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                            elem = stub3_seq[stub4_itr];
                            if (_pyfunc_truthy(elem.classList.contains("show"))) {
                                refresh_ajax_frame(elem);
                            }
                        }
                    }
                }
            }
            return null;
        }).bind(this);

        queryParams = (function flx_queryParams (p) {
            var base_elem, link;
            // Add serialized form data to table query parameters.
            base_elem = (table[0].closest)(".tabsort_panel");
            link = get_ajax_link(base_elem, "table");
            if ((_pyfunc_truthy(link) && ((_pyfunc_op_equals(_pymeth_lower.call(link.tagName), "form"))))) {
                p["form"] = (jQuery(link).serialize)();
            } else {
                link = get_ajax_link(base_elem, "page");
                if ((_pyfunc_truthy(link) && ((_pyfunc_op_equals(_pymeth_lower.call(link.tagName), "form"))))) {
                    p["form"] = (jQuery(link).serialize)();
                }
            }
            return p;
        }).bind(this);

        icons = ({fullscreen: "fa-arrows-alt", refresh: "fa-refresh", toggleOff: "fa-toggle-off", toggleOn: "fa-toggle-on", columns: "fa-th-list"});
        onRefresh = (function flx_onRefresh (params) {
            // After manual refresh: trigger auto-select if configured.
            if (_pyfunc_truthy((table[0].hasAttribute)("data-autoselect"))) {
                (((((table[0].closest)(".bootstrap-table")).querySelector)("[name='select']")).click)();
            }
            return null;
        }).bind(this);

        if (_pyfunc_truthy(table.hasClass("table_get"))) {
            table.bootstrapTable(({onLoadSuccess: onLoadSuccess, onPostHeader: onPostHeader, onCheck: onCheck, onRefresh: onRefresh, height: 350, rowStyle: _rowStyle, queryParams: queryParams, ajax: datatable_ajax, icons: icons}));
        } else {
            table.bootstrapTable(({onLoadSuccess: onLoadSuccess, onPostHeader: onPostHeader, onCheck: onCheck, onRefresh: onRefresh, rowStyle: _rowStyle, queryParams: queryParams, ajax: datatable_ajax, icons: icons, buttonsOrder: ["refresh", "toggle", "fullscreen", "menu", "select", "columns"]}));
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
        _on_column_resize_stop = (function flx__on_column_resize_stop (event) {
            datetable_set_height(table);
            return null;
        }).bind(this);

        table.on("column:resize:stop", _on_column_resize_stop);
        table_panel = (jQuery(table).closest)("div.win-content");
        btn = (_pymeth_find.call(table_panel, ".tabsort-toolbar-expand").first)();
        if (_pyfunc_truthy(btn)) {
            _handle_toolbar_expand = function (elem) {
                var panel, panel2;
                panel = (_pymeth_find.call(table_panel, ".fixed-table-toolbar").first)();
                panel2 = (_pymeth_find.call(table_panel, ".list_content_header_second_row").first)();
                if ((!_pyfunc_truthy((jQuery(this).hasClass)("active")))) {
                    panel.show();
                    panel2.show();
                } else {
                    panel.hide();
                    panel2.hide();
                }
                process_resize(document.body);
                return null;
            };

            btn.on("click", _handle_toolbar_expand);
            if (_pyfunc_truthy(btn.hasClass("active"))) {
                panel = _pymeth_find.call(table_panel, ".fixed-table-toolbar");
                panel2 = jQuery(".list_content_header_second_row");
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

window.init_table = init_table;
table_loadeddata = function flx_table_loadeddata (event) {
    var _data, _update, datatable, dt, link, options, pk, post, table, txt, url;
    // Handle the loadeddata event for table elements.
    // 
    //     Processes server response markers and updates the table accordingly:
    //     - $$RETURN_REFRESH / $$RETURN_REFRESH_PARENT: refresh the table.
    //     - $$RETURN_ERROR: refresh with error region.
    //     - $$RETURN_HTML_ERROR: show SweetAlert error dialog.
    //     - $$RETURN_NEW_ROW_OK / $$RETURN_UPDATE_ROW_OK: append or update a row.
    //     - $$RETURN_OK: refresh the table.
    //     - Other: delegate to refresh_ajax_frame with 'page' region.
    if (_pyfunc_truthy(_pyfunc_getattr(event, "data"))) {
        dt = data_type(event.data);
        if (_pyfunc_op_contains(dt, ["$$RETURN_REFRESH_PARENT", "$$RETURN_REFRESH"])) {
            ((_pymeth_find.call(jQuery(event.target), "table[name=tabsort].datatable")).bootstrapTable)("refresh", ({silent: true}));
        } else if (_pyfunc_op_equals(dt, "$$RETURN_ERROR")) {
            refresh_ajax_frame((_pyfunc_truthy(event.srcElement))? (event.srcElement) : (event.data_source), "error", event.data);
        } else if (_pyfunc_op_equals(dt, "$$RETURN_HTML_ERROR")) {
            if ((Object.prototype.toString.call(event.data).slice(8,-1).toLowerCase() === 'string')) {
                txt = event.data;
            } else {
                txt = event.data.innerHTML;
            }
            options = ({title: "Error!", html: txt, icon: "error", buttonsStyling: false, showCancelButton: false, customClass: ({confirmButton: "btn btn-primary btn-lg"})});
            Swal.fire(options);
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_UPDATE_ROW_OK", "$$RETURN_NEW_ROW_OK"])) {
            try {
                if ((Object.prototype.toString.call(event.data).slice(8,-1).toLowerCase() === 'string')) {
                    _data = event.data;
                } else {
                    _data = event.data.innerHTML;
                }
                pk = _pyfunc_int((_pymeth_strip.call(((_pymeth_split.call(_data, "id:")[1])))));
                table = (_pyfunc_truthy(event.srcElement))? (event.srcElement) : (event.data_source);
                datatable = _pymeth_find.call(jQuery(table), "table[name=tabsort].datatable");
                link = get_ajax_link(table, "page-content", true);
                if ((!_pyfunc_truthy(link))) {
                    link = get_ajax_link(table, "page");
                }
                url = null;
                if (_pyfunc_truthy(link)) {
                    if (_pyfunc_truthy(link.hasAttribute("href"))) {
                        url = link.getAttribute("href");
                    } else if (_pyfunc_truthy(link.hasAttribute("action"))) {
                        url = link.getAttribute("action");
                        post = true;
                    } else if (_pyfunc_truthy(link.hasAttribute("src"))) {
                        url = link.getAttribute("src");
                    }
                }
                if (_pyfunc_truthy(url)) {
                    if (_pyfunc_op_contains("?", url)) {
                        url = _pyfunc_op_add(url, "&json=1&pk=" + _pyfunc_str(pk));
                    } else {
                        url = _pyfunc_op_add(url, "?&json=1&pk=" + _pyfunc_str(pk));
                    }
                    url = _pymeth_replace.call(url, "/form/", "/json/");
                    url = correct_href(url, [link]);
                    url = process_href(url, jQuery(link.parentElement));
                    _update = (function flx__update (data) {
                        var d, id2, row;
                        // Update or append a row in the datatable.
                        try {
                            d = JSON.parse(data);
                            if (_pyfunc_op_equals(dt, "$$RETURN_NEW_ROW_OK")) {
                                datatable.bootstrapTable("append", d["rows"][0]);
                                datatable.bootstrapTable("scrollTo", "bottom");
                            } else {
                                id2 = d["rows"][0]["id"];
                                row = datatable.bootstrapTable("getRowByUniqueId", id2);
                                if (_pyfunc_truthy(row)) {
                                    datatable.bootstrapTable("updateByUniqueId", ({id: id2, row: d["rows"][0]}));
                                } else {
                                    datatable.bootstrapTable("refresh", ({silent: true}));
                                }
                            }
                        } catch(err_7) {
                            {
                                datatable.bootstrapTable("refresh", ({silent: true}));
                            }
                        }
                        return null;
                    }).bind(this);

                    ajax_get(url, _update);
                    return null;
                }
            } catch(err_4) {
                {
                }
            }
            ((_pymeth_find.call(jQuery(event.target), "table[name=tabsort].datatable")).bootstrapTable)("refresh", ({silent: true}));
        } else if (_pyfunc_op_contains(dt, ["$$RETURN_OK"])) {
            ((_pymeth_find.call(jQuery(event.target), "table[name=tabsort].datatable")).bootstrapTable)("refresh", ({silent: true}));
        } else {
            refresh_ajax_frame((_pyfunc_truthy(event.srcElement))? (event.srcElement) : (event.data_source), "page", event.data);
        }
    } else {
        ((_pymeth_find.call(jQuery(event.target), "table[name=tabsort].datatable")).bootstrapTable)("refresh", ({silent: true}));
    }
    return null;
};

window.table_loadeddata = table_loadeddata;
loading_template = function flx_loading_template (message) {
    // Return a Font Awesome spinner HTML template for loading states.
    return "<i class=\"fa fa-spinner fa-spin fa-fw fa-2x\"></i>";
};

window.loading_template = loading_template;
datatable_action = function flx_datatable_action (btn, action) {
    var _callback, datatable, div, item, pk_list_str, pk_tab, stub5_seq, stub6_itr, tab, url;
    // Execute an action on the selected rows of a datatable.
    // 
    //     Collects selected row PKs and sends them to the table_action endpoint.
    // 
    //     Args:
    //         btn: The button element that triggered the action.
    //         action: Action name to send to the server.
    div = btn.closest("div.tableframe");
    datatable = div.querySelector("table[name=tabsort].datatable");
    url = datatable.getAttribute("data-url") + "../table_action/";
    pk_tab = [];
    tab = (jQuery(datatable).bootstrapTable)("getSelections");
    stub5_seq = tab;
    if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
    for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
        item = stub5_seq[stub6_itr];
        _pymeth_append.call(pk_tab, _pyfunc_str(item.id));
    }
    pk_list_str = _pymeth_join.call(",", pk_tab);
    _callback = (function flx__callback (data) {
        if (_pyfunc_op_contains("RETURN_ACTION", data)) {
            if (_pyfunc_op_equals(data["RETURN_ACTION"], null)) {
                return null;
            }
        }
        (jQuery(datatable).bootstrapTable)("refresh", ({silent: true}));
        return null;
    }).bind(this);

    ajax_json((url + "?pks=") + pk_list_str, ({action: action}), _callback);
    return null;
};

window.datatable_action = datatable_action;
on_check_toggle_visibility = function flx_on_check_toggle_visibility () {
    var actions, container, datatable, div, dropdown, html, item, menu_btn, s, stub10_itr, stub7_seq, stub8_itr, stub9_seq, x;
    // Toggle visibility of table selection checkboxes and menu button.
    // 
    //     When the 'select' button is clicked, shows/hides the state checkbox
    //     column and builds a dropdown menu from data-actions if configured.
    datatable = this;
    container = _pyfunc_getattr(datatable, "$container")[0];
    menu_btn = container.querySelector("button[name=menu]");
    stub9_seq = datatable.getHiddenColumns();
    if ((typeof stub9_seq === "object") && (!Array.isArray(stub9_seq))) { stub9_seq = Object.keys(stub9_seq);}
    for (stub10_itr = 0; stub10_itr < stub9_seq.length; stub10_itr += 1) {
        item = stub9_seq[stub10_itr];
        if (_pyfunc_op_equals(item.field, "state")) {
            datatable.showColumn("state");
            menu_btn.style.display = "block";
            if (_pyfunc_truthy(menu_btn.classList.contains("btn-secondary"))) {
                div = container.closest("div.tableframe");
                if (_pyfunc_truthy(div.hasAttribute("data-actions"))) {
                    actions = _pymeth_split.call(div.getAttribute("data-actions"), ";");
                } else {
                    actions = [];
                }
                dropdown = document.createElement("div");
                dropdown.classList.add("dropleft");
                html = "<button name='menu' class='btn btn-info dropdown-toggle' type='button' data-bs-toggle='dropdown' data-toggle='dropdown'><i class='fa fa-bars'></i></button>";
                html += "<div class='dropdown-menu'>";
                stub7_seq = actions;
                if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
                for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
                    s = stub7_seq[stub8_itr];
                    if (_pyfunc_op_contains("/", s)) {
                        x = _pymeth_split.call(s, "/");
                    } else {
                        x = [s, s];
                    }
                    html = _pyfunc_op_add(html, (((("<button class='dropdown-item' type='button' onclick=\"datatable_action(this, '") + _pymeth_strip.call(x[0])) + ("');\">")) + _pymeth_strip.call(x[1])) + "</button>");
                }
                html += "</div>";
                dropdown.innerHTML = html;
                menu_btn.replaceWith(dropdown);
            }
            return null;
        }
    }
    datatable.hideColumn("state");
    menu_btn.style.display = "none";
    return null;
};

datatable_buttons = function flx_datatable_buttons (obj) {
    // Return button definitions for the Bootstrap Table toolbar.
    // 
    //     Provides 'select' (toggle checkboxes) and 'menu' (dropdown actions)
    //     button configurations.
    return ({select: ({text: "Select rows", icon: "fa-check", event: ({click: on_check_toggle_visibility}), attributes: ({title: "Add a new row to the table"})}), menu: ({text: "Menu", icon: "fa-bars", attributes: ({title: "Menu", style: "display: none;"})})});
};

window.datatable_buttons = datatable_buttons;
export {old_datetable_set_height, datetable_set_height, datatable_refresh, prepare_datatable, prepare0, datatable_ajax, init_table, table_loadeddata, loading_template, datatable_action, on_check_toggle_visibility, datatable_buttons};

var humanFileSize, img_field;
"\nWidget utility functions for form fields and UI components.\n\nProvides helper functions for file input display, human-readable\nfile sizes, and image preview functionality.\n";
humanFileSize = function flx_humanFileSize (bytes, si) {
    var thresh, u, units;
    // Convert a byte count into a human-readable file size string.
    // 
    //     Args:
    //         bytes: The number of bytes (numeric).
    //         si: If True, use SI units (1000-based: kB, MB, ...).
    //             If False, use IEC units (1024-based: KiB, MiB, ...).
    // 
    //     Returns:
    //         tuple: (formatted_size_string, unit_level)
    //             - formatted_size_string: e.g. "1.5 MB"
    //             - unit_level: 0-based index into the unit array (0 = B, 1 = kB/KiB, ...)
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
    // Handle file input change event for image/file upload fields.
    // 
    //     Displays a preview of the selected file:
    //     - For image files (jpeg, jpg, svg, gif, png): shows an img thumbnail.
    //     - For other files: shows file name, MIME type, and size.
    // 
    //     Args:
    //         elem: The file input DOM element that triggered the change event.
    txt = _pymeth_replace.call((((jQuery(elem).val)())), (new RegExp("^.*[\\\\\\ /]")), "");
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
            ext = (((((((elem.files[0].name) + "<br/>") + (elem.files[0].type)) + "<br /><span class='size_level_") + level) + "'>") + size) + "</span>";
            img = jQuery("<p class='img' />");
            img.insertAfter(_pymeth_find.call((((jQuery(elem).closest)("label"))), "input"));
            img.html(ext);
        }
    }
    return null;
};

window.img_field = img_field;
export {humanFileSize, img_field};

var _action_ctrl_init, _auto_init, _init_single_action_ctrl, _pwa_init, _treeview_init;
"\nInline scripts extracted from template files.\n\nContains widget initialization code previously embedded as inline <script>\ntags in Django templates. These functions are registered via\nregister_mount_fun to run automatically after both initial page load and\nAJAX content mounting.\n\nProvides:\n- Treeview toggle (expand/collapse) initialization.\n- Action control widget click handler initialization.\n- PWA service worker registration.\n";
_treeview_init = function flx__treeview_init (dest_elem) {
    var on_click;
    // Initialize treeview toggle functionality in the given element.
    // 
    //     Attaches click handlers to treeview parent nodes for expand/collapse
    //     behavior. Also initializes CSS classes and hides initially-hidden nodes.
    // 
    //     Safe to call multiple times - uses off/on to make handlers idempotent.
    // 
    //     Args:
    //         dest_elem: DOM element to scan for .tree containers.
    ((_pymeth_find.call(((((_pymeth_find.call(jQuery(dest_elem), ".tree li:has(ul)")).addClass)("parent_li"))), " > span")).attr)("title", "Collapse this branch");
    on_click = (function flx_on_click (e) {
        var children;
        // Toggle visibility of child nodes on click.
        children = _pymeth_find.call((((jQuery(this).parent)("li.parent_li"))), " > ul > li");
        if (_pyfunc_truthy(children.is(':visible'))) {
            children.hide("fast");
            ((((_pymeth_find.call((((jQuery(this).attr)("title", "Expand this branch"))), " > i")).addClass)("fa-plus")).removeClass)("fa-minus");
        } else {
            children.show("fast");
            ((((_pymeth_find.call((((jQuery(this).attr)("title", "Collapse this branch"))), " > i")).addClass)("fa-minus")).removeClass)("fa-plus");
        }
        if (_pyfunc_truthy(e)) {
            e.stopPropagation();
        }
        return null;
    }).bind(this);

    ((((_pymeth_find.call(jQuery(dest_elem), ".tree li.parent_li > span")).off)("click", on_click)).on)("click", on_click);
    ((((_pymeth_find.call(jQuery(dest_elem), ".hide_node")).hide)()).removeClass)("hide");
    return null;
};

_action_ctrl_init = function flx__action_ctrl_init (dest_elem) {
    // Initialize action control widgets in the given element.
    // 
    //     Finds all .action-ctrl elements and sets up click handlers for their
    //     child anchor elements. Uses data-ctrl-id and data-ctrl-value attributes
    //     for per-instance configuration.
    // 
    //     Args:
    //         dest_elem: DOM element to scan for .action-ctrl containers.
    ((_pymeth_find.call(jQuery(dest_elem), ".action-ctrl")).each)(_init_single_action_ctrl);
    return null;
};

_init_single_action_ctrl = function flx__init_single_action_ctrl (i, el) {
    var ctrl_id, ctrl_value, on_link_click, sel_class;
    // Initialize a single action control widget.
    // 
    //     Args:
    //         i: Index in the jQuery collection.
    //         el: The raw DOM element (.action-ctrl container).
    ctrl_id = el.getAttribute("data-ctrl-id");
    if ((!_pyfunc_truthy(ctrl_id))) {
        return null;
    }
    ctrl_value = (_pyfunc_truthy(el.getAttribute("data-ctrl-value"))) || "None";
    sel_class = "control_sel";
    window[("_action_ctrl_" + ctrl_id) + "_var"] = null;
    on_link_click = (function flx_on_link_click (e) {
        var href_attr, new_value, prev;
        prev = window[("_action_ctrl_" + ctrl_id) + "_var"];
        if (_pyfunc_truthy(prev)) {
            (prev.parent(".control").removeClass)(sel_class);
        }
        window[("_action_ctrl_" + ctrl_id) + "_var"] = jQuery(this);
        (((jQuery(this).parent)(".control")).addClass)(sel_class);
        href_attr = (jQuery(this).attr)("href");
        if (_pyfunc_truthy(href_attr)) {
            new_value = _pymeth_replace.call(href_attr, "action/", "");
            if (_pyfunc_hasattr(window, "cmd_to_python")) {
                cmd_to_python(((("python|self." + ctrl_id) + ".SetValue('") + new_value) + "')");
            } else {
                (jQuery("#id_" + ctrl_id).val)(new_value);
            }
        }
        return false;
    }).bind(this);

    ((((_pymeth_find.call(jQuery(el), "a")).off)("click", on_link_click)).on)("click", on_link_click);
    if ((_pyfunc_truthy(ctrl_value) && ((!_pyfunc_op_equals(ctrl_value, "None"))))) {
        ((_pymeth_find.call(jQuery(el), "a")).each)((function (idx, a) {return ((_pyfunc_op_equals(((jQuery(a).attr)("href")), ("action/" + ctrl_value))))? ((jQuery(a).click)()) : (null);}).bind(this));
    }
    return null;
};

_pwa_init = function flx__pwa_init (dest_elem) {
    var on_error, on_success, sw_scope, sw_scope_meta, sw_url, sw_url_meta;
    // Register the PWA service worker if supported by the browser.
    // 
    //     Reads the service worker URL and scope from meta tags:
    //     <meta name="pwa-sw-url" content="...">
    //     <meta name="pwa-sw-scope" content="...">
    // 
    //     Args:
    //         dest_elem: DOM element (unused, reads from document.head).
    if ((!_pyfunc_truthy('serviceWorker' in navigator))) {
        return null;
    }
    sw_url_meta = document.querySelector("meta[name=\"pwa-sw-url\"]");
    sw_scope_meta = document.querySelector("meta[name=\"pwa-sw-scope\"]");
    if ((!_pyfunc_truthy(sw_url_meta))) {
        return null;
    }
    sw_url = sw_url_meta.getAttribute("content");
    sw_scope = (_pyfunc_truthy(sw_scope_meta))? (sw_scope_meta.getAttribute("content")) : ("/");
    on_success = (function flx_on_success (registration) {
        // Log successful service worker registration.
        console.log("django-pwa: ServiceWorker registration successful with scope: ", registration.scope);
        return null;
    }).bind(this);

    on_error = (function flx_on_error (err) {
        // Log failed service worker registration.
        console.log("django-pwa: ServiceWorker registration failed: ", err);
        return null;
    }).bind(this);

    ((navigator.serviceWorker.register(sw_url, ({scope: sw_scope}))).then)(on_success, on_error);
    return null;
};

register_mount_fun(_treeview_init);
register_mount_fun(_action_ctrl_init);
_auto_init = function flx__auto_init () {
    // Auto-initialize widgets when the DOM is ready (initial page load).
    _treeview_init(document);
    _action_ctrl_init(document);
    _pwa_init(document);
    return null;
};

(jQuery(document).ready)(_auto_init);

var _on_error, _on_key, _on_popstate, activate_menu, app_init, dom_content_loaded, jquery_ready, static_path;
"\nApplication entry point and initialization module.\n\nThis is the main bootstrap module that initializes the entire client-side\napplication. It sets up:\n- Global state (window-level variables).\n- Keyboard event handling (Enter key on DialogForm).\n- Application initialization (app_init).\n- Static path resolution.\n- Menu activation and highlighting.\n- Error handling for AJAX requests.\n- Browser history (popstate) navigation.\n\nDependencies (loaded via pscript cross-module references):\n    pytigon_js.tabmenu: Page, get_menu\n    pytigon_js.offline: service_worker_and_indexedDB_test, install_service_worker\n    pytigon_js.db: sync_and_run\n    pytigon_js.component: GlobalBus\n    pytigon_js.events: register_global_event\n    pytigon_js.ajax_region: ajax_load, mount_html\n";
window.PS = null;
window.MOUNTED_COMPONENTS = 0;
window.GLOBAL_BUS = new GlobalBus();
window.START_MENU_ID = null;
_on_key = function (e) {
    var elem, form;
    // Handle keypress events globally.
    // 
    //     When Enter is pressed on a non-TEXTAREA element within a DialogForm,
    //     triggers the form's OK action (on_edit_ok) and prevents default.
    // 
    //     Args:
    //         self: The event target element.
    //         e: jQuery keypress event object.
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
    // Handle DOMContentLoaded event for traditional application template.
    // 
    //     Mounts the initial HTML content into the body-body section.
    mount_html(document.querySelector("section.body-body"), null);
    return null;
};

app_init = function flx_app_init (prj_name, application_template, menu_id, lang, base_path, base_fragment_init, component_init, offline_support, start_page, gen_time, callback) {
    var _init_start_page, _on_sync, desktop, href, obj, objects, stub1_seq, stub2_itr;
    callback = (callback === undefined) ? null: callback;
    // Initialize the entire client-side application.
    // 
    //     This is the main entry point called by the server-rendered page.
    //     It sets up all window-level configuration, initializes the offline
    //     service worker, runs database synchronization, and mounts the
    //     initial page content.
    // 
    //     Args:
    //         prj_name: Project name (used for IndexedDB database name).
    //         application_template: UI template mode:
    //             'modern', 'standard', 'simple', 'traditional', 'mobile',
    //             'tablet', 'hybrid'.
    //         menu_id: ID of the starting menu item.
    //         lang: Language/locale code (e.g. 'en', 'pl').
    //         base_path: Base URL path prefix for the application.
    //         base_fragment_init: Fragment initialization mode.
    //         component_init: Component initialization callback.
    //         offline_support: Whether to enable offline/PWA features.
    //         start_page: URL of the initial page to load.
    //         gen_time: Server-side generation timestamp for cache busting.
    //         callback: Optional callback invoked after initialization.
    window.IN_MORPH_PROCESS = false;
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
    if (_pyfunc_truthy(offline_support)) {
        if ((_pyfunc_truthy(navigator.onLine) && (_pyfunc_truthy(service_worker_and_indexedDB_test())))) {
            install_service_worker();
        }
    }
    _on_sync = (function flx__on_sync (status) {
        // Handle system sync completion - reload page if cache was stale.
        if (_pyfunc_op_equals(status, "OK-refresh")) {
            location.reload();
        }
        return null;
    }).bind(this);

    sync_and_run("sys", _on_sync);
    _init_start_page = (function flx__init_start_page () {
        var _on_load, p;
        // Load the initial start page content via AJAX.
        // 
        //         Only loads if start_page is specified and the current URL matches
        //         the base path or ends with index.html.
        if ((_pyfunc_truthy(start_page) && ((!_pyfunc_op_equals(start_page, "None"))) && ((_pyfunc_op_equals(window.location.pathname, base_path) || _pymeth_endswith.call(window.location.pathname, "index.html"))))) {
            _on_load = (function flx__on_load (responseText, status, response) {
                console.log("_init_start_page::_on_load");
                return null;
            }).bind(this);

            p = _pyfunc_op_add(base_path, start_page);
            ajax_load(document.querySelector("#body_desktop"), p, _on_load);
        }
        return null;
    }).bind(this);

    window.init_start_page = _init_start_page;
    _init_start_page();
    if (_pyfunc_hasattr(window, "init_callback")) {
        window.init_callback();
    }
    jQuery.fn.editable.defaults.mode = "inline";
    jQuery.fn.combodate.defaults["maxYear"] = 2025;
    desktop = document.getElementById("body_desktop");
    if (_pyfunc_truthy(desktop)) {
        mount_html(desktop, null, null);
    }
    if ((_pyfunc_truthy(window.location.search) && _pyfunc_op_contains("subpage", window.location.search))) {
        href = _pymeth_split.call(window.location.search, "=")[1];
        objects = Array.prototype.slice.call(document.querySelectorAll("a"));
        stub1_seq = objects;
        if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
        for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
            obj = stub1_seq[stub2_itr];
            if ((_pyfunc_truthy(obj.href) && (_pyfunc_truthy(obj.classList.contains("menu-href"))))) {
                if (_pyfunc_op_contains(href, obj.href)) {
                    obj.click();
                    break;
                }
            }
        }
    }
    return null;
};

window.app_init = app_init;
static_path = function flx_static_path (path) {
    // Resolve a static asset path with the application base path prefix.
    // 
    //     Args:
    //         path: Absolute path starting with '/' (e.g. '/static/js/app.js').
    // 
    //     Returns:
    //         str: Path with BASE_PATH prepended (minus the leading '/'),
    //              or the original path if BASE_PATH is not set.
    if ((_pyfunc_hasattr(window, BASE_PATH) && _pyfunc_truthy(window.BASE_PATH) && (window.BASE_PATH.length > 0))) {
        return _pyfunc_op_add(window.BASE_PATH, path.slice(1));
    } else {
        return path;
    }
    return null;
};

window.static_path = static_path;
activate_menu = function flx_activate_menu () {
    var a, a_tab, div, event, href, id_elem, li, menu, pathname, pathname2, stub3_seq, stub4_itr, x;
    // Highlight the current menu item based on the browser URL pathname.
    // 
    //     Scans all 'a.menu-href' elements and activates the one matching the
    //     current URL. For sidebar menus (sys-sidebarmenu), expands parent
    //     treeview nodes. For tab menus, switches to the matching tab.
    pathname = window.location.pathname;
    if (_pymeth_startswith.call(pathname, window.BASE_PATH)) {
        pathname2 = pathname.slice(window.BASE_PATH.length);
    } else {
        pathname2 = pathname;
    }
    if (_pyfunc_truthy(pathname2)) {
        menu = document.querySelector("sys-sidebarmenu");
        a_tab = Array.prototype.slice.call(document.querySelectorAll("a.menu-href"));
        stub3_seq = a_tab;
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            a = stub3_seq[stub4_itr];
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

window.activate_menu = activate_menu;
_on_error = function flx__on_error (request, settings) {
    var d, end, start;
    // Global AJAX error handler.
    // 
    //     Displays server error responses in a modal dialog. When the response
    //     contains a <body> tag, extracts the body content for display.
    // 
    //     Args:
    //         request: The XMLHttpRequest object.
    //         settings: jQuery AJAX settings including status and responseText.
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
            if (_pyfunc_truthy(window.hasOwnProperty("bootstrap"))) {
                d = new bootstrap.Modal(document.getElementById("dialog-form-error"));
                d.hide();
            } else {
                (jQuery("#dialog-form-error").modal)();
            }
        } else {
            mount_html(jQuery("#dialog-data-error"), settings.responseText);
            if (_pyfunc_truthy(window.hasOwnProperty("bootstrap"))) {
                d = new bootstrap.Modal(document.getElementById("dialog-form-error"));
                d.hide();
            } else {
                (jQuery("#dialog-form-error").modal)();
            }
        }
    }
    return null;
};

jquery_ready = function flx_jquery_ready () {
    // Placeholder for jQuery document ready callback.
    // 
    //     Override or extend this function to run code after the DOM is ready.
    return null;
};

window.jquery_ready = jquery_ready;
_on_popstate = function (e) {
    var menu, x;
    // Handle browser back/forward navigation (popstate event).
    // 
    //     Restores page state from history:
    //     - In 'modern' template: activates the tab from stored state.
    //     - In other templates: decompresses and mounts stored HTML content.
    //     - In 'standard' template: also restores button highlighting.
    // 
    //     Args:
    //         self: The window object.
    //         e: PopStateEvent with state data.
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
export {dom_content_loaded, app_init, static_path, activate_menu, jquery_ready};

