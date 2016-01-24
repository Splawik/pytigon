#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os.path

from django.template import Template
from django.http import HttpResponse
from django.conf import settings
from django.template.base import TemplateDoesNotExist

from schlib.schfs.vfstools import get_temp_filename
from zipfile import ZipFile
import xml.dom.minidom

from schlib.schodf.odf_process import DocTransform

"""
Składnia:
    Pierwszy znak w komórce arkusza:
        * - wynik w postaci tekstowej
        : - wynik jako liczba
        @ lub $ - wynik jako formuła
    Pierwszy znak w notatce:
        !   - przeniesienie wyrażenia do poziomu aktualnej komórki 
              element przed komórką oddzielony od elementu za komórką znakiem @
              !{% for i in lista %}@{%endfor%}
        !!  - przeniesienie wyrażenia do poziomu aktualnego wiersza 
        !!! - przeniesienie wyrażenia do poziomu aktualnego arkusza
        
    W dowolnym miejscu składnia zgodna z django:
        {{zmienna}}, {% blok %} itp. 
    Dodatkowo wyrażenie: _start_ zamieniane jest na: {{
                         _end_ zamieniane jest na: }}
"""

template_dirs = getattr(settings, 'TEMPLATES')[0]['DIRS']

class DocTemplateTransform(DocTransform):
    def process_template(self, doc_str, context):
        return Template('{% load exsyntax %}' + doc_str).render(context)


def oo_dict(template_name):
    z = ZipFile(template_dirs[0] + "/" + template_name, "r")
    doc_content = z.read("content.xml")
    z.close()
    doc = xml.dom.minidom.parseString(doc_content.replace('&apos;', "'"))
    elementy = doc.getElementsByTagName("table:table")
    ret = []
    for element in elementy:
        element.getAttribute("table:name")
        ret.append((element.getAttribute("table:name"), element.getAttribute("table:name")))
    return ret

class DefaultTbl(object):
  def __init__(self):
    self.Row = -1
    self.Col = -1

  def IncRow(self, row=1):
      self.Row = self.Row+row
      #return ""
      #return self.Row

  def IncCol(self, col=1):
      self.Col = self.Col + col
      #return self.Col
      #return ""

  def SetCol(self, col):
    self.Col=col

  def SetRow(self, row):
    self.Row=row


def render_odf(
    template_name,
    dictionary=None,
    context_instance=None,
    mimetype=None,
    tabele=None,
    debug=None,
    ):


    if not 'tbl' in context_instance:
        context = { 'tbl':  DefaultTbl(), }
    else:
        context = {}

    ret2 = None

    with context_instance.push(context):
        if not 'tbl' in context_instance:
            context_instance['tbl'] = DefaultTbl()

        if template_name.__class__ in (list, tuple):
            test = False
            for tname in template_name:
                if tname[0] == '/':
                    name = tname
                    if os.path.exists(name):
                        test = True
                        break
                else:
                    for template_dir in template_dirs:
                        name = template_dir + '/' + tname
                        if os.path.exists(name):
                            test = True
                            break
                    if test:
                        break
            if not test:
                raise TemplateDoesNotExist(";".join(template_name))
        else:
            name = template_name
        name_out = get_temp_filename()
        doc = DocTemplateTransform(name, name_out)
        ret = doc.process(context_instance, debug)
        if ret != 1:
            ret2 = (None, name)
            os.remove(name_out)
        else:
            ret2 = (name_out, name)
    return ret2


def render_to_response_odf(
    template_name,
    dictionary=None,
    context_instance=None,
    mimetype=None,
    tabele=None,
    debug=None,
    ):
    s = render_odf(template_name, dictionary, context_instance, mimetype, tabele, debug)
    if not s[0]:
        response = None
    else:
        if '_' in s[1]:
            name = s[1].split('_')[1]
        else:
            name = s[1]

        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=%s'% name
        response['Content-Type'] = 'application/vnd.oasis.opendocument.spreadsheet'                        
        f = open(s[0],'rb')
        response.content = f.read()
        f.close()
        os.remove(s[0])
    return response

