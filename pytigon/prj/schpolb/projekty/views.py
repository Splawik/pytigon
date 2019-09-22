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

from django.template import Context, Template
 

PFORM = form_with_perms('projekty') 


class _FilterFormProjektNawierzchni(forms.Form):
    projektant = forms.ChoiceField(label=_('Projektanci'), required=True, choices=models.lista_projektant)
    
    def process(self, request, queryset=None):
    
        projektant = self.cleaned_data['projektant']
        if projektant:
            if projektant=='Wszystkie':
                pass
            elif projektant=='Tylko moje':
                queryset = queryset.filter(projektant__username=request.user.username)
            else:
                queryset = queryset.filter(projektant__username=projektant)
        return queryset
    

def view__filterformprojektnawierzchni(request, *argi, **argv):
    return PFORM(request, _FilterFormProjektNawierzchni, 'projekty/form_filterformprojektnawierzchni.html', {})


class Raporty(forms.Form):
    typ_raportu = forms.ChoiceField(label=_('Typ raportu'), required=True, choices=models.TypRaportu)
    
    def process(self, request, queryset=None):
    
        typ_raportu = self.cleaned_data['typ_raportu']
        
        if typ_raportu == 'proj_naw_sumy':
            projekty = models.ProjektNawierzchni.objects.all()
            object_list = []
            
            data = {}
            projektanci = []
            
            for projekt in projekty:
                if projekt.projektant:
                    projektant = projekt.projektant.username
                else:
                    projektant = "diabli wiedzą kto"
                data_prz = projekt.data_prz
                year = data_prz.year
                month = data_prz.month
                if not year in data:
                    data[year] = {}
                if not month in data[year]:
                    data[year][month] = {}
                if not projektant in data[year][month]:
                    data[year][month][projektant] = 0
                data[year][month][projektant] += 1
                if not projektant in projektanci:
                    projektanci.append(projektant)
            print(data)        
            for year in sorted(list([y for y in data]))[::-1]:
                for month in sorted(list([m for m in data[year]]))[::-1]:
                    x = []
                    for projektant in projektanci:
                        c = 0
                        if projektant in data[year][month]:
                            c = data[year][month][projektant]
                        x.append(c)
                    object_list.append([year, month, ] + x )
        
        doc_type='html'        
        
        return { "object_list": object_list, 'doc_type': doc_type, 'typ_raportu': typ_raportu, 'projektanci': projektanci }
    

def view_raporty(request, *argi, **argv):
    return PFORM(request, Raporty, 'projekty/formraporty.html', {})








def projekt_status(request, pk):
    
    obj=models.ProjektInw.objects.get(id=pk)
    obj.status = int(request.GET['status'])
    obj.save()
    return redirect("ok")
    






def etap_status(request, pk):
    
    obj=models.EtapProjektuInw.objects.get(id=pk)
    obj.status = int(request.GET['status'])
    obj.save()
    return redirect("ok")
    






def projekt_naw_status(request, pk):
    
    obj=models.ProjektNawierzchni.objects.get(id=pk)
    obj.status = int(request.GET['status'])
    obj.save()
    return redirect("ok")
    


 
