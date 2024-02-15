from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schdoc"
Title = _("Nested documents")
Perms = True
Index = ""
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
