__pragma__("alias", "jquery_is", "js_is")

#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'

from page import Page
from tabmenuitem import TabMenuItem
from tabmenu import get_menu
from popup import (
    on_get_tbl_value,
    on_new_tbl_value,
    on_get_row,
    on_popup_edit_new,
    on_popup_inline,
    on_popup_info,
    on_popup_delete,
    on_cancel_inline,
    refresh_fragment,
    on_edit_ok,
    on_delete_ok,
    ret_ok,
    refresh_current_object,
    refresh_current_page,
    refresh_current_app,
    only_get,
)
from tbl import init_table, datatable_onresize
from tools import (
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
    process_resize
)
from offline import service_worker_and_indexedDB_test, install_service_worker
from db import sync_and_run
from widget import img_field
from click_process import process_on_click, process_href

window.PS = None
window.MOUNTED_COMPONENTS = 0


window.REINIT = None

def app_reinit():
    if window.REINIT:
        return app_init(
            window.REINIT[0],
            window.REINIT[1],
            window.REINIT[2],
            window.REINIT[3],
            window.REINIT[4],
            window.REINIT[5],
            window.REINIT[6],
            window.REINIT[7],
            window.REINIT[8],
            window.REINIT[9]
        )

window.app_reinit = app_reinit

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
    callback=None
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
    window.MENU_ID = 0
    window.BASE_FRAGMENT_INIT = base_fragment_init
    window.COUNTER = 1
    window.EDIT_RET_FUNCTION = None
    window.RET_CONTROL = None
    window.COMPONENT_INIT = component_init
    window.LANG = lang
    window.GEN_TIME = gen_time

    if jQuery("#dialog-form-modal").length == 0:
        window.REINIT = [
            prj_name,
            application_template,
            menu_id,
            lang,
            base_path,
            base_fragment_init,
            component_init,
            offline_support,
            start_page,
            gen_time
        ]

        def _on_login_submit(e):
            self = jQuery(this)
            e.preventDefault()

            def _on_login_submit2(data):
                nonlocal href, self

                window.location.pathname = window.BASE_PATH

                jQuery('body').removeClass('login_background')

                start = data.indexOf("<body>")
                end = data.lastIndexOf("</body>")

                if start > 0 and end > 0:
                    title = jQuery("<div>" + data + "</div>").find("title").text()
                    data = data.substring(start + 6, end - 1)
                    data = "<title>" + title +"</title>" + data + ""
                mount_html(jQuery('body'), data, False)
                app_reinit()
                window.init2()
                if window.window.BASE_FRAGMENT_INIT:
                    window.BASE_FRAGMENT_INIT()
                if window.WAIT_ICON:
                    window.WAIT_ICON.stop()
                if window.WAIT_ICON2:
                    jQuery("#loading-indicator").hide()
                    window.WAIT_ICON2 = False

            ajax_submit(jQuery(this), _on_login_submit2)

        jQuery("body").on("submit", "form.login-form", _on_login_submit)

        return


    if offline_support:
        if navigator.onLine and service_worker_and_indexedDB_test():
            install_service_worker()

    def _on_sync(status):
        if status == "OK-refresh":
            location.reload()

    sync_and_run("sys", _on_sync)
    #jQuery(window).resize(datatable_onresize)
    jQuery(window).resize(process_resize)
    register_resize_fun(datatable_onresize)

    def _on_submit(e):
        self = jQuery(this)
        if jQuery(this).hasClass("DialogForm"):
            e.preventDefault()
            on_edit_ok(False, jQuery(this))
            return

        if jQuery(this).attr("target") == "_blank":
            jQuery(this).attr("enctype", "multipart/form-data").attr(
                "encoding", "multipart/form-data"
            )
            return True

        if jQuery(this).attr("target") == "_self":
            return True

        if jQuery(this).attr("target") == "refresh_obj":
            if refresh_fragment(jQuery(this), None, True, None, True):
                return False

        data = jQuery(this).serialize()

        if data and "pdf=on" in data:
            jQuery(this).attr("target", "_blank")
            jQuery(this).attr("enctype", "multipart/form-data").attr(
                "encoding", "multipart/form-data"
            )
            return True
        if data and "odf=on" in data:
            jQuery(this).attr("target", "_blank")
            jQuery(this).attr("enctype", "multipart/form-data").attr(
                "encoding", "multipart/form-data"
            )
            return True

        e.preventDefault()

        submit_button = jQuery(this).find('button[type="submit"]')
        if submit_button.length > 0:
            submit_button.attr("data-style", "zoom-out")
            submit_button.attr("data-spinner-color", "#FF0000")
            window.WAIT_ICON = Ladda.create(submit_button[0])
            window.WAIT_ICON.start()
        else:
            window.WAIT_ICON2 = True
            jQuery("#loading-indicator").show()

        href = jQuery(this).attr("action")
        if href:
            jQuery(this).attr("action", corect_href(remove_page_from_href(href)))

        def _on_submit2(data):
            nonlocal href, self
            if window.ACTIVE_PAGE:
                mount_html(window.ACTIVE_PAGE.page, data)
            else:
                _on_menu_href(self, self.attr("title"), None, data)

            if window.WAIT_ICON:
                window.WAIT_ICON.stop()
            if window.WAIT_ICON2:
                jQuery("#loading-indicator").hide()
                window.WAIT_ICON2 = False

        ajax_submit(jQuery(this), _on_submit2)

    jQuery("#tabs2_content").on("submit", "form", _on_submit)
    jQuery("#dialog-form-modal").on("submit", "form", _on_submit)
    jQuery("#search").on("submit", "form", _on_submit)


    # jQuery('#menu').perfectScrollbar()

    if jQuery("#menu").length > 0:
        window.PS = __new__(PerfectScrollbar("#menu"))

        def _on_resize():
            window.PS.js_update()

        jQuery(window).resize(_on_resize)

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

    jQuery(document).keypress(_on_key)

    # jQuery('#tabs2_content').on("submit", "button", _on_submit)
    # jQuery('#dialog-form-modal').on("submit", "button", _on_submit)

    # init_popup_events()

    process_on_click(EVENT_TAB)

    if can_popup():

        def _local_fun():
            nonlocal menu_id
            # jQuery("#tabs").tabdrop()
            # jQuery("#tabs2").tabdrop()
            if window.APPLICATION_TEMPLATE != "traditional":
                pos = jQuery(".menu-href.btn-warning")
                if pos.length > 0:
                    elem = jQuery("#a_" + pos.closest("div.tab-pane").attr("id"))
                    elem.tab("show")
                else:
                    elem = jQuery(".first_pos")
                    elem.tab("show")
            else:
                id = int(menu_id) + 1
                elem = jQuery("#tabs a:eq(" + id + ")")
                elem.tab("show")

            # jQuery(elem.prop("hash")).perfectScrollbar()

            def _on_menu_click(e):
                if window.APPLICATION_TEMPLATE != "traditional":
                    e.preventDefault()

                    toggler = jQuery("#topmenu").find(".navbar-toggler")
                    if toggler and toggler.jquery_is(":visible"):
                        obj = this

                        def _on_collapse():
                            _on_menu_href(obj)
                            jQuery("#navbar-ex1-collapse").off(
                                "hidden.bs.collapse", _on_collapse
                            )

                        jQuery("#navbar-ex1-collapse").on(
                            "hidden.bs.collapse", _on_collapse
                        )
                        jQuery("#navbar-ex1-collapse").collapse("hide")
                    else:
                        _on_menu_href(this)

            jQuery("body").on("click", "a.menu-href", _on_menu_click)

            # def _on_submit(e):
            #    e.preventDefault()
            #    on_edit_ok(False, jQuery(this))
            # jQuery('body').on('submit', 'form.DialogForm', _on_submit)

            def _on_logout_click():
                window.location = jQuery(this).attr("action")

            jQuery("#logout").on("click", _on_logout_click)

            def _on_sysmenu_click():
                window.location = jQuery(this).attr("action")

            jQuery(".system_menu").on("click", _on_sysmenu_click)

            def _on_tabs_click(e):
                e.preventDefault()
                jQuery(this).tab("show")
                # jQuery(jQuery(this).prop("hash")).perfectScrollbar()

            jQuery("#tabs a").click(_on_tabs_click)

            def _on_resize(e):
                datatable_onresize()

            jQuery("#tabs2").on("shown.bs.tab", _on_resize)

            def _on_timeout(e):
                window.setTimeout(datatable_onresize, 300)

            jQuery("body").on("expanded.pushMenu collapsed.pushMenu", _on_timeout)

            # jQuery(window).resize(datatable_onresize)

        jQuery(_local_fun)

    def _init_start_wiki_page():
        if (
            start_page
            and start_page != "None"
            and window.location.pathname == base_path
        ):

            def _on_load(responseText, status, response):
                pass

            ajax_load(
                jQuery("#wiki_start"),
                base_path + start_page + "?only_content&schtml=1",
                _on_load,
            )

    window.init_start_wiki_page = _init_start_wiki_page
    _init_start_wiki_page()

    # alert(window.location.pathname)
    # alert(base_path)
    if hasattr(window, "init_callback"):
        window.init_callback()


