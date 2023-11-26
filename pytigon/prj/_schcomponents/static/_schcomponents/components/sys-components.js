var comp, convert_rem_to_pixels, drag_element, init, stub10_err, stub11_context, stub12_err, stub13_context, stub14_err, stub15_context, stub16_err, stub1_context, stub2_err, stub3_context, stub4_err, stub7_context, stub8_err, stub9_context, test;
stub1_context = (new DefineWebComponent("sys-sidebarmenu", false));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var _init, _on_resize;
        _on_resize = (function flx__on_resize () {
            window.process_resize(document.body);
            return null;
        }).bind(this);

        _init = (function flx__init () {
            var _on_click, btn, client_type, sidebar_menu, state;
            client_type = component.getAttribute("type");
            sidebar_menu = component.querySelector(".sidebar-menu");
            jQuery.sidebarMenu(sidebar_menu);
            btn = document.querySelector(".main-sidebar-toggle");
            if (((_pyfunc_truthy(component.hasAttribute("state"))) && ((_pyfunc_op_equals(component.getAttribute("state"), "on"))))) {
                state = false;
            } else {
                state = true;
            }
            _on_click = (function flx__on_click () {
                var obj1, obj2;
                obj1 = document.querySelector("#menu");
                obj2 = document.querySelector("#panel");
                state = !_pyfunc_truthy(state);
                if (_pyfunc_truthy(state)) {
                    obj1.classList.add("off");
                    _pymeth_remove.call(obj1.classList, "on");
                    obj2.classList.add("on");
                    _pymeth_remove.call(obj2.classList, "off");
                    _on_resize();
                } else {
                    obj1.classList.add("on");
                    _pymeth_remove.call(obj1.classList, "off");
                    obj2.classList.add("off");
                    _pymeth_remove.call(obj2.classList, "on");
                    _on_resize();
                }
                return null;
            }).bind(this);

            btn.addEventListener("click", _on_click);
            setTimeout(_on_click, 100);
            return null;
        }).bind(this);

        setTimeout(_init, 100);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}
