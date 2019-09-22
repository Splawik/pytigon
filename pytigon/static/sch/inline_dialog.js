var INLINE_DIALOG_UPDATE_HTML = "\
<div style='position:relative'>\
    <div class='dark_background'></div>\
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>\
        <div class='modal-content'>\
            <div class='modal-header'>\
                <h4 class='modal-title'>Modal title</h4>\
                <button type='button' class='btn btn-outline-secondary minimize' data-dismiss='modal' onclick='popup_minimize(this)' style='diplay:none;'> \
                    <span class='fa fa-window-minimize'></span> \
                </button> \
                <button type='button' class='btn btn-outline-secondary maximize' data-dismiss='modal' onclick='popup_maximize(this)'> \
                    <span class='fa fa-window-maximize'></span> \
                </button> \
                <button type='button' class='close btn-raised' data-dismiss='modal' aria-label='Close' onclick='on_cancel_inline($(this));return false'><span aria-hidden='true'>&times;</span></button>\
            </div>\
            <div class='modal-body inline-update-modal-body'>\
                <div class='refr_target dialog-data-inner'></div>\
            </div>\
            <div class='modal-footer'>\
                <button type='button' class='btn btn-secondary' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
                <button type='button' class='btn btn-primary' onclick=\"javascript:on_edit_ok($(this).parent().parent().find('form:first'));return false;\">OK</button>\
            </div>\
        </div>\
    </div>\
</div>\
";

var INLINE_TABLE_HTML = "\
<div style='position:relative'>\
    <div class='dark_background'></div>\
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>\
        <div class='modal-content'>\
            <div class='modal-header'>\
                <h4 class='modal-title'>{{title}}</h4>\
                <button type='button' class='btn btn-outline-secondary minimize' data-dismiss='modal' onclick='popup_minimize(this)' style='diplay:none;'> \
                    <span class='fa fa-window-minimize'></span> \
                </button> \
                <button type='button' class='btn btn-outline-secondary maximize' data-dismiss='modal' onclick='popup_maximize(this)'> \
                    <span class='fa fa-window-maximize'></span> \
                </button> \
                <button type='button' class='close btn-raised' data-dismiss='modal' aria-label='Close' onclick='on_cancel_inline($(this));return false'><span aria-hidden='true'>&times;</span></button>\
            </div>\
            <div class='modal-body inline-table-modal-body'>\
                <div class='refr_target dialog-data-inner'></div>\
            </div>\
        </div>\
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


var INLINE_FRAME_HTML = "\
<div>\
        <div class='frame-data-inner'></div>\
</div>\
";

