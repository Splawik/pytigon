var ՐՏ_modules = {};
ՐՏ_modules["glob"] = {};
ՐՏ_modules["page"] = {};
ՐՏ_modules["tabmenuitem"] = {};
ՐՏ_modules["tabmenu"] = {};
ՐՏ_modules["schclient"] = {};
ՐՏ_modules["tools"] = {};
ՐՏ_modules["popup"] = {};
ՐՏ_modules["scrolltbl"] = {};
ՐՏ_modules["tbl"] = {};

(function(){
    var __name__ = "glob";
    var ACTIVE_PAGE;
    ACTIVE_PAGE = null;
    ՐՏ_modules["glob"]["ACTIVE_PAGE"] = ACTIVE_PAGE;
})();

(function(){
    var __name__ = "page";
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

    ՐՏ_modules["page"]["Page"] = Page;
})();

(function(){
    var __name__ = "tabmenuitem";
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

    ՐՏ_modules["tabmenuitem"]["TabMenuItem"] = TabMenuItem;
})();

(function(){
    var __name__ = "tabmenu";
    var glob = ՐՏ_modules["glob"];
    
    var Page = ՐՏ_modules["page"].Page;
    
    var TabMenuItem = ՐՏ_modules["tabmenuitem"].TabMenuItem;
    
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
        if (ՐՏ_in(title, self.titles) && self.titles[title]) {
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
    TabMenu.prototype.new_page = function new_page(title, data, href, riot_init){
        var self = this;
        var _id, menu_item, scripts;
        _id = "tab" + self.id;
        menu_item = new TabMenuItem(_id, title, href, data);
        self.titles[title] = menu_item;
        jQuery("#tabs2").append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", [ _id, _id, title, _id ]));
        jQuery("#tabs2_content").append(sprintf("<div class='tab-pane' id='%s'></div>", _id));
        glob.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
        self.active_item = menu_item;
        jQuery("#" + _id).html(data);
        if (PUSH_STATE) {
            history_push_state(title, href);
        }
        jQuery("#tabs2 a:last").on("shown.bs.tab", function(e) {
            var menu;
            glob.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id), menu_item);
            menu = get_menu();
            menu_item = menu.titles[jQuery.trim(e.target.text)];
            self.active_item = menu_item;
            if (PUSH_STATE) {
                history_push_state(menu_item.title, menu_item.url);
            }
        });
        jQuery("#tabs2 a:last").tab("show");
        page_init(_id);
        jQuery(sprintf("#button_%s", _id)).click(function(event) {
            get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""));
        });
        scripts = jQuery("#" + _id + " script");
        scripts.each(function(index, element) {
            eval(this.innerHTML);
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
    ՐՏ_modules["tabmenu"]["TabMenu"] = TabMenu;

    ՐՏ_modules["tabmenu"]["get_menu"] = get_menu;
})();

