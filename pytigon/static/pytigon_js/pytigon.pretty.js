'use strict';
import{AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, 
__init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, 
callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip}from "./org.transcrypt.__runtime__.js";
import{ajax_load}from "./pytigon_js.ajax_region.js";
import{register_global_event}from "./pytigon_js.events.js";
import{GlobalBus}from "./pytigon_js.component.js";
import{sync_and_run}from "./pytigon_js.db.js";
import{install_service_worker, service_worker_and_indexedDB_test}from "./pytigon_js.offline.js";
import{Page, get_menu}from "./pytigon_js.tabmenu.js";
var __name__ = "__main__";
window.PS = null;
window.MOUNTED_COMPONENTS = 0;
window.GLOBAL_BUS = GlobalBus();
window.START_MENU_ID = null;
export var _on_key = function(e) {
  if (e.which == 13) {
    var elem = jQuery(e.target);
    if (elem.prop("tagName") != "TEXTAREA") {
      var form = elem.closest("form");
      if (form.length > 0) {
        if (form.hasClass("DialogForm")) {
          e.preventDefault();
          on_edit_ok(false, form);
          return;
        }
      }
    }
  }
};
register_global_event("keypress", _on_key, null);
export var dom_content_loaded = function() {
  if (jQuery("#dialog-form-modal").length > 0) {
    jQuery(document).ajaxError(_on_error);
    if (window.APPLICATION_TEMPLATE == "traditional") {
      window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"));
    } else {
      window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"));
    }
  }
};
export var app_init = function(prj_name, application_template, menu_id, lang, base_path, base_fragment_init, component_init, offline_support, start_page, gen_time, callback) {
  if (typeof callback == "undefined" || callback != null && callback.hasOwnProperty("__kwargtrans__")) {
    var callback = null;
  }
  moment.locale(lang);
  window.ACTIVE_PAGE = null;
  window.PRJ_NAME = prj_name;
  window.APPLICATION_TEMPLATE = application_template;
  window.MENU = null;
  window.PUSH_STATE = true;
  if (base_path) {
    window.BASE_PATH = base_path;
  } else {
    window.BASE_PATH = "";
  }
  window.WAIT_ICON = null;
  window.WAIT_ICON2 = false;
  window.START_MENU_ID = menu_id;
  window.BASE_FRAGMENT_INIT = base_fragment_init;
  window.COUNTER = 1;
  window.EDIT_RET_FUNCTION = null;
  window.RET_CONTROL = null;
  window.COMPONENT_INIT = component_init;
  window.LANG = lang;
  window.GEN_TIME = gen_time;
  document.addEventListener("DOMContentLoaded", dom_content_loaded);
  if (offline_support) {
    if (navigator.onLine && service_worker_and_indexedDB_test()) {
      install_service_worker();
    }
  }
  var _on_sync = function(status) {
    if (status == "OK-refresh") {
      location.reload();
    }
  };
  sync_and_run("sys", _on_sync);
  var _init_start_wiki_page = function() {
    if (start_page && start_page != "None" && window.location.pathname == base_path) {
      var _on_load = function(responseText, status, response) {
        print("_init_strart_wiki_page::_on_load");
      };
      ajax_load(jQuery("#body_desktop"), base_path + start_page + "?only_content&schtml=1", _on_load);
    }
  };
  window.init_start_wiki_page = _init_start_wiki_page;
  _init_start_wiki_page();
  if (hasattr(window, "init_callback")) {
    window.init_callback();
  }
  jQuery.fn.editable.defaults.mode = "inline";
  jQuery.fn.combodate.defaults["maxYear"] = 2025;
};
export var _on_error = function(request, settings) {
  if (window.WAIT_ICON) {
    window.WAIT_ICON.stop();
    window.WAIT_ICON = null;
  }
  if (window.WAIT_ICON2) {
    jQuery("#loading-indicator").hide();
    window.WAIT_ICON2 = false;
  }
  if (settings.status == 200) {
    return;
  }
  if (settings.responseText) {
    var start = settings.responseText.indexOf("<body>");
    var end = settings.responseText.lastIndexOf("</body>");
    if (start > 0 && end > 0) {
      mount_html(jQuery("#dialog-data-error"), settings.responseText.substring(start + 6, end - 1));
      jQuery("#dialog-form-error").modal();
    } else {
      mount_html(jQuery("#dialog-data-error"), settings.responseText);
      jQuery("#dialog-form-error").modal();
    }
  }
};
export var jquery_ready = function() {
};
export var _on_popstate = function(e) {
  if (e.state) {
    window.PUSH_STATE = false;
    if (window.APPLICATION_TEMPLATE == "modern") {
      var menu = get_menu().activate(e.state, false);
    } else {
      var x = e.state;
      mount_html(jQuery("#body_desktop"), LZString.decompress(x[0]));
      window.ACTIVE_PAGE = Page(0, jQuery("#body_desktop"));
      window.ACTIVE_PAGE.set_href(document.location);
      if (window.APPLICATION_TEMPLATE == "standard") {
        jQuery("a.menu-href").removeClass("btn-warning");
        jQuery("#" + x[1]).addClass("btn-warning");
      }
    }
    window.PUSH_STATE = true;
  } else {
    if (window.APPLICATION_TEMPLATE == "modern") {
    } else {
      mount_html(jQuery("#body_desktop"), "", false, false);
      window.ACTIVE_PAGE = null;
      if (window.APPLICATION_TEMPLATE == "standard") {
        jQuery("a.menu-href").removeClass("btn-warning");
      }
    }
  }
};
window.addEventListener("popstate", _on_popstate, false);
