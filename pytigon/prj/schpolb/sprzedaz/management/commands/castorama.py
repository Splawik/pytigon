#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from sprzedaz.models import CastoramaKli, CastoramaKar, CastoramaLog, Nag, Lin

import sys
import io
import getopt
from decimal import Decimal

from io import StringIO
from html.parser import HTMLParser

import urllib.request

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.utils import set_debug_logging

from datetime import datetime, date

class StringIO2(StringIO):
    encoding = 'utf-8'


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.in_div = False
        self.div_tag = None
        self.div_txt = ""
        self.data = []
        super().__init__()
        
    def handle_starttag(self, tag, attrs):        
        if tag.lower()=='div':
            x = dict(attrs)
            if 'style' in x:
                y1 = [ str(pos).split(':') for pos in x['style'].split(';') ]
                y2 = dict([ (pos2[0].strip(), pos2[1].strip())  for pos2 in y1 if len(pos2)==2 ] )               
                top = int(y2['top'].replace('px','')) if 'width' in y2 else None
                left = int(y2['left'].replace('px','')) if 'height' in y2 else None                
            else:
                top = 0
                left = 0
            self.div_tag = (top, left)
            self.in_div = True
            self.div_txt = ""

    def handle_endtag(self, tag):
        if tag.lower()=='div':
            if self.div_tag[0] and self.div_tag[1]:
                self.data.append((self.div_tag[0], self.div_tag[1], self.div_txt.strip()))
            self.in_div = False
            
    def handle_data(self, data):
        self.div_txt += data



def convert(fp):
    showpageno = True
    
    pagenos = set()
    laparams = LAParams()
    rsrcmgr = PDFResourceManager(caching=False)
    retstr = StringIO2()
    retstr.encoding = 'utf-8'
    device = HTMLConverter(rsrcmgr, retstr, scale=1, layoutmode='normal', laparams=laparams, outdir=None, debug=False)
    
    process_pdf(rsrcmgr, device, fp, pagenos, maxpages=0, password='', caching=False, check_extractable=True)
    device.close()
    
    return  retstr.getvalue()


def getKey(item):
    return item[0]*1000+item[1]


def pdf_to_order(fp):

    x = convert(fp)

    parser = MyHTMLParser()
    parser.feed(x)

    data = sorted(parser.data, key=getKey)

    header = []
    table = []
    footer = []

    status = 0
    for pos in data:
        if status == 0:
            if pos[2] =='Total':
                status = 1
                continue
            if '\n' in pos[2]:
                pos[2].split('\n')
                for pos2 in pos[2].split('\n'):
                    header.append((pos2, pos[0], pos[1]))
            else:
                header.append((pos[2], pos[0], pos[1]))
        if status==1:
            if 'Total Zamowienia' in pos[2]:
                status = 2
                continue
            table.append((pos[2], pos[0], pos[1]))            
        if status == 2:        
            footer.append((pos[2], pos[0], pos[1]))
            
    i = 0
    lp = 1
    rows = []
    row = []
    for pos in table: 
        if len(row)==0:
            row.append(pos)
        else:
            if pos[1]==row[0][1]:
                row.append(pos)
            else:
                rows.append(row)
                row=[pos,]
    if len(row)>0:
        rows.append(row)
        
    clean_rows = []

    lp=1
    for row in rows:
        try:
            row2 = list([pos[0] for pos in row])
            
            try:
                lp2 = int(row2[0])
            except:
                lp2 = 0
            
            if lp2 != lp:
                continue
                
            lp +=1
            if len(row2)<9:
                row3 = []
                k = 0
                for pos in row2:
                    if ' ' in pos and k!=3:                        
                        for pos2 in pos.split(' '):
                            row3.append(pos2)
                    else:
                        row3.append(pos)
                    k +=1
                row2 = row3
                
            
            row2[0] = int(row2[0])
            row2[3] = row2[3].replace('\n', ' ')
            row2[4] = Decimal(row2[4])
            
            row2[6] = Decimal(row2[6])
            row2[7] = Decimal(row2[7])
            
            row2[8] = Decimal(row2[8].replace('\n', '').replace(' ',''))
        except:
            print("##################################################################")
            #for row in table:
            #    print(row)                        
            print(len(row2), row2)
            print("##################################################################")
        
        clean_rows.append(row2)
        
            

    order_id = None
    data_dok = None

    nazwa_klienta = None
    adres_klienta = None

    data_dost = None
    komentarz = None 
    adres_dostawy = None

    status = 0
    status2 = 0
    for pos in header:
        if status == 0:
            if pos[0].startswith('ORDERS'):
                order_id = pos[0].split(' ')[1]
                status = 1
                continue
        if status == 1:
            data_dok = pos[0]
            status = 2
            status2 = 0
            continue
        if status == 2:
            if status2 == 0:
                nazwa_klienta = pos[0]
                status2 = 1
            if status2 == 1:
                if pos[0].startswith('POLBRUK'):
                    status2 = 2
                    continue
            if status2 == 2:
                adres_klienta = pos[0]
                status2 = 3
                continue
            if status2 == 3:
                if pos[0].startswith('Waluta'):
                    status2 = 0
                    status = 3
                    continue
        if status == 3:
            if pos[0].startswith('Data'):
                data_dost = pos[0].replace('Data dostawy : ','')
            if pos[0].startswith('Komentarz'):
                komentarz = pos[0].replace('Komentarz :','')
            if pos[0].startswith('Adres'):
                adres_dostawy = pos[0].replace("Adres dostawy : ",'')

    clean_header = [order_id, data_dok, nazwa_klienta, adres_klienta, data_dost, komentarz, adres_dostawy]            
    
    try:
        total = Decimal(footer[0][0].replace(' ',''))
        total2 = sum([pos[8] for pos in clean_rows])
    except:
        total2 = 0
        
    if total != total2:
        print(total, total2)
    return (total == total2, clean_header, clean_rows)


