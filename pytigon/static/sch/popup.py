__pragma__("alias", "jquery_type", "type")

from tools import (
    can_popup,
    corect_href,
    ajax_load,
    ajax_get,
    ajax_post,
    ajax_submit,
    mount_html,
    get_table_type,
    register_fragment_init_fun,
    remove_page_from_href,
    process_resize,
)

from tbl import datatable_refresh, datatable_onresize, init_table

from tabmenu import get_menu


def refresh_fragment(
    data_item_to_refresh, fun=None, only_table=False, data=None, remove_pagination=False
):
    only_table_href = False
    refr_block = data_item_to_refresh.closest(".refr_object")
    if refr_block.hasClass("refr_target"):
        target = refr_block
    else:
        target = refr_block.find(".refr_target")
        if target.length > 1:
            target = jQuery(target[0])

    if only_table:
        datatable = target.find("table[name=tabsort].datatable")
        if datatable.length > 0:
            datatable_refresh(datatable)
            target.find(".inline_dialog").remove()
            if fun:
                fun()
            return True
        datatable = target.find("table[name=tabsort].tabsort")
        if datatable.length > 0:
            only_table_href = True
            target.find(".inline_dialog").remove()
            target = datatable.closest("div.tableframe")
        else:
            return False

    if data:
        mount_html(target, data)
        if fun:
            fun()
    else:
        if refr_block.hasClass("refr_source"):
            src = refr_block
        else:
            src = refr_block.find(".refr_source")
        if src.length > 0:
            src = jQuery(src[0])
            href = src.attr("href")

            if remove_pagination:
                href = remove_page_from_href(href)

            if src.prop("tagName") == "FORM":

                def _refr2(data):
                    mount_html(target, data)
                    if fun:
                        fun()

                ajax_post(corect_href(href, only_table_href), src.serialize(), _refr2)
            else:

                def _on_load(responseText):
                    if fun:
                        fun()

                ajax_load(target, corect_href(href, only_table_href), _on_load)
        else:
            if fun:
                fun()
    return True


def on_popup_inline(url, elem, e):
    jelem = jQuery(elem)
    if jelem.hasClass("edit"):
        return on_popup_edit_new(url, elem, e)
    if jelem.hasClass("delete"):
        return on_popup_delete(url, elem, e)
    if jelem.hasClass("info"):
        return on_popup_info(url, elem, e)

    jelem.attr("data-style", "zoom-out")
    jelem.attr("data-spinner-color", "#FF0000")
    window.WAIT_ICON = Ladda.create(elem)
    if window.WAIT_ICON:
        window.WAIT_ICON.start()

    jQuery("body").addClass("shown_inline_dialog")

    jelem.closest("table").find(".inline_dialog").remove()

    window.COUNTER = window.COUNTER + 1
    id = window.COUNTER

    href2 = corect_href(jQuery(elem).attr("href"))

    new_fragment = jQuery(
        "<tr class='refr_source refr_object inline_dialog hide' id='IDIAL_"
        + id
        + "' href='"
        + href2
        + "'><td colspan='20'>"
        + INLINE_TABLE_HTML.replace("{{title}}", elem.getAttribute("title"))
        + "</td></tr>"
    )
    new_fragment.insertAfter(jQuery(elem).closest("tr"))

    elem2 = new_fragment.find(".refr_target")

    def _on_load(responseText, status, response):
        nonlocal new_fragment
        new_fragment.removeClass("hide")
        if status != "error":
            _dialog_loaded(False, elem2)
            on_dialog_load()
        if window.WAIT_ICON:
            window.WAIT_ICON.stop()
            window.WAIT_ICON = None

    ajax_load(elem2, href2, _on_load)
    return False


