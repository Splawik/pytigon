APPLICATION_TEMPLATE = 'standard'

#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

RET_BUFOR = None
RET_OBJ = None

IS_POPUP = False
SUBWIN = False
LANG = "en"
MENU = None
ACTIVE_PAGE = None
PUSH_STATE = True
BASE_PATH = None
WAIT_ICON = None

import page
import tabmenuitem
import tabmenu
import popup
import scrolltbl
import tbl
import schclient
import tools


def fragment_init(elem=None):
    nonlocal ACTIVE_PAGE
    if elem:
        elem2 = elem
    else:
        elem2 = ACTIVE_PAGE.page

    elem2.find('.dateinput').datetimepicker({ 'pickTime': False, 'format': "YYYY-MM-DD", 'language': LANG })
    elem2.find('.datetimeinput').datetimepicker({'format': "YYYY-MM-DD hh:mm", 'language': 'pl'})


def page_init(id):
    table_type = get_table_type(jQuery('#'+ id))

    paginator = get_page(jQuery('#'+ id)).find('.pagination')
    if paginator.length>0:
        paginate = True
        pg = ACTIVE_PAGE.page.find('.pagination')
        totalPages = pg.attr('totalPages')
        options = {
            'totalPages': totalPages,
            'visiblePages': 3, 'first': '<<', 'prev': '<', 'next': '>', 'last': '>>',
            'onPageClick':def(event, page):
                form = pg.closest('form')
                if form:
                    def _on_new_page(data):
                        pg.closest('.content').find(".tabsort tbody").html(jQuery(jQuery.parseHTML(data)).find(".tabsort tbody").html())
                    jQuery.ajax({'type': "POST", 'url': pg.attr('href').replace('[[page]]', page)+'&hybrid=1', 'data': form.serialize(), 'success': _on_new_page })
        }
        pg.twbsPagination(options)
    else:
        paginate = False

    set_table_type(table_type, '#'+ id + ' .tabsort', paginate)
    jQuery('#'+ id + " a" ).on( "click",
        def(e):
            nonlocal ACTIVE_PAGE
            if jQuery(this).hasClass( "menu-href" ) or (jQuery(this).attr('href') and '/admin/' in jQuery(this).attr('href')):
                e.preventDefault()
                href = jQuery(this).attr("href")
                jQuery.ajax({'type': "GET", 'url': href, 'success': def(data):
                    if APPLICATION_TEMPLATE == 'modern':
                        ACTIVE_PAGE.page.html(data)
                        ACTIVE_PAGE.set_href(href)
                        page_init(ACTIVE_PAGE.id)
                    else:
                        jQuery('#body_body').html(data)
                })
                popup_init()
    )
    fragment_init()


def popup_init():
    nonlocal WAIT_ICON
    ACTIVE_PAGE.page.find('a.popup').click(_on_popup)
    ACTIVE_PAGE.page.find('a.popup_info').click(_on_popup_info)
    ACTIVE_PAGE.page.find('a.popup_delete').click(_on_popup_delete)


    ACTIVE_PAGE.page.find('form').attr('target', '_blank')
    ACTIVE_PAGE.page.find('form').submit(
        def(e):
            nonlocal ACTIVE_PAGE, WAIT_ICON

            data = jQuery(this).serialize()
            console.log(data)
            if 'pdf=on' in data:
                return True
            if 'odf=on' in data:
                return True

            e.preventDefault()

            submit_button = jQuery(this).find('button[type="submit"]')
            if submit_button.length > 0:
                WAIT_ICON = Ladda.create(submit_button[0])
                WAIT_ICON.start()

            jQuery(this).find('input[type="submit"]')

            href = jQuery(this).attr("action")
            if href:
                if '?' in href and not hybrid in href:
                    href2 = href + '&hybrid=1'
                else:
                    href2 = href + '?hybrid=1'
                jQuery(this).attr('action', href2)

            ajax_submit(jQuery(this), def(data):
                nonlocal ACTIVE_PAGE, WAIT_ICON
                ACTIVE_PAGE.page.html(data)
                popup_init()
                if WAIT_ICON:
                    WAIT_ICON.stop()
            )
    )


def global_init():
    jQuery('div.dialog-form').on('hide.bs.modal',
        def(e):
            nonlocal IS_POPUP
            IS_POPUP = False
            jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>")
    )


