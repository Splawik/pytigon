## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_tab_action('UserAD', 'synchr_ad', views.synchr_ad),
    gen_tab_action('UserSoftlab', 'synchr_softlab', views.synchr_softlab),
    gen_tab_action('NowyKomputer', 'synchr_komp', views.synchr_komp),
    
    
    
    
    
    
    
    
    
    
    
    url('form/RaportForm/$', views.view_raportform, {}),
    url('form/ImportPracForm/$', views.view_importpracform, {}),
]

gen = generic_table_start(urlpatterns, 'spisy', views)


gen.standard('UserAD', _('AD user'), _('AD users'))
gen.standard('UserSoftlab', _('Softlab user'), _('Softab users'))
gen.standard('TypKomputera', _('Computer type'), _('Computer types'))
gen.standard('NowyKomputer', _('New computer'), _('New computers'))
gen.standard('StarySprzet', _('Old equipment'), _('Old equipments'))
gen.standard('Lokalizacja', _('Location'), _('Locations'))
gen.standard('Switch', _('Switch'), _('Switches'))
gen.standard('WAN', _('WAN'), _('WAN'))
gen.standard('WiFi', _('WiFi'), _('WiFi'))
gen.standard('CentralaTel', _('Telephone exchange'), _('Telephone exchanges'))
gen.standard('NowaDrukarka', _('New printer'), _('New printers'))
gen.standard('UserPolbruk', _('UserPolbruk'), _('UserPolbruk'))

gen.for_field('TypKomputera', 'nowykomputer_set', _('New computer'), _('New computers'))
gen.for_field('UserAD', 'nowykomputer_set', _('New computer'), _('New computers'))
gen.for_field('UserAD', 'operator_staregosprzetu', _('Old equipment'), _('Old equipments'))
