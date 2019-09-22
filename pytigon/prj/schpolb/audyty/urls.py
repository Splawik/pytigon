## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_row_action('Audyt', 'akceptacja1', views.akceptacja1),
    gen_row_action('Audyt', 'akceptacja2', views.akceptacja2),
    gen_row_action('Audyt', 'pdf', views.pdf),
    gen_row_action('TestForUser', 'change_accept', views.change_accept),
    
    
    
    
    
    
    
]

gen = generic_table_start(urlpatterns, 'audyty', views)


gen.standard('TypAudytu', _('Typ audytu'), _('Typy audytow'))
gen.standard('Audyt', _('Audyt'), _('Audyty'))
gen.standard('Change', _('Change'), _('Changes'))
gen.standard('Test', _('Test'), _('Tests'))
gen.standard('TestForUser', _('Test for user'), _('Tests for user'))

gen.for_field('prawa.Operator', 'sporzadzajacy', _('Typ audytu'), _('Typy audytow'))
gen.for_field('prawa.Operator', 'zatwierdzajacy', _('Typ audytu'), _('Typy audytow'))
gen.for_field('TypAudytu', 'audyt_set', _('Audyt'), _('Audyty'))
gen.for_field('Change', 'test_set', _('Test'), _('Tests'))
gen.for_field('Test', 'testforuser_set', _('Test for user'), _('Tests for user'))
