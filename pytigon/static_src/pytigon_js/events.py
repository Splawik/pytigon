"""
Event handling and navigation target routing module.

This is the core event system that handles:
- Global event delegation (click, submit, keypress) with selector matching.
- URL processing with template placeholder substitution ([[variable]]).
- Navigation target dispatching: inline, popup, tab, subpage, subframe, etc.
- Dialog creation and lifecycle management (modal/inline).
- History-based close/back navigation for subpages and subframes.

The EVENT_CLICK_TAB table maps target names to handler functions:
    Target types: inline, inline_edit, inline_info, inline_delete,
    popup, popup_edit, popup_info, popup_delete, popup_error,
    _top, _self, _parent, page, subpage, subframe,
    refresh_frame, close_frame, refresh_page, refresh_app, message, null

Dependencies (pscript cross-module):
    pytigon_js.tabmenu: get_menu
    pytigon_js.tools: Loading, is_visible, correct_href, ajax_get,
                      get_template, super_insert, remove_element,
                      process_resize, can_popup, get_elem_from_string
    pytigon_js.ajax_region: get_ajax_region, refresh_ajax_frame, mount_html
"""

# =============================================================================
# Global event delegation system
# =============================================================================

EVENT_TAB = []
REGISTERED_EVENT_TYPES = []


def _check_element(element, selector):
    """Check if an element matches a CSS-like selector.

    Supports tag.class, #id, and plain tag selectors.

    Args:
        element: DOM element to test.
        selector: Selector string (e.g. 'a.menu-href', '#myid', 'button').

    Returns:
        bool: True if the element matches the selector.
    """
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
    """Extract a title from element attributes or response data.

    Priority: element's title attribute > data's <title> tag > truncated URL.

    Args:
        element: Source DOM element.
        data_element: Response data element (may contain <title>).
        url: Fallback URL for generating title.

    Returns:
        tuple: (title, title_alt) where title_alt is the alternate title
               from the data element (empty string if none).
    """
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
    """Global event dispatcher - routes events to registered handlers.

    Walks up the DOM tree from the event target, checking each element
    against registered selectors. Stops at the body element.

    Args:
        self: The event target element.
        event: The DOM event object.
    """
    global EVENT_TAB
    for pos in EVENT_TAB:
        if pos[0] == event.type:
            element = event.target
            while element:
                if _check_element(element, pos[2]):
                    return pos[1](event, element)
                element = element.parentElement
                if element and element.tagName.lower() == "body":
                    break


def register_global_event(event_type, fun, selector):
    """Register a global event handler with optional CSS selector filter.

    On first registration for an event type, adds a single event listener
    to document.body that dispatches to all registered handlers.

    Args:
        event_type: DOM event name (e.g. 'click', 'submit', 'keypress').
        fun: Handler function(event, element).
        selector: CSS-like selector to filter target elements, or None.
    """
    if not event_type in REGISTERED_EVENT_TYPES:
        document.body.addEventListener(event_type, on_global_event)
        REGISTERED_EVENT_TYPES.append(event_type)
    EVENT_TAB.append((event_type, fun, selector))


window.register_global_event = register_global_event


# =============================================================================
# URL template processing
# =============================================================================


def _get_value(elem, name):
    """Resolve a template variable to its value.

    Variables starting with '$' reference window properties.
    Other variables are looked up in form inputs within the current
    region, page, or document scope.

    Args:
        elem: jQuery element providing context for the lookup.
        name: Variable name (with optional '$' prefix for window scope).

    Returns:
        The resolved value, or '[[ERROR]]' if not found.
    """
    if name.startswith("$"):
        name = name[1:]
        if hasattr(window, name):
            return getattr(window, name)
    elif elem.length > 0:
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
    """Replace [[variable]] placeholders in a URL with actual values.

    Placeholders are resolved via _get_value. If a value is None,
    the placeholder is replaced with an empty string.

    Args:
        href: URL string possibly containing [[...]] placeholders.
        elem: jQuery element providing context for value resolution.

    Returns:
        str: The processed URL with placeholders replaced.
    """
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


