from django.utils.translation import gettext_lazy as _

ModuleName = "forms"
ModuleTitle = _("forms")
Name = "forms_demo"
Title = _("Forms")
Perms = False
Index = ""
Urls = (
    (
        "form/form_test/?view_in=desktop",
        _("Form example 1"),
        None,
        """png://actions/window-new.png""",
    ),
    (
        "form/form_test2/?view_in=desktop",
        _("Form example 2"),
        None,
        """png://actions/edit-select-all.png""",
    ),
    (
        "form/form_test3/?view_in=desktop",
        _("Form example 3"),
        None,
        """png://mimetypes/x-office-address-book.png""",
    ),
    (
        "table/Select2Example/-/form/list/?view_in=desktop",
        _("Select2 example tab"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "form/form_test4/",
        _("Form combo select"),
        None,
        """png://actions/media-seek-forward.png""",
    ),
)
UserParam = {}
