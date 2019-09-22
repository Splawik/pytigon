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

import django
import datetime
import json
import collections
from django.db import connection


sel1 = "select Nazwa, Opis from dbo.sl_fn_OperatorNaglSlo(0) sl where Operator = 0"
sel2 = "select Login, Imie, Nazwisko FROM dbo.sl_vv_operatorbro as s(NOLOCK) where locked=0 and login not like 'abs%' and login not like 'adm%'"
sel3 = "select distinct grupa, dzial FROM dbo.sl_vv_HierOrgOperator_Bro as s(NOLOCK) where Grupa like 'POLBRUK%'"
sel4 = "select login, grupa FROM dbo.sl_vv_HierOrgOperator_Bro as s(NOLOCK) where Grupa like 'POLBRUK%'"
sel5 = "select NazwaDet, NazwaGrup from SL_VV_OPERATORGRUP g(NOLOCK) order by NazwaDet"
sel6 = "select FunkcjaPraw, Opis FROM dbo.[w_funkcjePraw_opis] s WITH (NOLOCK) order by FunkcjaPraw, Idk"
sel7 = "select RightsOprName, RightsOprDesc FROM dbo.rgt_vv_OprBro as s(NOLOCK) where Enabled=1 and exists (select top 1 * from dbo.rgt_vv_OprOperator as ss(NOLOCK) where ss.RightsOprName = s.RightsOprName)"

sel8 = "select * from sl_Operator op(NOLOCK)  where locked=0 and login not like 'abs_%' order by Nazwisko, Imie"
sel9 = "exec w_rls_uprawnienia2 '%s' "
sel10 = "select * from rgt_vv_OprBro opr(NOLOCK) "
sel11 = "select * from sl_OperatorNagl bro(NOLOCK) "

sel12=""" select Login, Imie, Nazwisko, LastPasswordChange,Logo, Mail   from sl_Operator op(NOLOCK)  where locked=0 and login not like 'abs_%' order by Nazwisko, Imie """
sel13=""" exec w_rls_uprawnienia2 '%s' """
sel14=""" select * from rgt_vv_OprBro opr(NOLOCK) """
sel15=""" select * from sl_OperatorNagl bro(NOLOCK) """


sel21=""" 
select typ.RodzajAsortymentu, typ.typasortymentu, typ.opis, typ.pd_konto4, IsNull(akc.login,''), IsNull(akc.Poziom,0) from W_VV_MG_TYPASORTYMENTU typ(NOLOCK) 
left join W_VV_MG_TYPASORTYMENTU_AKC_VIEW akc(NOLOCK) on akc.TypAsortymentu = typ.typasortymentu
where pd_zapob=1 --and login <> 'brak'
order by typ.RodzajAsortymentu, typ.TypAsortymentu, typ.pd_konto4, akc.poziom, akc.login
"""

sel22 = """select symkar, OpiKar, OpiKar4, jm from MG_VV_KAR_ALL_BW kar(NOLOCK) where pd_typ ='%s' """

sel100 = """
select ifnull(prawa_dzial.opis, tab3.dz) Stanowisko, tab3.nazwa  from (
    select tab.*, tab2.oper_count from
    (
        select ifnull(prawa_dzial.profil, prawa_dzial.nazwa) dz, prawa_grupapraw.nazwa, count(*) grupa_count from prawa_operator
        left join prawa_dzial on prawa_dzial.id = prawa_operator.dzial_id
        left join prawa_operator_grupy on prawa_operator_grupy.operator_id = prawa_operator.id
        left join prawa_grupapraw on prawa_grupapraw.id = prawa_operator_grupy.grupapraw_id
        where prawa_operator.aktywny = 1
        group by ifnull(profil, nazwa), prawa_grupapraw.nazwa
    ) tab
    left join (
        select ifnull(prawa_dzial.profil, prawa_dzial.nazwa) dz, count(*) oper_count from prawa_operator
        left join prawa_dzial on prawa_dzial.id = prawa_operator.dzial_id
        where prawa_operator.aktywny = 1
        group by ifnull(profil, nazwa)
    ) tab2 on tab2.dz = tab.dz
) tab3
left join prawa_dzial on prawa_dzial.nazwa = tab3.dz
where grupa_count = oper_count and grupa_count > 1
order by ifnull(prawa_dzial.opis, tab3.dz), tab3.nazwa
"""

