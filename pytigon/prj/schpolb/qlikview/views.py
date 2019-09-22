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

import  openpyxl
from pytigon_lib.schfs.vfstools import get_temp_filename

SEL1=""" SELECT count(*) from [POLBRUK_TECH].[dbo].[w_polbruk_tkw_y] where SymKarY = '%s' """
SEL2=""" insert into [POLBRUK_TECH].[dbo].[w_polbruk_tkw_y](SymKarY, SymKar2, SymKar, TKW_SUR, TKW_ROB, TKW_ADM, TKW_ZMIEN, TKW_AMOR, TKW_KOSZTMAG) values('%s', '%s', '%s', %f, %f, %f, %f, %f, %f) """
SEL3=""" update [POLBRUK_TECH].[dbo].[w_polbruk_tkw_y] set TKW_SUR = '%s', TKW_ROB = '%s', TKW_ADM = '%s', TKW_ZMIEN = '%s', TKW_AMOR = '%s', TKW_KOSZTMAG = '%s' where symkary = '%s' """

SEL11=""" SELECT count(*) from [POLBRUK_TECH].[dbo].[w_polbruk_tkw_y_alt] where SymKarY = '%s' """
SEL12=""" insert into [POLBRUK_TECH].[dbo].[w_polbruk_tkw_y_alt](SymKarY, SymKar2, SymKar, TKW_SUR, TKW_ROB, TKW_ADM, TKW_ZMIEN, TKW_AMOR, TKW_KOSZTMAG) values('%s', '%s', '%s', %f, %f, %f, %f, %f, %f) """
SEL13=""" update [POLBRUK_TECH].[dbo].[w_polbruk_tkw_y_alt] set TKW_SUR = '%s', TKW_ROB = '%s', TKW_ADM = '%s', TKW_ZMIEN = '%s', TKW_AMOR = '%s', TKW_KOSZTMAG = '%s' where symkary = '%s' """

sel4=""" delete from [POLBRUK_TECH].[dbo].[w_polbruk_spec_rab] """
sel5=""" insert into [POLBRUK_TECH].[dbo].[w_polbruk_spec_rab](logo, data_od, data_do, grupa, symkar, rabat) values('%s', '%s', '%s', '%s', '%s', %f) """

def process_import(data, sel1, sel2, sel3):
    ret_messages = []
    file_name = get_temp_filename("temp.xlsx")
    plik = open(file_name, 'wb')
    plik.write(data)
    plik.close()

    workbook = openpyxl.load_workbook(filename=file_name, read_only=True)
    worksheets = workbook.get_sheet_names()
    worksheet = workbook.get_sheet_by_name(worksheets[0])

    ret = []

    def_date = str(datetime.date.today().year)

    with settings.DB as db:

        def insert_tkw(symkary, symkar2, symkar, f1, f2, f3, f4, f5, f6):
            upd = sel2 % ( symkary, symkar2, symkar, f1, f2, f3, f4, f5, f6 )
            db.execute(upd, True)

        def update_tkw(symkary, symkar2, symkar, f1, f2, f3, f4, f5, f6):
            upd = sel3 % ( f1, f2, f3, f4, f5, f6, symkary )
            db.execute(upd, True)

        def is_in_database(symkary):
            symkar2 = str(symkary).replace("'","").replace("\"","")
            sel = sel1 % symkar2
            db.execute(sel)
            tab = db.fetchall()
            if int(tab[0][0]) == 0:
                return False
            else:
                return True

        def is_in_database(symkary):
            symkar2 = str(symkary).replace("'","").replace("\"","")
            sel = sel1 % symkar2
            db.execute(sel)
            tab = db.fetchall()
            if int(tab[0][0]) == 0:
                return False
            else:
                return True

        for row in worksheet.rows:
            symkar = row[0].value
            if symkar:
                symkar = symkar.replace("'","").replace("\"","")
                if '/' in symkar:
                    parts = symkar.split('/')
                    if len(parts)==2:
                        ysymkar = def_date + "/" + symkar
                    else:
                        ysymkar = symkar
                    ret.append([ysymkar, parts[-1], symkar, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value ] )
            else:
                break

        for pos in ret:
            if not is_in_database(pos[0]):
                insert_tkw(pos[0], pos[1], pos[2], float(pos[3]), float(pos[4]), float(pos[5]), float(pos[6]), float(pos[7]), float(pos[8]))
                ret_messages.append(("Insert:", pos[1:]))
            else:
                update_tkw(pos[0], pos[1], pos[2], float(pos[3]), float(pos[4]), float(pos[5]), float(pos[6]), float(pos[7]), float(pos[8]))
                ret_messages.append(("Update:", pos[1:]))

    return ret_messages
 

