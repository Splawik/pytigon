__pragma__("alias", "jquery_is", "js_is")

#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

from pytigon_js.tabmenu import Page, get_menu, on_menu_href
from pytigon_js.tbl import init_table, datatable_onresize
from pytigon_js.tools import (
    can_popup,
    corect_href,
    get_table_type,
    ajax_get,
    ajax_post,
    ajax_load,
    ajax_submit,
    load_css,
    load_js,
    load_many_js,
    history_push_state,
    mount_html,
    register_fragment_init_fun,
    register_mount_fun,
    remove_page_from_href,
    get_and_run_script,
    register_resize_fun,
    process_resize,
    fragment_init
)
from pytigon_js.offline import service_worker_and_indexedDB_test, install_service_worker
from pytigon_js.db import sync_and_run
from pytigon_js.component import GlobalBus
from pytigon_js.events import register_global_event


window.PS = None
window.MOUNTED_COMPONENTS = 0

window.GLOBAL_BUS = GlobalBus()

window.START_MENU_ID = None


def _on_resize(event, target_element):
    datatable_onresize()

register_global_event("shown.bs.tab", _on_resize, "#tabs2")

def _on_timeout_resize(evetn, target_element):
    window.setTimeout(datatable_onresize, 300)

register_global_event("expanded.pushMenu", _on_timeout_resize, None)
register_global_event("collapsed.pushMenu", _on_timeout_resize, None)

#register_global_event("submit", on_login_submit, "form.login-form")
#register_global_event("submit", form_on_submit,  "form")


def _on_key(e):
    if e.which == 13:
        elem = jQuery(e.target)
        if elem.prop("tagName") != "TEXTAREA":
            form = elem.closest("form")
            if form.length > 0:
                if form.hasClass("DialogForm"):
                    e.preventDefault()
                    on_edit_ok(False, form)
                    return

register_global_event("keypress", _on_key, None)


#jQuery("#tabs2_content").on("submit", "form", form_on_submit)
#jQuery("#dialog-form-modal").on("submit", "form", form_on_submit)
#jQuery("#search").on("submit", "form", form_on_submit)
# jQuery("#wiki_start").on("submit", "form", _on_submit)
#jQuery("#body_desktop").on("submit", "form", form_on_submit)


def dom_content_loaded():
    #if window.APPLICATION_TEMPLATE != "traditional":
    #    pos = jQuery(".menu-href.btn-warning")
    #    if pos.length > 0:
    #        elem = jQuery("#a_" + pos.closest("div.tab-pane").attr("id"))
    #        elem.tab("show")
    #    else:
    #        elem = jQuery(".first_pos")
    #        if elem.length>0:
    #            elem.tab("show")
    #else:
    #    id = int(window.START_MENU_ID) + 1
    #    elem = jQuery("#tabs a:eq(" + id + ")")
    #    elem.tab("show")

    #def _on_logout_click():
    #    window.location = jQuery(this).attr("action")

    #jQuery("#logout").on("click", _on_logout_click)


    #def _on_tabs_click(e):
    #    e.preventDefault()
    #    jQuery(this).tab("show")
    #    # jQuery(jQuery(this).prop("hash")).perfectScrollbar()
    #
    ##jQuery("#tabs a").click(_on_tabs_click)

    #def _on_resize(e):
    #    datatable_onresize()

    #jQuery("#tabs2").on("shown.bs.tab", _on_resize)

    #def _on_timeout(e):
    #    window.setTimeout(datatable_onresize, 300)

    #jQuery("body").on("expanded.pushMenu collapsed.pushMenu", _on_timeout)


    #init2
    if jQuery("#dialog-form-modal").length > 0:
        jQuery(document).ajaxError(_on_error)

        def _on_hide(e):
            mount_html(
                jQuery(this).find("div.dialog-data"),
                "<div class='alert alert-info' role='alert'>Sending data - please wait</div>",
                False,
                False,
            )

        jQuery("div.dialog-form").on("hide.bs.modal", _on_hide)

        def _local_fun():
            console.log("collapsed")

        jQuery(".navbar-ex1-collapse").on("hidden.bs.collapse", _local_fun)

        if window.APPLICATION_TEMPLATE == "traditional":
            window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"))
            # __new__(Vue({'el': '#body_body'}))
        else:
            #if window.APPLICATION_TEMPLATE == "modern":
            #    txt = jQuery(".page").html()
            #    txt2 = jQuery.trim(txt)
            #    if txt2:
            #        txt = jQuery.trim(jQuery(".page")[0].outerHTML)
            #        jQuery(".page").remove()
            #        menu = get_menu()
            #        menu.new_page(jQuery("title").text(), txt, window.location.href)
            #else:
            window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"))
            #if window.APPLICATION_TEMPLATE == "to_print":
            #    __new__(Vue({"el": "#body_desktop"}))


