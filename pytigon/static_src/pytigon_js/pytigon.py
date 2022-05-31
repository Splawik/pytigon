# from pytigon_js.tabmenu import Page, get_menu
# from pytigon_js.offline import service_worker_and_indexedDB_test, install_service_worker
# from pytigon_js.db import sync_and_run
# from pytigon_js.component import GlobalBus
# from pytigon_js.events import register_global_event
# from pytigon_js.ajax_region import ajax_load, mount_html
# from pytigon_js.widget import *

window.PS = None
window.MOUNTED_COMPONENTS = 0
window.GLOBAL_BUS = GlobalBus()
window.START_MENU_ID = None


def _on_key(self, e):
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


def dom_content_loaded():
    mount_html(document.querySelector("section.body-body"), None)


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

    # if APPLICATION_TEMPLATE == "traditional":
    #    document.addEventListener("DOMContentLoaded", dom_content_loaded)

    if offline_support:
        if navigator.onLine and service_worker_and_indexedDB_test():
            install_service_worker()

    def _on_sync(status):
        if status == "OK-refresh":
            location.reload()

    sync_and_run("sys", _on_sync)

    def _init_start_wiki_page():
        if (
            start_page
            and start_page != "None"
            and window.location.pathname == base_path
        ):

            def _on_load(responseText, status, response):
                print("_init_strart_wiki_page::_on_load")
                # pass

            ajax_load(
                # jQuery("#wiki_start"),
                # jQuery("#body_desktop"),
                document.querySelector("#body_desktop"),
                base_path + start_page + "?only_content&schtml=1",
                _on_load,
            )

    window.init_start_wiki_page = _init_start_wiki_page
    _init_start_wiki_page()

    if hasattr(window, "init_callback"):
        window.init_callback()

    jQuery.fn.editable.defaults.mode = "inline"
    jQuery.fn.combodate.defaults["maxYear"] = 2025

    # activate_menu()
    desktop = document.getElementById("body_desktop")
    if desktop:
        mount_html(desktop, None, None)

    if window.location.search:
        href = window.location.search.split("=")[1]
        objects = Array.prototype.slice.call(document.querySelectorAll("a"))
        for obj in objects:
            if obj.href and obj.classList.contains("menu-href"):
                if href in obj.href:
                    obj.click()
                    break

        # try:
        #    href = window.location.search.split("=")[1]
        #
        #    def _callback(data):
        #        return get_menu().on_menu_href(None, data, "", "", None)
        #
        #    ajax_get(href, _callback)

        # except:
        #    pass


window.app_init = app_init


def activate_menu():
    pathname = window.location.pathname
    if pathname.startswith(window.BASE_PATH):
        pathname2 = pathname[len(window.BASE_PATH) :]
    else:
        pathname2 = pathname

    if pathname2:
        menu = document.querySelector("sys-sidebarmenu")
        # if menu:
        #    menu.activate_url(pathname2)
        # else:
        a_tab = Array.prototype.slice.call(document.querySelectorAll("a.menu-href"))
        for a in a_tab:
            if a.hasAttribute("href"):
                href = a.getAttribute("href").split("?")[0]
                if href.startswith("/" + pathname2):
                    if menu:
                        li = a.closest("li.treeview")
                        if li and not li.classList.contains("active"):
                            a = li.querySelector("a")
                            if a:
                                event = document.createEvent("MouseEvents")
                                event.initMouseEvent(
                                    "click",
                                    True,
                                    True,
                                    window,
                                    1,
                                    0,
                                    0,
                                    0,
                                    0,
                                    False,
                                    False,
                                    False,
                                    False,
                                    0,
                                    None,
                                )
                                a.dispatchEvent(event)
                    else:
                        div = a.closest(".tab-tab")
                        if div:
                            id_elem = "a_" + div.id
                            x = document.getElementById(id_elem)
                            if x:
                                jQuery(x).tab("show")


window.activate_menu = activate_menu


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
            if window.hasOwnProperty("bootstrap"):
                d = bootstrap.Modal(document.getElementById("dialog-form-error"))
                d.hide()
            else:
                jQuery("#dialog-form-error").modal()
        else:
            mount_html(jQuery("#dialog-data-error"), settings.responseText)
            if window.hasOwnProperty("bootstrap"):
                d = bootstrap.Modal(document.getElementById("dialog-form-error"))
                d.hide()
            else:
                jQuery("#dialog-form-error").modal()


def jquery_ready():
    pass


window.jquery_ready = jquery_ready


def _on_popstate(self, e):
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
