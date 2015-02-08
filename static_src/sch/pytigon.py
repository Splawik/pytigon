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

class TabMenuItem:
    def __init__(self, id, title, url, data=None):
        self.id = id
        self.title = title
        self.url = url
        self.data = data

class Menu:
    def __init__(self):
        self.id = 0
        self.titles = {}

    def is_open(self, title):
        if title in self.titles and self.titles[title]:
            return True
        else:
            return False

    def activate(self, title, push_state=True):
        nonlocal PUSH_STATE
        menu_item = self.titles[title]
        jQuery(sprintf('#li_%s a', menu_item.id)).tab('show')
        if push_state and PUSH_STATE:
            history_push_state(menu_item.title, menu_item.url)

    def new_page(self, title, data, href):
        nonlocal ACTIVE_PAGE, PUSH_STATE
        _id = "tab" + self.id
        self.titles[title] = new TabMenuItem(_id, title, href, data)

        jQuery('#tabs2').append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='glyphicon glyphicon-remove'></span></button></li>", [_id, _id, title, _id]))
        jQuery('#tabs2_content').append(sprintf("<div class='tab-pane' id='%s'></div>", _id) )

        ACTIVE_PAGE = jQuery('#'+_id)

        jQuery('#'+_id).html(data)
        if PUSH_STATE:
            history_push_state(title, href)


        jQuery('#tabs2 a:last').tab('show')


        jQuery('#tabs2 a:last').on('shown.bs.tab',def(e):
                nonlocal PUSH_STATE, ACTIVE_PAGE
                ACTIVE_PAGE = jQuery('#'+_id)
                menu = get_menu()
                menu_item = menu.titles[jQuery.trim(e.target.text)]
                if PUSH_STATE:
                    history_push_state(menu_item.title, menu_item.url)
        )
        self.on_new_page(_id)

        jQuery(sprintf('#button_%s', _id)).click(def(event):
            get_menu().remove_page(jQuery(this).attr('id').replace('button_',''))
        )
        self.id += 1

        return _id


    def remove_page(self, id):
        jQuery.each(self.titles, def(index, value):
            if value and value.id == id:
                self.titles[index] = None
        )
        jQuery(sprintf('#li_%s', id) ).remove()
        jQuery(sprintf('#%s', id)).remove()
        jQuery('#tabs2 a:last').tab('show')


    def on_new_page(self, id):
        table_type = get_table_type(jQuery('#'+ id))

        paginator = get_page(jQuery('#'+ id)).find('.pagination')
        if paginator.length>0:
            paginate = True
            pg = ACTIVE_PAGE.find('.pagination')
            totalPages = pg.attr('totalPages')
            options = {
                'totalPages': totalPages,
                'visiblePages': 3, 'first': '<<', 'prev': '<', 'next': '>', 'last': '>>',
                'onPageClick': def(event, page):
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




def get_datatable_dy(selector):
    dy_table = ACTIVE_PAGE.find('.tabsort_panel').offset().top
    dy_win = jQuery(window).height()
    dy = dy_win - dy_table
    if dy<100: dy = 100
    return dy


def set_table_type(table_type, selector, paginate):
    if table_type == '' or table_type == 'simple':
        pass
    if table_type == 'scrolled':
        stick_header()
    if table_type == 'datatable':
        if paginate:
            options = get_datatable_options1()
            options['scrollY'] += get_datatable_dy(selector)
            jQuery(selector).dataTable( options )
        else:
            options = get_datatable_options()
            options['scrollY'] += get_datatable_dy(selector)
            jQuery(selector).dataTable( options )
    if table_type == 'server-side':
        options = get_datatable_options2()
        options['scrollY'] += get_datatable_dy(selector)
        jQuery(selector).dataTable( options )

    jQuery(selector).on('click', 'a.popup', _on_popup)
    jQuery(selector).on('click', 'a.popup_info', _on_popup_info)
    jQuery(selector).on('click', 'a.popup_delete', _on_popup_delete)


def get_menu():
    nonlocal MENU
    if not MENU:
        MENU = Menu()
    return MENU


def cmd_to_python(value):
    document.title = ':'
    document.title = ':'+value


def is_hybrid():
    if window.location.host == '127.0.0.2':
        return True
    else:
        return False


def to_absolute_url(url):
    if url[0]=='/':
        return window.location.protocol + "//" + window.location.host  + url
    else:
        return window.location.protocol + "//" + window.location.host  + window.location.pathname + "/" + url


def ret_submit():
    RET_OBJ(RET_BUFOR,"OK")


def ajax_submit(form, func):
    if is_hybrid():
        queryString = form.formSerialize()
        cmd_to_python('href_to_var|'+to_absolute_url(form.attr('action'))+'?'+queryString+'|RET_BUFOR')
        RET_OBJ = func
        cmd_to_python('run_js|ret_submit();')
    else:
        form.ajaxSubmit( { success: func } )


def get_page(elem):
    return elem.closest('.tab-pane')


def get_table_type(elem):
    tabsort = get_page(elem).find('.tabsort')
    if tabsort.length>0:
        return tabsort.attr('table_type')
    else:
        return ""


def can_popup():
    if(IS_POPUP):
        return False
    else:
        return True


def _dialog_loaded(is_modal):
    nonlocal IS_POPUP
    date_init()
    jQuery("div.resizable").resizable()
    if is_modal:
        jQuery('div.dialog-form').modal()
        IS_POPUP = True


def on_dialog_load():
    pass


def dialog_ex_load2(responseText, status, response):
    if status!='error':
        _dialog_loaded(False)
        on_dialog_load()



def _on_popup():
    l = Ladda.create(this)
    if is_hybrid():
        cmd_to_python("href_to_elem|"+this.href+"|#dialog-data")
        jQuery('div.dialog-form').modal()
    else:
        if can_popup():
            jQuery("div.dialog-data").load(jQuery(this).attr("href"), None, def(responseText, status, response):
                if status!='error':
                    _dialog_loaded(True)
                    on_dialog_load()
            )
        else:
            l.start()
            jQuery(".inline_dialog").remove()
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"))
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"),None,def(responseText, status, response):
                if status!='error':
                    _dialog_loaded(False)
                    on_dialog_load()
                l.stop()
            )
    return False

