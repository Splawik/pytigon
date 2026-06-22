"""
Bootstrap Table integration and data table management module.

Provides initialization and lifecycle management for Bootstrap Table
widgets including:
- Table height management and responsive sizing.
- AJAX data loading with server-side pagination/sorting.
- Row selection, checkboxes, and inline editing.
- Table action dropdowns and toolbar expand/collapse.
- Data change event handling (loadeddata) for table refresh.
- Visual feedback for row-level operations.

Dependencies (pscript cross-module):
    pytigon_js.tools: ajax_post, ajax_get, get_table_type, load_js
    pytigon_js.ajax_region: refresh_ajax_frame
"""


# =============================================================================
# Visibility helpers
# =============================================================================


def _is_visible(element):
    """Check if an element is visible using jQuery's :visible selector."""
    test = RawJS('jQuery(element).is(":visible")')
    if test:
        return True
    else:
        return False


# =============================================================================
# Table height management
# =============================================================================


def old_datetable_set_height(element):
    """Legacy table height calculation based on window/viewport offsets.

    Used for tables with the 'table_get' class.
    """
    if jQuery(element).hasClass("table_get"):
        return
    if not _is_visible(element):
        return

    elem = jQuery(element).closest(".tabsort_panel")

    table_offset = elem.offset().top
    dy_win = jQuery(window).height()

    dy = dy_win - table_offset

    if (
        elem[0].hasAttribute("table-details")
        and elem[0].getAttribute("table-details") == "1"
    ):
        details = super_query_selector(elem[0], "^.table-and-details/.row-details")
        details_height = details.clientHeight
        dydy = details_height * dy_win / 100

    dy -= dydy

    if dy < 200:
        dy = 200

    panel = elem.find(".fixed-table-toolbar")
    if not _is_visible(panel):
        dy += panel.outerHeight() + 5

    jQuery(element).bootstrapTable("resetView", {"height": dy - 5})


def datetable_set_height(element):
    """Calculate table height based on parent container height.

    Modern approach: uses the parent's height instead of window offsets.
    """
    if not _is_visible(element):
        return

    elem = jQuery(element).closest(".tabsort_panel")

    dy = elem.parent().height()

    if dy < 200:
        dy = 200

    panel = elem.find(".fixed-table-toolbar")
    if not _is_visible(panel):
        dy += panel.outerHeight() + 5

    jQuery(element).bootstrapTable("resetView", {"height": dy - 10})


# =============================================================================
# Table refresh
# =============================================================================


def datatable_refresh(element):
    """Refresh a Bootstrap Table - either directly or via parent region.

    If the element itself has the .tabsort class, refreshes it directly.
    Otherwise, looks for the nearest 'table' region and refreshes tables within.
    """
    if element.classList.contains("tabsort"):
        jQuery(element).bootstrapTable("refresh", {"silent": True})
    else:
        region = get_ajax_region(element, "table")
        if region != None:
            jQuery(region).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh", {"silent": True}
            )


window.datatable_refresh = datatable_refresh


# =============================================================================
# Table row styling
# =============================================================================


def _rowStyle(value, row, index):
    """Extract row CSS class from the cid (cell identifier) column.

    Looks for a div.td_information within the cid column and extracts
    additional CSS classes for row-level styling.

    Args:
        value: Row data object.
        row: Full row data.
        index: Row index.

    Returns:
        dict: {'classes': css_class} if found, otherwise {}.
    """
    x = jQuery("<div class='cid'>" + value["cid"] + "</div>").find("div.td_information")
    if x.length > 0:
        c = x.attr("class").replace("td_information", "").replace(" ", "")
        if c.length > 0:
            return {"classes": c}
    return {}


# =============================================================================
# Table preparation helpers
# =============================================================================


def prepare_datatable(table):
    """Post-render cleanup: merge second_row cells and auto-select if needed.

    - Merges div.second_row cells by removing siblings and setting colspan.
    - Triggers auto-select checkbox if data-autoselect attribute is set.
    """

    def _local_fun(index):
        td = jQuery(this).parent()
        tr = td.parent()
        l = tr.find("td").length
        tr.find("td:gt(0)").remove()
        td.attr("colspan", l)

    table.find("div.second_row").each(_local_fun)
    if table[0].hasAttribute("data-autoselect"):
        table[0].closest(".bootstrap-table").querySelector("[name='select']").click()


def prepare0(table):
    """Remove 'flexible_size' class from header tables within the frame."""
    refr_block = table.closest(".ajax-frame")
    if refr_block:
        tables = Array.prototype.slice.call(
            refr_block[0].querySelectorAll("div.fixed-table-header table.tabsort")
        )
        for table in tables:
            table.classList.remove("flexible_size")


