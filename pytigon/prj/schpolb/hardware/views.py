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

import sqlite3 










def raport_domena_softlab(request):
    
    with settings.DB as db:
        db.execute('select * from wusr_SprzetKomputerowy komp(NOLOCK)')
        softlab_tab=list(db.fetchall())
    
    p = os.path.expanduser("~")
    db_name = os.path.join(p, "inw.db")
        
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM computers where ADPath like '%%POLBRUK%%' ")
    inw_tab=list(c.fetchall())
    conn.close()
    
    html_ret = "<html><body><table border='1'>"
    
    first_row =  True
    
    for row in softlab_tab:
        if first_row:
            i=0
            for pos in row:
                html_ret += "<td>%d</td>" % i
                i+=1
            first_row = False
            
        html_ret += "<tr>"
        for pos in row:
            html_ret += "<td>%s</td>" % str(pos)
        html_ret += "</tr>"
    
    html_ret += "</table><table border='1'>"
    
    first_row =  True
    
    for row in inw_tab:
        if first_row:
            i=0
            for pos in row:
                html_ret += "<td>%d</td>" % i
                i+=1
            first_row = False
            
        html_ret += "<tr>"
        for pos in row:
            html_ret += "<td>%s</td>" % str(pos)
        html_ret += "</tr>"
    
    html_ret += "</table><table border='1'>"
    
    inw_dict = {}
    
    for row in inw_tab:
        key = str(row[16]).upper().replace(' ','') #2
        key2 = str(row[2]).upper().replace(' ','') #2
        inw_dict[key] = row
        inw_dict[key2] = row
    
    
    softlab_dict = {}
    
    for row in softlab_tab:
        key = str(row[30]).upper().replace(' ','') #8
        key2 = str(row[8]).upper().replace(' ','') #8
        softlab_dict[key] = row
        softlab_dict[key2] = row
    
    lp = 1
    
    for row in softlab_tab:
        key = str(row[30]).upper().replace(' ','') #8
        key2 = str(row[8]).upper().replace(' ','') #8
        if key in inw_dict or key2 in inw_dict:
            pass
        else:        
            html_ret += "<tr>"
            html_ret += "<td>%d</td><td>%s</td><td>%s</td>" % (lp, key, key2)
            html_ret += "</tr>"
            lp+=1
            
    html_ret += "</table><table border='1'>"
    
    lp = 1
    
    for row in inw_tab:
        key = str(row[16]).upper().replace(' ','') #2
        key2 = str(row[2]).upper().replace(' ','') #2
        if key in softlab_dict or key2 in softlab_dict:
            pass
        else:        
            html_ret += "<tr>"
            html_ret += "<td>%d</td><td>%s</td><td>%s</td>" % (lp, key, key2)
            html_ret += "</tr>"
            lp+=1
    
    html_ret += "</table></body></html>"
    
    return HttpResponse(html_ret)
    


 
