from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schdescriptions"
Title = _("International descriptions")
Perms = True
Index = ""
Urls = (
    (
        "table/Description/-/form/list/",
        _("Descriptions"),
        "admin_description",
        """png://actions/mail-reply-all.png""",
    ),
)
UserParam = {}
