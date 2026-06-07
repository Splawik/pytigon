"""
AJAX region management and HTML mounting module.

Provides the core DOM manipulation and AJAX content loading layer:
- data_type: Detects server response type markers for routing.
- mount_html: Renders HTML content into a target element with morph support.
- register_mount_fun: Plugin system for post-mount initialization hooks.
- Select2, SelectPicker, DataTable initialization hooks.
- AJAX region/link/frame element lookup helpers.
- refresh_ajax_frame: Core function for AJAX-based content updates.

Dependencies (pscript cross-module):
    pytigon_js.tools: Loading, correct_href, ajax_get, ajax_post,
                      get_table_type, super_insert
    pytigon_js.tbl: init_table
"""


# =============================================================================
# Server response type detection
# =============================================================================


def data_type(data_or_html):
    """Detect the server response type from markers in the response.

    Checks for special `$$RETURN_*` markers in string responses or
    `<meta name="RETURN" content="...">` tags in HTML responses.

    Args:
        data_or_html: String or DOM element containing server response.

    Returns:
        str: One of the `$$RETURN_*` constants, or `$$RETURN_HTML` if
             no special marker is found.
    """
    if data_or_html:
        if isinstance(data_or_html, str):
            # String response: check for embedded markers
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
            # HTML element: check for <meta> tags
            meta_list = Array.prototype.slice.call(
                data_or_html.querySelectorAll("meta")
            )
            for pos in meta_list:
                if pos.hasAttribute("name"):
                    if pos.getAttribute("name").upper() == "RETURN":
                        if pos.hasAttribute("content"):
                            return pos.getAttribute("content").upper()
    return "$$RETURN_HTML"


# =============================================================================
# Mount initialization plugin system
# =============================================================================

MOUNT_INIT_FUN = []


def register_mount_fun(fun):
    """Register a callback to run after every mount_html operation.

    The callback receives the destination element that was just mounted.

    Args:
        fun: Callback function(dest_elem) invoked after each mount.
    """
    global MOUNT_INIT_FUN
    MOUNT_INIT_FUN.append(fun)


window.register_mount_fun = register_mount_fun


# =============================================================================
# HTML mounting with Idiomorph support
# =============================================================================


def mount_html(dest_elem, data_or_html, link=None):
    """Mount HTML content into a destination element.

    This is the central DOM update function. It supports:
    - 'loadeddata' event delegation for elements with onloadeddata handlers.
    - 'data-link' attribute redirection (.. = replace parent).
    - Idiomorph-based DOM morphing for smooth transitions.
    - 'call_on_remove' cleanup callbacks.
    - 'ajax-temp-item' container unwrapping.
    - Post-mount initialization hooks (MOUNT_INIT_FUN).

    Args:
        dest_elem: Target DOM element to receive content.
        data_or_html: HTML string or DOM element to mount.
        link: Optional source element for data-source tracking.

    Returns:
        The destination element after mounting, or None if dest_elem is None.
    """
    global MOUNT_INIT_FUN

    replace = False

    if dest_elem == None:
        return None

    # If destination has a loadeddata handler, dispatch event instead
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

    # Handle data-link redirection
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
            """Invoke on_remove callback on elements marked for cleanup."""
            value.on_remove()

        jQuery.each(jQuery(dest_elem).find(".call_on_remove"), _on_remove)

        if dest_elem.children.length > 0:
            # Morph path: clone destination, inject content, then morph
            elem2 = dest_elem.cloneNode()
            if Object.prototype.toString.call(data_or_html) == "[object String]":
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
                    # Unwrap ajax-temp-item container
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
            # Empty destination: direct innerHTML or append
            if Object.prototype.toString.call(data_or_html) == "[object String]":
                dest_elem.innerHTML = data_or_html
                if replace:
                    if dest_elem.children.length > 0:
                        dest_elem.replaceWith(dest_elem.children[0])
            else:
                if (
                    data_or_html.tagName.lower() == "div"
                    and data_or_html.classList.contains("ajax-temp-item")
                ):
                    # Unwrap ajax-temp-item container
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

    # Run post-mount initialization hooks
    if MOUNT_INIT_FUN:
        for fun in MOUNT_INIT_FUN:
            fun(dest_elem)

    return dest_elem


