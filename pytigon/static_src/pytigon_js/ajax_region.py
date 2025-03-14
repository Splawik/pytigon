# from pytigon_js.tools import Loading, correct_href, ajax_get, ajax_post, get_table_type, super_insert
# from pytigon_js.tbl import init_table


def data_type(data_or_html):
    if data_or_html:
        if isinstance(data_or_html, str):
            if "$$RETURN_OK" in data_or_html:
                return "$$RETURN_OK"
            elif "$$RETURN_NEW_ROW_OK" in data_or_html:
                return "$$RETURN_NEW_ROW_OK"
            elif "$$RETURN_UPDATE_ROW_OK" in data_or_html:
                return "$$RETURN_UPDATE_ROW_OK"
            elif "$$RETURN_REFRESH_PARENT" in data_or_html:
                return "$$RETURN_REFRESH_PARENT"
            elif "$$RETURN_RELOAD_PAGE" in data_or_html:
                return "$$RETURN_RELOAD_PAGE"
            elif "$$RETURN_REFRESH" in data_or_html:
                return "$$RETURN_REFRESH"
            elif "$$RETURN_CANCEL" in data_or_html:
                return "$$RETURN_CANCEL"
            elif "$$RETURN_RELOAD" in data_or_html:
                return "$$RETURN_RELOAD"
            elif "$$RETURN_ERROR" in data_or_html:
                return "$$RETURN_ERROR"
            elif "$$RETURN_REFRESH_AUTO_FRAME" in data_or_html:
                return "$$RETURN_REFRESH_AUTO_FRAME"
            elif "$$RETURN_HTML_ERROR" in data_or_html:
                return "$$RETURN_HTML_ERROR"
            elif "$$RETURN_JSON" in data_or_html:
                return "$$RETURN_JSON"
        else:
            meta_list = Array.prototype.slice.call(
                data_or_html.querySelectorAll("meta")
            )
            for pos in meta_list:
                if pos.hasAttribute("name"):
                    if pos.getAttribute("name").upper() == "RETURN":
                        if pos.hasAttribute("content"):
                            return pos.getAttribute("content").upper()
    return "$$RETURN_HTML"


MOUNT_INIT_FUN = []


def register_mount_fun(fun):
    global MOUNT_INIT_FUN
    MOUNT_INIT_FUN.append(fun)


window.register_mount_fun = register_mount_fun


def mount_html(dest_elem, data_or_html, link=None):
    global MOUNT_INIT_FUN

    replace = False

    if dest_elem == None:
        return None

    if (
        hasattr(dest_elem, "onloadeddata")
        and getattr(dest_elem, "onloadeddata")
        and dest_elem.onloadeddata
    ):
        evt = document.createEvent("HTMLEvents")
        evt.initEvent("loadeddata", False, True)
        evt.data = data_or_html
        evt.data_source = link
        dest_elem.dispatchEvent(evt)
        return dest_elem

    if dest_elem.hasAttribute("data-link"):
        attr = dest_elem.getAttribute("data-link")
        if attr == "..":
            replace = True
        else:
            obj = window.super_query_selector(
                dest_elem, dest_elem.getAttribute("data-link")
            )
            if obj:
                dest_elem = obj

    if data_or_html != None:

        def _on_remove(index, value):
            value.on_remove()

        jQuery.each(jQuery(dest_elem).find(".call_on_remove"), _on_remove)

        if dest_elem.children.length > 0:
            elem2 = dest_elem.cloneNode()
            if jQuery.type(data_or_html) == "string":
                window.IN_MORPH_PROCESS = True
                elem2.innerHTML = data_or_html
                window.IN_MORPH_PROCESS = False
                if replace:
                    if elem2.children.length > 0:
                        elem2 = elem2.children[0]
            else:
                if (
                    data_or_html.tagName.lower() == "div"
                    and data_or_html.classList.contains("ajax-temp-item")
                ):
                    for item in Array.prototype.slice.call(data_or_html.children):
                        if replace:
                            elem2.replaceWith(item)
                            break
                        else:
                            elem2.appendChild(item)
                else:
                    if replace:
                        elem2.replaceWith(data_or_html)
                    else:
                        elem2.appendChild(data_or_html)
            Idiomorph.morph(dest_elem, elem2)
        else:
            if jQuery.type(data_or_html) == "string":
                dest_elem.innerHTML = data_or_html
                if replace:
                    if dest_elem.children.length > 0:
                        dest_elem.replaceWith(dest_elem.children[0])
            else:
                if (
                    data_or_html.tagName.lower() == "div"
                    and data_or_html.classList.contains("ajax-temp-item")
                ):
                    for item in Array.prototype.slice.call(data_or_html.children):
                        if replace:
                            dest_elem.replaceWith(item)
                            break
                        else:
                            dest_elem.appendChild(item)
                else:
                    if replace:
                        dest_elem.replaceWith(data_or_html)
                    else:
                        dest_elem.appendChild(data_or_html)

    if MOUNT_INIT_FUN:
        for fun in MOUNT_INIT_FUN:
            fun(dest_elem)

    return dest_elem