# =============================================================================
# Click event routing
# =============================================================================


def _get_click_event_from_tab(target_element, target, href):
    """Look up the handler for a given target type in EVENT_CLICK_TAB.

    Args:
        target_element: The clicked DOM element.
        target: Target name (e.g. 'inline', 'popup', '_top').
        href: The URL being navigated to.

    Returns:
        tuple: (url, callback) or (None, None) if no match found.
    """
    global EVENT_CLICK_TAB
    for pos in EVENT_CLICK_TAB:
        if pos[0] == "*" or pos[0] == target:
            if pos[1] == "*" or target_element.classList.contains(pos[1]):
                url = correct_href(href, (target_element,))
                return url, pos[4]
    return None, None


def on_click_default_action(event, target_element):
    """Handle click/submit events and route to the appropriate action.

    This is the main event handler for navigation. It:
    1. Resolves data-link indirection.
    2. Extracts href/action/src from the target element.
    3. Determines the target type and finds the matching handler.
    4. For forms: detects file uploads, PDF/ODF generation.
    5. Executes GET/POST AJAX requests with loading indicators.
    6. Routes responses through the target handler callbacks.

    Args:
        event: The DOM event object.
        target_element: The clicked/submitted element.

    Returns:
        True if the event was handled (prevent default navigation),
        None for _blank target (allow default).
    """
    global EVENT_CLICK_TAB

    # Handle data-link indirection: redirect the click to another element
    if target_element.hasAttribute("data-link"):
        obj = super_query_selector(
            target_element, target_element.getAttribute("data-link")
        )
        if obj:
            # Merge URLs from the source and target elements
            tmp_url1 = window.element_get_url(obj)
            tmp_url2 = window.element_get_url(target_element)
            if tmp_url1 != None and tmp_url2:
                element_set_url(obj, join_urls(tmp_url1, tmp_url2))
            setattr(obj, "data", target_element)
            ret = on_click_default_action(event, obj)
            setattr(obj, "data", None)
            return ret

    target = target_element.getAttribute("target")

    src_obj = jQuery(target_element)

    # Extract URL from various possible attributes
    href = target_element.getAttribute("xlink:href")
    if not href:
        href = target_element.getAttribute("href")
    if not href:
        href = target_element.getAttribute("action")
    if not href:
        href = target_element.getAttribute("src")

    # Hash-only links are handled by the browser
    if href and "#" in href:
        return True

    # Editable elements handle their own clicks
    if src_obj.hasClass("editable"):
        return True

    if href:
        href = process_href(href, jQuery(target_element))

    # Form handling: detect file uploads, PDF/ODF generation
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
            # Let the browser handle _blank links normally
            return

    def _get_or_post(url, callback, data2=None):
        """Execute the AJAX request and route the response."""
        nonlocal target_element, target, param, event

        req = None

        loading = Loading(target_element)
        loading.create()
        loading.start()

        def _callback(data):
            """Process the AJAX response and dispatch to the handler."""
            nonlocal target_element, target, param, event, url, callback, loading, req

            element = None

            loading.stop()
            loading.remove()

            # Check for meta redirect in the response
            data_element = get_elem_from_string(data)
            if (
                data_element.nodeName == "META"
                and data_element.hasAttribute("name")
                and data_element.getAttribute("name") == "target"
            ):
                new_target_elem = data_element
            else:
                new_target_elem = data_element.querySelector("meta[name='target']")
            if new_target_elem:
                new_target = new_target_elem.getAttribute("content")
            else:
                new_target = None
            if new_target and new_target != target:
                new_url, new_callback = _get_click_event_from_tab(
                    target_element, new_target, url
                )
                element = new_callback(
                    target_element, data_element, new_url, param, event
                )
            else:
                element = callback(target_element, data_element, url, param, event)
            return element

        def _callback_on_error(req):
            """Handle AJAX errors."""
            nonlocal loading
            loading.stop()
            loading.remove()
            window.standard_error_handler(req)

        if url:
            if param:
                req = ajax_post(url, param, _callback, _callback_on_error)
            else:
                req = ajax_get(url, _callback, _callback_on_error)
        else:
            _callback(data2)

    # Find the matching handler for this target
    url, callback = _get_click_event_from_tab(target_element, target, href)
    if callback:
        if param == "file":

            def _callback2(data2):
                _get_or_post(None, callback, data2)

            ajax_submit(target_element, _callback2, None, None, None)
        elif url:
            _get_or_post(url, callback, None)
        else:
            callback(target_element, None, None, None, event)
        event.preventDefault()
        return True


