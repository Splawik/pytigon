#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

#target:
## _blank: new browser window
## _top: new app tab
## _self: replace current page
## refresh_obj: replace current object
## refresh_page: replace current page (like _self)
## refresh_app: replace current app

APPLICATION_TEMPLATE = 'standard'

RET_BUFOR = None
RET_OBJ = None

LANG = "en"
MENU = None
PUSH_STATE = True
BASE_PATH = None
WAIT_ICON = None
WAIT_ICON2 = False
MENU_ID = 0
BASE_FRAGMENT_INIT = None
COUNTER = 1
EDIT_RET_FUNCTION = None
RET_CONTROL = None
RIOT_INIT = None

import glob
from page import Page
from tabmenuitem import TabMenuItem
from tabmenu import get_menu
from popup import on_get_tbl_value, on_new_tbl_value, on_get_row, on_popup_edit_new, on_popup_inline, on_popup_info,\
     on_popup_delete, on_cancel_inline, refresh_fragment, on_edit_ok, on_delete_ok, ret_ok
from tbl import init_table, datatable_onresize
from tools import can_popup, corect_href, get_table_type, handle_class_click, ajax_get, ajax_post, ajax_load, ajax_submit, load_css, load_js, load_many_js

def init_pagintor(pg):
    nonlocal WAIT_ICON2
    if pg.length>0:
        paginate = True
        totalPages = pg.attr('totalPages')
        page_number = pg.attr('start_page')
        options = {
            'totalPages': +totalPages,
            'startPage': +page_number,
            'visiblePages': 3, 'first': '<<', 'prev': '<', 'next': '>', 'last': '>>',
            'onPageClick':def(event, page):
                form = pg.closest('.refr_object').find('form.refr_source')
                if form:
                    def _on_new_page(data):
                        nonlocal WAIT_ICON2
                        pg.closest('.content').find(".tabsort tbody").html(jQuery(jQuery.parseHTML(data)).find(".tabsort tbody").html())
                        fragment_init(pg.closest('.content').find(".tabsort tbody"))
                        if WAIT_ICON2:
                            $('#loading-indicator').hide()
                            WAIT_ICON2 = False

                    url = pg.attr('href').replace('[[page]]', page)+'&only_content=1'
                    form.attr('action', url)
                    form.attr('href', url)
                    active_button = pg.find('.page active')
                    WAIT_ICON2 = True
                    $('#loading-indicator').show()
                    ajax_post(url, form.serialize(), _on_new_page)
        }
        pg.twbsPagination(options)
        if +page_number != 1:
            form = pg.closest('.refr_object').find('form.refr_source')
            url = pg.attr('href').replace('[[page]]', page_number)+'&only_content=1'
            form.attr('action', url)
            form.attr('href', url)
    else:
        paginate = False

    return paginate

def fragment_init(elem=None):
    nonlocal RIOT_INIT
    if elem:
        elem2 = elem
    else:
        elem2 = glob.ACTIVE_PAGE.page

    d = elem2.find('.dateinput')
    d.wrap( "<div class='input-group date'></div>" )
    d.after("<span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span>")
    d.parent().datetimepicker({'format': 'YYYY-MM-DD', 'locale': 'pl', 'showTodayButton': True})

    d = elem2.find('.datetimeinput')
    d.wrap( "<div class='input-group date datetime'></div>" )
    d.after("<span class='input-group-addon'><span class='glyphicon glyphicon-time'></span></span>")
    d.parent().datetimepicker({'format': 'YYYY-MM-DD hh:mm', 'locale': 'pl', 'showTodayButton': True})

    elem2.find('.win-content').bind('resize', datatable_onresize)

    jQuery('.selectpicker').selectpicker()

    if RIOT_INIT:
        _id = jQuery(elem).uid()
        for pos in RIOT_INIT:
            x = sprintf("riot.mount('#%s')", _id+" "+pos)
            eval(x)

    if BASE_FRAGMENT_INIT:
        BASE_FRAGMENT_INIT()

    datatable_onresize()