window.mount_html = mount_html


# def datetime_init(dest_elem):
#    format = {
#        "singleDatePicker": True,
#        "showDropdowns": True,
#        "buttonClasses": "btn",
#        "applyClass": "btn-success align-top",
#        "cancelClass": "btn-danger btn-sm align-top",
#        "timePicker24Hour": True,
#        "autoApply": True,
#        "locale": {
#            "format": "YYYY-MM-DD",
#            "separator": "-",
#            "applyLabel": "&nbsp; OK &nbsp;",
#            "cancelLabel": "<i class='fa fa-close'></i>",
#        },
#    }
#
#    d = jQuery(dest_elem).find("div.group_datefield input")
#    d.daterangepicker(format)
#
#    format["locale"]["format"] = "YYYY-MM-DD HH:mm"
#    format["timePicker"] = True
#    format["timePickerIncrement"] = 30
#
#    d = jQuery(dest_elem).find("div.group_datetimefield input")
#    d.daterangepicker(format)

# register_mount_fun(datetime_init)


def selectpicker_init(dest_elem):
    if hasattr(jQuery.fn, "selectpicker"):
        jQuery(dest_elem).find(".selectpicker").selectpicker()


register_mount_fun(selectpicker_init)


def auto_frame_init(dest_elem):
    frame_list = Array.prototype.slice.call(dest_elem.querySelectorAll(".auto-frame"))
    for elem in frame_list:
        refresh_ajax_frame(elem)


register_mount_fun(auto_frame_init)


def _on_shown_bs_tab(event):
    if event.target.hasAttribute("data-bs-target"):
        target = event.target.getAttribute("data-bs-target")
        div = event.target.closest("div.auto-refresh")
        frame = div.querySelector(target)
        if frame.hasAttribute("auto-refresh-target"):
            auto_refresh_target = frame.getAttribute("auto-refresh-target")
            item_list = Array.prototype.slice.call(
                frame.querySelectorAll(auto_refresh_target)
            )
            for item in item_list:
                window.refresh_ajax_frame(item)
        else:
            refresh_ajax_frame(frame)


def auto_refresh_tab(dest_elem):
    item_list = Array.prototype.slice.call(
        dest_elem.querySelectorAll("div.auto-refresh button")
    )
    for elem in item_list:
        elem.addEventListener("shown.bs.tab", _on_shown_bs_tab)


register_mount_fun(auto_refresh_tab)


def get_click_on_focus_fun(element):
    def _click(event):
        nonlocal element
        if not document.hidden:
            element.click()

    return _click


def get_refresh_on_focus_fun(element):
    def _refresh(event):
        nonlocal element
        if not document.hidden:
            refresh_ajax_frame(element)

    return _refresh


