## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('sum/(?P<x>\d+)/(?P<y>\d+)/$', views.json_test, {}),
     url(r'^standardcontrols', TemplateView.as_view(template_name='schsimplecontrolsdemo/standard_controls.html'), {"title": "Standard controls"}), 
     url(r'^htmlcontrols', TemplateView.as_view(template_name='schsimplecontrolsdemo/html_controls.html'), {}), 
     url(r'^extendedcontrols', TemplateView.as_view(template_name='schsimplecontrolsdemo/extended_controls.html'), {}), 
    
     url(r'^markdeep', TemplateView.as_view(template_name='schsimplecontrolsdemo/markdeep.html'), {}), 
    
    
    
    url('form/TestForm/$', views.view_testform, {}),
]

gen = generic_table_start(urlpatterns, 'schsimplecontrolsdemo', views)



