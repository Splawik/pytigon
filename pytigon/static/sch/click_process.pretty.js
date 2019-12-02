'use strict';
import{AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, 
__init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, 
callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip}from "./org.transcrypt.__runtime__.js";
import{get_menu}from "./tabmenu.js";
import{refresh_fragment}from "./popup.js";
import{ajax_get, corect_href, mount_html}from "./tools.js";
var __name__ = "click_process";
export var get_value = function(elem, py_name) {
  if (elem.length > 0) {
    var x = elem.closest(".refr_object");
    if (x.length > 0) {
      var x2 = x.find(sprintf("[name='%s']", py_name));
      if (x2.length > 0) {
        return x2.val();
      }
    }
  }
  return "[[ERROR]]";
};
export var process_href = function(href, elem) {
  var ret = [];
  if (__in__("[[", href) && __in__("]]", href)) {
    var x1 = href.py_split("[[");
    var process = false;
    for (var pos of x1) {
      if (process) {
        if (__in__("]]", pos)) {
          var x2 = pos.py_split("]]", 1);
          var value = get_value(elem, x2[0]);
          if (value && value != "None") {
            ret.append(value + x2[1]);
          } else {
            ret.append(x2[1]);
          }
        } else {
          ret.append(pos);
        }
        var process = false;
      } else {
        ret.append(pos);
        var process = true;
      }
    }
    return "".join(ret);
  } else {
    return href;
  }
};
export var process_on_click = function(event_tab, elem) {
  if (typeof elem == "undefined" || elem != null && elem.hasOwnProperty("__kwargtrans__")) {
    var elem = null;
  }
  var _on_click = function(e) {
    var target = jQuery(e.currentTarget).attr("target");
    if (target == "_blank" || target == "_parent") {
      return true;
    }
    var src_obj = jQuery(this);
    if (__in__("xlink:href", e.currentTarget.attributes)) {
      var href = jQuery(this).attr("xlink:href");
    } else {
      var href = jQuery(this).attr("href");
    }
    if (href && __in__("#", href)) {
      return true;
    }
    if (!href) {
      return true;
    }
    var href = process_href(href, src_obj);
    for (var pos of event_tab) {
      if (pos[0] == "*" || pos[0] == target) {
        if (pos[1] == "*" || src_obj.hasClass(pos[1])) {
          if (pos[3]) {
            var url = corect_href(href, true);
          } else {
            if (pos[2]) {
              var url = corect_href(href, false);
            } else {
              var url = href;
            }
          }
          e.preventDefault();
          pos[4](url, this, e);
          return true;
        }
      }
    }
    e.preventDefault();
    var href2 = corect_href(href);
    var _on_data = function(data) {
      if (data && __in__("_parent_refr", data) || __in__(target, tuple(["refresh_obj", "refresh_page"]))) {
        if (target == "refresh_obj") {
          if (!refresh_fragment(src_obj, null, true)) {
            refresh_fragment(src_obj);
          }
        } else {
          refresh_fragment(src_obj);
        }
      } else {
        if (window.APPLICATION_TEMPLATE == "modern") {
          if (window.ACTIVE_PAGE) {
            mount_html(window.ACTIVE_PAGE.page, data);
          } else {
            mount_html(jQuery("#wiki_start"), data);
            return;
          }
          window.ACTIVE_PAGE.set_href(href);
        } else {
          mount_html(jQuery("#body_body"), data);
        }
        window.ACTIVE_PAGE.set_href(href);
        get_menu().get_active_item().url = href;
        if (window.PUSH_STATE) {
          history_push_state("title", href);
        }
      }
    };
    ajax_get(href2, _on_data);
  };
  if (elem) {
    elem.on("click", "a", _on_click);
  } else {
    jQuery("#tabs2_content").on("click", "a", _on_click);
    jQuery("#dialog-form-modal").on("click", "a", _on_click);
    jQuery("#body_body").on("click", "a", _on_click);
    jQuery("#wiki_start").on("click", "a", _on_click);
  }
};