def _on_menu_click(event, target_element):
    """Handle menu link clicks with mobile collapse support.

    If the navbar toggler is visible (mobile view), collapses the menu
    first and then processes the click after the collapse animation.
    """
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


# Register global event handlers
register_global_event("click", _on_menu_click, "a.menu-href")

register_global_event("click", on_click_default_action, "a")
register_global_event("click", on_click_default_action, "button")
register_global_event("submit", on_click_default_action, "form")


def create_event_handler(href, target="inline_info", position="div.page.active"):
    """Create a synthetic click event handler for programmatic navigation.

    Creates a temporary <a> element, attaches it to the DOM, simulates
    a click, and returns a handler function.

    Args:
        href: URL to navigate to.
        target: Target type (default 'inline_info').
        position: CSS selector for where to attach the temporary element.

    Returns:
        A handler function that triggers the navigation when called.
    """

    def _handler(event):
        nonlocal href, target, position
        a = document.createElement("a")
        a.setAttribute("href", href)
        a.setAttribute("target", target)
        document.querySelector(position).appendChild(a)
        on_click_default_action(event.originalEvent, a)
        return False

    return _handler


window.create_event_handler = create_event_handler


# =============================================================================
# Scroll utilities
# =============================================================================


def _get_scrolled_parent(node):
    """Find the nearest scrollable ancestor of a node.

    Args:
        node: Starting DOM node.

    Returns:
        The first ancestor with scrollHeight > clientHeight, or None.
    """
    if node == None:
        return None
    if node.scrollHeight > node.clientHeight:
        return node
    else:
        return _get_scrolled_parent(node.parentNode)


# =============================================================================
# Inline dialog creation
# =============================================================================


def _on_inline(target_element, data_element, url, param, event, template_name):
    """Create an inline (non-modal) dialog within the page flow.

    Inline dialogs are embedded in the page rather than floating as modals.
    They can be positioned after a table row (tr), in a div slot, or within
    a plug container.

    Features:
    - Auto-scrolling to keep the dialog visible.
    - Copy-to-clipboard support for INFO dialogs.
    - Maximize/minimize via CSS classes.
    - After-close refresh callbacks.

    Args:
        target_element: The element that triggered the dialog.
        data_element: The content to display.
        url: Source URL (may contain after_close= parameter).
        param: Request parameters.
        event: The triggering DOM event.
        template_name: Template key (INLINE, INLINE_EDIT, INLINE_INFO, ...).

    Returns:
        The created dialog slot DOM element.
    """
    inline_position = target_element.getAttribute("data-inline-position")

    # Create dialog slot based on positioning type
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

    # Render the inline template with title and href
    dialog_slot2.innerHTML = get_template(
        template_name.replace("MODAL", "INLINE"),
        {"title": _get_title(target_element, data_element, url)[0], "href": url},
    )

    # Apply visual effects to the trigger element
    target_element.setAttribute("data-style", "zoom-out")
    target_element.setAttribute("data-spinner-color", "#FF0000")

    content = dialog_slot.querySelector("div.dialog-data")

    # Handle ajax-temp-item container unwrapping
    if data_element.tagName.lower() == "div" and data_element.classList.contains(
        "ajax-temp-item"
    ):
        for item in Array.prototype.slice.call(data_element.childNodes):
            content.appendChild(item)
    else:
        content.appendChild(data_element)

    super_insert(target_element, inline_position, dialog_slot)
    mount_html(dialog_slot, None)

    # Apply maximize state if data indicates it
    if data_element.classList.contains("maximized"):
        inline_maximize(data_element)

    def on_hidden(self, event):
        """Clean up the dialog when closed."""
        nonlocal target_element, url
        region = get_ajax_region(
            target_element, target_element.getAttribute("data-region")
        )
        if region:
            obj = region.querySelector(".plug")
            obj.remove()

            # Handle after_close=refresh in URL
            if "after_close=" in url:
                x = url.split("after_close=")[1]
                if x.startswith("refresh"):
                    window.refresh_ajax_frame(region)

        return False

    dialog = dialog_slot.firstElementChild

    if dialog != None:
        jQuery(dialog).on("click", "button.ptig-btn-close", on_hidden)

    # Adjust scroll position to keep dialog visible
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

    # Copy-to-clipboard functionality for INFO dialogs
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
    return dialog_slot


