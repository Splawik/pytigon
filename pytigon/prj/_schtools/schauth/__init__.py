from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Authorization")
Title = _("Authorization")
Perms = True
Index = "None"
Urls = (
    (
        "table/UrlWithAuth/-/form/list/?schtml=desktop",
        _("Urls with auth"),
        None,
        """png://apps/system-users.png""",
    ),
)
UserParam = {}