sel101 = """
select * from
(
    select DataM Data, status, __EntityName, __BKString from replinfo info(NOLOCK) 
    where __EntityName in ('sl_OperatorGrup', 'rgt_OprOperator') and datam >= getdate()-120
    union all
    select DataD Data, 'D', __EntityName, __BKString from replinfodeleted infod(NOLOCK) 
    where __EntityName in ('sl_OperatorGrup', 'rgt_OprOperator') and datad >= getdate()-120
) tab 
order by data
"""

sel102 = """
select NazwaDet, NazwaGrup from SL_VV_OPERATORGRUP g(NOLOCK)
order by NazwaDet
"""

sel103 = """
select login, grupa FROM dbo.sl_vv_HierOrgOperator_Bro as s(NOLOCK) where Grupa like 'POLBRUK%'
"""


def null_to_str(value):
    if value:
        return value
    return ""

def int_key_from_str(v):
    try:
        ret = int(v)
    except:
        ret = 0
    return ret

def key_for_autoryz(v):
    return key.split('/')[3]
 

PFORM = form_with_perms('prawa') 


class __FilterFormOperator(forms.Form):
    nazwisko = forms.CharField(label=_('Nazwisko'), required=True, )
    
    
    

def view___filterformoperator(request, *argi, **argv):
    return PFORM(request, __FilterFormOperator, 'prawa/form__filterformoperator.html', {})


class GrupyFunkcjeForm(forms.Form):
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        
        tab_rights_1 = {}
        tab_rights_2 = {}                
        desc = {}                
        grupy = {}
        
        with settings.DB as db:
            db.execute(sel10)
            prawa =db.fetchall()
            for prawo in prawa:
                desc[prawo[2]] = prawo[3]
        
            db.execute(sel11)
            grupy2 =list(db.fetchall())
            for grupa2 in grupy2:
                desc[grupa2[1]] = grupa2[2]
        
            db.execute(sel8)
            operators = list(db.fetchall())
            for operator in operators:
                login_name = operator[1]     
                db.execute(sel9 % login_name )
                rights = db.fetchall()
                
                rights_mod = []
                for right in rights:
                    if right[0]  == 'Funkcje praw':
                        if right[3] in tab_rights_1:
                            tab_rights_1[right[3]].append(login_name)
                        else:
                            tab_rights_1[right[3]] = [ login_name, ]                        
                    if right[0]  ==  'Grupa operatorów:':
                        if right[3] in tab_rights_2:
                            tab_rights_2[right[3]].append(login_name)
                        else:
                            tab_rights_2[right[3]] = [ login_name, ]
        
                    if right[0].startswith('Funkcje praw wynika'): 
                        rrr = "Grupa: "+right[4]
                        if not right[4] in grupy:
                            grupy[right[4]] = {}
                        if not right[3] in grupy[right[4]]:
                            if right[3] in desc:
                                ddd = desc[right[3]]
                            else:
                                ddd = right[4]
                            grupy[right[4]][right[3]] = ddd
                    else:
                        rrr = right[0]
                    
                    if right[3] in desc:
                            rights_mod.append(( rrr, right[3], desc[right[3]]) )
                    else:
                            rights_mod.append(( rrr, right[3], right[4]) )
        
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': grupy, 'keys': sorted(grupy.keys()), 'date': d[:10], 'time': d[11:16], 'rights': rights, 'doc_type': doc_type, }
    

def view_grupyfunkcjeform(request, *argi, **argv):
    return PFORM(request, GrupyFunkcjeForm, 'prawa/formgrupyfunkcjeform.html', {})


