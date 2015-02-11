APPLICATION_TEMPLATE = "standard";
ZORRO = true;
RET_BUFOR = null;
RET_OBJ = null;
IS_POPUP = false;
SUBWIN = false;
LANG = "en";
MENU = null;
ACTIVE_PAGE = null;
PUSH_STATE = true;
BASE_PATH = null;
function Page() {
    Page.prototype.__init__.apply(this, arguments);
}
Page.prototype.__init__ = function __init__(id, page){
    var self = this;
    self.id = id;
    self.page = page;
};

function TabMenuItem() {
    TabMenuItem.prototype.__init__.apply(this, arguments);
}
TabMenuItem.prototype.__init__ = function __init__(id, title, url, data){
    var self = this;
    if (typeof data === "undefined") data = null;
    self.id = id;
    self.title = title;
    self.url = url;
    self.data = data;
};

function Menu() {
    Menu.prototype.__init__.apply(this, arguments);
}
Menu.prototype.__init__ = function __init__(){
    var self = this;
    self.id = 0;
    self.titles = {};
};
Menu.prototype.is_open = function is_open(title){
    var self = this;
    if (_$rapyd$_in(title, self.titles) && self.titles[title]) {
        return true;
    } else {
        return false;
    }
};
Menu.prototype.activate = function activate(title, push_state){
    var self = this;
    if (typeof push_state === "undefined") push_state = true;
    var menu_item;
    menu_item = self.titles[title];
    jQuery(sprintf("#li_%s a", menu_item.id)).tab("show");
    if (push_state && PUSH_STATE) {
        history_push_state(menu_item.title, menu_item.url);
    }
};
Menu.prototype.new_page = function new_page(title, data, href){
    var self = this;
    var _id;
    _id = "tab" + self.id;
    self.titles[title] = new TabMenuItem(_id, title, href, data);
    jQuery("#tabs2").append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='glyphicon glyphicon-remove'></span></button></li>", [ _id, _id, title, _id ]));
    jQuery("#tabs2_content").append(sprintf("<div class='tab-pane' id='%s'></div>", _id));
    ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
    jQuery("#" + _id).html(data);
    if (PUSH_STATE) {
        history_push_state(title, href);
    }
    jQuery("#tabs2 a:last").tab("show");
    jQuery("#tabs2 a:last").on("shown.bs.tab", function(e) {
        var menu, menu_item;
        ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
        menu = get_menu();
        menu_item = menu.titles[jQuery.trim(e.target.text)];
        if (PUSH_STATE) {
            history_push_state(menu_item.title, menu_item.url);
        }
    });
    self.on_new_page(_id);
    jQuery(sprintf("#button_%s", _id)).click(function(event) {
        get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""));
    });
    self.id += 1;
    return _id;
};
Menu.prototype.remove_page = function remove_page(id){
    var self = this;
    jQuery.each(self.titles, function(index, value) {
        if (value && value.id === id) {
            self.titles[index] = null;
        }
    });
    jQuery(sprintf("#li_%s", id)).remove();
    jQuery(sprintf("#%s", id)).remove();
    jQuery("#tabs2 a:last").tab("show");
};
Menu.prototype.on_new_page = function on_new_page(id){
    var self = this;
    var table_type, paginator, pg, totalPages, options, paginate;
    table_type = get_table_type(jQuery("#" + id));
    paginator = get_page(jQuery("#" + id)).find(".pagination");
    if (paginator.length > 0) {
        paginate = true;
        pg = ACTIVE_PAGE.page.find(".pagination");
        totalPages = pg.attr("totalPages");
        options = {
            "totalPages": totalPages,
            "visiblePages": 3,
            "first": "<<",
            "prev": "<",
            "next": ">",
            "last": ">>",
            "onPageClick": function(event, page) {
                var form;
                form = pg.closest("form");
                if (form) {
                    function _on_new_page(data) {
                        pg.closest(".content").find(".tabsort tbody").html(jQuery(jQuery.parseHTML(data)).find(".tabsort tbody").html());
                    }
                    jQuery.ajax({
                        "type": "POST",
                        "url": pg.attr("href").replace("[[page]]", page) + "&hybrid=1",
                        "data": form.serialize(),
                        "success": _on_new_page
                    });
                }
            }
        };
        pg.twbsPagination(options);
    } else {
        paginate = false;
    }
    set_table_type(table_type, "#" + id + " .tabsort", paginate);
    self.activate_new_page(id);
};
Menu.prototype.activate_new_page = function activate_new_page(id){
    var self = this;
    $("#" + id + " a").on("click", function(e) {
        if ($(this).hasClass("menu-href") || $(this).attr("href") && _$rapyd$_in("/admin/", $(this).attr("href"))) {
            e.preventDefault();
            return _on_menu_href3(this);
        }
    });
};

