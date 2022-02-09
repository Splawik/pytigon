from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Simple controls")
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
        "htmlcontrols",
        _("Html controls"),
        None,
        """client://apps/internet-web-browser.png""",
    ),
    (
        "extendedcontrols",
        _("Extended controls"),
        None,
        """client://categories/applications-other.png""",
    ),
    (
        "form/TestForm/",
        _("Form"),
        None,
        """client://categories/preferences-desktop.png""",
    ),
)
UserParam = {}