def on_popup_in_form(elem, absolute=False):
    jQuery(elem).attr("data-style", "zoom-out")
    jQuery(elem).attr("data-spinner-color", "#FF0000")
    window.WAIT_ICON = Ladda.create(elem)
    if window.WAIT_ICON:
        window.WAIT_ICON.start()

    jQuery("body").addClass("shown_inline_dialog")
    jQuery(elem).closest("div.Dialog").find(".inline_dialog").remove()

    window.COUNTER = window.COUNTER + 1
    id = window.COUNTER

    href2 = corect_href(jQuery(elem).attr("href"))
    if absolute:
        add_html = ABSOLUTE_HTML
    else:
        add_html = INLINE_TABLE_HTML
    new_fragment = jQuery(
        "<div class='refr_source refr_object inline_dialog hide' id='IDIAL_"
        + id
        + "' href='"
        + href2
        + "'>"
        + add_html.replace("{{title}}", elem.getAttribute("title"))
        + "</div>"
    )
    new_fragment.insertAfter(jQuery(elem).closest("div.form-group"))
    elem2 = new_fragment.find(".refr_target")

    def _on_load(responseText, status, response):
        jQuery("#IDIAL_" + id).hide()
        jQuery("#IDIAL_" + id).removeClass("hide")
        jQuery("#IDIAL_" + id).show("slow")
        if status != "error":
            _dialog_loaded(False, elem2)
            on_dialog_load()
        if window.WAIT_ICON:
            window.WAIT_ICON.stop()
            window.WAIT_ICON = None

    ajax_load(elem2, href2, _on_load)

    return False


def on_popup_edit_new(url, elem, e):
    if e:
        target = jQuery(e.currentTarget).attr("target")
    else:
        target = "popup"

    if url:
        href2 = corect_href(url)
    else:
        href2 = corect_href(jQuery(elem).attr("href"))

    jQuery(elem).attr("data-style", "zoom-out")
    jQuery(elem).attr("data-spinner-color", "#FF0000")
    window.WAIT_ICON = Ladda.create(elem)
    if (
        can_popup()
        and not target == "inline"
        and not jQuery(elem).hasClass("inline")
        and not (jQuery(elem).attr("name") and "_inline" in jQuery(elem).attr("name"))
    ):
        jQuery("#ModalLabel").html(jQuery(elem).attr("title"))

        elem2 = jQuery("div.dialog-data")
        elem2.closest(".refr_object").attr("related-object", jQuery(elem).uid())

        def _on_load(responseText, status, response):
            _dialog_loaded(True, elem2)
            on_dialog_load()

        ajax_load(elem2, href2, _on_load)
    else:
        jQuery("body").addClass("shown_inline_dialog")
        if window.WAIT_ICON:
            window.WAIT_ICON.start()
        if jQuery(elem).hasClass("new-row"):
            elem2 = jQuery(
                sprintf(
                    "<div class='refr_source refr_object inline_dialog tr hide' href='%s'>",
                    href2,
                )
                + INLINE_DIALOG_UPDATE_HTML
                + "</div>"
            )
            new_position = jQuery(elem).closest(".refr_object").find("div.new_row")
            if new_position.length > 0:
                elem2.insertAfter(jQuery(new_position[0]))
            else:
                elem2.insertAfter(jQuery(elem).closest("div.tr"))
        else:
            in_table = False
            for obj in [jQuery(elem).parent(), jQuery(elem).parent().parent()]:
                for c in ["td_action", "td_information"]:
                    if obj.hasClass(c):
                        in_table = True
                        break
            if in_table:
                elem2 = jQuery(
                    sprintf(
                        "<tr class='refr_source refr_object inline_dialog hide' href='%s'><td colspan='20'>",
                        href2,
                    )
                    + INLINE_DIALOG_UPDATE_HTML
                    + "</td></tr>"
                )
                elem2.insertAfter(jQuery(elem).closest("tr"))
            else:
                test = jQuery(elem).closest("form")
                if test.length > 0:
                    elem2 = jQuery(
                        sprintf(
                            "<div class='refr_source refr_object inline_dialog hide' href='%s'>",
                            href2,
                        )
                        + INLINE_DIALOG_UPDATE_HTML
                        + "</div>"
                    )
                    elem2.insertAfter(jQuery(elem).closest("div.form-group"))
                else:
                    elem2 = jQuery(
                        sprintf(
                            "<div class='refr_source refr_object inline_dialog tr hide' href='%s'>",
                            href2,
                        )
                        + INLINE_DIALOG_UPDATE_HTML
                        + "</div>"
                    )
                    new_position = (
                        jQuery(elem).closest(".refr_object").find("div.new_row")
                    )
                    if new_position.length > 0:
                        elem2.insertAfter(jQuery(new_position[0]))
                    else:
                        elem2.insertAfter(jQuery(elem).closest("div.tr"))
        mount_html(elem2.find(".modal-title"), jQuery(elem).attr("title"), False, False)
        # elem2.find(".refr_object").attr("related-object", jQuery(elem).uid())
        elem2.attr("related-object", jQuery(elem).uid())
        elem3 = elem2.find("div.dialog-data-inner")

        def _on_load2(responseText, status, response):
            elem2.hide()
            elem2.removeClass("hide")
            elem2.show("slow")
            if status != "error":
                _dialog_loaded(False, elem3)
                on_dialog_load()
            if window.WAIT_ICON:
                window.WAIT_ICON.stop()
                window.WAIT_ICON = None

        ajax_load(elem3, href2, _on_load2)

    return False


