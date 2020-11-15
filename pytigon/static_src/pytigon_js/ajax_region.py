from pytigon_js.tools import Loading, corect_href, ajax_get, ajax_post

MOUNT_INIT_FUN = []

def register_mount_fun(fun):
    global MOUNT_INIT_FUN
    MOUNT_INIT_FUN.append(fun)

def mount_html(dest_elem, data_or_html):
    global MOUNT_INIT_FUN

    def _on_remove(index, value):
        value.on_remove()

    jQuery.each(jQuery(dest_elem).find('.call_on_remove'), _on_remove)

    if type(data_or_html) == str:
        dest_elem.innerHTML = html_txt
    else:
        dest_elem.innerHTML = ""
        dest_elem.appendChild(data_or_html)

    if MOUNT_INIT_FUN:
        for fun in MOUNT_INIT_FUN:
            fun(dest_elem)

def get_ajax_region(element, region_name=None):
    if element.classList.contains("ajax-region") and ((not region_name) or element.getAttribute('data-region') == region_name):
        return element
    else:
        if region_name:
            ret = element.closest(".ajax-region")
            while ret:
                if ret.getAttribute('data-region')==region_name:
                    return ret
                ret = ret.closest('.ajax-region')
            if region_name:
                return get_ajax_region(element, None)
            else:
                return None
        else:
            return element.closest(".ajax-region")

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

def refresh_ajax_frame(element, region_name=None, data_element=None,  callback=None):
    frame = get_ajax_frame(element, region_name)
    if not frame:
        return
    link = get_ajax_link(element, region_name)

    loading = Loading(element)

    def _callback(data):
        nonlocal frame, callback, loading

        loading.stop()
        loading.remove()

        if getattr(frame,'onloadeddata') and frame.onloadeddata:
            evt = document.createEvent("HTMLEvents")
            evt.initEvent("loadeddata", False, True)
            evt.data = data
            frame.dispatchEvent(evt)
        else:
            mount_html(frame, data)
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
