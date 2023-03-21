var TAG, TEMPLATE, comp, disconnectedCallback, get_screen_cordinates, init, stub1_context, stub2_err;
TAG = "ptig-scroll-action";
TEMPLATE = '        <div>\n' +
    '                <slot></slot>\n' +
    '        </div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    get_screen_cordinates = function flx_get_screen_cordinates (obj) {
        var x, y;
        x = obj.offsetLeft;
        y = obj.offsetTop;
        while (obj.offsetParent) {
            x = _pyfunc_op_add(x, obj.offsetParent.offsetLeft);
            y = _pyfunc_op_add(y, obj.offsetParent.offsetTop);
            if ((_pyfunc_op_equals(obj, (document.getElementsByTagName("body")[0])))) {
                break;
            } else {
                obj = obj.offsetParent;
            }
        }
        return [x, y];
    };

    init = function flx_init (component) {
        var div, handle_scroll, offset_to_parent;
        div = component.root.querySelector("div");
        offset_to_parent = (((jQuery(div).offset)()).top) - (((jQuery(component.parentNode).offset)()).top);
        handle_scroll = (function flx_handle_scroll (event) {
            var active_zone_dy, bottom_is_visible, div_y1, div_y2, offset_bottom, offset_top, top_is_visible, v, window_dy, window_y;
            window_dy = component.parentNode.offsetHeight;
            div_y1 = offset_to_parent - component.parentNode.scrollTop;
            div_y2 = _pyfunc_op_add(div_y1, div.offsetHeight);
            if (_pyfunc_truthy(component.hasAttribute("y"))) {
                window_y = window_dy - (_pyfunc_int(((_pyfunc_op_mult((_pyfunc_int((_pymeth_replace.call(component.getAttribute("y"), "%", "")))), window_dy)) / 100)));
            } else {
                window_y = _pyfunc_int((window_dy / 2));
            }
            if (_pyfunc_truthy(component.hasAttribute("dy"))) {
                active_zone_dy = _pyfunc_int(((_pyfunc_op_mult((_pyfunc_int((_pymeth_replace.call(component.getAttribute("dy"), "%", "")))), (div_y2 - div_y1))) / 100));
            } else {
                active_zone_dy = _pyfunc_int(((div_y2 - div_y1) / 2));
            }
            if ((div_y1 > window_dy)) {
                offset_top = 0;
            } else if ((div_y1 < 0)) {
                offset_top = 1;
            } else {
                offset_top = 1 - (div_y1 / window_dy);
            }
            if ((div_y2 > window_dy)) {
                offset_bottom = 0;
            } else if ((div_y2 < 0)) {
                offset_bottom = 1;
            } else {
                offset_bottom = 1 - (div_y2 / window_dy);
            }
            if (((offset_top > 0) && (offset_top < 1))) {
                top_is_visible = true;
            } else {
                top_is_visible = false;
            }
            if (((offset_bottom > 0) && (offset_bottom < 1))) {
                bottom_is_visible = true;
            } else {
                bottom_is_visible = false;
            }
            v = (_pyfunc_op_mult(2, (window_y - (_pyfunc_op_add(div_y1, div_y2) / 2)))) / active_zone_dy;
            component.set_state(({offset_top: offset_top, offset_bottom: offset_bottom, top_is_visible: top_is_visible, bottom_is_visible: bottom_is_visible, v: v}));
            return null;
        }).bind(this);

        if (_pyfunc_truthy(component.parentNode)) {
            component.parentNode.addEventListener("scroll", handle_scroll);
        }
        return null;
    };

    comp.options["init"] = init;
    disconnectedCallback = function flx_disconnectedCallback (component) {
        window.removeEventListener("scroll", component.handle_scroll);
        return null;
    };

    comp.options["disconnectedCallback"] = disconnectedCallback;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}