class FunkcjePrawForm(forms.Form):
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        
        with settings.DB as db:
            db.execute(sel6)
            tab=db.fetchall()
        
            fun_opis = {}
            for pos in tab:
                if pos[0] in fun_opis:
                    fun_opis[pos[0]] = fun_opis[pos[0]]+"\n" + pos[1]
                else:
                    fun_opis[pos[0]] = pos[1]
        
            db.execute(sel7)
            tab=db.fetchall()
        
        def format(s):    
            return s.replace('\n','<br />')
        
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': tab, 'fun_opis': fun_opis, 'format': format, 'date': d[:10], 'time': d[11:16], 'doc_type': doc_type }
    

def view_funkcjeprawform(request, *argi, **argv):
    return PFORM(request, FunkcjePrawForm, 'prawa/formfunkcjeprawform.html', {})


class KartyPrawForm(forms.Form):
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        
        tab_rights_1 = {}
        tab_rights_2 = {}                
        desc = {}                
        grupy = {}
        ret = []
        
        pewne_grupy = {}
        cursor = connection.cursor()
        cursor.execute(sel100)
        for row in cursor.fetchall():
            if row[0] in pewne_grupy:        
                pewne_grupy[row[0]].append(row[1])
            else:
                pewne_grupy[row[0]] = [ row[1], ]
                
        prac_test = {}
        for prac in models.Operator.objects.all():
            prac_test[prac.login] = list( [ g.nazwa for g in prac.grupy.all() ] )
        
        with settings.DB as db:
            def ls_operators():            
                sel = sel12
                db.execute(sel)
                tab=db.fetchall()    
                _ret = []
                for pos in tab:
                    try:
                        p=models.Operator.objects.get(login=pos[0])
                        x =  p.dzial.profil
                        if not x:
                            x = p.dzial.opis
                    except:
                        x = ''        
                    row = [x, pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]]
                    _ret.append(row)
                return sorted(_ret, key=lambda row: row[0]) 
                
            def get_operator_rights(login_name):
                sel = sel13 % login_name
                db.execute(sel)
                tab=db.fetchall()
                return tab
        
            def ls_fun_praw():    
                sel = sel14
                db.execute(sel)
                tab=db.fetchall()
                return tab
        
            def ls_grup():    
                sel = sel15
                db.execute(sel)
                tab=db.fetchall()
                return tab
        
            lsprawa = ls_fun_praw()
            for prawo in lsprawa:
                desc[prawo[2]] = prawo[3]
        
            lsgrupy = ls_grup()
            for grupa in lsgrupy:
                desc[grupa[1]] = grupa[2]
        
            operators = ls_operators()
            for operator in operators:
                login_name = operator[1]                                    
                print(login_name)
                rights = get_operator_rights(login_name)
                
                rights_mod = []
                for right in rights:
                    if right[0]  == 'Funkcje praw':
                        if right[3] in tab_rights_1:
                            tab_rights_1[right[3]].append(login_name)
                        else:
                            tab_rights_1[right[3]] = [ login_name, ]                        
                    if right[0]  ==  'Grupa operatorów:':
                        if right[3] in tab_rights_2:
                            tab_rights_2[right[3]].append(login_name)
                        else:
                            tab_rights_2[right[3]] = [ login_name, ]
        
                    if right[0].startswith('Funkcje praw wynika'): 
                        rrr = "Grupa: "+right[4]
                        if not right[4] in grupy:
                            grupy[right[4]] = {}
                        if not right[3] in grupy[right[4]]:
                            if right[3] in desc:
                                ddd = desc[right[3]]
                            else:
                                ddd = right[4]
                            grupy[right[4]][right[3]] = ddd
                    else:
                        rrr = right[0]
                    
                    if right[3] in desc:
                            rights_mod.append(( rrr, right[3], desc[right[3]]) )
                    else:
                            rights_mod.append(( rrr, right[3], right[4]) )
                
                test=False
                for pos in rights_mod:
                    if 'Grupa oper' in pos[0]:
                        test=True
                        break        
                if test:
                    ret.append([operator, rights_mod])
        
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': ret, 'date': d[:10], 'time': d[11:16], 'doc_type': doc_type, 'pewne_grupy': pewne_grupy, 'prac_test': prac_test }
        
    

