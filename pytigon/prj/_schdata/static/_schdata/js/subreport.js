var subreport_dragstart, subreport_drop, subreport_ondragenter, subreport_ondragleave, subreport_ondragover;
subreport_dragstart = function flx_subreport_dragstart (ev) {
    ev.dataTransfer.setData("text", ev.target.getAttribute("name"));
    return null;
};

window.subreport_dragstart = subreport_dragstart;
subreport_drop = function flx_subreport_drop (ev, base_path) {
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
        href = ((((base_path + "schreports/table/Report/") + data) + "/") + data2) + "/action/move_to/";
        _callback = (function flx__callback (data) {
            window.refresh_ajax_frame(target);
            return null;
        }).bind(this);

        window.ajax_get(href, _callback);
    }
    return null;
};

window.subreport_drop = subreport_drop;
subreport_ondragenter = function flx_subreport_ondragenter (ev) {
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        (jQuery(ev.target).addClass)("bg-success");
    }
    return null;
};

window.subreport_ondragenter = subreport_ondragenter;
subreport_ondragleave = function flx_subreport_ondragleave (ev) {
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        (jQuery(ev.target).removeClass)("bg-success");
    }
    return null;
};

window.subreport_ondragleave = subreport_ondragleave;
subreport_ondragover = function flx_subreport_ondragover (ev) {
    if (_pyfunc_op_equals(ev.target.tagName, "LABEL")) {
        ev.preventDefault();
    }
    return null;
};

window.subreport_ondragover = subreport_ondragover;
export {subreport_dragstart, subreport_drop, subreport_ondragenter, subreport_ondragleave, subreport_ondragover};