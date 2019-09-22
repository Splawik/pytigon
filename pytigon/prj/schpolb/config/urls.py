## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_tab_action('Employee', 'sync', views.sync),
    gen_tab_action('Employee', 'compare', views.compare),
    
    
    
    
    
    
    
    url('form/employee_import/$', views.view_employee_import, {}),
]

gen = generic_table_start(urlpatterns, 'config', views)


gen.standard('Employee', _('Employee'), _('Employees'))

