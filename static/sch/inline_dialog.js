var INLINE_DIALOG_UPDATE_HTML = "\
<div class='panel panel-default'>\
    <div class='panel-body'>\
        <div class='refr_target dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
        <button type='button' class='btn btn-primary' onclick=\"javascript:on_edit_ok($(this).parent().parent().find('form:first'));return false;\">OK</button>\
    </div>\
</div>\
";

var INLINE_DIALOG_DELETE_HTML = "\
<div class='panel panel-default alert alert-danger'>\
    <div class='panel-body'>\
        <div class='refr_target dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
        <button type='button' class='btn btn-primary' onclick='on_delete_ok($(this));return false'>OK</button>\
    </div>\
</div>\
";

var INLINE_DIALOG_INFO_HTML = "\
<div class='panel panel-default'>\
    <div class='panel-body'>\
        <div class='refr_target dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
    </div>\
</div>\
";

var INLINE_TABLE_HTML = "\
<div class='indent shadow-z-2'>\
    <button type='button' class='btn btn-danger btn-xs' onclick='on_cancel_inline($(this));return false'>\
        <span class='glyphicon glyphicon-remove' aria-hidden='true'></span>\
    </button>\
    <div class='refr_target dialog-data-inner'></div>\
</div>\
";


var INLINE_FRAME_HTML = "\
<div>\
        <div class='frame-data-inner'></div>\
</div>\
";