def app_init(
    prj_name,
    application_template,
    menu_id,
    lang,
    base_path,
    base_fragment_init,
    component_init,
    offline_support,
    start_page,
    gen_time,
    callback=None,
):

    moment.locale(lang)
    window.ACTIVE_PAGE = None
    window.PRJ_NAME = prj_name
    window.APPLICATION_TEMPLATE = application_template
    window.MENU = None
    window.PUSH_STATE = True
    if base_path:
        window.BASE_PATH = base_path
    else:
        window.BASE_PATH = ""
    window.WAIT_ICON = None
    window.WAIT_ICON2 = False
    window.START_MENU_ID = menu_id
    window.BASE_FRAGMENT_INIT = base_fragment_init
    window.COUNTER = 1
    window.EDIT_RET_FUNCTION = None
    window.RET_CONTROL = None
    window.COMPONENT_INIT = component_init
    window.LANG = lang
    window.GEN_TIME = gen_time

    document.addEventListener("DOMContentLoaded", dom_content_loaded)

    #if jQuery("#dialog-form-modal").length == 0:
    #    jQuery("body").on("submit", "form.login-form", on_login_submit)
    #    return

    if offline_support:
        if navigator.onLine and service_worker_and_indexedDB_test():
            install_service_worker()

    def _on_sync(status):
        if status == "OK-refresh":
            location.reload()

    sync_and_run("sys", _on_sync)

    #if not reinit:
    #    sync_and_run("sys", _on_sync)
    #jQuery(window).resize(datatable_onresize)

    register_resize_fun(datatable_onresize)
    jQuery(window).resize(process_resize)


    #jQuery("#tabs2_content").on("submit", "form", form_on_submit)
    #jQuery("#dialog-form-modal").on("submit", "form", form_on_submit)
    #jQuery("#search").on("submit", "form", form_on_submit)
    ##jQuery("#wiki_start").on("submit", "form", _on_submit)
    #jQuery("#body_desktop").on("submit", "form", form_on_submit)
    ##fragment_init(jQuery("#body_desktop"))

    #def _on_key(e):
    #    if e.which == 13:
    #        elem = jQuery(e.target)
    #        if elem.prop("tagName") != "TEXTAREA":
    #            form = elem.closest("form")
    #            if form.length > 0:
    #                if form.hasClass("DialogForm"):
    #                    e.preventDefault()
    #                    on_edit_ok(False, form)
    #                    return
    #
    #jQuery(document).keypress(_on_key)

    # jQuery('#tabs2_content').on("submit", "button", _on_submit)
    # jQuery('#dialog-form-modal').on("submit", "button", _on_submit)

    # init_popup_events()

    #process_on_click(EVENT_TAB)

    def _init_start_wiki_page():
        if (
            start_page
            and start_page != "None"
            and window.location.pathname == base_path
        ):

            def _on_load(responseText, status, response):
                print("_init_strart_wiki_page::_on_load")
                #pass

            ajax_load(
                #jQuery("#wiki_start"),
                jQuery("#body_desktop"),
                base_path + start_page + "?only_content&schtml=1",
                _on_load,
            )

    window.init_start_wiki_page = _init_start_wiki_page
    _init_start_wiki_page()

    # alert(window.location.pathname)
    # alert(base_path)
    if hasattr(window, "init_callback"):
        window.init_callback()

    jQuery.fn.editable.defaults.mode = 'inline'
    jQuery.fn.combodate.defaults['maxYear'] = 2025


def _on_error(request, settings):
    if window.WAIT_ICON:
        window.WAIT_ICON.stop()
        window.WAIT_ICON = None
    if window.WAIT_ICON2:
        jQuery("#loading-indicator").hide()
        window.WAIT_ICON2 = False

    if settings.status == 200:
        return

    if settings.responseText:
        start = settings.responseText.indexOf("<body>")
        end = settings.responseText.lastIndexOf("</body>")
        if start > 0 and end > 0:
            mount_html(
                jQuery("#dialog-data-error"),
                settings.responseText.substring(start + 6, end - 1),
            )
            jQuery("#dialog-form-error").modal()
        else:
            mount_html(jQuery("#dialog-data-error"), settings.responseText)
            jQuery("#dialog-form-error").modal()
    # else:
    #    jQuery("#dialog-data-error").html("ERROR")
    #    jQuery('#dialog-form-error').modal()


