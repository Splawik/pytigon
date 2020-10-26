## -- coding: utf-8 --

from django.urls import path, re_path, include
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('form/', views.form, {}),
     path('codeeditor', TemplateView.as_view(template_name='schcomponents/code_editor.html'), {}), 
     path('d3', TemplateView.as_view(template_name='schcomponents/d3.html'), {}), 
     path('spreadsheet', TemplateView.as_view(template_name='schcomponents/spreadsheet.html'), {}), 
     path('pivottable', TemplateView.as_view(template_name='schcomponents/pivottable.html'), {}), 
     path('plotly', TemplateView.as_view(template_name='schcomponents/plotly.html'), {}), 
     path('leaflet', TemplateView.as_view(template_name='schcomponents/leaflet.html'), {}), 
     path('video', TemplateView.as_view(template_name='schcomponents/video.html'), {}), 
     path('wysiwyg', TemplateView.as_view(template_name='schcomponents/wysiwygeditor.html'), {}), 
     path('xterm', TemplateView.as_view(template_name='schcomponents/xterm.html'), {}), 
     path('calendar', TemplateView.as_view(template_name='schcomponents/calendar.html'), {}), 
     path('mask', TemplateView.as_view(template_name='schcomponents/mask.html'), {}), 
     path('markdeep', TemplateView.as_view(template_name='schcomponents/markdeep.html'), {}), 
     path('webrtc', TemplateView.as_view(template_name='schcomponents/webrtc.html'), {}), 
     path('time', TemplateView.as_view(template_name='schcomponents/time.html'), {}), 
     path('scrollaction', TemplateView.as_view(template_name='schcomponents/scrollaction.html'), {}), 
     path('test', TemplateView.as_view(template_name='schcomponents/test.html'), {}), 
     path('svg', TemplateView.as_view(template_name='schcomponents/svg.html'), {}), 
     path('select2', TemplateView.as_view(template_name='schcomponents/select2.html'), {}), 
     path('db', TemplateView.as_view(template_name='schcomponents/db.html'), {}), 
     path('form', TemplateView.as_view(template_name='schcomponents/form.html'), {}), 
    
    
]

gen = generic_table_start(urlpatterns, 'schcomponents', views)



