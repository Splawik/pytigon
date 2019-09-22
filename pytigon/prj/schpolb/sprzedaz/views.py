#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

import time
import requests
from pytigon_lib.schtools.schjson import json_dumps, json_loads

PFORM = form_with_perms('sprzedaz') 


class LoadKalkulatorData(forms.Form):
    data = forms.FileField(label=_('Dane zasilające kalkulator'), required=True, )
    
    
    

def view_loadkalkulatordata(request, *argi, **argv):
    return PFORM(request, LoadKalkulatorData, 'sprzedaz/formloadkalkulatordata.html', {})








def rebuild(request):
    
    naglowki = models.Nag.objects.filter(status=2)
    for nag in naglowki:
        errors = False
        nag_save = False
        if not nag.logo or nag.logo=="":
            lok = models.CastoramaKli.objects.filter(numer=nag.nr_lok_dost)
            if len(lok) > 0:
                if len(lok)==1:
                    nag.logo = lok[0].logo
                    nag.mag = lok[0].mag
                    nag_save = True
                else:
                    errors = True
            else:
                errors = True
                
        for lin in nag.lin_set.all():
            if not lin.symkar:
                x = models.CastoramaKar.objects.filter(id_castorama = lin.castorama_kar)
                if len(x)==1:
                    lin.symkar = x[0].id_softlab
                    lin.save()
                else:
                    errors = True
        if not errors:
            nag_save = True
            nag.status = 5
            
        if nag_save:
            nag.save()
    
    return HttpResponse("REFRESH")
    




@dict_to_json

def kalkulator_tables(request, tab):
    
    with settings.DB as db:
        if tab=='0':
            sel = "select * from POLBRUK_TECH.dbo.grupy_asortymentowe_polbruk_rc rc(NOLOCK)"
        elif tab=='1':
            sel = "select * from POLBRUK_TECH.dbo.w_polbruk_vv_qlik_mag mag(NOLOCK) where mag like '__' and OpisMag like '%wyrob%'"
        elif tab=='2':
            sel = "select * from POLBRUK_TECH.dbo.w_polbruk_vv_tkw_mag y(NOLOCK) where SymkarY like '2017%' "
        elif tab=='3':
            sel = "select kar.symkar, waga, waga/180 from POLBRUK_PROD.dbo.mg_kar kar(NOLOCK) left join POLBRUK_PROD.dbo.mg_jm jm(NOLOCK) on jm.symkar = kar.symkar and jm.jm = kar.jm  where Status = 'A' and IsNull(waga,0) <> 0"
        else:
            sel = None
        
        if sel:
            rettab = []
            db.execute(sel)
            ret=db.fetchall()
            for row in ret:
                tmp = []
                for item in row:
                    if type(item).__name__=='Decimal':
                        tmp.append(float(item))
                    else:
                        tmp.append(item)
                rettab.append(tmp)
            return rettab
        else:
            return []
    






def kalkulator_zmieniony(request, **argv):
    
    key = 'sprz/kalk/time_to_sync'
    gmt = time.gmtime()
    value = "%04d.%02d.%02d %02d:%02d:%02d" % (gmt[0], gmt[1], gmt[2], gmt[3], gmt[4], gmt[5])
    user =  request.user.username
    
    p = models.SprzedazParameter.objects.filter(type='sys_user', subtype='polbruk', key=key)
    if len(p)>0:
        obj = p[0]
    else:
        obj = models.SprzedazParameter()
        obj.type = 'sys_user'
        obj.subtype = 'polbruk'
        obj.key = key
    
    obj.value = value
    obj.save()
    
    return HttpResponse('OK')
    




@dict_to_json

def kiedy_kalk_zmieniony(request, **argv):
    
    key = 'sprz/kalk/time_to_sync'
    p = models.SprzedazParameter.objects.filter(type='sys_user', subtype='polbruk', key=key)
    if len(p)>0:
        obj = p[0]
        return { 'TIME': obj.value }
    else:
        return { 'TIME': None }
    

@dict_to_template('sprzedaz/v_load_castorama_data.html')




def load_castorama_data(request):
    
    url_base = "https://www.castorama.pl/cataloginventory/index/checkAvailabilityInStores?sku=%s&&qty=1&qty=1&province=%s"
    models.CastoramaStanMag.objects.all().delete()
    regiony = list(models.CastoramaRegion.objects.all())
    kartoteki = list(models.CastoramaKar.objects.all())
    log  = []
    for region in regiony:
        for kar in kartoteki:
            url = url_base % (kar.id_castorama, region.name)
            log.append(url)
            r = requests.get(url)
            try:
                jdata = json_loads(r.text)
            except:
                continue
            if 'error' in jdata and jdata['error'] == False:
                if 'success' in jdata:
                    for pos in jdata['success']:
                        x = models.CastoramaStanMag()
                        x.store_id = pos['id']
                        x.store_code = pos['store_code']
                        x.nazwa = pos['nazwa']
                        x.ulica = pos['ulica']
                        x.telefon = pos['telefon']
                        x.qty = float(pos['qty'])
                        
                        x.region = region.name
                        
                        x.mag = ""
                        x.logo = ""
                        
                        try:            
                            objs = models.CastoramaKli.objects.all()
                            for obj in objs:
                                if int(obj.numer) == pos['store_code']:
                                    x.mag = obj.mag 
                                    x.logo = obj.logo
                        except:
                            pass
                                                
                        x.symkar = kar.id_softlab
                        x.nazwa_kar = kar.nazwa_kar
                        
                        x.save()
    
    return { 'log': log}
    


 
