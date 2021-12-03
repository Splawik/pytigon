from django.utils.translation import gettext_lazy as _

ModuleTitle = _("tasks_demo")
Title = _("Tasks")
Perms = False
Index = "None"
Urls = (
    (
        "action_ctrl?schtml=shtml",
        _("Action control"),
        None,
        """client://actions/media-playback-start.png""",
    ),
    ("plots?schtml=desktop", _("Plots"), None, """fa://rocket.png"""),
)
UserParam = {}
