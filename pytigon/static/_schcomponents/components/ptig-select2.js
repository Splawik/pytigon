var BASE_PATH, TAG, TEMPLATE, comp, constructor, init, stub1_context, stub2_err;
import {JSONPath} from '../../vanillajs_plugins/jsonpath_plus/index-es.min.js';;
TAG = "ptig-select2";
TEMPLATE = '        <div class=\"ajax-region input-group flex-nowrap\" style=\"position:relative;\" data-bind=\"style-padding-right:padding;style-width:width\" data-region=\"get_row\">\n' +
    '                <select style=\"width:100%;\" data-bind=\":multiple\"></select>\n' +
    '                <a type=\"button\" target=\"popup_info\" name=\"get_tbl_value\" class=\"btn btn-secondary btn-flat foreignkey_button get_tbl_value\" data-inline-position=\"^div.ajax-region:append\" style=\"position:absolute;right:2px\" data-bind=\"style-visibility:visibility;:href\">\n' +
    '                        <span class=\"fa-table fa\"></span>\n' +
    '                </a>\n' +
    '        </div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/jquery_plugins/select2";
stub1_context = (new DefineWebComponent(TAG, false));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, multiple: null, href: null, target: null});
    constructor = function flx_constructor (component) {
        component.style.display = "none";
        return null;
    };

    comp.options["constructor"] = constructor;
    init = function flx_init (component) {
        var _onloadeddata, _set_select2_value, ajax_options, append_to, data, elem, graphql, options, process_results, query, select, state;
        elem = document.createElement("div");
        elem.innerHTML = TEMPLATE;
        select = elem.querySelector("select");
        options = ({theme: "bootstrap-5"});
        graphql = component.querySelector("graphql");
        if (_pyfunc_truthy(graphql)) {
            query = graphql.innerHTML;
            data = (function flx_data (params) {
                if (_pyfunc_truthy(params.term)) {
                    return ({query: _pymeth_replace.call(query, "$$$", params.term)});
                } else {
                    return ({query: _pymeth_replace.call(query, "$$$", "")});
                }
                return null;
            }).bind(this);

            process_results = (function flx_process_results (data) {
                var pos, stub3_seq, stub4_itr, tmp;
                tmp = new JSONPath(({path: "$..node", json: data}));
                stub3_seq = tmp;
                if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                    pos = stub3_seq[stub4_itr];
                    pos["id"] = _pymeth_split.call(atob(pos["id"]), ":")[1];
                }
                return ({results: tmp});
            }).bind(this);

            ajax_options = ({});
            ajax_options["processResults"] = process_results;
            ajax_options["data"] = data;
            ajax_options["type"] = "post";
            ajax_options["dataType"] = "json";
            ajax_options["delay"] = 250;
            ajax_options["cache"] = true;
            ajax_options["url"] = window.BASE_PATH + "graphql/";
            options["ajax"] = ajax_options;
        } else {
            data = [];
            append_to = (function flx_append_to (parent, children) {
                var append;
                append = (function flx_append (item, index) {
                    var tmp;
                    if ((_pyfunc_op_equals(_pymeth_lower.call(item.tagName), "optgroup"))) {
                        tmp = [];
                        append_to(tmp, item.children);
                        _pymeth_append.call(parent, ({text: item.innerHTML, children: tmp}));
                    } else if ((_pyfunc_op_equals(_pymeth_lower.call(item.tagName), "option"))) {
                        if (_pyfunc_truthy(item.hasAttribute("value"))) {
                            _pymeth_append.call(parent, (({id: item.getAttribute("value"), text: item.innerHTML})));
                        }
                    }
                    return null;
                }).bind(this);

                children.forEach(append);
                return null;
            }).bind(this);

            append_to(data, component.children);
            options["data"] = data;
        }
        component.innerHTML = "";
        component.appendChild(elem);
        (jQuery(select).select2)(options);
        _set_select2_value = (function flx__set_select2_value (sel2, id, text) {
            _pymeth_append.call(sel2, (jQuery("<option>", ({value: id, text: text}))));
            sel2.val(id.toString());
            sel2.trigger("change");
            return null;
        }).bind(this);

        _onloadeddata = (function flx__onloadeddata (event) {
            var id, src_elem, text;
            if (_pyfunc_hasattr(event, "data_source")) {
                src_elem = event.data_source;
                if (_pyfunc_truthy(src_elem)) {
                    id = src_elem.getAttribute("data-id");
                    text = src_elem.getAttribute("data-text");
                    _set_select2_value(jQuery(select), id, text);
                }
            }
            return null;
        }).bind(this);

        select.onloadeddata = _onloadeddata;
        select.classList.add("ajax-frame");
        select.setAttribute("data-region", "get_row");
        component.style.display = "block";
        if (_pyfunc_truthy(component.hasAttribute("href"))) {
            state = ({padding: "52px", visibility: "visible"});
        } else {
            state = ({padding: "2px", visibility: "hidden"});
        }
        state["onclick"] = window.handle_click;
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}