def export_dok(link, row, header, table):
    print(header)
    errors = False 
    nag = Nag()
    nag.nr_zam = header[0]
    nag.data_dok = datetime.strptime(header[1], '%d/%m/%Y')
    nag.lokalizacja = header[2]
    nag.adres = header[3]
    
    d = header[4].split(' ')
    
    dzien = int(d[0])
    rok = int(d[2])
    m = ['sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'paź', 'lis', 'gru'].index(d[1][:3].lower())
    m+=1
    
    nag.data_dost =date(rok, m, dzien)
    nag.komentarz = header[5]
    nag.nr_lok_dost = header[6].split(' ')[0]
    
    lok = CastoramaKli.objects.filter(numer=nag.nr_lok_dost)
    if len(lok)==1:    
        nag.logo = lok[0].logo
        nag.mag = lok[0].mag
    else:
        errors = True
    if errors:
        nag.status = '2'
    else:
        nag.status = '5'
    
    nag.pdf_link = link
        
    nag.save()
    
    for pos in table:
        lin = Lin()
        lin.parent=nag
        lin.lp = pos[0]
        lin.castorama_kar = pos[1]
        if pos[2] and pos[2]!='???':
            lin.symkar = pos[2]
        else:
            x = CastoramaKar.objects.filter(id_castorama = pos[1])
            if len(x)==1:
                lin.symkar = x[0].id_softlab
            else:
                errors = True
        
        lin.opis = pos[3]
        lin.ilosc = pos[4]
        lin.jz = pos[5]
        lin.cena = pos[7]
        lin.netto = pos[8]
        lin.save()
        
    if errors:
        nag.status='2'
        nag.save()
    
    
def process_row(row):    
    if '.pdf' in row[3].lower():
        file_name = row[2].split('\\')[-1]    
        link = "http://10.48.241.99/castorama_files/"+file_name
        x = Nag.objects.filter(pdf_link = link)
        if len(x)==0:
            data = urllib.request.urlopen(link)
            if True:
                ok, header, table = pdf_to_order(data)
                if not ok:
                    print(header)
                    print(table)
                    raise Exception('Error') 
                else:
                    export_dok(link, row, header, table)
                    print(row[3], "OK")
            #except:
             #   print("###########################################################")
             #   print("ERROR:")
              #  print(row)
               # print("###########################################################")
               # data = urllib.request.urlopen("http://10.48.241.99/castorama_files/"+file_name)
               # f=open("error.pdf", "wb")
                #f.write(data.read())
                #f.close()
                #exit(0)

class TabHTMLParser(HTMLParser):
    def __init__(self):
        self.row = []
        self.td = ""
        super().__init__()
        
    def handle_starttag(self, tag, attrs):        
        if tag.lower()=='tr':
            self.row=[]
        if tag.lower()=='td':
            self.td=""

    def handle_endtag(self, tag):
        if tag.lower()=='td':
            self.row.append(self.td)
        
        if tag.lower()=='tr':
            process_row(self.row)
            
    def handle_data(self, data):
        self.td += data


class Command(BaseCommand):
    help = 'Scan pdf files'

    def handle(self, *args, **options):
        data = urllib.request.urlopen("http://10.48.241.99/castorama").read().decode('utf-8')
        parser = TabHTMLParser()
        parser.feed(data)

            