from django.utils.translation import gettext_lazy as _

ModuleName = "templates"
ModuleTitle = _("templates")
Name = "templates_demo"
Title = _("Templates")
Perms = False
Index = ""
Urls = (
    (
        "example_template/",
        _("Example template"),
        None,
        """png://mimetypes/x-office-presentation.png""",
    ),
    (
        "excel/",
        _("Excel template"),
        None,
        """png://mimetypes/x-office-spreadsheet.png""",
    ),
    ("odf/", _("odf template"), None, """png://mimetypes/x-office-spreadsheet.png"""),
    ("min/", _("Minimal page"), None, """png://actions/media-playback-stop.png"""),
)
UserParam = {}
