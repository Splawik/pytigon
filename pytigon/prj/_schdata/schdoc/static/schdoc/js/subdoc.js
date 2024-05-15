var subdoc_dragstart, subdoc_drop, subdoc_ondragenter, subdoc_ondragleave, subdoc_ondragover;
subdoc_dragstart = function flx_subdoc_dragstart (ev) {
    ev.dataTransfer.setData("text", ev.target.getAttribute("name"));
    return null;
};

window.subdoc_dragstart = subdoc_dragstart;
subdoc_drop = function flx_subdoc_drop (ev, base_path) {
    var _callback, data, data2, href, target;
    ev.preventDefault();
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        target = ev.target;
    } else {
        target = ev.target.parentElement;
    }
    data = ev.dataTransfer.getData("text");
    data2 = target.getAttribute("name");
    if ((!_pyfunc_op_equals(data2, data))) {
        href = ((((base_path + "schdoc/table/Doc/") + data) + "/") + data2) + "/action/move_to/";
        _callback = (function flx__callback (data) {
            window.refresh_ajax_frame(target);
            return null;
        }).bind(this);

        window.ajax_get(href, _callback);
    }
    return null;
};

window.subdoc_drop = subdoc_drop;
subdoc_ondragenter = function flx_subdoc_ondragenter (ev) {
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        (jQuery(ev.target).addClass)("bg-success");
    }
    return null;
};

window.subdoc_ondragenter = subdoc_ondragenter;
subdoc_ondragleave = function flx_subdoc_ondragleave (ev) {
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        (jQuery(ev.target).removeClass)("bg-success");
    }
    return null;
};

window.subdoc_ondragleave = subdoc_ondragleave;
subdoc_ondragover = function flx_subdoc_ondragover (ev) {
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        ev.preventDefault();
    }
    return null;
};

window.subdoc_ondragover = subdoc_ondragover;
export {subdoc_dragstart, subdoc_drop, subdoc_ondragenter, subdoc_ondragleave, subdoc_ondragover};