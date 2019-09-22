## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
     url(r'^action_ctrl', TemplateView.as_view(template_name='schadvcontrolsdemo/action_ctrl.html'), {}), 
     url(r'^plots', TemplateView.as_view(template_name='schadvcontrolsdemo/plots.html'), {}), 
    
    
]

gen = generic_table_start(urlpatterns, 'schadvcontrolsdemo', views)



