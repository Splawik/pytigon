# from pytigon_js.tabmenu import get_menu
# from pytigon_js.tools import Loading, is_visible, correct_href, ajax_get, get_template, super_insert, remove_element, process_resize, can_popup, get_elem_from_string
# from pytigon_js.ajax_region import get_ajax_region, refresh_ajax_frame, mount_html

EVENT_TAB = []
REGISTERED_EVENT_TYPES = []


def _chcek_element(element, selector):
    if not selector:
        return True
    if "." in selector:
        x = selector.split(".")
        tag = x[0]
        sel = x[1]
    else:
        if selector.startswith("#"):
            tag = None
            sel = selector
        else:
            tag = selector
            sel = None
    if tag:
        if not element.tagName.lower() == tag:
            return False
    if sel:
        if sel.startswith("#"):
            if element.id != sel[1:]:
                return False
        else:
            if not element.classList.contains(sel):
                return False
    return True


def _get_title(element, data_element, url):
    title = element.getAttribute("title")
    if data_element:
        title_element = data_element.querySelector("title")
        if title_element:
            title_alt = title_element.innerHTML.strip()
        else:
            title_alt = ""
    else:
        title_alt = ""
    if not title and not title_alt:
        url2 = url.split("?")[0]
        if len(url2) > 16:
            title = "..." + url2[-13:]
        else:
            title = url2
    else:
        if not title:
            title = title_alt
            title_alt = ""
    return title, title_alt


def on_global_event(self, event):
    global EVENT_TAB
    for pos in EVENT_TAB:
        if pos[0] == event.type:
            element = event.target
            while element:
                if _chcek_element(element, pos[2]):
                    return pos[1](event, element)
                element = element.parentElement
                if element and element.tagName.lower() == "body":
                    break


def register_global_event(event_type, fun, selector):
    if not event_type in REGISTERED_EVENT_TYPES:
        document.body.addEventListener(event_type, on_global_event)
        REGISTERED_EVENT_TYPES.append(event_type)
    EVENT_TAB.append((event_type, fun, selector))


window.register_global_event = register_global_event


def _get_value(elem, name):
    if elem.length > 0:
        x1 = elem.closest(".ajax-region")
        x2 = elem.closest(".page")
        x3 = jQuery(document)
        for x in (x1, x2, x3):
            if x.length > 0:
                xx = x.find(sprintf("[name='%s']", name))
                if xx.length > 0:
                    return xx.val()
    return "[[ERROR]]"


def process_href(href, elem):
    ret = []
    if "[[" in href and "]]" in href:
        x1 = href.split("[[")
        process = False
        for pos in x1:
            if process:
                if "]]" in pos:
                    x2 = pos.split("]]", 1)
                    value = _get_value(elem, x2[0])
                    if value and value != "None":
                        ret.append(value + x2[1])
                    else:
                        ret.append(x2[1])
                else:
                    ret.append(pos)
                process = False
            else:
                ret.append(pos)
                process = True
        return "".join(ret)
    else:
        return href


window.process_href = process_href


def _get_click_event_from_tab(target_element, target, href):
    global EVENT_CLICK_TAB
    for pos in EVENT_CLICK_TAB:
        if pos[0] == "*" or pos[0] == target:
            if pos[1] == "*" or target_element.classList.contains(pos[1]):
                url = correct_href(href, (target_element,))

                # if (
                #        target_element.hasAttribute("data-region")
                #        and target_element.getAttribute("data-region") == "table"
                # ):
                # if pos[3]:
                #    url = corect_href(href, True)
                # elif pos[2]:
                #    url = corect_href(href, False)
                # else:
                #    url = href
                return url, pos[4]
    return None, None


