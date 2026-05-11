"""
Application entry point and initialization module.

This is the main bootstrap module that initializes the entire client-side
application. It sets up:
- Global state (window-level variables).
- Keyboard event handling (Enter key on DialogForm).
- Application initialization (app_init).
- Static path resolution.
- Menu activation and highlighting.
- Error handling for AJAX requests.
- Browser history (popstate) navigation.

Dependencies (loaded via pscript cross-module references):
    pytigon_js.tabmenu: Page, get_menu
    pytigon_js.offline: service_worker_and_indexedDB_test, install_service_worker
    pytigon_js.db: sync_and_run
    pytigon_js.component: GlobalBus
    pytigon_js.events: register_global_event
    pytigon_js.ajax_region: ajax_load, mount_html
"""

# =============================================================================
# Global state initialization
# =============================================================================

window.PS = None
window.MOUNTED_COMPONENTS = 0
window.GLOBAL_BUS = GlobalBus()
window.START_MENU_ID = None


# =============================================================================
# Keyboard event handlers
# =============================================================================


def _on_key(self, e):
    """Handle keypress events globally.

    When Enter is pressed on a non-TEXTAREA element within a DialogForm,
    triggers the form's OK action (on_edit_ok) and prevents default.

    Args:
        self: The event target element.
        e: jQuery keypress event object.
    """
    if e.which == 13:
        elem = jQuery(e.target)
        if elem.prop("tagName") != "TEXTAREA":
            form = elem.closest("form")
            if form.length > 0:
                if form.hasClass("DialogForm"):
                    e.preventDefault()
                    on_edit_ok(False, form)
                    return


register_global_event("keypress", _on_key, None)


# =============================================================================
# DOM ready handler (for traditional template)
# =============================================================================


def dom_content_loaded():
    """Handle DOMContentLoaded event for traditional application template.

    Mounts the initial HTML content into the body-body section.
    """
    mount_html(document.querySelector("section.body-body"), None)


# =============================================================================
# Application initialization
# =============================================================================


def app_init(
    prj_name,
    application_template,
    menu_id,
    lang,
    base_path,
    base_fragment_init,
    component_init,
    offline_support,
    start_page,
    gen_time,
    callback=None,
):
    """Initialize the entire client-side application.

    This is the main entry point called by the server-rendered page.
    It sets up all window-level configuration, initializes the offline
    service worker, runs database synchronization, and mounts the
    initial page content.

    Args:
        prj_name: Project name (used for IndexedDB database name).
        application_template: UI template mode:
            'modern', 'standard', 'simple', 'traditional', 'mobile',
            'tablet', 'hybrid'.
        menu_id: ID of the starting menu item.
        lang: Language/locale code (e.g. 'en', 'pl').
        base_path: Base URL path prefix for the application.
        base_fragment_init: Fragment initialization mode.
        component_init: Component initialization callback.
        offline_support: Whether to enable offline/PWA features.
        start_page: URL of the initial page to load.
        gen_time: Server-side generation timestamp for cache busting.
        callback: Optional callback invoked after initialization.
    """
    window.IN_MORPH_PROCESS = False
    moment.locale(lang)
    window.ACTIVE_PAGE = None
    window.PRJ_NAME = prj_name
    window.APPLICATION_TEMPLATE = application_template
    window.MENU = None
    window.PUSH_STATE = True
    if base_path:
        window.BASE_PATH = base_path
    else:
        window.BASE_PATH = ""
    window.WAIT_ICON = None
    window.WAIT_ICON2 = False
    window.START_MENU_ID = menu_id
    window.BASE_FRAGMENT_INIT = base_fragment_init
    window.COUNTER = 1
    window.EDIT_RET_FUNCTION = None
    window.RET_CONTROL = None
    window.COMPONENT_INIT = component_init
    window.LANG = lang
    window.GEN_TIME = gen_time

    # Register service worker for offline support if available
    if offline_support:
        if navigator.onLine and service_worker_and_indexedDB_test():
            install_service_worker()

    def _on_sync(status):
        """Handle system sync completion - reload page if cache was stale."""
        if status == "OK-refresh":
            location.reload()

    sync_and_run("sys", _on_sync)

    def _init_start_page():
        """Load the initial start page content via AJAX.

        Only loads if start_page is specified and the current URL matches
        the base path or ends with index.html.
        """
        if (
            start_page
            and start_page != "None"
            and (
                window.location.pathname == base_path
                or window.location.pathname.endswith("index.html")
            )
        ):

            def _on_load(responseText, status, response):
                print("_init_start_page::_on_load")

            p = base_path + start_page
            ajax_load(document.querySelector("#body_desktop"), p, _on_load)

    window.init_start_page = _init_start_page
    _init_start_page()

    # Invoke custom init callback if defined on window
    if hasattr(window, "init_callback"):
        window.init_callback()

    # Set jQuery plugin defaults
    jQuery.fn.editable.defaults.mode = "inline"
    jQuery.fn.combodate.defaults["maxYear"] = 2025

    # Mount initial HTML in the desktop area
    desktop = document.getElementById("body_desktop")
    if desktop:
        mount_html(desktop, None, None)

    # Handle subpage navigation from URL query parameter
    if window.location.search and "subpage" in window.location.search:
        href = window.location.search.split("=")[1]
        objects = Array.prototype.slice.call(document.querySelectorAll("a"))
        for obj in objects:
            if obj.href and obj.classList.contains("menu-href"):
                if href in obj.href:
                    obj.click()
                    break