(function(){
    var __name__ = "schclient";
    function cmd_to_python(value) {
        document.title = ":" + value;
    }
    function is_hybrid() {
        return false;
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
    ՐՏ_modules["schclient"]["cmd_to_python"] = cmd_to_python;

    ՐՏ_modules["schclient"]["is_hybrid"] = is_hybrid;

    ՐՏ_modules["schclient"]["to_absolute_url"] = to_absolute_url;

    ՐՏ_modules["schclient"]["ret_submit"] = ret_submit;
})();

(function(){
    var __name__ = "tools";
    var LOADED_FILES;
    var cmd_to_python = ՐՏ_modules["schclient"].cmd_to_python;
    var is_hybrid = ՐՏ_modules["schclient"].is_hybrid;
    var to_absolute_url = ՐՏ_modules["schclient"].to_absolute_url;
    var ret_submit = ՐՏ_modules["schclient"].ret_submit;
    
    LOADED_FILES = {};
    function download_binary_file(buf, content_disposition) {
        var l, buffer, view, i, mimetype, blob, blobURL;
        l = buf.length;
        buffer = new ArrayBuffer(l);
        view = new Uint8Array(buffer);
        for (i = 0; i < l; i++) {
            view[i] = buf.charCodeAt(i);
        }
        mimetype = "text/html";
        if (ՐՏ_in("odf", content_disposition) || ՐՏ_in("ods", content_disposition)) {
            mimetype = "application/vnd.oasis.opendocument.formula";
        } else if (ՐՏ_in("pdf", content_disposition)) {
            mimetype = "application/pdf";
        } else if (ՐՏ_in("zip", content_disposition)) {
            mimetype = "application/x-compressed";
        } else if (ՐՏ_in("xls", content_disposition)) {
            mimetype = "application/excel";
        }
        blob = new Blob([ view ], {
            "type": mimetype
        });
        blobURL = window.URL.createObjectURL(blob);
        window.open(blobURL);
    }
    function ajax_get(url, complete) {
        var req;
        req = new XMLHttpRequest();
        function _onload() {
            var disp;
            disp = req.getResponseHeader("Content-Disposition");
            if (disp && ՐՏ_in("attachment", disp)) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                complete(req.responseText);
            }
        }
        req.onload = _onload;
        req.open("GET", url, true);
        req.send();
    }
    function ajax_load(elem, url, complete) {
        function _onload(responseText) {
            elem.html(responseText);
            complete(responseText);
        }
        ajax_get(url, _onload);
    }
    function _req_post(req, url, data, complete) {
        function _onload() {
            var disp;
            disp = req.getResponseHeader("Content-Disposition");
            if (disp && ՐՏ_in("attachment", disp)) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                complete(req.responseText);
            }
        }
        req.onload = _onload;
        req.open("POST", url, true);
        req.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
        if (data.length) {
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.setRequestHeader("Content-length", data.length);
            req.setRequestHeader("Connection", "close");
        }
        req.send(data);
    }
    function ajax_post(url, data, complete) {
        var req;
        req = new XMLHttpRequest();
        _req_post(req, url, data, complete);
    }
    function ajax_submit(form, complete) {
        var req, data;
        req = new XMLHttpRequest();
        if (form.find("[type='file']").length > 0) {
            form.attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
            data = new FormData(form[0]);
            form.closest("div").append("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>");
            function _progressHandlingFunction(e) {
                if (e.lengthComputable) {
                    $("#progress").width("" + parseInt(100 * e.loaded / e.total) + "%");
                }
            }
            req.upload.addEventListener("progress", _progressHandlingFunction, false);
        } else {
            data = form.serialize();
        }
        _req_post(req, corect_href(form.attr("action")), data, complete);
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
        if (jQuery("div.dialog-form").hasClass("in") || jQuery("div.dialog-form-delete").hasClass("in") || jQuery("div.dialog-form-info").hasClass("in")) {
            return false;
        } else {
            return true;
        }
    }
    function corect_href(href) {
        if (ՐՏ_in("only_content", href)) {
            return href;
        } else {
            if (ՐՏ_in("?", href)) {
                return href + "&only_content=1";
            } else {
                return href + "?only_content=1";
            }
        }
    }
    function handle_class_click(fragment_obj, obj_class, fun) {
        fragment_obj.on("click", "." + obj_class, function(e) {
            var src_obj;
            src_obj = jQuery(this);
            e.preventDefault();
            fun(this);
            return false;
        });
    }
    function load_css(path) {
        var req;
        if (!(LOADED_FILES && ՐՏ_in(path, LOADED_FILES))) {
            LOADED_FILES[path] = null;
            req = new XMLHttpRequest();
            function _onload() {
                jQuery("<style type=\"text/css\"></style>").html(req.responseText).appendTo("head");
            }
            req.onload = _onload;
            req.open("GET", path, true);
            req.send("");
        }
    }
    function on_load_js(path) {
        var functions, fun;
        if (LOADED_FILES && ՐՏ_in(path, LOADED_FILES)) {
            functions = LOADED_FILES[path];
            if (functions) {
                var ՐՏ_Iter0 = ՐՏ_Iterable(functions);
                for (var ՐՏ_Index0 = 0; ՐՏ_Index0 < ՐՏ_Iter0.length; ՐՏ_Index0++) {
                    fun = ՐՏ_Iter0[ՐՏ_Index0];
                    fun();
                }
            }
            LOADED_FILES[path] = null;
        }
    }
    function load_js(path, fun) {
        var req;
        if (LOADED_FILES && ՐՏ_in(path, LOADED_FILES)) {
            if (LOADED_FILES[path]) {
                LOADED_FILES[path].push(fun);
            } else {
                fun();
            }
        } else {
            LOADED_FILES[path] = [ fun ];
            req = new XMLHttpRequest();
            function _onload() {
                jQuery.globalEval(req.responseText);
                on_load_js(path);
            }
            req.onload = _onload;
            req.open("GET", path, true);
            req.send("");
        }
    }
    function load_many_js(paths, fun) {
        var counter, path;
        counter = 0;
        function _fun() {
            counter = counter - 1;
            if (counter === 0) {
                fun();
            }
        }
        var ՐՏ_Iter1 = ՐՏ_Iterable(paths.split(paths, ";"));
        for (var ՐՏ_Index1 = 0; ՐՏ_Index1 < ՐՏ_Iter1.length; ՐՏ_Index1++) {
            path = ՐՏ_Iter1[ՐՏ_Index1];
            if (path.lenght() > 0) {
                counter = counter + 1;
                load_js(path, _fun);
                {}
            }
        }
    }
    ՐՏ_modules["tools"]["LOADED_FILES"] = LOADED_FILES;

    ՐՏ_modules["tools"]["download_binary_file"] = download_binary_file;

    ՐՏ_modules["tools"]["ajax_get"] = ajax_get;

    ՐՏ_modules["tools"]["ajax_load"] = ajax_load;

    ՐՏ_modules["tools"]["_req_post"] = _req_post;

    ՐՏ_modules["tools"]["ajax_post"] = ajax_post;

    ՐՏ_modules["tools"]["ajax_submit"] = ajax_submit;

    ՐՏ_modules["tools"]["get_page"] = get_page;

    ՐՏ_modules["tools"]["get_table_type"] = get_table_type;

    ՐՏ_modules["tools"]["can_popup"] = can_popup;

    ՐՏ_modules["tools"]["corect_href"] = corect_href;

    ՐՏ_modules["tools"]["handle_class_click"] = handle_class_click;

    ՐՏ_modules["tools"]["load_css"] = load_css;

    ՐՏ_modules["tools"]["on_load_js"] = on_load_js;

    ՐՏ_modules["tools"]["load_js"] = load_js;

    ՐՏ_modules["tools"]["load_many_js"] = load_many_js;
})();

