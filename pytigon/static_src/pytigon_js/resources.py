MODAL = """
    <div class="dialog-data"></div>
"""

MODAL_BASE = """
<div class="dialog-form modal" role="dialog" title="{title}">
    <div class="modal-dialog" role="document">
        <div class="modal-content ajax-region" data-region="error">
            <div class="modal-header">
                <h5 class="modal-title" id="ModalLabel">{title}</h5>
                <button type="button" class="close" data-dismiss='modal' aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <div class="container-fluid ajax-region ajax-frame" data-region='page' href='{href}'>
                    <div class="dialog-data ajax-frame" data-region="error"></div>
                </div>
            </div>
            <div class="modal-footer">
                {{modal_footer}}
            </div>
        </div>
    </div>
</div>
"""

MODAL_DELETE_BASE = """
<div class="dialog-form modal" role="dialog" title="{title}">
    <div class="modal-dialog" role="document">
        <div class="modal-header">
            <h5 class="modal-title" id="ModalLabel">{title}</h5>
            <button type="button" class="close" data-dismiss='modal' aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <div class="container-fluid">
                <div class="dialog-data ajax-frame" data-region="error"></div>
            </div>
        </div>
        <div class="modal-footer">
            {{modal_footer}}
        </div>
    </div>
</div>
"""

EDIT_FOOTER = """ 
<button type="button" class="btn btn-secondary btn-close" data-dismiss='modal'>Cancel</button>
<button type="button" class="btn btn-primary" target="refresh_frame">OK</button>
"""

INFO_FOOTER = """
<button type = "button" class ="btn btn-secondary btn-close" data-dismiss='modal'>Close</button>
"""

DELETE_FOOTER = """
<button type="button" class="btn btn-secondary btn-close" data-dismiss='modal'>Cancel</button>
<button type="button" class="btn btn-danger" target="refresh_frame">OK</button>
"""

ERROR_FOOTER = """
<button type="button" class="btn btn-secondary btn-close" data-dismiss='modal'>Close</button>
"""

MODAL_EDIT = MODAL_BASE.replace("{{modal_footer}}", EDIT_FOOTER)
MODAL_INFO = MODAL_BASE.replace("{{modal_footer}}", INFO_FOOTER)
MODAL_DELETE = MODAL_BASE.replace("{{modal_footer}}", DELETE_FOOTER)
MODAL_ERROR = MODAL_BASE.replace("{{modal_footer}}", ERROR_FOOTER)

INLINE = """
    <div class="dialog-data"></div>
"""

INLINE_BASE = """
<div style='position:relative'>
    <div class='dark_background'></div>
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>
        <div class="modal-content ajax-region" data-region="error">
            <div class='modal-content'>
                <div class='modal-header'>
                    <h4 class='modal-title'>{title}</h4>
                    <button type='button' class='btn btn-outline-secondary minimize' onclick='popup_minimize(this)' style='diplay:none;'> 
                        <span class='fa fa-window-minimize'></span> 
                    </button> 
                    <button type='button' class='btn btn-outline-secondary maximize' onclick='popup_maximize(this);return false;'> 
                        <span class='fa fa-window-maximize'></span> 
                    </button> 
                    <button type='button' class='close btn-raised btn-close' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
                </div>
                <div class='modal-body ajax-region ajax-frame' data-region='page' href='{href}'>
                    <div class='dialog-data ajax-frame' data-region='error'></div>
                </div>
                <div class='modal-footer'>
                    {{modal_footer}}
                </div>
            </div>
        </div>
    </div>
</div>
"""

INLINE_DELETE_BASE = """
<div style='position:relative'>
    <div class='dark_background'></div>
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>
        <div class='modal-content'>
            <div class='modal-header'>
                <h4 class='modal-title'>{title}</h4>
                <button type='button' class='btn btn-outline-secondary minimize' onclick='popup_minimize(this)' style='diplay:none;'> 
                    <span class='fa fa-window-minimize'></span> 
                </button> 
                <button type='button' class='btn btn-outline-secondary maximize' onclick='popup_maximize(this);return false;'> 
                    <span class='fa fa-window-maximize'></span> 
                </button> 
                <button type='button' class='close btn-raised btn-close' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
            </div>
            <div class='modal-body'>
                <div class='dialog-data ajax-frame' data-region='error'></div>
            </div>
            <div class='modal-footer'>
                {{modal_footer}}
            </div>
        </div>
    </div>
</div>
"""

INLINE_EDIT = INLINE_BASE.replace("{{modal_footer}}", EDIT_FOOTER).replace("data-dismiss='modal'", "")
INLINE_INFO = INLINE_BASE.replace("{{modal_footer}}", INFO_FOOTER).replace("data-dismiss='modal'", "")
INLINE_DELETE = INLINE_BASE.replace("{{modal_footer}}", DELETE_FOOTER).replace("data-dismiss='modal'", "")
INLINE_ERROR = INLINE_BASE.replace("{{modal_footer}}", ERROR_FOOTER).replace("data-dismiss='modal'", "")
