from pytigon_js.tools import Loading, corect_href, ajax_get, ajax_post, get_table_type, super_insert
from pytigon_js.tbl import init_table


MOUNT_INIT_FUN = []

def register_mount_fun(fun):
    global MOUNT_INIT_FUN
    MOUNT_INIT_FUN.append(fun)

window.register_mount_fun = register_mount_fun

def mount_html(dest_elem, data_or_html, link=None):
    global MOUNT_INIT_FUN

    if getattr(dest_elem, 'onloadeddata') and dest_elem.onloadeddata:
        evt = document.createEvent("HTMLEvents")
        evt.initEvent("loadeddata", False, True)
        evt.data = data_or_html
        evt.data_source = link
        dest_elem.dispatchEvent(evt)
        return

    if data_or_html != None:
        def _on_remove(index, value):
            value.on_remove()

        jQuery.each(jQuery(dest_elem).find('.call_on_remove'), _on_remove)

        if type(data_or_html) == str:
            dest_elem.innerHTML = data_or_html
        else:
            dest_elem.innerHTML = ""
            dest_elem.appendChild(data_or_html)

    if MOUNT_INIT_FUN:
        for fun in MOUNT_INIT_FUN:
            fun(dest_elem)

window.mount_html = mount_html

def datetime_init(dest_elem):
    format = {
        "singleDatePicker": True,
        "showDropdowns": True,
        "buttonClasses": "btn",
        "applyClass": "btn-success align-top",
        "cancelClass": "btn-danger btn-sm align-top",
        "timePicker24Hour": True,
        "autoApply": True,
        "locale": {
            "format": "YYYY-MM-DD",
            "separator": "-",
            "applyLabel": "&nbsp; OK &nbsp;",
            "cancelLabel": "<i class='fa fa-close'></i>",
        },
    }

    d = jQuery(dest_elem).find("div.form-group .datefield input")
    d.daterangepicker(format)

    format["locale"]["format"] = "YYYY-MM-DD HH:mm"
    format["timePicker"] = True
    format["timePickerIncrement"] = 30

    d = jQuery(dest_elem).find("div.form-group .datetimefield input")
    d.daterangepicker(format)

register_mount_fun(datetime_init)


def selectpicker_init(dest_elem):
    jQuery(dest_elem).find(".selectpicker").selectpicker()

register_mount_fun(selectpicker_init)

def moveelement_init(dest_elem):
    objs = dest_elem.querySelectorAll('.move-element')
    if objs:
        for obj in objs:
            if obj.hasAttribute('data-position'):
                obj.classList.remove("move-element")
                data_position = obj.getAttribute('data-position')

                parent = obj.parentElement
                elem2 = super_insert(dest_elem,  obj.getAttribute('data-position'), obj)

                if data_position.endswith(':class'):
                    def _on_remove():
                        nonlocal obj, elem2
                        for c in obj.classList:
                            elem2.classList.remove(c)
                else:
                    def _on_remove():
                        nonlocal obj
                        obj.remove()
                parent.on_remove = _on_remove
                parent.classList.add("call_on_remove")

register_mount_fun(moveelement_init)

def label_floating_init(dest_elem):
    def _on_blur(e):
        if e["type"] == "focus" or this.value.length > 0:
            test = True
        else:
            test = False
        jQuery(this).parents(".form-group").toggleClass("focused", test)

    jQuery(dest_elem).find(".label-floating .form-control").on("focus blur", _on_blur).trigger(
        "blur"
    )

register_mount_fun(label_floating_init)

def select2_init(dest_elem):
    jQuery(dest_elem).find(".django-select2:not(.select2-full-width)").djangoSelect2(
        {"width": "calc(100% - 48px)", "minimumInputLength": 1}
    )
    jQuery(dest_elem).find(".django-select2.select2-full-width").djangoSelect2(
        {"width": "calc(100%)", "minimumInputLength": 1}
    )

    def set_select2_value(sel2, id, text):
        sel2.append(jQuery("<option>", {"value": id, "text": text}))
        sel2.val(id.toString())
        sel2.trigger("change")

    controls = dest_elem.querySelectorAll(".django-select2")
    if controls:
        for control in controls:
            def _onloadeddata(event):
                nonlocal control
                if hasattr(event, 'data_source'):
                    src_elem = event.data_source
                    if src_elem:
                        id = src_elem.getAttribute('data-id')
                        text = src_elem.getAttribute('data-text')
                        set_select2_value(jQuery(control), id, text)
            control.onloadeddata = _onloadeddata
            control.classList.add('ajax-frame')
            control.setAttribute('data-region', "get_row")

    def init_select2_ctrl():
        sel2 = jQuery(this)
        src = sel2.closest(".input-group")
        if src.length == 1:
            if src[0].hasAttribute("item_id"):
                id = src.attr("item_id")
                if id:
                    text = src.attr("item_str")
                    set_select2_value(sel2, id, text)
                    #sel2.append(jQuery("<option>", {"value": id, "text": text}))
                    #sel2.val(id.toString())
                    #sel2.trigger("change")

    jQuery(dest_elem).find(".django-select2").each(init_select2_ctrl)

