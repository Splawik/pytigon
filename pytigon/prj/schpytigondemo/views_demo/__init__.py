from django.utils.translation import gettext_lazy as _

ModuleName = "views"
ModuleTitle = _("views")
Name = "views_demo"
Title = _("Views")
Perms = False
Index = ""
Urls = (
    (
        "template_example?view_in=desktop",
        _("template example"),
        None,
        """png://mimetypes/x-office-presentation-template.png""",
    ),
    (
        "odf_example?view_in=desktop",
        _("odf example"),
        None,
        """png://mimetypes/x-office-spreadsheet-template.png""",
    ),
    (
        "pdf_example?view_in=desktop",
        _("pdf example"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "json?view_in=desktop",
        _("json example"),
        None,
        """png://actions/format-justify-right.png""",
    ),
    (
        "xml_example?view_in=desktop",
        _("xml example"),
        None,
        """png://actions/contact-new.png""",
    ),
    (
        "xlsx_example?view_in=desktop",
        _("xlsx example"),
        None,
        """png://mimetypes/x-office-spreadsheet-template.png""",
    ),
    (
        "txt_example?view_in=desktop",
        _("txt example"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "hdoc_example",
        _("hdoc example"),
        None,
        """png://actions/format-justify-center.png""",
    ),
    ("plotly", _("plotly example"), None, """png://actions/edit-clear.png"""),
    (
        "plotly_export",
        _("plotlib export example"),
        None,
        """png://mimetypes/x-office-presentation-template.png""",
    ),
)
UserParam = {}
