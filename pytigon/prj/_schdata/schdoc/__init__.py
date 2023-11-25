from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
Title = _("Nested documents")
Perms = True
Index = "None"
Urls = (
    (
        "table/DocDef/-/form/list/?view_in=desktop",
        _("Document definition"),
        "schdoc.admin_docdef",
        """client://actions/document-properties.png""",
    ),
    (
        "table/Doc/main_docs/form/list/?view_in=desktop",
        _("Documents"),
        "schdoc.admin_doc",
        """client://actions/format-justify-fill.png""",
    ),
)
UserParam = {}