window.mount_html = mount_html


# =============================================================================
# Mount initialization hooks
# =============================================================================
# These functions are registered via register_mount_fun and run after
# each mount_html operation to initialize UI components within the
# newly mounted content.


def selectpicker_init(dest_elem):
    """Initialize Bootstrap SelectPicker widgets in mounted content."""
    if hasattr(jQuery.fn, "selectpicker"):
        jQuery(dest_elem).find(".selectpicker").selectpicker()


register_mount_fun(selectpicker_init)


def auto_frame_init(dest_elem):
    """Auto-refresh all .auto-frame elements in mounted content."""
    frame_list = Array.prototype.slice.call(dest_elem.querySelectorAll(".auto-frame"))
    for elem in frame_list:
        refresh_ajax_frame(elem)


register_mount_fun(auto_frame_init)


def _on_shown_bs_tab(event):
    """Handle Bootstrap tab shown event for auto-refresh tabs.

    When a tab is shown, refreshes the associated frame or specific
    targets within it based on auto-refresh-target attribute.
    """
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
    """Bind auto-refresh behavior to tabs in .auto-refresh containers."""
    item_list = Array.prototype.slice.call(
        dest_elem.querySelectorAll("div.auto-refresh button")
    )
    for elem in item_list:
        elem.addEventListener("shown.bs.tab", _on_shown_bs_tab)


register_mount_fun(auto_refresh_tab)


def get_click_on_focus_fun(element):
    """Create a visibilitychange handler that clicks the element.

    Args:
        element: DOM element to click when page becomes visible.

    Returns:
        Callback for the visibilitychange event.
    """

    def _click(event):
        nonlocal element
        if not document.hidden:
            element.click()

    return _click


def get_refresh_on_focus_fun(element):
    """Create a visibilitychange handler that refreshes the element.

    Args:
        element: DOM element to refresh when page becomes visible.

    Returns:
        Callback for the visibilitychange event.
    """

    def _refresh(event):
        nonlocal element
        if not document.hidden:
            refresh_ajax_frame(element)

    return _refresh


def on_focus_action(dest_elem):
    """Bind visibilitychange-based actions to .on-focus-action elements.

    Supports two modes:
    - .on-focus-action-click: clicks the element when page becomes visible.
    - .on-focus-action-refresh: refreshes the element when page becomes visible.
    """
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
    """Process .move-element directives: move elements to target positions.

    Elements with class 'move-element' and 'data-position' attribute are
    moved to the specified DOM location via super_insert. Registers cleanup
    callbacks for proper element removal.
    """
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
                        """Remove classes from target when source is removed."""
                        nonlocal obj, elem2
                        for c in Array.prototype.slice.call(obj.classList):
                            elem2.classList.remove(c)

                else:

                    def _on_remove():
                        """Remove the original element when source is removed."""
                        nonlocal obj
                        obj.remove()

                parent.on_remove = _on_remove
                parent.classList.add("call_on_remove")


register_mount_fun(moveelement_init)


# =============================================================================
# Select2 widget initialization
# =============================================================================


def set_select2_value(sel2, id, text):
    """Set the value and display text of a Select2 widget.

    Args:
        sel2: jQuery Select2 element.
        id: Option value to select.
        text: Display text for the option.
    """
    sel2.append(jQuery("<option>", {"value": id, "text": text}))
    sel2.val(id.toString())
    sel2.trigger("change")


