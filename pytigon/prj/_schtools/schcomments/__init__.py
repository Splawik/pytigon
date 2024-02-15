from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schcomments"
Title = _("Comments")
Perms = True
Index = ""
Urls = (
    (
        "table/Comment/-/form/list/",
        _("Comments"),
        "admin_comment",
        """fa://question.png""",
    ),
)
UserParam = {}