def view_kartyprawform(request, *argi, **argv):
    return PFORM(request, KartyPrawForm, 'prawa/formkartyprawform.html', {})


class __FilterFormDokPrzydzielenia(forms.Form):
    nazwisko = forms.CharField(label=_('Nazwisko'), required=True, )
    
    
    

def view___filterformdokprzydzielenia(request, *argi, **argv):
    return PFORM(request, __FilterFormDokPrzydzielenia, 'prawa/form__filterformdokprzydzielenia.html', {})


class __FilterFormDokOdebrania(forms.Form):
    nazwisko = forms.CharField(label=_('Nazwisko'), required=True, )
    
    
    

def view___filterformdokodebrania(request, *argi, **argv):
    return PFORM(request, __FilterFormDokOdebrania, 'prawa/form__filterformdokodebrania.html', {})


class AkceptacjeDP(forms.Form):
    extended = forms.BooleanField(label=_('Z kartotekami'), required=False, initial=True,)
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        extended = self.cleaned_data['extended']
        pdf = self.cleaned_data['pdf']
        
        with settings.DB as db:
            db.execute(sel21)
            tab =db.fetchall()
        
            akceptacje = collections.OrderedDict()
            poziomy_akceptacji = []
            object_list = []
        
            for row in tab:  
                key = null_to_str(row[0])+"/"+null_to_str(row[1])+"/"+null_to_str(row[2])+"/" + null_to_str(row[3])
                if not str(row[5]) in poziomy_akceptacji:
                    if str(row[5]) and str(row[5])!='0':
                        poziomy_akceptacji.append(str(row[5]))
                if key in akceptacje:
                    if str(row[5]) in akceptacje[key]:
                        akceptacje[key][str(row[5])] = akceptacje[key][str(row[5])] + ";" + row[4]
                    else:
                        akceptacje[key][str(row[5])] = row[4]
                else:
                    p = {}
                    p[str(row[5])] = row[4]
                    akceptacje[key] = p
        
            if not '6' in poziomy_akceptacji:
                poziomy_akceptacji.append('6')
        
            poziomy_akceptacji.sort(key=int_key_from_str)
        
            class Akceptacja():
                def __init__(self, key, values, tab):
                    self.key = key
                    self.values = values
                    self.tab = tab
        
                def key_values(self):
                    return self.key.split('/')
        
            for key, values in akceptacje.items():
                keys = key.split('/')    
                if extended:
                    db.execute(sel22 % keys[1])
                    tab =db.fetchall()
                else:
                    tab = []
                object_list.append(Akceptacja(key, values, list(tab)))
        
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': object_list,  "poziomy_akceptacji": poziomy_akceptacji, "extended": extended,  'date': d[:10], 'time': d[11:16], 'doc_type': doc_type, }
    

def view_akceptacjedp(request, *argi, **argv):
    return PFORM(request, AkceptacjeDP, 'prawa/formakceptacjedp.html', {})


class PrawaWyklucz(forms.Form):
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        
        object_list = []
        tab = models.GrupaPraw.objects.all()
        for obj in tab:    
            if obj.zakaz.count() >0:
                for grupa2 in obj.zakaz.all():
                    if grupa2.id > obj.id:
                        object_list.append([obj.nazwa, obj.opis, grupa2.nazwa, grupa2.opis])
                
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': object_list,  'date': d[:10], 'time': d[11:16], 'doc_type': doc_type, }
    

def view_prawawyklucz(request, *argi, **argv):
    return PFORM(request, PrawaWyklucz, 'prawa/formprawawyklucz.html', {})


class GrupyZOperatorami(forms.Form):
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        
        object_list = []
        tab = models.GrupaPraw.objects.all()
        for obj in tab:    
            operatorzy = obj.operator_set.filter(aktywny=True)
            if len(operatorzy)>0:
                object_list.append([obj.nazwa, list(operatorzy)])
                     
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': object_list,  'date': d[:10], 'time': d[11:16], 'doc_type': doc_type, }
    

