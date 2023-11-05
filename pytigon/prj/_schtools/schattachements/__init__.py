from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
Title = _("Attachements")
Perms = True
Index = "None"
Urls = (
    (
        "table/Attachement/-/form/list/?view_in=desktop",
        _("Attachements"),
        "schattachements.admin_attachement",
        """client://status/mail-attachment.png""",
    ),
)
UserParam = {}
