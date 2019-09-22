## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_tab_action('Nag', 'rebuild', views.rebuild),
    url('kalkulator_tables/(?P<tab>\d+)/$', views.kalkulator_tables, {}),
    url('kalkulator_zmieniony/$', views.kalkulator_zmieniony, {}),
    url('kiedy_kalk_zmieniony/$', views.kiedy_kalk_zmieniony, {}),
    gen_tab_action('CastoramaStanMag', 'load_castorama_data', views.load_castorama_data),
    
    
    
    
    
     url(r'^kalkulator1', TemplateView.as_view(template_name='sprzedaz/kalkulator_cenowy.html'), {"title": "Kalkulator cenowy"}), 
     url(r'^kalkulator2', TemplateView.as_view(template_name='sprzedaz/kalkulator_mm.html'), {}), 
     url(r'^kalkulator3', TemplateView.as_view(template_name='sprzedaz/kalkulator_kontrakt.html'), {}), 
     url(r'^kalkulator_sync', TemplateView.as_view(template_name='sprzedaz/kalkulator_synchronizacja.html'), {}), 
    
    
    
    
    
    
    
    url('form/LoadKalkulatorData/$', views.view_loadkalkulatordata, {}),
]

gen = generic_table_start(urlpatterns, 'sprzedaz', views)


gen.standard('CastoramaKli', _('Oddzial Castoramy'), _('Oddzialy Castoramy'))
gen.standard('CastoramaKar', _('Kartoteka Castoramy'), _('Kartoteki Castoramy'))
gen.standard('CastoramaLog', _('Castorama - log'), _('Castorama - log'))
gen.standard('Nag', _('Naglowek'), _('Naglowki'))
gen.standard('Lin', _('Linijki'), _('Linijki'))
gen.standard('CastoramaRegion', _('Region Castoramy'), _('Regiony Castoramy'))
gen.standard('CastoramaStanMag', _('Stan mag. Castoramy'), _('Stany mag. Castoramy'))

gen.for_field('Nag', 'lin_set', _('Linijki'), _('Linijki'))
