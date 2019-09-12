#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2019 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

from lxml import etree

def make_update_filter_fun(cache_field_name, pivot_table_name, pivot_field_name, value):
        def _update_filter(doc_transform, root):
            nonlocal cache_field_name, pivot_table_name, pivot_field_name, value            
            fields = root.findall('.//cacheFields/cacheField', namespaces=root.nsmap)        
            tab = []
            for field in fields:
                if 'name' in field.attrib and field.attrib['name'] == cache_field_name:
                    s = field.findall('.//sharedItems', namespaces=root.nsmap)        
                    for pos in s:
                        for pos2 in pos:
                            tab.append(pos2.attrib.get('v', ""))
                    break
                        
            try:
                id = tab.index(value)
            except:
                id = -1
                    
            if id>=0:
                xml_name = pivot_table_name
                ret = doc_transform.get_xml_content(xml_name)
                root2 = ret['data']
                #content = doc_transform.zip_file.read(xml_name)
                #root2 = etree.XML(content)
                fields2 = root2.findall('.//pivotFields/pivotField', namespaces=root2.nsmap)
                for field2 in fields2:
                    if 'name' in field2.attrib and field2.attrib['name'] == pivot_field_name:
                        items = field2.findall('.//items/item', namespaces=root2.nsmap)
                        for item in items:
                            if 'x' in item.attrib:                                
                                if int(item.attrib['x']) == id:
                                    if 'h' in item.attrib:
                                        del item.attrib['h']                                    
                                else:
                                    item.attrib['h'] = '1'
                        break
                if not ret['from_cache']:
                    doc_transform.to_update.append( (xml_name, root2), )
            
            return False
            
        return _update_filter

def make_group_fun(pivot_field_no, values_on):
    def _update_group(doc_transform, root):
        nonlocal pivot_field_no, values_on
        values_tab = values_on.split(';')
        fields = root.findall('.//pivotFields/pivotField', namespaces=root.nsmap)
        field = fields[pivot_field_no]
        items = field.findall(".//item", root.nsmap)
        for item in items:
            if 'n' in item.attrib and item.attrib['n'] in values_tab:
                if 'sd' in item.attrib:
                    del item.attrib['sd']
            else:
                item.attrib['sd'] = '0'                    
        return True
    
    return _update_group
