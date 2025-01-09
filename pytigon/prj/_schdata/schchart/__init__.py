from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schchart"
Title = _("Charts")
Perms = True
Index = ""
Urls = (
    (
        "table/Plot/-/form/list/?view_in=desktop",
        _("Plots"),
        None,
        """fa://pencil-square.png""",
    ),
)
UserParam = {}
