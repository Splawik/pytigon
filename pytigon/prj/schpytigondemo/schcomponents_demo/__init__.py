from django.utils.translation import gettext_lazy as _

ModuleName = "main tools"
ModuleTitle = _("main tools")
Name = "schcomponents_demo"
Title = _("Components")
Perms = False
Index = ""
Urls = (
    (
        "codeeditor?view_in=browser",
        _("Code editor"),
        None,
        """png://actions/format-justify-center.png""",
    ),
    ("d3?view_in=browser", _("D3"), None, """"""),
    (
        "spreadsheet?view_in=browser",
        _("Spreadsheet"),
        None,
        """png://apps/accessories-calculator.png""",
    ),
    (
        "pivottable?view_in=browser",
        _("Pivot table"),
        None,
        """png://mimetypes/x-office-spreadsheet.png""",
    ),
    (
        "leaflet?view_in=browser",
        _("Leaflet"),
        None,
        """png://apps/preferences-system-network-proxy.png""",
    ),
    (
        "video?view_in=browser",
        _("Video"),
        None,
        """png://mimetypes/video-x-generic.png""",
    ),
    (
        "wysiwyg?view_in=browser",
        _("Wysiwyg editor"),
        None,
        """png://mimetypes/x-office-document.png""",
    ),
    (
        "xterm?view_in=browser",
        _("Xterm"),
        None,
        """png://apps/utilities-terminal.png""",
    ),
    (
        "calendar?view_in=browser",
        _("Calendar"),
        None,
        """png://actions/appointment-new.png""",
    ),
    (
        "mask?view_in=browser",
        _("Mask edit"),
        None,
        """png://actions/format-text-underline.png""",
    ),
    (
        "webrtc?view_in=browser",
        _("WebRTC"),
        None,
        """png://status/network-transmit-receive.png""",
    ),
    (
        "time?view_in=browser",
        _("Time edit"),
        None,
        """png://actions/appointment-new.png""",
    ),
    (
        "scrollaction?view_in=browser",
        _("Scroll actions"),
        None,
        """png://actions/go-down.png""",
    ),
    (
        "plotly?view_in=browser",
        _("Plotly"),
        None,
        """png://mimetypes/x-office-drawing-template.png""",
    ),
    (
        "test?view_in=browser",
        _("Test"),
        None,
        """png://actions/document-properties.png""",
    ),
    ("svg?view_in=browser", _("Svg"), None, """png://actions/edit-find-replace.png"""),
    ("select2?view_in=browser", _("Select2"), None, """png://actions/edit-find.png"""),
    ("db?view_in=browser", _("Db"), None, """png://actions/address-book-new.png"""),
    (
        "form?view_in=browser",
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
    (
        "event-calendar",
        _("Event calendar"),
        None,
        """png://mimetypes/x-office-calendar.png""",
    ),
)
UserParam = {}
