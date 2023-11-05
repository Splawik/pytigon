from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
Title = _("Structures")
Perms = True
Index = "None"
Urls = (
    (
        "table/CommonGroupDef/-/form/list/?view_in=desktop",
        _("Common group definitons"),
        "schreports.admin_commongroupdef",
        """png://apps/system-file-manager.png""",
    ),
    (
        "table/CommonGroup/0/form/tree/?view_in=desktop",
        _("Common groups"),
        "schreports.admin_commongroup",
        """png://apps/system-file-manager.png""",
    ),
)
UserParam = {}
