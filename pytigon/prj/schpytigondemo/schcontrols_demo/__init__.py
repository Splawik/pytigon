from django.utils.translation import gettext_lazy as _

ModuleName = "main tools"
ModuleTitle = _("main tools")
Name = "schcontrols_demo"
Title = _("Controls")
Perms = False
Index = ""
Urls = (
    (
        "standardcontrols",
        _("Standard controls"),
        None,
        """client://mimetypes/x-office-document-template.png""",
    ),
    (
        "extendedcontrols?view_in=desktop",
        _("Extended controls"),
        None,
        """client://categories/applications-other.png""",
    ),
)
UserParam = {}
