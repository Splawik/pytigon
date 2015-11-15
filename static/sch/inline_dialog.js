var INLINE_DIALOG_UPDATE_HTML = "\
<div class='modal-admin refr_object'>\
    <div class='modal-content'>\
        <div class='modal-header'>\
            <button type='button' class='close' data-dismiss='modal' aria-label='Close' onclick='on_cancel_inline($(this));return false'><span aria-hidden='true'>&times;</span></button>\
            <h4 class='modal-title'>Modal title</h4>\
        </div>\
        <div class='modal-body'>\
            <div class='refr_target dialog-data-inner'></div>\
        </div>\
        <div class='modal-footer'>\
            <button type='button' class='btn btn-default' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
            <button type='button' class='btn btn-primary' onclick=\"javascript:on_edit_ok($(this).parent().parent().find('form:first'));return false;\">OK</button>\
        </div>\
    </div>\
</div>\
";

var INLINE_DIALOG_DELETE_HTML = "\
<div class='panel panel-default alert alert-danger refr_object'>\
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
<div class='indent shadow-z-2 refr_object'>\
    <button type='button' class='btn btn-danger btn-xs' onclick='on_cancel_inline($(this));return false'>\
        <span class='fa fa-times' aria-hidden='true'></span>\
    </button>\
    <div class='refr_target dialog-data-inner'></div>\
</div>\
";


var INLINE_FRAME_HTML = "\
<div>\
        <div class='frame-data-inner'></div>\
</div>\
";