def on_click_default_action(event, target_element):
    global EVENT_CLICK_TAB

    target = target_element.getAttribute("target")

    # if window.APPLICATION_TEMPLATE == "traditional":
    #    if not target or (target and target in ("_self", "_parent", "_top")):
    #        return False

    src_obj = jQuery(target_element)

    href = target_element.getAttribute("xlink:href")
    if not href:
        href = target_element.getAttribute("href")
    if not href:
        href = target_element.getAttribute("action")
    if not href:
        href = target_element.getAttribute("src")

    if href and "#" in href:
        return True

    if src_obj.hasClass("editable"):
        return True

    if href:
        href = process_href(href, jQuery(target_element))

    if target_element.tagName.lower() == "form":

        if target_element.getAttribute("target") == "_blank":
            target_element.setAttribute("enctype", "multipart/form-data")
            target_element.setAttribute("encoding", "multipart/form-data")
            return True

        if target_element.getAttribute("target") == "_self":
            return True

        if target_element.querySelector("[type='file']"):
            param = "file"
        else:
            param = jQuery(target_element).serialize()

        if param and "pdf=on" in param:
            target_element.setAttribute("enctype", "multipart/form-data")
            target_element.setAttribute("encoding", "multipart/form-data")
            return True
        if target_element and "odf=on" in param:
            target_element.setAttribute("enctype", "multipart/form-data")
            target_element.setAttribute("encoding", "multipart/form-data")
            return True
    else:
        param = None
        if target == "_blank":
            # event.preventDefault()
            # window.open(href, target)
            return

    def _get_or_post(url, callback, data2=None):
        nonlocal target_element, target, param, event

        loading = Loading(target_element)
        loading.create()
        loading.start()

        def _callback(data):
            nonlocal target_element, target, param, event, url, callback, loading

            loading.stop()
            loading.remove()

            data_element = get_elem_from_string(data)
            new_target_elem = data_element.querySelector("meta[name='target']")
            if new_target_elem:
                new_target = new_target_elem.getAttribute("content")
            else:
                new_target = None
            if new_target and new_target != target:
                new_callback, new_url = _get_click_event_from_tab(
                    target_element, new_target, url
                )
                new_callback(target_element, data_element, new_url, param, event)
            else:
                callback(target_element, data_element, url, param, event)

        if url:
            if param:
                ajax_post(url, param, _callback)
            else:
                ajax_get(url, _callback)
        else:
            _callback(data2)

    url, callback = _get_click_event_from_tab(target_element, target, href)
    if callback:
        if param == "file":

            def _callback2(data2):
                _get_or_post(None, callback, data2)

            ajax_submit(target_element, _callback2, None, None)
        elif url:
            _get_or_post(url, callback, None)
        else:
            callback(target_element, None, None, None, event)
        event.preventDefault()
        return True


def _on_menu_click(event, target_element):
    # if window.APPLICATION_TEMPLATE != "traditional":
    event.preventDefault()
    toggler = document.querySelector("#topmenu .navbar-toggler")
    if toggler and is_visible(toggler):

        def _on_collapse(self):
            nonlocal target_element
            on_click_default_action(event, target_element)
            jQuery("#navbar-ex1-collapse").off("hidden.bs.collapse", _on_collapse)

        jQuery("#navbar-ex1-collapse").on("hidden.bs.collapse", _on_collapse)
        jQuery("#navbar-ex1-collapse").collapse("hide")
    else:
        on_click_default_action(event, target_element)


register_global_event("click", _on_menu_click, "a.menu-href")

register_global_event("click", on_click_default_action, "a")
register_global_event("click", on_click_default_action, "button")
register_global_event("submit", on_click_default_action, "form")


def _get_scrolled_parent(node):
    if node == None:
        return None
    if node.scrollHeight > node.clientHeight:
        return node
    else:
        return _get_scrolled_parent(node.parentNode)