def on_focus_action(dest_elem):
    item_list = Array.prototype.slice.call(
        dest_elem.querySelectorAll(".on-focus-action")
    )
    for elem in item_list:
        fun = None
        if elem.classList.contains("on-focus-action-click"):
            fun = get_click_on_focus_fun(elem)
        elif elem.classList.contains("on-focus-action-refresh"):
            fun = get_refresh_on_focus_fun(elem)
        if fun:
            window.addEventListener("visibilitychange", fun)


register_mount_fun(on_focus_action)


def moveelement_init(dest_elem):
    objs = Array.prototype.slice.call(dest_elem.querySelectorAll(".move-element"))
    if objs:
        for obj in objs:
            if obj.hasAttribute("data-position"):
                obj.classList.remove("move-element")
                data_position = obj.getAttribute("data-position")

                parent = obj.parentElement
                elem2 = super_insert(dest_elem, obj.getAttribute("data-position"), obj)
                if not elem2:
                    continue

                if data_position.endswith(":class"):

                    def _on_remove():
                        nonlocal obj, elem2
                        for c in Array.prototype.slice.call(obj.classList):
                            elem2.classList.remove(c)

                else:

                    def _on_remove():
                        nonlocal obj
                        obj.remove()

                parent.on_remove = _on_remove
                parent.classList.add("call_on_remove")


register_mount_fun(moveelement_init)


# def label_floating_init(dest_elem):
#    def _on_blur(self, e):
#        if self.tagName.lower() == "input":
#            if e["type"] == "focus" or self.value.length > 0:
#                test = True
#            else:
#                test = False
#        else:
#            test = True
#        jQuery(self).parents(".form-group").toggleClass("focused", test)
#
#    jQuery(dest_elem).find(".label-floating .form-control").on(
#        "focus blur", _on_blur
#    ).trigger("blur")
#
#    def _on_blur2(self, e):
#        jQuery(self).parents(".form-group").toggleClass("focused", True)
#
#    jQuery(dest_elem).find(".label-floating .form-control-file").on(
#        "focus blur", _on_blur2
#    ).trigger("blur")


# register_mount_fun(label_floating_init)


def set_select2_value(sel2, id, text):
    sel2.append(jQuery("<option>", {"value": id, "text": text}))
    sel2.val(id.toString())
    sel2.trigger("change")


def create_onloadeddata(control):
    def _onloadeddata(self, event):
        nonlocal control
        if hasattr(event, "data_source"):
            src_elem = event.data_source
            if src_elem:
                id = src_elem.getAttribute("data-id")
                text = src_elem.getAttribute("data-text")
                if id and text:
                    set_select2_value(jQuery(control), id, text)

    return _onloadeddata


def init_select2_ctrl(self):
    sel2 = jQuery(self)
    src = sel2.closest(".input-group")
    if src.length == 1:
        if src[0].hasAttribute("item_id"):
            id = src.attr("item_id")
            if id:
                text = src.attr("item_str")
                set_select2_value(sel2, id, text)


def select2_init(dest_elem):
    # jQuery(dest_elem).find(".django-select2:not(.select2-full-width)").djangoSelect2(
    #    {"width": "calc(100% - 48px)", "minimumInputLength": 0, "theme": "bootstrap-5"}
    # )
    # jQuery(dest_elem).find(".django-select2.select2-full-width").djangoSelect2(
    #    {"width": "calc(100%)", "minimumInputLength": 0, "theme": "bootstrap-5"}
    # )

    # jQuery(dest_elem).find(".django-select2:not(.select2-full-width)").djangoSelect2(
    #    {"minimumInputLength": 0, "placeholder": "Select an option", 'dropdownParent': jQuery(dest_elem) }
    # )
    # jQuery(dest_elem).find(".django-select2.select2-full-width").djangoSelect2(
    #    {"minimumInputLength": 0, "placeholder": "Select an option", 'dropdownParent': jQuery(dest_elem)}
    # )

    controls = Array.prototype.slice.call(dest_elem.querySelectorAll(".django-select2"))
    if controls:
        for control in controls:
            modal = control.closest(".modal")
            if modal:
                jQuery(control).djangoSelect2(
                    {
                        "minimumInputLength": 0,
                        "placeholder": "Select an option",
                        "dropdownParent": jQuery(modal),
                    }
                )
            else:
                jQuery(control).djangoSelect2(
                    {
                        "minimumInputLength": 0,
                        "placeholder": "Select an option",
                    }
                )
            control.onloadeddata = create_onloadeddata(control)
            control.classList.add("ajax-frame")
            control.setAttribute("data-region", "get_row")

    jQuery(dest_elem).find(".django-select2").each(init_select2_ctrl)


