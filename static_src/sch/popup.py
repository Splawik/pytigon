from tools import can_popup, corect_href, ajax_load, ajax_get, ajax_post, ajax_submit, handle_class_click
from tbl import datatable_refresh, datatable_onresize


def refresh_fragment(data_item_to_refresh, fun=None, only_table=False):
    refr_block = data_item_to_refresh.closest('.refr_object')
    if refr_block.hasClass('refr_target'):
        target = refr_block
    else:
        target = refr_block.find('.refr_target')

    if only_table:
        datatable = target.find('table[name=tabsort].datatable')
        if datatable.length>0:
            datatable_refresh(datatable)
            if fun:
                fun()
            return True
        return False

    src = refr_block.find('.refr_source')
    if src.length > 0:
        href = src.attr('href')
        if src.prop("tagName") == 'FORM':
            def _refr2(data):
                target.html(data);
                fragment_init(target)
                if fun:
                    fun();
            ajax_post(corect_href(href), src.serialize(), _refr2)
        else:
            def _on_load(responseText):
                pass
            ajax_load(target, corect_href(href), _on_load)
    return True

def on_popup_inline(elem):
    jQuery(elem).attr("data-style", "zoom-out")
    jQuery(elem).attr("data-spinner-color", "#FF0000")
    window.WAIT_ICON = Ladda.create(elem)
    if window.WAIT_ICON:
        window.WAIT_ICON.start()

    jQuery(elem).closest('table').find(".inline_dialog").remove()

    window.COUNTER = window.COUNTER    + 1
    id = window.COUNTER

    href2 = corect_href(jQuery(elem).attr("href"))
    new_fragment = jQuery("<tr class='refr_source inline_dialog hide' id='IDIAL_"+id+"' href='"+href2+"'><td colspan='20'>" + INLINE_TABLE_HTML + "</td></tr>")
    new_fragment.insertAfter(jQuery(elem).closest("tr"))
    elem2 = new_fragment.find(".refr_target")

    def _on_load(responseText, status, response):
        jQuery('#IDIAL_'+id).hide()
        jQuery('#IDIAL_'+id).removeClass('hide')
        jQuery('#IDIAL_'+id).show("slow")
        if status!='error':
            _dialog_loaded(False, elem2)
            on_dialog_load()
        if window.WAIT_ICON:
            window.WAIT_ICON.stop()
            window.WAIT_ICON = None
    ajax_load(elem2, href2, _on_load)
    return False


def on_popup_in_form(elem):
    jQuery(elem).attr("data-style", "zoom-out")
    jQuery(elem).attr("data-spinner-color", "#FF0000")
    window.WAIT_ICON = Ladda.create(elem)
    if window.WAIT_ICON:
        window.WAIT_ICON.start()

    jQuery(elem).closest('div.Dialog').find(".inline_dialog").remove()

    window.COUNTER = window.COUNTER + 1
    id = window.COUNTER

    href2 = corect_href(jQuery(elem).attr("href"))
    new_fragment = jQuery("<div class='refr_source inline_dialog hide' id='IDIAL_"+id+"' href='"+href2+"'>" + INLINE_TABLE_HTML + "</div>")
    new_fragment.insertAfter(jQuery(elem).closest("div.form-group"))
    elem2 = new_fragment.find(".refr_target")

    def _on_load(responseText, status, response):
        jQuery('#IDIAL_'+id).hide()
        jQuery('#IDIAL_'+id).removeClass('hide')
        jQuery('#IDIAL_'+id).show("slow")
        if status!='error':
            _dialog_loaded(False, elem2)
            table_type = get_table_type(elem2)
            tbl = elem2.find('.tabsort')
            if tbl.length > 0:
                init_table(tbl, table_type)
            on_dialog_load()
        if window.WAIT_ICON:
            window.WAIT_ICON.stop()
            window.WAIT_ICON = None
    ajax_load(elem2, href2, _on_load)

    return False


