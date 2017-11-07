def stick_resize():
    tbl = window.ACTIVE_PAGE.page.find(".tbl_scroll")
    if tbl.length>0:
        tbl2 = jQuery(tbl[0])
        if tbl2.closest('.tabsort').length>0:
            return
        dy_table = tbl.offset().top
        dy_win = dy_win = jQuery(window).height()
        dy = dy_win - dy_table
        if dy<100: dy = 100
        tbl2.height(dy-35)


def resize_win():
    stick_resize()
    tab2 = []
    tabs = window.ACTIVE_PAGE.page.find("table[name='tabsort']")
    if tabs.length > 0:
        first_tab_on_page = jQuery(tabs[0])
        tab_width = jQuery(first_tab_on_page).width()
        jQuery(first_tab_on_page.find(".tbl_header")[0]).width(tab_width)

        def _local_fun():
            tab2.push(jQuery(this).width())
        first_tab_on_page.find("tr:first td").each(_local_fun)

        tab2 = tab2.reverse()

        def _local_fun2():
            jQuery(this).width(tab2.pop())
        first_tab_on_page.find(".tbl_header:first th").each(_local_fun2)


def stick_header(tbl):
    tab = []
    tab2 = []

    def _local_fun():
        tab.push(jQuery(this).width())
    tbl.find("table.tabsort th").each(_local_fun)

    table = jQuery('<table class="tabsort tbl_header" style="overflow-x: hidden;"></table>')
    table.append(tbl.find("table.tabsort thead") )

    tbl.find('.tbl_scroll').before(table)

    def _local_fun2():
        tab2.push(jQuery(this).width())

    tbl.find(".tbl_header th").each(_local_fun2)

    tab2 = tab2.reverse()

    def _local_fun3():
        x = tab2.pop()
        if x > jQuery(this).width():
            jQuery(this).css("min-width", x)
    tbl.find("table[name='tabsort'] tr:first td").each(_local_fun3)

    tab = tab.reverse()

    def _local_fun4():
        jQuery(this).width(tab.pop())
    tbl.find(".tbl_header th").each(_local_fun4)

    jQuery(window).resize(resize_win)

    resize_win()


window.icons = {
    'refresh': 'fa-refresh',
    'toggle': 'fa-toggle-on fa-lg',
    'columns': 'fa-th-list',
    'detailOpen': 'fa-plus-square',
    'detailClose': 'fa-minus-square'
}

