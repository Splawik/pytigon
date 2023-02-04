from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("select2query/", views.select2query, {}, name="forms_demo_select2query"),
    path("list2", views.list2, {}, name="forms_demo_list2"),
    path("list3", views.list3, {}, name="forms_demo_list3"),
    path("form/form_test/", views.view_form_test, {}),
    path("form/form_test2/", views.view_form_test2, {}),
    path("form/form_test3/", views.view_form_test3, {}),
    path("form/form_test4/", views.view_form_test4, {}),
]

gen = generic_table_start(urlpatterns, "forms_demo", views)


gen.standard("Select2Example", _("Select2 example"), _("Select2 examples"))
