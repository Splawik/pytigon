APPLICATION_TEMPLATE = 'traditional'
#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

RET_BUFOR = None
RET_OBJ = None

IS_POPUP = False
SUBWIN = False
LANG = "en"
MENU = None

def _on_close_page(event):
    get_menu().remove_page(jQuery(this).attr('id').replace('button_',''))

class Menu:
    def __init__(self):
        self.id = 0
        self.titles = {}

    def new_pos(self, title):
        if title in self.titles and self.titles[title]:
            _id = self.titles[title]
            $('#li_%s a' % (_id,)).tab('show')
            return None
        else:
            _id = "tab" + str(self.id)
            self.titles[title] = _id
            jQuery('#tabs2').append("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='glyphicon glyphicon-remove'></span></button></li>" % (_id, _id, title, _id))
            jQuery('#tabs2_content').append("<div class='tab-pane' id='%s'></div>" % ( _id, ) )
            $('#tabs2 a:last').tab('show')
            $('#button_%s' % (_id,) ).click(_on_close_page)
            self.id += 1
            return _id

    def remove_page(self, id):
        for pos in self.titles:
            if self.titles[pos] == id:
                self.titles[pos] = None
        jQuery('#li_%s' % (id,) ).remove()
        jQuery('#%s' % (id,) ).remove()
        jQuery('#tabs2 a:last').tab('show')


def get_menu():
    global MENU
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


def can_popup():
    if(IS_POPUP):
        return False
    else:
        return True


def _dialog_loaded(is_modal):
    global IS_POPUP
    date_init()
    jQuery("div.resizable").resizable()
    if is_modal:
        jQuery('div.dialog-form').modal()
        IS_POPUP = True


def on_dialog_load():
    pass


def _dialog_ex_load1(responseText, status, response):
    if status!='error':
        _dialog_loaded(True)
        on_dialog_load()


def dialog_ex_load2(responseText, status, response):
    if status!='error':
        _dialog_loaded(False)
        on_dialog_load()


def dialog_ex_load_delete(responseText, status, response):
    jQuery('div.dialog-form-delete').modal()


def dialog_ex_load_info(responseText, status, response):
    jQuery('div.dialog-form-info').modal()


def _on_hide(e):
    global IS_POPUP
    IS_POPUP = False
    jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>")


def _on_popup():
    l = Ladda.create(this)
    if is_hybrid():
        cmd_to_python("href_to_elem|"+this.href+"|#dialog-data")
        jQuery('div.dialog-form').modal()
    else:
        if can_popup():
            jQuery("div.dialog-data").load(jQuery(this).attr("href"), None, _dialog_ex_load1)
        else:
            l.start()
            jQuery(".inline_dialog").remove()
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"))
            def _on_loaded(responseText, status, response):
                dialog_ex_load2(responseText, status, response)
                l.stop()
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"),None,_on_loaded)
    return False

def _on_popup_info():
    if is_hybrid():
        cmd_to_python("href_to_elem|"+this.href+"|#dialog-data-info")
        jQuery('div.dialog-form-info').modal()
    else:
        if can_popup():
            jQuery("div.dialog-data-info").load(jQuery(this).attr("href"),None,dialog_ex_load_info)
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
            jQuery("div.dialog-data-delete").load(jQuery(this).attr("href"),None,dialog_ex_load_delete)
        else:
            jQuery(".inline_dialog").remove()
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"))
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"),None)

    return False

def _on_error(request, settings):
    var start,end
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
        #var data = form.closest('form.TableFiltr')
        jQuery("div.dialog-data").html(responseText)


def on_edit_ok(form):
    def _on_refresh_win(data):
        _refresh_win(data, form)
    jQuery.ajax({'type': "POST", 'url': form.attr('action'), 'data': form.serialize(), 'success': _on_refresh_win })
    return False


def on_delete_ok(form):
    def _on_refresh_win(data):
        _refresh_win(data, form)
    jQuery.ajax({'type': "POST", 'url': form.attr('action'), 'data': form.serialize(),'success': _on_refresh_win })
    return False


def on_cancel_inline():
    jQuery(".inline_dialog").remove()


def date_init():
    jQuery('.dateinput').datetimepicker({ 'pickTime': False, 'format': "YYYY-MM-DD", 'language': LANG })
    jQuery('.datetimeinput').datetimepicker({'format': "YYYY-MM-DD hh:mm", 'language': 'pl'})


def popup_init():
    jQuery('div.dialog-form').on('hide.bs.modal', _on_hide)
    jQuery('a.popup').click(_on_popup)
    jQuery('a.popup_info').click(_on_popup_info)
    jQuery('a.popup_delete').click(_on_popup_delete)


#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
def _on_menu_href(event):
    if APPLICATION_TEMPLATE != 'traditional':
        if APPLICATION_TEMPLATE in ('standard', 'simple', 'tablet'):
            l = Ladda.create(this)
        title =  $(this).text()

        def _on_new_win(data):
            if APPLICATION_TEMPLATE in ('standard', 'tablet'):
                menu = get_menu()
                id = menu.new_pos(title)
                jQuery('#'+id).html(data)
            else:
                jQuery('#body_body').html(data)

            popup_init()
            if APPLICATION_TEMPLATE in ('standard', 'simple', 'tablet'):
                l.stop()

        href = jQuery(this).attr("href")
        if '?' in href:
            href = href + '&hybrid=1'
        else:
            href = href + '?hybrid=1'
        if APPLICATION_TEMPLATE == 'simple':
            jQuery('a.menu-href').removeClass('btn-warning').addClass('btn-info')
            jQuery(this).removeClass('btn-info').addClass('btn-warning')
        if APPLICATION_TEMPLATE in ('standard', 'simple', 'tablet'):
           l.start()
        jQuery.ajax({'type': "GET", 'url': href, 'success': _on_new_win })
        if APPLICATION_TEMPLATE in ('mobile', 'tablet'):
            $(this).closest('.dropdown-menu').dropdown('toggle')
            $('.navbar-ex1-collapse').collapse('hide')
        return False

def jquery_init(application_template, scroll_table, menu_id, lang):
    global APPLICATION_TEMPLATE, LANG
    APPLICATION_TEMPLATE = application_template
    LANG = lang
    if IS_POPUP:
        SUBWIN = True
    else:
        SUBWIN = False

    if not SUBWIN:
        if scroll_table=='True':
            jQuery(window).load(stick_header)

        def _tabs():
            jQuery("#menu_tabs").tabs()
            if APPLICATION_TEMPLATE in ('standard', 'simple', 'tablet'):
                jQuery("#tabs a:eq(1)").tab('show')
            else:
                jQuery('#tabs a:eq('+ str(menu_id) + ')').tab('show')
            jQuery('a.menu-href').click(_on_menu_href)

        jQuery(_tabs)


def jquery_ready():
    jQuery(document).ajaxError(_on_error)
    date_init()
    jQuery("div.resizable" ).resizable()