window._on_inline = _on_inline


def on_inline(target_element, data_element, new_url, param, event):
    """Create an inline dialog with INLINE template."""
    return _on_inline(target_element, data_element, new_url, param, event, "INLINE")


window.on_inline = on_inline


def on_inline_edit_new(target_element, data_element, new_url, param, event):
    """Create an inline edit dialog."""
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_EDIT"
    )


window.on_inline_edit_new = on_inline_edit_new


def on_inline_info(target_element, data_element, new_url, param, event):
    """Create an inline info dialog with copy-to-clipboard."""
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_INFO"
    )


window.on_inline_info = on_inline_info

# Backward-compatible alias (historical typo preserved)
window.on_inline_inf = on_inline_info


def on_inline_delete(target_element, data_element, new_url, param, event):
    """Create an inline delete confirmation dialog."""
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_DELETE"
    )


window.on_inline_delete = on_inline_delete


def on_inline_error(target_element, data_element, new_url, param, event):
    """Create an inline error dialog."""
    return _on_inline(
        target_element, data_element, new_url, param, event, "INLINE_ERROR"
    )


window.on_inline_error = on_inline_error


# =============================================================================
# Popup (modal) dialog creation
# =============================================================================


def _on_popup(target_element, data_element, url, param, event, template_name):
    """Create a Bootstrap modal popup dialog.

    Falls back to inline mode if a modal is already open (to avoid
    stacking modals).

    Features:
    - Bootstrap 5 Modal with backdrop support.
    - Draggable via jQuery drags plugin.
    - Copy-to-clipboard for INFO dialogs.
    - After-close refresh callbacks.

    Args:
        target_element: The element that triggered the popup.
        data_element: The content to display.
        url: Source URL (may contain after_close= parameter).
        param: Request parameters.
        event: The triggering DOM event.
        template_name: Template key (MODAL, MODAL_EDIT, MODAL_INFO, ...).

    Returns:
        The created dialog content element.
    """
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
        """Clean up the popup when hidden."""
        nonlocal region, url
        obj = region.querySelector(".plug")
        if obj:
            obj.remove()

        if "after_close=" in url:
            x = url.split("after_close=")[1]
            if x.startswith("refresh"):
                window.refresh_ajax_frame(region)

        return False

    # Initialize Bootstrap modal (v5 or legacy)
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

    # Copy-to-clipboard for INFO dialogs
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
    return content


window._on_popup = _on_popup


def on_popup(target_element, data_element, new_url, param, event):
    """Create a modal popup dialog."""
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL")


window.on_popup = on_popup


def on_popup_edit_new(target_element, data_element, new_url, param, event):
    """Create a modal edit popup dialog."""
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_EDIT")


window.on_popup_edit_new = on_popup_edit_new


def on_popup_info(target_element, data_element, new_url, param, event):
    """Create a modal info popup dialog."""
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_INFO")


window.on_popup_info = on_popup_info


