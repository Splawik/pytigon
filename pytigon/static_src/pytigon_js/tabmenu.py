"""
Tab-based navigation menu system.

Provides a multi-tab page management system that creates and manages
Bootstrap tab panels for navigation. Supports:
- Creating new tabs with dynamic content loading.
- Activating existing tabs by title.
- Removing tabs and cleaning up associated DOM elements.
- Push state history integration for back/forward navigation.
- Different behavior based on APPLICATION_TEMPLATE setting.

Classes:
    Page: Represents an active page/tab in the UI.
    TabMenuItem: Metadata for a single menu tab item.
    TabMenu: Core tab management engine.
"""


# =============================================================================
# Page abstraction
# =============================================================================


class Page:
    """Represents an active page (tab pane) in the UI.

    Associates a tab DOM element with its identifier and tracks
    the current href for history management.

    Attributes:
        id: Unique tab identifier (string).
        page: jQuery-wrapped tab pane DOM element.
    """

    def __init__(self, id, page):
        self.id = id
        self.page = page

    def set_href(self, href):
        """Store the href associated with this page for history."""
        self.page.attr("_href", href)

    def get_href(self):
        """Retrieve the stored href for this page."""
        return self.page.attr("_href")


# =============================================================================
# Tab menu item metadata
# =============================================================================


class TabMenuItem:
    """Metadata for a single tab in the menu system.

    Attributes:
        id: Unique DOM identifier for the tab (string).
        title: Display title of the tab (trimmed).
        url: Navigation URL associated with the tab.
        data: Optional content data for the tab.
    """

    def __init__(self, id, title, url, data=None):
        self.id = id
        self.title = title.trim()
        self.url = url
        self.data = data


# =============================================================================
# Tab menu manager
# =============================================================================


