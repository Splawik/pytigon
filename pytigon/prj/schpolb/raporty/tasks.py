#!/usr/bin/python

# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty

from asgiref.sync import sync_to_async
from applib.raporty.send_report import gen_report
from schreports.models import CommonGroup
from multiprocessing import Process

import logging
logger = logging.getLogger("pytigon_task")

def _send_reports(schedule_str):
    reports = CommonGroup.objects.filter(group_def_name='SimpleReport')
    if len(reports)>0:
        x = schedule_str.strip().split('.')[0]
        for report in reports:            
            test = False
            try:
                test = report.json_schedule.strip().startswith(x+".")
            except:
                continue
            if test:
                try:
                    gen_report(report.title)                    
                except:
                    logger.exception(f"Report error: {report.title}")
                    pass
    
async def send_reports(schedule_str):
    p = Process(target=_send_reports, args=(schedule_str,))
    p.start()
    
async def manage_send_mail(cmd):
    #await cmd("send_mail")
    p = Process(target=cmd, args=("send_mail",))
    p.start()
        
async def manage_castorama(cmd):
    #await cmd("castorama")
    p = Process(target=cmd, args=("castorama",))
    p.start()

async def gen(http, id,):
    param = { 'id': id }
    href = "/raporty/table/Raporty/action/gen/"
    #await http.post(None, href, param)    
    p = Process(target=http.post, args=(None, href, param,))
    p.start()
    
    
async def gen2(http):
    href = "/raporty/table/Raporty/action/gen2/"
    #await http.post(None, href, param)
    p = Process(target=http.post, args=(None, href, param,))
    p.start()


def init_schedule(scheduler, cmd, http):            
    scheduler.add_task("in_minute_intervals()", manage_send_mail, cmd=cmd)
        
    scheduler.add_task("in_minute_intervals(period=15)", manage_castorama, cmd=cmd)    
        
    scheduler.add_task("monthly(day=4, at='22:45')", gen2, http=http)

    scheduler.add_task("in_minute_intervals(period=5, in_weekdays=range(0,5), in_hours=range(5,17))", send_reports,  "1. Co 5 min w dni robocze")
    scheduler.add_task("in_minute_intervals(period=15, in_weekdays=range(0,5), in_hours=range(5,17))", send_reports,  "2. Co 15 min w dni robocze")
    scheduler.add_task("hourly(at='15', in_weekdays=range(0,5), in_hours=range(5,17));hourly(at='45', in_weekdays=range(0,5), in_hours=range(5,17))", send_reports,  "3. Co pÃ³Å‚ godziny w dni robocze")
    scheduler.add_task("hourly(in_weekdays=range(0,5), in_hours=range(5,17))", send_reports,  "4. Co godzinÄ™ w dni robocze")
    scheduler.add_task("daily(at='22:30', in_weekdays=range(0,5))", send_reports,  "5. Coddziennie w dni robocze")
    scheduler.add_task("monthly(day=1, at='22:35')", send_reports,  "6. Dwa razy w miesiÄ…cu")
    scheduler.add_task("monthly(day=15, at='22:35')", send_reports,  "6. Dwa razy w miesiÄ…cu")
    scheduler.add_task("monthly(day=7, at='22:40')", send_reports,  "7. Raz w miesiÄ…cu")
    scheduler.add_task("monthly(day=31, at='22:45', in_months=(3,6,9,12) )", send_reports,  "8. Raz w kwartale")
    scheduler.add_task("monthly(day=31, at='22:50', in_months=(6,12) )", send_reports,  "9. Raz na pÃ³Å‚ roku")
    scheduler.add_task("monthly(day=31, at='22:55', in_months=(12,) )", send_reports,  "10. Raz do roku")
    scheduler.add_task("in_minute_intervals(period=5)", send_reports,  "11. Co 5 min - takÅ¼e w dni wolne")
    scheduler.add_task("in_minute_intervals(period=15)", send_reports,  "12. Co 15 min - takÅ¼e w dni wolne")
    scheduler.add_task("hourly(at='15');hourly(at='45')", send_reports,  "13. Co pÃ³Å‚ godziny - takÅ¼e w dni wolne")
    scheduler.add_task("hourly()", send_reports,  "14. Co godzinÄ™ - takÅ¼e w dni wolne")    
    scheduler.add_task("daily(at='22:30')", send_reports,  "15. Codziennie - takÅ¼e w dni wolne") 
    scheduler.add_task("daily(at='23:00', in_weekdays=(6,))", send_reports,  "16. Raz w tygodniu")
    
 


def send_raports(cproxy, *args, **kwargs):
    
    pass
    return 0
    


 
