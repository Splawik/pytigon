'use strict';
import{AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, 
__init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, 
callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip}from "./org.transcrypt.__runtime__.js";
import{refresh_page}from "./pytigon_js.events.js";
import{ajax_post, get_table_type, load_js}from "./pytigon_js.tools.js";
var __name__ = "pytigon_js.tbl";
export var datetable_set_height = function(element) {
  if (jQuery(element).hasClass("table_get")) {
    return;
  }
  if (!jQuery(element).is(":visible")) {
    return;
  }
  var elem = jQuery(element).closest(".tabsort_panel");
  var table_offset = elem.offset().top;
  var dy_win = jQuery(window).height();
  var dy = dy_win - table_offset;
  if (dy < 200) {
    var dy = 200;
  }
  var panel = elem.find(".fixed-table-toolbar");
  if (!panel.is(":visible")) {
    dy += panel.height() - 15;
  }
  jQuery(element).bootstrapTable("resetView", dict({"height":dy - 5}));
};
export var datatable_refresh = function(table) {
  table.bootstrapTable("refresh");
};
export var _rowStyle = function(value, row, index) {
  var x = jQuery("<div>" + value["cid"] + "</div>").find("div.td_information");
  if (x.length > 0) {
    var c = x.attr("class").py_replace("td_information", "").py_replace(" ", "");
    if (c.length > 0) {
      return {"classes":c};
    }
  }
  return {};
};
export var prepare_datatable = function(table) {
  var _local_fun = function(index) {
    var td = jQuery(this).parent();
    var tr = td.parent();
    var l = tr.find("td").length;
    tr.find("td:gt(0)").remove();
    td.attr("colspan", l);
  };
  table.find("div.second_row").each(_local_fun);
};
export var datatable_ajax = function(params) {
  var url = params["url"];
  var success = params["success"];
  if (__in__("form", dict(params["data"]))) {
    var form = params["data"]["form"];
    delete params["data"]["form"];
    var d = jQuery.param(params["data"]);
    url += "?" + d;
    var _on_post_data = function(data) {
      var d2 = JSON.parse(data);
      success(d2);
    };
    ajax_post(url, form, _on_post_data);
  } else {
    var d = jQuery.param(params["data"]);
    url += "?" + d;
    var _on_get_data = function(data) {
      var d2 = JSON.parse(data);
      success(d2);
    };
    ajax_get(url, _on_get_data);
  }
};
export var init_table = function(table, table_type) {
  if (table_type == "datatable") {
    var onLoadSuccess = function(data) {
      prepare_datatable(table);
      var _pagination = function() {
        jQuery(table).closest(".fixed-table-container").find(".fixed-table-pagination ul.pagination a").addClass("page-link");
      };
      setTimeout(_pagination, 0);
      return false;
    };
    var queryParams = function(p) {
      var refr_block = jQuery(table).closest(".ajax-frame");
      var src = refr_block.find(".ajax-link");
      if (src.length > 0 && src.prop("tagName") == "FORM") {
        p["form"] = src.serialize();
      }
      return p;
    };
    if (table.hasClass("table_get")) {
      table.bootstrapTable(dict({"onLoadSuccess":onLoadSuccess, "height":350, "rowStyle":_rowStyle, "queryParams":queryParams, "ajax":datatable_ajax}));
    } else {
      table.bootstrapTable(dict({"onLoadSuccess":onLoadSuccess, "rowStyle":_rowStyle, "queryParams":queryParams, "ajax":datatable_ajax}));
    }
    var init_bootstrap_table = function(e, data) {
      table.find("a.editable").editable(dict({"step":"any"}));
      var on_hidden_editable = function(e, reason) {
        if (reason == "save" || reason == "nochange") {
          var py_next = jQuery(this).closest("tr").next().find(".editable");
          if (py_next.length > 0) {
            if (py_next.hasClass("autoopen")) {
              var edit_next = function() {
                py_next.editable("show");
              };
              setTimeout(edit_next, 300);
            } else {
              py_next.focus();
            }
          }
        }
      };
      table.find("a.editable").on("hidden", on_hidden_editable);
    };
    table.on("post-body.bs.table", init_bootstrap_table);
    var table_panel = jQuery(table).closest(".content");
    var btn = table_panel.find(".tabsort-toolbar-expand");
    if (btn) {
      var _handle_toolbar_expand = function(elem) {
        var panel = table_panel.find(".fixed-table-toolbar");
        var panel2 = jQuery(".list_content_header_two_row");
        if (jQuery(this).hasClass("active")) {
          panel.show();
          panel2.show();
        } else {
          panel.hide();
          panel2.hide();
        }
        process_resize(document.body);
      };
      table_panel.on("click", ".tabsort-toolbar-expand", _handle_toolbar_expand);
      if (btn.hasClass("active")) {
        var panel = table_panel.find(".fixed-table-toolbar");
        var panel2 = jQuery(".list_content_header_two_row");
        panel.hide();
        panel2.hide();
      }
    }
    var _process_resize = function(size_object) {
      datetable_set_height(table[0]);
    };
    table[0].process_resize = _process_resize;
  }
};
export var table_loadeddata = function(event) {
  if (getattr(event, "data")) {
    if (event.data && __in__("RETURN_OK", event.data)) {
      jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable("refresh");
    } else {
      refresh_page(event.target, event.data, null, null, null);
    }
  } else {
    jQuery(event.target).find("table[name=tabsort].datatable").bootstrapTable("refresh");
  }
};
window.table_loadeddata = table_loadeddata;