def view_grupyzoperatorami(request, *argi, **argv):
    return PFORM(request, GrupyZOperatorami, 'prawa/formgrupyzoperatorami.html', {})


class LogZmian(forms.Form):
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        object_list = []
        
        with settings.DB as db:
            db.execute(sel101)
            zmiany =db.fetchall()
            for zmiana in zmiany:
                i = zmiana[1]
                typ = zmiana[2]
                desc = zmiana[3].split('~')
                if len(desc)==2:
                    if i=='I':
                        if typ == 'sl_OperatorGrup':                
                            object_list.append([1, zmiana[0], 'Dodanie operatora: <strong>%s </strong> do grupy: <strong>%s</strong>' % (desc[1], desc[0] )] )
                        else:
                            object_list.append([1, zmiana[0], 'Dodanie grupy: <strong>%s </strong> do funkcji praw: <strong>%s</strong>' % (desc[1], desc[0] )] )
                    else:
                        if typ == 'sl_OperatorGrup':                
                            object_list.append([2, zmiana[0], 'Odłączenie operatora: <strong>%s </strong> od grupy: <strong>%s</strong>' % (desc[1], desc[0] )] )
                        else:
                            object_list.append([2, zmiana[0], 'Odłączenie grupy: <strong>%s </strong> od funkcji praw: <strong>%s</strong>' % (desc[1], desc[0] )] )
        
        d = datetime.datetime.now().isoformat()
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        
        return { 'object_list': object_list,  'date': d[:10], 'time': d[11:16], 'doc_type': doc_type, }
    

def view_logzmian(request, *argi, **argv):
    return PFORM(request, LogZmian, 'prawa/formlogzmian.html', {})








def grupy_import(request):
    
    with settings.DB as db:
        db.execute(sel1)
        ret=db.fetchall()
        for pos in ret:
            nazwa = pos[0]
            opis = pos[1]
            if pos[1]:
                    opis = pos[1][:128]
            else:
                opis = pos[1]
            if not opis:
                opis = nazwa
            if len(nazwa)>0:
                objs = models.GrupaPraw.objects.filter(nazwa=nazwa)
                if len(objs)==0:
                    obj = models.GrupaPraw(nazwa=nazwa, opis=opis)
                    obj.save()
    new_url = request.path +"/../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def dzial_import(request):
    
    with settings.DB as db:
        db.execute(sel3)
        ret=db.fetchall()
        for pos in ret:
            nazwa = pos[0]
            opis = pos[1]
            if len(nazwa)>0 and opis:
                objs = models.Dzial.objects.filter(nazwa=nazwa)
                if len(objs)==0:
                    obj = models.Dzial(nazwa=nazwa, opis=opis)
                    obj.save()
                    
        db.execute(sel103)
        ret=db.fetchall()
        for pos in ret:
            login = pos[0]
            dzial = pos[1]    
            p=models.Operator.objects.filter(login=pos[0])
            d=models.Dzial.objects.filter(nazwa=dzial)
            if len(p)==1 and len(d)==1:
                p[0].dzial = d[0]
                p[0].save()
    
    new_url = request.path +"/../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def lok_import(request):
    
    pass
    