def _on_popup_info():
    if is_hybrid():
        cmd_to_python("href_to_elem|"+this.href+"|#dialog-data-info")
        jQuery('div.dialog-form-info').modal()
    else:
        if can_popup():
            jQuery("div.dialog-data-info").load(jQuery(this).attr("href"),None, def(responseText, status, response):
                jQuery('div.dialog-form-info').modal()
            )
        else:
            jQuery(".inline_dialog").remove()
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"))
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"),None)

    return False


def _on_popup_delete():
    if is_hybrid():
        cmd_to_python("href_to_elem|"+this.href+"|#dialog-data-delete")
        jQuery('div.dialog-form-delete').modal()
    else:
        if can_popup():
            jQuery("div.dialog-data-delete").load(jQuery(this).attr("href"),None, def(responseText, status, response):
                jQuery('div.dialog-form-delete').modal()
            )
        else:
            jQuery(".inline_dialog").remove()
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"))
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"),None)

    return False

def _on_error(request, settings):
    start = settings.responseText.indexOf("<body>")
    end = settings.responseText.lastIndexOf("</body>")
    if start > 0 and end > 0:
        jQuery("div.dialog-data-error").html(settings.responseText.substring(start+6,end-1))
        jQuery('div.dialog-form-error').modal()
    else:
        jQuery("div.dialog-data-error").html(settings.responseText)
        jQuery('div.dialog-form-error').modal()


def _refresh_win(responseText, form):
    if "RETURN_OK" in responseText:
        subform = form.closest('div.inline_frame')
        if subform.length>0:
            subform.find("div.frame-data-inner").load(subform.attr('href'),None)
        else:
            filter = form.closest('div.content').find('form.TableFiltr')
            jQuery("div.dialog-form").fadeTo( "slow", 0.5 )
            if filter.length>0:
                filter.attr('action', window.location.href)
                filter.submit()
    else:
        jQuery("div.dialog-data").html(responseText)


def on_edit_ok(form):
    jQuery.ajax({'type': "POST", 'url': form.attr('action'), 'data': form.serialize(), 'success': def(data): _refresh_win(data, form); })
    return False


def on_delete_ok(form):
    jQuery.ajax({'type': "POST", 'url': form.attr('action'), 'data': form.serialize(),'success': def(data): _refresh_win(data, form); })
    return False


def on_cancel_inline():
    jQuery(".inline_dialog").remove()


def date_init():
    jQuery('.dateinput').datetimepicker({ 'pickTime': False, 'format': "YYYY-MM-DD", 'language': LANG })
    jQuery('.datetimeinput').datetimepicker({'format': "YYYY-MM-DD hh:mm", 'language': 'pl'})


def popup_init():
    jQuery('div.dialog-form').on('hide.bs.modal', def(e):
        nonlocal IS_POPUP
        IS_POPUP = False
        jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>")
    )
    jQuery('a.popup').click(_on_popup)
    jQuery('a.popup_info').click(_on_popup_info)
    jQuery('a.popup_delete').click(_on_popup_delete)



def get_datatable_options():
    options = { 'scrollY': -120,
                'paging': False,
                'responsive': True,
                "dom": 'RC<"clear">frt',
                "language": { "url": "/static/jquery_plugins/datatables/i18n/Polish.lang" }
    }
    return options

def get_datatable_options1():
    options = { 'scrollY': -75,
                'paging': False,
                'responsive': True,
                "dom": 'lrt',
                "bSort" : False,
                "language": { "url": "/static/jquery_plugins/datatables/i18n/Polish.lang" }
    }
    return options

def get_datatable_options2():
    options = { 'scrollY': 0,
                'paging': False,
                'responsive': True,
                "dom": 'lrt',
                "language": { "url": "/static/jquery_plugins/datatables/i18n/Polish.lang" }
    }
    return options