def on_popup_delete(target_element, data_element, new_url, param, event):
    """Create a modal delete confirmation popup."""
    return _on_popup(
        target_element, data_element, new_url, param, event, "MODAL_DELETE"
    )


window.on_popup_delete = on_popup_delete


def on_popup_error(target_element, data_element, new_url, param, event):
    """Create a modal error popup."""
    return _on_popup(target_element, data_element, new_url, param, event, "MODAL_ERROR")


window.on_popup_error = on_popup_error


# =============================================================================
# Tab navigation handlers
# =============================================================================


def on_new_tab(target_element, data_element, new_url, param, event):
    """Open content in a new application tab (or activate existing).

    Extracts the title from the response and delegates to the menu system.
    """
    title, title_alt = _get_title(target_element, data_element, new_url)
    data_element2 = data_element.querySelector("section.body-body")
    if not data_element2:
        data_element2 = data_element
    return get_menu().on_menu_href(
        target_element, data_element2, title, title_alt, new_url
    )


window.on_new_tab = on_new_tab


def on_replace_app(target_element, data_element, new_url, param, event):
    """Replace the entire application content (for _top targets).

    Clears the current content wrapper, mounts new content from the
    response's body-body section, reinitializes the start page, and
    re-activates the menu. Preserves subpage navigation if present.
    """
    subpages = (URLSearchParams(window.location.search)).getAll("subpage")
    if subpages:
        subpage = subpages[0]
    else:
        subpage = None

    if window.PUSH_STATE:
        history_push_state("", window.BASE_PATH)
    else:
        window.location.pathname = window.BASE_PATH

    window.MENU = None

    wrapper = document.querySelector("div.content-wrapper")
    if wrapper:
        wrapper.innerHTML = ""
    mount_html(
        wrapper,
        data_element.querySelector("section.body-body"),
        False,
    )
    window.init_start_page()
    window.activate_menu()

    if subpage:
        objects = Array.prototype.slice.call(document.querySelectorAll("a"))
        for obj in objects:
            if obj.href and obj.classList.contains("menu-href"):
                if subpage in obj.href:
                    obj.click()
                    break

    return wrapper


# =============================================================================
# Subpage/subframe navigation (stack-based)
# =============================================================================


def _on_subframe(frame_element, target_element, data_element, url, param, event):
    """Push new content onto the subframe stack.

    Saves the current frame content into a hidden stack-slot and
    replaces it with new data.
    """
    stack_slot = document.createElement("div")
    stack_slot.style.display = "none"
    stack_slot.classList.add("stack-slot")
    while frame_element.childNodes.length > 0:
        stack_slot.appendChild(frame_element.childNodes[0])
    mount_html(frame_element, data_element)
    frame_element.prepend(stack_slot)


def on_subpage(target_element, data_element, new_url, param, event):
    """Navigate to a subpage within the current page."""
    page = target_element.closest(".page")
    return _on_subframe(page, target_element, data_element, new_url, param, event)


window.on_subpage = on_subpage


def on_subframe(target_element, data_element, new_url, param, event):
    """Navigate to a subframe (within an ajax-frame or data-link target)."""
    if target_element.hasAttribute("data-link"):
        frame = super_query_selector(
            target_element, target_element.getAttribute("data-link")
        )
    else:
        frame = target_element.closest(".ajax-frame")
    return _on_subframe(frame, target_element, data_element, new_url, param, event)


window.on_subframe = on_subframe


def _on_close_subpage(page, target_element, data_element, new_url, param, event):
    """Pop the subpage/subframe stack, restoring previous content.

    Removes 'count' levels of stack-slots from the page.
    """
    if target_element.hasAttribute("subpage-count"):
        count = int(target_element.getAttribute("subpage-count"))
    else:
        count = 1
    temp_slot = document.createElement("div")
    if page.childNodes.length > 0:
        child = page.childNodes[0]
        if (
            (not child)
            or (not hasattr(child, "classList"))
            or (not child.classList.contains("stack-slot"))
        ):
            return
        temp_slot.appendChild(child)

    def _on_remove(index, value):
        value.on_remove()

    jQuery.each(jQuery(page).find(".call_on_remove"), _on_remove)

    stack_slot = temp_slot.childNodes[0]
    while count > 1:
        child = stack_slot.childNodes[0]
        if (
            (not child)
            or (not hasattr(child, "classList"))
            or (not child.classList.contains("stack-slot"))
        ):
            break
        stack_slot = child
        count -= 1

    page.innerHTML = ""
    while stack_slot.childNodes.length > 0:
        page.appendChild(stack_slot.childNodes[0])

    return page