window.on_popup_edit_new = on_popup_edit_new


def on_popup_info(url, elem, e):
    if can_popup():

        def _on_load(responseText, status, response):
            jQuery("div.dialog-form-info").modal()

        ajax_load(jQuery("div.dialog-data-info"), jQuery(elem).attr("href"), _on_load)
    else:
        jQuery(".inline_dialog").remove()
        jQuery(
            "<tr class='refr_object inline_dialog'><td colspan='20'>"
            + INLINE_DIALOG_INFO_HTML
            + "</td></tr>"
        ).insertAfter(jQuery(elem).parents("tr"))

        def _on_load2(responseText, status, response):
            pass

        ajax_load(jQuery("div.dialog-data-inner"), jQuery(elem).attr("href"), _on_load2)

    return False


def on_popup_delete(url, elem, e):
    if can_popup():
        jQuery("div.dialog-data-delete").closest(".refr_object").attr(
            "related-object", jQuery(elem).uid()
        )

        def _on_load(responseText, status, response):
            jQuery("div.dialog-form-delete").modal()
            jQuery("div.dialog-form-delete").fadeTo("fast", 1)

        ajax_load(jQuery("div.dialog-data-delete"), jQuery(elem).attr("href"), _on_load)
    else:
        jQuery(".inline_dialog").remove()
        elem2 = jQuery(
            "<tr class='refr_object inline_dialog'><td colspan='20'>"
            + INLINE_DIALOG_DELETE_HTML
            + "</td></tr>"
        )
        elem2.insertAfter(jQuery(elem).parents("tr"))
        elem2.find(".refr_object").attr("related-object", jQuery(elem).uid())

        def _on_load2():
            pass

        ajax_load(jQuery("div.dialog-data-inner"), jQuery(elem).attr("href"), _on_load2)

    return False


def on_dialog_load():
    process_resize()

def _dialog_loaded(is_modal, elem):
    obj = elem.closest(".refr_object")
    if obj.length > 0:
        if obj[0].hasAttribute("related-object"):
            btn = jQuery("#" + obj.attr("related-object"))
        else:
            btn = obj

        if btn.hasClass("no_cancel"):
            obj.find(".btn_cancel").hide()
            obj.find(".close").hide()
        else:
            obj.find(".btn_cancel").show()
            obj.find(".close").show()

        if btn.hasClass("no_close"):
            obj.find(".close").hide()
        else:
            obj.find(".close").show()

        if btn.hasClass("no_ok"):
            obj.find(".btn_ok").hide()
        else:
            obj.find(".btn_ok").show()

    if is_modal:
        jQuery("div.dialog-form").fadeTo("fast", 1)
        jQuery("div.dialog-form").find(".modal-dialog").removeClass(
            "modal-lg"
        ).removeClass("modal-sm")

        x = jQuery("div.dialog-form").find("div[name=modal-type-ref]")
        if x.length > 0:
            jQuery("div.dialog-form").find(".modal-dialog").addClass(x.attr("class"))

        jQuery("div.dialog-form").modal()
        jQuery("div.dialog-form").drags({"handle": ".modal-header"})