register_mount_fun(select2_init)


def select_combo_init(dest_elem):
    select_ctrl_list = Array.prototype.slice.call(
        dest_elem.querySelectorAll(".select_combo")
    )

    def on_change_element(element):
        region = element.closest(".ajax-region")
        if region != None:
            next_elements = document.getElementsByName(
                element.getAttribute("data-rel-name")
            )
            if next_elements.length > 0:
                next_element = next_elements[0]

                if next_element.hasAttribute("src"):
                    src = next_element.getAttribute("src")
                    if element.value:
                        src = process_href(src, jQuery(element))

                        def _onload(responseText):
                            nonlocal next_element, src
                            if (
                                hasattr(next_element, "onloadeddata")
                                and getattr(next_element, "onloadeddata")
                                and next_element.onloadeddata
                            ):
                                evt = document.createEvent("HTMLEvents")
                                evt.initEvent("loadeddata", False, True)
                                evt.data = responseText
                                evt.data_source = src
                                next_element.dispatchEvent(evt)
                            else:
                                next_element.innerHTML = responseText
                                on_change_element(next_element)

                        ajax_get(src, _onload)
                    else:
                        if (
                            hasattr(next_element, "onloadeddata")
                            and getattr(next_element, "onloadeddata")
                            and next_element.onloadeddata
                        ):
                            evt = document.createEvent("HTMLEvents")
                            evt.initEvent("loadeddata", False, True)
                            evt.data = ""
                            evt.data_source = src
                            next_element.dispatchEvent(evt)
                        else:
                            next_element.innerHTML = (
                                "<option disabled selected value></option>"
                            )
                            on_change_element(next_element)

    def on_change(event):
        element = event.target
        return on_change_element(element)

    for elem in select_ctrl_list:
        if elem.hasAttribute("data-rel-name"):
            elem.addEventListener("change", on_change)


register_mount_fun(select_combo_init)


def datatable_init(dest_elem):
    # datatable_onresize()
    table_type = get_table_type(jQuery(dest_elem))
    tbl = jQuery(dest_elem).find(".tabsort")
    if tbl.length > 0:
        init_table(tbl, table_type)
    if hasattr(jQuery.fn, "treegrid"):
        jQuery(dest_elem).find(".tree").treegrid()


register_mount_fun(datatable_init)
register_mount_fun(process_resize)


def _valid_region_element(element, class_name, region_name=None):
    if not region_name:
        return True
    if element.hasAttribute("data-region"):
        x = element.getAttribute("data-region")
        if region_name == x:
            return True
        if "(" + region_name + ")" in x:
            return True
        if "(" + class_name + ":" + region_name + ")" in x:
            return True
    return False


def _get_region_elements_inside(element, class_name, region_name=None):
    item_list = Array.prototype.slice.call(element.querySelectorAll("." + class_name))
    ret = []
    for item in item_list:
        if item.classList.contains(class_name):
            if _valid_region_element(item, class_name, region_name):
                ret.append(item)
        else:
            if not region_name:
                ret.append(item)
    return ret


def _get_region_element_closest(element, class_name, region_name=None):
    item = element.closest("." + class_name)
    if not region_name:
        return item
    while item:
        if _valid_region_element(item, class_name, region_name):
            return ret
        ret = ret.parentElement
        if ret != None:
            ret = ret.closest("." + class_name)
    return None


