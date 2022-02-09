from django.utils.translation import gettext_lazy as _

ModuleTitle = _("forms")
Title = _("Forms")
Perms = False
Index = "None"
Urls = (
    (
        "form/form_test/?schtml=desktop",
        _("Form example 1"),
        None,
        """png://actions/window-new.png""",
    ),
    (
        "form/form_test2/?schtml=desktop",
        _("Form example 2"),
        None,
        """png://actions/edit-select-all.png""",
    ),
    (
        "form/form_test3/?schtml=desktop",
        _("Form example 3"),
        None,
        """png://mimetypes/x-office-address-book.png""",
    ),
    (
        "table/Select2Example/-/form/list/?schtml=desktop",
        _("Select2 example tab"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
)
UserParam = {}
