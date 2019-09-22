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

import prawa.models as models_rights
from ldap3 import Server, Connection, SUBTREE

import  openpyxl
from pytigon_lib.schfs.vfstools import get_temp_filename

sel1 = """
select DomainName, DomainUserName, oper.login, mail, NazwiskoImie, log3.logdata, hostname, hier.grupa, hier.dzial, REPLACE(oddz.Nazwa1, 'KOSTKA BRUKOWA ','') as oddz from SL_VV_OPERATORBRO oper(NOLOCK)
left join 
( select username, max(logdata) logdata from SL_SECURITYLOGVIEW log(NOLOCK) where scategory = 'Audyt sukces' group by username
) log2 on log2.username = oper.login
left join SL_SECURITYLOGVIEW log3(NOLOCK) on log3.username=oper.login and log3.logdata = log2.logdata
left join SL_VV_HIERORGOPERATOR_BRO hier(NOLOCK) on hier.login = oper.login and hier.grupa like 'POLBRUK%'
left join MG_VV_ODDZIALY_HIERARCHYBRO oddz(NOLOCK) on oddz.SymOdd = oper.pd_lok
where oper.locked=0 and oper.login like '%.%' and IsNull(log3.logdata,'2000-01-01') <> '2000-01-01'
order by logdata
"""

def convert(str_in):
    x1 = 'ąćęłńóśżź'
    x2 = 'acelnoszz'
    m = list(zip(x1+x1.upper(), x2+x2.upper()))
    ret = str_in
    for pos in m:
        ret  = ret.replace(pos[0], pos[1])
    return ret
    
     

PFORM = form_with_perms('spisy') 