def create_onloadeddata(control):
    """Create a loadeddata event handler for a Select2 control.

    When the control receives a loadeddata event with data_source,
    extracts data-id and data-text attributes to set the Select2 value.

    Args:
        control: The Select2 DOM element.

    Returns:
        Event handler function for the 'loadeddata' event.
    """

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
    """Initialize a single Select2 control with existing data from parent.

    Looks for item_id/item_str attributes on the parent .input-group
    and sets the Select2 value accordingly.
    """
    sel2 = jQuery(self)
    src = sel2.closest(".input-group")
    if src.length == 1:
        if src[0].hasAttribute("item_id"):
            id = src.attr("item_id")
            if id:
                text = src.attr("item_str")
                set_select2_value(sel2, id, text)


def select2_init(dest_elem):
    """Initialize Django Select2 widgets in mounted content.

    Configures Select2 with proper dropdown parents (especially for modals)
    and wires up loadeddata handlers for dynamic value updates.
    """
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


# =============================================================================
# Select combo (cascading dropdown) initialization
# =============================================================================


def select_combo_init(dest_elem):
    """Initialize cascading select combos (.select_combo class).

    When a select with data-rel-name changes, finds the associated element
    by name and loads its options via AJAX from its src attribute.
    Supports loadeddata event delegation for custom handlers.
    """
    select_ctrl_list = Array.prototype.slice.call(
        dest_elem.querySelectorAll(".select_combo")
    )

    def on_change_element(element):
        """Handle cascading update for a changed select element."""
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


# =============================================================================
# DataTable initialization
# =============================================================================


def datatable_init(dest_elem):
    """Initialize DataTables and treegrid widgets in mounted content.

    Detects the table type and initializes Bootstrap Table and treegrid
    components as appropriate.
    """
    table_type = get_table_type(jQuery(dest_elem))
    tbl = jQuery(dest_elem).find(".tabsort")
    if tbl.length > 0:
        init_table(tbl, table_type)
    if hasattr(jQuery.fn, "treegrid"):
        jQuery(dest_elem).find(".tree").treegrid()


register_mount_fun(datatable_init)
register_mount_fun(process_resize)


# =============================================================================
# AJAX region/link/frame element lookup helpers
# =============================================================================
# These functions traverse the DOM to find elements marked with
# .ajax-region, .ajax-link, and .ajax-frame CSS classes, respecting
# data-region naming scopes.


def _valid_region_element(element, class_name, region_name=None):
    """Check if an element belongs to the specified region scope.

    An element is valid if it has no region_name requirement, or if its
    data-region attribute contains the region_name (possibly with a
    parenthesized scope qualifier).

    Args:
        element: DOM element to check.
        class_name: The CSS class type ('ajax-region', 'ajax-link', etc.).
        region_name: Optional region name to match.

    Returns:
        bool: True if the element is valid for the given region.
    """
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
    """Find all elements with a given class inside a container.

    Args:
        element: Container DOM element.
        class_name: CSS class to query (e.g. 'ajax-link').
        region_name: Optional region scope filter.

    Returns:
        list: Matching DOM elements.
    """
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
    """Find the closest ancestor matching class_name and optional region.

    Args:
        element: Starting DOM element.
        class_name: CSS class to match.
        region_name: Optional region scope filter.

    Returns:
        Matching ancestor element or None.
    """
    item = element.closest("." + class_name)
    if not region_name:
        return item
    while item:
        if _valid_region_element(item, class_name, region_name):
            return item
        item = item.parentElement
        if item != None:
            item = item.closest("." + class_name)
    return None


def get_ajax_region(element, region_name=None, strict_mode=False):
    """Find the nearest .ajax-region ancestor matching the region name.

    Args:
        element: Starting DOM element.
        region_name: Optional region name to match (from data-region attr).
        strict_mode: If True, returns None instead of falling back to
            the closest region without name matching.

    Returns:
        The matching .ajax-region element or None.
    """
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
    """Find the .ajax-link element for a given region scope.

    Searches for elements that provide the URL for AJAX operations within
    a region. Priority: direct class match > single child > closest child.

    Args:
        element: Starting DOM element.
        region_name: Optional region name scope.
        strict_mode: If True, don't fall back to un-scoped lookup.

    Returns:
        The matching .ajax-link element or None.
    """
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
    """Find the .ajax-frame element for a given region scope.

    Similar to get_ajax_link but for frame elements (content containers).

    Args:
        element: Starting DOM element.
        region_name: Optional region name scope.
        strict_mode: If True, don't fall back to un-scoped lookup.

    Returns:
        The matching .ajax-frame element or None.
    """
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