# =============================================================================
# AJAX data source for Bootstrap Table
# =============================================================================


def datatable_ajax(params):
    """Custom AJAX handler for Bootstrap Table server-side processing.

    For tables within a form: serializes the form data and sends a POST.
    Otherwise: sends a GET with query parameters.

    Args:
        params: Bootstrap Table AJAX parameters dict with url, data, success keys.
    """
    url = params["url"]
    success = params["success"]
    if "form" in dict(params["data"]):
        form = params["data"]["form"]
        del params["data"]["form"]
        d = jQuery.param(params["data"])
        url += "?" + d

        def _on_post_data(data):
            d2 = JSON.parse(data)
            success(d2)

        ajax_post(url, form, _on_post_data)

    else:
        d = jQuery.param(params["data"])
        url += "?" + d

        def _on_get_data(data):
            d2 = JSON.parse(data)
            success(d2)

        ajax_get(url, _on_get_data)


# =============================================================================
# Main table initialization
# =============================================================================


def init_table(table, table_type):
    """Initialize a Bootstrap Table with full configuration.

    Sets up:
    - Checkbox columns (visible for .multiple-select, hidden otherwise).
    - Row ID column.
    - AJAX data loading.
    - Row click handling and row-active region updates.
    - Toolbar expand/collapse.
    - Resize handling.
    - Inline editing with auto-advance.

    Args:
        table: jQuery-wrapped table element.
        table_type: Table type string (e.g. 'datatable').
    """
    if table_type == "datatable":
        # Add checkbox column (visible or hidden depending on multiple-select)
        if table.hasClass("multiple-select"):
            jQuery(table).find("tr:first").find("th:first").before(
                "<th data-field='state' data-checkbox='true' data-visible='true'></th>"
            )
        else:
            jQuery(table).find("tr:first").find("th:first").before(
                "<th data-field='state' data-checkbox='true' data-visible='false'></th>"
            )

        # Add hidden ID column
        jQuery(table).find("tr:first").find("th:last").after(
            "<th data-field='id' data-visible='false'>ID</th>"
        )

        def onLoadSuccess(data):
            """After loading data: prepare table and add pagination styling."""
            nonlocal table
            prepare_datatable(table)

            def _pagination():
                nonlocal table
                jQuery(table).closest(".fixed-table-container").find(
                    ".fixed-table-pagination ul.pagination a"
                ).addClass("page-link")

            setTimeout(_pagination, 0)
            return False

        def onPostHeader(data):
            """After header render: remove flexible_size from header tables."""
            nonlocal table
            prepare0(table)
            return False

        def onCheck(row, elem):
            """Handle row checkbox: update table_row_pk input and refresh active areas."""
            if elem.length > 0:
                x = elem[0].closest(".ajax-region[data-region='page'")
                if x:
                    x2 = x.querySelector("input[name='table_row_pk']")
                    if x2:
                        x2.value = row.id
                        row_active_divs = Array.prototype.slice.call(
                            x.querySelectorAll(".table-row-active")
                        )
                        for elem in row_active_divs:
                            if elem.classList.contains("show"):
                                refresh_ajax_frame(elem)

        def queryParams(p):
            """Add serialized form data to table query parameters."""
            nonlocal table
            base_elem = table[0].closest(".tabsort_panel")
            link = get_ajax_link(base_elem, "table")
            if link and link.tagName.lower() == "form":
                p["form"] = jQuery(link).serialize()
            else:
                link = get_ajax_link(base_elem, "page")
                if link and link.tagName.lower() == "form":
                    p["form"] = jQuery(link).serialize()
            return p

        icons = {
            "fullscreen": "fa-arrows-alt",
            "refresh": "fa-refresh",
            "toggleOff": "fa-toggle-off",
            "toggleOn": "fa-toggle-on",
            "columns": "fa-th-list",
        }

        def onRefresh(params):
            """After manual refresh: trigger auto-select if configured."""
            nonlocal table
            if table[0].hasAttribute("data-autoselect"):
                table[0].closest(".bootstrap-table").querySelector(
                    "[name='select']"
                ).click()

        # Initialize Bootstrap Table with full config
        if table.hasClass("table_get"):
            table.bootstrapTable(
                {
                    "onLoadSuccess": onLoadSuccess,
                    "onPostHeader": onPostHeader,
                    "onCheck": onCheck,
                    "onRefresh": onRefresh,
                    "height": 350,
                    "rowStyle": _rowStyle,
                    "queryParams": queryParams,
                    "ajax": datatable_ajax,
                    "icons": icons,
                }
            )
        else:
            table.bootstrapTable(
                {
                    "onLoadSuccess": onLoadSuccess,
                    "onPostHeader": onPostHeader,
                    "onCheck": onCheck,
                    "onRefresh": onRefresh,
                    "rowStyle": _rowStyle,
                    "queryParams": queryParams,
                    "ajax": datatable_ajax,
                    "icons": icons,
                    "buttonsOrder": [
                        "refresh",
                        "toggle",
                        "fullscreen",
                        "menu",
                        "select",
                        "columns",
                    ],
                }
            )

        # Initialize inline editing with auto-advance to next row
        def init_bootstrap_table(self, e, data):
            table.find("a.editable").editable({"step": "any"})

            def on_hidden_editable(self, e, reason):
                if reason == "save" or reason == "nochange":
                    next = jQuery(this).closest("tr").next().find(".editable")
                    if next.length > 0:
                        if next.hasClass("autoopen"):

                            def edit_next():
                                nonlocal next
                                next.editable("show")

                            setTimeout(edit_next, 300)
                        else:
                            next.focus()

            table.find("a.editable").on("hidden", on_hidden_editable)

        table.on("post-body.bs.table", init_bootstrap_table)

        # Handle column resize to recalculate table height
        def _on_column_resize_stop(event):
            nonlocal table
            datetable_set_height(table)

        table.on("column:resize:stop", _on_column_resize_stop)

        # Toolbar expand/collapse toggle
        table_panel = jQuery(table).closest("div.win-content")
        btn = table_panel.find(".tabsort-toolbar-expand").first()
        if btn:

            def _handle_toolbar_expand(self, elem):
                panel = table_panel.find(".fixed-table-toolbar").first()
                panel2 = table_panel.find(".list_content_header_second_row").first()
                if not jQuery(this).hasClass("active"):
                    panel.show()
                    panel2.show()
                else:
                    panel.hide()
                    panel2.hide()
                process_resize(document.body)

            btn.on("click", _handle_toolbar_expand)
            if btn.hasClass("active"):
                panel = table_panel.find(".fixed-table-toolbar")
                panel2 = jQuery(".list_content_header_second_row")
                panel.hide()
                panel2.hide()

        # Register resize callback on the table element
        def _process_resize(size_object):
            nonlocal table
            datetable_set_height(table[0])

        table[0].process_resize = _process_resize


