var BASE_PATH, TAG, TEMPLATE, comp, decimal_separator, init, stub1_context, stub2_err;
TAG = "ptig-imask";
TEMPLATE = '        <slot></slot>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
decimal_separator = function flx_decimal_separator () {
    return 1.1.toLocaleString()[1];
};

stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/imask/imask.js"]));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _mask, imask, input, mask, options;
        input = component.querySelector("input");
        options = ({});
        mask = component.getAttribute("mask");
        _mask = _pymeth_lower.call(mask);
        if ((_pyfunc_op_equals(_mask, "number") || _pyfunc_op_equals(_mask, "monay"))) {
            options["mask"] = window.Number;
            if (_pyfunc_op_equals(_mask, "monay")) {
                options["scale"] = 2;
                options["thousandsSeparator"] = " ";
                options["radix"] = decimal_separator();
            }
            if (_pyfunc_truthy(component.hasAttribute("scale"))) {
                options["scale"] = _pyfunc_int(component.getAttribute("scale"));
            }
            if (_pyfunc_truthy(component.hasAttribute("signed"))) {
                options["signed"] = true;
            }
            if (_pyfunc_truthy(component.hasAttribute("thousands-separator"))) {
                if (_pyfunc_truthy(component.getAttribute("thousands-separator"))) {
                    options["thousandsSeparator"] = component.getAttribute("thousands-separator");
                } else {
                    options["thousandsSeparator"] = " ";
                }
            }
            if (_pyfunc_truthy(component.hasAttribute("pad-fractional-zeros"))) {
                options["padFractionalZeros"] = true;
            }
            if (_pyfunc_truthy(component.hasAttribute("normalize-zeros"))) {
                options["normalizeZeros"] = true;
            }
            if (_pyfunc_truthy(component.hasAttribute("radix"))) {
                if (_pyfunc_truthy(component.getAttribute("radix"))) {
                    options["radix"] = component.getAttribute("radix");
                } else {
                    options["radix"] = decimal_separator();
                }
            }
            if (_pyfunc_truthy(component.hasAttribute("map-to-radix"))) {
                options["mapToRadix"] = component.getAttribute("map-to-radix");
            }
        } else if (_pyfunc_op_equals(_mask, "range")) {
            options["mask"] = IMask.MaskedRange;
            if (_pyfunc_truthy(component.hasAttribute("from"))) {
                options["from"] = _pyfunc_int(component.getAttribute("from"));
            }
            if (_pyfunc_truthy(component.hasAttribute("to"))) {
                options["to"] = _pyfunc_int(component.getAttribute("to"));
            }
            if (_pyfunc_truthy(component.hasAttribute("max-length"))) {
                options["maxLength"] = _pyfunc_int(component.getAttribute("max-length"));
            }
        } else if (_pyfunc_op_equals(_mask, "enum")) {
            options["mask"] = IMask.MaskedEnum;
            options["enum"] = _pymeth_split.call(component.getAttribute("enum"), ";");
        } else if (_pyfunc_op_equals(_mask, "date")) {
            options["mask"] = window.Date;
            if (_pyfunc_truthy(component.hasAttribute("pattern"))) {
                options["pattern"] = component.getAttribute("pattern");
            } else {
                options["pattern"] = "Y-m-000";
                options["blocks"] = ({d: ({mask: window.IMask.MaskedRange, from: 1, to: 12, maxLength: 2}), m: ({mask: window.IMask.MaskedRange, from: 1, to: 12, maxLength: 2}), Y: ({mask: window.IMask.MaskedRange, from: 1900, to: 9999})});
            }
        } else {
            options["mask"] = mask;
        }
        imask = new IMask(input, options);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}
export {decimal_separator};