PFORM = form_with_perms('qlikview') 


class QlikViewUploadForm(forms.Form):
    qlikview_file = forms.FileField(label=_('xls[x]'), required=True, )
    
    def process(self, request, queryset=None):
    
        return {}
    
    def render_to_response(self, request, template, context_instance):
        firma = None
        
        if 'firm' in request.GET:
            firma = request.GET['firm']
    
        print("Get:", firma)
        
        if firma:
            qlikviewdata= request.FILES['qlikview_file']
            data = qlikviewdata.read()
    
            try:
                syg = data[:2].decode('utf-8')
            except:
                syg = 'bi'
                
            print("Syg:", syg)
    
            if syg=='PK':
                file_name = get_temp_filename("temp.xlsx")
            
                plik = open(file_name, 'wb')
                plik.write(data)
                plik.close()
    
                workbook = xlrd.open_workbook(file_name)
                worksheets = workbook.sheet_names()
        
                def lokalizacja_from_row(row):
                    obj = models.qlik_lokalizacje()
                    obj.FIRMA_ID = firma
                    obj.MagSprz = row[0]
                    obj.Opis = row[1]
                    obj.Region = row[2]
                    return obj
    
                def segmentacja_from_row(row):
                    obj = models.qlik_segmentacja()
                    obj.FIRMA_ID = firma
                    try:
                        obj.LogoP = str(int(row[0]))
                    except:
                        obj.LogoP = row[0]
                    obj.Klastrowanie_BEH_FD = row[1]
                    obj.Klastrowanie_VAL_FD = row[2]
                    obj.Klastrowanie_BEH_Hurtownie = row[3]
                    obj.Klastrowanie_VAL_Hurtownie = row[4]
                    obj.Segment_2 = row[5]
                    return obj
    
                def grupa_as_from_row(row):
                    obj = models.qlik_grupa_asortyment()
                    obj.FIRMA_ID = firma
                    obj.GrupaAsortymentuNazwa = row[0]
                    obj.GrupaAsortymentuNazwa2 = row[1]
                    return obj
    
                for worksheet_name in worksheets:
                    if worksheet_name == 'qlik_lokalizacje':
                        model = models.qlik_lokalizacje
                        obj_from_row = lokalizacja_from_row
                    elif worksheet_name == 'qlik_grupa_asortyment':
                        model = models.qlik_grupa_asortyment
                        obj_from_row = grupa_as_from_row
                    elif worksheet_name == 'qlik_segmentacja':
                        model=models.qlik_segmentacja                    
                        obj_from_row = segmentacja_from_row
                    else:
                        break
    
                    model.objects.filter(FIRMA_ID=firma).delete()
                    tab_obj = []
    
                    worksheet = workbook.sheet_by_name(worksheet_name)
                    num_rows = worksheet.nrows - 1                    
                    if num_rows>1:
                        curr_row = 1                    
                        ret = []
                        titles = []
                        first_row = worksheet.row(0)
                        for item in first_row:
                            if item.value:
                                titles.append(item.value)
                            else:
                                break
                        width = len(titles)
                        if width>0:
                            print("TITLE:", titles)                            
                            while curr_row <= num_rows:                    
                                row = worksheet.row(curr_row)
                                row2 = []
                                for i in range(0,width):
                                    row2.append(row[i].value)
                                curr_row += 1
                                obj = obj_from_row(row2)
                                tab_obj.append(obj)
                                print("ROW:", row2)
                                if len(tab_obj)>500:
                                    model.objects.bulk_create(tab_obj)
                                    tab_obj = []
                    if len(tab_obj)>0:
                        model.objects.bulk_create(tab_obj)
    
        
        return HttpResponseRedirect("../../table/qlik_firmy/-/form/list?schtml=1")

