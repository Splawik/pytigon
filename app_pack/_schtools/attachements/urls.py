## -- coding: utf-8 --

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = patterns('',
    gen_row_action('Attachements', 'download', views.download),
    
    
    
)

gen = generic_table_start(urlpatterns, 'attachements', views)


gen.standard('Attachements', _('Attachements'), _('Attachements'))