register_mount_fun(select2_init)


def datatable_init(dest_elem):
    #datatable_onresize()
    table_type = get_table_type(jQuery(dest_elem))
    tbl = jQuery(dest_elem).find(".tabsort")
    if tbl.length > 0:
        init_table(tbl, table_type)
    jQuery(dest_elem).find(".tree").treegrid()

register_mount_fun(datatable_init)
register_mount_fun(process_resize)

def get_ajax_region(element, region_name=None):
    if element.classList.contains("ajax-region") and ((not region_name) or element.getAttribute('data-region') == region_name):
        return element
    else:
        if region_name:
            ret = element.closest(".ajax-region")
            while ret:
                if ret.getAttribute('data-region')==region_name:
                    return ret
                ret = ret.parentElement
                if ret:
                    ret = ret.closest('.ajax-region')
            if region_name:
                return get_ajax_region(element, None)
            else:
                return None
        else:
            return element.closest(".ajax-region")

window.get_ajax_region = get_ajax_region

def get_ajax_link(element, region_name=None):
    if element.classList.contains("ajax-link") and ((not region_name) or element.getAttribute('data-region') == region_name):
        return element
    region = get_ajax_region(element, region_name)
    if region:
        if region.classList.contains("ajax-link") :
            return region
        else:
            if region_name:
                link =  region.querySelector(".ajax-link[data-region='"+region_name+"']")
                if link:
                    return link
            else:
                return region.querySelector(".ajax-link")
    if region_name:
        return get_ajax_link(element, None)
    else:
        return None

window.get_ajax_link = get_ajax_link

def get_ajax_frame(element, region_name=None):
    region = get_ajax_region(element, region_name)
    if region:
        if region.classList.contains("ajax-frame") and ((not region_name) or region.getAttribute('data-region') == region_name):
            return region
        else:
            if region_name:
                frame = region.querySelector(".ajax-frame[data-region='"+region_name+"']")
                if frame:
                    return frame
            else:
                return region.querySelector(".ajax-frame")
    if region_name:
        return get_ajax_frame(element, None)
    else:
        return None

window.get_ajax_frame = get_ajax_frame

def refresh_ajax_frame(element, region_name=None, data_element=None,  callback=None):
    frame = get_ajax_frame(element, region_name)
    if not frame:
        return
    link = get_ajax_link(element, region_name)

    loading = Loading(element)

    def _callback(data):
        nonlocal link, frame, callback, loading

        loading.stop()
        loading.remove()

        #if getattr(frame,'onloadeddata') and frame.onloadeddata:
        #    evt = document.createEvent("HTMLEvents")
        #    evt.initEvent("loadeddata", False, True)
        #    evt.data = data
        #    evt.data_source = link
        #    frame.dispatchEvent(evt)
        #else:
        mount_html(frame, data, link)
        callback()

    if data_element:
        _callback(data_element)
        return

    url = None
    post = False
    if link.hasAttribute('href'):
        url = link.getAttribute('href')
    elif link.hasAttribute('action'):
        url = link.getAttribute('action')
        post = True
    elif link.hasAttribute('src'):
        url = link.getAttribute('src')

    if url:
        loading.create()
        loading.start()

        if post:
            data = jQuery(link).serialize()
            ajax_post(url, data, _callback)
        else:
            ajax_get(url, _callback)
    else:
        _callback(None)

window.refresh_ajax_frame = refresh_ajax_frame

def ajax_load(element, url, complete):
    def _onload(responseText):
        mount_html(element, responseText, None)
        complete(responseText)

    ajax_get(url, _onload)

window.ajax_load = ajax_load