def get_ajax_region(element, region_name=None, strict_mode=False):
    if element.classList.contains("ajax-region") and _valid_region_element(
        element, "ajax-region", region_name
    ):
        return element
    else:
        if region_name:
            ret = element.closest(".ajax-region")
            while ret:
                if _valid_region_element(ret, "ajax-region", region_name):
                    return ret
                ret = ret.parentElement
                if ret != None:
                    ret = ret.closest(".ajax-region")
            if region_name and not strict_mode:
                return get_ajax_region(element, None)
            else:
                return None
        else:
            return element.closest(".ajax-region")


window.get_ajax_region = get_ajax_region


def get_ajax_link(element, region_name=None, strict_mode=False):
    if element.classList.contains("ajax-link") and _valid_region_element(
        element, "ajax-link", region_name
    ):
        return element
    region = get_ajax_region(element, region_name, strict_mode)
    if region != None:
        if region.classList.contains("ajax-link") and _valid_region_element(
            region, "ajax-link", region_name
        ):
            return region
        else:
            if region_name:
                link_list = _get_region_elements_inside(
                    region, "ajax-link", region_name
                )
                if len(link_list) == 1:
                    return link_list[0]
                for link in link_list:
                    if (
                        _get_region_element_closest(link, "ajax-region", region_name)
                        == region
                    ):
                        return link
                if len(link_list) > 0:
                    return link_list[0]
            else:
                return region.querySelector(".ajax-link")
    if region_name and not strict_mode:
        return get_ajax_link(element, None)
    else:
        return None


window.get_ajax_link = get_ajax_link


def get_ajax_frame(element, region_name=None, strict_mode=False):
    region = get_ajax_region(element, region_name, strict_mode)
    if region != None:
        if region.classList.contains("ajax-frame") and _valid_region_element(
            region, "ajax-frame", region_name
        ):
            return region
        else:
            if region_name:
                frame_list = _get_region_elements_inside(
                    region, "ajax-frame", region_name
                )
                if len(frame_list) == 1:
                    return frame_list[0]
                for f in frame_list:
                    if (
                        _get_region_element_closest(f, "ajax-region", region_name)
                        == region
                    ):
                        return f
                if len(frame_list) > 0:
                    return frame_list[0]
            else:
                return region.querySelector(".ajax-frame")
    if region_name and not strict_mode:
        return get_ajax_frame(element, None)
    else:
        return None


window.get_ajax_frame = get_ajax_frame


def _refresh_page(target_element, data_element):
    frame = target_element.closest("div.content")
    if frame and frame.firstElementChild:
        if isinstance(data_element, str):
            data_element2 = None
        else:
            data_element2 = data_element.querySelector("div.content")
        if data_element2:
            if data_element2.firstElementChild:
                data_element2 = data_element2.firstElementChild
        if not data_element2:
            data_element2 = data_element
        mount_html(frame, data_element2)