def on_popup_edit_new(elem):
    jQuery(elem).attr("data-style", "zoom-out")
    jQuery(elem).attr("data-spinner-color", "#FF0000")
    window.WAIT_ICON = Ladda.create(elem)
    if can_popup() and not jQuery(elem).hasClass('inline') and not (jQuery(elem).attr('name') and '_inline' in jQuery(elem).attr('name')) :
        elem2 = jQuery("div.dialog-data")
        elem2.closest(".refr_object").attr("related-object", jQuery(elem).uid())

        def _on_load(responseText, status, response):
            _dialog_loaded(True, elem2)
            on_dialog_load()
        ajax_load(elem2, jQuery(elem).attr("href"), _on_load)
    else:
        if window.WAIT_ICON:
            window.WAIT_ICON.start()
        if jQuery(elem).hasClass('new-row'):
            elem2 = jQuery("<div class='refr_source inline_dialog tr hide'>" + INLINE_DIALOG_UPDATE_HTML + "</div>")
            elem2.insertAfter(jQuery(elem).closest("div.tr"))
        else:
            test = jQuery(elem).closest('form')
            if test.length > 0:
                elem2 = jQuery("<div class='refr_source inline_dialog hide'>" + INLINE_DIALOG_UPDATE_HTML + "</div>")
                elem2.insertAfter(jQuery(elem).closest("div.form-group"))
            else:
                elem2 = jQuery("<tr class='inline_dialog hide'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>")
                elem2.insertAfter(jQuery(elem).closest("tr"))
        elem2.find('.modal-title').html(jQuery(elem).attr('title'))
        elem2.find(".refr_object").attr("related-object", jQuery(elem).uid())
        elem3 = elem2.find("div.dialog-data-inner")

        def _on_load2(responseText, status, response):
            elem2.hide()
            elem2.removeClass('hide')
            elem2.show("slow")
            if status!='error':
                _dialog_loaded(False, elem3)
                table_type = get_table_type(elem3)
                init_table(elem3, table_type)
                on_dialog_load()
            if window.WAIT_ICON:
                window.WAIT_ICON.stop()
                window.WAIT_ICON = None
        ajax_load(elem3,jQuery(elem).attr("href"), _on_load2)

    return False



def on_popup_info(elem):
    if can_popup():
        def _on_load(responseText, status, response):
            jQuery('div.dialog-form-info').modal()
        ajax_load(jQuery("div.dialog-data-info"),jQuery(elem).attr("href"), _on_load)
    else:
        jQuery(".inline_dialog").remove()
        jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML + "</td></tr>").insertAfter(jQuery(elem).parents("tr"))

        def _on_load2(responseText, status, response):
            pass
        ajax_load(jQuery("div.dialog-data-inner"),jQuery(elem).attr("href"), _on_load2)

    return False


def on_popup_delete(elem):
    if can_popup():
        jQuery("div.dialog-data-delete").closest(".refr_object").attr("related-object", jQuery(elem).uid())

        def _on_load(responseText, status, response):
            jQuery('div.dialog-form-delete').modal()
            jQuery("div.dialog-form-delete").fadeTo( "fast", 1)
        ajax_load(jQuery("div.dialog-data-delete"),jQuery(elem).attr("href"), _on_load)
    else:
        jQuery(".inline_dialog").remove()
        elem2 = jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>")
        elem2.insertAfter(jQuery(elem).parents("tr"))
        elem2.find(".refr_object").attr("related-object", jQuery(elem).uid())
        def _on_load2():
            pass
        ajax_load(jQuery("div.dialog-data-inner"),jQuery(elem).attr("href"), _on_load2)

    return False


def on_dialog_load():
    pass


def _dialog_loaded(is_modal, elem):
    fragment_init(elem)
    if is_modal:
        jQuery("div.dialog-form").fadeTo( "fast", 1)

        if jQuery('div.dialog-form').find('div.form2columns').length > 0:
            jQuery('div.dialog-form').find('.modal-dialog').addClass('modal-lg')
        else:
            jQuery('div.dialog-form').find('.modal-dialog').removeClass('modal-lg')

        jQuery('div.dialog-form').modal()
        jQuery('div.dialog-form').drags({ "handle": ".modal-header" })


