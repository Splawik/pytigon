'use strict';import{AssertionError,AttributeError,BaseException,DeprecationWarning,Exception,IndexError,IterableError,KeyError,NotImplementedError,RuntimeWarning,StopIteration,UserWarning,ValueError,Warning,__JsIterator__,__PyIterator__,__Terminal__,__add__,__and__,__call__,__class__,__envir__,__eq__,__floordiv__,__ge__,__get__,__getcm__,__getitem__,__getslice__,__getsm__,__gt__,__i__,__iadd__,__iand__,__idiv__,__ijsmod__,__ilshift__,__imatmul__,__imod__,__imul__,__in__,__init__,__ior__,__ipow__,
__irshift__,__isub__,__ixor__,__jsUsePyNext__,__jsmod__,__k__,__kwargtrans__,__le__,__lshift__,__lt__,__matmul__,__mergefields__,__mergekwargtrans__,__mod__,__mul__,__ne__,__neg__,__nest__,__or__,__pow__,__pragma__,__proxy__,__pyUseJsNext__,__rshift__,__setitem__,__setproperty__,__setslice__,__sort__,__specialattrib__,__sub__,__super__,__t__,__terminal__,__truediv__,__withblock__,__xor__,abs,all,any,assert,bool,bytearray,bytes,callable,chr,copy,deepcopy,delattr,dict,dir,divmod,enumerate,filter,float,
getattr,hasattr,input,int,isinstance,issubclass,len,list,map,max,min,object,ord,pow,print,property,py_TypeError,py_iter,py_metatype,py_next,py_reversed,py_typeof,range,repr,round,set,setattr,sorted,str,sum,tuple,zip}from"./org.transcrypt.__runtime__.js";import{ajax_post,get_table_type,load_js,mount_html,register_fragment_init_fun}from"./tools.js";var __name__="tbl";export var datetable_set_height=function(){if(jQuery(this).hasClass("table_get"))return;if(!jQuery(this).is(":visible"))return;var elem=
jQuery(this).closest(".tabsort_panel");var table_offset=elem.offset().top;var dy_win=jQuery(window).height();var dy=dy_win-table_offset;if(dy<200)var dy=200;var panel=elem.find(".fixed-table-toolbar");if(!panel.is(":visible"))dy+=panel.height()-15;jQuery(this).bootstrapTable("resetView",dict({"height":dy-5}))};export var datatable_refresh=function(table){table.bootstrapTable("refresh")};export var _rowStyle=function(value,row,index){var x=jQuery("<div>"+value["cid"]+"</div>").find("div.td_information");
if(x.length>0){var c=x.attr("class").py_replace("td_information","");if(c.length>0)return dict({"classes":c})}return dict({})};export var prepare_datatable=function(table){var _local_fun=function(index){var td=jQuery(this).parent();var tr=td.parent();var l=tr.find("td").length;tr.find("td:gt(0)").remove();td.attr("colspan",l)};table.find("div.second_row").each(_local_fun)};export var datatable_ajax=function(params){var url=params["url"];var success=params["success"];if(__in__("form",dict(params["data"]))){var form=
params["data"]["form"];delete params["data"]["form"];var d=jQuery.param(params["data"]);url+="?"+d;var _on_post_data=function(data){var d2=JSON.parse(data);success(d2)};ajax_post(url,form,_on_post_data)}else{var d=jQuery.param(params["data"]);url+="?"+d;var _on_get_data=function(data){var d2=JSON.parse(data);success(d2)};ajax_get(url,_on_get_data)}};export var init_table=function(table,table_type){if(table_type=="datatable"){var onLoadSuccess=function(data){prepare_datatable(table);var _pagination=
function(){jQuery(table).closest(".fixed-table-container").find(".fixed-table-pagination ul.pagination a").addClass("page-link");datatable_onresize()};setTimeout(_pagination,0);return false};var queryParams=function(p){var refr_block=jQuery(table).closest(".refr_object");var src=refr_block.find(".refr_source");if(src.length>0&&src.prop("tagName")=="FORM")p["form"]=src.serialize();return p};if(table.hasClass("table_get"))table.bootstrapTable(dict({"onLoadSuccess":onLoadSuccess,"height":350,"rowStyle":_rowStyle,
"queryParams":queryParams,"ajax":datatable_ajax}));else table.bootstrapTable(dict({"onLoadSuccess":onLoadSuccess,"rowStyle":_rowStyle,"queryParams":queryParams,"ajax":datatable_ajax}));var table_panel=jQuery(table).closest(".content");var btn=table_panel.find(".tabsort-toolbar-expand");if(btn){var _handle_toolbar_expand=function(elem){var panel=table_panel.find(".fixed-table-toolbar");if(jQuery(this).hasClass("active")){panel.show();datatable_onresize()}else{panel.hide();datatable_onresize()}};table_panel.on("click",
".tabsort-toolbar-expand",_handle_toolbar_expand);if(btn.hasClass("active")){var panel=table_panel.find(".fixed-table-toolbar");panel.hide();datatable_onresize()}}}};export var content_set_height=function(){if(!jQuery(this).is(":visible"))return;if(jQuery(this).closest(".tabsort").length>0)return;if(jQuery(this).closest("#dialog-form-modal").length>0)return;var content_offset=jQuery(this).offset().top;var dy_win=jQuery(window).height();var dy=dy_win-content_offset-30;if(dy<200)var dy=200;jQuery(this).height(dy)};
export var datatable_onresize=function(){jQuery(".datatable:not(.table_get)").each(datetable_set_height);jQuery(".content").each(content_set_height)};window.datatable_onresize=datatable_onresize;export var _on_fragment_init=function(elem){datatable_onresize();var table_type=get_table_type(elem);var tbl=elem.find(".tabsort");if(tbl.length>0)init_table(tbl,table_type)};register_fragment_init_fun(_on_fragment_init);

//# sourceMappingURL=tbl.map