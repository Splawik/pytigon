APPLICATION_TEMPLATE = "standard";
RET_BUFOR = null;
RET_OBJ = null;
IS_POPUP = false;
SUBWIN = false;
LANG = "en";
MENU = null;
ACTIVE_PAGE = null;
PUSH_STATE = true;
BASE_PATH = null;
WAIT_ICON = null;
WAIT_ICON2 = false;
MENU_ID = 0;
BASE_FRAGMENT_INIT = null;
POPUP_ACTIVATOR = null;
COUNTER = 1;
function Page() {
    Page.prototype.__init__.apply(this, arguments);
}
Page.prototype.__init__ = function __init__(id, page){
    var self = this;
    self.id = id;
    self.page = page;
};
Page.prototype.set_href = function set_href(href){
    var self = this;
    self.page.attr("_href", href);
};
Page.prototype.get_href = function get_href(){
    var self = this;
    return self.page.attr("_href");
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



function TabMenu() {
    TabMenu.prototype.__init__.apply(this, arguments);
}
TabMenu.prototype.__init__ = function __init__(){
    var self = this;
    self.id = 0;
    self.titles = {};
    self.active_item = null;
};
TabMenu.prototype.get_active_item = function get_active_item(){
    var self = this;
    return self.active_item;
};
TabMenu.prototype.is_open = function is_open(title){
    var self = this;
    if (_$rapyd$_in(title, self.titles) && self.titles[title]) {
        return true;
    } else {
        return false;
    }
};
TabMenu.prototype.activate = function activate(title, push_state){
    var self = this;
    if (typeof push_state === "undefined") push_state = true;
    var menu_item;
    menu_item = self.titles[title];
    jQuery(sprintf("#li_%s a", menu_item.id)).tab("show");
    if (push_state && PUSH_STATE) {
        history_push_state(menu_item.title, menu_item.url);
    }
};
TabMenu.prototype.new_page = function new_page(title, data, href){
    var self = this;
    var _id, menu_item;
    _id = "tab" + self.id;
    menu_item = new TabMenuItem(_id, title, href, data);
    self.titles[title] = menu_item;
    jQuery("#tabs2").append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='glyphicon glyphicon-remove'></span></button></li>", [ _id, _id, title, _id ]));
    jQuery("#tabs2_content").append(sprintf("<div class='tab-pane' id='%s'></div>", _id));
    ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
    self.active_item = menu_item;
    jQuery("#" + _id).html(data);
    if (PUSH_STATE) {
        history_push_state(title, href);
    }
    jQuery("#tabs2 a:last").tab("show");
    jQuery("#tabs2 a:last").on("shown.bs.tab", function(e) {
        var menu;
        ACTIVE_PAGE = new Page(_id, jQuery("#" + _id), menu_item);
        menu = get_menu();
        menu_item = menu.titles[jQuery.trim(e.target.text)];
        self.active_item = menu_item;
        if (PUSH_STATE) {
            history_push_state(menu_item.title, menu_item.url);
        }
    });
    page_init(_id);
    jQuery(sprintf("#button_%s", _id)).click(function(event) {
        get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""));
    });
    self.id += 1;
    return _id;
};
TabMenu.prototype.remove_page = function remove_page(id){
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

function get_menu() {
    if (!MENU) {
        MENU = new TabMenu();
    }
    return MENU;
}
function on_popup(elem) {
    POPUP_ACTIVATOR = jQuery(elem);
    WAIT_ICON = Ladda.create(elem);
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + elem.href + "|#dialog-data");
        jQuery("div.dialog-form").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data").load(jQuery(elem).attr("href"), null, function(responseText, status, response) {
                if (status !== "error") {
                    _dialog_loaded(true);
                    on_dialog_load();
                }
            });
        } else {
            if (WAIT_ICON) {
                WAIT_ICON.start();
            }
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>").insertAfter(jQuery(elem).parents("tr"));
            jQuery("div.dialog-data-inner").load(jQuery(elem).attr("href"), null, function(responseText, status, response) {
                if (status !== "error") {
                    _dialog_loaded(false);
                    on_dialog_load();
                }
                if (WAIT_ICON) {
                    WAIT_ICON.stop();
                    WAIT_ICON = null;
                }
            });
        }
    }
    return false;
}
function on_popup_inline(elem) {
    var id, href2;
    jQuery(elem).attr("data-style", "zoom-out");
    jQuery(elem).attr("data-spinner-color", "#FF0000");
    WAIT_ICON = Ladda.create(elem);
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + elem.href + "|#dialog-data");
        jQuery("div.dialog-form-info").modal();
    } else {
        if (WAIT_ICON) {
            WAIT_ICON.start();
        }
        jQuery(elem).closest("table").find(".inline_dialog").remove();
        COUNTER = COUNTER + 1;
        id = COUNTER;
        jQuery("<tr class='inline_dialog hide' id='IDIAL_" + id + "'><td colspan='20'>" + INLINE_TABLE_HTML + "</td></tr>").insertAfter(jQuery(elem).closest("tr"));
        href2 = corect_href(jQuery(elem).attr("href"));
        jQuery(elem).closest("table").find("div.dialog-data-inner").load(href2, null, function(responseText, status, response) {
            $("#IDIAL_" + id).hide();
            $("#IDIAL_" + id).removeClass("hide");
            $("#IDIAL_" + id).show("slow");
            if (status !== "error") {
                _dialog_loaded(false);
                on_dialog_load();
            }
            if (WAIT_ICON) {
                WAIT_ICON.stop();
                WAIT_ICON = null;
            }
        });
    }
    return false;
}
function on_popup_info(elem) {
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + elem.href + "|#dialog-data-info");
        jQuery("div.dialog-form-info").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data-info").load(jQuery(elem).attr("href"), null, function(responseText, status, response) {
                jQuery("div.dialog-form-info").modal();
            });
        } else {
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML + "</td></tr>").insertAfter(jQuery(elem).parents("tr"));
            jQuery("div.dialog-data-inner").load(jQuery(elem).attr("href"), null);
        }
    }
    return false;
}
function on_popup_delete(elem) {
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + elem.href + "|#dialog-data-delete");
        jQuery("div.dialog-form-delete").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data-delete").load(jQuery(elem).attr("href"), null, function(responseText, status, response) {
                jQuery("div.dialog-form-delete").modal();
            });
        } else {
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>").insertAfter(jQuery(elem).parents("tr"));
            jQuery("div.dialog-data-inner").load(jQuery(elem).attr("href"), null);
        }
    }
    return false;
}
function on_dialog_load() {
}
function _dialog_loaded(is_modal) {
    fragment_init(jQuery("div.dialog-form"));
    ACTIVE_PAGE.page.find("div.resizable").resizable();
    if (is_modal) {
        jQuery("div.dialog-form").fadeTo("fast", 1);
        jQuery("div.dialog-form").modal();
        jQuery("div.dialog-form").draggable({
            "handle": ".modal-header"
        });
        IS_POPUP = true;
    }
}
function dialog_ex_load2(responseText, status, response) {
    if (status !== "error") {
        _dialog_loaded(false);
        on_dialog_load();
    }
}
function progressHandlingFunction(e) {
    if (e.lengthComputable) {
        $("#progress").width("" + parseInt(100 * e.loaded / e.total) + "%");
    }
}
function xhr() {
    var myXhr;
    myXhr = jQuery.ajaxSettings.xhr();
    if (myXhr.upload) {
        myXhr.upload.addEventListener("progress", progressHandlingFunction, false);
    }
    return myXhr;
}
function on_edit_ok(form) {
    var data;
    data = new FormData(form[0]);
    if (_$rapyd$_in("multipart", form.attr("enctype"))) {
        form.closest("div").append("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>");
        jQuery.ajax({
            "type": "POST",
            "url": corect_href(form.attr("action")),
            "data": data,
            contentType: false,
            processData: false,
            "xhr": xhr,
            "success": function(data) {
                _refresh_win(data, form);
            }
        });
    } else {
        jQuery.ajax({
            "type": "POST",
            "url": corect_href(form.attr("action")),
            "data": data,
            contentType: false,
            processData: false,
            "success": function(data) {
                _refresh_win(data, form);
            }
        });
    }
    return false;
}
function on_delete_ok(form) {
    jQuery.ajax({
        "type": "POST",
        "url": corect_href(form.attr("action")),
        "data": form.serialize(),
        "success": function(data) {
            _refresh_win(data, form);
        }
    });
    return false;
}
function _refresh_win2(responseText, form) {
    var subform, filter;
    if (_$rapyd$_in("RETURN_OK", responseText)) {
        subform = form.closest("div.inline_frame");
        if (subform.length > 0) {
            subform.find("div.frame-data-inner").load(subform.attr("href"), null);
        } else {
            filter = ACTIVE_PAGE.page.find("form.TableFiltr");
            jQuery("div.dialog-form").fadeTo("slow", .5);
            if (filter.length > 0) {
                filter.attr("action", ACTIVE_PAGE.get_href());
                ajax_submit(filter, function(data) {
                    ACTIVE_PAGE.page.html(data);
                    jQuery("div.dialog-form").modal("hide");
                    page_init(ACTIVE_PAGE.id, false);
                });
            } else {
                jQuery("div.dialog-form").modal("hide");
            }
        }
    } else {
        jQuery("div.dialog-data").html(responseText);
    }
}
function _refresh_win(responseText, ok_button) {
    var form, subform, div, href, filter;
    form = POPUP_ACTIVATOR.closest("div.content").find("form.TableFiltr");
    if (_$rapyd$_in("RETURN_OK", responseText)) {
        subform = form.closest("div.inline_frame");
        if (subform.length > 0) {
            subform.find("div.frame-data-inner").load(subform.attr("href"), null);
        } else {
            div = POPUP_ACTIVATOR.closest("div.dialog-data-inner");
            if (div.length > 0) {
                href = corect_href(form.attr("action"));
                div.load(href, null);
                jQuery("div.dialog-form").modal("hide");
            } else {
                filter = form;
                jQuery("div.dialog-form").fadeTo("slow", .5);
                if (filter.length > 0) {
                    filter.attr("action", ACTIVE_PAGE.get_href());
                    ajax_submit(filter, function(data) {
                        ACTIVE_PAGE.page.html(data);
                        jQuery("div.dialog-form").modal("hide");
                        page_init(ACTIVE_PAGE.id, false);
                    });
                } else {
                    jQuery("div.dialog-form").modal("hide");
                }
            }
        }
    } else {
        form.jQuery("div.dialog-data").html(responseText);
    }
}
function on_cancel_inline(elem) {
    jQuery(elem).closest(".inline_dialog").remove();
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
function stick_header() {
    var table, tab2, tab;
    tab = [];
    tab2 = [];
    ACTIVE_PAGE.page.find("table.tabsort th").each(function() {
        tab.push(jQuery(this).width());
    });
    table = jQuery("<table class=\"tabsort tbl_header\" style=\"overflow-x: hidden;\"></table>");
    table.append(ACTIVE_PAGE.page.find("table.tabsort thead"));
    ACTIVE_PAGE.page.find(".tbl_scroll").before(table);
    ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
        tab2.push(jQuery(this).width());
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
        jQuery.ajax({
            "type": "POST",
            "url": corect_href(form.attr("action")),
            "data": form.serialize(),
            "success": func
        });
    }
}
function get_page(elem) {
    if (elem.hasClass(".tab-pane")) {
        return elem;
    } else {
        return elem.closest(".tab-pane");
    }
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
function corect_href(href) {
    if (_$rapyd$_in("hybrid", href)) {
        return href;
    } else {
        if (_$rapyd$_in("?", href)) {
            return href + "&hybrid=1";
        } else {
            return href + "?hybrid=1";
        }
    }
}
function fragment_init(elem) {
    if (typeof elem === "undefined") elem = null;
    var elem2;
    if (elem) {
        elem2 = elem;
    } else {
        elem2 = ACTIVE_PAGE.page;
    }
    elem2.find(".dateinput").datetimepicker({
        "pickTime": false,
        "format": "YYYY-MM-DD",
        "language": "pl"
    });
    elem2.find(".datetimeinput").datetimepicker({
        "format": "YYYY-MM-DD hh:mm",
        "language": "pl"
    });
    if (BASE_FRAGMENT_INIT) {
        BASE_FRAGMENT_INIT();
    }
}
function page_init(id, first_time) {
    if (typeof first_time === "undefined") first_time = true;
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
                        fragment_init(pg.closest(".content").find(".tabsort tbody"));
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
    if (first_time) {
        jQuery("#" + id).on("click", "a", function(e) {
            var pos, href, href2;
            var _$rapyd$_Iter0 = [ ["popup", on_popup], ["popup_inline", on_popup_inline], ["popup_info", 
            on_popup_info], ["popup_delete", on_popup_delete] ];
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                pos = _$rapyd$_Iter0[_$rapyd$_Index0];
                if (jQuery(this).hasClass(pos[0])) {
                    pos[1](this);
                    return false;
                }
            }
            href = jQuery(this).attr("href");
            if (_$rapyd$_in("#", href)) {
                return true;
            }
            e.preventDefault();
            href2 = corect_href(href);
            jQuery.ajax({
                "type": "GET",
                "url": href2,
                "success": function(data) {
                    if (APPLICATION_TEMPLATE === "modern") {
                        ACTIVE_PAGE.page.html(data);
                        ACTIVE_PAGE.set_href(href);
                        page_init(ACTIVE_PAGE.id, false);
                    } else {
                        jQuery("#body_body").html(data);
                        page_init("body_body", false);
                    }
                    ACTIVE_PAGE.set_href(href);
                    get_menu().get_active_item().url = href;
                    if (PUSH_STATE) {
                        history_push_state("title", href);
                    }
                }
            });
        });
    }
    ACTIVE_PAGE.page.find("form").attr("target", "_blank");
    ACTIVE_PAGE.page.find("form").submit(function(e) {
        var data, submit_button, href;
        data = jQuery(this).serialize();
        console.log(data);
        if (_$rapyd$_in("pdf=on", data)) {
            return true;
        }
        if (_$rapyd$_in("odf=on", data)) {
            return true;
        }
        e.preventDefault();
        submit_button = jQuery(this).find("button[type=\"submit\"]");
        if (submit_button.length > 0) {
            WAIT_ICON = Ladda.create(submit_button[0]);
            WAIT_ICON.start();
        } else {
            WAIT_ICON2 = true;
            $("#loading-indicator").show();
        }
        href = jQuery(this).attr("action");
        if (href) {
            jQuery(this).attr("action", corect_href(href));
        }
        ajax_submit(jQuery(this), function(data) {
            ACTIVE_PAGE.page.html(data);
            page_init(id, false);
            if (WAIT_ICON) {
                WAIT_ICON.stop();
            }
            if (WAIT_ICON2) {
                $("#loading-indicator").hide();
                WAIT_ICON2 = false;
            }
        });
    });
    fragment_init(ACTIVE_PAGE.page);
}
function app_init(application_template, menu_id, lang, base_path, base_fragment_init) {
    var SUBWIN;
    APPLICATION_TEMPLATE = application_template;
    LANG = lang;
    BASE_PATH = base_path;
    BASE_FRAGMENT_INIT = base_fragment_init;
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
            jQuery("body").on("click", "a.menu-href", function(e) {
                if (APPLICATION_TEMPLATE !== "traditional") {
                    e.preventDefault();
                    _on_menu_href(this);
                }
            });
            jQuery("body").on("submit", "form.DialogForm", function(e) {
                e.preventDefault();
                on_edit_ok($(this));
            });
        });
    }
}
function _on_menu_href(elem, title) {
    if (typeof title === "undefined") title = null;
    var menu, classname, href, href2;
    if (APPLICATION_TEMPLATE !== "traditional") {
        if (!title) {
            title = jQuery.trim(jQuery(elem).text());
        }
        menu = get_menu();
        classname = jQuery(elem).attr("class");
        if (classname && _$rapyd$_in("btn", classname)) {
            if (WAIT_ICON) {
                WAIT_ICON.stop();
            }
            WAIT_ICON = Ladda.create(elem);
        } else {
            WAIT_ICON = null;
        }
        if (APPLICATION_TEMPLATE === "modern" && menu.is_open(title)) {
            menu.activate(title);
        } else {
            href = jQuery(elem).attr("href");
            href2 = corect_href(href);
            function _on_new_win(data) {
                var ACTIVE_PAGE, id;
                if (APPLICATION_TEMPLATE === "modern") {
                    id = menu.new_page(title, data, href);
                } else {
                    jQuery("#body_body").html(data);
                    ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
                    ACTIVE_PAGE.set_href(href2);
                    page_init("body_body", false);
                    if (PUSH_STATE) {
                        id = jQuery(elem).attr("id");
                        if (!id) {
                            id = "menu_id_" + MENU_ID;
                            MENU_ID = MENU_ID + 1;
                            jQuery(elem).attr("id", id);
                        }
                        history_push_state(title, href, [ data, id ]);
                    }
                }
                if (WAIT_ICON) {
                    WAIT_ICON.stop();
                    WAIT_ICON = null;
                }
                if (WAIT_ICON2) {
                    $("#loading-indicator").hide();
                    WAIT_ICON2 = false;
                }
            }
            if (APPLICATION_TEMPLATE === "standard" && _$rapyd$_in("btn", classname)) {
                jQuery("a.menu-href").removeClass("btn-warning");
                jQuery(elem).addClass("btn-warning");
            }
            if (WAIT_ICON) {
                WAIT_ICON.start();
            } else {
                WAIT_ICON2 = true;
                $("#loading-indicator").show();
            }
            jQuery.ajax({
                "type": "GET",
                "url": href2,
                "success": _on_new_win
            });
        }
        return false;
    }
}
function _on_error(request, settings) {
    var start, end;
    if (WAIT_ICON) {
        WAIT_ICON.stop();
        WAIT_ICON = null;
    }
    if (WAIT_ICON2) {
        $("#loading-indicator").hide();
        WAIT_ICON2 = false;
    }
    start = settings.responseText.indexOf("<body>");
    end = settings.responseText.lastIndexOf("</body>");
    if (start > 0 && end > 0) {
        jQuery("#dialog-data-error").html(settings.responseText.substring(start + 6, end - 1));
        jQuery("#dialog-form-error").modal();
    } else {
        jQuery("#dialog-data-error").html(settings.responseText);
        jQuery("#dialog-form-error").modal();
    }
}
function jquery_ready() {
    var txt2, txt, menu;
    jQuery(document).ajaxError(_on_error);
    jQuery("div.dialog-form").on("hide.bs.modal", function(e) {
        IS_POPUP = false;
        jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>");
    });
    if (APPLICATION_TEMPLATE === "traditional") {
        ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
        page_init("body_body");
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
        } else {
            ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
            page_init("body_body");
        }
    }
}
window.addEventListener("popstate", function(e) {
    var menu, x, ACTIVE_PAGE;
    if (e.state) {
        PUSH_STATE = false;
        if (APPLICATION_TEMPLATE === "modern") {
            menu = get_menu().activate(e.state, false);
        } else {
            x = e.state;
            jQuery("#body_body").html(LZString.decompress(x[0]));
            ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
            ACTIVE_PAGE.set_href(document.location);
            if (APPLICATION_TEMPLATE === "standard") {
                jQuery("a.menu-href").removeClass("btn-warning");
                jQuery("#" + x[1]).addClass("btn-warning");
            }
        }
        PUSH_STATE = true;
    } else {
        if (APPLICATION_TEMPLATE === "modern") {
            alert("X1");
        } else {
            jQuery("#body_body").html("");
            ACTIVE_PAGE = null;
            if (APPLICATION_TEMPLATE === "standard") {
                jQuery("a.menu-href").removeClass("btn-warning");
            }
        }
    }
}, false);
function history_push_state(title, url, data) {
    if (typeof data === "undefined") data = null;
    var url2, data2;
    url2 = url.split("?")[0];
    if (data) {
        data2 = [ LZString.compress(data[0]), data[1] ];
    } else {
        data2 = title;
    }
    window.history.pushState(data2, title, url2);
}