def on_close_subpage(target_element, data_element, new_url, param, event):
    """Close the current subpage and restore the previous one."""
    page = target_element.closest(".page")
    return _on_close_subpage(page, target_element, data_element, new_url, param, event)


def on_close_subpage_and_refresh(target_element, data_element, new_url, param, event):
    """Close subpage and refresh the parent frame."""
    page = target_element.closest(".page")
    ret = on_close_subpage(target_element, data_element, new_url, param, event)
    window.refresh_ajax_frame(page)
    return ret


def on_close_subframe(target_element, data_element, new_url, param, event):
    """Close the current subframe and restore previous content."""
    if target_element.hasAttribute("data-link"):
        frame = super_query_selector(
            target_element, target_element.getAttribute("data-link")
        )
    else:
        frame = target_element.closest(".ajax-frame")
    return _on_close_subpage(frame, target_element, data_element, new_url, param, event)


def on_close_subframe_and_refresh(target_element, data_element, new_url, param, event):
    """Close subframe and refresh the parent."""
    if target_element.hasAttribute("data-link"):
        frame = super_query_selector(
            target_element, target_element.getAttribute("data-link")
        )
    else:
        frame = target_element.closest(".ajax-frame")
    ret = on_close_subframe(target_element, data_element, new_url, param, event)
    window.refresh_ajax_frame(frame)
    return ret


# =============================================================================
# Close and refresh frame handlers
# =============================================================================


def close_frame(target_element, data_element, new_url, param, event, data_region=None):
    """Close a dialog/frame and optionally refresh the parent region.

    Handles both modal (Bootstrap) and inline plug dismissal,
    with opacity feedback during the close operation.

    Args:
        target_element: The element that triggered the close.
        data_element: Response data to mount after close.
        data_region: Optional region name override.
    """
    f = target_element.getAttribute("data-link")
    if f:
        data_element2 = super_query_selector(data_element, f)
    else:
        data_element2 = data_element

    if data_region:
        data_region2 = data_region
    else:
        data_region2 = target_element.getAttribute("data-region")

    region = get_ajax_region(
        get_ajax_region(target_element, "page").parentElement, data_region2
    )

    dialog = None
    aside = target_element.closest(".plug")
    if aside and region.contains(aside):
        dialog = aside.firstElementChild
    else:
        aside = None

    def _callback():
        """After successful refresh, dismiss the dialog."""
        nonlocal aside, dialog
        if aside:
            if dialog and dialog.classList.contains("modal"):
                jQuery(dialog).modal("hide")
            else:
                aside.remove()

    def _callback_on_error():
        """On error, restore dialog opacity."""
        nonlocal aside, dialog
        if aside:
            aside.style.opacity = "100%"

    if aside:
        aside.style.opacity = "50%"

    return refresh_ajax_frame(
        target_element, data_region2, data_element2, _callback, _callback_on_error
    )


def refresh_frame(
    target_element, data_element, new_url, param, event, data_region=None
):
    """Refresh a frame with new content.

    Args:
        target_element: Element to use for region lookup.
        data_element: New content to mount.
        data_region: Optional region name for the frame to refresh.
    """
    f = target_element.getAttribute("data-link")
    if f:
        data_element2 = super_query_selector(data_element, f)
    else:
        data_element2 = data_element

    if data_region:
        data_region2 = data_region
    else:
        data_region2 = target_element.getAttribute("data-region")

    return refresh_ajax_frame(target_element, data_region2, data_element2)


