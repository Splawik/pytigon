"""
Inline scripts extracted from template files.

Contains widget initialization code previously embedded as inline <script>
tags in Django templates. These functions are registered via
register_mount_fun to run automatically after both initial page load and
AJAX content mounting.

Provides:
- Treeview toggle (expand/collapse) initialization.
- Action control widget click handler initialization.
- PWA service worker registration.
"""


# =============================================================================
# Treeview initialization
# =============================================================================


def _treeview_init(dest_elem):
    """Initialize treeview toggle functionality in the given element.

    Attaches click handlers to treeview parent nodes for expand/collapse
    behavior. Also initializes CSS classes and hides initially-hidden nodes.

    Safe to call multiple times - uses off/on to make handlers idempotent.

    Args:
        dest_elem: DOM element to scan for .tree containers.
    """
    jQuery(dest_elem).find(".tree li:has(ul)").addClass("parent_li").find(
        " > span"
    ).attr("title", "Collapse this branch")

    def on_click(e):
        """Toggle visibility of child nodes on click."""
        children = jQuery(this).parent("li.parent_li").find(" > ul > li")
        if RawJS("children.is(':visible')"):
            children.hide("fast")
            jQuery(this).attr("title", "Expand this branch").find(" > i").addClass(
                "fa-plus"
            ).removeClass("fa-minus")
        else:
            children.show("fast")
            jQuery(this).attr("title", "Collapse this branch").find(" > i").addClass(
                "fa-minus"
            ).removeClass("fa-plus")
        if e:
            e.stopPropagation()

    # Use off/on to make it idempotent (safe for repeated calls)
    jQuery(dest_elem).find(".tree li.parent_li > span").off("click", on_click).on(
        "click", on_click
    )
    jQuery(dest_elem).find(".hide_node").hide().removeClass("hide")


# =============================================================================
# Action control widget initialization
# =============================================================================


def _action_ctrl_init(dest_elem):
    """Initialize action control widgets in the given element.

    Finds all .action-ctrl elements and sets up click handlers for their
    child anchor elements. Uses data-ctrl-id and data-ctrl-value attributes
    for per-instance configuration.

    Args:
        dest_elem: DOM element to scan for .action-ctrl containers.
    """
    jQuery(dest_elem).find(".action-ctrl").each(_init_single_action_ctrl)


def _init_single_action_ctrl(i, el):
    """Initialize a single action control widget.

    Args:
        i: Index in the jQuery collection.
        el: The raw DOM element (.action-ctrl container).
    """
    ctrl_id = el.getAttribute("data-ctrl-id")
    if not ctrl_id:
        return

    ctrl_value = el.getAttribute("data-ctrl-value") or "None"
    sel_class = "control_sel"

    # Store the selected element reference keyed by ctrl_id
    window["_action_ctrl_" + ctrl_id + "_var"] = None

    def on_link_click(e):
        nonlocal ctrl_id, sel_class
        # Deselect previously selected
        prev = window["_action_ctrl_" + ctrl_id + "_var"]
        if prev:
            prev.parent(".control").removeClass(sel_class)

        # Select current
        window["_action_ctrl_" + ctrl_id + "_var"] = jQuery(this)
        jQuery(this).parent(".control").addClass(sel_class)

        href_attr = jQuery(this).attr("href")
        if href_attr:
            new_value = href_attr.replace("action/", "")
            if hasattr(window, "cmd_to_python"):
                cmd_to_python(
                    "python|self." + ctrl_id + ".SetValue('" + new_value + "')"
                )
            else:
                jQuery("#id_" + ctrl_id).val(new_value)

        return False

    jQuery(el).find("a").off("click", on_link_click).on("click", on_link_click)

    # Auto-select the current value if set
    if ctrl_value and ctrl_value != "None":
        jQuery(el).find("a").each(
            lambda idx, a: (
                jQuery(a).click()
                if jQuery(a).attr("href") == "action/" + ctrl_value
                else None
            )
        )


# =============================================================================
# PWA service worker registration
# =============================================================================


def _pwa_init(dest_elem):
    """Register the PWA service worker if supported by the browser.

    Reads the service worker URL and scope from meta tags:
    <meta name="pwa-sw-url" content="...">
    <meta name="pwa-sw-scope" content="...">

    Args:
        dest_elem: DOM element (unused, reads from document.head).
    """
    if not RawJS("'serviceWorker' in navigator"):
        return

    sw_url_meta = document.querySelector('meta[name="pwa-sw-url"]')
    sw_scope_meta = document.querySelector('meta[name="pwa-sw-scope"]')

    if not sw_url_meta:
        return

    sw_url = sw_url_meta.getAttribute("content")
    sw_scope = sw_scope_meta.getAttribute("content") if sw_scope_meta else "/"

    def on_success(registration):
        """Log successful service worker registration."""
        console.log(
            "django-pwa: ServiceWorker registration successful with scope: ",
            registration.scope,
        )

    def on_error(err):
        """Log failed service worker registration."""
        console.log("django-pwa: ServiceWorker registration failed: ", err)

    navigator.serviceWorker.register(sw_url, {"scope": sw_scope}).then(
        on_success, on_error
    )


# =============================================================================
# Register mount hooks for automatic initialization
# =============================================================================

register_mount_fun(_treeview_init)
register_mount_fun(_action_ctrl_init)


# =============================================================================
# Auto-initialize on DOM ready (for initial page load before any mount_html)
# =============================================================================


def _auto_init():
    """Auto-initialize widgets when the DOM is ready (initial page load)."""
    _treeview_init(document)
    _action_ctrl_init(document)
    _pwa_init(document)


jQuery(document).ready(_auto_init)
