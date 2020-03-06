from tools import corect_href, ajax_get, mount_html
from popup import refresh_fragment
from tabmenu import get_menu


def get_value(elem, name):
    if elem.length > 0:
        x = elem.closest('.refr_object')
        if x.length > 0:
            x2 = x.find(sprintf("[name='%s']", name))
            if x2.length > 0:
                return x2.val()
    return "[[ERROR]]"

def process_href(href, elem):
    ret = []
    if '[[' in href and ']]' in href:
        x1 = href.split('[[')
        process = False
        for pos in x1:
            if process:
                if ']]' in pos:
                    x2 = pos.split(']]', 1)
                    value = get_value(elem, x2[0])
                    if value and value != "None":
                        ret.append(value+x2[1])
                    else:
                        ret.append(x2[1])
                else:
                    ret.append(pos)
                process = False
            else:
                ret.append(pos)
                process = True
        return "".join(ret)
    else:
        return href

window.process_href = process_href

def process_on_click(event_tab, elem=None):
    def _on_click(e):
        nonlocal event_tab

        target = jQuery(e.currentTarget).attr('target')
        if target == "_blank" or target == '_parent':
            return True

        src_obj = jQuery(this)

        if 'xlink:href' in e.currentTarget.attributes:
            href = jQuery(this).attr('xlink:href')
        else:
            href = jQuery(this).attr("href")

        if href and '#' in href:
            return True

        if not href:
            return True

        href = process_href(href, src_obj)

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
                    if window.ACTIVE_PAGE:
                        mount_html(window.ACTIVE_PAGE.page, data)
                    else:
                        mount_html(jQuery('#wiki_start'), data)
                        return
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
        jQuery('#body_body').on("click", "a", _on_click)
        jQuery('#wiki_start').on("click", "a", _on_click)
