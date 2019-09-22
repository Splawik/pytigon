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

from ldap3 import Server, Connection, SUBTREE

def get_users(server, user, password,  ou):
    _attributes = """
        c 
        company
        co
        st 
        physicalDeliveryOfficeName 
        postalCode 
        l 
        streetAddress
        employeeID
        sAMAccountName
        displayName 
        name
        cn
        givenName
        sn
        title
        department
        distinguishedName
        userPrincipalName
        mail
        telephoneNumber
        mobile
        manager
        userAccountControl
        whenCreated
        PwdLastSet
    """
    attributes = [ attr.strip() for attr in _attributes.split('\n') if attr.strip() != "" ]
    lp = 1    
    ret = []
        
    def process_response(response):
        nonlocal lp, attributes, ret
        
        for row in response:
            mail = row["attributes"]['mail']
            if not mail:
                continue
            mail = str(mail)      
            tmp = mail.split('@')
            if len(tmp)!=2:
                continue
            if not tmp[1].lower() in ['polbruk.pl', 'masfalt.pl', 'drogomex.pl', 'crhlab.com', 'bostabeton.com.pl', 'crhpoland.com', 'ozarow.com.pl', 'trzuskawica.pl' ]:
                continue
            #if not '.' in mail:
            #    continue
            if 'ModelOffice' in mail:
                continue
            pd = row["attributes"]['physicalDeliveryOfficeName']
            #if not pd:
            #    continue

            manager = row["attributes"]['manager']
            if type(manager)==list:
                if len(manager)>0:
                    manager = manager[0]
                else:
                    manager=""
            if manager:
                x = manager.split(',')
                xx = x[0].replace('\\','').replace('CN=','') + ' ' + x[1]
            else:
                xx = ""
            
            buf = []
            for attr in attributes:
                try: 
                    tmp = str(row["attributes"][attr])
                    if tmp == '[]':
                        buf.append('')
                    else:
                        buf.append(tmp.strip())
                except:
                    buf.append('-')
            buf.append(xx)
            lp += 1
            ret.append(buf)
                
    s = Server('ldap://%s:3268' % server)
    c = Connection(s, user=user, password=password, auto_bind=True, auto_range=True)
    c.search(ou,'(&(objectclass=*))', SUBTREE, attributes = attributes, paged_size=512) 
    cookie = c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    process_response(c.response)
    while cookie:
        with c:
            c.search(ou,'(&(objectclass=*))', SUBTREE, attributes = attributes, paged_size=512, paged_cookie = cookie)
            cookie = c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            process_response(c.response)        
            
    return ret
 





@dict_to_template('crh/v_sync.html')




def sync(request):
    
    tab1 = get_users('10.157.251.71', 'ematcrh\\sa_qlickview', 'L0ngf0rd15', 'OU=Poland,OU=CRH Users,DC=EMAT,DC=CRH,DC=NET')
    tab2 = get_users('10.157.251.71', 'ematcrh\\sa_qlickview', 'L0ngf0rd15', 'OU=Disabled objects,DC=EMAT,DC=CRH,DC=NET')
    tab3 = get_users('10.48.241.40', 'crhem\SRV_PL_NEWSLETTER', 'xWz7GvZLzTFZ', 'OU=MASFALT,OU=Poland,OU=Country,DC=CRHEM,DC=PL')
    tab4 = get_users('10.48.241.40', 'crhem\SRV_PL_NEWSLETTER', 'xWz7GvZLzTFZ', 'OU=DROGOMEX,OU=Poland,OU=Country,DC=CRHEM,DC=PL')
    
    #models.Ad.objects.all().delete()    
    models.Ad.objects.all().update(active=False)
    object_list = []
    tab_names = ["emtacrh", "ematcrh/skrzynki współdzielone", "Masfalt", "Drogomex"]
    
    k = 0
    for tab in [tab1, tab2, tab3, tab4]:
        lp = 0
        if tab:
            for pos in tab:
                objs = models.Ad.objects.filter(mail=pos[19])
                if len(objs)>0:
                    obj = objs[0]
                else:
                    obj = models.Ad()
                obj.active = True
                lp+=1
                obj.c = pos[0]
                obj.company = pos[1]
                obj.co = pos[2]
                obj.st = pos[3]
                obj.physicalDeliveryOfficeName = pos[4]
                obj.postalCode = pos[5]
                obj.l = pos[6]
                obj.streetAddress = pos[7]
                obj.employeeID = pos[8]
                obj.sAMAccountName = pos[9]
                obj.displayName = pos[10]
                obj.name = pos[11]
                obj.cn = pos[12]
                obj.givenName = pos[13]
                obj.sn = pos[14]
                obj.title = pos[15]
                obj.department = pos[16]
                obj.distinguishedName = pos[17]
                obj.userPrincipalName = pos[18]
                obj.mail = pos[19]
                obj.telephoneNumber = pos[20]
                obj.mobile = pos[21]
                obj.manager = pos[22]
                obj.userAccountControl = pos[23]
                obj.whenCreated = pos[24]
                obj.PwdLastSet = pos[25]
                obj.manager_name = pos[26]
                obj.is_ok = True
                obj.save()
        object_list.append([tab_names[k], lp ])    
        k+=1
    
    return { 'object_list': object_list }
    

@dict_to_template('crh/v_errors.html')




def errors(request):
    
    object_list = models.Ad.objects.all()
    object_list.update(errors="")
    object_list = models.Ad.objects.all()
    
    for pos in object_list:
        buf = ""
        #if (not pos.mobile) or pos.mobile  == '[]':
        #     buf = "Brak telefonu mob.;"
        
        if pos.userPrincipalName.lower() != pos.mail.lower():
            buf += "UPN niezgodny z mail; "
        
        if buf:
            pos.errors = buf
            pos.save()
    
    object_error = models.Ad.objects.exclude(errors = "")
    return { 'object_list': object_error }
    

@dict_to_template('crh/v_confirm.html')




def confirm(request, **argv):
    
    pass
    


 
