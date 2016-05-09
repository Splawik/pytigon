## -- coding: utf-8 --

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    
    
    
]

gen = generic_table_start(urlpatterns, 'log', views)


gen.standard('Log', _('Log'), _('Logi'))

