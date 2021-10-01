from django.utils.translation import gettext_lazy as _

ModuleTitle = _("attachements")
Title = _("Attachements")
Perms = True
Index = "None"
Urls = (
    (
        "table/Attachements/-/form/list/?schtml=desktop",
        _("Attachements"),
        "wiki.change_attachements",
        """client://status/mail-attachment.png""",
    ),
)
UserParam = {}