class RaportForm(forms.Form):
    typ_raportu = forms.ChoiceField(label=_('Typ raportu'), required=False, choices=models.TypRaportu)
    pdf = forms.BooleanField(label=_('Pdf'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        pdf = self.cleaned_data['pdf']
        typ_raportu = self.cleaned_data['typ_raportu']
        
        if typ_raportu == '1':
            ad_list = models.UserAD.objects.filter(aktywny=True)
            ad_logins = []
            for pos in ad_list:
                ad_logins.append(pos.loginname.lower())
        
            softlab_list = models.UserSoftlab.objects.filter(aktywny = True)
            tab = []
            for pos in softlab_list:
                if not pos.loginname.lower() in ad_logins:
                    tab.append([pos.loginname.lower(), pos.nazwisko_imie])
        
        
        if typ_raportu == '2':
            softlab_list = models.UserSoftlab.objects.filter(aktywny = True)
            softlab_logins = []
            for pos in softlab_list:
                softlab_logins.append(pos.loginname.lower())
        
            ad_list = models.UserAD.objects.filter(aktywny=True)
            tab = []
            for pos in ad_list:
                if not pos.loginname.lower() in softlab_logins:
                    tab.append([pos.loginname.lower(), pos.nazwisko_imie])
        
        if typ_raportu == '3':    
            rights_list = models_rights.Operator.objects.filter(aktywny=True)
            rights_logins = []
            for pos in rights_list:
                rights_logins.append(pos.login.lower())
        
            softlab_list = models.UserSoftlab.objects.filter(aktywny=True)
            tab = []
            for pos in softlab_list:
                if not pos.oldloginname.lower() in rights_logins:
                    tab.append([pos.oldloginname, pos.nazwisko_imie])
        
        
        if typ_raportu == '4':
            ad_list = models.UserAD.objects.filter(aktywny=True)
            tab = []
            
            for pos in ad_list:
                computers = pos.nowykomputer_set.all()
                if len(computers)!=1:        
                    tab.append(pos)
        
        
        if typ_raportu == '5':
            prac_list = models.UserPolbruk.objects.all()
            prac_logins = []
            for pos in prac_list:
                prac_logins.append(pos.loginname.lower())
        
            ad_list = models.UserAD.objects.filter(aktywny=True)
            tab = []
            for pos in ad_list:
                if not pos.loginname.lower() in prac_logins:
                    tab.append([pos.loginname.lower(), pos.nazwisko_imie])
        
        
        d = datetime.datetime.now().isoformat()
        
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        return { 'object_list': tab, 'typ_raportu': typ_raportu,  'date': d[:10], 'time': d[11:16], 'doc_type': doc_type }
    

def view_raportform(request, *argi, **argv):
    return PFORM(request, RaportForm, 'spisy/formraportform.html', {})


class _FilterFormNowyKomputer(forms.Form):
    nazwisko = forms.CharField(label=_('Nazwisko'), required=False, )
    hostname = forms.CharField(label=_('Hostname'), required=False, )
    
    def process(self, request, queryset=None):
    
        nazwisko = self.cleaned_data['nazwisko']
        hostname = self.cleaned_data['hostname']
        if nazwisko:
            queryset = queryset.filter(operator__nazwisko_imie__icontains=nazwisko)
        if hostname:
            queryset = queryset.filter(hostname__icontains=hostname)
        return queryset
    

def view__filterformnowykomputer(request, *argi, **argv):
    return PFORM(request, _FilterFormNowyKomputer, 'spisy/form_filterformnowykomputer.html', {})


class _FilterFormUserAD(forms.Form):
    nazwisko = forms.CharField(label=_('Nazwisko'), required=False, )
    
    def process(self, request, queryset=None):
    
        nazwisko = self.cleaned_data['nazwisko']
        if nazwisko:
            queryset = queryset.filter(nazwisko_imie__icontains=nazwisko)
        return queryset
    

def view__filterformuserad(request, *argi, **argv):
    return PFORM(request, _FilterFormUserAD, 'spisy/form_filterformuserad.html', {})


class _FilterFormUserSoftlab(forms.Form):
    nazwisko = forms.CharField(label=_('Nazwisko'), required=False, )
    
    def process(self, request, queryset=None):
    
        nazwisko = self.cleaned_data['nazwisko']
        if nazwisko:
            queryset = queryset.filter(nazwisko_imie__icontains=nazwisko)
        return queryset
    

def view__filterformusersoftlab(request, *argi, **argv):
    return PFORM(request, _FilterFormUserSoftlab, 'spisy/form_filterformusersoftlab.html', {})


class ImportPracForm(forms.Form):
    prac_file = forms.FileField(label=_('Plik z listą pracowników'), required=True, )
    
    def process(self, request, queryset=None):
    
        return {}
    
    def render_to_response(self, request, template, context_instance):
        print("X1")
        qlikviewdata= request.FILES['prac_file']
        data = qlikviewdata.read()
    
        file_name = get_temp_filename("temp.xlsx")
        
        plik = open(file_name, 'wb')
        plik.write(data)
        plik.close()
        print("X2")
        
        workbook = openpyxl.load_workbook(filename=file_name, read_only=True)
        worksheets = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(worksheets[0])
        print("X3")
        
        models.UserPolbruk.objects.all().delete()      
        print("X4")
        
        for row in list(worksheet.rows)[1:]:
            try:
                print("<")
                obj = models.UserPolbruk()
                obj.loginname = (convert(row[2].value)[0]+convert(row[3].value)).lower()
                obj.imie = row[2].value
                obj.nazwisko = row[3].value
                #oddz = row[0].value
                #if oddz:
                #    oddz = str(oddz)
                #    if len(oddz)==2:
                #       obj.oddz = oddz
                obj.oddz = row[0].value
                obj.dzial = row[4].value
                print(">")
                obj.save()
                print(">")
            except:
                pass
        print("END")
        return HttpResponseRedirect("../../table/UserPolbruk/-/form/list?schtml=1")
        

def view_importpracform(request, *argi, **argv):
    return PFORM(request, ImportPracForm, 'spisy/formimportpracform.html', {})








def synchr_ad(request):
    
    _attributes = """
    sAMAccountName
    uid
    department
    displayName
    distinguishedName
    employeeID
    givenName
    name
    physicalDeliveryOfficeName
    mail
    manager
    postalCode
    st
    streetAddress
    telephoneNumber
    title
    whenCreated
    cn
    l
    """
    
    attributes = [ attr.strip() for attr in _attributes.split('\n') if attr.strip() != "" ]
    
    def _attr(_row, name):
        if name in _row["attributes"]:
            if _row["attributes"][name]:
                return _row["attributes"][name]
            else:
                return ""
        else:
            return ""
    
    s = Server('ldap://10.157.251.71:3268')
    c = Connection(s, user='ematcrh\\sa_qlickview', password='L0ngf0rd15', auto_bind=True)
    with c:
        c.search('OU=Polbruk,OU=Poland,OU=CRH Users,DC=EMAT,DC=CRH,DC=NET','(&(objectclass=*))', SUBTREE, attributes = attributes)
        models.UserAD.objects.all().update(aktywny=False)
        for row in c.response:
            if 'displayName' in row["attributes"]:
                displayName = row["attributes"]["displayName"]
                if len(displayName)>0 and ( ',' not in displayName or 'polbruk' in displayName.lower() or 'poland' in displayName.lower() or 'dzial' in displayName.lower()):
                    continue
            else:
                continue
    
            if 'sAMAccountName' in row["attributes"] and len(row['attributes']['sAMAccountName'])>0:
                loginname = row["attributes"]['sAMAccountName']
                users = models.UserAD.objects.filter(loginname=loginname)
    
                if len(users)>0:
                    user = users[0]
                else:
                    user = models.UserAD()
                    user.loginname = loginname
    
                user.employee_id = _attr(row, 'employeeID')
                user.nazwisko_imie = _attr(row, 'displayName').replace(',', '')
                user.dzial = _attr(row, 'department')
                user.lokalizacja = _attr(row, 'physicalDeliveryOfficeName')
                user.mail = _attr(row, 'mail')
                try:
                    szef = _attr(row, 'manager').split('OU').split('CN=')[1].replace(',','').replace('\\','')
                except:
                    szef = None
                user.szef = szef
                user.adres = _attr(row, 'postalCode') + " " + _attr(row, 'l')+" "+ _attr(row, 'streetAddress')
                user.tel = _attr(row, 'telephoneNumber')
                user.tytul = _attr(row, 'title')[:63]
                #user.data_start =datetime.datetime.strptime(_attr(row, 'whenCreated')[:8], "%Y%m%d").date()
                user.data_start =_attr(row, 'whenCreated')
                user.aktywny = True
    
                user.save()
    
    return redirect("ok")
    






def synchr_softlab(request):
    
    with settings.DB as db:
        db.execute(sel1)
        ret=db.fetchall()
    
    models.UserSoftlab.objects.all().update(aktywny=False)
    
    for pos in ret:
        login = pos[2]
        operatorzy = models.UserSoftlab.objects.filter(oldloginname=login)
        if len(operatorzy)>0:
            operator=operatorzy[0]
        else:
            operator=models.UserSoftlab()
            operator.oldloginname = login
    
        operator.loginname = pos[1]
        operator.nazwisko_imie = pos[4]
        operator.domena = pos[0]
        operator.ostatnie_logowanie = pos[5]
        operator.ostatni_komputer = pos[6]
        operator.grupa = pos[7]
        
        if pos[8]:
            operator.dzial = pos[8][:63]
        else:
            operator.dzial = ""
            
        if pos[9]:
            operator.oddzial = pos[9][:63]
        else:
            operator.oddzial = ""
            
        operator.aktywny = True
        
        operator.save()
    return redirect("ok")
    






def synchr_komp(request):
    
    laptop = models.TypKomputera.objects.filter(nazwa='Laptop standard')[0]
    desktop = models.TypKomputera.objects.filter(nazwa='Desktop')[0]
    ad_list = models.UserAD.objects.filter(aktywny=True)
    for obj in models.NowyKomputer.objects.all():
        obj.aktywny = False
    for ad_user in ad_list:
        loginname = ad_user.loginname.lower()
        softlab_list = models.UserSoftlab.objects.filter(loginname=loginname)    
        if len(softlab_list)>0:
            s_user=softlab_list[0]
            hostname = s_user.ostatni_komputer
            if hostname and hostname[0]=='L' or hostname[0]=='D':
                komputery = models.NowyKomputer.objects.filter(hostname=hostname)
                if len(komputery)>0:
                    if len(komputery)>1:
                        x = len(komputery)
                        k = komputery[x-1]
                        for i in range(0,x-1):
                            komputery[i].delete()
                    else:
                        k = komputery[0]
                else:
                    k = models.NowyKomputer()                
                    k.hostname = hostname
                    
                if hostname[0]=='L':
                    k.typ_komputera = laptop
                else:
                    k.typ_komputera = desktop           
                k.operator = ad_user
                k.aktywny=True
                k.save()
    
    return redirect("ok")
    


 
