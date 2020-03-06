__pragma__("alias", "jquery_is", "js_is")

from tools import (
    ajax_post,
    ajax_post,
    register_fragment_init_fun,
    get_table_type,
    load_js,
    mount_html,
)


def datetable_set_height():

    if jQuery(this).hasClass("table_get"):
        return
    if not jQuery(this).jquery_is(":visible"):
        return

    elem = jQuery(this).closest(".tabsort_panel")

    table_offset = elem.offset().top
    dy_win = jQuery(window).height()

    dy = dy_win - table_offset

    if dy < 200:
        dy = 200

    panel = elem.find(".fixed-table-toolbar")
    if not panel.jquery_is(":visible"):
        dy += panel.height() - 15

    jQuery(this).bootstrapTable("resetView", {"height": dy - 5})


def datatable_refresh(table):
    table.bootstrapTable("refresh")


def _rowStyle(value, row, index):
    x = jQuery("<div>" + value["cid"] + "</div>").find("div.td_information")
    if x.length > 0:
        c = x.attr("class").replace("td_information", "")
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
            success(d2)

        ajax_post(url, form, _on_post_data)

    else:
        d = jQuery.param(params["data"])
        url += "?" + d

        def _on_get_data(data):
            d2 = JSON.parse(data)
            success(d2)

        ajax_get(url, _on_get_data)


def init_table(table, table_type):
    if table_type == "datatable":

        def onLoadSuccess(data):
            prepare_datatable(table)

            def _pagination():
                nonlocal table
                jQuery(table).closest(".fixed-table-container").find(
                    ".fixed-table-pagination ul.pagination a"
                ).addClass("page-link")
                datatable_onresize()

            setTimeout(_pagination, 0)
            return False

        def queryParams(p):
            refr_block = jQuery(table).closest(".refr_object")
            src = refr_block.find(".refr_source")
            if src.length > 0 and src.prop("tagName") == "FORM":
                p["form"] = src.serialize()
            return p

        if table.hasClass("table_get"):
            table.bootstrapTable(
                {
                    "onLoadSuccess": onLoadSuccess,
                    "height": 350,
                    "rowStyle": _rowStyle,
                    "queryParams": queryParams,
                    "ajax": datatable_ajax,
                }
            )
        else:
            table.bootstrapTable(
                {
                    "onLoadSuccess": onLoadSuccess,
                    "rowStyle": _rowStyle,
                    "queryParams": queryParams,
                    "ajax": datatable_ajax,
                }
            )

        table_panel = jQuery(table).closest(".content")
        btn = table_panel.find(".tabsort-toolbar-expand")
        if btn:

            def _handle_toolbar_expand(elem):
                panel = table_panel.find(".fixed-table-toolbar")
                if jQuery(this).hasClass("active"):
                    panel.show()
                    datatable_onresize()
                else:
                    panel.hide()
                    datatable_onresize()

            table_panel.on("click", ".tabsort-toolbar-expand", _handle_toolbar_expand)
            if btn.hasClass("active"):
                panel = table_panel.find(".fixed-table-toolbar")
                panel.hide()
                datatable_onresize()


def content_set_height():
    if not jQuery(this).jquery_is(":visible"):
        return

    if jQuery(this).closest(".tabsort").length > 0:
        return

    if jQuery(this).closest("#dialog-form-modal").length > 0:
        return

    # elem = jQuery(this).findclosest('.tab-pane')
    # content_offset = elem.offset().top
    # content_offset = elem.offset().height()
    # dy_win = jQuery('.desktop_content').height()
    # console.log(content_offset)
    # console.log(dy_win)
    content_offset = jQuery(this).offset().top
    dy_win = jQuery(window).height()

    dy = dy_win - content_offset - 30
    if dy < 200:
        dy = 200

    # console.log(content_offset2)

    jQuery(this).height(dy)


def datatable_onresize():
    jQuery(".datatable:not(.table_get)").each(datetable_set_height)
    jQuery(".content").each(content_set_height)
    jQuery(".content1").each(content_set_height)
    jQuery(".content2").each(content_set_height)


window.datatable_onresize = datatable_onresize


def _on_fragment_init(elem):
    # elem.find('.win-content').bind('resize', datatable_onresize)
    datatable_onresize()
    table_type = get_table_type(elem)
    # if table_type != 'datatable':
    # pg = elem.find('.pagination')
    # paginate = init_pagintor(pg)
    tbl = elem.find(".tabsort")
    if tbl.length > 0:
        init_table(tbl, table_type)
    elem.find('.tree').treegrid()

register_fragment_init_fun(_on_fragment_init)