#'standard' 'simple', 'traditional', 'mobile', 'tablet', 'hybrid'
def _on_menu_href(elem, title=None, url=None, txt=None):
    if window.APPLICATION_TEMPLATE != "traditional":
        if not title:
            title = jQuery.trim(jQuery(elem).text())
        if txt:
            value = jQuery("<div>" + txt + "</div>").find("head").find("title").text()
            if value:
                title = value

        menu = get_menu()
        classname = jQuery(elem).attr("class")
        if classname and "btn" in classname:
            if window.WAIT_ICON:
                window.WAIT_ICON.stop()
            jQuery(elem).attr("data-style", "zoom-out")
            jQuery(elem).attr("data-spinner-color", "#FF0000")
            window.WAIT_ICON = Ladda.create(elem)
        else:
            window.WAIT_ICON = None

        if window.APPLICATION_TEMPLATE == "modern" and menu.is_open(title):
            menu.activate(title)
        else:
            if url:
                href = url
            else:
                href = jQuery(elem).attr("href")
            href2 = corect_href(href)

            def _on_new_win(data):
                nonlocal href, href2, title

                jQuery("#wiki_start").hide()

                if window.APPLICATION_TEMPLATE == "modern":
                    id = menu.new_page(title, data, href2)
                else:
                    mount_html(jQuery("#body_body"), data)
                    window.ACTIVE_PAGE = Page(0, jQuery("#body_body"))
                    window.ACTIVE_PAGE.set_href(href2)
                    if window.PUSH_STATE:
                        id = jQuery(elem).attr("id")
                        if not id:
                            id = "menu_id_" + window.MENU_ID
                            window.MENU_ID = window.MENU_ID + 1
                            jQuery(elem).attr("id", id)
                        history_push_state(title, href, [data, id])

                if window.WAIT_ICON:
                    window.WAIT_ICON.stop()
                    window.WAIT_ICON = None

                if window.WAIT_ICON2:
                    jQuery("#loading-indicator").hide()
                    window.WAIT_ICON2 = False

            if (
                window.APPLICATION_TEMPLATE == "standard"
                and classname
                and "btn" in classname
            ):
                jQuery("a.menu-href").removeClass("btn-warning")
                jQuery(elem).addClass("btn-warning")

            if txt:
                _on_new_win(txt)
            else:
                if window.WAIT_ICON:
                    window.WAIT_ICON.start()
                else:
                    window.WAIT_ICON2 = True
                    jQuery("#loading-indicator").show()
                ajax_get(href2, _on_new_win)
                jQuery(".navbar-ex1-collapse").collapse("hide")

        jQuery(".auto-hide").trigger("click")

        return False


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
            window.ACTIVE_PAGE = Page(0, jQuery("#body_body"))
            # __new__(Vue({'el': '#body_body'}))
        else:
            if window.APPLICATION_TEMPLATE == "modern":
                txt = jQuery(".page").html()
                txt2 = jQuery.trim(txt)
                if txt2:
                    txt = jQuery.trim(jQuery(".page")[0].outerHTML)
                    jQuery(".page").remove()
                    menu = get_menu()
                    menu.new_page(jQuery("title").text(), txt, window.location.href)
            else:
                window.ACTIVE_PAGE = Page(0, jQuery("#body_body"))
                if window.APPLICATION_TEMPLATE == "to_print":
                    __new__(Vue({"el": "#body_body"}))


