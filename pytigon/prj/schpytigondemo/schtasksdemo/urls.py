## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('gen_task1', views.gen_task1, {}),
    url('gen_task2', views.gen_task2, {}),
    url('gen_task3', views.gen_task3, {}),
    url('from_script/$', views.from_script, {}),
    
    
]

gen = generic_table_start(urlpatterns, 'schtasksdemo', views)



