from pytigon_js.tools import history_push_state, corect_href, remove_element, process_resize
from pytigon_js.ajax_region import mount_html

class Page:
    def __init__(self, id, page):
        self.id = id
        self.page = page

    def set_href(self, href):
        self.page.attr('_href', href)

    def get_href(self):
        return self.page.attr('_href')

class TabMenuItem:
    def __init__(self, id, title, url, data=None):
        self.id = id
        self.title = jQuery.trim(title)
        self.url = url
        self.data = data

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
        jQuery(sprintf("#li_%s a", menu_item.id)).tab("show")
        if push_state and window.PUSH_STATE:
            history_push_state(menu_item.title, menu_item.url)

    def register(self, title):
        self.titles[title] = "$$$"

    def new_page(self, title, data_or_html, href, title_alt=None):
        _id = "tab" + self.id

        menu_item = TabMenuItem(_id, title, href, data_or_html)
        self.titles[title] = menu_item
        if title_alt and title_alt != title:
            self.titles[title_alt] = menu_item
        menu_pos = vsprintf(
            "<li id='li_%s' class ='nav-item'><a href='#%s' class='nav-link bg-info' data-toggle='tab' role='tab' title='%s'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-outline-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>",
            [_id, _id, title, title, _id],
        )

        append_left = jQuery("#tabs2").hasClass("append-left")

        if append_left:
            jQuery("#tabs2").prepend(menu_pos)
        else:
            jQuery("#tabs2").append(menu_pos)
        jQuery("#tabs2_content").append(
            sprintf(
                "<div class='tab-pane container-fluid ajax-region ajax-frame win-content page' id='%s'></div>",
                _id,
            )
        )

        window.ACTIVE_PAGE = Page(_id, jQuery("#" + _id))
        self.active_item = menu_item

        if window.PUSH_STATE:
            history_push_state(title, href)

        def _on_show_tab(e):
            nonlocal menu_item
            window.ACTIVE_PAGE = Page(_id, jQuery("#" + _id), menu_item)

            menu = get_menu()
            menu_item = menu.titles[jQuery.trim(e.target.text)]
            self.active_item = menu_item
            if window.PUSH_STATE:
                history_push_state(menu_item.title, menu_item.url)

            process_resize(document.getElementById(menu_item.id))

        if append_left:
            jQuery("#tabs2 a:first").on("shown.bs.tab", _on_show_tab)
            jQuery("#tabs2 a:first").tab("show")
        else:
            jQuery("#tabs2 a:last").on("shown.bs.tab", _on_show_tab)
            jQuery("#tabs2 a:last").tab("show")

        mount_html(document.getElementById(_id), data_or_html, None)

        def _on_button_click(event):
            get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""))

        jQuery(sprintf("#button_%s", _id)).click(_on_button_click)

        scripts = jQuery("#" + _id + " script")

        def _local_fun(index, element):
            eval(this.innerHTML)

        scripts.each(_local_fun)
        self.id += 1

        return _id

    def remove_page(self, id):
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
                window.init_start_wiki_page()
            jQuery("#body_desktop").show()


    #'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
    def on_menu_href(self, elem, data_or_html, title, title_alt=None, url=None):
        if window.APPLICATION_TEMPLATE == "modern":
            if self.is_open(title):
                self.activate(title)
            else:
                self.register(title)
                if url:
                    href = url
                else:
                    href = jQuery(elem).attr("href")
                href2 = corect_href(href)

                jQuery("#body_desktop").hide()
                self.new_page(title, data_or_html.innerHTML, href2, title_alt)

            jQuery(".auto-hide").trigger("click")
            return False
        else:
            mount_html(document.querySelector("#body_desktop"), data_or_html, None)
            jQuery(".auto-hide").trigger("click")
            return False

def get_menu():
    if not window.MENU:
        window.MENU = TabMenu()
    return window.MENU
