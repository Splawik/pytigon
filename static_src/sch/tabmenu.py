from page import Page
from tabmenuitem import TabMenuItem
from tbl import datatable_onresize
from tools import history_push_state

class TabMenu:
    def __init__(self):
        self.id = 0
        self.titles = {}
        self.active_item = None

    def get_active_item(self):
        return self.active_item

    def is_open(self, title):
        if self.titles and title in self.titles and self.titles[title]:
            return True
        else:
            return False

    def activate(self, title, push_state=True):
        menu_item = self.titles[title]
        jQuery(sprintf('#li_%s a', menu_item.id)).tab('show')
        if push_state and window.PUSH_STATE:
            history_push_state(menu_item.title, menu_item.url)
        datatable_onresize()

    def new_page(self, title, data, href, riot_init, page_init):
        _id = "tab" + self.id
        title2 = jQuery.trim(title)
        menu_item = TabMenuItem(_id, title2, href, data)
        self.titles[title2] = menu_item

        jQuery('#tabs2').append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-raised btn-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", [_id, _id, title2, _id]))
        jQuery('#tabs2_content').append(sprintf("<div class='tab-pane' id='%s'></div>", _id) )

        window.ACTIVE_PAGE = Page(_id, jQuery('#'+_id))
        self.active_item = menu_item

        jQuery('#'+_id).html(data)

        if window.PUSH_STATE:
            history_push_state(title2, href)


        def _on_show_tab(e):
            nonlocal menu_item
            window.ACTIVE_PAGE = Page(_id, jQuery('#'+_id), menu_item)

            menu = get_menu()
            menu_item = menu.titles[jQuery.trim(e.target.text)]
            self.active_item = menu_item
            if window.PUSH_STATE:
                history_push_state(menu_item.title, menu_item.url)
        jQuery('#tabs2 a:last').on('shown.bs.tab', _on_show_tab)

        jQuery('#tabs2 a:last').tab('show')

        page_init(_id, False)


        def _on_button_click(event):
            get_menu().remove_page(jQuery(this).attr('id').replace('button_',''))

        jQuery(sprintf('#button_%s', _id)).click(_on_button_click)

        scripts = jQuery('#'+_id+' script')

        def _local_fun( index, element ):
            eval(this.innerHTML)

        scripts.each(_local_fun)
        self.id += 1

        return _id


    def remove_page(self, id):

        def _local_fun(index, value):
            if value and value.id == id:
                self.titles[index] = None

        jQuery.each(self.titles, _local_fun)
        jQuery(sprintf('#li_%s', id) ).remove()
        jQuery(sprintf('#%s', id)).remove()
        jQuery('#tabs2 a:last').tab('show')


def get_menu():
    if not window.MENU:
        window.MENU = TabMenu()
    return window.MENU