window.init_table = init_table


# =============================================================================
# Table loadeddata event handler
# =============================================================================


def table_loadeddata(event):
    """Handle the loadeddata event for table elements.

    Processes server response markers and updates the table accordingly:
    - $$RETURN_REFRESH / $$RETURN_REFRESH_PARENT: refresh the table.
    - $$RETURN_ERROR: refresh with error region.
    - $$RETURN_HTML_ERROR: show SweetAlert error dialog.
    - $$RETURN_NEW_ROW_OK / $$RETURN_UPDATE_ROW_OK: append or update a row.
    - $$RETURN_OK: refresh the table.
    - Other: delegate to refresh_ajax_frame with 'page' region.
    """
    if getattr(event, "data"):
        dt = data_type(event.data)
        if dt in ("$$RETURN_REFRESH_PARENT", "$$RETURN_REFRESH"):
            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh", {"silent": True}
            )
        elif dt == "$$RETURN_ERROR":
            refresh_ajax_frame(
                event.srcElement if event.srcElement else event.data_source,
                "error",
                event.data,
            )
        elif dt == "$$RETURN_HTML_ERROR":
            if isinstance(event.data, str):
                txt = event.data
            else:
                txt = event.data.innerHTML
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
        elif dt in ("$$RETURN_UPDATE_ROW_OK", "$$RETURN_NEW_ROW_OK"):
            try:
                if isinstance(event.data, str):
                    _data = event.data
                else:
                    _data = event.data.innerHTML
                pk = int(_data.split("id:")[1].strip())
                table = event.srcElement if event.srcElement else event.data_source
                datatable = jQuery(table).find("table[name=tabsort].datatable")
                link = get_ajax_link(table, "page-content", True)
                if not link:
                    link = get_ajax_link(table, "page")
                url = None
                if link:
                    if link.hasAttribute("href"):
                        url = link.getAttribute("href")
                    elif link.hasAttribute("action"):
                        url = link.getAttribute("action")
                        post = True
                    elif link.hasAttribute("src"):
                        url = link.getAttribute("src")
                if url:
                    if "?" in url:
                        url += "&json=1&pk=" + str(pk)
                    else:
                        url += "?&json=1&pk=" + str(pk)
                    url = url.replace("/form/", "/json/")

                    url = correct_href(url, (link,))
                    url = process_href(url, jQuery(link.parentElement))

                    def _update(data):
                        """Update or append a row in the datatable."""
                        nonlocal datatable, dt
                        try:
                            d = JSON.parse(data)
                            if dt == "$$RETURN_NEW_ROW_OK":
                                datatable.bootstrapTable("append", d["rows"][0])
                                datatable.bootstrapTable("scrollTo", "bottom")
                            else:
                                id2 = d["rows"][0]["id"]
                                row = datatable.bootstrapTable("getRowByUniqueId", id2)
                                if row:
                                    datatable.bootstrapTable(
                                        "updateByUniqueId",
                                        {"id": id2, "row": d["rows"][0]},
                                    )
                                else:
                                    datatable.bootstrapTable(
                                        "refresh", {"silent": True}
                                    )
                        except Exception:
                            datatable.bootstrapTable("refresh", {"silent": True})

                    ajax_get(url, _update)
                    return
            except Exception:
                pass

            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh", {"silent": True}
            )
        elif dt in ("$$RETURN_OK",):
            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh", {"silent": True}
            )
        else:
            refresh_ajax_frame(
                event.srcElement if event.srcElement else event.data_source,
                "page",
                event.data,
            )
    else:
        jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
            "refresh", {"silent": True}
        )


