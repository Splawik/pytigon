from django.utils.translation import gettext_lazy as _

ModuleName = "tasks"
ModuleTitle = _("tasks")
Name = "tasks_demo"
Title = _("Tasks")
Perms = False
Index = ""
Urls = (
    ("test_task/", _("Task1"), None, """png://actions/media-seek-forward.png"""),
    ("test_task2/", _("Task2"), None, """png://actions/media-skip-forward.png"""),
)
UserParam = {}