def init2():
    if jQuery("#dialog-form-modal").length > 0:
        jQuery(document).ajaxError(_on_error)

        def _on_hide(e):
            mount_html(
                jQuery(this).find("div.dialog-data"),
                "<div class='alert alert-info' role='alert'>Sending data - please wait</div>",
                False,
                False,
            )

        jQuery("div.dialog-form").on("hide.bs.modal", _on_hide)

        def _local_fun():
            console.log("collapsed")

        jQuery(".navbar-ex1-collapse").on("hidden.bs.collapse", _local_fun)

        if window.APPLICATION_TEMPLATE == "traditional":
            window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"))
            # __new__(Vue({'el': '#body_body'}))
        else:
            #if window.APPLICATION_TEMPLATE == "modern":
            #    txt = jQuery(".page").html()
            #    txt2 = jQuery.trim(txt)
            #    if txt2:
            #        txt = jQuery.trim(jQuery(".page")[0].outerHTML)
            #        jQuery(".page").remove()
            #        menu = get_menu()
            #        menu.new_page(jQuery("title").text(), txt, window.location.href)
            #else:
            window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"))
            #if window.APPLICATION_TEMPLATE == "to_print":
            #    __new__(Vue({"el": "#body_desktop"}))


#window.init2 = init2

def jquery_ready():
    pass
#    init2()


#def on_new_tab(url, elem, e):
#    title = jQuery(e.currentTarget).attr("title")
#    url2 = url.split("?")[0]
#    if not title:
#        if len(url2) > 16:
#            title = "..." + url2[-13:]
#        else:
#            title = url2
#    return on_menu_href(elem, title, url)


## target:
## _blank: new browser window (pdf) - default action
## _parent: new app tab
## _top: replace current app window
## _self: replace current frame
## popup: new popup window
## popup_edit: new popup window
## popup_info: new popup window
## popup_delete: new popup window
## inline_edit: new popup window
## inline_info: new popup window
## inline_delete: new popup window
## inline: new inline window
## none, get request (no gui)
## refresh_obj: replace current object
## refresh_page: replace current page (like _self)
## refresh_app: replace current app (like _top)

#EVENT_TAB = [
#    # target, class, get only content, get only tab, function
#    ("*", "get_tbl_value", True, False, on_get_tbl_value),
#    ("*", "new_tbl_value", True, False, on_new_tbl_value),
#    ("*", "get_row", True, False, on_get_row),
#    ("popup_edit", "*", True, False, on_popup_edit_new),
#    ("popup_info", "*", True, False, on_popup_info),
#    ("popup_delete", "*", True, False, on_popup_delete),
#    ("inline", "*", True, False, on_popup_inline),
#    ("_top", "*", True, False, on_new_tab),
#    ("_top2", "*", True, False, on_new_tab),
#    ("refresh_obj", "*", True, False, refresh_current_object),
#    ("refresh_page", "*", True, False, refresh_current_page),
#    ("refresh_app", "*", False, False, refresh_current_app),
#    ("run_script", "*", False, False, get_and_run_script),
#    ("null", "*", False, False, only_get),
#    # ('*', 'popup_info', True, False, on_popup_info),
#    # ('*', 'popup_delete', True, False, on_popup_delete),
#    # ('*', 'popup_inline', True, False, on_popup_inline),
#    # ('*', 'popup', True, False, on_popup_edit_new),
#]


def standard_on_data(src_obj, href):
    def _standard_on_data(data):
        nonlocal href, src_obj

        if data and "_parent_refr" in data:
            refresh_fragment(src_obj)
        else:
            if window.APPLICATION_TEMPLATE == "modern":
                mount_html(window.ACTIVE_PAGE.page, data)
                window.ACTIVE_PAGE.set_href(href)
            else:
                mount_html(jQuery("#body_desktop"), data)
            window.ACTIVE_PAGE.set_href(href)
            get_menu().get_active_item().url = href
            if window.PUSH_STATE:
                history_push_state("title", href)

    return _standard_on_data


window.standard_on_data = standard_on_data


def _on_popstate(e):
    if e.state:
        window.PUSH_STATE = False
        if window.APPLICATION_TEMPLATE == "modern":
            menu = get_menu().activate(e.state, False)
        else:
            x = e.state
            mount_html(jQuery("#body_desktop"), LZString.decompress(x[0]))
            window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"))
            window.ACTIVE_PAGE.set_href(document.location)

            if window.APPLICATION_TEMPLATE == "standard":
                jQuery("a.menu-href").removeClass("btn-warning")
                jQuery("#" + x[1]).addClass("btn-warning")
        window.PUSH_STATE = True
    else:
        if window.APPLICATION_TEMPLATE == "modern":
            pass
        else:
            mount_html(jQuery("#body_desktop"), "", False, False)
            window.ACTIVE_PAGE = None
            if window.APPLICATION_TEMPLATE == "standard":
                jQuery("a.menu-href").removeClass("btn-warning")


window.addEventListener("popstate", _on_popstate, False)