def _refresh_win(responseText, ok_button):
    refr_obj = jQuery(ok_button).closest(".refr_object")
    popup_activator = jQuery("#" + refr_obj.attr("related-object"))
    if responseText and "RETURN_OK" in responseText:
        if refr_obj.hasClass("modal"):
            if jQuery("div.dialog-form").hasClass("show"):
                dialog = "div.dialog-form"
            else:
                if jQuery("div.dialog-form-delete").hasClass("show"):
                    dialog = "div.dialog-form-delete"
                else:
                    dialog = "div.dialog-form-info"

            def hide_dialog_form():
                jQuery(dialog).modal("hide")

            jQuery(dialog).fadeTo("slow", 0.5)
            if not refresh_fragment(popup_activator, hide_dialog_form, True):
                refresh_fragment(popup_activator, hide_dialog_form, False)
        else:
            if refr_obj.hasClass("inline_dialog"):
                inline_dialog = refr_obj
            else:
                inline_dialog = refr_obj.find(".inline_dialog")
            if inline_dialog.length > 0:
                inline_dialog.remove()

            if not refresh_fragment(popup_activator, None, True):
                return refresh_fragment(popup_activator, None, False)
    else:
        if refr_obj.hasClass("modal"):
            mount_html(jQuery("div.dialog-data"), responseText)
        else:
            mount_html(ok_button.closest(".refr_target"), responseText)


def _refresh_win_and_ret(responseText, ok_button):
    if responseText and "RETURN_OK" in responseText:
        related_object = (
            jQuery(ok_button).closest(".refr_object").attr("related-object")
        )
        popup_activator = jQuery("#" + related_object)
        if jQuery(ok_button).closest(".refr_object").hasClass("show"):
            jQuery("div.dialog-form").modal("hide")
        else:
            jQuery(ok_button).closest(".refr_object").remove()
        if popup_activator and popup_activator.data("edit_ret_function"):
            window.RET_CONTROL = popup_activator.data("ret_control")
            window.EDIT_RET_FUNCTION = popup_activator.data("edit_ret_function")
            # q = jQuery(responseText)
            q = jQuery("<div>" + responseText + "</div>").find("script")
            eval(q.text())
    else:
        mount_html(jQuery("div.dialog-data"), responseText)


def _refresh_win_after_ok(responseText, ok_button):
    related_object = jQuery(ok_button).closest(".refr_object").attr("related-object")
    popup_activator = jQuery("#" + related_object)
    if popup_activator and popup_activator.data("edit_ret_function"):
        window.EDIT_RET_FUNCTION = popup_activator.data("edit_ret_function")
        window.EDIT_RET_FUNCTION(responseText, ok_button)
        window.EDIT_RET_FUNCTION = False
    else:
        _refresh_win(responseText, ok_button)


def on_edit_ok(button, form):
    if form:
        f = form
    else:
        f = jQuery(button).parent().parent().find("form:first")

    def _fun(data):
        _refresh_win_after_ok(data, f)

    if f.length > 0:
        ajax_submit(f, _fun)
    else:
        _refresh_win("RETURN_OK", jQuery(button))

    return False


window.on_edit_ok = on_edit_ok


def on_delete_ok(form):
    def _on_data(data):
        _refresh_win(data, form)

    ajax_post(corect_href(form.attr("action")), form.serialize(), _on_data)
    return False


window.on_delete_ok = on_delete_ok


def on_cancel_inline(elem):
    refr = False
    inline_dialog = jQuery(elem).closest(".inline_dialog")
    if inline_dialog.length > 0:
        test = inline_dialog.find(".refresh_after_close")
        if test.length > 0:
            refr = True
    jQuery("body").removeClass("shown_inline_dialog")
    if refr:
        _refresh_win("RETURN_OK", inline_dialog.parent())
    else:
        inline_dialog.remove()
        datatable_onresize()


window.on_cancel_inline = on_cancel_inline


def ret_ok(id, title):
    # window.RET_CONTROL.select2('data', { 'id': id, 'text': title})
    # window.RET_CONTROL.trigger("change")
    # window.RET_CONTROL.val(id.toString())
    # window.RET_CONTROL[0].defaultValue = id.toString()

    text = title

    ret_control = window.RET_CONTROL
    if ret_control.find("option[value='" + id + "']").length == 0:
        ret_control.append(jQuery("<option>", {"value": id, "text": text}))
    ret_control.val(id.toString())
    ret_control.trigger("change")


def on_get_tbl_value(url, elem, e):
    on_popup_in_form(elem, True)


def on_new_tbl_value(url, elem, e):
    window.EDIT_RET_FUNCTION = _refresh_win_and_ret
    window.RET_CONTROL = jQuery(elem).closest(".input-group").find(".django-select2")
    jQuery(elem).data("edit_ret_function", window.EDIT_RET_FUNCTION)
    jQuery(elem).data("ret_control", window.RET_CONTROL)
    return on_popup_edit_new(url, elem, e)


