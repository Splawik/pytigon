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


def datetable_set_height(element):

    if jQuery(element).hasClass("table_get"):
        return
    if not _is_visible(element):
        return

    elem = jQuery(element).closest(".tabsort_panel")

    table_offset = elem.offset().top
    dy_win = jQuery(window).height()

    dy = dy_win - table_offset

    if dy < 200:
        dy = 200

    panel = elem.find(".fixed-table-toolbar")
    if not _is_visible(panel):
        dy += panel.height() - 15

    jQuery(element).bootstrapTable("resetView", {"height": dy - 5})


def datatable_refresh(table):
    table.bootstrapTable("refresh")


def _rowStyle(value, row, index):
    x = jQuery("<div>" + value["cid"] + "</div>").find("div.td_information")
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
            jQuery(table).find("tr:first").find('th:first').before("<th data-field='state' data-checkbox='true' data-visible='true'></th>")
        else:
            jQuery(table).find("tr:first").find('th:first').before("<th data-field='state' data-checkbox='true' data-visible='false'></th>")

        jQuery(table).find("tr:first").find('th:last').after("<th data-field='id' data-visible='false'>ID</th>")

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

        def queryParams(p):
            nonlocal table
            link = get_ajax_link(table[0], "page")
            if link and link.tagName.lower()=='form':
                p["form"] = jQuery(link).serialize()
            return p
            #refr_block = jQuery(table).closest(".ajax-frame")
            #src = refr_block.find(".ajax-link")
            #if src.length > 0 and src.prop("tagName") == "FORM":
            #    p["form"] = src.serialize()
            #return p

        icons = {
            'fullscreen': 'fa-arrows-alt',
            'refresh': 'fa-refresh',
            'toggleOff': 'fa-toggle-off',
            'toggleOn': 'fa-toggle-on',
            'columns': 'fa-th-list',
        }

        if table.hasClass("table_get"):
            table.bootstrapTable(
                {
                    "onLoadSuccess": onLoadSuccess,
                    "onPostHeader": onPostHeader,
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
                    "rowStyle": _rowStyle,
                    "queryParams": queryParams,
                    "ajax": datatable_ajax,
                    "icons": icons,
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

        table_panel = jQuery(table).closest(".content")
        btn = table_panel.find(".tabsort-toolbar-expand")
        if btn:

            def _handle_toolbar_expand(self, elem):
                panel = table_panel.find(".fixed-table-toolbar")
                panel2 = jQuery(".list_content_header_two_row")
                if jQuery(this).hasClass("active"):
                    panel.show()
                    panel2.show()
                else:
                    panel.hide()
                    panel2.hide()
                process_resize(document.body)

            table_panel.on("click", ".tabsort-toolbar-expand", _handle_toolbar_expand)
            if btn.hasClass("active"):
                panel = table_panel.find(".fixed-table-toolbar")
                panel2 = jQuery(".list_content_header_two_row")
                panel.hide()
                panel2.hide()
                # datatable_onresize()

        def _process_resize(size_object):
            nonlocal table
            datetable_set_height(table[0])

        table[0].process_resize = _process_resize


def table_loadeddata(event):
    if getattr(event, "data"):
        dt = data_type(event.data)
        if dt in ("$$RETURN_REFRESH_PARENT", "$$RETURN_REFRESH"):
            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
            )
        elif dt == "$$RETURN_ERROR":
            refresh_ajax_frame(event.data_source if event.data_source else event.srcElement , "error", event.data)
        elif dt in ("$$RETURN_UPDATE_ROW_OK", "$$RETURN_NEW_ROW_OK"):
            try:
                if isinstance(event.data, str):
                    _data = event.data
                else:
                    _data = event.data.innerHTML
                pk = int(_data.split('id:')[1].strip())
                table = event.data_source if event.data_source else event.srcElement
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
                    if '?' in url:
                        url += "&pk=" + str(pk)
                    else:
                        url += "?pk=" + str(pk)
                    url = url.replace('/form/', '/json/')
                    def _update(data):
                        nonlocal datatable, dt
                        d = JSON.parse(data)
                        if dt == "$$RETURN_NEW_ROW_OK":
                            datatable.bootstrapTable('append', d['rows'][0])
                            datatable.bootstrapTable('scrollTo', 'bottom')
                        else:
                            id2 = d['rows'][0]['id']
                            datatable.bootstrapTable('updateByUniqueId', {'id': id2, 'row': d['rows'][0]})
                    ajax_get(url, _update)
                    return
            except:
                pass

            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
            )
        elif dt in (
                "$$RETURN_OK",
            ):
            jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
                "refresh"
            )
        else:
            refresh_ajax_frame(event.data_source if event.data_source else event.srcElement, "page", event.data)
    else:
        jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable(
            "refresh"
        )


window.table_loadeddata = table_loadeddata


def loading_template(message):
    return '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>'

window.loading_template = loading_template
