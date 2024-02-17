var BASE_PATH, HelloWorld, TAG, TEMPLATE, comp, height, init, stub1_context, stub2_err, width;
TAG = "ptig-d3";
TEMPLATE = '        <div name=\"d3div\"></div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
HelloWorld = function () {
    _pyfunc_op_instantiate(this, arguments);
}
HelloWorld.prototype = Object.create(HTMLElement.prototype);
HelloWorld.prototype._base_class = HTMLElement.prototype;
HelloWorld.prototype.__name__ = "HelloWorld";

HelloWorld.prototype.__init__ = function () {
    console.log("Hello 1");
    return null;
};

HelloWorld.prototype.connectedCallback = function () {
    this.textContent = "Hello World!";
    return null;
};


stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/d3/d3.v3.min.js"]));
comp = stub1_context.__enter__();
try {
    width = function flx_width (component, old_value, new_value) {
        component.style.width = new_value;
        return null;
    };

    height = function flx_height (component, old_value, new_value) {
        component.style.height = new_value;
        return null;
    };

    comp.options["attributes"] = ({width: width, height: height});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _on_mouseout, _on_mouseover, circle, div, sample_svg;
        div = component.root.querySelector("div");
        sample_svg = d3.select(div).append("svg");
        sample_svg.attr("width", 100);
        sample_svg.attr("height", 100);
        _on_mouseover = function (event) {
            var obj;
            obj = d3.select(this);
            obj.style("fill", "aliceblue");
            return null;
        };

        _on_mouseout = function (event) {
            var obj;
            obj = d3.select(this);
            obj.style("fill", "white");
            return null;
        };

        circle = sample_svg.append("circle");
        circle.style("stroke", "gray");
        circle.style("fill", "white");
        circle.attr("r", 40);
        circle.attr("cx", 50);
        circle.attr("cy", 50);
        circle.on("mouseover", _on_mouseover);
        circle.on("mouseout", _on_mouseout);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}
export {HelloWorld};