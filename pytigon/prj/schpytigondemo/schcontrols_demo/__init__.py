from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Controls")
Perms = False
Index = "None"
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
