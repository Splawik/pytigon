var BASE_PATH, BASE_PLOTLY_PATH, TAG, TEMPLATE, comp, from_dict, init, on_plotly, process_response_data, stub5_context, stub6_err, transform_event_data;
TAG = "ptig-plotly";
TEMPLATE = '        <div name=\"plotlydiv\" data-bind:style-width:width;style-height:height></div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
BASE_PLOTLY_PATH = window.BASE_PATH + "schdoc/plot_service/";
from_dict = function flx_from_dict (d, name) {
    if (_pyfunc_op_contains(name, d)) {
        return d[name];
    } else {
        return ({});
    }
    return null;
};

transform_event_data = function flx_transform_event_data (data) {
    var key, p, point, pp, ret, stub1_seq, stub2_itr, stub3_seq, stub4_itr;
    ret = ({});
    if (_pyfunc_op_contains("destination", data)) {
        ret["destination"] = data["destination"];
    }
    if (_pyfunc_op_contains("event_name", data)) {
        ret["event_name"] = data["event_name"];
    }
    if (_pyfunc_op_contains("points", data)) {
        pp = [];
        stub3_seq = data["points"];
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            point = stub3_seq[stub4_itr];
            p = ({});
            stub1_seq = ["curveNumber", "pointNumber", "x", "y", "z", "lat", "lon"];
            if ((typeof stub1_seq === "object") && (!Array.isArray(stub1_seq))) { stub1_seq = Object.keys(stub1_seq);}
            for (stub2_itr = 0; stub2_itr < stub1_seq.length; stub2_itr += 1) {
                key = stub1_seq[stub2_itr];
                if (_pyfunc_truthy(point.hasOwnProperty(key))) {
                    p[key] = point[key];
                }
            }
            _pymeth_append.call(pp, p);
        }
        ret["points"] = pp;
    }
    return ret;
};

process_response_data = function flx_process_response_data (component, data) {
    var el, fun, layout;
    if ((_pyfunc_op_contains("redirect", data) && _pyfunc_truthy(data["redirect"]))) {
        data["redirect"] = false;
        window.GLOBAL_BUS.emit("plotly", data);
    } else if (_pyfunc_op_contains("function", data)) {
        fun = data["function"];
        el = component.div;
        layout = from_dict(data, "layout");
        if (_pyfunc_truthy(component.width)) {
            layout["width"] = component.width;
        }
        if (_pyfunc_truthy(component.height)) {
            layout["height"] = component.height;
        }
        if (_pyfunc_op_equals(fun, "newPlot")) {
            Plotly.newPlot(el, from_dict(data, "data"), layout, from_dict(data, "config"));
        } else if (_pyfunc_op_equals(fun, "react")) {
            Plotly.react(el, from_dict(data, "data"), layout, from_dict(data, "config"));
        } else if (_pyfunc_op_equals(fun, "restyle")) {
            if (_pyfunc_op_contains("traceIndices", data)) {
                Plotly.restyle(el, from_dict(data, "update"), from_dict(data, "traceIndices"));
            } else {
                Plotly.restyle(el, from_dict(data, "update"));
            }
        } else if (_pyfunc_op_equals(fun, "relayout")) {
            Plotly.relayout(el, from_dict(data, "update"));
        } else if (_pyfunc_op_equals(fun, "update")) {
            if (_pyfunc_op_contains("traceIndices", data)) {
                Plotly.restyle(el, from_dict(data, "data"), from_dict(data, "layout"), from_dict(data, "traceIndices"));
            } else {
                Plotly.restyle(el, from_dict(data, "data"), from_dict(data, "layout"));
            }
        } else if (_pyfunc_op_equals(fun, "addTraces")) {
            if (_pyfunc_op_contains("id", data)) {
                Plotly.addTraces(el, from_dict(data, "traces"), data["id"]);
            } else {
                Plotly.addTraces(el, from_dict(data, "traces"));
            }
        } else if (_pyfunc_op_equals(fun, "deleteTraces")) {
            Plotly.deleteTraces(el, from_dict(data, "traceIndices"));
        } else if (_pyfunc_op_equals(fun, "moveTraces")) {
            if (_pyfunc_op_contains("id", data)) {
                Plotly.moveTraces(el, from_dict(data, "traceIndices"), data["id"]);
            } else {
                Plotly.moveTraces(el, from_dict(data, "traceIndices"));
            }
        } else if (_pyfunc_op_equals(fun, "extendTraces")) {
            Plotly.extendTraces(el, from_dict(data, "traces"), from_dict(data, "traceIndices"));
        } else if (_pyfunc_op_equals(fun, "prependTraces")) {
            Plotly.prependTraces(el, from_dict(data, "traces"), from_dict(data, "traceIndices"));
        } else if (_pyfunc_op_equals(fun, "addFrames")) {
        } else if (_pyfunc_op_equals(fun, "animate")) {
        }
    }
    return null;
};

