from django.utils.translation import gettext_lazy as _

ModuleTitle = _("htmllib")
Title = _("Html lib")
Perms = False
Index = "None"
Urls = (
    (
        "tbl_grid?schtml=desktop",
        _("table_grid"),
        None,
        """client://mimetypes/x-office-spreadsheet.png""",
    ),
    (
        "table/demo_tbl/-/form/list?schtml=desktop",
        _("demo_tbl"),
        None,
        """client://actions/document-properties.png""",
    ),
)
UserParam = {}
