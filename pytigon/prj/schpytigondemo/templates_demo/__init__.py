from django.utils.translation import gettext_lazy as _

ModuleTitle = _("templates")
Title = _("Templates")
Perms = False
Index = "None"
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
)
UserParam = {}