def page_init(id, first_time = True):
    nonlocal WAIT_ICON, WAIT_ICON2 #, ACTIVE_PAGE
    table_type = get_table_type(jQuery('#'+ id))

    if table_type != 'datatable':
        if glob.ACTIVE_PAGE:
            pg = glob.ACTIVE_PAGE.page.find('.pagination')
            paginate = init_pagintor(pg)

    init_table(jQuery('#'+ id + ' .tabsort'), table_type)

    if first_time:
        elem2 = jQuery('body')
        handle_class_click(elem2, 'get_tbl_value', on_get_tbl_value)
        handle_class_click(elem2, 'new_tbl_value', on_new_tbl_value)
        handle_class_click(elem2, 'get_row', on_get_row)
        jQuery('#'+ id).on( "click", "a",
            def(e):
                target = jQuery(e.currentTarget).attr('target')
                src_obj = jQuery(this)

                if target == "_blank":
                    return

                for pos in ['get_tbl_value', 'new_tbl_value', 'get_row']:
                    if jQuery(this).hasClass(pos):
                        return True

                for pos in [ ('popup', on_popup_edit_new), ('popup_inline', on_popup_inline),  ('popup_info', on_popup_info), ('popup_delete', on_popup_delete) ]:
                    if jQuery(this).hasClass(pos[0]):
                        e.preventDefault()
                        pos[1](this)
                        return True

                href = jQuery(this).attr("href")
                if href and '#' in href:
                    return True

                e.preventDefault()

                if $(e.currentTarget).attr('target') in ("_top", "_top2"):
                    title = $(e.currentTarget).attr('title')
                    if not title:
                        if len(href)>16:
                            title = '...'+href[-13:]
                        else:
                            title = href
                    return _on_menu_href(this,title)

                href2 = corect_href(href)

                ajax_get(href2, def (data):
                    nonlocal href, src_obj

                    if (data and "_parent_refr" in data) or target in ("refresh_obj", "refresh_page"):
                        if target=="refresh_obj":
                            refresh_fragment(src_obj, None, True)
                        else:
                            refresh_fragment(src_obj)
                    else:
                        if APPLICATION_TEMPLATE == 'modern':
                            glob.ACTIVE_PAGE.page.html(data)
                            glob.ACTIVE_PAGE.set_href(href)
                            page_init(glob.ACTIVE_PAGE.id, False)
                        else:
                            jQuery('#body_body').html(data)
                            page_init('body_body', False)
                        glob.ACTIVE_PAGE.set_href(href)
                        get_menu().get_active_item().url = href
                        if PUSH_STATE:
                            history_push_state("title", href)
                )
        )
    glob.ACTIVE_PAGE.page.find('form').submit(
        def(e):
            nonlocal WAIT_ICON, WAIT_ICON2 #ACTIVE_PAGE,

            if jQuery(this).attr('target')=='_blank':
                jQuery(this).attr( "enctype", "multipart/form-data" ).attr( "encoding", "multipart/form-data" )
                return True

            data = jQuery(this).serialize()

            if data and 'pdf=on' in data:
                jQuery(this).attr('target','_blank')
                jQuery(this).attr( "enctype", "multipart/form-data" ).attr( "encoding", "multipart/form-data" )
                return True
            if data and 'odf=on' in data:
                jQuery(this).attr('target','_blank')
                jQuery(this).attr( "enctype", "multipart/form-data" ).attr( "encoding", "multipart/form-data" )
                return True

            e.preventDefault()

            submit_button = jQuery(this).find('button[type="submit"]')
            if submit_button.length > 0:
                submit_button.attr("data-style", "zoom-out")
                submit_button.attr("data-spinner-color", "#FF0000")
                WAIT_ICON = Ladda.create(submit_button[0])
                WAIT_ICON.start()
            else:
                WAIT_ICON2 = True
                $('#loading-indicator').show()


            href = jQuery(this).attr("action")
            if href:
                jQuery(this).attr('action', corect_href(href))

            ajax_submit(jQuery(this), def(data):
                nonlocal  WAIT_ICON, WAIT_ICON2, id #, ACTIVE_PAGE,
                glob.ACTIVE_PAGE.page.html(data)
                page_init(id, False)
                if WAIT_ICON:
                    WAIT_ICON.stop()
                if WAIT_ICON2:
                    jQuery('#loading-indicator').hide()
                    WAIT_ICON2 = False
            )
    )
    fragment_init(glob.ACTIVE_PAGE.page)


