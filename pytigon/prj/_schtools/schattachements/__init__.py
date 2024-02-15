from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schattachements"
Title = _("Attachements")
Perms = True
Index = ""
Urls = (
    (
        "table/Attachement/-/form/list/?view_in=desktop",
        _("Attachements"),
        "schattachements.admin_attachement",
        """client://status/mail-attachment.png""",
    ),
)
UserParam = {}
