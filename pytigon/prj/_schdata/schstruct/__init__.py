from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schstruct"
Title = _("Structures")
Perms = True
Index = ""
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
