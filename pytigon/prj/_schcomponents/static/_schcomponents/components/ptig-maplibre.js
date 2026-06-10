var BASE_PATH, TAG, TEMPLATE, comp, constructor, init, stub1_context, stub2_err, stub5_context, stub6_err;
TAG = "ptig-maplibre";
TEMPLATE = '        <div class=\"maplibreframe\" data-bind=\"style-width:width;style-height:height\">\n' +
    '                <div class=\"maplibrediv\" style=\"width:100%;height:100%\"></div>\n' +
    '        </div>\n' +
    '        <slot></slot>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/_schcomponents/maplibre";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/maplibre.js"], [BASE_PATH + "/maplibre.css"], true));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null});
    comp.options["template"] = TEMPLATE;
    constructor = function flx_constructor (component) {
        var process_slot;
        component.markers = [];
        process_slot = (function flx_process_slot (slot) {
            _pymeth_append.call(component.markers, [slot.getAttribute("x"), slot.getAttribute("y"), slot.getAttribute("txt"), slot.getAttribute("href"), slot.getAttribute("target")]);
            return null;
        }).bind(this);

        component["process_slot"] = process_slot;
        return null;
    };

    comp.options["constructor"] = constructor;
    init = function flx_init (component) {
        var create, div, maplibregl, state, x, y, z;
        maplibregl = component.modules[0].maplibregl;
        div = component.root.querySelector("div.maplibrediv");
        if (_pyfunc_truthy(component.hasAttribute("x"))) {
            x = _pyfunc_float(component.getAttribute("x"));
        } else {
            x = 0;
        }
        if (_pyfunc_truthy(component.hasAttribute("y"))) {
            y = _pyfunc_float(component.getAttribute("y"));
        } else {
            y = 0;
        }
        if (_pyfunc_truthy(component.hasAttribute("z"))) {
            z = _pyfunc_float(component.getAttribute("z"));
        } else {
            z = 10;
        }
        if (_pyfunc_truthy(component.getAttribute("height"))) {
            state = ({height: component.getAttribute("height")});
            component.set_state(state);
        }
        create = (function flx_create () {
            var mapobj, on_load, style;
            style = ({version: 8, sources: ({osm: ({type: "raster", tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"], tileSize: 256, attribution: "&copy; <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors"})}), layers: [({id: "osm", type: "raster", source: "osm"})]});
            mapobj = new maplibregl.Map(({container: div, style: style, center: [y, x], zoom: z}));
            mapobj.addControl(new maplibregl.NavigationControl(), "top-right");
            mapobj.addControl(new maplibregl.GeolocateControl(), "top-right");
            on_load = (function flx_on_load () {
                var href, lat, lng, marker, on_click, pos, stub3_seq, stub4_itr, target, txt;
                if (_pyfunc_truthy(component.markers)) {
                    stub3_seq = component.markers;
                    if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                    for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                        pos = stub3_seq[stub4_itr];
                        lat = _pyfunc_float(pos[0]);
                        lng = _pyfunc_float(pos[1]);
                        txt = pos[2];
                        href = pos[3];
                        target = _pyfunc_truthy(pos[4]) || "_blank";
                        marker = ((((((new maplibregl.Marker()).setLngLat)([lng, lat])).setPopup)(((new maplibregl.Popup()).setHTML)(txt))).addTo)(mapobj);
                        if (_pyfunc_truthy(href)) {
                            on_click = (function flx_on_click (e) {
                                e.stopPropagation();
                                window.create_event_handler(href, target)(e);
                                return null;
                            }).bind(this);

                            (marker.getElement().addEventListener)("click", on_click);
                        }
                    }
                }
                component.mapobj = mapobj;
                window.dispatchEvent(new Event("resize"));
                return null;
            }).bind(this);

            mapobj.on("load", on_load);
            return null;
        }).bind(this);

        setTimeout(create, 1000);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}
stub5_context = (new DefineWebComponent("ptig-marker", false));
comp = stub5_context.__enter__();
try {
    comp.options["template"] = "";
    init = function flx_init (component) {
        component.parentNode.process_slot(component);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub6_err=err_0;
} finally {
    if (stub6_err) { if (!stub5_context.__exit__(stub6_err.name || "error", stub6_err, null)) { throw stub6_err; }
    } else { stub5_context.__exit__(null, null, null); }
}