def view_qlikviewuploadform(request, *argi, **argv):
    return PFORM(request, QlikViewUploadForm, 'qlikview/formqlikviewuploadform.html', {})


class _FilterFormqlik_handlowiec(forms.Form):
    nazwa_h = forms.CharField(label=_('Nazwa'), required=True, )
    
    def process(self, request, queryset=None):
    
        name = self.cleaned_data['nazwa_h']
        queryset = queryset.filter(NazwaH__icontains=name)
        return queryset
    

def view__filterformqlik_handlowiec(request, *argi, **argv):
    return PFORM(request, _FilterFormqlik_handlowiec, 'qlikview/form_filterformqlik_handlowiec.html', {})


class QlikTkw(forms.Form):
    tkw_file = forms.FileField(label=_('Arkusz .xlsx z tkw'), required=True, )
    
    def process(self, request, queryset=None):
    
        qlikviewdata= self.cleaned_data['tkw_file']
        data = qlikviewdata.read()
        messages = process_import(data, SEL1, SEL2, SEL3)
        return { "object_list": messages }
    

def view_qliktkw(request, *argi, **argv):
    return PFORM(request, QlikTkw, 'qlikview/formqliktkw.html', {})


class QlikRabat(forms.Form):
    rabat_file = forms.FileField(label=_('Plik z rabatami [.xlsx]'), required=True, )
    
    def process(self, request, queryset=None):
    
        qlikviewdata= self.cleaned_data['rabat_file']
        data = qlikviewdata.read()
        
        ret = []
        
        file_name = get_temp_filename("temp.xlsx")
        plik = open(file_name, 'wb')
        plik.write(data)
        plik.close()
        
        workbook = openpyxl.load_workbook(filename=file_name, read_only=True)
        worksheets = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(worksheets[0])
        
        with settings.DB as db:
        
            db.execute(sel4, True)
            
            def insert_rabat(logo, data_od, data_do, grupa, symkar, rabat):    
                upd = sel5 % (logo, data_od, data_do, grupa, symkar, rabat)
                db.execute(upd, True)
        
            for row in worksheet.rows:
                logo = row[0].value
                if logo:
                    try:
                        logo2 = int(logo)
                        if logo2>0:
                            insert_rabat(row[0].value, row[1].value.isoformat().replace('-','')[:8], row[2].value.isoformat().replace('-','')[:8], row[3].value, row[4].value, float(row[5].value))                    
                            ret.append([row[0].value, row[1].value.isoformat().replace('-','')[:8], row[2].value.isoformat().replace('-','')[:8], row[3].value, row[4].value, float(row[5].value)])
                    except:
                        pass
                else:
                    break
                    
        return { "object_list": ret }
    

def view_qlikrabat(request, *argi, **argv):
    return PFORM(request, QlikRabat, 'qlikview/formqlikrabat.html', {})


class QlikViewTkw2(forms.Form):
    tkw_file = forms.FileField(label=_('Arkusz .xlsx z tkw'), required=True, )
    
    def process(self, request, queryset=None):
    
        qlikviewdata= self.cleaned_data['tkw_file']
        data = qlikviewdata.read()
        messages = process_import(data, SEL11, SEL12, SEL13)
        return { "object_list": messages }
    

def view_qlikviewtkw2(request, *argi, **argv):
    return PFORM(request, QlikViewTkw2, 'qlikview/formqlikviewtkw2.html', {})








def import_data(request, pk):
    
    obj = models.qlik_firmy.objects.get(pk=int(pk))
    f_id = obj.FIRMA_ID
    
    if f_id=='POLBRUK':
        import_sql('polbruk', f_id, settings.DB)
    elif f_id=='GP':
        db = settings.DB.duplicate()
        db.connection_string = CONNECTION_GP_STRING
        import_sql('gp', f_id, db)
    
    return HttpResponseRedirect("../../-/form/list?schtml=1")
    






def import_data2(request, pk):
    
    obj = models.qlik_firmy.objects.get(pk=int(pk))
    f_id = obj.FIRMA_ID
    return HttpResponseRedirect('../../../../form/QlikViewUploadForm/?firm=%s' % f_id)
    


 
