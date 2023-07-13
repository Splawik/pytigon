var BASE_PATH, TAG, TEMPLATE, comp, constructor, init, stub1_context, stub2_err, stub5_context, stub6_err;
TAG = "ptig-leaflet";
TEMPLATE = '        <div class=\"leafletframe\" data-bind=\"style-width:width;style-height:height\">\n' +
    '                <div class=\"leafletdiv\" style=\"width:100%;height:100%\"></div>\n' +
    '        </div>\n' +
    '        <slot></slot>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/leaflet";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/leaflet.js"], [BASE_PATH + "/leaflet.css"]));
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
        var create, div, state, x, y, z;
        div = component.root.querySelector("div.leafletdiv");
        L.Icon.Default.imagePath = BASE_PATH + "/images";
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
            z = 13;
        }
        if (_pyfunc_truthy(component.getAttribute("height"))) {
            state = ({height: component.getAttribute("height")});
            component.set_state(state);
        }
        create = (function flx_create () {
            var mapobj, marker, pos, stub3_seq, stub4_itr;
            mapobj = (L.map(div).setView)([x, y], z);
            ((L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", ({attribution: "&copy; <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors"}))).addTo)(mapobj);
            if (_pyfunc_truthy(component.markers)) {
                stub3_seq = component.markers;
                if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                    pos = stub3_seq[stub4_itr];
                    marker = L.marker([pos[0], pos[1]]);
                    marker.addTo(mapobj);
                    marker.bindPopup(pos[2]);
                    marker.openPopup();
                    if (_pyfunc_truthy(pos[3])) {
                        marker.on("click", window.create_event_handler(pos[3], pos[4]));
                    }
                }
            }
            component.mapobj = mapobj;
            window.dispatchEvent(new Event("resize"));
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