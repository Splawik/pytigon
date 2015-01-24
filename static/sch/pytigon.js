function _$rapyd$_extends(child, parent) {
    child.prototype = new parent;
    child.prototype.constructor = child;
}
function _$rapyd$_in(val, arr) {
    if (arr instanceof Array || typeof arr === "string") return arr.indexOf(val) != -1;
    else {
        if (arr.hasOwnProperty(val)) return true;
        return false;
    }
}
APPLICATION_TEMPLATE = "standard";
RET_BUFOR = null;
RET_OBJ = null;
IS_POPUP = false;
SUBWIN = false;
LANG = "en";
MENU = null;
function _on_close_page(event) {
    get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""));
}
function Menu() {
    this.__init__.apply(this, arguments);
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
Menu.prototype.activate = function activate(title){
    var self = this;
    var _id;
    _id = self.titles[title];
    jQuery(sprintf("#li_%s a", _id)).tab("show");
};
Menu.prototype.new_pos = function new_pos(title, data){
    var self = this;
    var _id, options;
    if (self.is_open()) {
        self.activate(title);
        return null;
    } else {
        _id = "tab" + self.id;
        self.titles[title] = _id;
        jQuery("#tabs2").append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='glyphicon glyphicon-remove'></span></button></li>", [ _id, _id, title, _id ]));
        jQuery("#tabs2_content").append(sprintf("<div class='tab-pane' id='%s'></div>", _id));
        jQuery("#" + _id).html(data);
        options = get_datatable_options();
        jQuery("#" + _id + " .tabsort").dataTable(get_datatable_options());
        $("#tabs2 a:last").tab("show");
        $(sprintf("#button_%s", _id)).click(_on_close_page);
        self.id += 1;
        return _id;
    }
};
Menu.prototype.remove_page = function remove_page(id){
    var self = this;
    var pos;
    var _$rapyd$_Iter0 = self.titles;
    for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
        pos = _$rapyd$_Iter0[_$rapyd$_Index0];
        if (self.titles[pos] === id) {
            self.titles[pos] = null;
        }
    }
    jQuery(sprintf("#li_%s", id)).remove();
    jQuery(sprintf("#%s", id)).remove();
    jQuery("#tabs2 a:last").tab("show");
};

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
function _dialog_ex_load1(responseText, status, response) {
    if (status !== "error") {
        _dialog_loaded(true);
        on_dialog_load();
    }
}
function dialog_ex_load2(responseText, status, response) {
    if (status !== "error") {
        _dialog_loaded(false);
        on_dialog_load();
    }
}
function dialog_ex_load_delete(responseText, status, response) {
    jQuery("div.dialog-form-delete").modal();
}
function dialog_ex_load_info(responseText, status, response) {
    jQuery("div.dialog-form-info").modal();
}
function _on_hide(e) {
    IS_POPUP = false;
    jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>");
}
function _on_popup() {
    var l;
    l = Ladda.create(this);
    if (is_hybrid()) {
        cmd_to_python("href_to_elem|" + this.href + "|#dialog-data");
        jQuery("div.dialog-form").modal();
    } else {
        if (can_popup()) {
            jQuery("div.dialog-data").load(jQuery(this).attr("href"), null, _dialog_ex_load1);
        } else {
            l.start();
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>").insertAfter(jQuery(this).parents("tr"));
            function _on_loaded(responseText, status, response) {
                dialog_ex_load2(responseText, status, response);
                l.stop();
            }
            jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null, _on_loaded);
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
            jQuery("div.dialog-data-info").load(jQuery(this).attr("href"), null, dialog_ex_load_info);
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
            jQuery("div.dialog-data-delete").load(jQuery(this).attr("href"), null, dialog_ex_load_delete);
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
    jQuery("div.dialog-form").on("hide.bs.modal", _on_hide);
    jQuery("a.popup").click(_on_popup);
    jQuery("a.popup_info").click(_on_popup_info);
    jQuery("a.popup_delete").click(_on_popup_delete);
}
function get_datatable_options() {
    var options;
    options = {
        "scrollY": 400,
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
    var title, menu, classname, l, href;
    if (APPLICATION_TEMPLATE !== "traditional") {
        title = $(this).text();
        menu = get_menu();
        classname = $(this).attr("class");
        if (_$rapyd$_in("btn", classname)) {
            l = Ladda.create(this);
        } else {
            l = null;
        }
        if (APPLICATION_TEMPLATE === "modern" && menu.is_open(title)) {
            menu.activate(title);
        } else {
            function _on_new_win(data) {
                var id;
                if (APPLICATION_TEMPLATE === "modern") {
                    id = menu.new_pos(title, data);
                    function _on_new_page(data) {
                        alert("X2");
                        alert(data);
                    }
                    function _on_click() {
                        alert("X1");
                        return false;
                    }
                    jQuery("#" + id + " .paginator").click(_on_click);
                } else {
                    jQuery("#body_body").html(data);
                }
                popup_init();
                if (l) {
                    l.stop();
                }
            }
            href = jQuery(this).attr("href");
            if (_$rapyd$_in("?", href)) {
                href = href + "&hybrid=1";
            } else {
                href = href + "?hybrid=1";
            }
            if (APPLICATION_TEMPLATE === "standard" && _$rapyd$_in("btn", classname)) {
                jQuery("a.menu-href").removeClass("btn-warning").addClass("btn-info");
                jQuery(this).removeClass("btn-info").addClass("btn-warning");
            }
            if (l) {
                l.start();
            }
            jQuery.ajax({
                "type": "GET",
                "url": href,
                "success": _on_new_win
            });
            $(this).closest(".dropdown-menu").dropdown("toggle");
            $(".navbar-ex1-collapse").collapse("hide");
        }
        return false;
    }
}
function jquery_init(application_template, scroll_table, menu_id, lang) {
    var SUBWIN;
    scroll_table = false;
    APPLICATION_TEMPLATE = application_template;
    LANG = lang;
    if (IS_POPUP) {
        SUBWIN = true;
    } else {
        SUBWIN = false;
    }
    if (!SUBWIN) {
        if (scroll_table === "True") {
            jQuery(window).load(stick_header);
        }
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
    jQuery(document).ajaxError(_on_error);
    date_init();
    if (APPLICATION_TEMPLATE === "traditional") {
        jQuery(".tabsort").dataTable(get_datatable_options());
    }
}