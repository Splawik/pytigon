from django.utils.translation import gettext_lazy as _

ModuleTitle = _("tables")
Title = _("Advanced tables")
Perms = False
Index = "None"
Urls = (
    (
        "table/Album/-/form/list/?view_in=desktop",
        _("All albums"),
        None,
        """png://mimetypes/audio-x-generic.png""",
    ),
    (
        "table/Album/r/form__jazz/list/?view_in=desktop",
        _("Rock albums"),
        None,
        """png://emotes/face-smile.png""",
    ),
    (
        "table/AlbumProxy/-/form/list/?view_in=desktop",
        _("All albums - datatable"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
)
UserParam = {}
