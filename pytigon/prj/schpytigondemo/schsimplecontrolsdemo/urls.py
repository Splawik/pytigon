## -- coding: utf-8 --

from django.urls import path, re_path
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    re_path('sum/(?P<x>\d+)/(?P<y>\d+)/$', views.json_test, {}),
     path('standardcontrols', TemplateView.as_view(template_name='schsimplecontrolsdemo/standard_controls.html'), {"title": "Standard controls"}), 
     path('htmlcontrols', TemplateView.as_view(template_name='schsimplecontrolsdemo/html_controls.html'), {}), 
     path('extendedcontrols', TemplateView.as_view(template_name='schsimplecontrolsdemo/extended_controls.html'), {}), 
    
     path('markdeep', TemplateView.as_view(template_name='schsimplecontrolsdemo/markdeep.html'), {}), 
    
    
    
    path('form/TestForm/$', views.view_testform, {}),
]

gen = generic_table_start(urlpatterns, 'schsimplecontrolsdemo', views)



