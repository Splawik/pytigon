var INLINE_DIALOG_UPDATE_HTML = "\
<div class='panel panel-default'>\
    <div class='panel-body'>\
        <div class='dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline();return false'>Cancel</button>\
        <button type='button' class='btn btn-primary' onclick=\"javascript:on_edit_ok($(this).parent().parent().find('form:first'));return false;\">OK</button>\
    </div>\
</div>\
";

var INLINE_DIALOG_DELETE_HTML = "\
<div class='panel panel-default alert alert-danger'>\
    <div class='panel-body'>\
        <div class='dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline();return false'>Cancel</button>\
        <button type='button' class='btn btn-primary' onclick='on_delete_ok();return false'>OK</button>\
    </div>\
</div>\
";

var INLINE_DIALOG_INFO_HTML = "\
<div class='panel panel-default'>\
    <div class='panel-body'>\
        <div class='dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline();return false'>Cancel</button>\
    </div>\
</div>\
";

var INLINE_FRAME_HTML = "\
<div>\
        <div class='frame-data-inner'></div>\
</div>\
";