def gen_karty(request):
    
    new_url = request.path +"/../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def oper_import(request):
    
    with settings.DB as db:
        db.execute(sel2)
        ret=db.fetchall()
        for pos in ret:
            login = pos[0]
            imie = pos[1]
            nazwisko = pos[2]
            if len(login)>0:
                objs = models.Operator.objects.filter(login=login)
                if len(objs)==0:
                    obj = models.Operator(login=login, imie=imie, nazwisko=nazwisko)
                    obj.save()
    new_url = request.path +"/../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def oper_imp_dzial(request):
    
    with settings.DB as db:
        db.execute(sel4)
        ret=db.fetchall()
        for pos in ret:
            login = pos[0]
            dzial = pos[1]
            if len(login)>0:
                objs = models.Operator.objects.filter(login=login)
                if len(objs)==1:
                    oper = objs[0]
                    dzialy = models.Dzial.objects.filter(nazwa=dzial)
                    if len(dzialy)>0:
                        oper.dzial = dzialy[0]
                        oper.save()
    new_url = request.path +"/../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def oper_imp_przel(request):
    
    opers = list(models.Operator.objects.all())
    for oper in opers:
        if oper.dzial:
            dzial = oper.dzial.nazwa
            nr = dzial.rfind('\\')
            if nr>=0:
                dzial_parent = dzial[:nr]
                parents = models.Operator.objects.filter(dzial__nazwa=dzial_parent)
                if len(parents)==1:
                    oper.przelozony = parents[0]
                    oper.save()
    new_url = request.path +"/../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def zatwierdz(request, pk):
    
    u = django.contrib.auth.get_user(request)
    uname = u.email.split('@')[0]
    oprs = models.Operator.objects.filter(login=uname)
    if len(oprs)==1:
        obj=models.DokPrzydzielenia.objects.get(id=pk)
        obj.zatwierdzil = oprs[0].nazwisko + " " + oprs[0].imie
        obj.save()
        obj.parent.grupy.clear()
        for pos in obj.grupy.all():
            obj.parent.grupy.add(pos)
        obj.parent.aktywny = True
        obj.parent.save()
    
        log = models.LogZmian()
        log.kto = obj.zatwierdzil
        log.kiedy = datetime.date.today()
        log.opis = "Zatwierdzenie obiektu DokPrzydzielenia: "+obj.parent.nazwisko + " " + obj.parent.imie + " /" + str(obj.data_przydzial)
        log.save()
    
    new_url = request.path +"/../../../niezatwierdzone/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def oper_imp_lokal(request):
    
    #workbook = xlrd.open_workbook('c:/prj/kontakty_polbruk.xlsx')
    worksheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(worksheets[0])
    num_rows = worksheet.nrows - 1
    curr_row = -1
    
    ret = []
    
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        ret.append([row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value])
    
    for row in ret:
        lokalizacja = row[2]
        lok = models.Lokalizacja.objects.filter(opis=lokalizacja)
        if len(lok)==1:
            oprs = models.Operator.objects.filter(login=row[6].split('@')[0])
            if len(oprs)==1:
                oprs[0].lokalizacja = lok[0]
                oprs[0].save()
    






def zatwierdz2(request, pk):
    
    u = django.contrib.auth.get_user(request)
    uname = u.email.split('@')[0]
    oprs = models.Operator.objects.filter(login=uname)
    if len(oprs)==1:
        obj=models.DokOdebrania.objects.get(id=pk)
        obj.zatwierdzil = oprs[0].nazwisko + " " + oprs[0].imie
        obj.save()
        
        obj.parent.grupy.clear()
        obj.parent.aktywny = False
        obj.parent.save()
        
        log = models.LogZmian()
        log.kto = obj.zatwierdzil
        log.kiedy = datetime.date.today()
        log.opis = "Odebranie praw - zatwierdzenie"    
        log.save()
        
    new_url = request.path +"/../../../-/form/list?schtml=1"
    return HttpResponseRedirect(new_url)
    






def fun_praw(request):
    
    pass
    






def grupa_praw(request):
    
    pass
    






def spr_praw(request):
    
    with settings.DB as db:
        db.execute(sel5)
        ret=db.fetchall()
        old_oper = ""
        grupy = []
        err_oper = []
        for pos in ret:
            oper = pos[0]
            grupa = pos[1]
            if oper != old_oper:
                if len(grupy)>0:
                    objs = models.Operator.objects.filter(login=old_oper)
                    if len(objs)==1:
                        obj = objs[0]
                        grupy2 = []
                        test=False
                        for grupa2 in obj.grupy:
                            grupy2.append(grupa2.nazwa)
                        if len(grupy2)!=len(grupy):
                            test=True
                        if not test:
                            for g in grupy:
                                if not g in grupy2:
                                    test=True
                                    break
                        if test:
                            err_oper.append(obj)                    
                grupy = []
            else:
                grupy.append[grupa]
        
        user_dict = { "objects": grupy, }
        return render_to_response('prawa/operator.html', user_dict, requeset=request)
    