def _on_inline(target_element, data_element, url, param, event, template_name):
    inline_position = target_element.getAttribute("data-inline-position")

    if inline_position and inline_position.split(":")[0].endswith("tr"):
        dialog_slot = document.createElement("tr")
        child = document.createElement("td")
        child.setAttribute("colspan", "100")
        dialog_slot.appendChild(child)
        dialog_slot2 = child
    else:
        dialog_slot = document.createElement("div")
        dialog_slot.classList.add("dialog-slot")
        dialog_slot.classList.add("col-12")
        dialog_slot2 = dialog_slot

    dialog_slot.classList.add("plug")

    dialog_slot2.innerHTML = get_template(
        template_name.replace("MODAL", "INLINE"),
        {"title": _get_title(target_element, data_element, url)[0], "href": url},
    )

    target_element.setAttribute("data-style", "zoom-out")
    target_element.setAttribute("data-spinner-color", "#FF0000")

    content = dialog_slot.querySelector("div.dialog-data")
    content.appendChild(data_element)

    super_insert(target_element, inline_position, dialog_slot)
    mount_html(dialog_slot, None)

    if data_element.classList.contains("maximized"):
        inline_maximize(data_element)

    def on_hidden(self, event):
        nonlocal target_element
        region = get_ajax_region(
            target_element, target_element.getAttribute("data-region")
        )
        if region:
            obj = region.querySelector(".plug")
            obj.remove()

    dialog = dialog_slot.firstElementChild

    if dialog != None:
        jQuery(dialog).on("click", "button.ptig-btn-close", on_hidden)

    plug = dialog.closest("aside.plug")
    if plug != None:
        viewportOffset = dialog.getBoundingClientRect()
        top = viewportOffset.top
        bottom = top + viewportOffset.height
        height = window.innerHeight
        if bottom > height:
            if height > viewportOffset.height:
                top2 = (height - viewportOffset.height) / 2
            else:
                top2 = 0
            dy = top - top2

            scroll_frame = plug.firstElementChild
            sy = scroll_frame.scrollTop
            scroll_frame.scrollTop = dy + sy
    else:
        plug = dialog.closest(".plug")
        if plug != None:
            scroll_frame = _get_scrolled_parent(plug)
            if scroll_frame != None:
                rect1 = dialog.getBoundingClientRect()
                rect2 = scroll_frame.getBoundingClientRect()
                sy = scroll_frame.scrollTop

                if rect1.top > rect2.top:
                    if rect1.height < rect2.height:
                        if rect1.top + rect1.height > rect2.top + rect2.height:
                            scroll_frame.scrollTop = int(sy) + (
                                rect1.top + rect1.height - (rect2.top + rect2.height)
                            )
                    else:
                        scroll_frame.scrollTop = int(sy) + (rect1.top - rect2.top)
                else:
                    scroll_frame.scrollTop = int(sy) + (rect1.top - rect2.top)
    if "INFO" in template_name:
        txt = dialog_slot.querySelector("textarea.copy_to_clipboard")
        btn = dialog_slot.querySelector("button.copy_to_clipboard")
        if btn:
            if txt and txt.value:
                btn.style.display = "block"

                def _on_click():
                    nonlocal txt
                    txt.select()
                    document.execCommand("copy")

                btn.addEventListener("click", _on_click)
            else:
                btn.style.display = "none"


def on_inline(target_element, data_element, new_url, param, event):
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE")


window.on_inline = on_inline


def on_inline_edit_new(target_element, data_element, new_url, param, event):
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_EDIT"
    )


window.on_inline_edit_new = on_inline_edit_new


def on_inline_info(target_element, data_element, new_url, param, event):
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_INFO"
    )


window.on_inline_inf = on_inline_info


def on_inline_delete(target_element, data_element, new_url, param, event):
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_DELETE"
    )


window.on_inline_delete = on_inline_delete


def on_inline_error(target_element, data_element, new_url, param, event):
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_ERROR"
    )


window.on_inline_error = on_inline_error