stub3_context = (new DefineWebComponent("sys-button", false));
comp = stub3_context.__enter__();
try {
    init = function flx_init (component) {
        var _init;
        _init = (function flx__init () {
            var _on_click, btn, classes_off, classes_on, elements, state;
            btn = component.querySelector(".btn");
            elements = _pymeth_split.call(component.getAttribute("elements"), "|");
            classes_on = _pymeth_split.call(component.getAttribute("class-on"), "|");
            classes_off = _pymeth_split.call(component.getAttribute("class-off"), "|");
            if (((_pyfunc_truthy(component.hasAttribute("state"))) && ((_pyfunc_op_equals(component.getAttribute("state"), "on"))))) {
                state = true;
            } else {
                state = false;
            }
            _on_click = (function flx__on_click () {
                var el, element, i, stub5_seq, stub6_itr;
                state = !_pyfunc_truthy(state);
                i = 0;
                stub5_seq = elements;
                if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
                for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
                    element = stub5_seq[stub6_itr];
                    el = window.super_query_selector(component, element);
                    if (_pyfunc_truthy(state)) {
                        el.classList.add(classes_on[i]);
                        _pymeth_remove.call(el.classList, classes_off[i]);
                    } else {
                        _pymeth_remove.call(el.classList, classes_on[i]);
                        el.classList.add(classes_off[i]);
                    }
                    i += 1;
                }
                return null;
            }).bind(this);

            btn.addEventListener("click", _on_click);
            return null;
        }).bind(this);

        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub4_err=err_0;
} finally {
    if (stub4_err) { if (!stub3_context.__exit__(stub4_err.name || "error", stub4_err, null)) { throw stub4_err; }
    } else { stub3_context.__exit__(null, null, null); }
}
stub7_context = (new DefineWebComponent("sys-perfectscrollbar", false));
comp = stub7_context.__enter__();
try {
    init = function flx_init (component) {
        var _on_resize;
        window.PS = new PerfectScrollbar("#menu");
        _on_resize = (function flx__on_resize () {
            window.PS.update();
            return null;
        }).bind(this);

        (jQuery(window).resize)(_on_resize);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub8_err=err_0;
} finally {
    if (stub8_err) { if (!stub7_context.__exit__(stub8_err.name || "error", stub8_err, null)) { throw stub8_err; }
    } else { stub7_context.__exit__(null, null, null); }
}
stub9_context = (new DefineWebComponent("sys-datatable", false));
comp = stub9_context.__enter__();
try {
    init = function flx_init (component) {
        var onchange, table_type, tbl;
        table_type = get_table_type(jQuery(component));
        tbl = component.querySelector(".tabsort");
        if (_pyfunc_truthy(tbl)) {
            init_table(jQuery(tbl), table_type);
            onchange = (function flx_onchange () {
                (jQuery(tbl).bootstrapTable)("refresh");
                return null;
            }).bind(this);

            component.onchange = onchange;
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub10_err=err_0;
} finally {
    if (stub10_err) { if (!stub9_context.__exit__(stub10_err.name || "error", stub10_err, null)) { throw stub10_err; }
    } else { stub9_context.__exit__(null, null, null); }
}
stub11_context = (new DefineWebComponent("move-attr", false));
comp = stub11_context.__enter__();
try {
    init = function flx_init (component) {
        var element, i, l, tag;
        if (_pyfunc_truthy(component.hasAttribute("target-tag"))) {
            tag = component.getAttribute("target-tag");
        } else {
            tag = "tr";
        }
        element = component.closest(tag);
        l = component.attributes.length;
        for (i = 0; i < l; i += 1) {
            if ((_pymeth_startswith.call((component.attributes[i].value), "+"))) {
                element.setAttribute(component.attributes[i].name, (element.getAttribute(component.attributes[i].name) + " ") + (component.attributes[i].value.slice(1)));
            } else {
                element.setAttribute(component.attributes[i].name, component.attributes[i].value);
            }
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub12_err=err_0;
} finally {
    if (stub12_err) { if (!stub11_context.__exit__(stub12_err.name || "error", stub12_err, null)) { throw stub12_err; }
    } else { stub11_context.__exit__(null, null, null); }
}
stub13_context = (new DefineWebComponent("ptig-paste", false));
comp = stub13_context.__enter__();
try {
    comp.options["template"] = '<a class=\"btn btn_size btn-light shadow-none\" title=\"Paste\" target=\"refresh_frame\" data-region=\"page-content\" data-bind=\":onclick\">Paste</a>\n' +
    '\n' +
    '';
    comp.options["attributes"] = ({href: null, onclick: null});
    init = function flx_init (component) {
        var _onclick, state;
        state = ({});
        _onclick = (function flx__onclick (event) {
            var _send_text;
            _send_text = (function flx__send_text (text) {
                var _complete;
                _complete = (function flx__complete () {
                    refresh_ajax_frame(component, "page-content");
                    return null;
                }).bind(this);

                ajax_post(component.getAttribute("href"), text, _complete, null, null, "application/json");
                return null;
            }).bind(this);

            (navigator.clipboard.readText().then)(_send_text);
            return null;
        }).bind(this);

        state["onclick"] = _onclick;
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub14_err=err_0;
} finally {
    if (stub14_err) { if (!stub13_context.__exit__(stub14_err.name || "error", stub14_err, null)) { throw stub14_err; }
    } else { stub13_context.__exit__(null, null, null); }
}
stub15_context = (new DefineWebComponent("ptig-sliderline", false));
comp = stub15_context.__enter__();
try {
    comp.options["template"] = '<div class=\"slider-line\" style=\"width:100%;height:7px;cursor:move;\"></div>\n' +
    '\n' +
    '';
    convert_rem_to_pixels = function flx_convert_rem_to_pixels (rem) {
        return _pyfunc_op_mult(rem, (parseFloat(getComputedStyle(document.documentElement).fontSize)));
    };

    drag_element = function flx_drag_element (elmnt, related_element, multiplier, vertical) {
        var close_drag_element, drag_mouse_down, element_drag, height, width, x, y;
        multiplier = (multiplier === undefined) ? 1: multiplier;
        vertical = (vertical === undefined) ? false: vertical;
        x = 0;
        y = 0;
        width = 0;
        height = 0;
        drag_mouse_down = (function flx_drag_mouse_down (e) {
            e = (_pyfunc_truthy(e))? (e) : (window.event);
            e.preventDefault();
            x = e.screenX;
            y = e.screenY;
            document.onmouseup = close_drag_element;
            document.onmousemove = element_drag;
            return null;
        }).bind(this);

        element_drag = (function flx_element_drag (e) {
            var h, w;
            e = (_pyfunc_truthy(e))? (e) : (window.event);
            e.preventDefault();
            width = x - e.screenX;
            height = y - e.screenY;
            x = e.screenX;
            y = e.screenY;
            if (_pyfunc_truthy(vertical)) {
                w = _pyfunc_op_add(related_element.clientWidth, _pyfunc_op_mult(width, multiplier));
                related_element.style.width = _pyfunc_str(w) + "px";
            } else {
                h = _pyfunc_op_add(related_element.clientHeight, _pyfunc_op_mult(height, multiplier));
                related_element.style.height = _pyfunc_str(h) + "px";
            }
            window.process_resize(document.body);
            return null;
        }).bind(this);

        close_drag_element = (function flx_close_drag_element () {
            document.onmouseup = null;
            document.onmousemove = null;
            return null;
        }).bind(this);

        elmnt.onmousedown = drag_mouse_down;
        return null;
    };

    init = function flx_init (component) {
        var div, elem, stub17_;
        div = component.root.querySelector("div");
        elem = window.super_query_selector(div, component.getAttribute("rel"));
        if (((_pyfunc_truthy(component.hasAttribute("vertical"))) && ((_pyfunc_op_equals(component.getAttribute("vertical"), "1"))))) {
            stub17_ = [div.style.height, div.style.width];
            div.style.width = stub17_[0];div.style.height = stub17_[1];
            _pymeth_remove.call(div.classList, "slider-line");
            div.classList.add("v-slider-line");
            drag_element(div, elem, 1, true);
        } else {
            drag_element(div, elem, 1, false);
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub16_err=err_0;
} finally {
    if (stub16_err) { if (!stub15_context.__exit__(stub16_err.name || "error", stub16_err, null)) { throw stub16_err; }
    } else { stub15_context.__exit__(null, null, null); }
}
test = function flx_test (x) {
    return x;
};

export {test};