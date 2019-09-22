## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_tab_action('GrupaPraw', 'grupy_import', views.grupy_import),
    gen_tab_action('Dzial', 'dzial_import', views.dzial_import),
    gen_tab_action('Lokalizacja', 'lok_import', views.lok_import),
    gen_tab_action('Operator', 'gen_karty', views.gen_karty),
    gen_tab_action('Operator', 'oper_import', views.oper_import),
    gen_tab_action('Operator', 'oper_imp_dzial', views.oper_imp_dzial),
    gen_tab_action('Operator', 'oper_imp_przel', views.oper_imp_przel),
    gen_row_action('DokPrzydzielenia', 'zatwierdz', views.zatwierdz),
    gen_tab_action('Operator', 'oper_imp_lokal', views.oper_imp_lokal),
    gen_row_action('DokOdebrania', 'zatwierdz2', views.zatwierdz2),
    gen_tab_action('GrupaPraw', 'fun_praw', views.fun_praw),
    gen_tab_action('GrupaPraw', 'grupa_praw', views.grupa_praw),
    gen_tab_action('Operator', 'spr_praw', views.spr_praw),
    gen_tab_action('Operator', 'regenerate_user_groups', views.regenerate_user_groups),
    gen_tab_action('Operator', 'gen_wnioski_wg_softlaba', views.gen_wnioski_wg_softlaba),
    gen_row_action('Operator', 'gen', views.gen),
    gen_row_action('Operator', 'gen', views.gen),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    url('form/GrupyFunkcjeForm/$', views.view_grupyfunkcjeform, {}),
    url('form/FunkcjePrawForm/$', views.view_funkcjeprawform, {}),
    url('form/KartyPrawForm/$', views.view_kartyprawform, {}),
    url('form/AkceptacjeDP/$', views.view_akceptacjedp, {}),
    url('form/PrawaWyklucz/$', views.view_prawawyklucz, {}),
    url('form/GrupyZOperatorami/$', views.view_grupyzoperatorami, {}),
    url('form/LogZmian/$', views.view_logzmian, {}),
]

gen = generic_table_start(urlpatterns, 'prawa', views)


gen.standard('LogZmian', _('Log zmian uprawnien'), _('Log zmian uprawnien'))
gen.standard('Lokalizacja', _('Lokalizacja'), _('Lokalizacje'))
gen.standard('Dzial', _('Dzial'), _('Dzialy'))
gen.standard('GrupaPraw', _('Grupa praw'), _('Grupy praw'))
gen.standard('Operator', _('Operator'), _('Operatorzy'))
gen.standard('DokPrzydzielenia', _('Dokument przydzielenia praw'), _('Dokumenty przydzielenia praw'))
gen.standard('DokOdebrania', _('Dokument odebrania praw'), _('Dokumenty odebrania praw'))