def _on_popup(target_element, data_element, url, param, event, template_name):
    if not can_popup():
        return _on_inline(
            target_element, data_element, url, param, event, template_name
        )
    dialog_slot = document.createElement("aside")
    dialog_slot.setAttribute("class", "plug")

    dialog_slot.innerHTML = get_template(
        template_name,
        {"title": _get_title(target_element, data_element, url)[0], "href": url},
    )

    region = get_ajax_region(target_element, target_element.getAttribute("data-region"))
    if not region:
        return

    region.appendChild(dialog_slot)

    target_element.setAttribute("data-style", "zoom-out")
    target_element.setAttribute("data-spinner-color", "#FF0000")

    content = dialog_slot.querySelector("div.dialog-data")

    mount_html(content, data_element)

    def on_hidden(self, event):
        nonlocal region
        obj = region.querySelector(".plug")
        if obj:
            obj.remove()

    if window.hasOwnProperty("bootstrap"):
        dialog_slot.firstElementChild.addEventListener("hidden.bs.modal", on_hidden)
        dialog = window.bootstrap.Modal(
            dialog_slot.firstElementChild, {"backdrop": False}
        )
        if dialog:
            dialog.show()
            jQuery(dialog_slot).drags({"handle": ".modal-header"})
    else:
        dialog = jQuery(dialog_slot.firstElementChild)
        if dialog:
            dialog.on("hidden.bs.modal", on_hidden)
            dialog.drags({"handle": ".modal-header"})
            dialog.modal(
                {
                    "show": True,
                    "backdrop": False,
                }
            )
    if "INFO" in template_name:
        txt = dialog_slot.querySelector("textarea.copy_to_clipboard")
        btn = dialog_slot.querySelector("button.copy_to_clipboard")
        if btn:
            if txt and txt.value:
                btn.style.display = "block"

                def _on_click():
                    nonlocal txt
                    txt.select()
                    document.execCommand("copy")

                btn.addEventListener("click", _on_click)
            else:
                btn.style.display = "none"


def on_popup(target_element, data_element, new_url, param, event):
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL")


window.on_popup = on_popup


def on_popup_edit_new(target_element, data_element, new_url, param, event):
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_EDIT")


window.on_popup_edit_new = on_popup_edit_new


def on_popup_info(target_element, data_element, new_url, param, event):
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_INFO")


window.on_popup_info = on_popup_info


def on_popup_delete(target_element, data_element, new_url, param, event):
    return _on_popup(
        target_element, data_element, new_url, param, event, "MODAL_DELETE"
    )


window.on_popup_delete = on_popup_delete


def on_popup_error(target_element, data_element, new_url, param, event):
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_ERROR")


window.on_popup_error = on_popup_error


def on_new_tab(target_element, data_element, new_url, param, event):
    title, title_alt = _get_title(target_element, data_element, new_url)
    data_element2 = data_element.querySelector("section.body-body")
    if not data_element2:
        data_element2 = data_element
    return get_menu().on_menu_href(
        target_element, data_element2, title, title_alt, new_url
    )


def on_replace_app(target_element, data_element, new_url, param, event):
    if window.PUSH_STATE:
        history_push_state("", window.BASE_PATH)
    else:
        window.location.pathname = window.BASE_PATH

    window.MENU = None
    wrapper = document.querySelector("div.content-wrapper")
    if wrapper:
        wrapper.innerHTML = ""
    mount_html(
        document.querySelector("div.content-wrapper"),
        data_element.querySelector("section.body-body"),
        False,
    )
    window.init_start_page()
    window.activate_menu()


def refresh_frame(
    target_element, data_element, new_url, param, event, data_region=None
):
    f = target_element.getAttribute("data-remote-elem")
    if f:
        data_element2 = data_element.querySelector(f)
    else:
        data_element2 = data_element

    if data_region:
        data_region2 = data_region
    else:
        data_region2 = target_element.getAttribute("data-region")
    # if not data_region2:
    #    data_region2 = data_region
    region = get_ajax_region(target_element, data_region2)
    if data_region2 != "error" and region.getAttribute("data-region") == "error":
        region = get_ajax_region(region.parentElement, data_region2)

    dialog = None
    aside = target_element.closest(".plug")
    if aside and region.contains(aside):
        dialog = aside.firstElementChild
    else:
        aside = None

    def _callback():
        nonlocal aside, dialog
        if aside:
            if dialog and dialog.classList.contains("modal"):
                jQuery(dialog).modal("hide")
            else:
                aside.remove()

    def _callback_on_error():
        nonlocal aside, dialog
        if aside:
            aside.style.opacity = "100%"

    if aside:
        aside.style.opacity = "50%"

    refresh_ajax_frame(
        target_element, data_region2, data_element2, _callback, _callback_on_error
    )


