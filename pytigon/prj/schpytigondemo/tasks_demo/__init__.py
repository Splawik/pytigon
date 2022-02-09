from django.utils.translation import gettext_lazy as _

ModuleTitle = _("tasks")
Title = _("Tasks")
Perms = False
Index = "None"
Urls = (
    ("test_task/", _("Task1"), None, """png://actions/media-seek-forward.png"""),
    ("test_task2/", _("Task2"), None, """png://actions/media-skip-forward.png"""),
)
UserParam = {}
