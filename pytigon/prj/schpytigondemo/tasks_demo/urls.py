from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("test_task/", views.test_task, {}, name="tasks_demo_test_task"),
    path("test_task2/", views.test_task2, {}, name="tasks_demo_test_task2"),
]

gen = generic_table_start(urlpatterns, "tasks_demo", views)
