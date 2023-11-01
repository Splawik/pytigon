var BASE_PATH, BASE_PATH0, TAG, TEMPLATE, comp, css_tab, height, init, js_tab, stub1_context, stub2_err, width;
TAG = "ptig-event-calendar";
TEMPLATE = '        <div class=\"ajax-frame ajax-link ajax-region\" data-region=\"table\" data-bind=\"onloadeddata:on_loaded_data\" style=\"position:absolute;top:5px;bottom:5px;left:5px;right:5px;\">\n' +
    '                <div name=\"calendar\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/event-calendar";
BASE_PATH0 = window.BASE_PATH + "static/vanillajs_plugins";
js_tab = [BASE_PATH + "/event-calendar.min.js"];
css_tab = [BASE_PATH + "/event-calendar.min.css", BASE_PATH0 + "/event-calendar-extra-styles.css"];
stub1_context = (new DefineWebComponent(TAG, false, js_tab, css_tab));
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
        var button_text, calendar, click1, div, event_change, event_click, get_events, item, l, on_loaded_data, options, resources, rid, select, state, stub5_seq, stub6_itr, stub7_, stub8_seq, stub9_itr, views;
        div = component.root.querySelector("div");
        get_events = (function flx_get_events (info, successCallback, failureCallback) {
            var _callback;
            if (_pyfunc_truthy(component.hasAttribute("href"))) {
                _callback = (function flx__callback (data) {
                    var row, stub3_seq, stub4_itr;
                    stub3_seq = data;
                    if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                    for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                        row = stub3_seq[stub4_itr];
                        row["start"] = new Date(_pymeth_replace.call(row["start"], "+00:00", ".000Z"));
                        row["end"] = new Date(_pymeth_replace.call(row["end"], "+00:00", ".000Z"));
                        row["resource_id"] = _pyfunc_int(row["resource_id"]);
                    }
                    successCallback(data);
                    return null;
                }).bind(this);

                ajax_json(component.getAttribute("href"), ({action: "calendar_events", start: info.startStr, end: info.endStr}), _callback);
            } else {
                successCallback([]);
            }
            return null;
        }).bind(this);

        click1 = (function flx_click1 (event) {
            if (_pyfunc_truthy(event.target.classList.contains("btn-danger"))) {
                _pymeth_remove.call(event.target.classList, "btn-danger");
            } else {
                event.target.classList.add("btn-danger");
            }
            return null;
        }).bind(this);

        event_click = (function flx_event_click (info) {
            var _callback, eventObj, href, remove_mode;
            remove_mode = false;
            if (_pyfunc_op_equals(info.view.type, "listWeek")) {
                remove_mode = true;
            }
            eventObj = info.event;
            if (_pyfunc_truthy(remove_mode)) {
                if (_pyfunc_truthy(component.hasAttribute("href-delete"))) {
                    href = _pymeth_replace.call(component.getAttribute("href-delete"), "{id}", _pyfunc_str(eventObj.id));
                } else if (_pyfunc_truthy(component.hasAttribute("href-edit"))) {
                    href = _pymeth_replace.call(((_pymeth_replace.call(component.getAttribute("href-edit"), "{id}", _pyfunc_str(eventObj.id)))), "/edit/", "/delete/");
                }
                if (_pyfunc_truthy(href)) {
                    _callback = (function flx__callback (data) {
                        on_popup_delete(info.el, get_elem_from_string(data), href, null, null);
                        return null;
                    }).bind(this);

                    ajax_get(href, _callback);
                }
            } else if (_pyfunc_truthy(component.hasAttribute("href-edit"))) {
                href = _pymeth_replace.call(component.getAttribute("href-edit"), "{id}", _pyfunc_str(eventObj.id));
                _callback = (function flx__callback (data) {
                    if (_pyfunc_truthy((_pyfunc_truthy(component.hasAttribute("href-edit-target"))) && ((_pyfunc_op_contains(component.getAttribute("href-edit-target"), ["_parent", "_top2"]))))) {
                        on_new_tab(info.el, get_elem_from_string(data), href, null, null);
                    } else {
                        on_popup_edit_new(info.el, get_elem_from_string(data), href, null, null);
                    }
                    return null;
                }).bind(this);

                ajax_get(href, _callback);
            }
            return null;
        }).bind(this);

        select = (function flx_select (info) {
            var _callback, end, eventObj, href, resource_id, start;
            eventObj = info.event;
            if (_pyfunc_truthy(component.hasAttribute("href-new"))) {
                if (_pyfunc_hasattr(info, "startStr")) {
                    start = info.startStr;
                    end = info.endStr;
                } else {
                    start = _pymeth_format.call(moment(info.date));
                    end = _pymeth_format.call(moment(info.date));
                }
                if (_pyfunc_hasattr(info, "resource")) {
                    resource_id = _pyfunc_str(info.resource.id);
                } else {
                    resource_id = 0;
                }
                href = _pymeth_replace.call(((_pymeth_replace.call(((_pymeth_replace.call(component.getAttribute("href-new"), "{start}", start))), "{end}", end))), "{resource_id}", resource_id);
                _callback = (function flx__callback (data) {
                    on_popup_edit_new(div, get_elem_from_string(data), href, null, null);
                    return null;
                }).bind(this);

                ajax_get(href, _callback);
            }
            return null;
        }).bind(this);

        event_change = (function flx_event_change (changeInfo) {
            var _callback, end, resource_id, start;
            if (_pyfunc_truthy(component.hasAttribute("href"))) {
                _callback = (function flx__callback (data) {
                    calendar.refetchEvents();
                    return null;
                }).bind(this);

                start = _pymeth_format.call(moment(changeInfo.event.start));
                end = _pymeth_format.call(moment(changeInfo.event.end));
                if (_pyfunc_hasattr(changeInfo.event, "resourceIds")) {
                    resource_id = _pyfunc_str(changeInfo.event.resourceIds[0]);
                } else {
                    resource_id = 0;
                }
                ajax_json(component.getAttribute("href"), ({action: "calendar_change_event", id: changeInfo.event.id, start: start, end: end, resource_id: resource_id}), _callback);
            }
            return null;
        }).bind(this);

        button_text = (function flx_button_text (texts) {
            texts.today = gettext("today");
            texts.dayGridMonth = gettext("month");
            texts.listDay = gettext("list");
            texts.listWeek = gettext("delete mode");
            texts.listMonth = gettext("list");
            texts.listYear = gettext("list");
            texts.resourceTimeGridDay = gettext("resources - day");
            texts.resourceTimeGridWeek = gettext("resources - week");
            texts.timeGridDay = gettext("day");
            texts.timeGridWeek = gettext("week");
            return texts;
        }).bind(this);

        options = ({view: "resourceTimeGridWeek", height: "100%", eventSources: [({events: get_events})], allDaySlot: false, nowIndicator: true, eventClick: event_click, selectable: true, select: select, dateClick: select, editable: true, eventDrop: event_change, eventResize: event_change, headerToolbar: ({start: "prev,next today", center: "title", end: "dayGridMonth, timeGridWeek, timeGridDay, listMonth, resourceTimeGridDay, resourceTimeGridWeek, listWeek"}), buttonText: button_text});
        if (_pyfunc_truthy(component.hasAttribute("view"))) {
            options["view"] = component.getAttribute("view");
        }
        if (_pyfunc_truthy(component.hasAttribute("views"))) {
            views = [];
            stub5_seq = _pymeth_split.call(component.getAttribute("resources"), ";");
            if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
            for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
                item = stub5_seq[stub6_itr];
                if (_pyfunc_truthy(item)) {
                    _pymeth_append.call(views, (_pyfunc_create_dict(item, ({pointer: true}))));
                }
            }
            options["views"] = component.getAttribute("view");
        }
        if (_pyfunc_truthy(component.hasAttribute("alldayslot"))) {
            options["allDaySlot"] = true;
        }
        if (_pyfunc_truthy(component.hasAttribute("toolbar-buttons"))) {
            options["headerToolbar"]["end"] = component.getAttribute("toolbar-buttons");
        }
        if (_pyfunc_truthy(component.hasAttribute("noselectable"))) {
            options["selectable"] = false;
        }
        if (_pyfunc_truthy(component.hasAttribute("noeditabe"))) {
            options["editable"] = false;
        }
        if (_pyfunc_truthy(component.hasAttribute("resources"))) {
            resources = [];
            l = 1;
            stub8_seq = _pymeth_split.call(component.getAttribute("resources"), ";");
            if ((typeof stub8_seq === "object") && (!Array.isArray(stub8_seq))) { stub8_seq = Object.keys(stub8_seq);}
            for (stub9_itr = 0; stub9_itr < stub8_seq.length; stub9_itr += 1) {
                item = stub8_seq[stub9_itr];
                if (_pyfunc_truthy(item)) {
                    if (_pyfunc_op_contains(":", item)) {
                        stub7_ = _pymeth_split.call(item, ":", 1);
                        rid = stub7_[0];item = stub7_[1];
                        rid = _pyfunc_int(rid);
                    } else {
                        rid = l;
                    }
                    _pymeth_append.call(resources, ({id: rid, title: item}));
                    l += 1;
                }
            }
            options["resources"] = resources;
        }
        if (_pyfunc_truthy(component.hasAttribute("duration"))) {
            options["slotDuration"] = component.getAttribute("duration");
        }
        calendar = new EventCalendar(div, options);
        on_loaded_data = (function flx_on_loaded_data (event) {
            calendar.refetchEvents();
            return null;
        }).bind(this);

        state = ({on_loaded_data: on_loaded_data});
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}