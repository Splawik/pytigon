#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

APPLICATION_TEMPLATE = 'standard'

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
WAIT_ICON2 = False
MENU_ID = 0
BASE_FRAGMENT_INIT = None

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
    if BASE_FRAGMENT_INIT:
        BASE_FRAGMENT_INIT()


def page_init(id, first_time = True):
    nonlocal WAIT_ICON, WAIT_ICON2, ACTIVE_PAGE
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
                        #page_init(ACTIVE_PAGE.id)
                        fragment_init(pg.closest('.content').find(".tabsort tbody"))

                    jQuery.ajax({'type': "POST", 'url': pg.attr('href').replace('[[page]]', page)+'&hybrid=1', 'data': form.serialize(), 'success': _on_new_page })
        }
        pg.twbsPagination(options)
    else:
        paginate = False

    set_table_type(table_type, '#'+ id + ' .tabsort', paginate)
    if first_time:
        jQuery('#'+ id).on( "click", "a",
            def(e):
                nonlocal ACTIVE_PAGE
                #if jQuery(this).hasClass( "menu-href" ):

                for pos in [ ('popup', on_popup), ('popup_info', on_popup_info), ('popup_delete', on_popup_delete) ]:
                    if jQuery(this).hasClass(pos[0]):
                        pos[1](this)
                        return False

                href = jQuery(this).attr("href")
                if '#' in href:
                    return True

                e.preventDefault()

                href2 = corect_href(href)

                jQuery.ajax({'type': "GET", 'url': href2, 'success': def(data):
                    nonlocal href
                    if APPLICATION_TEMPLATE == 'modern':
                        ACTIVE_PAGE.page.html(data)
                        ACTIVE_PAGE.set_href(href)
                        page_init(ACTIVE_PAGE.id, False)
                    else:
                        jQuery('#body_body').html(data)
                        page_init('body_body', False)
                    ACTIVE_PAGE.set_href(href)
                    get_menu().get_active_item().url = href
                    if PUSH_STATE:
                        history_push_state("title", href)
                })
        )
    ACTIVE_PAGE.page.find('form').attr('target', '_blank')
    ACTIVE_PAGE.page.find('form').submit(
        def(e):
            nonlocal ACTIVE_PAGE, WAIT_ICON, WAIT_ICON2

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
            else:
                WAIT_ICON2 = True
                $('#loading-indicator').show()


            #jQuery(this).find('input[type="submit"]')

            href = jQuery(this).attr("action")
            if href:
                jQuery(this).attr('action', corect_href(href))

            ajax_submit(jQuery(this), def(data):
                nonlocal ACTIVE_PAGE, WAIT_ICON, WAIT_ICON2, id
                ACTIVE_PAGE.page.html(data)
                page_init(id, False)
                if WAIT_ICON:
                    WAIT_ICON.stop()
                if WAIT_ICON2:
                    $('#loading-indicator').hide()
                    WAIT_ICON2 = False
            )
    )
    fragment_init(ACTIVE_PAGE.page)


def app_init(application_template, menu_id, lang, base_path, base_fragment_init):
    nonlocal APPLICATION_TEMPLATE, LANG, BASE_PATH, BASE_FRAGMENT_INIT
    APPLICATION_TEMPLATE = application_template
    LANG = lang
    BASE_PATH = base_path
    BASE_FRAGMENT_INIT = base_fragment_init
    if IS_POPUP:
        SUBWIN = True
    else:
        SUBWIN = False

    if not SUBWIN:
        jQuery(def ():
            nonlocal menu_id
            jQuery("#menu_tabs").tabs()
            if APPLICATION_TEMPLATE != 'traditional':
                jQuery("#tabs a:eq(1)").tab('show')
            else:
                jQuery('#tabs a:eq('+ menu_id + ')').tab('show')

            jQuery('body').on('click', 'a.menu-href',
                def(e):
                    if APPLICATION_TEMPLATE != 'traditional':
                        e.preventDefault()
                        _on_menu_href(this)
            )

            jQuery('body').on('submit', 'form.DialogForm',
                def(e):
                    e.preventDefault()
                    on_edit_ok($(this))
            )

        )


#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
def _on_menu_href(elem, title=None):
    nonlocal WAIT_ICON, WAIT_ICON2
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
            href2 = corect_href(href)
            def _on_new_win(data):
                nonlocal href, href2, title, WAIT_ICON, WAIT_ICON2, MENU_ID

                if APPLICATION_TEMPLATE == 'modern':
                    id = menu.new_page(title, data, href)
                else:
                    jQuery('#body_body').html(data)
                    ACTIVE_PAGE = Page(0, jQuery('#body_body'))
                    ACTIVE_PAGE.set_href(href2)
                    page_init('body_body', False)
                    if PUSH_STATE:
                        id = jQuery(elem).attr('id')
                        if not id:
                            id = 'menu_id_' + MENU_ID
                            MENU_ID = MENU_ID + 1
                            jQuery(elem).attr('id', id)
                        history_push_state(title, href, [data, id])

                if WAIT_ICON:
                    WAIT_ICON.stop()
                    WAIT_ICON = None

                if WAIT_ICON2:
                    $('#loading-indicator').hide()
                    WAIT_ICON2 = False

            if APPLICATION_TEMPLATE == 'standard' and 'btn' in classname:
                #jQuery('a.menu-href').removeClass('btn-warning').addClass('btn-info')
                #jQuery(elem).removeClass('btn-info').addClass('btn-warning')

                jQuery('a.menu-href').removeClass('btn-warning')
                jQuery(elem).addClass('btn-warning')

            if WAIT_ICON:
                WAIT_ICON.start()
            else:
                WAIT_ICON2 = True
                $('#loading-indicator').show()
            jQuery.ajax({'type': "GET", 'url': href2, 'success': _on_new_win })
            #jQuery(elem).closest('.dropdown-menu').dropdown('toggle')
            #jQuery('.navbar-ex1-collapse').collapse('hide')
        return False




def _on_error(request, settings):
    nonlocal WAIT_ICON, WAIT_ICON2
    if WAIT_ICON:
        WAIT_ICON.stop()
        WAIT_ICON = None
    if WAIT_ICON2:
        $('#loading-indicator').hide()
        WAIT_ICON2 = False

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

    jQuery('div.dialog-form').on('hide.bs.modal',
        def(e):
            nonlocal IS_POPUP
            IS_POPUP = False
            jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>")
    )

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
                x = e.state
                jQuery('#body_body').html(LZString.decompress(x[0]))
                ACTIVE_PAGE = Page(0, jQuery('#body_body'))
                ACTIVE_PAGE.set_href(document.location)
                #menu.on_new_page('body_body')

                if APPLICATION_TEMPLATE == 'standard':
                    #jQuery('a.menu-href').removeClass('btn-warning').addClass('btn-info')
                    #jQuery('#'+x[1]).removeClass('btn-info').addClass('btn-warning')

                    jQuery('a.menu-href').removeClass('btn-warning')
                    jQuery('#'+x[1]).addClass('btn-warning')

                #page_init('body_body')
            PUSH_STATE = True
        else:
            if APPLICATION_TEMPLATE == 'modern':
                alert("X1")
            else:
                jQuery('#body_body').html("")
                ACTIVE_PAGE = None
                if APPLICATION_TEMPLATE == 'standard':
                    jQuery('a.menu-href').removeClass('btn-warning')
                    #.addClass('btn-info')
,False)


def history_push_state(title, url, data=None):
    url2 = url.split("?")[0]
    if data:
        data2 = [LZString.compress(data[0]),data[1]]
    else:
        data2 = title
    window.history.pushState(data2, title, url2)