def on_get_row(url, elem, e):
    id = jQuery(elem).attr("data-id")
    text = jQuery(elem).attr("data-text")
    ret_control = (
        jQuery(elem).closest(".refr_source").prev(".form-group").find(".django-select2")
    )
    if ret_control.find("option[value='" + id + "']").length == 0:
        ret_control.append(jQuery("<option>", {"value": id, "text": text}))
    ret_control.val(id.toString())
    ret_control.trigger("change")

    jQuery(elem).closest(".refr_source").remove()


def _init_subforms(elem):
    subforms = elem.find(".subform_frame")

    def _load_subform(index, obj):
        content = jQuery(this).find(".subform_content")
        if content.length > 0:
            href = jQuery(this).attr("href")

            def _finish():
                pass

            ajax_load(content, corect_href(href), _finish)

    subforms.each(_load_subform)


register_fragment_init_fun(_init_subforms)


def refresh_current_object(url, elem, e):
    href = url
    href2 = corect_href(url)
    target = "refresh_obj"
    src_obj = jQuery(elem)

    refr_block = src_obj.closest(".refr_object")
    if refr_block.hasClass("refr_source"):
        src = refr_block
    else:
        src = refr_block.find(".refr_source")
    if src.length > 0:
        src.attr("href", href2)
        src.attr("action", href2)

    def _on_data(data):
        nonlocal href, src_obj, target

        if (data and "_parent_refr" in data) or target in (
            "refresh_obj",
            "refresh_page",
        ):
            if target == "refresh_obj":
                if "only_table" in href:
                    if not refresh_fragment(src_obj, None, True, data):
                        refresh_fragment(src_obj, None, False, data)
                else:
                    refresh_fragment(src_obj, None, False, data)
            else:
                refresh_fragment(src_obj, None, False, data)
        else:
            if window.APPLICATION_TEMPLATE == "modern":
                mount_html(window.ACTIVE_PAGE.page, data)
                window.ACTIVE_PAGE.set_href(href)
            else:
                mount_html(jQuery("#body_body"), data)
            window.ACTIVE_PAGE.set_href(href)
            get_menu().get_active_item().url = href
            if window.PUSH_STATE:
                history_push_state("title", href)

    if src_obj.hasClass("page-link"):
        ajax_submit(src, _on_data)
    else:
        ajax_get(href2, _on_data)


def refresh_current_page(url, elem, e):
    pass


def refresh_current_app(url, elem, e):
    pass


def _none():
    pass


def only_get(url, elem, e):
    href = url
    href2 = corect_href(url)
    target = "refresh_obj"
    src_obj = jQuery(elem)

    refr_block = src_obj.closest(".refr_object")
    if refr_block.hasClass("refr_source"):
        src = refr_block
    else:
        src = refr_block.find(".refr_source")
    if src.length > 0:
        src.attr("href", href2)
        src.attr("action", href2)

    def _on_data(data):
        nonlocal href, src_obj, target

        if data and "_parent_refr" in data and "YES" in data or "OK" in data:
            if not refresh_fragment(jQuery(elem), None, True):
                return refresh_fragment(jQuery(elem), None, False)

    if src_obj.hasClass("page-link"):
        ajax_submit(src, _on_data)
    else:
        ajax_get(href2, _on_data)


def popup_min_max(elm, max=True):
    elem = jQuery(elm)
    if elem.hasClass("modal-dialog"):
        popup = elem
    else:
        popup = elem.closest(".modal-dialog")
    if popup.length > 0:
        minimize = popup.find(".minimize")
        maximize = popup.find(".maximize")
        if minimize.length > 0:
            if max:
                minimize.show()
            else:
                minimize.hide()
        if maximize.length > 0:
            if max:
                maximize.hide()
            else:
                maximize.show()
        if max:
            popup.addClass("modal-fullscreen")
            popup.addClass("modal-open")
        else:
            popup.removeClass("modal-fullscreen")
            popup.removeClass("modal-open")
        jQuery(window).trigger("resize")


def popup_minimize(elem):
    return popup_min_max(elem, False)


window.popup_minimize = popup_minimize


def popup_maximize(elem):
    return popup_min_max(elem, True)


window.popup_maximize = popup_maximize


jQuery.fn.modal.Constructor.prototype.enforceFocus = _none
