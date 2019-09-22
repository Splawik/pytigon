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

from pytigon_lib.schfs.vfstools import get_temp_filename
from pytigon_lib.schdjangoext.tools import gettempdir
import  openpyxl

from crh.models import Ad

def check(val1, val2):
    if val1 == val2:
        return [val1, True]
    elif not val1:
        if val2 == '[]':
            return ["", True]
        else:
            return [val2, True]
    else:
        return [val1, False] 

PFORM = form_with_perms('config') 


class employee_import(forms.Form):
    import_file = forms.FileField(label=_('Import employes (*.xlsx)'), required=True, )
    
    def process(self, request, queryset=None):
    
        object_list = []
        data = request.FILES['import_file']
        tmp_dir = gettempdir()
        file_name = os.path.join(tmp_dir, "employees.xlsx")
        with open(file_name, "wb") as f:
            f.write(data.read())
        
        workbook = openpyxl.load_workbook(filename=file_name, read_only=True)
        worksheets = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(worksheets[0])
        lp = 0
        fields = []
        id_type = 0
        
        for row in worksheet.rows:        
            if lp==0:
                for pos in row:
                    if pos.value:
                        fields.append(str(pos.value).strip())    
                    else:
                        fields.append("X")
                if 'email' in fields:
                    id_type = 1
                    lp += 1
                    continue
                else:
                    if 'surname' in fields and 'name' in fields and 'company' in fields:
                        id_type = 2
                        continue
                    else:
                        object_list.append("Błędna struktura pliku, brak zestawu pól: email lub (name, surname, company)")
                        break
            else:
                values = []
                for pos in row:
                    if pos.value:
                        values.append(str(pos.value).strip())
                    else:
                        values.append("")
            
            lp += 1
            
            obj = {}
            i=0
            for field in fields:
                obj[field] = values[i]
                i+=1
                
            if id_type==1:
                email = obj['email']        
            else:
                if obj['name'] and obj['surname'] and obj['company']:
                    email = obj['name']+"."+obj['surname']+"@"+obj['company']+".pl"
                    email = email.lower()
                else:
                    email = ""
            
            if email and '@' in email:
                employees = models.Employee.objects.filter(email = email)
                if employees.count()>0:
                    e = employees[0]
                else:
                    e = models.Employee()
                
                for field in fields:
                    if hasattr(e, field):
                        setattr(e, field, obj[field])
                e.email = email
                e.active = True
                
                e.save()
            else:
                object_list.append("Wiersz nie został wczytany: "+ str(values) )
        
        workbook._archive.close()
        
        return { "object_list": object_list }
    

def view_employee_import(request, *argi, **argv):
    return PFORM(request, employee_import, 'config/formemployee_import.html', {})



@dict_to_template('config/v_sync.html')




def sync(request):
    
    object_list = []
    count_dict = {}
    
    users = Ad.objects.all()
    for user in users:
        email = user.mail.lower().strip()
        employees = models.Employee.objects.filter(email = email)
        if employees.count()>0:
            employee = employees[0]
        else:
            employee = models.Employee()
            
        employee.surname = user.name.split(',')[0].strip()
        try:
            employee.name = user.name.split(',')[1].strip()
        except:
            employee.name = ""
    
        employee.email = email
        employee.company = user.company
        employee.department = user.department
        employee.location = ""        
        employee.title = user.title
        if user.employeeID and user.employeeID != '[]':    
            employee.external_id = user.employeeID
        employee.postalCode = user.postalCode
        employee.city = user.l
        employee.street = user.streetAddress
        employee.telephoneNumber = user.telephoneNumber
        employee.mobile = user.mobile
        employee.manager_name = user.manager_name
        employee.active = user.active
        employee.save()
        if user.company in count_dict:
            count_dict[user.company] += 1
        else:
            count_dict[user.company] = 1
    
    for key, value in count_dict.items():
        object_list.append([key, value])
    
    return { 'object_list': object_list }
    

@dict_to_template('config/v_compare.html')




def compare(request):
    
    users = Ad.objects.all()
    object_list = []
    for user in users:
        rec = []
        if not ',' in user.displayName:
            continue
        email = user.mail.lower()
        employees = models.Employee.objects.filter(email=email)
        if employees.count()>0:
            employee = employees[0]        
            rec.append([email, True])
            rec.append(check(employee.surname+", "+employee.name, user.displayName))
            rec.append(check(employee.company, user.company))
            rec.append(check(employee.department, user.department))        
            rec.append(check(employee.title, user.title))
            rec.append(check(employee.external_id, user.employeeID))
            rec.append(check(employee.postalCode, user.postalCode))
            rec.append(check(employee.city, user.l))
            rec.append(check(employee.street, user.streetAddress))
            rec.append(check(employee.telephoneNumber, user.telephoneNumber))
            rec.append(check(employee.mobile, user.mobile))
            rec.append(check(employee.manager_name, user.manager_name))
            #object_list.append(rec)
            #print(rec)
            for pos in rec:
                if not pos[1]:
                    object_list.append(rec)
                    break
                    
    return { 'object_list': object_list }
    


 
