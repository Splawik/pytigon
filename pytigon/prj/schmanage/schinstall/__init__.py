from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schinstall"
Title = _("Pytigon setup")
Perms = True
Index = ""
Urls = (
    (
        "form/upload_ptig/?view_in=desktop",
        _("Install pytigon application (*.ptig)"),
        None,
        """fa://rocket.png""",
    ),
)
UserParam = {}
