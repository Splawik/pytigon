from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
Title = _("Comments")
Perms = True
Index = "None"
Urls = (
    (
        "table/Comment/-/form/list/",
        _("Comments"),
        "admin_comment",
        """fa://question.png""",
    ),
)
UserParam = {}