window.table_loadeddata = table_loadeddata


# =============================================================================
# Loading template
# =============================================================================


def loading_template(message):
    """Return a Font Awesome spinner HTML template for loading states."""
    return '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>'


window.loading_template = loading_template


# =============================================================================
# Table action buttons
# =============================================================================


def datatable_action(btn, action):
    """Execute an action on the selected rows of a datatable.

    Collects selected row PKs and sends them to the table_action endpoint.

    Args:
        btn: The button element that triggered the action.
        action: Action name to send to the server.
    """
    div = btn.closest("div.tableframe")
    datatable = div.querySelector("table[name=tabsort].datatable")
    url = datatable.getAttribute("data-url") + "../table_action/"

    pk_tab = []
    tab = jQuery(datatable).bootstrapTable("getSelections")
    for item in tab:
        pk_tab.append(str(item.id))
    pk_list_str = ",".join(pk_tab)

    def _callback(data):
        if "RETURN_ACTION" in data:
            if data["RETURN_ACTION"] == None:
                return
        jQuery(datatable).bootstrapTable("refresh", {"silent": True})

    ajax_json(url + "?pks=" + pk_list_str, {"action": action}, _callback)


window.datatable_action = datatable_action


# =============================================================================
# Select/Menu toggle visibility
# =============================================================================


def on_check_toggle_visibility():
    """Toggle visibility of table selection checkboxes and menu button.

    When the 'select' button is clicked, shows/hides the state checkbox
    column and builds a dropdown menu from data-actions if configured.
    """
    datatable = this

    container = getattr(datatable, "$container")[0]
    menu_btn = container.querySelector("button[name=menu]")

    for item in datatable.getHiddenColumns():
        if item.field == "state":
            datatable.showColumn("state")
            menu_btn.style.display = "block"
            if menu_btn.classList.contains("btn-secondary"):
                div = container.closest("div.tableframe")
                if div.hasAttribute("data-actions"):
                    actions = div.getAttribute("data-actions").split(";")
                else:
                    actions = []

                dropdown = document.createElement("div")
                dropdown.classList.add("dropleft")

                html = "<button name='menu' class='btn btn-info dropdown-toggle' type='button' data-bs-toggle='dropdown' data-toggle='dropdown'><i class='fa fa-bars'></i></button>"
                html += "<div class='dropdown-menu'>"
                for s in actions:
                    if "/" in s:
                        x = s.split("/")
                    else:
                        x = (s, s)
                    html += (
                        "<button class='dropdown-item' type='button' onclick=\"datatable_action(this, '"
                        + x[0].strip()
                        + "');\">"
                        + x[1].strip()
                        + "</button>"
                    )
                html += "</div>"

                dropdown.innerHTML = html
                menu_btn.replaceWith(dropdown)
            return
    datatable.hideColumn("state")
    menu_btn.style.display = "none"


# =============================================================================
# Datatable button definitions
# =============================================================================


def datatable_buttons(obj):
    """Return button definitions for the Bootstrap Table toolbar.

    Provides 'select' (toggle checkboxes) and 'menu' (dropdown actions)
    button configurations.
    """
    return {
        "select": {
            "text": "Select rows",
            "icon": "fa-check",
            "event": {
                "click": on_check_toggle_visibility,
            },
            "attributes": {"title": "Add a new row to the table"},
        },
        "menu": {
            "text": "Menu",
            "icon": "fa-bars",
            "attributes": {
                "title": "Menu",
                "style": "display: none;",
            },
        },
    }


window.datatable_buttons = datatable_buttons
