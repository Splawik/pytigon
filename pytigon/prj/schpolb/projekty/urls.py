## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_row_action('ProjektInw', 'projekt_status', views.projekt_status),
    gen_row_action('EtapProjektuInw', 'etap_status', views.etap_status),
    gen_row_action('ProjektNawierzchni', 'projekt_naw_status', views.projekt_naw_status),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    url('form/Raporty/$', views.view_raporty, {}),
]

gen = generic_table_start(urlpatterns, 'projekty', views)


gen.standard('Asortyment', _('Asortyment'), _('Asortyment'))
gen.standard('BiuroProjekt', _('Biuro projektowe'), _('Biura projektowe'))
gen.standard('ProjektInw', _('Projekt inwestycyjny'), _('Projekty inwestycyjne'))
gen.standard('EtapProjektuInw', _('Etap '), _('Etapy projektu'))
gen.standard('Hurtownia', _('Hurtownia'), _('Hurtownie'))
gen.standard('Akcja', _('Akcja'), _('Akcje'))
gen.standard('ProjektNawierzchni', _('Projekt nawierzchni'), _('Projekty nawierzchni'))
gen.standard('Zdarzenie', _('Zdarzenie'), _('Zdarzenia'))

gen.for_field('User', 'b_projekt', _('Biuro projektowe'), _('Biura projektowe'))
gen.for_field('User', 'gl_projektant', _('Projekt inwestycyjny'), _('Projekty inwestycyjne'))
gen.for_field('User', 'projektant', _('Projekt inwestycyjny'), _('Projekty inwestycyjne'))
gen.for_field('User', 'szef', _('Projekt inwestycyjny'), _('Projekty inwestycyjne'))
gen.for_field('BiuroProjekt', 'projektinw_set', _('Projekt inwestycyjny'), _('Projekty inwestycyjne'))
gen.for_field('ProjektInw', 'etapprojektuinw_set', _('Etap '), _('Etapy projektu'))
gen.for_field('User', 'etapprojektuinw_set', _('Etap '), _('Etapy projektu'))
gen.for_field('EtapProjektuInw', 'akcja_set', _('Akcja'), _('Akcje'))
gen.for_field('Hurtownia', 'projektnawierzchni_set', _('Projekt nawierzchni'), _('Projekty nawierzchni'))
