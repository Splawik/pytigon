APPLICATION_TEMPLATE = "standard";
RET_BUFOR = null;
RET_OBJ = null;
IS_POPUP = false;
SUBWIN = false;
LANG = "en";
MENU = null;
var _on_close_page = function(event) {
  
  get_menu().remove_page(__replace_method(jQuery(this).attr("id"), "button_", ""));
}

var Menu = function() {
  Menu.__init__(this);
  this.__class__ = Menu;
  this.__uid__ = ("￼" + _PythonJS_UID);
  _PythonJS_UID += 1;
}

Menu.__uid__ = ("￼" + _PythonJS_UID);
_PythonJS_UID += 1;
Menu.prototype.__init__ = function() {
  
  this.id = 0;
  this.titles = __jsdict([]);
}

Menu.__init__ = function () { return Menu.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
Menu.prototype.is_open = function(title) {
  
  if (__test_if_true__((__contains__(this.titles, title) && this.titles[((title.__uid__) ? title.__uid__ : ((title instanceof Array) ? JSON.stringify(title) : title))]))) {
    return true;
  } else {
    return false;
  }
}

Menu.is_open = function () { return Menu.prototype.is_open.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
Menu.prototype.activate = function(title) {
  var _id;
  _id = this.titles[((title.__uid__) ? title.__uid__ : ((title instanceof Array) ? JSON.stringify(title) : title))];
  $(__sprintf("#li_%s a", [_id])).tab("show");
}

Menu.activate = function () { return Menu.prototype.activate.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
Menu.prototype.new_pos = function(title) {
  var _id;
  if (__test_if_true__(this.is_open())) {
    this.activate(title);
    return null;
  } else {
    var __left0,__right1;
    __left0 = "tab";
    __right1 = str(this.id);
    _id = (((typeof(__left0) instanceof Array ? JSON.stringify(typeof(__left0))==JSON.stringify("number") : typeof(__left0)==="number")) ? (__left0 + __right1) : __add_op(__left0, __right1));
    this.titles[((title.__uid__) ? title.__uid__ : ((title instanceof Array) ? JSON.stringify(title) : title))] = _id;
    jQuery("#tabs2").append(__sprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-danger btn-xs' title='remove page' type='button'><span class='glyphicon glyphicon-remove'></span></button></li>", [_id, _id, title, _id]));
    jQuery("#tabs2_content").append(__sprintf("<div class='tab-pane' id='%s'></div>", [_id]));
    $("#tabs2 a:last").tab("show");
    $(__sprintf("#button_%s", [_id])).click(_on_close_page);
    this.id += 1;
    return _id;
  }
}

Menu.new_pos = function () { return Menu.prototype.new_pos.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
Menu.prototype.remove_page = function(id) {
  
    var __iter1 = this.titles;
  if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
  for (var __idx1=0; __idx1 < __iter1.length; __idx1++) {
    var pos = __iter1[ __idx1 ];
    if ((this.titles[((pos.__uid__) ? pos.__uid__ : ((pos instanceof Array) ? JSON.stringify(pos) : pos))] instanceof Array ? JSON.stringify(this.titles[((pos.__uid__) ? pos.__uid__ : ((pos instanceof Array) ? JSON.stringify(pos) : pos))])==JSON.stringify(id) : this.titles[((pos.__uid__) ? pos.__uid__ : ((pos instanceof Array) ? JSON.stringify(pos) : pos))]===id)) {
      this.titles[((pos.__uid__) ? pos.__uid__ : ((pos instanceof Array) ? JSON.stringify(pos) : pos))] = null;
    }
  }
  jQuery(__sprintf("#li_%s", [id])).remove();
  jQuery(__sprintf("#%s", [id])).remove();
  jQuery("#tabs2 a:last").tab("show");
}

Menu.remove_page = function () { return Menu.prototype.remove_page.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
Menu.prototype.__properties__ = {  };
Menu.prototype.__unbound_methods__ = {  };
var get_menu = function() {
  
  if (__test_if_true__(! (MENU))) {
    MENU =  new Menu();
  }
  return MENU;
}

var cmd_to_python = function(value) {
  
  document.title = ":";
  var __left2,__right3;
  __left2 = ":";
  __right3 = value;
  document.title = (((typeof(__left2) instanceof Array ? JSON.stringify(typeof(__left2))==JSON.stringify("number") : typeof(__left2)==="number")) ? (__left2 + __right3) : __add_op(__left2, __right3));
}

var is_hybrid = function() {
  
  if ((window.location.host instanceof Array ? JSON.stringify(window.location.host)==JSON.stringify("127.0.0.2") : window.location.host==="127.0.0.2")) {
    return true;
  } else {
    return false;
  }
}

var to_absolute_url = function(url) {
  
  if ((url[0] instanceof Array ? JSON.stringify(url[0])==JSON.stringify("/") : url[0]==="/")) {
    var __left4,__right5;
    __left4 = window.location.protocol;
    __right5 = "//";
    var __left6,__right7;
    __left6 = (((typeof(__left4) instanceof Array ? JSON.stringify(typeof(__left4))==JSON.stringify("number") : typeof(__left4)==="number")) ? (__left4 + __right5) : __add_op(__left4, __right5));
    __right7 = window.location.host;
    var __left8,__right9;
    __left8 = (((typeof(__left6) instanceof Array ? JSON.stringify(typeof(__left6))==JSON.stringify("number") : typeof(__left6)==="number")) ? (__left6 + __right7) : __add_op(__left6, __right7));
    __right9 = url;
    return (((typeof(__left8) instanceof Array ? JSON.stringify(typeof(__left8))==JSON.stringify("number") : typeof(__left8)==="number")) ? (__left8 + __right9) : __add_op(__left8, __right9));
  } else {
    var __left10,__right11;
    __left10 = window.location.protocol;
    __right11 = "//";
    var __left12,__right13;
    __left12 = (((typeof(__left10) instanceof Array ? JSON.stringify(typeof(__left10))==JSON.stringify("number") : typeof(__left10)==="number")) ? (__left10 + __right11) : __add_op(__left10, __right11));
    __right13 = window.location.host;
    var __left14,__right15;
    __left14 = (((typeof(__left12) instanceof Array ? JSON.stringify(typeof(__left12))==JSON.stringify("number") : typeof(__left12)==="number")) ? (__left12 + __right13) : __add_op(__left12, __right13));
    __right15 = window.location.pathname;
    var __left16,__right17;
    __left16 = (((typeof(__left14) instanceof Array ? JSON.stringify(typeof(__left14))==JSON.stringify("number") : typeof(__left14)==="number")) ? (__left14 + __right15) : __add_op(__left14, __right15));
    __right17 = "/";
    var __left18,__right19;
    __left18 = (((typeof(__left16) instanceof Array ? JSON.stringify(typeof(__left16))==JSON.stringify("number") : typeof(__left16)==="number")) ? (__left16 + __right17) : __add_op(__left16, __right17));
    __right19 = url;
    return (((typeof(__left18) instanceof Array ? JSON.stringify(typeof(__left18))==JSON.stringify("number") : typeof(__left18)==="number")) ? (__left18 + __right19) : __add_op(__left18, __right19));
  }
}

var ret_submit = function() {
  
  RET_OBJ(RET_BUFOR, "OK");
}

var ajax_submit = function(form, func) {
  var RET_OBJ,queryString;
  if (__test_if_true__(is_hybrid())) {
    queryString = form.formSerialize();
    var __left20,__right21;
    __left20 = "href_to_var|";
    __right21 = to_absolute_url(form.attr("action"));
    var __left22,__right23;
    __left22 = (((typeof(__left20) instanceof Array ? JSON.stringify(typeof(__left20))==JSON.stringify("number") : typeof(__left20)==="number")) ? (__left20 + __right21) : __add_op(__left20, __right21));
    __right23 = "?";
    var __left24,__right25;
    __left24 = (((typeof(__left22) instanceof Array ? JSON.stringify(typeof(__left22))==JSON.stringify("number") : typeof(__left22)==="number")) ? (__left22 + __right23) : __add_op(__left22, __right23));
    __right25 = queryString;
    var __left26,__right27;
    __left26 = (((typeof(__left24) instanceof Array ? JSON.stringify(typeof(__left24))==JSON.stringify("number") : typeof(__left24)==="number")) ? (__left24 + __right25) : __add_op(__left24, __right25));
    __right27 = "|RET_BUFOR";
    cmd_to_python((((typeof(__left26) instanceof Array ? JSON.stringify(typeof(__left26))==JSON.stringify("number") : typeof(__left26)==="number")) ? (__left26 + __right27) : __add_op(__left26, __right27)));
    RET_OBJ = func;
    cmd_to_python("run_js|ret_submit();");
  } else {
    form.ajaxSubmit(__jsdict([[success, func]]));
  }
}

var can_popup = function() {
  
  if (__test_if_true__(IS_POPUP)) {
    return false;
  } else {
    return true;
  }
}

var _dialog_loaded = function(is_modal) {
  
  date_init();
  jQuery("div.resizable").resizable();
  if (__test_if_true__(is_modal)) {
    jQuery("div.dialog-form").modal();
    IS_POPUP = true;
  }
}

var on_dialog_load = function() {
  
  /*pass*/
}

var _dialog_ex_load1 = function(responseText, status, response) {
  
  if ((!(status instanceof Array ? JSON.stringify(status)==JSON.stringify("error") : status==="error"))) {
    _dialog_loaded(true);
    on_dialog_load();
  }
}

var dialog_ex_load2 = function(responseText, status, response) {
  
  if ((!(status instanceof Array ? JSON.stringify(status)==JSON.stringify("error") : status==="error"))) {
    _dialog_loaded(false);
    on_dialog_load();
  }
}

var dialog_ex_load_delete = function(responseText, status, response) {
  
  jQuery("div.dialog-form-delete").modal();
}

var dialog_ex_load_info = function(responseText, status, response) {
  
  jQuery("div.dialog-form-info").modal();
}

var _on_hide = function(e) {
  
  IS_POPUP = false;
  jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>");
}

var _on_popup = function() {
  var l;
  l = Ladda.create(this);
  if (__test_if_true__(is_hybrid())) {
    var __left28,__right29;
    __left28 = "href_to_elem|";
    __right29 = this.href;
    var __left30,__right31;
    __left30 = (((typeof(__left28) instanceof Array ? JSON.stringify(typeof(__left28))==JSON.stringify("number") : typeof(__left28)==="number")) ? (__left28 + __right29) : __add_op(__left28, __right29));
    __right31 = "|#dialog-data";
    cmd_to_python((((typeof(__left30) instanceof Array ? JSON.stringify(typeof(__left30))==JSON.stringify("number") : typeof(__left30)==="number")) ? (__left30 + __right31) : __add_op(__left30, __right31)));
    jQuery("div.dialog-form").modal();
  } else {
    if (__test_if_true__(can_popup())) {
      jQuery("div.dialog-data").load(jQuery(this).attr("href"), null, _dialog_ex_load1);
    } else {
      l.start();
      jQuery(".inline_dialog").remove();
      var __left32,__right33;
      __left32 = "<tr class='inline_dialog'><td colspan='20'>";
      __right33 = INLINE_DIALOG_UPDATE_HTML;
      var __left34,__right35;
      __left34 = (((typeof(__left32) instanceof Array ? JSON.stringify(typeof(__left32))==JSON.stringify("number") : typeof(__left32)==="number")) ? (__left32 + __right33) : __add_op(__left32, __right33));
      __right35 = "</td></tr>";
      var __left36,__right37;
      __left36 = "<tr class='inline_dialog'><td colspan='20'>";
      __right37 = INLINE_DIALOG_UPDATE_HTML;
      var __left38,__right39;
      __left38 = (((typeof(__left36) instanceof Array ? JSON.stringify(typeof(__left36))==JSON.stringify("number") : typeof(__left36)==="number")) ? (__left36 + __right37) : __add_op(__left36, __right37));
      __right39 = "</td></tr>";
      var __left40,__right41;
      __left40 = "<tr class='inline_dialog'><td colspan='20'>";
      __right41 = INLINE_DIALOG_UPDATE_HTML;
      var __left42,__right43;
      __left42 = (((typeof(__left40) instanceof Array ? JSON.stringify(typeof(__left40))==JSON.stringify("number") : typeof(__left40)==="number")) ? (__left40 + __right41) : __add_op(__left40, __right41));
      __right43 = "</td></tr>";
      jQuery((((typeof(__left38) instanceof Array ? JSON.stringify(typeof(__left38))==JSON.stringify("number") : typeof(__left38)==="number")) ? (__left38 + __right39) : __add_op(__left38, __right39))).insertAfter(jQuery(this).parents("tr"));
                  var _on_loaded = function(responseText, status, response) {
        
        dialog_ex_load2(responseText, status, response);
        l.stop();
      }

      jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null, _on_loaded);
    }
  }
  return false;
}

var _on_popup_info = function() {
  
  if (__test_if_true__(is_hybrid())) {
    var __left44,__right45;
    __left44 = "href_to_elem|";
    __right45 = this.href;
    var __left46,__right47;
    __left46 = (((typeof(__left44) instanceof Array ? JSON.stringify(typeof(__left44))==JSON.stringify("number") : typeof(__left44)==="number")) ? (__left44 + __right45) : __add_op(__left44, __right45));
    __right47 = "|#dialog-data-info";
    cmd_to_python((((typeof(__left46) instanceof Array ? JSON.stringify(typeof(__left46))==JSON.stringify("number") : typeof(__left46)==="number")) ? (__left46 + __right47) : __add_op(__left46, __right47)));
    jQuery("div.dialog-form-info").modal();
  } else {
    if (__test_if_true__(can_popup())) {
      jQuery("div.dialog-data-info").load(jQuery(this).attr("href"), null, dialog_ex_load_info);
    } else {
      jQuery(".inline_dialog").remove();
      var __left48,__right49;
      __left48 = "<tr class='inline_dialog'><td colspan='20'>";
      __right49 = INLINE_DIALOG_INFO_HTML;
      var __left50,__right51;
      __left50 = (((typeof(__left48) instanceof Array ? JSON.stringify(typeof(__left48))==JSON.stringify("number") : typeof(__left48)==="number")) ? (__left48 + __right49) : __add_op(__left48, __right49));
      __right51 = "</td></tr>";
      var __left52,__right53;
      __left52 = "<tr class='inline_dialog'><td colspan='20'>";
      __right53 = INLINE_DIALOG_INFO_HTML;
      var __left54,__right55;
      __left54 = (((typeof(__left52) instanceof Array ? JSON.stringify(typeof(__left52))==JSON.stringify("number") : typeof(__left52)==="number")) ? (__left52 + __right53) : __add_op(__left52, __right53));
      __right55 = "</td></tr>";
      var __left56,__right57;
      __left56 = "<tr class='inline_dialog'><td colspan='20'>";
      __right57 = INLINE_DIALOG_INFO_HTML;
      var __left58,__right59;
      __left58 = (((typeof(__left56) instanceof Array ? JSON.stringify(typeof(__left56))==JSON.stringify("number") : typeof(__left56)==="number")) ? (__left56 + __right57) : __add_op(__left56, __right57));
      __right59 = "</td></tr>";
      jQuery((((typeof(__left54) instanceof Array ? JSON.stringify(typeof(__left54))==JSON.stringify("number") : typeof(__left54)==="number")) ? (__left54 + __right55) : __add_op(__left54, __right55))).insertAfter(jQuery(this).parents("tr"));
      jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null);
    }
  }
  return false;
}

var _on_popup_delete = function() {
  
  if (__test_if_true__(is_hybrid())) {
    var __left60,__right61;
    __left60 = "href_to_elem|";
    __right61 = this.href;
    var __left62,__right63;
    __left62 = (((typeof(__left60) instanceof Array ? JSON.stringify(typeof(__left60))==JSON.stringify("number") : typeof(__left60)==="number")) ? (__left60 + __right61) : __add_op(__left60, __right61));
    __right63 = "|#dialog-data-delete";
    cmd_to_python((((typeof(__left62) instanceof Array ? JSON.stringify(typeof(__left62))==JSON.stringify("number") : typeof(__left62)==="number")) ? (__left62 + __right63) : __add_op(__left62, __right63)));
    jQuery("div.dialog-form-delete").modal();
  } else {
    if (__test_if_true__(can_popup())) {
      jQuery("div.dialog-data-delete").load(jQuery(this).attr("href"), null, dialog_ex_load_delete);
    } else {
      jQuery(".inline_dialog").remove();
      var __left64,__right65;
      __left64 = "<tr class='inline_dialog'><td colspan='20'>";
      __right65 = INLINE_DIALOG_DELETE_HTML;
      var __left66,__right67;
      __left66 = (((typeof(__left64) instanceof Array ? JSON.stringify(typeof(__left64))==JSON.stringify("number") : typeof(__left64)==="number")) ? (__left64 + __right65) : __add_op(__left64, __right65));
      __right67 = "</td></tr>";
      var __left68,__right69;
      __left68 = "<tr class='inline_dialog'><td colspan='20'>";
      __right69 = INLINE_DIALOG_DELETE_HTML;
      var __left70,__right71;
      __left70 = (((typeof(__left68) instanceof Array ? JSON.stringify(typeof(__left68))==JSON.stringify("number") : typeof(__left68)==="number")) ? (__left68 + __right69) : __add_op(__left68, __right69));
      __right71 = "</td></tr>";
      var __left72,__right73;
      __left72 = "<tr class='inline_dialog'><td colspan='20'>";
      __right73 = INLINE_DIALOG_DELETE_HTML;
      var __left74,__right75;
      __left74 = (((typeof(__left72) instanceof Array ? JSON.stringify(typeof(__left72))==JSON.stringify("number") : typeof(__left72)==="number")) ? (__left72 + __right73) : __add_op(__left72, __right73));
      __right75 = "</td></tr>";
      jQuery((((typeof(__left70) instanceof Array ? JSON.stringify(typeof(__left70))==JSON.stringify("number") : typeof(__left70)==="number")) ? (__left70 + __right71) : __add_op(__left70, __right71))).insertAfter(jQuery(this).parents("tr"));
      jQuery("div.dialog-data-inner").load(jQuery(this).attr("href"), null);
    }
  }
  return false;
}

var _on_error = function(request, settings) {
  var end,start;
  [start, end];
  start = settings.responseText.indexOf("<body>");
  end = settings.responseText.lastIndexOf("</body>");
  if (__test_if_true__((( start ) > 0 && ( end ) > 0))) {
    var __left76,__right77;
    __left76 = start;
    __right77 = 6;
    jQuery("div.dialog-data-error").html(settings.responseText.substring((((typeof(__left76) instanceof Array ? JSON.stringify(typeof(__left76))==JSON.stringify("number") : typeof(__left76)==="number")) ? (__left76 + __right77) : __add_op(__left76, __right77)), (end - 1)));
    jQuery("div.dialog-form-error").modal();
  } else {
    jQuery("div.dialog-data-error").html(settings.responseText);
    jQuery("div.dialog-form-error").modal();
  }
}

var _refresh_win = function(responseText, form) {
  var filter,subform;
  if (__contains__(responseText, "RETURN_OK")) {
    subform = form.closest("div.inline_frame");
    if (( subform.length ) > 0) {
      subform.find("div.frame-data-inner").load(subform.attr("href"), null);
    } else {
      filter = form.closest("div.content").find("form.TableFiltr");
      jQuery("div.dialog-form").fadeTo("slow", 0.5);
      if (( filter.length ) > 0) {
        filter.attr("action", window.location.href);
        filter.submit();
      }
    }
  } else {
    jQuery("div.dialog-data").html(responseText);
  }
}

var on_edit_ok = function(form) {
  
      var _on_refresh_win = function(data) {
    
    _refresh_win(data, form);
  }

  jQuery.ajax(__jsdict([["type", "POST"], ["url", form.attr("action")], ["data", form.serialize()], ["success", _on_refresh_win]]));
  return false;
}

var on_delete_ok = function(form) {
  
      var _on_refresh_win = function(data) {
    
    _refresh_win(data, form);
  }

  jQuery.ajax(__jsdict([["type", "POST"], ["url", form.attr("action")], ["data", form.serialize()], ["success", _on_refresh_win]]));
  return false;
}

var on_cancel_inline = function() {
  
  jQuery(".inline_dialog").remove();
}

var date_init = function() {
  
  jQuery(".dateinput").datetimepicker(__jsdict([["pickTime", false], ["format", "YYYY-MM-DD"], ["language", LANG]]));
  jQuery(".datetimeinput").datetimepicker(__jsdict([["format", "YYYY-MM-DD hh:mm"], ["language", "pl"]]));
}

var popup_init = function() {
  
  jQuery("div.dialog-form").on("hide.bs.modal", _on_hide);
  jQuery("a.popup").click(_on_popup);
  jQuery("a.popup_info").click(_on_popup_info);
  jQuery("a.popup_delete").click(_on_popup_delete);
}

var _on_menu_href = function(event) {
  var title,l,href,classname,menu;
  if ((!(APPLICATION_TEMPLATE instanceof Array ? JSON.stringify(APPLICATION_TEMPLATE)==JSON.stringify("traditional") : APPLICATION_TEMPLATE==="traditional"))) {
    title = $(this).text();
    menu = get_menu();
    classname = $(this).attr("class");
    if (__contains__(classname, "btn")) {
      l = Ladda.create(this);
    } else {
      l = null;
    }
    if (__test_if_true__(((APPLICATION_TEMPLATE instanceof Array ? JSON.stringify(APPLICATION_TEMPLATE)==JSON.stringify("modern") : APPLICATION_TEMPLATE==="modern") && menu.is_open(title)))) {
      menu.activate(title);
    } else {
                  var _on_new_win = function(data) {
        var id;
        if ((APPLICATION_TEMPLATE instanceof Array ? JSON.stringify(APPLICATION_TEMPLATE)==JSON.stringify("modern") : APPLICATION_TEMPLATE==="modern")) {
          id = menu.new_pos(title);
          var __left78,__right79;
          __left78 = "#";
          __right79 = id;
          var __left80,__right81;
          __left80 = "#";
          __right81 = id;
          var __left82,__right83;
          __left82 = "#";
          __right83 = id;
          jQuery((((typeof(__left80) instanceof Array ? JSON.stringify(typeof(__left80))==JSON.stringify("number") : typeof(__left80)==="number")) ? (__left80 + __right81) : __add_op(__left80, __right81))).html(data);
        } else {
          jQuery("#body_body").html(data);
        }
        popup_init();
        if (__test_if_true__(l)) {
          l.stop();
        }
      }

      href = jQuery(this).attr("href");
      if (__contains__(href, "?")) {
        var __left84,__right85;
        __left84 = href;
        __right85 = "&hybrid=1";
        href = (((typeof(__left84) instanceof Array ? JSON.stringify(typeof(__left84))==JSON.stringify("number") : typeof(__left84)==="number")) ? (__left84 + __right85) : __add_op(__left84, __right85));
      } else {
        var __left86,__right87;
        __left86 = href;
        __right87 = "?hybrid=1";
        href = (((typeof(__left86) instanceof Array ? JSON.stringify(typeof(__left86))==JSON.stringify("number") : typeof(__left86)==="number")) ? (__left86 + __right87) : __add_op(__left86, __right87));
      }
      if (__test_if_true__(((APPLICATION_TEMPLATE instanceof Array ? JSON.stringify(APPLICATION_TEMPLATE)==JSON.stringify("standard") : APPLICATION_TEMPLATE==="standard") && __contains__(classname, "btn")))) {
        jQuery("a.menu-href").removeClass("btn-warning").addClass("btn-info");
        jQuery(this).removeClass("btn-info").addClass("btn-warning");
      }
      if (__test_if_true__(l)) {
        l.start();
      }
      jQuery.ajax(__jsdict([["type", "GET"], ["url", href], ["success", _on_new_win]]));
      $(this).closest(".dropdown-menu").dropdown("toggle");
      $(".navbar-ex1-collapse").collapse("hide");
    }
    return false;
  }
}

var jquery_init = function(application_template, scroll_table, menu_id, lang) {
  var SUBWIN;
  APPLICATION_TEMPLATE = application_template;
  LANG = lang;
  if (__test_if_true__(IS_POPUP)) {
    SUBWIN = true;
  } else {
    SUBWIN = false;
  }
  if (__test_if_true__(! (SUBWIN))) {
    if ((scroll_table instanceof Array ? JSON.stringify(scroll_table)==JSON.stringify("True") : scroll_table==="True")) {
      jQuery(window).load(stick_header);
    }
            var _tabs = function() {
      
      jQuery("#menu_tabs").tabs();
      if ((!(APPLICATION_TEMPLATE instanceof Array ? JSON.stringify(APPLICATION_TEMPLATE)==JSON.stringify("traditional") : APPLICATION_TEMPLATE==="traditional"))) {
        jQuery("#tabs a:eq(1)").tab("show");
      } else {
        var __left88,__right89;
        __left88 = "#tabs a:eq(";
        __right89 = str(menu_id);
        var __left90,__right91;
        __left90 = (((typeof(__left88) instanceof Array ? JSON.stringify(typeof(__left88))==JSON.stringify("number") : typeof(__left88)==="number")) ? (__left88 + __right89) : __add_op(__left88, __right89));
        __right91 = ")";
        var __left92,__right93;
        __left92 = "#tabs a:eq(";
        __right93 = str(menu_id);
        var __left94,__right95;
        __left94 = (((typeof(__left92) instanceof Array ? JSON.stringify(typeof(__left92))==JSON.stringify("number") : typeof(__left92)==="number")) ? (__left92 + __right93) : __add_op(__left92, __right93));
        __right95 = ")";
        var __left96,__right97;
        __left96 = "#tabs a:eq(";
        __right97 = str(menu_id);
        var __left98,__right99;
        __left98 = (((typeof(__left96) instanceof Array ? JSON.stringify(typeof(__left96))==JSON.stringify("number") : typeof(__left96)==="number")) ? (__left96 + __right97) : __add_op(__left96, __right97));
        __right99 = ")";
        jQuery((((typeof(__left94) instanceof Array ? JSON.stringify(typeof(__left94))==JSON.stringify("number") : typeof(__left94)==="number")) ? (__left94 + __right95) : __add_op(__left94, __right95))).tab("show");
      }
      jQuery("a.menu-href").click(_on_menu_href);
    }

    jQuery(_tabs);
  }
}

var jquery_ready = function() {
  
  jQuery(document).ajaxError(_on_error);
  date_init();
  jQuery("div.resizable").resizable();
}
