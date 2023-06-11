# from pytigon_js.tools import (
#    ajax_post,
#    ajax_post,
#    get_table_type,
#    load_js,
# )

# from pytigon_js.ajax_region import refresh_ajax_frame


def _is_visible(element):
    test = RawJS('jQuery(element).is(":visible")')
    if test:
        return True
    else:
        return False


def old_datetable_set_height(element):

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
        dydy = (
            # int(elem[0].getAttribute("table-details-height").replace("%", "").replace("vh", ""))
            details_height
            * dy_win
            / 100
        )

    dy -= dydy

    if dy < 200:
        dy = 200

    panel = elem.find(".fixed-table-toolbar")
    if not _is_visible(panel):
        dy += panel.outerHeight() + 5  # height() #- 15

    jQuery(element).bootstrapTable("resetView", {"height": dy - 5})


def datetable_set_height(element):

    # if jQuery(element).hasClass("table_get"):
    #    return
    if not _is_visible(element):
        return

    elem = jQuery(element).closest(".tabsort_panel")

    # table_offset = elem.offset().top
    dy = elem.parent().height()

    if dy < 200:
        dy = 200

    panel = elem.find(".fixed-table-toolbar")
    if not _is_visible(panel):
        dy += panel.outerHeight() + 5  # height() #- 15

    jQuery(element).bootstrapTable("resetView", {"height": dy - 10})


def datatable_refresh(element):
    if element.classList.contains("tabsort"):
        jQuery(element).bootstrapTable("refresh")
    else:
        region = get_ajax_region(element, "table")
        if region != None:
            jQuery(region).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
            )


window.datatable_refresh = datatable_refresh


def _rowStyle(value, row, index):
    x = jQuery("<div class='cid'>" + value["cid"] + "</div>").find("div.td_information")
    if x.length > 0:
        c = x.attr("class").replace("td_information", "").replace(" ", "")
        if c.length > 0:
            return {"classes": c}
    return {}


def prepare_datatable(table):
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
    refr_block = table.closest(".ajax-frame")
    if refr_block:
        tables = Array.prototype.slice.call(
            refr_block[0].querySelectorAll("div.fixed-table-header table.tabsort")
        )
        for table in tables:
            table.classList.remove("flexible_size")


def datatable_ajax(params):
    url = params["url"]
    success = params["success"]
    if "form" in dict(params["data"]):
        form = params["data"]["form"]
        del params["data"]["form"]
        d = jQuery.param(params["data"])
        url += "?" + d

        def _on_post_data(data):
            d2 = JSON.parse(data)
            print("POST:", data)
            success(d2)

        ajax_post(url, form, _on_post_data)

    else:
        d = jQuery.param(params["data"])
        url += "?" + d

        def _on_get_data(data):
            d2 = JSON.parse(data)
            print("GET:", data)
            success(d2)

        ajax_get(url, _on_get_data)


def init_table(table, table_type):
    if table_type == "datatable":
        if table.hasClass("multiple-select"):
            jQuery(table).find("tr:first").find("th:first").before(
                "<th data-field='state' data-checkbox='true' data-visible='true'></th>"
            )
        else:
            jQuery(table).find("tr:first").find("th:first").before(
                "<th data-field='state' data-checkbox='true' data-visible='false'></th>"
            )

        jQuery(table).find("tr:first").find("th:last").after(
            "<th data-field='id' data-visible='false'>ID</th>"
        )

        def onLoadSuccess(data):
            nonlocal table
            prepare_datatable(table)

            def _pagination():
                nonlocal table
                jQuery(table).closest(".fixed-table-container").find(
                    ".fixed-table-pagination ul.pagination a"
                ).addClass("page-link")
                # datatable_onresize()

            setTimeout(_pagination, 0)
            return False

        def onPostHeader(data):
            nonlocal table
            prepare0(table)
            return False

        def onCheck(row, elem):
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

                        x.querySelector(".table-row-active")

        def queryParams(p):
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
            nonlocal table
            if table[0].hasAttribute("data-autoselect"):
                table[0].closest(".bootstrap-table").querySelector(
                    "[name='select']"
                ).click()

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

        # table_panel = jQuery(table).closest(".content")
        table_panel = jQuery(table).closest("div.win-content")
        btn = table_panel.find(".tabsort-toolbar-expand").first()
        if btn:

            def _handle_toolbar_expand(self, elem):
                panel = table_panel.find(".fixed-table-toolbar").first()
                panel2 = table_panel.find(".list_content_header_second_row").first()
                if not jQuery(this).hasClass("active"):
                    # if panel[0].style.display == "none":
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
                # datatable_onresize()

        def _process_resize(size_object):
            nonlocal table
            datetable_set_height(table[0])

        table[0].process_resize = _process_resize


window.init_table = init_table


def table_loadeddata(event):
    if getattr(event, "data"):
        dt = data_type(event.data)
        if dt in ("$$RETURN_REFRESH_PARENT", "$$RETURN_REFRESH"):
            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
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
                    print(url)
                    if "?" in url:
                        url += "&json=1&pk=" + str(pk)
                    else:
                        url += "?&json=1&pk=" + str(pk)
                    url = url.replace("/form/", "/json/")

                    def _update(data):
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
                                    datatable.bootstrapTable("refresh")
                        except:
                            datatable.bootstrapTable("refresh")

                    ajax_get(url, _update)
                    return
            except:
                pass

            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
            )
        elif dt in ("$$RETURN_OK",):
            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
            )
        else:
            refresh_ajax_frame(
                event.srcElement if event.srcElement else event.data_source,
                "page",
                event.data,
            )
    else:
        jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
            "refresh"
        )


window.table_loadeddata = table_loadeddata


def loading_template(message):
    return '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>'


window.loading_template = loading_template


def datatable_action(btn, action):
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
        jQuery(datatable).bootstrapTable("refresh")

    ajax_json(url + "?pks=" + pk_list_str, {"action": action}, _callback)


window.datatable_action = datatable_action


def on_check_toggle_visibility():
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
                    # html += "<a class ='dropdown-item' href=../action/?'" + x[0] + "' target='" + x[2] + "'>" + x[1] + "</a>"
                html += "</div>"

                dropdown.innerHTML = html
                menu_btn.replaceWith(dropdown)
            return
    datatable.hideColumn("state")
    menu_btn.style.display = "none"


# def on_menu():
#    datatable = this
#    alert(datatable)


def datatable_buttons(obj):
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
            #'event': {
            #    'click': on_menu,
            # },
            "attributes": {
                "title": "Menu",
                "style": "display: none;",
            },
        },
    }


window.datatable_buttons = datatable_buttons
