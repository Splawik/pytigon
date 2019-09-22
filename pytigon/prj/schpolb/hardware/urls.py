## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('raport_domena_softlab', views.raport_domena_softlab),
    
    
]

gen = generic_table_start(urlpatterns, 'hardware', views)