window.app_init = app_init


# =============================================================================
# Static path resolution
# =============================================================================


def static_path(path):
    """Resolve a static asset path with the application base path prefix.

    Args:
        path: Absolute path starting with '/' (e.g. '/static/js/app.js').

    Returns:
        str: Path with BASE_PATH prepended (minus the leading '/'),
             or the original path if BASE_PATH is not set.
    """
    if hasattr(window, BASE_PATH) and window.BASE_PATH and len(window.BASE_PATH) > 0:
        return window.BASE_PATH + path[1:]
    else:
        return path


window.static_path = static_path


# =============================================================================
# Menu activation
# =============================================================================


def activate_menu():
    """Highlight the current menu item based on the browser URL pathname.

    Scans all 'a.menu-href' elements and activates the one matching the
    current URL. For sidebar menus (sys-sidebarmenu), expands parent
    treeview nodes. For tab menus, switches to the matching tab.
    """
    pathname = window.location.pathname
    if pathname.startswith(window.BASE_PATH):
        pathname2 = pathname[len(window.BASE_PATH) :]
    else:
        pathname2 = pathname

    if pathname2:
        menu = document.querySelector("sys-sidebarmenu")
        a_tab = Array.prototype.slice.call(document.querySelectorAll("a.menu-href"))
        for a in a_tab:
            if a.hasAttribute("href"):
                href = a.getAttribute("href").split("?")[0]
                if href.startswith("/" + pathname2):
                    if menu:
                        # Sidebar menu: expand parent treeview node
                        li = a.closest("li.treeview")
                        if li and not li.classList.contains("active"):
                            a = li.querySelector("a")
                            if a:
                                event = document.createEvent("MouseEvents")
                                event.initMouseEvent(
                                    "click",
                                    True,
                                    True,
                                    window,
                                    1,
                                    0,
                                    0,
                                    0,
                                    0,
                                    False,
                                    False,
                                    False,
                                    False,
                                    0,
                                    None,
                                )
                                a.dispatchEvent(event)
                    else:
                        # Tab menu: switch to matching tab
                        div = a.closest(".tab-tab")
                        if div:
                            id_elem = "a_" + div.id
                            x = document.getElementById(id_elem)
                            if x:
                                jQuery(x).tab("show")


window.activate_menu = activate_menu


# =============================================================================
# Error handling
# =============================================================================


def _on_error(request, settings):
    """Global AJAX error handler.

    Displays server error responses in a modal dialog. When the response
    contains a <body> tag, extracts the body content for display.

    Args:
        request: The XMLHttpRequest object.
        settings: jQuery AJAX settings including status and responseText.
    """
    # Stop any active loading indicators
    if window.WAIT_ICON:
        window.WAIT_ICON.stop()
        window.WAIT_ICON = None
    if window.WAIT_ICON2:
        jQuery("#loading-indicator").hide()
        window.WAIT_ICON2 = False

    if settings.status == 200:
        return

    if settings.responseText:
        # Try to extract <body> content from the error response
        start = settings.responseText.indexOf("<body>")
        end = settings.responseText.lastIndexOf("</body>")
        if start > 0 and end > 0:
            mount_html(
                jQuery("#dialog-data-error"),
                settings.responseText.substring(start + 6, end - 1),
            )
            if window.hasOwnProperty("bootstrap"):
                d = bootstrap.Modal(document.getElementById("dialog-form-error"))
                d.hide()
            else:
                jQuery("#dialog-form-error").modal()
        else:
            mount_html(jQuery("#dialog-data-error"), settings.responseText)
            if window.hasOwnProperty("bootstrap"):
                d = bootstrap.Modal(document.getElementById("dialog-form-error"))
                d.hide()
            else:
                jQuery("#dialog-form-error").modal()


# =============================================================================
# jQuery ready callback (placeholder for extensions)
# =============================================================================


def jquery_ready():
    """Placeholder for jQuery document ready callback.

    Override or extend this function to run code after the DOM is ready.
    """
    pass


window.jquery_ready = jquery_ready


# =============================================================================
# Browser history (popstate) navigation
# =============================================================================


def _on_popstate(self, e):
    """Handle browser back/forward navigation (popstate event).

    Restores page state from history:
    - In 'modern' template: activates the tab from stored state.
    - In other templates: decompresses and mounts stored HTML content.
    - In 'standard' template: also restores button highlighting.

    Args:
        self: The window object.
        e: PopStateEvent with state data.
    """
    if e.state:
        window.PUSH_STATE = False
        if window.APPLICATION_TEMPLATE == "modern":
            menu = get_menu().activate(e.state, False)
        else:
            x = e.state
            mount_html(jQuery("#body_desktop"), LZString.decompress(x[0]))
            window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"))
            window.ACTIVE_PAGE.set_href(document.location)

            if window.APPLICATION_TEMPLATE == "standard":
                jQuery("a.menu-href").removeClass("btn-warning")
                jQuery("#" + x[1]).addClass("btn-warning")
        window.PUSH_STATE = True
    else:
        if window.APPLICATION_TEMPLATE == "modern":
            pass
        else:
            mount_html(jQuery("#body_desktop"), "", False, False)
            window.ACTIVE_PAGE = None
            if window.APPLICATION_TEMPLATE == "standard":
                jQuery("a.menu-href").removeClass("btn-warning")


window.addEventListener("popstate", _on_popstate, False)