stub5_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/plotly/plotly.min.js", BASE_PATH + "/d3/d3.v3.min.js"], [BASE_PATH + "/plotly/plotly.css"]));
comp = stub5_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null});
    comp.options["template"] = TEMPLATE;
    on_plotly = function flx_on_plotly (component, data) {
        if ((_pyfunc_op_contains("destination", data) && ((_pyfunc_op_equals(data["destination"], (("plotly/" + component.getAttribute("plotly-name")) + "/")))))) {
            process_response_data(component, data);
        }
        return null;
    };

    comp.options["global_state_actions"] = ({plotly: on_plotly});
    init = function flx_init (component) {
        var _onloadeddata, config, data, div, events, layout, on_config_loaded, on_data_loaded, on_layout_loaded, on_loaded, parent, plotly_name, run_script, src, url;
        div = component.root.querySelector("div");
        component.div = div;
        if (_pyfunc_truthy(component.hasAttribute("plotly-name"))) {
            plotly_name = component.getAttribute("plotly-name");
            url = _pyfunc_op_add(BASE_PLOTLY_PATH, plotly_name) + "/";
            if (_pyfunc_truthy(component.hasAttribute("param"))) {
                url = _pyfunc_op_add(url, "?param=" + component.getAttribute(param));
            }
        } else {
            url = null;
        }
        data = null;
        layout = null;
        config = null;
        events = null;
        on_loaded = (function flx_on_loaded () {
            var _callback, make_callback, plot, pos, stub7_seq, stub8_itr, x;
            if (_pyfunc_truthy(component.hasAttribute("width"))) {
                layout["width"] = component.getAttribute("widht");
            }
            if (_pyfunc_truthy(component.hasAttribute("height"))) {
                layout["height"] = component.getAttribute("height");
            }
            plot = Plotly.newPlot(div, data, layout, config);
            component.plot = plot;
            if (_pyfunc_truthy(events)) {
                stub7_seq = events;
                if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
                for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
                    pos = stub7_seq[stub8_itr];
                    if (_pyfunc_op_contains("=>", pos)) {
                        x = _pymeth_split.call(pos, "=>");
                        _callback = (function flx__callback (data1) {
                            data1["destination"] = x[1];
                            data1["event_name"] = x[0];
                            window.GLOBAL_BUS.emit("plotly", data1);
                            return null;
                        }).bind(this);

                        div.on("plotly_" + x[0], _callback);
                    } else {
                        make_callback = (function flx_make_callback (event_name) {
                            var _callback;
                            _callback = (function flx__callback (data2) {
                                var _on_server_response;
                                data2["event_name"] = event_name;
                                _on_server_response = (function flx__on_server_response (server_data) {
                                    server_data["event_name"] = event_name;
                                    process_response_data(component, server_data);
                                    return null;
                                }).bind(this);

                                ajax_json(url, ({name: component.getAttribute("plotly-name"), action: "on_event", event_name: event_name, data: transform_event_data(data2)}), _on_server_response);
                                return null;
                            }).bind(this);

                            return _callback;
                        }).bind(this);

                        div.on("plotly_" + pos, make_callback(pos));
                    }
                }
            }
            return null;
        }).bind(this);

        on_data_loaded = (function flx_on_data_loaded (_data) {
            data = _data["data"];
            if (_pyfunc_op_contains("events", _data)) {
                events = _data["events"];
            }
            if ((((!_pyfunc_op_equals(layout, null))) && ((!_pyfunc_op_equals(config, null))))) {
                on_loaded();
            }
            return null;
        }).bind(this);

        on_layout_loaded = (function flx_on_layout_loaded (_data) {
            layout = _data;
            if ((((!_pyfunc_op_equals(data, null))) && ((!_pyfunc_op_equals(config, null))))) {
                on_loaded();
            }
            return null;
        }).bind(this);

        on_config_loaded = (function flx_on_config_loaded (_data) {
            config = _data;
            if ((((!_pyfunc_op_equals(data, null))) && ((!_pyfunc_op_equals(layout, null))))) {
                on_loaded();
            }
            return null;
        }).bind(this);

        if (_pyfunc_truthy(url)) {
            ajax_json(url, ({name: plotly_name, action: "get_data"}), on_data_loaded);
            ajax_json(url, ({name: plotly_name, action: "get_layout"}), on_layout_loaded);
            ajax_json(url, ({name: plotly_name, action: "get_config"}), on_config_loaded);
        } else {
            parent = component.parentElement;
            div = component.children[0].children[0];
            src = component.children[0].children[1];
            parent.append(div);
            run_script = (function flx_run_script () {
                if (_pyfunc_truthy(document.getElementById(div.id))) {
                    eval(src.innerHTML);
                } else {
                    setTimeout(run_script, 100);
                }
                return null;
            }).bind(this);

            setTimeout(run_script, 100);
            _onloadeddata = function (event) {
                var src, tmp;
                tmp = document.createElement("div");
                tmp.innerHTML = event.data;
                src = tmp.querySelector("script");
                eval(src.innerHTML);
                console.log("BZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ");
                return null;
            };

            component.onloadeddata = _onloadeddata;
        }
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub6_err=err_0;
} finally {
    if (stub6_err) { if (!stub5_context.__exit__(stub6_err.name || "error", stub6_err, null)) { throw stub6_err; }
    } else { stub5_context.__exit__(null, null, null); }
}
export {from_dict, transform_event_data, process_response_data};