def app_init(application_template, menu_id, lang, base_path, base_fragment_init, riot_init):
    nonlocal APPLICATION_TEMPLATE, LANG, BASE_PATH, BASE_FRAGMENT_INIT, RIOT_INIT
    APPLICATION_TEMPLATE = application_template
    LANG = lang
    BASE_PATH = base_path
    BASE_FRAGMENT_INIT = base_fragment_init
    RIOT_INIT = riot_init
    if can_popup():
        SUBWIN = False

        jQuery(def ():
            nonlocal menu_id
            jQuery("#tabs").tabdrop()
            jQuery("#tabs2").tabdrop()
            if APPLICATION_TEMPLATE != 'traditional':
                pos = jQuery(".menu-href.btn-warning")
                if pos.length > 0:
                    elem = jQuery('#a_'+pos.closest('div.tab-pane').attr('id'))
                    elem.tab('show')
                else:
                    elem = jQuery(".first_pos")
                    elem.tab('show')
            else:
                id = int(menu_id) +1
                elem = jQuery('#tabs a:eq('+ id + ')')
                elem.tab('show')

            jQuery(elem.prop("hash")).perfectScrollbar()

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

            jQuery('#logout').on('click',
                def():
                    window.location = jQuery(this).attr('action')
            )

            jQuery('.system_menu').on('click',
                def():
                    window.location = jQuery(this).attr('action')
            )

            #jQuery('.tab-tab').perfectScrollbar()

            jQuery('#tabs a').click(
                def (e):
                    e.preventDefault()
                    jQuery(this).tab('show')
                    jQuery(jQuery(this).prop("hash")).perfectScrollbar()
            )

            jQuery("#tabs2").on('shown.bs.tab',
                def (e):
                    datatable_onresize()
            )

            jQuery('body').on('expanded.pushMenu collapsed.pushMenu',
                def (e):
                    window.setTimeout(datatable_onresize, 300)
            )

            jQuery(window).resize(datatable_onresize)

        )
    else:
        SUBWIN = True

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
            jQuery(elem).attr("data-style", "zoom-out")
            jQuery(elem).attr("data-spinner-color", "#FF0000")
            WAIT_ICON = Ladda.create(elem)
        else:
            WAIT_ICON = None

        if APPLICATION_TEMPLATE == 'modern' and menu.is_open(title):
            menu.activate(title)
        else:
            href = jQuery(elem).attr("href")
            href2 = corect_href(href)
            def _on_new_win(data):
                nonlocal href, href2, title, WAIT_ICON, WAIT_ICON2, MENU_ID, RIOT_INIT

                if APPLICATION_TEMPLATE == 'modern':
                    id = menu.new_page(title, data, href2, RIOT_INIT)
                else:
                    jQuery('#body_body').html(data)
                    glob.ACTIVE_PAGE = Page(0, jQuery('#body_body'))
                    glob.ACTIVE_PAGE.set_href(href2)
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

            if APPLICATION_TEMPLATE == 'standard' and classname and 'btn' in classname:
                #jQuery('a.menu-href').removeClass('btn-warning').addClass('btn-info')
                #jQuery(elem).removeClass('btn-info').addClass('btn-warning')

                jQuery('a.menu-href').removeClass('btn-warning')
                jQuery(elem).addClass('btn-warning')

            if WAIT_ICON:
                WAIT_ICON.start()
            else:
                WAIT_ICON2 = True
                $('#loading-indicator').show()
            ajax_get(href2, _on_new_win)
            jQuery('.navbar-ex1-collapse').collapse('hide')
            #datatable_onresize()
        return False


def _on_error(request, settings):
    nonlocal WAIT_ICON, WAIT_ICON2
    if WAIT_ICON:
        WAIT_ICON.stop()
        WAIT_ICON = None
    if WAIT_ICON2:
        $('#loading-indicator').hide()
        WAIT_ICON2 = False

    if settings.status==200:
        return

    if settings.responseText:
        start = settings.responseText.indexOf("<body>")
        end = settings.responseText.lastIndexOf("</body>")
        if start > 0 and end > 0:
            jQuery("#dialog-data-error").html(settings.responseText.substring(start+6,end-1))
            jQuery('#dialog-form-error').modal()
        else:
            jQuery("#dialog-data-error").html(settings.responseText)
            jQuery('#dialog-form-error').modal()
    #else:
    #    jQuery("#dialog-data-error").html("ERROR")
    #    jQuery('#dialog-form-error').modal()


def jquery_ready():
    nonlocal BASE_PATH, RIOT_INIT

    jQuery(document).ajaxError(_on_error)

    jQuery('div.dialog-form').on('hide.bs.modal',
        def(e):
            nonlocal IS_POPUP
            IS_POPUP = False
            jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>")
    )

    jQuery(".navbar-ex1-collapse").on("hidden.bs.collapse",
        def():
            console.log("collapsed")
    )

    if APPLICATION_TEMPLATE == 'traditional':
        glob.ACTIVE_PAGE = Page(0, jQuery('#body_body'))

        page_init('body_body')
    else:
        if APPLICATION_TEMPLATE == 'modern':
            txt  = jQuery('.page').text()
            txt2 = jQuery.trim(txt)
            if txt2:
                txt = jQuery.trim(jQuery('.page')[0].outerHTML)
                jQuery('.page').remove()
                menu = get_menu()
                menu.new_page(jQuery('title').text(), txt, window.location.href, RIOT_INIT)
        else:
            glob.ACTIVE_PAGE = Page(0, jQuery('#body_body'))
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
                glob.ACTIVE_PAGE = Page(0, jQuery('#body_body'))
                glob.ACTIVE_PAGE.set_href(document.location)

                if APPLICATION_TEMPLATE == 'standard':
                    jQuery('a.menu-href').removeClass('btn-warning')
                    jQuery('#'+x[1]).addClass('btn-warning')
            PUSH_STATE = True
        else:
            if APPLICATION_TEMPLATE == 'modern':
                pass
            else:
                jQuery('#body_body').html("")
                glob.ACTIVE_PAGE = None
                if APPLICATION_TEMPLATE == 'standard':
                    jQuery('a.menu-href').removeClass('btn-warning')
,False)


def history_push_state(title, url, data=None):
    url2 = url.split("?")[0]
    if data:
        data2 = [LZString.compress(data[0]),data[1]]
    else:
        data2 = title
    window.history.pushState(data2, title, url2)

