from django.utils.translation import gettext_lazy as _

ModuleTitle = _("components")
Title = _("Components")
Perms = False
Index = "None"
Urls = (
    (
        "codeeditor?schtml=browser",
        _("Code editor"),
        None,
        """png://actions/format-justify-center.png""",
    ),
    ("d3?schtml=browser", _("D3"), None, """"""),
    (
        "spreadsheet?schtml=browser",
        _("Spreadsheet"),
        None,
        """png://apps/accessories-calculator.png""",
    ),
    (
        "pivottable?schtml=browser",
        _("Pivot table"),
        None,
        """png://mimetypes/x-office-spreadsheet.png""",
    ),
    (
        "leaflet?schtml=browser",
        _("Leaflet"),
        None,
        """png://apps/preferences-system-network-proxy.png""",
    ),
    (
        "video?schtml=browser",
        _("Video"),
        None,
        """png://mimetypes/video-x-generic.png""",
    ),
    (
        "wysiwyg?schtml=browser",
        _("Wysiwyg editor"),
        None,
        """png://mimetypes/x-office-document.png""",
    ),
    ("xterm?schtml=browser", _("Xterm"), None, """png://apps/utilities-terminal.png"""),
    (
        "calendar?schtml=browser",
        _("Calendar"),
        None,
        """png://actions/appointment-new.png""",
    ),
    (
        "mask?schtml=browser",
        _("Mask edit"),
        None,
        """png://actions/format-text-underline.png""",
    ),
    (
        "webrtc?schtml=browser",
        _("WebRTC"),
        None,
        """png://status/network-transmit-receive.png""",
    ),
    (
        "time?schtml=browser",
        _("Time edit"),
        None,
        """png://actions/appointment-new.png""",
    ),
    (
        "scrollaction?schtml=browser",
        _("Scroll actions"),
        None,
        """png://actions/go-down.png""",
    ),
    (
        "plotly?schtml=browser",
        _("Plotly"),
        None,
        """png://mimetypes/x-office-drawing-template.png""",
    ),
    (
        "test?schtml=browser",
        _("Test"),
        None,
        """png://actions/document-properties.png""",
    ),
    ("svg?schtml=browser", _("Svg"), None, """png://actions/edit-find-replace.png"""),
    ("select2?schtml=browser", _("Select2"), None, """png://actions/edit-find.png"""),
    ("db?schtml=browser", _("Db"), None, """png://actions/address-book-new.png"""),
    (
        "form?schtml=browser",
        _("Form"),
        None,
        """png://categories/preferences-desktop.png""",
    ),
    (
        "../static/schcomponents_demo/views/sample.fview",
        _("Frontent view and template"),
        None,
        """png://actions/edit-clear.png""",
    ),
    (
        "../static/schcomponents_demo/views/login_form.fview",
        _("Graphql login"),
        None,
        """png://apps/preferences-desktop-theme.png""",
    ),
    (
        "../static/schcomponents_demo/views/users.fview",
        _("users"),
        None,
        """png://apps/system-users.png""",
    ),
)
UserParam = {}
