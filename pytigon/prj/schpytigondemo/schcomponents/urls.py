## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
     url(r'^codeeditor', TemplateView.as_view(template_name='schcomponents/code_editor.html'), {}), 
     url(r'^d3', TemplateView.as_view(template_name='schcomponents/d3.html'), {}), 
     url(r'^spreadsheet', TemplateView.as_view(template_name='schcomponents/spreadsheet.html'), {}), 
     url(r'^pivottable', TemplateView.as_view(template_name='schcomponents/pivottable.html'), {}), 
     url(r'^plotly', TemplateView.as_view(template_name='schcomponents/plotly.html'), {}), 
     url(r'^leaflet', TemplateView.as_view(template_name='schcomponents/leaflet.html'), {}), 
     url(r'^video', TemplateView.as_view(template_name='schcomponents/video.html'), {}), 
     url(r'^wysiwyg', TemplateView.as_view(template_name='schcomponents/wysiwygeditor.html'), {}), 
     url(r'^xterm', TemplateView.as_view(template_name='schcomponents/xterm.html'), {}), 
     url(r'^calendar', TemplateView.as_view(template_name='schcomponents/calendar.html'), {}), 
     url(r'^mask', TemplateView.as_view(template_name='schcomponents/mask.html'), {}), 
     url(r'^money', TemplateView.as_view(template_name='schcomponents/money.html'), {}), 
     url(r'^markdeep', TemplateView.as_view(template_name='schcomponents/markdeep.html'), {}), 
     url(r'^webrtc', TemplateView.as_view(template_name='schcomponents/webrtc.html'), {}), 
     url(r'^time', TemplateView.as_view(template_name='schcomponents/time.html'), {}), 
     url(r'^scrollaction', TemplateView.as_view(template_name='schcomponents/scrollaction.html'), {}), 
    
    
]

gen = generic_table_start(urlpatterns, 'schcomponents', views)



