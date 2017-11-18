from tools import corect_href, ajax_get, mount_html
from popup import refresh_fragment
from tabmenu import get_menu

def process_on_click(event_tab, elem=None):
    def _on_click(e):
        nonlocal event_tab

        target = jQuery(e.currentTarget).attr('target')
        if target == "_blank" or target == '_parent':
            return True

        src_obj = jQuery(this)

        href = jQuery(this).attr("href")
        if href and '#' in href:
            return True

        for pos in event_tab:
            if pos[0] == '*' or pos[0] == target:
                if pos[1] == '*' or src_obj.hasClass(pos[1]):
                    if pos[3]:
                        url = corect_href(href, True)
                    elif pos[2]:
                        url = corect_href(href, False)
                    else:
                        url = href
                    e.preventDefault()
                    pos[4](url, this, e)
                    return True

        e.preventDefault()

        #if jQuery(e.currentTarget).attr('target') in ("_top", "_top2"):
        #    title = jQuery(e.currentTarget).attr('title')
        #    if not title:
        #        if len(href)>16:
        #            title = '...'+href[-13:]
        #        else:
        #            title = href
        #    return _on_menu_href(this,title)

        href2 = corect_href(href)

        def _on_data(data):
            nonlocal href, src_obj, target

            if (data and "_parent_refr" in data) or target in ("refresh_obj", "refresh_page"):
                if target=="refresh_obj":
                    if not refresh_fragment(src_obj, None, True):
                        refresh_fragment(src_obj)
                else:
                    refresh_fragment(src_obj)
            else:
                if window.APPLICATION_TEMPLATE == 'modern':
                    mount_html(window.ACTIVE_PAGE.page, data)
                    window.ACTIVE_PAGE.set_href(href)
                else:
                    mount_html(jQuery('#body_body'), data)
                window.ACTIVE_PAGE.set_href(href)
                get_menu().get_active_item().url = href
                if window.PUSH_STATE:
                    history_push_state("title", href)
        ajax_get(href2,_on_data)

    if elem:
        elem.on("click", "a", _on_click)
    else:
        jQuery('#tabs2_content').on("click", "a", _on_click)
        jQuery('#dialog-form-modal').on("click", "a", _on_click)
