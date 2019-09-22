## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    
    
    
    
    
    url('form/ProdukcjaForm/$', views.view_produkcjaform, {}),
    url('form/ConfigUploadForm/$', views.view_configuploadform, {}),
]

gen = generic_table_start(urlpatterns, 'produkcja', views)


gen.standard('Config', _('Config'), _('Config'))
gen.standard('TruckPhotos', _('Fotografia ciezarowki'), _('Fotografie ciezarowek'))
gen.standard('TimeLoadTruck', _('Czas zaladunku ciezarowki'), _('Czasy zaladunku ciezarowek'))
gen.standard('TruckConfig', _('Konfiguracja monitorowania ciezarowek'), _('Konfiguracja monitorowania ciezarowek'))