window.init2 = init2

def jquery_ready():
    init2()


def on_new_tab(url, elem, e):
    title = jQuery(e.currentTarget).attr("title")
    url2 = url.split("?")[0]
    if not title:
        if len(url2) > 16:
            title = "..." + url2[-13:]
        else:
            title = url2
    return _on_menu_href(elem, title, url)


## target:
## _blank: new browser window (pdf) - default action
## _parent: default action
## _top: new app tab
## _self: replace current page
## popup_edit: new popup window
## popup_info: new popup window
## popup_delete: new popup window
## inline: new inline window
## none, get request (no gui)
## refresh_obj: replace current object
## refresh_page: replace current page (like _self)
## refresh_app: replace current app

EVENT_TAB = [
    # target, class, get only content, get only tab, function
    ("*", "get_tbl_value", True, False, on_get_tbl_value),
    ("*", "new_tbl_value", True, False, on_new_tbl_value),
    ("*", "get_row", True, False, on_get_row),
    ("popup_edit", "*", True, False, on_popup_edit_new),
    ("popup_info", "*", True, False, on_popup_info),
    ("popup_delete", "*", True, False, on_popup_delete),
    ("inline", "*", True, False, on_popup_inline),
    ("_top", "*", True, False, on_new_tab),
    ("_top2", "*", True, False, on_new_tab),
    ("refresh_obj", "*", True, False, refresh_current_object),
    ("refresh_page", "*", True, False, refresh_current_page),
    ("refresh_app", "*", False, False, refresh_current_app),
    ("run_script", "*", False, False, get_and_run_script),
    ("null", "*", False, False, only_get),
    # ('*', 'popup_info', True, False, on_popup_info),
    # ('*', 'popup_delete', True, False, on_popup_delete),
    # ('*', 'popup_inline', True, False, on_popup_inline),
    # ('*', 'popup', True, False, on_popup_edit_new),
]


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
                mount_html(jQuery("#body_body"), data)
            window.ACTIVE_PAGE.set_href(href)
            get_menu().get_active_item().url = href
            if window.PUSH_STATE:
                history_push_state("title", href)

    return _standard_on_data


