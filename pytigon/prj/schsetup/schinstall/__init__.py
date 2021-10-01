from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Pytigon setup")
Perms = True
Index = "None"
Urls = (
    (
        "form/upload_ptig/?schtml=desktop",
        _("Install pytigon application (*.ptig)"),
        None,
        """fa://rocket.png""",
    ),
)
UserParam = {}