# =============================================================================
# Page-level refresh
# =============================================================================


def _refresh_page(target_element, data_element):
    """Refresh the content of a full page section.

    Replaces the content inside div.content with new data.

    Args:
        target_element: Element within the page to refresh.
        data_element: New content (string or DOM element).
    """
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


# =============================================================================
# Core AJAX frame refresh
# =============================================================================


def refresh_ajax_frame(
    element,
    region_name=None,
    data_element=None,
    callback=None,
    callback_on_error=None,
    data_if_none=None,
):
    """Refresh an AJAX frame with content from the server or provided data.

    This is the central function for AJAX-based content updates. It:
    1. Locates the region, frame, and link elements.
    2. If data_element is provided, uses it directly.
    3. Otherwise, fetches the URL from the link element via GET or POST.
    4. Processes the response based on its data_type marker.
    5. Handles special markers: REFRESH, RELOAD, CANCEL, ERROR, JSON, etc.

    Args:
        element: Starting element for region/link/frame lookup.
        region_name: Optional region scope name.
        data_element: Pre-fetched content to mount (skips AJAX if provided).
        callback: Success callback invoked after content is mounted.
        callback_on_error: Error callback for failed requests.
        data_if_none: Content to use if the URL contains unresolved [[placeholders]].

    Returns:
        The result of mount_html, or None.
    """
    region = get_ajax_region(element, region_name)
    frame = get_ajax_frame(element, region_name)
    if frame == None:
        return
    link = get_ajax_link(element, region_name)
    url = None

    loading = Loading(element)

    def _callback(data):
        """Process the AJAX response and route based on data_type."""
        nonlocal element, link, frame, region, callback, loading, url
        ret = None

        loading.stop()
        loading.remove()

        dt = data_type(data)

        # Override data_type from element's rettype attribute
        if dt != "$$RETURN_ERROR" and element and element.hasAttribute("rettype"):
            dt = "$$" + element.getAttribute("rettype")

        # If frame has loadeddata handler and not an error, delegate to mount
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
                # After successful action, refresh the parent frame
                plug = region.closest(".plug")
                if plug:
                    elem = region.closest(".plug").parentElement
                else:
                    elem = element
                if callback:
                    callback()
                return refresh_ajax_frame(elem, "", None, None, callback_on_error, data)
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

        # Invoke appropriate callback
        if dt in ("$$RETURN_ERROR", "$$RETURN_RELOAD", "$$RETURN_HTML_ERROR"):
            if callback_on_error:
                callback_on_error()
        else:
            if callback:
                callback()

        return ret

    def _callback_on_error(req):
        """Handle AJAX request failure."""
        loading.stop()
        loading.remove()
        window.standard_error_handler(req)

    # Use provided data_element if available (skip AJAX fetch)
    if data_element:
        return _callback(data_element)

    # Determine URL from the link element
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
        # If URL still has unresolved placeholders, use data_if_none
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


# =============================================================================
# Convenience: AJAX load into element
# =============================================================================


def ajax_load(element, url, complete):
    """Load content from a URL and mount it into the specified element.

    Simple wrapper around ajax_get + mount_html.

    Args:
        element: Target DOM element for the loaded content.
        url: URL to fetch content from.
        complete: Callback invoked with the response text after mounting.
    """

    def _onload(responseText):
        mount_html(element, responseText, None)
        complete(responseText)

    ajax_get(url, _onload)


window.ajax_load = ajax_load
