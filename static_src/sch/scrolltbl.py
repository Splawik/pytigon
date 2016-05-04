def stick_resize():
    tbl = window.ACTIVE_PAGE.page.find(".tbl_scroll")
    if tbl.length>0:
        dy_table = tbl.offset().top
        dy_win = dy_win = jQuery(window).height()
        dy = dy_win - dy_table
        if dy<100: dy = 100
        tbl.height(dy-35)


def resize_win():
    stick_resize()
    tab2 = []
    tab_width = window.ACTIVE_PAGE.page.find("table[name='tabsort']").width()
    window.ACTIVE_PAGE.page.find(".tbl_header").width(tab_width)

    def _local_fun():
        tab2.push(jQuery(this).width())
    window.ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(_local_fun)

    tab2 = tab2.reverse()

    def _local_fun2():
        jQuery(this).width(tab2.pop())
    window.ACTIVE_PAGE.page.find(".tbl_header th").each(_local_fun2)


def stick_header():
    tab = []
    tab2 = []

    def _local_fun():
        tab.push(jQuery(this).width())
    window.ACTIVE_PAGE.page.find("table.tabsort th").each(_local_fun)

    table = jQuery('<table class="tabsort tbl_header" style="overflow-x: hidden;"></table>')
    table.append( window.ACTIVE_PAGE.page.find("table.tabsort thead") )

    window.ACTIVE_PAGE.page.find('.tbl_scroll').before(table)

    def _local_fun2():
        tab2.push(jQuery(this).width())

    window.ACTIVE_PAGE.page.find(".tbl_header th").each(_local_fun2)

    tab2 = tab2.reverse()

    def _local_fun3():
        x = tab2.pop()
        if x > jQuery(this).width():
            jQuery(this).css("min-width", x)
    window.ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(_local_fun3)

    tab = tab.reverse()

    def _local_fun4():
        jQuery(this).width(tab.pop())
    window.ACTIVE_PAGE.page.find(".tbl_header th").each(_local_fun4)

    jQuery(window).resize(resize_win)

    resize_win()