class TabMenu:
    """Core manager for the Bootstrap-based tab navigation system.

    Creates and manages tab elements in the #tabs2 container, handling
    tab creation, activation, removal, and browser history integration.

    The menu behavior differs by APPLICATION_TEMPLATE:
        - 'modern': Uses the full tab system with history push state.
        - Other: Uses simpler body_desktop content replacement.
    """

    def __init__(self):
        """Initialize the tab menu with an empty state."""
        self.id = 0
        self.titles = {}
        self.active_item = None

    def get_active_item(self):
        """Return the currently active TabMenuItem, or None."""
        return self.active_item

    def is_open(self, title):
        """Check whether a tab with the given title is currently open.

        Args:
            title: Tab title to check.

        Returns:
            bool: True if the tab exists and is open.
        """
        if self.titles and title in self.titles and self.titles[title]:
            return True
        else:
            return False

    def activate(self, title, push_state=True):
        """Activate an existing tab by its title.

        Shows the tab panel and optionally pushes a history state entry.

        Args:
            title: Title of the tab to activate.
            push_state: If True (and window.PUSH_STATE is True), push
                a history entry for back/forward navigation.
        """
        menu_item = self.titles[title]
        jQuery(sprintf("#li_%s a", menu_item.id)).tab("show")
        if push_state and window.PUSH_STATE:
            history_push_state(menu_item.title, menu_item.url)

    def register_title(self, title):
        """Pre-register a tab title (marks it as reserved with '$$$').

        Args:
            title: Title to reserve in the tab registry.
        """
        self.titles[title] = "$$$"

    def new_page(self, title, data_or_html, href, title_alt=None):
        """Create a new tab page with content.

        Builds the tab navigation element (#tabs2 li), the tab content
        pane (#tabs2_content div), mounts the provided HTML content,
        and binds tab events (show, close button, inline scripts).

        Args:
            title: Display title for the new tab.
            data_or_html: HTML content or DOM element to mount in the tab.
            href: URL associated with the tab (for history and reloading).
            title_alt: Alternative title for lookup (optional).

        Returns:
            str: The generated tab DOM id.
        """
        _id = "tab" + self.id

        # Register the menu item in the titles dictionary
        menu_item = TabMenuItem(_id, title, href, data_or_html)
        self.titles[title] = menu_item
        if title_alt and title_alt != title:
            self.titles[title_alt] = menu_item

        # Build the tab navigation element
        menu_pos = vsprintf(
            "<li id='li_%s' class ='nav-item'><a href='#%s' class='nav-link bg-info' data-toggle='tab' data-bs-toggle='tab' role='tab' title='%s'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-outline-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>",
            [_id, _id, title, title, _id],
        )

        append_left = jQuery("#tabs2").hasClass("append-left")

        if append_left:
            jQuery("#tabs2").prepend(menu_pos)
        else:
            jQuery("#tabs2").append(menu_pos)

        # Build the tab content pane
        jQuery("#tabs2_content").append(
            sprintf(
                "<div class='tab-pane container-fluid ajax-region ajax-frame ajax-link win-content content page' id='%s' data-region='page' href='%s'></div>",
                _id,
                href,
            )
        )

        # Set as active page and push history state
        window.ACTIVE_PAGE = Page(_id, jQuery("#" + _id))
        self.active_item = menu_item

        if window.PUSH_STATE:
            history_push_state(title, href)

        def _on_show_tab(self, e):
            """Handle tab shown event: update active page and push history."""
            nonlocal menu_item
            window.ACTIVE_PAGE = Page(_id, jQuery("#" + _id), menu_item)

            menu = get_menu()
            menu_item = menu.titles[e.target.text.trim()]
            self.active_item = menu_item
            if window.PUSH_STATE:
                history_push_state(menu_item.title, menu_item.url)

            process_resize(document.getElementById(menu_item.id))

        # Show the new tab (first or last depending on append direction)
        if append_left:
            jQuery("#tabs2 a:first").on("shown.bs.tab", _on_show_tab)
            jQuery("#tabs2 a:first").tab("show")
        else:
            jQuery("#tabs2 a:last").on("shown.bs.tab", _on_show_tab)
            jQuery("#tabs2 a:last").tab("show")

        # Mount the HTML content into the new tab pane
        mount_html(document.getElementById(_id), data_or_html, None)

        def _on_button_click(self, event):
            """Handle close button click on the tab."""
            get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""))

        jQuery(sprintf("#button_%s", _id)).click(_on_button_click)

        # Evaluate any inline scripts within the new tab content
        scripts = jQuery("#" + _id + " script")

        def _local_fun(index, element):
            eval(this.innerHTML)

        scripts.each(_local_fun)

        self.id += 1
        return _id

    def remove_page(self, id):
        """Remove a tab by its DOM id.

        Cleans up both the navigation element (#li_<id>) and the content
        pane (#<id>). Activates the last remaining tab or restores the
        body_desktop if no tabs remain.

        Args:
            id: The tab DOM id to remove (without '#' prefix).
        """

        def _local_fun(index, value):
            if value and value.id == id:
                self.titles[index] = None

        jQuery.each(self.titles, _local_fun)

        remove_element(sprintf("#li_%s", id))
        remove_element(sprintf("#%s", id))

        last_a = jQuery("#tabs2 a:last")
        if last_a.length > 0:
            last_a.tab("show")
        else:
            window.ACTIVE_PAGE = None
            if window.PUSH_STATE:
                history_push_state("", window.BASE_PATH)
            if jQuery("#body_desktop").find(".content").length == 0:
                window.init_start_page()
            jQuery("#body_desktop").show()

    def on_menu_href(self, elem, data_or_html, title, title_alt=None, url=None):
        """Handle a menu link click: either activate an existing tab or create a new one.

        Behavior depends on APPLICATION_TEMPLATE:
        - 'modern': Uses the full tab system.
        - Other: Replaces body_desktop content directly.

        Valid APPLICATION_TEMPLATE values:
            'standard', 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

        Args:
            elem: The clicked DOM element.
            data_or_html: HTML content to display.
            title: Title for the tab/page.
            title_alt: Alternative title for lookup.
            url: Navigation URL (falls back to elem's href if not provided).

        Returns:
            bool: False to prevent default navigation.
        """
        if window.APPLICATION_TEMPLATE == "modern":
            if self.is_open(title):
                self.activate(title)
            else:
                self.register_title(title)
                href = url or jQuery(elem).attr("href")
                href2 = correct_href(href)

                jQuery("#body_desktop").hide()
                self.new_page(title, data_or_html, href2, title_alt)

            jQuery(".auto-hide").trigger("click")
            return False
        else:
            mount_html(document.querySelector("#body_desktop"), data_or_html, None)
            jQuery(".auto-hide").trigger("click")
            return False


# =============================================================================
# Singleton accessor
# =============================================================================


def get_menu():
    """Get or create the singleton TabMenu instance.

    Returns:
        TabMenu: The global menu instance stored in window.MENU.
    """
    if not window.MENU:
        window.MENU = TabMenu()
    return window.MENU