#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
def _on_menu_href(elem, title=None):
    nonlocal WAIT_ICON
    if APPLICATION_TEMPLATE != 'traditional':
        if not title:
            title = jQuery.trim(jQuery(elem).text())
        menu = get_menu()
        classname = jQuery(elem).attr("class")
        if classname and 'btn' in classname:
            if WAIT_ICON:
                WAIT_ICON.stop()
            WAIT_ICON = Ladda.create(elem)
        else:
            WAIT_ICON = None

        if APPLICATION_TEMPLATE == 'modern' and menu.is_open(title):
            menu.activate(title)
        else:
            href = jQuery(elem).attr("href")
            if '?' in href:
                href2 = href + '&hybrid=1'
            else:
                href2 = href + '?hybrid=1'
            def _on_new_win(data):
                nonlocal href, href2, title, WAIT_ICON

                if APPLICATION_TEMPLATE == 'modern':
                    id = menu.new_page(title, data, href)
                else:
                    jQuery('#body_body').html(data)
                    ACTIVE_PAGE = Page(0, jQuery('#body_body'))
                    ACTIVE_PAGE.set_href(href2)
                    #menu.on_new_page('body_body')
                    page_init('body_body')
                    if PUSH_STATE:
                        history_push_state(title, href)

                popup_init()
                if WAIT_ICON:
                    WAIT_ICON.stop()
                    WAIT_ICON = None

            if APPLICATION_TEMPLATE == 'standard' and 'btn' in classname:
                jQuery('a.menu-href').removeClass('btn-warning').addClass('btn-info')
                jQuery(elem).removeClass('btn-info').addClass('btn-warning')
            if WAIT_ICON:
                WAIT_ICON.start()
            jQuery.ajax({'type': "GET", 'url': href2, 'success': _on_new_win })
            jQuery(elem).closest('.dropdown-menu').dropdown('toggle')
            jQuery('.navbar-ex1-collapse').collapse('hide')
        return False


def jquery_init(application_template, menu_id, lang, base_path):
    nonlocal APPLICATION_TEMPLATE, LANG, BASE_PATH
    APPLICATION_TEMPLATE = application_template
    LANG = lang
    BASE_PATH = base_path
    if IS_POPUP:
        SUBWIN = True
    else:
        SUBWIN = False

    if not SUBWIN:
        jQuery(def ():
            jQuery("#menu_tabs").tabs()
            if APPLICATION_TEMPLATE != 'traditional':
                jQuery("#tabs a:eq(1)").tab('show')
            else:
                jQuery('#tabs a:eq('+ menu_id + ')').tab('show')
            jQuery('a.menu-href').click(
                def(e):
                    e.preventDefault()
                    _on_menu_href(this)
            )
        )


def _on_error(request, settings):
    nonlocal WAIT_ICON
    if WAIT_ICON:
        WAIT_ICON.stop()
        WAIT_ICON = None

    start = settings.responseText.indexOf("<body>")
    end = settings.responseText.lastIndexOf("</body>")
    if start > 0 and end > 0:
        jQuery("#dialog-data-error").html(settings.responseText.substring(start+6,end-1))
        jQuery('#dialog-form-error').modal()
    else:
        jQuery("#dialog-data-error").html(settings.responseText)
        jQuery('#dialog-form-error').modal()


def jquery_ready():
    nonlocal ACTIVE_PAGE, BASE_PATH

    jQuery(document).ajaxError(_on_error)
    global_init()

    if APPLICATION_TEMPLATE == 'traditional':
        ACTIVE_PAGE = Page(0, jQuery('#body_body'))

        page_init('body_body')
    else:
        if APPLICATION_TEMPLATE == 'modern':
            txt  = jQuery('#body_body').text()
            txt2 = jQuery.trim(txt)
            if txt2:
                txt = jQuery.trim(jQuery('#body_body').html())
                jQuery('#body_body').html("")
                menu = get_menu()
                menu.new_page(jQuery('title').text(), txt, BASE_PATH)
        else:
            ACTIVE_PAGE = Page(0, jQuery('#body_body'))
            page_init('body_body')


window.addEventListener('popstate',
    def(e):
        nonlocal PUSH_STATE
        if e.state:
            PUSH_STATE = False
            if APPLICATION_TEMPLATE == 'modern':
                menu = get_menu().activate(e.state, False)
            else:
                alert("x1")
                jQuery('#body_body').html(event.state)
                ACTIVE_PAGE = Page(0, jQuery('#body_body'))
                ACTIVE_PAGE.set_href(href2)
                #menu.on_new_page('body_body')
                page_init('body_body')
            PUSH_STATE = True
,False)


def history_push_state(title, url, data=None):
    url2 = url.split("?")[0]
    if data:
        window.history.pushState(data, title, url2)
    else:
        window.history.pushState(title, title, url2)