def refresh_page(target_element, data_element, new_url, param, event):
    return refresh_frame(target_element, data_element, new_url, param, event, "page")


# def refresh_page2(target_element, data_element, new_url, param, event):
#    frame = target_element.closest("div.content")
#    if frame and frame.firstElementChild:
#        if isinstance(data_element, str):
#            data_element2 = None
#        else:
#            data_element2 = data_element.querySelector("div.content")
#        if data_element2:
#            if data_element2.firstElementChild:
#                data_element2 = data_element2.firstElementChild
#        if not data_element2:
#            data_element2 = data_element
#        mount_html(frame, data_element2)


def refresh_app(target_element, data_element, new_url, param, event):
    window.location.href = window.BASE_PATH


def only_get(target_element, data_element, url, param, event):
    pass


def on_message(target_element, data_element, new_url, param, event):
    options = {
        "icon": "success",
        "title": "Information",
        "text": "success",
    }

    if target_element.hasAttribute("data-icon"):
        options["icon"] = target_element.getAttribute("data-icon")
    if target_element.hasAttribute("data-title"):
        options["title"] = target_element.getAttribute("data-title")
    if target_element.hasAttribute("data-text"):
        options["text"] = target_element.getAttribute("data-text")
    if target_element.hasAttribute("data-footer"):
        options["footer"] = target_element.getAttribute("data-footer")
    if target_element.hasAttribute("data-timer"):
        options["timer"] = target_element.getAttribute("data-timer")

    Swal.fire(options)


## target:
## _blank: new browser window (pdf) - default action
## _parent: new app tab
## _top: replace current app window
## _self: replace current frame
## popup: new popup window
## popup_edit: new popup window
## popup_info: new popup window
## popup_delete: new popup window
## inline_edit: new popup window
## inline_info: new popup window
## inline_delete: new popup window
## inline: new inline window
## none, get request (no gui)
## refresh_obj: replace current object
## refresh_page: reload current page (like _self)
## refresh_app: reload current app (like _top)

EVENT_CLICK_TAB = [
    # target, class, get only content, get only tab, function
    # ("*", "get_tbl_value", True, False, on_get_tbl_value),
    # ("*", "new_tbl_value", True, False, on_new_tbl_value),
    # ("*", "get_row", True, False, on_get_row),
    ("inline", "*", True, False, on_inline),
    ("inline_edit", "*", True, False, on_inline_edit_new),
    ("inline_info", "*", True, False, on_inline_info),
    ("inline_delete", "*", True, False, on_inline_delete),
    ("inline_error", "*", True, False, on_inline_error),
    ("popup", "*", True, False, on_popup),
    ("popup_edit", "*", True, False, on_popup_edit_new),
    ("popup_info", "*", True, False, on_popup_info),
    ("popup_delete", "*", True, False, on_popup_delete),
    ("popup_error", "*", True, False, on_popup_error),
    ("_top", "*", False, False, on_replace_app),
    ("_top2", "*", True, False, on_new_tab),
    ("_self", "*", True, False, refresh_page),
    ("_parent", "*", True, False, on_new_tab),
    ("refresh_frame", "*", True, False, refresh_frame),
    ("refresh_page", "*", True, False, refresh_page),
    ("refresh_app", "*", False, False, refresh_app),
    ("message", "*", False, False, on_message),
    ("null", "*", False, False, only_get),
]


def on_resize(self, event):
    process_resize(document.body)


window.addEventListener("resize", on_resize)
