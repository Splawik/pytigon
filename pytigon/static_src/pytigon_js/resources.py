_CANCEL = gettext("Cancel")
_CLOSE = gettext("Close")
_COPY_TO_CLIP = gettext("Copy to clipboard")

MODAL = """
    <div class="dialog-data"></div>
"""

MODAL_BASE = """
<div class="dialog-form modal" role="dialog" title="{title}">
    <div class="ajax-region modal-dialog" role="document" data-region='(page)(page-content)'>
        <div class="modal-content ajax-region" data-region="error">
            <div class="modal-header">
                <h5 class="modal-title" id="ModalLabel">{title}</h5>
                <button type="button" class="close btn-close" data-dismiss='modal' data-bs-dismiss='modal' aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="container-fluid ajax-frame ajax-link win-content form-and-details" data-region='page' href='{href}'>
                    <div class="form-without-details d-flex flex-grow-1 flex-column">
                        <div class="dialog-data ajax-frame" data-region="error"></div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                {{modal_footer}}
            </div>
        </div>
    </div>
</div>
""".replace(
    "Close", _CLOSE
)

MODAL_DELETE_BASE = """
<div class="dialog-form modal" role="dialog" title="{title}">
    <div class="ajax-region modal-dialog" role="document" data-region='(page)(page-content)'>
        <div class="modal-header">
            <h5 class="modal-title" id="ModalLabel">{title}</h5>
            <button type="button" class="close btn-close" data-dismiss='modal' data-bs-dismiss='modal' aria-label="Close"></button>
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
""".replace(
    "Close", _CLOSE
)

EDIT_FOOTER = """ 
<button type="button" class="btn btn-secondary ptig-btn-close" data-dismiss='modal' data-bs-dismiss='modal'>Cancel</button>
<button type="button" class="btn btn-primary" data-region="page-content" target="close_frame">OK</button>
""".replace(
    "Cancel", _CANCEL
)

INFO_FOOTER = """
<button type = "button" class ="btn btn-info copy_to_clipboard">Copy to clipboard</button>
<button type = "button" class ="btn btn-secondary ptig-btn-close" data-dismiss='modal' data-bs-dismiss='modal'>Close</button>
""".replace(
    "Copy to clipboard", _COPY_TO_CLIP
).replace(
    "Close", _CLOSE
)

DELETE_FOOTER = """
<button type="button" class="btn btn-secondary ptig-btn-close" data-dismiss='modal' data-bs-dismiss='modal'>Cancel</button>
<button type="button" class="btn btn-danger" data-region="page-content" target="close_frame">OK</button>
""".replace(
    "Cancel", _CANCEL
)

ERROR_FOOTER = """
<button type="button" class="btn btn-secondary ptig-btn-close" data-dismiss='modal' data-bs-dismiss='modal'>Close</button>
""".replace(
    "Close", _CLOSE
)

MODAL_EDIT = MODAL_BASE.replace("{{modal_footer}}", EDIT_FOOTER)
MODAL_INFO = MODAL_BASE.replace("{{modal_footer}}", INFO_FOOTER)
MODAL_DELETE = MODAL_BASE.replace("{{modal_footer}}", DELETE_FOOTER)
MODAL_ERROR = MODAL_BASE.replace("{{modal_footer}}", ERROR_FOOTER)

INLINE = """
    <div class="dialog-data"></div>
"""

INLINE_BASE = """
<div class='inline-dialog-frame'>
    <div class='dark_background'></div>
    <div class='ajax-region modal-dialog modal-dialog-inline' role='document' data-region='(page)(page-content)'>
        <div class="modal-content ajax-region inline-content" data-region="error">
            <div class='modal-content2 d-flex flex-column' style='min-height: 50vh;'>
                <div class='modal-header'>
                    <h4 class='modal-title'>{title}</h4>
                    <div class='dialog-buttons>
                        <button type='button' class='btn btn-light btn-transparent minimize' onclick='inline_minimize(this)' style='display:none;'> 
                            <span class='fa fa-window-minimize'></span> 
                        </button> 
                        <button type='button' class='btn btn-light btn-transparent maximize' onclick='inline_maximize(this);return false;'> 
                            <span class='fa fa-window-maximize'></span> 
                        </button> 
                        <button type='button' class='close btn btn-light btn-transparent shadow-none ptig-btn-close' aria-label='Close'>
                            <span class='fa fa-times'></span>
                        </button>
                    </div>
                </div>
                <div class='modal-body ajax-frame ajax-link d-flex flex-column win-content table-and-details' data-region='page' href='{href}'>
                    <div class="table-without-details d-flex flex-grow-1 flex-column">
                        <div class='dialog-data ajax-frame d-flex flex-column flex-grow-1' data-region='error'></div>
                    </div>
                </div>
                <div class='modal-footer'>
                    {{modal_footer}}
                </div>
            </div>
        </div>
    </div>
</div>
""".replace(
    "Close", _CLOSE
)

INLINE_DELETE_BASE = """
<div style='position:relative;z-index:1001;'>
    <div class='dark_background'></div>
    <div class='ajax-region modal-dialog modal-dialog-inline' role='document' data-region='(page)(page-content)'>
        <div class='modal-content'>
            <div class='modal-header'>
                <h4 class='modal-title'>{title}</h4>
                <div>
                    <button type='button' class='btn btn-light btn-transparent minimize' onclick='inline_minimize(this)' style='display:none;'> 
                        <span class='fa fa-window-minimize'></span> 
                    </button> 
                    <button type='button' class='btn btn-light btn-transparent maximize' onclick='inline_maximize(this);return false;'> 
                        <span class='fa fa-window-maximize'></span> 
                    </button> 
                    <button type='button' class='close btn-close shadow-none ptig-btn-close' aria-label='Close'></button>
                </div>
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
""".replace(
    "Close", _CLOSE
)

INLINE_EDIT = (
    INLINE_BASE.replace("{{modal_footer}}", EDIT_FOOTER)
    .replace("data-dismiss='modal'", "")
    .replace("data-bs-dismiss='modal'", "")
)
INLINE_INFO = (
    INLINE_BASE.replace("{{modal_footer}}", INFO_FOOTER)
    .replace("data-dismiss='modal'", "")
    .replace("data-bs-dismiss='modal'", "")
)
INLINE_DELETE = (
    INLINE_BASE.replace("{{modal_footer}}", DELETE_FOOTER)
    .replace("data-dismiss='modal'", "")
    .replace("data-bs-dismiss='modal'", "")
)
INLINE_ERROR = (
    INLINE_BASE.replace("{{modal_footer}}", ERROR_FOOTER)
    .replace("data-dismiss='modal'", "")
    .replace("data-bs-dismiss='modal'", "")
)