def refresh_ajax_frame(
    element,
    region_name=None,
    data_element=None,
    callback=None,
    callback_on_error=None,
    data_if_none=None,
):
    region = get_ajax_region(element, region_name)
    frame = get_ajax_frame(element, region_name)
    if frame == None:
        return
    link = get_ajax_link(element, region_name)
    url = None

    loading = Loading(element)

    def _callback(data):
        nonlocal element, link, frame, region, callback, loading, url
        ret = None

        loading.stop()
        loading.remove()

        dt = data_type(data)

        if dt != "$$RETURN_ERROR" and element and element.hasAttribute("rettype"):
            dt = "$$" + element.getAttribute("rettype")

        if (
            dt != "$$RETURN_ERROR"
            and getattr(frame, "onloadeddata")
            and frame.onloadeddata
        ):
            ret = mount_html(frame, data, link)
        else:
            if dt in ("$$RETURN_REFRESH",):
                return refresh_ajax_frame(
                    region, region_name, None, callback, callback_on_error
                )
            elif dt in ("$$RETURN_REFRESH_PARENT",):
                return refresh_ajax_frame(
                    region.parentElement, region_name, None, callback, callback_on_error
                )
            elif dt in ("$$RETURN_RELOAD_PAGE",):
                return _refresh_page(region, data)
            elif dt in (
                "$$RETURN_OK",
                "$$RETURN_NEW_ROW_OK",
                "$$RETURN_UPDATE_ROW_OK",
            ):
                # if url and "fragment=" in url:
                #   x = url.split("fragment=")[1].split("&")[0]
                #    if x:
                #       region_name = x
                plug = region.closest(".plug")
                if plug:
                    elem = region.closest(".plug").parentElement
                    # elem = get_ajax_frame(region.closest(".plug"), None)
                else:
                    elem = element
                if callback:
                    callback()
                return refresh_ajax_frame(elem, "", None, None, callback_on_error, data)
                # return refresh_ajax_frame(
                #    get_ajax_region(elem, "page").parentElement, "", None, None, callback_on_error, data
                # )
            elif dt == "$$RETURN_RELOAD":
                if region_name == "error":
                    ret = mount_html(frame, data, link)
                else:
                    return refresh_ajax_frame(
                        element, "error", data, callback, callback_on_error
                    )
            elif dt == "$$RETURN_CANCEL":
                pass
            elif dt == "$$RETURN_ERROR":
                if isinstance(data, str):
                    window.open().document.write(data)
                else:
                    window.open().document.write(data.innerHTML)
            elif dt == "$$RETURN_REFRESH_AUTO_FRAME":
                auto_frame_init(frame)
            elif dt == "$$RETURN_HTML_ERROR":
                if isinstance(data, str):
                    txt = data
                else:
                    txt = data.innerHTML
                options = {
                    "title": "Error!",
                    "html": txt,
                    "icon": "error",
                    "buttonsStyling": False,
                    "showCancelButton": False,
                    "customClass": {
                        "confirmButton": "btn btn-primary btn-lg",
                    },
                }
                Swal.fire(options)
            elif dt == "$$RETURN_JSON":
                frame = get_ajax_frame(region, "json")
                callback()
                if frame:
                    if (
                        hasattr(frame, "onloadeddata")
                        and getattr(frame, "onloadeddata")
                        and frame.onloadeddata
                    ):
                        evt = document.createEvent("HTMLEvents")
                        evt.initEvent("loadeddata", False, True)
                        evt.data = data
                        evt.data_source = link
                        frame.dispatchEvent(evt)
                        return
                return
            else:
                ret = mount_html(frame, data, link)

        if dt in ("$$RETURN_ERROR", "$$RETURN_RELOAD", "$$RETURN_HTML_ERROR"):
            if callback_on_error:
                callback_on_error()
        else:
            if callback:
                callback()

        return ret

    def _callback_on_error(req):
        loading.stop()
        loading.remove()
        window.standard_error_handler(req)

    if data_element:
        return _callback(data_element)

    post = False
    if link != None:
        if link.hasAttribute("href"):
            url = link.getAttribute("href")
        elif link.hasAttribute("action"):
            url = link.getAttribute("action")
            post = True
        elif link.hasAttribute("src"):
            url = link.getAttribute("src")

    if url:
        url = correct_href(url, (element, link))
        url = process_href(url, jQuery(link.parentElement))
        if "[[" in url and "]]" in url:
            _callback(data_if_none)
            return

        loading.create()
        loading.start()

        if post:
            if link.tagName.lower() == "form":
                ajax_submit(link, _callback, _callback_on_error, None, None, url)
            else:
                data = jQuery(link).serialize()
                ajax_post(url, data, _callback, _callback_on_error)
        else:
            ajax_get(url, _callback, _callback_on_error)
        return None
    else:
        return _callback(data_if_none)


window.refresh_ajax_frame = refresh_ajax_frame


def ajax_load(element, url, complete):
    def _onload(responseText):
        mount_html(element, responseText, None)
        complete(responseText)

    ajax_get(url, _onload)


window.ajax_load = ajax_load