def regenerate_user_groups(request):
    
    oprs = models.Operator.objects.all()
    for operator in oprs:
        documents=models.DokPrzydzielenia.objects.filter(parent=operator).order_by('data_przydzial')
        documents2=models.DokOdebrania.objects.filter(parent=operator).order_by('data_odebrania')
        l1 = len(documents)
        l2 = len(documents2)
        if l1>0:
            if l2>0:
                if documents[l1-1].data_przydzial > documents2[l2-1].data_odebrania:
                    obj = documents[l1-1]
                else:
                    obj = None
            else:
                obj = documents[l1-1]
                
            if obj:
                obj.parent.grupy.clear()
                for pos in obj.grupy.all():
                    obj.parent.grupy.add(pos)
                obj.parent.aktywny = True
                obj.parent.save()
            else:
                operator.grupy.clear()
                operator.aktywny = False
                operator.save()
                
    return HttpResponse("OK")
    






def gen_wnioski_wg_softlaba(request):
    
    opr_grupy = {}
    with settings.DB as db:
        db.execute(sel102)
        ret=db.fetchall()
    
    for pos in ret:
        login = pos[0]
        grupa = pos[1]
        
        if login in opr_grupy:
            opr_grupy[login].append(grupa)
        else:
            opr_grupy[login] = [ grupa, ]
    
    oprs = models.Operator.objects.all()
    
    lp = 0
    
    for operator in oprs:
        grupy_intranet = list(operator.grupy.all())
        if operator.login in opr_grupy:
            grupy_softlab = opr_grupy[operator.login]
        else:
            grupy_softlab = []
        test = True
        if len(grupy_intranet) == len(grupy_softlab):        
            for grupa in grupy_intranet:
                if not grupa.nazwa in grupy_softlab:
                    test = False
                    break
        else:
            test = False 
        
        if test == False:
            lp = lp + 1
            if len(grupy_softlab)==0:
                document = models.DokOdebrania()
                document.data_odebrania = datetime.date.today()
            else:
                document = models.DokPrzydzielenia()
                document.data_przydzial = datetime.date.today()            
            document.parent = operator
            document.data = datetime.date.today()
            document.sporzadzil = 'slawomir.cholaj'
            document.zatwierdzil = 'slawomir.cholaj' 
            
            print()
            print(lp, "-----------------------------------------")
            print(operator.login)
            print(grupy_softlab)
            print([ gg.nazwa for gg in grupy_intranet])
            
            document.save()
                
            if len(grupy_softlab)!=0:
                for pos in grupy_softlab:
                    g = models.GrupaPraw.objects.filter(nazwa=pos)
                    if len(g) == 1:
                        document.grupy.add(g[0])
                                                
            
            if len(grupy_softlab)!=0:
                operator.grupy.clear()
                for pos in document.grupy.all():
                    operator.grupy.add(pos)            
            
            
    return HttpResponse("OK")
        
    

@dict_to_template('prawa/v_gen.html')




def gen(request, pk):
    
    obj=models.Operator.objects.get(id=pk)
    
    dok = models.DokPrzydzielenia()
    dok.parent = obj
    dok.data = datetime.datetime.now()
    dok.data_przydzial = datetime.datetime.now()
    #dok.data_przydzial = datetime.date.today()
    dok.save()
    
    dok.grupy.clear()
    
    for pos in obj.grupy.all():
        dok.grupy.add(pos)
        
    dok.save()
    
    return  {'object': obj, }
    






def gen(request, pk):
    
    obj=models.Operator.objects.get(id=pk)
    
    dok = models.DokPrzydzielenia()
    dok.parent = obj
    dok.data = datetime.datetime.now()
    dok.data_przydzial = datetime.datetime.now()
    #dok.data_przydzial = datetime.date.today()
    dok.save()
    
    dok.grupy.clear()
    
    for pos in obj.grupy.all():
        dok.grupy.add(pos)
        
    dok.save()
    
    return  HttpResponseRedirect(f'../../../../DokPrzydzielenia/{dok.pk}/edit/')
    


 