#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
def _on_menu_href(event):
    if APPLICATION_TEMPLATE != 'traditional':

        title = jQuery.trim(jQuery(this).text())
        menu = get_menu()
        classname = jQuery(this).attr("class")
        if 'btn' in classname:
            l = Ladda.create(this)
        else:
            l = None

        if APPLICATION_TEMPLATE == 'modern' and menu.is_open(title):
            menu.activate(title)
        else:
            href = jQuery(this).attr("href")
            def _on_new_win(data):
                nonlocal href
                if APPLICATION_TEMPLATE == 'modern':
                    id = menu.new_page(title, data, href)
                else:
                    jQuery('#body_body').html(data)


                popup_init()
                if l:
                    l.stop()

            if '?' in href:
                href = href + '&hybrid=1'
            else:
                href = href + '?hybrid=1'
            if APPLICATION_TEMPLATE == 'standard' and 'btn' in classname:
                jQuery('a.menu-href').removeClass('btn-warning').addClass('btn-info')
                jQuery(this).removeClass('btn-info').addClass('btn-warning')
            if l:
                l.start()
            jQuery.ajax({'type': "GET", 'url': href, 'success': _on_new_win })
            jQuery(this).closest('.dropdown-menu').dropdown('toggle')
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
            jQuery('a.menu-href').click(_on_menu_href)
        )


def jquery_ready():
    nonlocal ACTIVE_PAGE, BASE_PATH
    jQuery(document).ajaxError(_on_error)
    date_init()
    if APPLICATION_TEMPLATE == 'traditional':
        ACTIVE_PAGE = jQuery('#body_body')

        tabsort = JQuery('.tabsort')
        if tabsort.length>0:
            table_type =  tabsort.attr('table_type')
        else:
            table_type = ""
        paginator = JQuery('.paginator')
        if paginator.length>0:
            paginate = True
        else:
            paginate = False

        set_table_type(table_type, ".tabsort", paginate)
    else:
        if APPLICATION_TEMPLATE == 'modern':
            txt  = jQuery('#body_body').text()
            txt2 = jQuery.trim(txt)
            if txt2:
                txt = jQuery.trim(jQuery('#body_body').html())
                jQuery('#body_body').html("")
                menu = get_menu()
                menu.new_page(jQuery('title').text(), txt, BASE_PATH)


def stick_resize():
    tbl = ACTIVE_PAGE.find(".tbl_scroll")
    dy_table = tbl.offset().top
    dy_win = dy_win = jQuery(window).height()
    dy = dy_win - dy_table
    if(dy<100)  dy = 100
    tbl.height(dy-35)


def resize_win():
    stick_resize()
    tab2 = []
    tab_width = ACTIVE_PAGE.find("table[name='tabsort']").width()
    ACTIVE_PAGE.find(".tbl_header").width(tab_width)

    ACTIVE_PAGE.find("table[name='tabsort'] tr:first td").each(def():
        tab2.push(jQuery(this).width())
    )
    tab2 = tab2.reverse()
    ACTIVE_PAGE.find(".tbl_header th").each(def():
        jQuery(this).width(tab2.pop())
    )


def stick_header2():
    tab = []
    tab2 = []

    jQuery("table.tabsort th").each(def():
        tab.push($(this).width())
    )

    table = jQuery('<table id="tbl_header" class="tabsort" style="overflow-x: hidden;"></table>')
    table.append( jQuery("table.tabsort thead") )

    jQuery('#tbl_scroll').before(table)

    jQuery("#tbl_header th").each(def():
        tab2.push($(this).width())
    )

    tab2 = tab2.reverse()

    jQuery("table[name='tabsort'] tr:first td").each(def():
        x = tab2.pop()
        if x > jQuery(this).width():
            jQuery(this).css("min-width", x)
    )

    tab = tab.reverse()
    jQuery("#tbl_header th").each(def():
        jQuery(this).width(tab.pop())
    )

    jQuery(window).resize(resize_win)

    resize_win()



def stick_header():
    tab = []
    tab2 = []

    ACTIVE_PAGE.find("table.tabsort th").each(def():
        tab.push($(this).width())
    )

    table = jQuery('<table class="tabsort tbl_header" style="overflow-x: hidden;"></table>')
    table.append( ACTIVE_PAGE.find("table.tabsort thead") )

    ACTIVE_PAGE.find('.tbl_scroll').before(table)

    ACTIVE_PAGE.find(".tbl_header th").each(def():
        tab2.push($(this).width())
    )

    tab2 = tab2.reverse()

    ACTIVE_PAGE.find("table[name='tabsort'] tr:first td").each(def():
        x = tab2.pop()
        if x > jQuery(this).width():
            jQuery(this).css("min-width", x)
    )

    tab = tab.reverse()
    ACTIVE_PAGE.find(".tbl_header th").each(def():
        jQuery(this).width(tab.pop())
    )

    jQuery(window).resize(resize_win)

    resize_win()


window.addEventListener('popstate', def(e):
    nonlocal PUSH_STATE
    if e.state:
        PUSH_STATE = False
        menu = get_menu().activate(e.state, False)
        PUSH_STATE = True
,False)


def history_push_state(title, url):
    url2 = url.split("?")[0]
    window.history.pushState(title, title, url2)