function get_datatable_dy(selector) {
    var dy_table, dy_win, dy;
    dy_table = ACTIVE_PAGE.page.find(".tabsort_panel").offset().top;
    dy_win = jQuery(window).height();
    dy = dy_win - dy_table;
    if (dy < 100) {
        dy = 100;
    }
    return dy;
}
function set_table_type(table_type, selector, paginate) {
    var options;
    if (table_type === "" || table_type === "simple") {
    }
    if (table_type === "scrolled") {
        stick_header();
    }
    if (table_type === "datatable") {
        if (paginate) {
            options = get_datatable_options1();
            options["scrollY"] += get_datatable_dy(selector);
            jQuery(selector).dataTable(options);
        } else {
            options = get_datatable_options();
            options["scrollY"] += get_datatable_dy(selector);
            jQuery(selector).dataTable(options);
        }
    }
    if (table_type === "server-side") {
        options = get_datatable_options2();
        options["scrollY"] += get_datatable_dy(selector);
        jQuery(selector).dataTable(options);
    }
    jQuery(selector).on("click", "a.popup", _on_popup);
    jQuery(selector).on("click", "a.popup_info", _on_popup_info);
    jQuery(selector).on("click", "a.popup_delete", _on_popup_delete);
}
function get_menu() {
    if (!MENU) {
        MENU = new Menu();
    }
    return MENU;
}
function cmd_to_python(value) {
    document.title = ":";
    document.title = ":" + value;
}
function is_hybrid() {
    if (window.location.host === "127.0.0.2") {
        return true;
    } else {
        return false;
    }
}
function to_absolute_url(url) {
    if (url[0] === "/") {
        return window.location.protocol + "//" + window.location.host + url;
    } else {
        return window.location.protocol + "//" + window.location.host + window.location.pathname + "/" + url;
    }
}
function ret_submit() {
    RET_OBJ(RET_BUFOR, "OK");
}
function ajax_submit(form, func) {
    var queryString, RET_OBJ;
    if (is_hybrid()) {
        queryString = form.formSerialize();
        cmd_to_python("href_to_var|" + to_absolute_url(form.attr("action")) + "?" + queryString + "|RET_BUFOR");
        RET_OBJ = func;
        cmd_to_python("run_js|ret_submit();");
    } else {
        form.ajaxSubmit({
            success: func
        });
    }
}
function get_page(elem) {
    return elem.closest(".tab-pane");
}
function get_table_type(elem) {
    var tabsort;
    tabsort = get_page(elem).find(".tabsort");
    if (tabsort.length > 0) {
        return tabsort.attr("table_type");
    } else {
        return "";
    }
}
function can_popup() {
    if (IS_POPUP) {
        return false;
    } else {
        return true;
    }
}
function _dialog_loaded(is_modal) {
    date_init();
    jQuery("div.resizable").resizable();
    if (is_modal) {
        jQuery("div.dialog-form").modal();
        IS_POPUP = true;
    }
}
function on_dialog_load() {
}
function dialog_ex_load2(responseText, status, response) {
    if (status !== "error") {
        _dialog_loaded(false);
        on_dialog_load();
    }
}
function _on_popup() {
    var l;
    l = Ladda.create(this);
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + this.href + "|#dialog-data");
        jQuery("div.dialog-form").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data").load(jQuery(this).attr("href"), null, function(responseText, status, response) {
                if (status !== "error") {
                    _dialog_loaded(true);
                    on_dialog_load();
                }
            });
        } else {
            l.start();
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"));
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null, function(responseText, status, response) {
                if (status !== "error") {
                    _dialog_loaded(false);
                    on_dialog_load();
                }
                l.stop();
            });
        }
    }
    return false;
}
function _on_popup_info() {
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + this.href + "|#dialog-data-info");
        jQuery("div.dialog-form-info").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data-info").load(jQuery(this).attr("href"), null, function(responseText, status, response) {
                jQuery("div.dialog-form-info").modal();
            });
        } else {
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"));
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null);
        }
    }
    return false;
}
function _on_popup_delete() {
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + this.href + "|#dialog-data-delete");
        jQuery("div.dialog-form-delete").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data-delete").load(jQuery(this).attr("href"), null, function(responseText, status, response) {
                jQuery("div.dialog-form-delete").modal();
            });
        } else {
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"));
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null);
        }
    }
    return false;
}
function _on_error(request, settings) {
    var start, end;
    start = settings.responseText.indexOf("<body>");
    end = settings.responseText.lastIndexOf("</body>");
    if (start > 0 && end > 0) {
        jQuery("div.dialog-data-error").html(settings.responseText.substring(start + 6, end - 1));
        jQuery("div.dialog-form-error").modal();
    } else {
        jQuery("div.dialog-data-error").html(settings.responseText);
        jQuery("div.dialog-form-error").modal();
    }
}
function _refresh_win(responseText, form) {
    var subform, filter;
    if (_$rapyd$_in("RETURN_OK", responseText)) {
        subform = form.closest("div.inline_frame");
        if (subform.length > 0) {
            subform.find("div.frame-data-inner").load(subform.attr("href"), null);
        } else {
            filter = form.closest("div.content").find("form.TableFiltr");
            jQuery("div.dialog-form").fadeTo("slow", .5);
            if (filter.length > 0) {
                filter.attr("action", window.location.href);
                filter.submit();
            }
        }
    } else {
        jQuery("div.dialog-data").html(responseText);
    }
}
function on_edit_ok(form) {
    jQuery.ajax({
        "type": "POST",
        "url": form.attr("action"),
        "data": form.serialize(),
        "success": function(data) {
            _refresh_win(data, form);
        }
    });
    return false;
}
function on_delete_ok(form) {
    jQuery.ajax({
        "type": "POST",
        "url": form.attr("action"),
        "data": form.serialize(),
        "success": function(data) {
            _refresh_win(data, form);
        }
    });
    return false;
}
function on_cancel_inline() {
    jQuery(".inline_dialog").remove();
}
function date_init() {
    jQuery(".dateinput").datetimepicker({
        "pickTime": false,
        "format": "YYYY-MM-DD",
        "language": LANG
    });
    jQuery(".datetimeinput").datetimepicker({
        "format": "YYYY-MM-DD hh:mm",
        "language": "pl"
    });
}
function popup_init() {
    jQuery("div.dialog-form").on("hide.bs.modal", function(e) {
        IS_POPUP = false;
        jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>");
    });
    jQuery("a.popup").click(_on_popup);
    jQuery("a.popup_info").click(_on_popup_info);
    jQuery("a.popup_delete").click(_on_popup_delete);
}
function get_datatable_options() {
    var options;
    options = {
        "scrollY": -120,
        "paging": false,
        "responsive": true,
        "dom": "RC<\"clear\">frt",
        "language": {
            "url": "/static/jquery_plugins/datatables/i18n/Polish.lang"
        }
    };
    return options;
}
function get_datatable_options1() {
    var options;
    options = {
        "scrollY": -75,
        "paging": false,
        "responsive": true,
        "dom": "lrt",
        "bSort": false,
        "language": {
            "url": "/static/jquery_plugins/datatables/i18n/Polish.lang"
        }
    };
    return options;
}
function get_datatable_options2() {
    var options;
    options = {
        "scrollY": 0,
        "paging": false,
        "responsive": true,
        "dom": "lrt",
        "language": {
            "url": "/static/jquery_plugins/datatables/i18n/Polish.lang"
        }
    };
    return options;
}
function _on_menu_href(event) {
    return _on_menu_href2(this);
}
function _on_menu_href2(elem, title) {
    if (typeof title === "undefined") title = null;
    var menu, classname, l, href;
    if (APPLICATION_TEMPLATE !== "traditional") {
        if (!title) {
            title = jQuery.trim(jQuery(elem).text());
        }
        menu = get_menu();
        classname = jQuery(elem).attr("class");
        if (classname && _$rapyd$_in("btn", classname)) {
            l = Ladda.create(elem);
        } else {
            l = null;
        }
        if (APPLICATION_TEMPLATE === "modern" && menu.is_open(title)) {
            menu.activate(title);
        } else {
            href = jQuery(elem).attr("href");
            function _on_new_win(data) {
                var id;
                if (APPLICATION_TEMPLATE === "modern") {
                    id = menu.new_page(title, data, href);
                } else {
                    jQuery("#body_body").html(data);
                }
                popup_init();
                if (l) {
                    l.stop();
                }
            }
            if (_$rapyd$_in("?", href)) {
                href = href + "&hybrid=1";
            } else {
                href = href + "?hybrid=1";
            }
            if (APPLICATION_TEMPLATE === "standard" && _$rapyd$_in("btn", classname)) {
                jQuery("a.menu-href").removeClass("btn-warning").addClass("btn-info");
                jQuery(elem).removeClass("btn-info").addClass("btn-warning");
            }
            if (l) {
                l.start();
            }
            jQuery.ajax({
                "type": "GET",
                "url": href,
                "success": _on_new_win
            });
            jQuery(elem).closest(".dropdown-menu").dropdown("toggle");
            jQuery(".navbar-ex1-collapse").collapse("hide");
        }
        return false;
    }
}
function _on_menu_href3(elem) {
    var href;
    href = jQuery(elem).attr("href");
    jQuery.ajax({
        "type": "GET",
        "url": href,
        "success": function(data) {
            if (APPLICATION_TEMPLATE === "modern") {
                ACTIVE_PAGE.page.html(data);
                get_menu().activate_new_page(ACTIVE_PAGE.id);
            } else {
                jQuery("#body_body").html(data);
            }
        }
    });
}
function jquery_init(application_template, menu_id, lang, base_path) {
    var SUBWIN;
    APPLICATION_TEMPLATE = application_template;
    LANG = lang;
    BASE_PATH = base_path;
    if (IS_POPUP) {
        SUBWIN = true;
    } else {
        SUBWIN = false;
    }
    if (!SUBWIN) {
        jQuery(function() {
            jQuery("#menu_tabs").tabs();
            if (APPLICATION_TEMPLATE !== "traditional") {
                jQuery("#tabs a:eq(1)").tab("show");
            } else {
                jQuery("#tabs a:eq(" + menu_id + ")").tab("show");
            }
            jQuery("a.menu-href").click(_on_menu_href);
        });
    }
}
function jquery_ready() {
    var tabsort, table_type, paginator, paginate, txt2, txt, menu;
    jQuery(document).ajaxError(_on_error);
    date_init();
    if (APPLICATION_TEMPLATE === "traditional") {
        ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
        tabsort = JQuery(".tabsort");
        if (tabsort.length > 0) {
            table_type = tabsort.attr("table_type");
        } else {
            table_type = "";
        }
        paginator = JQuery(".paginator");
        if (paginator.length > 0) {
            paginate = true;
        } else {
            paginate = false;
        }
        set_table_type(table_type, ".tabsort", paginate);
    } else {
        if (APPLICATION_TEMPLATE === "modern") {
            txt = jQuery("#body_body").text();
            txt2 = jQuery.trim(txt);
            if (txt2) {
                txt = jQuery.trim(jQuery("#body_body").html());
                jQuery("#body_body").html("");
                menu = get_menu();
                menu.new_page(jQuery("title").text(), txt, BASE_PATH);
            }
        }
    }
}
function stick_resize() {
    var tbl, dy_table, dy_win, dy;
    tbl = ACTIVE_PAGE.page.find(".tbl_scroll");
    dy_table = tbl.offset().top;
    dy_win = dy_win = jQuery(window).height();
    dy = dy_win - dy_table;
    if (dy < 100) dy = 100;
    tbl.height(dy - 35);
}
function resize_win() {
    var tab_width, tab2;
    stick_resize();
    tab2 = [];
    tab_width = ACTIVE_PAGE.page.find("table[name='tabsort']").width();
    ACTIVE_PAGE.page.find(".tbl_header").width(tab_width);
    ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(function() {
        tab2.push(jQuery(this).width());
    });
    tab2 = tab2.reverse();
    ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
        jQuery(this).width(tab2.pop());
    });
}
function stick_header2() {
    var table, tab2, tab;
    tab = [];
    tab2 = [];
    jQuery("table.tabsort th").each(function() {
        tab.push($(this).width());
    });
    table = jQuery("<table id=\"tbl_header\" class=\"tabsort\" style=\"overflow-x: hidden;\"></table>");
    table.append(jQuery("table.tabsort thead"));
    jQuery("#tbl_scroll").before(table);
    jQuery("#tbl_header th").each(function() {
        tab2.push($(this).width());
    });
    tab2 = tab2.reverse();
    jQuery("table[name='tabsort'] tr:first td").each(function() {
        var x;
        x = tab2.pop();
        if (x > jQuery(this).width()) {
            jQuery(this).css("min-width", x);
        }
    });
    tab = tab.reverse();
    jQuery("#tbl_header th").each(function() {
        jQuery(this).width(tab.pop());
    });
    jQuery(window).resize(resize_win);
    resize_win();
}
function stick_header() {
    var table, tab2, tab;
    tab = [];
    tab2 = [];
    ACTIVE_PAGE.page.find("table.tabsort th").each(function() {
        tab.push($(this).width());
    });
    table = jQuery("<table class=\"tabsort tbl_header\" style=\"overflow-x: hidden;\"></table>");
    table.append(ACTIVE_PAGE.page.find("table.tabsort thead"));
    ACTIVE_PAGE.page.find(".tbl_scroll").before(table);
    ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
        tab2.push($(this).width());
    });
    tab2 = tab2.reverse();
    ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(function() {
        var x;
        x = tab2.pop();
        if (x > jQuery(this).width()) {
            jQuery(this).css("min-width", x);
        }
    });
    tab = tab.reverse();
    ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
        jQuery(this).width(tab.pop());
    });
    jQuery(window).resize(resize_win);
    resize_win();
}
window.addEventListener("popstate", function(e) {
    var menu;
    if (e.state) {
        PUSH_STATE = false;
        menu = get_menu().activate(e.state, false);
        PUSH_STATE = true;
    }
}, false);
function history_push_state(title, url) {
    var url2;
    url2 = url.split("?")[0];
    window.history.pushState(title, title, url2);
}