window.standard_on_data = standard_on_data

# def init_popup_events(elem=None):
#     def _on_click(e):
#         nonlocal EVENT_TAB
#
#         target = jQuery(e.currentTarget).attr('target')
#         src_obj = jQuery(this)
#
#         if target == "_blank" or target == '_parent':
#             return True
#
#         href = jQuery(this).attr("href")
#         if href and '#' in href:
#             return True
#
#         for pos in EVENT_TAB:
#             if jQuery(this).hasClass(pos[0]):
#                 e.preventDefault()
#                 pos[1](this)
#                 return True
#
#         e.preventDefault()
#
#         if jQuery(e.currentTarget).attr('target') in ("_top", "_top2"):
#             title = jQuery(e.currentTarget).attr('title')
#             if not title:
#                 if len(href)>16:
#                     title = '...'+href[-13:]
#                 else:
#                     title = href
#             return _on_menu_href(this,title)
#
#         href2 = corect_href(href)
#
#         def _on_data(data):
#             nonlocal href, src_obj
#
#             if (data and "_parent_refr" in data) or target in ("refresh_obj", "refresh_page"):
#                 if target=="refresh_obj":
#                     if not refresh_fragment(src_obj, None, True):
#                         refresh_fragment(src_obj)
#                 else:
#                     refresh_fragment(src_obj)
#             else:
#                 if window.APPLICATION_TEMPLATE == 'modern':
#                     mount_html(window.ACTIVE_PAGE.page, data)
#                     window.ACTIVE_PAGE.set_href(href)
#                 else:
#                     mount_html(jQuery('#body_body'), data)
#                 window.ACTIVE_PAGE.set_href(href)
#                 get_menu().get_active_item().url = href
#                 if window.PUSH_STATE:
#                     history_push_state("title", href)
#         ajax_get(href2,_on_data)
#
#     if elem:
#         elem.on("click", "a", _on_click)
#     else:
#         jQuery('#tabs2_content').on("click", "a", _on_click)
#         jQuery('#dialog-form-modal').on("click", "a", _on_click)


def _on_popstate(e):
    if e.state:
        window.PUSH_STATE = False
        if window.APPLICATION_TEMPLATE == "modern":
            menu = get_menu().activate(e.state, False)
        else:
            x = e.state
            mount_html(jQuery("#body_body"), LZString.decompress(x[0]))
            window.ACTIVE_PAGE = Page(0, jQuery("#body_body"))
            window.ACTIVE_PAGE.set_href(document.location)

            if window.APPLICATION_TEMPLATE == "standard":
                jQuery("a.menu-href").removeClass("btn-warning")
                jQuery("#" + x[1]).addClass("btn-warning")
        window.PUSH_STATE = True
    else:
        if window.APPLICATION_TEMPLATE == "modern":
            pass
        else:
            mount_html(jQuery("#body_body"), "", False, False)
            window.ACTIVE_PAGE = None
            if window.APPLICATION_TEMPLATE == "standard":
                jQuery("a.menu-href").removeClass("btn-warning")


window.addEventListener("popstate", _on_popstate, False)
