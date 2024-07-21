from django.utils.translation import gettext_lazy as _

ModuleName = "channels"
ModuleTitle = _("channels")
Name = "channels_demo"
Title = _("Channels")
Perms = False
Index = ""
Urls = (
    (
        "clock/",
        _("Clock channel example"),
        None,
        """png://actions/appointment-new.png""",
    ),
    ("ai/", _("AI chat"), None, """png://apps/help-browser.png"""),
)
UserParam = {}
