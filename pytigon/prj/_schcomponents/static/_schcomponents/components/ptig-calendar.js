var BASE_PATH, TAG, TEMPLATE, comp, css_tab, height, init, js_tab, stub1_context, stub2_err, width;
TAG = "ptig-calendar";
TEMPLATE = '        <div class=\"ajax-frame ajax-link ajax-region\" data-region=\"table\" data-bind=\"onloadeddata:on_loaded_data\">\n' +
    '                <div name=\"calendar\" style=\"{ width: 100%, height: 100%}\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/jquery_plugins/fullcalendar";
js_tab = [BASE_PATH + "/main.min.js", "|", BASE_PATH + "/locales-all.min.js"];
css_tab = [BASE_PATH + "/main.min.css"];
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
        var calendar, click1, div, event_change, event_click, get_events, on_loaded_data, options, select, state;
        div = component.root.querySelector("div");
        get_events = (function flx_get_events (info, successCallback, failureCallback) {
            var _callback;
            if (_pyfunc_truthy(component.hasAttribute("href"))) {
                _callback = (function flx__callback (data) {
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
            var _callback, btn, eventObj, href, remove_mode;
            remove_mode = false;
            btn = component.querySelector(".fc-custom1-button");
            if (_pyfunc_truthy(btn)) {
                if (_pyfunc_truthy(btn.classList.contains("btn-danger"))) {
                    remove_mode = true;
                }
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
                    on_popup_edit_new(info.el, get_elem_from_string(data), href, null, null);
                    return null;
                }).bind(this);

                ajax_get(href, _callback);
            }
            return null;
        }).bind(this);

        select = (function flx_select (info) {
            var _callback, eventObj, href;
            eventObj = info.event;
            if (_pyfunc_truthy(component.hasAttribute("href-new"))) {
                href = _pymeth_replace.call(((_pymeth_replace.call(component.getAttribute("href-new"), "{start}", info.startStr))), "{end}", info.endStr);
                _callback = (function flx__callback (data) {
                    on_popup_edit_new(div, get_elem_from_string(data), href, null, null);
                    return null;
                }).bind(this);

                ajax_get(href, _callback);
            }
            return null;
        }).bind(this);

        event_change = (function flx_event_change (changeInfo) {
            var _callback;
            if (_pyfunc_truthy(component.hasAttribute("href"))) {
                _callback = (function flx__callback (data) {
                    calendar.refetchEvents();
                    return null;
                }).bind(this);

                ajax_json(component.getAttribute("href"), ({action: "calendar_change_event", id: changeInfo.event.id, start: changeInfo.event.startStr, end: changeInfo.event.endStr}), _callback);
            }
            return null;
        }).bind(this);

        options = ({events: get_events, headerToolbar: ({left: "dayGridMonth,timeGridWeek,timeGridDay custom1", center: "title", right: "today prevYear,prev,next,nextYear"}), customButtons: ({custom1: ({text: "Tryb kasowania", click: click1})}), height: "100%", locale: "pl", dayMaxEvents: true, editable: true, selectable: true, eventClick: event_click, select: select, eventChange: event_change, navLinks: true, slotDuration: "00:05:00"});
        if (_pyfunc_truthy(component.hasAttribute("duration"))) {
            options["slotDuration"] = component.getAttribute("duration");
        }
        calendar = new FullCalendar.Calendar(div, options);
        calendar.render();
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