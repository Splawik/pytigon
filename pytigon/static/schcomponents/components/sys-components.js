var comp, init, stub1_context, stub2_err, stub3_context, stub4_err, stub5_context, stub6_err, stub7_context, stub8_err;
import { animate_combo, get_table_type, init_table } from '../../pytigon_js/pytigon.js';
stub1_context = (new DefineWebComponent("sys-sidebarmenu", false));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        var _on_resize, client_type, obj1, obj1_off, obj1_on, obj2, obj2_off, obj2_on, sidebar_menu;
        _on_resize = (function flx__on_resize () {
            window.process_resize(document.body);
            return null;
        }).bind(this);

        client_type = component.getAttribute("type");
        sidebar_menu = component.querySelector(".sidebar-menu");
        if ((_pyfunc_truthy(client_type) && _pyfunc_op_equals(client_type, "smartfon"))) {
            jQuery.sidebarMenu(sidebar_menu);
            obj1_off = ({width: "256px"});
            obj1_on = ({width: "0px"});
            obj2_off = _pyfunc_create_dict("margin-left", "256px", "margin-right", "-256px");
            obj2_on = _pyfunc_create_dict("margin-left", "0px", "margin-right", "0px");
            obj1 = jQuery("#menu");
            obj2 = jQuery("#panel");
            animate_combo(jQuery(".sidebar-toggle"), obj1, obj2, obj1_off, obj1_on, obj2_off, obj2_on, "fast", _on_resize);
        } else {
            jQuery.sidebarMenu(sidebar_menu);
            obj1_off = ({width: "256px"});
            obj1_on = ({width: "0px"});
            obj2_off = _pyfunc_create_dict("margin-left", "256px");
            obj2_on = _pyfunc_create_dict("margin-left", "0px");
            obj1 = jQuery("#menu");
            obj2 = jQuery("#panel");
            animate_combo(jQuery(".sidebar-toggle"), obj1, obj2, obj1_off, obj1_on, obj2_off, obj2_on, "fast", _on_resize);
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0; }
if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
} else { stub1_context.__exit__(null, null, null); }
stub3_context = (new DefineWebComponent("sys-perfectscrollbar", false));
comp = stub3_context.__enter__();
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
} catch(err_0)  { stub4_err=err_0; }
if (stub4_err) { if (!stub3_context.__exit__(stub4_err.name || "error", stub4_err, null)) { throw stub4_err; }
} else { stub3_context.__exit__(null, null, null); }
stub5_context = (new DefineWebComponent("sys-datatable", false));
comp = stub5_context.__enter__();
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
} catch(err_0)  { stub6_err=err_0; }
if (stub6_err) { if (!stub5_context.__exit__(stub6_err.name || "error", stub6_err, null)) { throw stub6_err; }
} else { stub5_context.__exit__(null, null, null); }
stub7_context = (new DefineWebComponent("move-attr", false));
comp = stub7_context.__enter__();
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
            element.setAttribute(component.attributes[i].name, component.attributes[i].value);
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub8_err=err_0; }
if (stub8_err) { if (!stub7_context.__exit__(stub8_err.name || "error", stub8_err, null)) { throw stub8_err; }
} else { stub7_context.__exit__(null, null, null); }