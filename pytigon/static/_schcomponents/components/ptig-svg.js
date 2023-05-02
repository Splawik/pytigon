var TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-svg";
TEMPLATE = '<div name=\"svgdiv\" data-bind=\"style-width:width;style-height:height\">\n' +
    '        <slot></slot>\n' +
    '</div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _onfocusin, _onfocusout, _onmousedown, _onmouseout, _onmouseover, _onmouseup, div, state;
        div = component.root.querySelector("div");
        state = ({});
        state["onclick"] = window.handle_click;
        _onmouseover = (function flx__onmouseover (event) {
            console.log("onmouseover");
            return null;
        }).bind(this);

        state["onmouseover"] = _onmouseover;
        _onmouseout = (function flx__onmouseout (event) {
            console.log("onmouseout");
            return null;
        }).bind(this);

        state["onmouseout"] = _onmouseout;
        _onmousedown = (function flx__onmousedown (event) {
            console.log("onmousedown");
            return null;
        }).bind(this);

        state["onmousedown"] = _onmousedown;
        _onmouseup = (function flx__onmouseup (event) {
            console.log("onmouseup");
            return null;
        }).bind(this);

        state["onmouseup"] = _onmouseup;
        _onfocusin = (function flx__onfocusin (event) {
            console.log("onfocusin");
            return null;
        }).bind(this);

        state["onfocusin"] = _onfocusin;
        _onfocusout = (function flx__onfocusout (event) {
            console.log("onfocusout");
            return null;
        }).bind(this);

        state["onfocusout"] = _onfocusout;
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}