def refresh_page(target_element, data_element, new_url, param, event):
    """Refresh the page-content region of the current page."""
    return refresh_frame(
        target_element, data_element, new_url, param, event, "page-content"
    )


def refresh_app(target_element, data_element, new_url, param, event):
    """Reload the entire application by navigating to the base path."""
    window.location.href = window.BASE_PATH


def only_get(target_element, data_element, url, param, event):
    """No-op handler for background GET requests (no UI update)."""
    pass


def on_message(target_element, data_element, new_url, param, event):
    """Display a SweetAlert2 message dialog.

    Reads icon, title, text, footer, and timer from data attributes
    on either the target_element or the data_element.
    """
    options = {
        "icon": "success",
        "title": "Information",
        "text": "success",
    }

    if target_element.hasAttribute("data-icon"):
        options["icon"] = target_element.getAttribute("data-icon")
    elif data_element.hasAttribute("data-icon"):
        options["icon"] = data_element.getAttribute("data-icon")

    if target_element.hasAttribute("data-title"):
        options["title"] = target_element.getAttribute("data-title")
    elif data_element.hasAttribute("data-title"):
        options["title"] = data_element.getAttribute("data-title")

    if target_element.hasAttribute("data-text"):
        options["text"] = target_element.getAttribute("data-text")
    elif data_element.hasAttribute("data-text"):
        options["text"] = data_element.getAttribute("data-text")

    if target_element.hasAttribute("data-footer"):
        options["footer"] = target_element.getAttribute("data-footer")
    elif data_element.hasAttribute("data-footer"):
        options["footer"] = data_element.getAttribute("data-footer")

    if target_element.hasAttribute("data-timer"):
        options["timer"] = target_element.getAttribute("data-timer")
    elif data_element.hasAttribute("data-timer"):
        options["timer"] = data_element.getAttribute("data-timer")

    Swal.fire(options)


# =============================================================================
# Event click routing table
# =============================================================================
# Maps (target, class_filter, get_only_content, get_only_tab, handler)
#
# Target types:
#   inline, inline_edit, inline_info, inline_delete, inline_error:
#       Embedded inline dialogs within the page.
#   popup, popup_edit, popup_info, popup_delete, popup_error:
#       Modal popup dialogs.
#   _top: Replace the entire application.
#   _top2: Open in a new application tab.
#   _self: Refresh the current page (page-content region).
#   _parent, page: Open in a new application tab.
#   refresh_frame: Refresh a specific frame region.
#   close_frame: Close a frame/dialog and refresh.
#   refresh_page: Refresh the current page.
#   refresh_app: Full application reload.
#   message: Display a Swal message.
#   subpage, subframe: Stack-based sub-navigation.
#   close-subpage, close-subframe: Pop the navigation stack.
#   null: Background GET, no UI update.

EVENT_CLICK_TAB = [
    # (target, class, get_only_content, get_only_tab, handler_function)
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
    ("page", "*", True, False, on_new_tab),
    ("refresh_frame", "*", True, False, refresh_frame),
    ("close_frame", "*", True, False, close_frame),
    ("refresh_page", "*", True, False, refresh_page),
    ("refresh_app", "*", False, False, refresh_app),
    ("message", "*", False, False, on_message),
    ("subpage", "*", True, False, on_subpage),
    ("subframe", "*", True, False, on_subframe),
    ("*", "close-subpage", True, False, on_close_subpage),
    ("*", "close-subpage-and-refresh", True, False, on_close_subpage_and_refresh),
    ("*", "close-subframe", True, False, on_close_subframe),
    ("*", "close-subframe-and-refresh", True, False, on_close_subframe_and_refresh),
    ("null", "*", False, False, only_get),
]


# =============================================================================
# Window resize handler
# =============================================================================


def on_resize(self, event):
    """Global window resize handler - triggers process_resize on body."""
    process_resize(document.body)


window.addEventListener("resize", on_resize)