(function(){
    var __name__ = "popup";
    var can_popup = ՐՏ_modules["tools"].can_popup;
    var corect_href = ՐՏ_modules["tools"].corect_href;
    var ajax_load = ՐՏ_modules["tools"].ajax_load;
    var ajax_get = ՐՏ_modules["tools"].ajax_get;
    var ajax_post = ՐՏ_modules["tools"].ajax_post;
    
    var is_hybrid = ՐՏ_modules["schclient"].is_hybrid;
    var cmd_to_python = ՐՏ_modules["schclient"].cmd_to_python;
    var is_hybrid = ՐՏ_modules["schclient"].is_hybrid;
    
    function refresh_fragment(data_item_to_refresh, fun) {
        if (typeof fun === "undefined") fun = null;
        var refr_block, target, src, href;
        refr_block = data_item_to_refresh.closest(".refr_object");
        if (refr_block.hasClass("refr_target")) {
            target = refr_block;
        } else {
            target = refr_block.find(".refr_target");
        }
        src = refr_block.find(".refr_source");
        if (src.length > 0) {
            href = src.attr("href");
            if (src.prop("tagName") === "FORM") {
                function _refr2(data) {
                    target.html(data);
                    fragment_init(target);
                    if (fun) {
                        fun();
                    }
                }
                ajax_post(corect_href(href), src.serialize(), _refr2);
            } else {
                ajax_load(target, corect_href(href), function(responseText) {
                });
            }
        }
    }
    function on_popup_inline(elem) {
        var id, href2, new_fragment, elem2;
        jQuery(elem).attr("data-style", "zoom-out");
        jQuery(elem).attr("data-spinner-color", "#FF0000");
        WAIT_ICON = Ladda.create(elem);
        if (is_hybrid()) {
            cmd_to_python("href_to_elem??" + elem.href + "??#dialog-data");
            jQuery("div.dialog-form-info").modal();
        } else {
            if (WAIT_ICON) {
                WAIT_ICON.start();
            }
            jQuery(elem).closest("table").find(".inline_dialog").remove();
            COUNTER = COUNTER + 1;
            id = COUNTER;
            href2 = corect_href(jQuery(elem).attr("href"));
            new_fragment = jQuery("<tr class='refr_source inline_dialog hide' id='IDIAL_" + id + "' href='" + href2 + "'><td colspan='20'>" + INLINE_TABLE_HTML + "</td></tr>");
            new_fragment.insertAfter(jQuery(elem).closest("tr"));
            elem2 = new_fragment.find(".refr_target");
            elem2.load(href2, null, function(responseText, status, response) {
                $("#IDIAL_" + id).hide();
                $("#IDIAL_" + id).removeClass("hide");
                $("#IDIAL_" + id).show("slow");
                if (status !== "error") {
                    _dialog_loaded(false, elem2);
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
    function on_popup_in_form(elem) {
        var id, href2, new_fragment, elem2;
        jQuery(elem).attr("data-style", "zoom-out");
        jQuery(elem).attr("data-spinner-color", "#FF0000");
        WAIT_ICON = Ladda.create(elem);
        if (is_hybrid()) {
            cmd_to_python("href_to_elem??" + elem.href + "??#dialog-data");
            jQuery("div.dialog-form-info").modal();
        } else {
            if (WAIT_ICON) {
                WAIT_ICON.start();
            }
            jQuery(elem).closest("div.Dialog").find(".inline_dialog").remove();
            COUNTER = COUNTER + 1;
            id = COUNTER;
            href2 = corect_href(jQuery(elem).attr("href"));
            new_fragment = jQuery("<div class='refr_source inline_dialog hide' id='IDIAL_" + id + "' href='" + href2 + "'>" + INLINE_TABLE_HTML + "</div>");
            new_fragment.insertAfter(jQuery(elem).closest("div.form-group"));
            elem2 = new_fragment.find(".refr_target");
            elem2.load(href2, null, function(responseText, status, response) {
                $("#IDIAL_" + id).hide();
                $("#IDIAL_" + id).removeClass("hide");
                $("#IDIAL_" + id).show("slow");
                if (status !== "error") {
                    _dialog_loaded(false, elem2);
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
    function on_popup_edit_new(elem) {
        var test, elem2, elem3;
        jQuery(elem).attr("data-style", "zoom-out");
        jQuery(elem).attr("data-spinner-color", "#FF0000");
        WAIT_ICON = Ladda.create(elem);
        if (is_hybrid()) {
            cmd_to_python("href_to_elem??" + elem.href + "??#dialog-data");
            jQuery("div.dialog-form").modal();
        } else {
            if (can_popup() && !jQuery(elem).hasClass("inline") && !(ՐՏ_in("_inline", jQuery(elem).attr("name")))) {
                elem2 = jQuery("div.dialog-data");
                elem2.closest(".refr_object").attr("related-object", jQuery(elem).uid());
                ajax_load(elem2, jQuery(elem).attr("href"), function(responseText, status, response) {
                    _dialog_loaded(true, elem2);
                    on_dialog_load();
                });
            } else {
                if (WAIT_ICON) {
                    WAIT_ICON.start();
                }
                if (jQuery(elem).hasClass("new-row")) {
                    elem2 = jQuery("<div class='refr_source inline_dialog tr hide'>" + INLINE_DIALOG_UPDATE_HTML + "</div>");
                    elem2.insertAfter(jQuery(elem).closest("div.tr"));
                } else {
                    test = jQuery(elem).closest("form");
                    if (test.length > 0) {
                        elem2 = jQuery("<div class='refr_source inline_dialog hide'>" + INLINE_DIALOG_UPDATE_HTML + "</div>");
                        elem2.insertAfter(jQuery(elem).closest("div.form-group"));
                    } else {
                        elem2 = jQuery("<tr class='inline_dialog hide'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>");
                        elem2.insertAfter(jQuery(elem).closest("tr"));
                    }
                }
                elem2.find(".modal-title").html(jQuery(elem).attr("title"));
                elem2.find(".refr_object").attr("related-object", jQuery(elem).uid());
                elem3 = elem2.find("div.dialog-data-inner");
                elem3.load(jQuery(elem).attr("href"), null, function(responseText, status, response) {
                    elem2.hide();
                    elem2.removeClass("hide");
                    elem2.show("slow");
                    if (status !== "error") {
                        _dialog_loaded(false, elem3);
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
    function on_popup_info(elem) {
        if (is_hybrid()) {
            cmd_to_python("href_to_elem??" + elem.href + "??#dialog-data-info");
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
        var elem2;
        if (is_hybrid()) {
            cmd_to_python("href_to_elem??" + elem.href + "??#dialog-data-delete");
            jQuery("div.dialog-form-delete").modal();
        } else {
            if (can_popup()) {
                jQuery("div.dialog-data-delete").closest(".refr_object").attr("related-object", jQuery(elem).uid());
                jQuery("div.dialog-data-delete").load(jQuery(elem).attr("href"), null, function(responseText, status, response) {
                    jQuery("div.dialog-form-delete").modal();
                    jQuery("div.dialog-form-delete").fadeTo("fast", 1);
                });
            } else {
                jQuery(".inline_dialog").remove();
                elem2 = jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>");
                elem2.insertAfter(jQuery(elem).parents("tr"));
                elem2.find(".refr_object").attr("related-object", jQuery(elem).uid());
                jQuery("div.dialog-data-inner").load(jQuery(elem).attr("href"), null);
            }
        }
        return false;
    }
    function on_dialog_load() {
    }
    function _dialog_loaded(is_modal, elem) {
        fragment_init(elem);
        if (is_modal) {
            jQuery("div.dialog-form").fadeTo("fast", 1);
            jQuery("div.dialog-form").modal();
            jQuery("div.dialog-form").drags({
                "handle": ".modal-header"
            });
        }
    }
    function on_edit_ok(form) {
        function _fun(data) {
            _refresh_win_after_ok(data, form);
        }
        ajax_submit(form, _fun);
        return false;
    }
    function on_delete_ok(form) {
        ajax_post(corect_href(form.attr("action")), form.serialize(), function(data) {
            _refresh_win(data, form);
        });
        return false;
    }
    function _refresh_win(responseText, ok_button) {
        var popup_activator, dialog;
        popup_activator = jQuery("#" + jQuery(ok_button).closest(".refr_object").attr("related-object"));
        if (ՐՏ_in("RETURN_OK", responseText)) {
            if (!can_popup()) {
                if (jQuery("div.dialog-form").hasClass("in")) {
                    dialog = "div.dialog-form";
                } else {
                    if (jQuery("div.dialog-form-delete").hasClass("in")) {
                        dialog = "div.dialog-form-delete";
                    } else {
                        dialog = "div.dialog-form-info";
                    }
                }
                function hide_dialog_form() {
                    jQuery(dialog).modal("hide");
                }
                jQuery(dialog).fadeTo("slow", .5);
                refresh_fragment(popup_activator, hide_dialog_form);
            } else {
                refresh_fragment(popup_activator);
            }
        } else {
            if (!can_popup()) {
                jQuery("div.dialog-data").html(responseText);
            } else {
                ok_button.closest(".refr_target").html(responseText);
            }
        }
    }
    function _refresh_win_and_ret(responseText, ok_button) {
        var related_object, popup_activator, RET_CONTROL, EDIT_RET_FUNCTION, q;
        if (ՐՏ_in("RETURN_OK", responseText)) {
            related_object = jQuery(ok_button).closest(".refr_object").attr("related-object");
            popup_activator = jQuery("#" + related_object);
            if (jQuery(ok_button).closest(".refr_object").hasClass("in")) {
                jQuery("div.dialog-form").modal("hide");
            } else {
                jQuery(ok_button).closest(".refr_object").remove();
            }
            if (popup_activator && popup_activator.data("edit_ret_function")) {
                RET_CONTROL = popup_activator.data("ret_control");
                EDIT_RET_FUNCTION = popup_activator.data("edit_ret_function");
                q = jQuery(responseText);
                eval(q[1].text);
            }
        } else {
            jQuery("div.dialog-data").html(responseText);
        }
    }
    function _refresh_win_after_ok(responseText, ok_button) {
        var related_object, popup_activator;
        related_object = jQuery(ok_button).closest(".refr_object").attr("related-object");
        popup_activator = jQuery("#" + related_object);
        if (popup_activator && popup_activator.data("edit_ret_function")) {
            EDIT_RET_FUNCTION = popup_activator.data("edit_ret_function");
            EDIT_RET_FUNCTION(responseText, ok_button);
            EDIT_RET_FUNCTION = false;
        } else {
            _refresh_win(responseText, ok_button);
        }
    }
    function on_cancel_inline(elem) {
        jQuery(elem).closest(".inline_dialog").remove();
    }
    function ret_ok(id, title) {
        RET_CONTROL.select2("data", {
            id: id,
            text: title
        }).trigger("change");
        RET_CONTROL.val(id.toString());
        RET_CONTROL[0].defaultValue = id.toString();
    }
    function on_get_tbl_value(elem) {
        on_popup_in_form(elem);
    }
    function on_new_tbl_value(elem) {
        EDIT_RET_FUNCTION = _refresh_win_and_ret;
        RET_CONTROL = jQuery(elem).closest(".input-group").find("input._autoheavyselect2widgetext");
        jQuery(elem).data("edit_ret_function", EDIT_RET_FUNCTION);
        jQuery(elem).data("ret_control", RET_CONTROL);
        return on_popup_edit_new(elem);
    }
    function on_get_row(elem) {
        var id, text, ret_control;
        id = jQuery(elem).attr("data-id");
        text = jQuery(elem).attr("data-text");
        ret_control = jQuery(elem).closest(".refr_source").prev(".form-group").find("input._autoheavyselect2widgetext");
        ret_control.select2("data", {
            id: id,
            text: text
        }).trigger("change");
        ret_control.val(id.toString());
        ret_control[0].defaultValue = id.toString();
        jQuery(elem).closest(".refr_source").remove();
    }
    ՐՏ_modules["popup"]["refresh_fragment"] = refresh_fragment;

    ՐՏ_modules["popup"]["on_popup_inline"] = on_popup_inline;

    ՐՏ_modules["popup"]["on_popup_in_form"] = on_popup_in_form;

    ՐՏ_modules["popup"]["on_popup_edit_new"] = on_popup_edit_new;

    ՐՏ_modules["popup"]["on_popup_info"] = on_popup_info;

    ՐՏ_modules["popup"]["on_popup_delete"] = on_popup_delete;

    ՐՏ_modules["popup"]["on_dialog_load"] = on_dialog_load;

    ՐՏ_modules["popup"]["_dialog_loaded"] = _dialog_loaded;

    ՐՏ_modules["popup"]["on_edit_ok"] = on_edit_ok;

    ՐՏ_modules["popup"]["on_delete_ok"] = on_delete_ok;

    ՐՏ_modules["popup"]["_refresh_win"] = _refresh_win;

    ՐՏ_modules["popup"]["_refresh_win_and_ret"] = _refresh_win_and_ret;

    ՐՏ_modules["popup"]["_refresh_win_after_ok"] = _refresh_win_after_ok;

    ՐՏ_modules["popup"]["on_cancel_inline"] = on_cancel_inline;

    ՐՏ_modules["popup"]["ret_ok"] = ret_ok;

    ՐՏ_modules["popup"]["on_get_tbl_value"] = on_get_tbl_value;

    ՐՏ_modules["popup"]["on_new_tbl_value"] = on_new_tbl_value;

    ՐՏ_modules["popup"]["on_get_row"] = on_get_row;
})();

(function(){
    var __name__ = "scrolltbl";
    var glob = ՐՏ_modules["glob"];
    
    function stick_resize() {
        var tbl, dy_table, dy_win, dy;
        tbl = glob.ACTIVE_PAGE.page.find(".tbl_scroll");
        if (tbl.length > 0) {
            dy_table = tbl.offset().top;
            dy_win = dy_win = jQuery(window).height();
            dy = dy_win - dy_table;
            if (dy < 100) dy = 100;
            tbl.height(dy - 35);
        }
    }
    function resize_win() {
        var tab_width, tab2;
        stick_resize();
        tab2 = [];
        tab_width = glob.ACTIVE_PAGE.page.find("table[name='tabsort']").width();
        glob.ACTIVE_PAGE.page.find(".tbl_header").width(tab_width);
        glob.ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(function() {
            tab2.push(jQuery(this).width());
        });
        tab2 = tab2.reverse();
        glob.ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
            jQuery(this).width(tab2.pop());
        });
    }
    function stick_header() {
        var table, tab2, tab;
        tab = [];
        tab2 = [];
        glob.ACTIVE_PAGE.page.find("table.tabsort th").each(function() {
            tab.push(jQuery(this).width());
        });
        table = jQuery("<table class=\"tabsort tbl_header\" style=\"overflow-x: hidden;\"></table>");
        table.append(glob.ACTIVE_PAGE.page.find("table.tabsort thead"));
        glob.ACTIVE_PAGE.page.find(".tbl_scroll").before(table);
        glob.ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
            tab2.push(jQuery(this).width());
        });
        tab2 = tab2.reverse();
        glob.ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(function() {
            var x;
            x = tab2.pop();
            if (x > jQuery(this).width()) {
                jQuery(this).css("min-width", x);
            }
        });
        tab = tab.reverse();
        glob.ACTIVE_PAGE.page.find(".tbl_header th").each(function() {
            jQuery(this).width(tab.pop());
        });
        jQuery(window).resize(resize_win);
        resize_win();
    }
    ՐՏ_modules["scrolltbl"]["stick_resize"] = stick_resize;

    ՐՏ_modules["scrolltbl"]["resize_win"] = resize_win;

    ՐՏ_modules["scrolltbl"]["stick_header"] = stick_header;
})();

(function(){
    var __name__ = "tbl";
    var glob = ՐՏ_modules["glob"];
    
    var stick_header = ՐՏ_modules["scrolltbl"].stick_header;
    
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
        dy_table = glob.ACTIVE_PAGE.page.find(".tabsort_panel").offset().top;
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
    ՐՏ_modules["tbl"]["get_datatable_options"] = get_datatable_options;

    ՐՏ_modules["tbl"]["get_datatable_options1"] = get_datatable_options1;

    ՐՏ_modules["tbl"]["get_datatable_options2"] = get_datatable_options2;

    ՐՏ_modules["tbl"]["get_datatable_dy"] = get_datatable_dy;

    ՐՏ_modules["tbl"]["set_table_type"] = set_table_type;
})();

var __name__ = "__main__";

APPLICATION_TEMPLATE = "standard";
RET_BUFOR = null;
RET_OBJ = null;
LANG = "en";
MENU = null;
PUSH_STATE = true;
BASE_PATH = null;
WAIT_ICON = null;
WAIT_ICON2 = false;
MENU_ID = 0;
BASE_FRAGMENT_INIT = null;
COUNTER = 1;
EDIT_RET_FUNCTION = null;
RET_CONTROL = null;
RIOT_INIT = null;
var glob = ՐՏ_modules["glob"];

var Page = ՐՏ_modules["page"].Page;

var TabMenuItem = ՐՏ_modules["tabmenuitem"].TabMenuItem;

var get_menu = ՐՏ_modules["tabmenu"].get_menu;

var on_get_tbl_value = ՐՏ_modules["popup"].on_get_tbl_value;
var on_new_tbl_value = ՐՏ_modules["popup"].on_new_tbl_value;
var on_get_row = ՐՏ_modules["popup"].on_get_row;
var on_popup_edit_new = ՐՏ_modules["popup"].on_popup_edit_new;
var on_popup_inline = ՐՏ_modules["popup"].on_popup_inline;
var on_popup_info = ՐՏ_modules["popup"].on_popup_info;
var on_popup_delete = ՐՏ_modules["popup"].on_popup_delete;
var on_cancel_inline = ՐՏ_modules["popup"].on_cancel_inline;
var refresh_fragment = ՐՏ_modules["popup"].refresh_fragment;
var on_edit_ok = ՐՏ_modules["popup"].on_edit_ok;
var on_delete_ok = ՐՏ_modules["popup"].on_delete_ok;
var ret_ok = ՐՏ_modules["popup"].ret_ok;

var set_table_type = ՐՏ_modules["tbl"].set_table_type;

var can_popup = ՐՏ_modules["tools"].can_popup;
var corect_href = ՐՏ_modules["tools"].corect_href;
var get_table_type = ՐՏ_modules["tools"].get_table_type;
var handle_class_click = ՐՏ_modules["tools"].handle_class_click;
var ajax_get = ՐՏ_modules["tools"].ajax_get;
var ajax_post = ՐՏ_modules["tools"].ajax_post;
var ajax_load = ՐՏ_modules["tools"].ajax_load;
var ajax_submit = ՐՏ_modules["tools"].ajax_submit;
var load_css = ՐՏ_modules["tools"].load_css;
var load_js = ՐՏ_modules["tools"].load_js;
var load_many_js = ՐՏ_modules["tools"].load_many_js;

function init_pagintor(pg) {
    var totalPages, page_number, options, form, url, paginate;
    if (pg.length > 0) {
        paginate = true;
        totalPages = pg.attr("totalPages");
        page_number = pg.attr("start_page");
        options = {
            "totalPages": +totalPages,
            "startPage": +page_number,
            "visiblePages": 3,
            "first": "<<",
            "prev": "<",
            "next": ">",
            "last": ">>",
            "onPageClick": function(event, page) {
                var form, url, active_button, WAIT_ICON2;
                form = pg.closest(".refr_object").find("form.refr_source");
                if (form) {
                    function _on_new_page(data) {
                        pg.closest(".content").find(".tabsort tbody").html(jQuery(jQuery.parseHTML(data)).find(".tabsort tbody").html());
                        fragment_init(pg.closest(".content").find(".tabsort tbody"));
                        if (WAIT_ICON2) {
                            $("#loading-indicator").hide();
                            WAIT_ICON2 = false;
                        }
                    }
                    url = pg.attr("href").replace("[[page]]", page) + "&only_content=1";
                    form.attr("action", url);
                    form.attr("href", url);
                    active_button = pg.find(".page active");
                    WAIT_ICON2 = true;
                    $("#loading-indicator").show();
                    ajax_post(url, form.serialize(), _on_new_page);
                }
            }
        };
        pg.twbsPagination(options);
        if (+page_number !== 1) {
            form = pg.closest(".refr_object").find("form.refr_source");
            url = pg.attr("href").replace("[[page]]", page_number) + "&only_content=1";
            form.attr("action", url);
            form.attr("href", url);
        }
    } else {
        paginate = false;
    }
    return paginate;
}
function fragment_init(elem) {
    if (typeof elem === "undefined") elem = null;
    var elem2, paginator, paginate, _id, x, pos;
    if (elem) {
        elem2 = elem;
    } else {
        elem2 = glob.ACTIVE_PAGE.page;
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
    paginator = elem2.find(".pagination");
    paginate = init_pagintor(paginator);
    if (RIOT_INIT) {
        _id = jQuery(elem).uid();
        var ՐՏ_Iter2 = ՐՏ_Iterable(RIOT_INIT);
        for (var ՐՏ_Index2 = 0; ՐՏ_Index2 < ՐՏ_Iter2.length; ՐՏ_Index2++) {
            pos = ՐՏ_Iter2[ՐՏ_Index2];
            x = sprintf("riot.mount('#%s')", _id + " " + pos);
            eval(x);
        }
    }
    if (BASE_FRAGMENT_INIT) {
        BASE_FRAGMENT_INIT();
    }
}
function page_init(id, first_time) {
    if (typeof first_time === "undefined") first_time = true;
    var table_type, pg, paginate, elem2;
    table_type = get_table_type(jQuery("#" + id));
    if (glob.ACTIVE_PAGE) {
        pg = glob.ACTIVE_PAGE.page.find(".pagination");
        paginate = init_pagintor(pg);
    }
    set_table_type(table_type, "#" + id + " .tabsort", paginate);
    if (first_time) {
        elem2 = jQuery("body");
        handle_class_click(elem2, "get_tbl_value", on_get_tbl_value);
        handle_class_click(elem2, "new_tbl_value", on_new_tbl_value);
        handle_class_click(elem2, "get_row", on_get_row);
        jQuery("#" + id).on("click", "a", function(e) {
            var pos, src_obj, href, title, href2;
            if ($(e.currentTarget).attr("target") === "_blank") {
                return;
            }
            var ՐՏ_Iter3 = ՐՏ_Iterable([ "get_tbl_value", "new_tbl_value", "get_row" ]);
            for (var ՐՏ_Index3 = 0; ՐՏ_Index3 < ՐՏ_Iter3.length; ՐՏ_Index3++) {
                pos = ՐՏ_Iter3[ՐՏ_Index3];
                if (jQuery(this).hasClass(pos)) {
                    return true;
                }
            }
            src_obj = jQuery(this);
            var ՐՏ_Iter4 = ՐՏ_Iterable([ ["popup", on_popup_edit_new], ["popup_inline", on_popup_inline], ["popup_info", 
            on_popup_info], ["popup_delete", on_popup_delete] ]);
            for (var ՐՏ_Index4 = 0; ՐՏ_Index4 < ՐՏ_Iter4.length; ՐՏ_Index4++) {
                pos = ՐՏ_Iter4[ՐՏ_Index4];
                if (jQuery(this).hasClass(pos[0])) {
                    e.preventDefault();
                    pos[1](this);
                    return true;
                }
            }
            href = jQuery(this).attr("href");
            if (ՐՏ_in("#", href)) {
                return true;
            }
            e.preventDefault();
            if (ՐՏ_in($(e.currentTarget).attr("target"), ["_top", "_top2"])) {
                title = $(e.currentTarget).attr("title");
                if (!title) {
                    if (len(href) > 16) {
                        title = "..." + href.slice(-13);
                    } else {
                        title = href;
                    }
                }
                return _on_menu_href(this, title);
            }
            href2 = corect_href(href);
            ajax_get(href2, function(data) {
                if (ՐՏ_in("_parent_refr", data)) {
                    refresh_fragment(src_obj);
                } else {
                    if (APPLICATION_TEMPLATE === "modern") {
                        glob.ACTIVE_PAGE.page.html(data);
                        glob.ACTIVE_PAGE.set_href(href);
                        page_init(glob.ACTIVE_PAGE.id, false);
                    } else {
                        jQuery("#body_body").html(data);
                        page_init("body_body", false);
                    }
                    glob.ACTIVE_PAGE.set_href(href);
                    get_menu().get_active_item().url = href;
                    if (PUSH_STATE) {
                        history_push_state("title", href);
                    }
                }
            });
        });
    }
    glob.ACTIVE_PAGE.page.find("form").submit(function(e) {
        var data, submit_button, href;
        if (jQuery(this).attr("target") === "_blank") {
            jQuery(this).attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
            return true;
        }
        data = jQuery(this).serialize();
        if (ՐՏ_in("pdf=on", data)) {
            jQuery(this).attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
            return true;
        }
        if (ՐՏ_in("odf=on", data)) {
            jQuery(this).attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
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
            glob.ACTIVE_PAGE.page.html(data);
            page_init(id, false);
            if (WAIT_ICON) {
                WAIT_ICON.stop();
            }
            if (WAIT_ICON2) {
                jQuery("#loading-indicator").hide();
                WAIT_ICON2 = false;
            }
        });
    });
    fragment_init(glob.ACTIVE_PAGE.page);
}
function app_init(application_template, menu_id, lang, base_path, base_fragment_init, riot_init) {
    var SUBWIN;
    APPLICATION_TEMPLATE = application_template;
    LANG = lang;
    BASE_PATH = base_path;
    BASE_FRAGMENT_INIT = base_fragment_init;
    RIOT_INIT = riot_init;
    if (can_popup()) {
        SUBWIN = false;
        jQuery(function() {
            var pos, id, elem;
            jQuery("#tabs").tabdrop();
            if (APPLICATION_TEMPLATE !== "traditional") {
                pos = jQuery(".menu-href.btn-warning");
                if (pos.length > 0) {
                    elem = jQuery("#a_" + pos.closest("div.tab-pane").attr("id"));
                    elem.tab("show");
                } else {
                    elem = jQuery(".first_pos");
                    elem.tab("show");
                }
            } else {
                id = parseInt(menu_id) + 1;
                elem = jQuery("#tabs a:eq(" + id + ")");
                elem.tab("show");
            }
            jQuery(elem.prop("hash")).perfectScrollbar();
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
            jQuery("#logout").on("click", function() {
                window.location = jQuery(this).attr("action");
            });
            jQuery("#tabs a").click(function(e) {
                e.preventDefault();
                jQuery(this).tab("show");
                jQuery(jQuery(this).prop("hash")).perfectScrollbar();
            });
        });
    } else {
        SUBWIN = true;
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
        if (classname && ՐՏ_in("btn", classname)) {
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
                var id;
                if (APPLICATION_TEMPLATE === "modern") {
                    id = menu.new_page(title, data, href2, RIOT_INIT);
                } else {
                    jQuery("#body_body").html(data);
                    glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
                    glob.ACTIVE_PAGE.set_href(href2);
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
            if (APPLICATION_TEMPLATE === "standard" && ՐՏ_in("btn", classname)) {
                jQuery("a.menu-href").removeClass("btn-warning");
                jQuery(elem).addClass("btn-warning");
            }
            if (WAIT_ICON) {
                WAIT_ICON.start();
            } else {
                WAIT_ICON2 = true;
                $("#loading-indicator").show();
            }
            ajax_get(href2, _on_new_win);
            jQuery(".navbar-ex1-collapse").collapse("hide");
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
        glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
        page_init("body_body");
    } else {
        if (APPLICATION_TEMPLATE === "modern") {
            txt = jQuery("#body_body").text();
            txt2 = jQuery.trim(txt);
            if (txt2) {
                txt = jQuery.trim(jQuery("#body_body").html());
                jQuery("#body_body").html("");
                menu = get_menu();
                menu.new_page(jQuery("title").text(), txt, window.location.href, RIOT_INIT);
            }
        } else {
            glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
            page_init("body_body");
        }
    }
}
window.addEventListener("popstate", function(e) {
    var menu, x;
    if (e.state) {
        PUSH_STATE = false;
        if (APPLICATION_TEMPLATE === "modern") {
            menu = get_menu().activate(e.state, false);
        } else {
            x = e.state;
            jQuery("#body_body").html(LZString.decompress(x[0]));
            glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
            glob.ACTIVE_PAGE.set_href(document.location);
            if (APPLICATION_TEMPLATE === "standard") {
                jQuery("a.menu-href").removeClass("btn-warning");
                jQuery("#" + x[1]).addClass("btn-warning");
            }
        }
        PUSH_STATE = true;
    } else {
        if (APPLICATION_TEMPLATE === "modern") {
        } else {
            jQuery("#body_body").html("");
            glob.ACTIVE_PAGE = null;
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