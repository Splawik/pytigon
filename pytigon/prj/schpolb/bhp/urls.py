## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('duplicate_rep/(?P<parm>\d+)/$', views.duplicate_rep, {}),
    
    
    
    
    
    
    
    
    
    
]

gen = generic_table_start(urlpatterns, 'bhp', views)


gen.standard('Proces', _('Proces'), _('Procesy'))
gen.standard('Etap', _('Etap'), _('Etapy'))
gen.standard('EventType', _('Event type'), _('Event types'))
gen.standard('Event', _('Event'), _('Events'))
gen.standard('EventUser', _('Event user'), _('Event users'))

gen.for_field('EventType', 'event_set', _('Event'), _('Events'))
gen.for_field('Event', 'eventuser_set', _('Event user'), _('Event users'))
gen.for_field('config.Employee', 'eventuser_set', _('Event user'), _('Event users'))
