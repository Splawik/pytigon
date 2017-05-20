__pragma__ ('alias', 'jquery_is', 'is')

from scrolltbl import stick_header
from tools import ajax_post, ajax_post


def datetable_set_height():
    if jQuery(this).hasClass('table_get'):
        return
    if not jQuery(this).jquery_is(':visible'):
        return

    elem = jQuery(this).closest(".tabsort_panel")

    table_offset = elem.offset().top
    dy_win = jQuery(window).height()

    dy = dy_win - table_offset

    if dy<200: dy = 200

    jQuery(this).bootstrapTable("resetView", {"height": dy-10})


def datatable_refresh(table):
    table.bootstrapTable('refresh')


def _rowStyle(value, row, index):
    x = jQuery("<div>"+value['cid']+"</div>").find("div.td_information")
    if x.length > 0:
        c = x.attr('class').replace('td_information', '')
        if c.length>0:
            return { 'classes': c, }
    return {}


def prepare_datatable(table):
    def _local_fun(index ):
        td = jQuery(this).parent()
        tr = td.parent()
        l = tr.find('td').length
        tr.find("td:gt(0)").remove()
        td.attr('colspan', l)
    table.find('div.second_row').each(_local_fun)

def datatable_ajax(params):
    url = params['url']
    success = params['success']
    if 'form' in dict(params['data']):
        form = params['data']['form']
        del params['data']['form']
        d = jQuery.param(params['data'])
        url += '?' + d

        def _on_post_data(data):
            d2 = JSON.parse(data)
            success(d2)
        ajax_post(url, form, _on_post_data)

    else:
        d = jQuery.param(params['data'])
        url += '?' + d

        def _on_get_data(data):
            d2 = JSON.parse(data)
            success(d2)
        ajax_get(url, _on_get_data)


def init_table(table, table_type):
    if table_type == 'scrolled':
        stick_header()
    if table_type == 'datatable':
        def onLoadSuccess(data):
            prepare_datatable(table)
            datatable_onresize()
            return False
        
        def queryParams(p):
            refr_block = jQuery(table).closest('.refr_object')
            src = refr_block.find('.refr_source')
            if src.length > 0 and src.prop("tagName") == 'FORM':
                p['form'] = src.serialize()
            return p
        
        if table.hasClass('table_get'):
            table.bootstrapTable({'onLoadSuccess': onLoadSuccess, 'height': 350, 'rowStyle': _rowStyle,  'queryParams': queryParams,  'ajax': datatable_ajax })
        else:
            table.bootstrapTable({'onLoadSuccess': onLoadSuccess, 'rowStyle': _rowStyle, 'queryParams': queryParams, 'ajax': datatable_ajax })

def datatable_onresize():
    jQuery('.datatable:not(.table_get)').each(datetable_set_height)