def _refresh_win(responseText, ok_button):
    popup_activator = jQuery("#"+jQuery(ok_button).closest(".refr_object").attr("related-object"))
    if responseText and "RETURN_OK" in responseText:
        if not can_popup():
            if jQuery("div.dialog-form").hasClass('in'):
                dialog = "div.dialog-form"
            else:
                if jQuery("div.dialog-form-delete").hasClass('in') :
                    dialog = "div.dialog-form-delete"
                else:
                    dialog = "div.dialog-form-info"

            def hide_dialog_form():
                jQuery(dialog).modal('hide')

            jQuery(dialog).fadeTo( "slow", 0.5 )
            if not refresh_fragment(popup_activator, hide_dialog_form, True):
                refresh_fragment(popup_activator, hide_dialog_form, False)
        else:
            if not refresh_fragment(popup_activator, None, True):
                return refresh_fragment(popup_activator, None, True)
    else:
        if not can_popup():
            jQuery("div.dialog-data").html(responseText)
        else:
            ok_button.closest('.refr_target').html(responseText)

def _refresh_win_and_ret(responseText, ok_button):
    if responseText and "RETURN_OK" in responseText:
        related_object = jQuery(ok_button).closest(".refr_object").attr('related-object')
        popup_activator = jQuery("#"+related_object)
        if jQuery(ok_button).closest(".refr_object").hasClass('in'):
            jQuery("div.dialog-form").modal('hide')
        else:
            jQuery(ok_button).closest(".refr_object").remove()
        if popup_activator and popup_activator.data('edit_ret_function'):
            window.RET_CONTROL = popup_activator.data('ret_control')
            window.EDIT_RET_FUNCTION = popup_activator.data('edit_ret_function')
            q = jQuery(responseText)
            eval(q[1].text)
    else:
        jQuery("div.dialog-data").html(responseText)


def _refresh_win_after_ok(responseText, ok_button):
    related_object = jQuery(ok_button).closest(".refr_object").attr('related-object')
    popup_activator = jQuery("#"+related_object)
    if popup_activator and popup_activator.data('edit_ret_function'):
        window.EDIT_RET_FUNCTION = popup_activator.data('edit_ret_function')
        window.EDIT_RET_FUNCTION(responseText, ok_button)
        window.EDIT_RET_FUNCTION = False
    else:
        _refresh_win(responseText, ok_button)


def on_edit_ok(form):
    def _fun(data):
        _refresh_win_after_ok(data, form)
    ajax_submit(form, _fun)
    return False

window.on_edit_ok = on_edit_ok

def on_delete_ok(form):
    def _on_data(data):
        _refresh_win(data, form);
    ajax_post(corect_href(form.attr('action')), form.serialize(), _on_data )
    return False

window.on_delete_ok = on_delete_ok


def on_cancel_inline(elem):
    jQuery(elem).closest('.inline_dialog').remove()


def ret_ok(id, title):
    window.RET_CONTROL.select2('data', {id: id, text: title}).trigger("change")
    window.RET_CONTROL.val(id.toString())
    window.RET_CONTROL[0].defaultValue = id.toString()

def on_get_tbl_value(elem):
    on_popup_in_form(elem)

def on_new_tbl_value(elem):
    window.EDIT_RET_FUNCTION = _refresh_win_and_ret
    window.RET_CONTROL = jQuery(elem).closest(".input-group").find('.django-select2')
    jQuery(elem).data('edit_ret_function', window.EDIT_RET_FUNCTION)
    jQuery(elem).data('ret_control', window.RET_CONTROL)
    return on_popup_edit_new(elem)

def on_get_row(elem):
    id = jQuery(elem).attr('data-id')
    text = jQuery(elem).attr('data-text')
    ret_control = jQuery(elem).closest(".refr_source").prev('.form-group').find('.django-select2')
    if ret_control.find("option[value='"+id+"']").length==0:
        ret_control.append(jQuery("<option>", { "value": id, "text": text }))
    ret_control.val(id.toString())
    ret_control.trigger('change')

    jQuery(elem).closest(".refr_source").remove()


def fragment_init(elem=None):
    if elem:
        elem2 = elem
    else:
        elem2 = window.ACTIVE_PAGE.page

    handle_class_click(elem, 'get_tbl_value', on_get_tbl_value)
    handle_class_click(elem, 'new_tbl_value', on_new_tbl_value)
    handle_class_click(elem, 'get_row', on_get_row)

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

    if window.RIOT_INIT:
        _id = jQuery(elem).uid()
        for pos in window.RIOT_INIT:
            x = sprintf("riot.mount('#%s')", _id+" "+pos)
            eval(x)

    if window.BASE_FRAGMENT_INIT:
        window.BASE_FRAGMENT_INIT()

    datatable_onresize()