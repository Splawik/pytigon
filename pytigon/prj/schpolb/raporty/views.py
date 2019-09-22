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

import datetime
import calendar
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.db import connection
import requests 
from pytigon_lib.schparser.html_parsers import SimpleTabParserBase

from pytigon_lib.schdjangoext.tools import gettempdir
from pytigon_lib.schfs.vfstools import get_temp_filename
from pytigon_lib.schdjangoext.spreadsheet_render import render_to_response_odf
from pytigon_lib.schviews.viewtools import render_to_response_ext
from pytigon_lib.schdjangoext.spreadsheet_render import render_odf

from schreports.models import CommonGroup
from applib.raporty.send_report import gen_report



WYKLUCZ = ('580',)
OBR_WN_MA = ( )
OBR_WN = ( '5',)
OBR_MA = ('7',)
SALDO_WN = ( )
SALDO_MA = ( '0', '1', '2', '3', '6', '8', '9')

def typ_salda_dla_konta(knt):
    for f in WYKLUCZ:
        if knt.startswith(f):
            return 0
    for f in OBR_WN_MA:
        if knt.startswith(f):
            return 1
    for f in OBR_WN:
        if knt.startswith(f):
            return 2
    for f in OBR_MA:
        if knt.startswith(f):
            return 3
    for f in SALDO_WN:
        if knt.startswith(f):
            return 4
    for f in SALDO_MA:
        if knt.startswith(f):
            return 5
    return 0

def not_null(l):
    if not l:
        return 0
    else:
        return l

def not_null_str(l):
    if not l:
        return ""
    else:
        return l

BGCOLOR = ('#fff','#eee','#ddd', '#ccc', '#bbb', '#aaa', '#999', '#888', '#777', '#866', '#A66')

sel_wiekowanie = """
select stany2.Mag, stany2.SymKar, stany2.SymCech, stany2.OpiKar, stany2.Stan, 
IIF(k30>0, k30, 0) k30,
IIF(k90>0, k90, 0) k90,
IIF(k180>0, k180, 0) k180,
IIF(k365>0, k365, 0) k365,
IIF(k547>0, k547, 0) k547,
IIF(k730>0, k730, 0) k730,
IIF(kend>0, kend, 0) kend,
stany2.JM,
stany2.pd_typ,
IIF(BZIl is not null, BZWar/BZIl, 0) cena,
case when RodzajHandlowy = 'PRODUKT' then IsNull(Waga,0)/180 else 0 end as przelicz
from
(    select Mag, SymKar, SymCech, OpiKar, Stan, 
    IIF(k30<Stan, k30, Stan) k30,
    IIF(k30+k90<Stan, k90, Stan-k30) k90,
    IIF(k30+k90+k180<Stan, k180, Stan-k30-k90) k180,
    IIF(k30+k90+k180+k365<Stan, k365, Stan-k30-k90-k180) k365,
    IIF(k30+k90+k180+k365+k547<Stan, k547, Stan-k30-k90-k180-k365) k547,
    IIF(k30+k90+k180+k365+k547+k730<Stan, k730, Stan-k30-k90-k180-k365-k547) k730,
    Stan-k30-k90-k180-k365-k547-k730 kend,
    stany.JM,
    stany.pd_typ
    from
    (   select obr.Mag Mag, obr.SymKar SymKar, obr.SymCech SymCech, kar.OpiKar OpiKar, 
        sum ( obr.CIloscMG ) Stan,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k30,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k90,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k180,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k365,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k547,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k730,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) >= %d then CIloscMG else 0 end ) kend,
        kar.JM,
        kar.pd_typ
        from W_MG_VV_OBRCECHMAGAZYNOWE obr(NOLOCK)
        left join mg_kar kar(NOLOCK) on kar.symkar = obr.SymKar
        where obr.Status > 0 and kar.IsUsluga=0 and obr.Mag like '%s' and %s and kar.RodzajHandlowy %s and  kar.pd_typ like '%s' and obr.Data <= GetDate()
        group by obr.Mag, obr.SymKar, obr.SymCech, kar.OpiKar, kar.JM, kar.pd_typ
    ) stany
    where stany.Stan > 0 and ( mag like '__' or mag like '[1234]__')
) stany2
left join W_MG_FN_OBROTYKARWOKRESIE(GetDate(), GetDate()) obr2 on  obr2.mag = stany2.mag and obr2.symkar = stany2.symkar and BZIl > 0
left join mg_jm jm(NOLOCK) on jm.symkar = stany2.symkar and jm.handlowa = 1 and jm.Waga > 0
order by Mag, SymKar, SymCech
"""

sel_wiekowanie5 = """
select stany2.Mag, stany2.SymKar, stany2.SymCech, stany2.OpiKar, stany2.Stan, 
IIF(k30>0, k30, 0) k30,
IIF(k60>0, k60, 0) k60,
IIF(k90>0, k90, 0) k90,
IIF(k120>0, k120, 0) k120,
IIF(k150>0, k150, 0) k150,
IIF(k180>0, k180, 0) k180,
IIF(k210>0, k210, 0) k210,
IIF(k240>0, k240, 0) k240,
IIF(k270>0, k270, 0) k270,
IIF(k300>0, k300, 0) k300,
IIF(k330>0, k330, 0) k330,
IIF(k365>0, k365, 0) k365,
IIF(k547>0, k547, 0) k547,
IIF(k730>0, k730, 0) k730,
IIF(kend>0, kend, 0) kend,
stany2.JM,
stany2.pd_typ,
IIF(BZIl is not null, BZWar/BZIl, 0) cena,
case when RodzajHandlowy = 'PRODUKT' then IsNull(Waga,0)/180 else 0 end as przelicz
from
(    select Mag, SymKar, SymCech, OpiKar, Stan, 
    IIF(k30<Stan, k30, Stan) k30,
    IIF(k30+k60<Stan, k60, Stan-k30) k60,
    IIF(k30+k60+k90<Stan, k90, Stan-k30-k60) k90,
    IIF(k30+k60+k90+k120<Stan, k120, Stan-k30-k60-k90) k120,
    IIF(k30+k60+k90+k120+k150<Stan, k150, Stan-k30-k60-k90-k120) k150,
    IIF(k30+k60+k90+k120+k150+k180<Stan, k180, Stan-k30-k60-k90-k120-k150) k180,
    IIF(k30+k60+k90+k120+k150+k180+k210<Stan, k210, Stan-k30-k60-k90-k120-k150-k180) k210,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240<Stan, k240, Stan-k30-k60-k90-k120-k150-k180-k210) k240,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240+k270<Stan, k270, Stan-k30-k60-k90-k120-k150-k180-k210-k240) k270,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240+k270+k300<Stan, k300, Stan-k30-k60-k90-k120-k150-k180-k210-k240-k270) k300,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240+k270+k300+k330<Stan, k330, Stan-k30-k60-k90-k120-k150-k180-k210-k240-k270-k300) k330,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240+k270+k300+k330+k365<Stan, k365, Stan-k30-k60-k90-k120-k150-k180-k210-k240-k270-k300-k330) k365,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240+k270+k300+k330+k365+k547<Stan, k547, Stan-k30-k60-k90-k120-k150-k180-k210-k240-k270-k300-k330-k365) k547,
    IIF(k30+k60+k90+k120+k150+k180+k210+k240+k270+k300+k330+k365+k547+k730<Stan, k730, Stan-k30-k60-k90-k120-k150-k180-k210-k240-k270-k300-k330-k365-k547) k730,    
    Stan-(k30+k60+k90+k120+k150+k180+k210+k240+k270+k300+k330+k365+k547+k730) kend,    
    stany.JM,
    stany.pd_typ
    from
    (   select obr.Mag Mag, obr.SymKar SymKar, obr.SymCech SymCech, kar.OpiKar OpiKar, 
        sum ( obr.CIloscMG ) Stan,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k30,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k60,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k90,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k120,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k150,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k180,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k210,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k240,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k270,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k300,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k330,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k365,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k547,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k730,
        sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) >= %d then CIloscMG else 0 end ) kend,
        kar.JM,
        kar.pd_typ
        from W_MG_VV_OBRCECHMAGAZYNOWE obr(NOLOCK)
        left join mg_kar kar(NOLOCK) on kar.symkar = obr.SymKar
        where obr.Status > 0 and kar.IsUsluga=0 and obr.Mag like '%s' and %s and kar.RodzajHandlowy %s and  kar.pd_typ like '%s' and obr.Data <= GetDate()
        group by obr.Mag, obr.SymKar, obr.SymCech, kar.OpiKar, kar.JM, kar.pd_typ
    ) stany
    where stany.Stan > 0
) stany2
left join W_MG_FN_OBROTYKARWOKRESIE(GetDate(), GetDate()) obr2 on  obr2.mag = stany2.mag and obr2.symkar = stany2.symkar and BZIl > 0
left join mg_jm jm(NOLOCK) on jm.symkar = stany2.symkar and jm.handlowa = 1 and jm.Waga > 0
left join POLBRUK_PROD.dbo.mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) ON gn.gniazdo = stany2.SymCech
where (stany2.Mag like '__' or stany2.Mag like '[1234]__') and stany2.Mag <> gn.Mag and gn.Mag is not NULL
order by Mag, SymKar, SymCech
"""


sel_wiekowanie2 = """
select stany2.Mag, stany2.SymKar, stany2.OpiKar, stany2.Stan, 
IIF(k30>0, k30, 0) k30,
IIF(k90>0, k90, 0) k90,
IIF(k180>0, k180, 0) k180,
IIF(k365>0, k365, 0) k365,
IIF(k547>0, k547, 0) k547,
IIF(k730>0, k730, 0) k730,
IIF(kend>0, kend, 0) kend,
stany2.JM,
stany2.pd_typ,
IIF(BZIl is not null, BZWar/BZIl, 0) cena,
case when RodzajHandlowy = 'PRODUKT' then IsNull(Waga,0)/180 else 0 end as przelicz
from
(    select Mag, SymKar, OpiKar, Stan, 
    IIF(k30<Stan, k30, Stan) k30,
    IIF(k30+k90<Stan, k90, Stan-k30) k90,
    IIF(k30+k90+k180<Stan, k180, Stan-k30-k90) k180,
    IIF(k30+k90+k180+k365<Stan, k365, Stan-k30-k90-k180) k365,
    IIF(k30+k90+k180+k365+k547<Stan, k547, Stan-k30-k90-k180-k365) k547,
    IIF(k30+k90+k180+k365+k547+k730<Stan, k730, Stan-k30-k90-k180-k365-k547) k730,
    Stan-k30-k90-k180-k365-k547-k730 kend,
    stany.JM,
    stany.pd_typ
    from
    (   select Mag, SymKar, OpiKar, sum(Stan) Stan, sum(k30) k30, sum(k90) k90, sum(k180) k180, sum(k365) k365, sum(k547) k547, sum(k730) k730, sum(kend) kend, JM, pd_typ
        from
        (   select obr.Mag Mag, obr.SymKar SymKar, obr.SymCech SymCech, kar.OpiKar OpiKar, 
            sum ( obr.CIloscMG ) Stan,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d  AND %d then CIloscMG else 0 end )  k30,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k90,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k180,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k365,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k547,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k730,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) >= %d then CIloscMG else 0 end ) kend,
            kar.JM,
            kar.pd_typ
            from W_MG_VV_OBRCECHMAGAZYNOWE obr(NOLOCK)
            left join mg_kar kar(NOLOCK) on kar.symkar = obr.SymKar
            where obr.Status > 0 and kar.IsUsluga=0 and obr.Mag like '%s' and %s and kar.RodzajHandlowy %s and kar.pd_typ like '%s' and obr.Data <= GetDate()
            group by obr.Mag, obr.SymKar, obr.SymCech, kar.OpiKar, kar.JM, kar.pd_typ, kar.RodzajHandlowy
        ) stany0
        group by stany0.Mag, stany0.SymKar, stany0.OpiKar, stany0.JM, stany0.pd_typ
    ) stany
    where stany.Stan > 0 and (mag like '__' or mag like '[1234]__')
) stany2
left join W_MG_FN_OBROTYKARWOKRESIE(GetDate(), GetDate()) obr2 on  obr2.mag = stany2.mag and obr2.symkar = stany2.symkar and BZIl > 0
left join mg_jm jm(NOLOCK) on jm.symkar = stany2.symkar and jm.handlowa = 1 and jm.Waga > 0
order by Mag, SymKar
"""

sel_wiekowanie3 = """
select stany2.SymKar, stany2.OpiKar, stany2.Stan,
IIF(k30>0, k30, 0) k30,
IIF(k90>0, k90, 0) k90,
IIF(k180>0, k180, 0) k180,
IIF(k365>0, k365, 0) k365,
IIF(k547>0, k547, 0) k547,
IIF(k730>0, k730, 0) k730,
IIF(kend>0, kend, 0) kend,
stany2.JM,
stany2.pd_typ,
IIF(BZIl is not null, BZWar/BZIl, 0) cena,
case when RodzajHandlowy = 'PRODUKT' then IsNull(Waga,0)/180 else 0 end as przelicz
from
(   select SymKar, OpiKar, Stan,
    BZIl, BZWar,
    IIF(k30<Stan, k30, Stan) k30,
    IIF(k30+k90<Stan, k90, Stan-k30) k90,
    IIF(k30+k90+k180<Stan, k180, Stan-k30-k90) k180,
    IIF(k30+k90+k180+k365<Stan, k365, Stan-k30-k90-k180) k365,
    IIF(k30+k90+k180+k365+k547<Stan, k547, Stan-k30-k90-k180-k365) k547,
    IIF(k30+k90+k180+k365+k547+k730<Stan, k730, Stan-k30-k90-k180-k365-k547) k730,
    Stan-k30-k90-k180-k365-k547-k730 kend,
    stany.JM,
    stany.pd_typ,
    RodzajHandlowy
    from
    (

      select SymKar, OpiKar, Sum(BZIl) * Sum(Wartosc) / Sum(Stan) BZWar, sum(BZIl) BZIl,
      sum(Stan) Stan, sum(k30) k30, sum(k90) k90, sum(k180) k180, sum(k365) k365, sum(k547) k547, sum(k730) k730, sum(kend) kend, JM, pd_typ, RodzajHandlowy
      from
      (
        select stany0.mag,
        stany0.SymKar, stany0.OpiKar,
        sum(BZWar) BZWar,
        sum(BZIl) BZIl,
        sum(Stan) Stan, sum(k30) k30, sum(k90) k90, sum(k180) k180, sum(k365) k365, sum(k547) k547, sum(k730) k730, sum(kend) kend, stany0.JM, stany0.pd_typ,
        stany0.RodzajHandlowy,
        sum(Stan) * sum(BZWar) / sum(BZIl) Wartosc
        from
        (   select obr.Mag Mag, obr.SymKar SymKar, obr.SymCech SymCech, kar.OpiKar OpiKar,
            sum ( obr.CIloscMG ) Stan,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k30,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k90,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end )  k180,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k365,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k547,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) BETWEEN %d AND %d then CIloscMG else 0 end ) k730,
            sum ( case when (( obr.pr > 0 AND CIloscMG > 0 and obr.rd not like 'MP%%' ) or obr.rd like 'BZ%%' ) and DATEDIFF(day, obr.Data, GetDate()) >= %d then CIloscMG else 0 end ) kend,
            kar.JM,
            kar.pd_typ,
            kar.RodzajHandlowy
            from W_MG_VV_OBRCECHMAGAZYNOWE obr(NOLOCK)
            left join mg_kar kar(NOLOCK) on kar.symkar = obr.SymKar
            where obr.Status > 0 and kar.IsUsluga=0 and obr.Mag like '%s' and %s and kar.RodzajHandlowy %s and kar.pd_typ like '%s' and obr.Data <= GetDate()
            group by obr.Mag, obr.SymKar, obr.SymCech, kar.OpiKar, kar.JM, kar.pd_typ, kar.RodzajHandlowy
        ) stany0
        left join W_MG_FN_OBROTYKARWOKRESIE(GetDate(), GetDate()) obr2 on  obr2.mag = stany0.mag and obr2.symkar = stany0.symkar and BZIl > 0
        where stany0.mag like '__' or stany0.mag like '[1234]__'
        group by stany0.mag, stany0.SymKar, stany0.OpiKar, stany0.JM, stany0.pd_typ, stany0.RodzajHandlowy
    )
    stany_pom
    group by SymKar, OpiKar,JM, pd_typ, RodzajHandlowy
    ) stany
    where stany.Stan > 0
) stany2
left join mg_jm jm(NOLOCK) on jm.symkar = stany2.symkar and jm.handlowa = 1 and jm.Waga > 0
order by SymKar
"""

sel_wiekowanie4 = """
select top 1000
DATEDIFF(day, obr.Data, GetDate()) WiekDni, 
obr.data, obr.Numer, obr.Mag Mag, obr.SymKar SymKar, obr.SymCech SymCech, kar.OpiKar OpiKar, obr.CIloscMG Ilosc,
obr.JM
from W_MG_VV_OBRCECHMAGAZYNOWE obr(NOLOCK)
left join mg_kar kar(NOLOCK) on kar.symkar = obr.SymKar
where (( obr.pr > 0 AND CIloscMG > 0 %s) or obr.rd like 'BZ%%' ) and obr.Status > 0 and kar.IsUsluga=0 
      and obr.Mag like '%s' and obr.SymKar = '%s' and obr.SymCech like '%s'
      and obr.Data <= GetDate()
order by obr.Data desc, obr.Mag, obr.SymCech, obr.RD desc
"""

__sel_salda1="""
select Konto, Opis, Rodzaj, Rozrachunkowe, Bilansowe, Dwustronne, Klasyfikowane, level
FROM dbo.fk7_Konta as s(NOLOCK) 
WHERE s.Rok = %s and s.Bilansowe=1 and
(   (left(konto, 3) in ('012', '290') and Rozrachunkowe=0 and level=1) or
    (left(konto, 3) not in ('012', '290') and Rozrachunkowe=0 and level=2 )  or
    (Rozrachunkowe=1 and level=1)
) 
order by Konto
"""

sel_salda1="""
select Konto, Opis, Rodzaj, Rozrachunkowe, Bilansowe, Dwustronne, Klasyfikowane, level
FROM dbo.fk7_Konta as s(NOLOCK) 
WHERE s.Rok = %s and s.Bilansowe=1  and (  (Rozrachunkowe=1 and level=1) or ( not Rozrachunkowe=1 and czynne=1) ) 
order by Konto
"""


sel_salda2="""
EXEC dbo.fk7_saldaokresprc_wrap @maska_rok = %d, @maska_konto = '%s', @maska_symwl = '%%', @maska_bil = 1, @maska_pbil = 1
"""
sel_salda3="""
SELECT rok, nr, 
    obrotywn, obrotyma, obrotywnsum, obrotymasum, saldown, saldoma, saldownsum, saldomasum, 
    obrotywnwtbo, obrotymawtbo, obrotywnsumwtbo, obrotymasumwtbo, saldownsumwtbo, saldomasumwtbo, saldownwtbo, saldomawtbo,
    konto, symwl 
FROM dbo.fk7_vv_saldaobrotyokres as s(NOLOCK) 
where nr = %d
"""
sel_salda4="""
select * from dbo.fk7_fn_SloSaldaObrotyGniazda(default,%d,%d,default,default,   '%s',default,default,default,default,default,default,   '%s','%s',default,default,default,default,default,default,default,default) 
"""

sel_transport1 = """
select PD_OpisMagazynu as Magazyn, Nazwa1 as Nazwa, max(NazPrzew) as NazwaPrzew, max(IsNull(OdlKopPolb,0)) as OdlKopPolb,
sum(Ilosc) as Ilosc, JM, sum(Netto) as Netto, sum("Transport;Waga(dokument)")/1000 as Waga,
sum(Netto)/sum(Ilosc) CenaJedn,  sum("Transport;Waga(dokument)")/(1000*sum(Ilosc)) WagaSr 
from
(
    select obr.*, zdop.LogoPrzew, zdop.NazPrzew, zdop.OdlKopPolb from W_MG_VV_OBRMAGAZYNOWETRANSPORTPLUSDP obr(NOLOCK)
    left join W_FN_RAPORTZDOP3('%', '%', '%', '%', '@data_od', '@data_do', NULL, NULL, '%', '2920', '%', '%') zdop
        on zdop.symkar='2920' and zdop.DataStart <= '@data_od' and zdop.DataStop >= '@data_do' and zdop.LogoDost = obr.logo and zdop.JM = obr.JM and zdop.MAG = obr.MAG
    where obr.Data >= '@data_od' and obr.Data <= '@data_do' and obr.SymKar ='2920' and obr.Status > 0 and obr.JM = 'KURS'
) tab
group by PD_OpisMagazynu, Nazwa1, JM
order by PD_OpisMagazynu, Nazwa1, JM
"""

sel_fak_wz = """
select tab2.mag, tab2.logo, tab2.numer, tab2.symkar, tab2.IloscMgPrzel, typdok from
(
select mag, logo, symkar,  sum(IloscMgPrzel) IloscMgPrzel
from
(
select n.mag, n.logo, n.nagid, l.symkar, ISNULL(lc.PD_IloscMGPrzel, l.PD_IloscMGPrzel) IloscMgPrzel
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.SymRej LIKE 'SPRZ%' AND n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
union all
select n.mag, n.logo, n.nagid, l.symkar, -1 * ISNULL(lc.PD_IloscMGPrzel, l.PD_IloscMGPrzel) IloscMgPrzel
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
and n.rd like 'wz%'
) tab0
group by mag, logo, symkar
having sum( IloscMGPrzel) * sum( IloscMGPrzel)  > 0
) tab
left join 
(
select n.mag, n.logo, n.nagid, l.symkar, n.numer, ISNULL(lc.PD_IloscMGPrzel, l.PD_IloscMGPrzel) IloscMgPrzel, 1 as typdok
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.SymRej LIKE 'SPRZ%' AND n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
union all
select n.mag, n.logo, n.nagid, l.symkar, n.numer, -1 * ISNULL(lc.PD_IloscMGPrzel, l.PD_IloscMGPrzel) IloscMgPrzel, -1 as typdok
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
and n.rd like 'wz%'
) tab2 on tab2.mag=tab.mag and tab2.logo = tab.logo and tab2.symkar=tab.symkar
order by tab2.mag, tab2.logo, tab2.symkar, tab2.IloscMgPrzel*tab2.IloscMgPrzel, tab2.typdok, tab2.IloscMgPrzel
"""

sel_fak_wz2 = """
select tab2.mag, tab2.logo, tab2.numer, tab2.symkar, tab2.IloscMg, typdok from
(
select mag, logo, symkar,  sum(IloscMg) IloscMg
from
(
select n.mag, n.logo, n.nagid, l.symkar, ISNULL(lc.IloscMG, l.IloscMG) IloscMg
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.SymRej LIKE 'SPRZ%' AND n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
union all
select n.mag, n.logo, n.nagid, l.symkar, -1 * ISNULL(lc.IloscMG, l.IloscMG) IloscMg
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
and n.rd like 'wz%'
) tab0
group by mag, logo, symkar
having sum( IloscMG) * sum( IloscMG)  > 0
) tab
left join 
(
select n.mag, n.logo, n.nagid, l.symkar, n.numer, ISNULL(lc.IloscMG, l.IloscMG) IloscMg, 1 as typdok
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.SymRej LIKE 'SPRZ%' AND n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
union all
select n.mag, n.logo, n.nagid, l.symkar, n.numer, -1 * ISNULL(lc.IloscMG, l.IloscMG) IloscMg, -1 as typdok
FROM dbo.mg_Nag n WITH(NOLOCK)
INNER JOIN dbo.mg_Lin l WITH(NOLOCK) ON n.NagId = l.NagId
LEFT JOIN dbo.mg_LinCech lc WITH (NOLOCK) ON lc.NagId = l.NagId AND lc.LinId = l.LinId
LEFT JOIN dbo.mg_Cechy c WITH(NOLOCK) ON c.SymKar = lc.SymKar AND c.SymCech = lc.SymCech
LEFT JOIN dbo.mg_vv_NagTermMain as nt WITH (NOLOCK) ON nt.NagId = n.NagId
LEFT JOIN dbo.mg_Kar kar(NOLOCK) on kar.symkar = l.SymKar
left join mg_vv_GniazdaProdukcyjneBro gn(NOLOCK) on gn.gniazdo = lc.SymCech
left join kli_Kontrahenci handlowcy(NOLOCK) on handlowcy.logo = n.logoH
WHERE n.Status>0 AND n.Data >= '{{data_od}}' AND  n.Data <= '{{data_do}}' and  kar.RodzajHandlowy = 'PRODUKT' and kar.pd_Typ like 'E%'
and n.rd like 'wz%'
) tab2 on tab2.mag=tab.mag and tab2.logo = tab.logo and tab2.symkar=tab.symkar
order by tab2.mag, tab2.logo, tab2.symkar, tab2.IloscMg*tab2.IloscMg, tab2.typdok, tab2.IloscMg
"""


MAIL_CONTENT = """
W załączeniu raport odświeżany i wysyłany automatycznie. W razie uwag proszę o kontakt z osobami:
- Sławomir Chołaj (slawomir.cholaj@polbruk.pl) - 502 620 952
- Robert Cmiel (robert.cmiel@polbruk.pl) - 694 485 136

Polbruk S.A. Siedziba Spółki: 80-299 Gdańsk, ul. Nowy Świat 16 c, tel. 58 554 97 45, fax 58 554 59 50
NIP: 584-025-35-91 | Sąd Rejonowy Gdańsk-Północ w Gdańsku, VII Wydz. Gospodarczy KRS, KRS: 0000062419 |Regon: 001388727 | Wysokość kapitału zakładowego: 31 766 250,00 zł
Otrzymana przez Panią / Pana wiadomość oraz załączone do niej pliki stanowią tajemnicę Przedsiębiorstwa i są przeznaczone tylko dla wymienionych adresatów. 
Jeżeli nie są Państwo zamierzonym odbiorcą, proszę poinformować o tym fakcie nadawcę oraz usunąć wiadomość ze swojego systemu. Nie powinni Państwo również nikomu ujawniać otrzymanych 
informacji ani sporządzać / zachowywać / dystrybuować żadnej kopii otrzymanych informacji. | This message and any attachments are confidential as a business secret and are intended solely for the 
use of the individual or entity to whom they are addressed. If you are not the intended recipient, please telephone or e-mail the sender and delete this message and any attachment from your system. 
Also, if you are not the intended recipient you should not disclose the content or take / retain / distribute any copies. 
Zanim wydrukujesz wiadomość - pomyśl o środowisku. Please consider the environment before printing out this e-mail.
"""

SEL_DOK_MAG = """
select nag.symrej, year(nag.datasprz) y, month(nag.datasprz) m, lin.RodzajHandlowy, kar.pd_typ, lin.symkar, sum(lin.ilosc) ilosc, sum(lin.dNetto) netto from mg_nag nag(NOLOCK)
left join mg_lin lin(NOLOCK) on lin.nagid = nag.nagid
left join mg_kar kar(NOLOCK) on kar.symkar = lin.symkar
where nag.data >= '%04d0101' and  nag.data < '%04d0101' and nag.symrej in ('PRZZEW', 'ZAKSEOD') and  nag.Status > 0 
and not (rd not in ('PZN', 'PZKN' ) and lin.RodzajHandlowy = 'PALETA')
group by nag.symrej, year(nag.datasprz), month(nag.datasprz), lin.RodzajHandlowy, kar.pd_typ, lin.symkar
order by nag.symrej, year(nag.datasprz), month(nag.datasprz), lin.RodzajHandlowy, kar.pd_typ, lin.symkar
"""

def gen_date():
    return datetime.datetime.now().isoformat().replace('T',' ')[:19]
     

PFORM = form_with_perms('raporty') 


class WiekowanieForm(forms.Form):
    typ = forms.ChoiceField(label=_('Typ raportu'), required=True, choices=models.WiekowanieTypChoices)
    data = forms.DateField(label=_('Data'), required=True, initial=datetime.datetime.today().isoformat()[:10],)
    mag = forms.CharField(label=_('Magazyn'), required=False, initial='%',)
    rodzaj_handlowy = forms.ChoiceField(label=_('Rodzaj handlowy'), required=True, choices=models.RodzajHandlowyChoices)
    pd_typ = forms.CharField(label=_('pd_typ'), required=True, initial='%',)
    pdf = forms.BooleanField(label=_('Do pdf'), required=False, initial=False,)
    odf = forms.BooleanField(label=_('Do arkusza'), required=False, initial=False,)
    przelicz = forms.BooleanField(label=_('Wartości przeliczone'), required=False, initial=False,)
    mag_typ = forms.ChoiceField(label=_('Typ magazynu'), required=True, choices=models.TypMagChoices)
    okresy = forms.CharField(label=_('Okresy'), required=True, initial='30;90;180;365;547;729',)
    
    def process(self, request, queryset=None):
    
        mag = self.cleaned_data['mag']
        pdf = self.cleaned_data['pdf']
        odf = self.cleaned_data['odf']
        _rodzaj_handlowy = self.cleaned_data['rodzaj_handlowy']
        typ = int(self.cleaned_data['typ'])
        data = self.cleaned_data['data']
        date = data.isoformat().replace('T',' ')[:16]
        pd_typ = self.cleaned_data['pd_typ']
        przelicz = self.cleaned_data['przelicz']
        _mag_typ = self.cleaned_data['mag_typ']
        okresy = self.cleaned_data['okresy']
        
        _rh = {
            'o1': "like 'PRODUKT'",
            'o2': "not like 'PRODUKT'",
            'o3': "like '%'"
        }
        
        _mt = {
            'o1': "obr.Mag like '%'",
            'o2': "(obr.Mag like '__' or obr.Mag like '[56]99' ) and not obr.Mag like '50'",
            'o3': "obr.Mag like '1__' and not obr.Mag like '__'",
            'o4': "obr.Mag like '3__' and not obr.Mag like '__'",
            'o5': "obr.Mag like '2__' and not obr.Mag like '__'",
            'o6': "obr.Mag like '9__' and not obr.Mag like '__'"
        }
        
        rodzaj_handlowy = _rh[_rodzaj_handlowy]
        mag_typ = _mt[_mag_typ]
        
        if typ == 4:    
            okr = [30,60,90,120,150,180,210,240,270,300,330,365,547,730]
            odf=True
            pdf=False
        else:
            okr = okresy.split(';')    
            if len(okr)!=6:
                return { "object_list": [],  'doc_type': 'html', 'typ': typ, 'date': None, 'mag':mag, 'rodzaj_handlowy': rodzaj_handlowy, 'sumy': [] }
            
        if not mag:
            return { "object_list": [],  'doc_type': 'html', 'typ': typ, 'date': None, 'mag':mag, 'rodzaj_handlowy': rodzaj_handlowy, 'sumy': [] }
        
        
        okr2 = [ 0, ]
        for pos in okr:
            try:
                x = int(pos)
            except:
                return { "object_list": [],  'doc_type': 'html', 'typ': typ, 'date': None, 'mag':mag, 'rodzaj_handlowy': rodzaj_handlowy, 'sumy': [] }
            okr2.append(x)
            okr2.append(x+1)
        
        with settings.DB as db:
            if typ==1:
                param = [mag, mag_typ, rodzaj_handlowy, pd_typ]
                db.execute(sel_wiekowanie.replace('GetDate()',"'%s'" % date.replace('-','')) % tuple(okr2+param))
            elif typ == 2:    
                param = [mag, mag_typ, rodzaj_handlowy, pd_typ]
                db.execute(sel_wiekowanie2.replace('GetDate()', "'%s'" % date.replace('-','')) % tuple(okr2+param))
            elif typ == 4:    
                param = [mag, mag_typ, rodzaj_handlowy, pd_typ]
                db.execute(sel_wiekowanie5.replace('GetDate()', "'%s'" % date.replace('-','')) % tuple(okr2+param))
            else:
                param = ['%', mag_typ, rodzaj_handlowy, pd_typ]
                db.execute(sel_wiekowanie3.replace('GetDate()', "'%s'" % date.replace('-','')) % tuple(okr2+param))
                self.data = self.data.copy()
                self.data['mag'] = '%'
                
            object_list=db.fetchall()
        
        object_list2 = []
        
        sumy_count = 8
        
        if typ==1:
            id_start = 5
        elif typ==2:
            id_start = 4
        elif typ==4:
            id_start = 5
            sumy_count = 16
        else:
            id_start = 3
            
        sumy_il=[]
        sumy_wart=[]
        for i in range(sumy_count):
            sumy_il.append(0.0)
            sumy_wart.append(0.0)
        
        for pos_tmp in object_list:
            if przelicz and not  odf:
                pos = []
                for p in pos_tmp:
                    pos.append(p)
                for i in range(sumy_count):
                    pos[i+id_start-1] = pos_tmp[i+id_start-1] * pos_tmp[-1]
                
                if pos_tmp[-1] != 0:
                    pos[id_start+sumy_count+1] = pos_tmp[id_start+sumy_count+1] / pos_tmp[-1]
                else:
                    pos[id_start+sumy_count+1] = pos_tmp[id_start+sumy_count+1]
                
                if not odf:
                    pos[-4] = 'mprzel'
                
            else:
                pos = pos_tmp
            
            sr = (1*pos_tmp[id_start+1] + 2*pos_tmp[id_start+2] + 3*pos_tmp[id_start+3] + 4*pos_tmp[id_start+4] + 5*pos_tmp[id_start+5] + 6*pos_tmp[id_start+6])/(pos_tmp[id_start-1]*6)
            sr = int(10 * sr)
            try:
                bgcolor = BGCOLOR[sr]
            except:
                print("error:", sr,  pos_tmp[id_start-1],  pos_tmp[id_start+1], pos_tmp[id_start+2], pos_tmp[id_start+3], pos_tmp[id_start+4], pos_tmp[id_start+5], pos_tmp[id_start+6])
                bgcolor = '#fff'
        
            for i in range(sumy_count):
                sumy_il[i] = sumy_il[i] + float(pos[i+id_start-1])
                sumy_wart[i] = sumy_wart[i] + float(pos_tmp[i+id_start-1] * pos_tmp[id_start+sumy_count+1])
            pos2 = list(pos)
            pos2.append(bgcolor)
            object_list2.append(pos2)
        
        
        doc_type = 'html'
        if pdf:
            doc_type = 'pdf'
        elif odf:
            doc_type = 'odf'
        
        sumy = [ pos for pos in zip(sumy_il,sumy_wart) ]
        
        date = data.isoformat().replace('T',' ')[:16]
        date10 = date[:10]
        return { "object_list": object_list2, 'doc_type': doc_type, 'typ': typ, 'date': date, 'date10': date10, 'mag':mag, 'rodzaj_handlowy': rodzaj_handlowy, 'pd_typ': pd_typ, 'sumy': sumy, 'okresy': okr2 }
    

def view_wiekowanieform(request, *argi, **argv):
    return PFORM(request, WiekowanieForm, 'raporty/formwiekowanieform.html', {})


class SaldaForm(forms.Form):
    rok = forms.ChoiceField(label=_('Rok'), required=True, choices=models.RokChoices)
    miesiac = forms.ChoiceField(label=_('Miesiąc'), required=True, choices=models.MiesiacChoices)
    odf = forms.BooleanField(label=_('Do arkusza'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        rok = self.cleaned_data['rok']
        miesiac = self.cleaned_data['miesiac']
        odf = self.cleaned_data['odf']
        
            
        with settings.DB as db:
            db.execute(sel_salda1 % int(rok))
                
            object_list=list(db.fetchall())
            object_list2 = []
        
            for pos in object_list:
                db.execute(sel_salda2 % (int(rok), pos[0]))
                db.execute(sel_salda3 % int(miesiac))        
                l=db.fetchall()
                if len(l)==1: 
                    typ = typ_salda_dla_konta(pos[0])        
                    rec = l[0]        
                    if typ==0:
                        pass
                    elif typ==1:
                        object_list2.append(('WN_'+pos[0], not_null_str(pos[1]), rec[8],  rec[4], rec[5], rec[8], rec[9],))
                        object_list2.append(('MA_'+pos[0], not_null_str(pos[1]), rec[9],  rec[4], rec[5], rec[8], rec[9],))
                    elif typ==2:
                        object_list2.append((pos[0], not_null_str(pos[1]), rec[4],  rec[4], rec[5], rec[8], rec[9],))
                    elif typ==3:
                        object_list2.append((pos[0], not_null_str(pos[1]), rec[5],  rec[4], rec[5], rec[8], rec[9],))
                    elif typ==4:
                        object_list2.append((pos[0], not_null_str(pos[1]), not_null(rec[8])-not_null(rec[9]),  rec[4], rec[5], rec[8], rec[9],))
                    elif typ==5:
                        object_list2.append((pos[0], not_null_str(pos[1]), not_null(rec[9])-not_null(rec[8]),  rec[4], rec[5], rec[8], rec[9],))
        
        object_list3 = []
        for pos in object_list2:
            if pos[2] and pos[2]!=0:
                x = []
                for item in pos:
                    if not item:
                        x.append(0.0)
                    else:
                        x.append(item)
                object_list3.append(x)
        
        doc_type = 'html'
        if odf:
            doc_type = 'odf'
        
        return { "object_list": object_list3,  'doc_type': doc_type, }
    

def view_saldaform(request, *argi, **argv):
    return PFORM(request, SaldaForm, 'raporty/formsaldaform.html', {})


class ObrotyTransport(forms.Form):
    data_od = forms.DateField(label=_('Data od:'), required=True, )
    data_do = forms.DateField(label=_('Data do:'), required=True, )
    odf = forms.BooleanField(label=_('Do arkusza'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        data_od = self.cleaned_data['data_od'].isoformat()
        data_do = self.cleaned_data['data_do'].isoformat()
        
        data_od2 = data_od.replace('-','')
        data_do2 = data_do.replace('-','')
        
        odf = self.cleaned_data['odf']
        
        with settings.DB as db:
            sel = sel_transport1.replace('@data_od', data_od2).replace('@data_do', data_do2)
            db.execute(sel)
            object_list=db.fetchall()
        
        doc_type = 'html'
        if odf:
            doc_type = 'odf'
        
        return { "object_list": object_list,  'doc_type': doc_type,  'data_od': data_od, 'data_do': data_do }
    

def view_obrotytransport(request, *argi, **argv):
    return PFORM(request, ObrotyTransport, 'raporty/formobrotytransport.html', {})


class FakturaWzTest(forms.Form):
    data_od = forms.DateField(label=_('Data od'), required=True, )
    data_do = forms.DateField(label=_('Data do'), required=True, )
    przeliczone = forms.BooleanField(label=_('M. przeliczone'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        data_od = self.cleaned_data['data_od'].isoformat()
        data_do = self.cleaned_data['data_do'].isoformat()
        przeliczone = self.cleaned_data['przeliczone']
        
        data_od2 = data_od.replace('-','')
        data_do2 = data_do.replace('-','')
        
        if przeliczone:
            sel = sel_fak_wz.replace('{{data_od}}', data_od2).replace('{{data_do}}', data_do2).replace('[[data_od]]', data_od2).replace('[[data_do]]', data_do2)
        else:
            sel = sel_fak_wz2.replace('{{data_od}}', data_od2).replace('{{data_do}}', data_do2).replace('[[data_od]]', data_od2).replace('[[data_do]]', data_do2)
        
        
        
        with settings.DB as db:
            db.execute(sel)
            tab=db.fetchall()
        
        result = []
        
        for row in tab:
            result.append(row)
        
        last_pos = None
        result2 = []
        for pos in result:
            if last_pos:
                if pos[0] == last_pos[0] and pos[1] == last_pos[1] and pos[3] == last_pos[3]:
                    if last_pos[4]==-1*pos[4] and last_pos[4]!=0 and last_pos[5]!=pos[5]:
                        if len(result2)>0:
                            del result2[-1]
                            if len(result2)>0:
                                last_pos=result2[-1]
                            else:
                                last_pos = None
                        continue
                    else:
                        result2.append(pos)
                else:
                    result2.append(pos)
            else:
                result2.append(pos)
            last_pos = pos
        result = result2
        result2 = []
        
        last_pos = None
        sum0 = 0.0
        sum1 = 0.0
        
        for pos in result:
            if last_pos:
                if pos[0] == last_pos[0] and pos[1] == last_pos[1] and pos[3] == last_pos[3]:
                    result2.append(("", "", pos[2], pos[3], pos[4]))
                    sum0 = sum0 + pos[4]
                else:
                    result2.append(("Różnica:", "", "", "", sum0))
                    result2.append(pos)
                    sum0 = pos[4]
            else:
                    result2.append(pos)
                    sum0 = pos[4]
                    sum1 = pos[4]
                    
            sum1 = sum1 + pos[4]
            last_pos = pos
        
        if len(result2)>0:
            result2.append(("Różnica:", "", "", "", sum0))
            result2.append(("Podsumowanie różnic:", "", "", "",  sum1))
                
        return { "object_list": result2,  'data_od': data_od, 'data_do': data_do, 'przeliczone': przeliczone }
    

def view_fakturawztest(request, *argi, **argv):
    return PFORM(request, FakturaWzTest, 'raporty/formfakturawztest.html', {})


class SimpleReport(forms.Form):
    report_type = forms.ChoiceField(label=_('Typ raportu'), required=True, choices=models.get_reports)
    year = forms.ChoiceField(label=_('Rok'), required=False, choices=[['', ''],]+list(models.RokChoices))
    month = forms.ChoiceField(label=_('Miesiąc'), required=False, choices=[['', ''],]+list(models.MiesiacChoices))
    date_start = forms.DateField(label=_('Od:'), required=False, )
    date_end = forms.DateField(label=_('Do:'), required=False, )
    date_gen = forms.CharField(label=_('Data generowania'), required=False, initial=gen_date,max_length=None, min_length=None)
    param = forms.CharField(label=_('Extra parametry'), required=False, max_length=None, min_length=None)
    pdf = forms.BooleanField(label=_('Pdf'), required=False, initial=False,)
    odf = forms.BooleanField(label=_('Odf'), required=False, initial=False,)
    xlsx = forms.BooleanField(label=_('Xlsx'), required=True, initial=False,)
    
    def process(self, request, queryset=None):
    
        report_type = self.cleaned_data['report_type']
        reports = models. Raporty.objects.filter(name=report_type)
        
        if len(reports)==1:
            report = reports[0]
        else:
            report = None
        
        year = self.cleaned_data['year']
        month = self.cleaned_data['month']
        if year and month:    
            if report.narast:
                date_start = '%04d-01-01' % int(year)
            else:
                date_start = '%04d-%02d-01' % (int(year), int(month))
            date_end = '%04d-%02d-%02d' % (int(year), int(month), calendar.monthrange(int(year), int(month))[1])
        else:
            date_start = self.cleaned_data['date_start'].isoformat()
            date_end = self.cleaned_data['date_end'].isoformat()
            year = self.cleaned_data['date_start'].year
            month = self.cleaned_data['date_start'].month
        
        date_gen = self.cleaned_data['date_gen']
        
        param = self.cleaned_data['param']
        
        pdf = self.cleaned_data['pdf']
        odf = self.cleaned_data['odf']
        xlsx = self.cleaned_data['xlsx']
        
        date_start2 = date_start.replace('-','')
        date_end2 = date_end.replace('-','')
        
        if report:
            sel = report.select 
            if 'mysql' in sel:
                cursor = connection.cursor()
                cursor.execute(sel.replace('{{data_od}}', date_start2).replace('{{data_do}}', date_end2).replace('{{param}}', param).replace('[[data_od]]', date_start2).replace('[[data_do]]', date_end2).replace('[[param]]', param))
                object_list=cursor.fetchall()
            elif 'http' in sel and '://' in sel:
                r = requests.get(sel.replace('{{data_od}}', date_start2).replace('{{data_do}}', date_end2).replace('{{param}}', param).replace('[[data_od]]', date_start2).replace('[[data_do]]', date_end2).replace('[[param]]', param))    
                p = r.text
                parser = SimpleTabParserBase()
                parser.feed(p)
                object_list = parser.tables[0][1:]
            else:
                with settings.DB as db:
                    db.execute(sel.replace('{{data_od}}', date_start2).replace('{{data_do}}', date_end2).replace('{{param}}', param).replace('[[data_od]]', date_start2).replace('[[data_do]]', date_end2).replace('[[param]]', param))
                    object_list=db.fetchall()
            columns = report.columns.split(';')
        else:
            object_list = []
            columns = []
        
        width_sum = 0
        columns2 = []
        width = []
        for pos in columns:
            c = pos.split(":")
            columns2.append(c[0])
            if len(c)>1:
                try:
                    w = int(c[1])
                except:
                    w=0
            else:
                w = 0
            width.append(w)
            width_sum+=w
        
        if width_sum<100:
            c = 0
            for pos in width:
                if pos==0:
                    c+=1
            if c>0:
                dx = int((100-width_sum)/c)
                width2 = []
                for pos in width:
                    if pos==0:
                        width2.append(dx)
                    else:
                        width2.append(pos)
                width = width2
        
        columns = []
        for i in range(len(columns2)):
            columns.append((columns2[i], width[i]))
                
        template_name = None 
        doc_type = 'txt'
        if pdf:
            doc_type = 'pdf'
        elif odf:
            doc_type = 'odf'
            template_name = 'raporty/formsimplereport_' + report_type
        elif xlsx:
            doc_type = 'xlsx'
            template_name = 'raporty/formsimplereport_' + report_type
        else:
            template_name = 'raporty/formsimplereport_txt_' + report_type
        
        if len(object_list)>0 and len(object_list[0])> len(columns):
            colors = True
            sli="0:"+str(len(columns))
        else:
            sli=":"
            colors = False
            
        ret = { "object_list": object_list, 'doc_type': doc_type, 'report_type': report_type, 'date_start': date_start, 'date_end': date_end,  'columns': columns,  'time_str': date_gen, 'report': report, 'rok': year, 'mies': month, 'colors': colors, 'sli': sli,  'param': param }
        if template_name:
            ret['template_name'] = template_name
        
        return ret
        
    

def view_simplereport(request, *argi, **argv):
    return PFORM(request, SimpleReport, 'raporty/formsimplereport.html', {})


class Tranformer(forms.Form):
    rap_wzr = forms.FileField(label=_('Wzorzec raportu (w formacie .ods)'), required=True, )
    
    def process(self, request, queryset=None):
    
        class TransformerTbl(object):
            def __init__(self):
                self.row = -1
                self.col = -1
                self.rok = 2017
                self.tabmag = None
        
            def ustaw_rok(self, rok):
                if rok != self.rok:
                    self.rok = rok
                    self.tabmag = None
                    
            def get_tabmag(self):
                if not self.tabmag:
                    with settings.DB as db:
                        db.execute(SEL_DOK_MAG % (int(self.rok), int(self.rok)+1))            
                        self.tabmag=list(db.fetchall())
                return self.tabmag
                
            def IncRow(self, row=1):
                self.row = self.row+row
        
            def IncCol(self, col=1):
                self.col = self.col + col
        
            def SetCol(self, col):
                self.col=col
        
            def SetRow(self, row):
                self.row=row
        
            def _mag(self, symrej, rodzajhandlowy, pd_typ='%', symkar='%', miesiac=0):
                miesiac2 = miesiac
                if miesiac==0:
                    if self.col>12:
                        miesiac2 = self.col-12
                    else:
                        miesiac2 = self.col
                    
                tab = self.get_tabmag()
                il = 0.0
                netto = 0.0
                for pos in tab:
                    if pos[2]==miesiac2:
                        if symrej=='%' or pos[0] == symrej:
                            if rodzajhandlowy=='%' or pos[3]==rodzajhandlowy:
                                if pd_typ=='%' or pos[4]==pd_typ:
                                    if symkar=='%' or pos[5]==symkar:
                                        il += float(pos[6])
                                        netto += float(pos[7])
                return (il, netto)
                
            def il(self, symrej, rodzajhandlowy, pd_typ='%', symkar='%', miesiac=0):
                return self._mag(symrej, rodzajhandlowy, pd_typ, symkar, miesiac)[0]
        
            def netto(self, symrej, rodzajhandlowy, pd_typ='%', symkar='%', miesiac=0):
                return self._mag(symrej, rodzajhandlowy, pd_typ, symkar, miesiac)[1]
        
            def cena(self, symrej, rodzajhandlowy, pd_typ='%', symkar='%', miesiac=0):
                x = self._mag(symrej, rodzajhandlowy, pd_typ, symkar, miesiac)
                if x[0]!=0:
                    return x[1]/x[0]
                else:
                    return 0
                
        tbl = TransformerTbl()
        
        return { 'tbl': tbl, 'mag': tbl, }
        
    
    def render_to_response(self, request, template, context_instance):
        odfdata= request.FILES['rap_wzr']
        file_name = get_temp_filename("temp.ods")
    
        plik = open(file_name, 'wb')
        plik.write(odfdata.read())
        plik.close()
        
        return render_to_response_odf(file_name, context_instance=context_instance)
        

def view_tranformer(request, *argi, **argv):
    return PFORM(request, Tranformer, 'raporty/formtranformer.html', {})








def edit_wiek(request, d, mg, kar, c, kw):
    
    date = d.replace('-','')
    if mg == '_':
        mag = '%'
        warunek = " and obr.rd not like 'MP%%'  and obr.Mag not like '9__'  "
    else:
        warunek = ""
        mag = mg
        
    if c == '_':
        cecha = '%'
    else:
        cecha = c
    
    ilosc = float(kw)        
    
    with settings.DB as db:
        db.execute(sel_wiekowanie4.replace('GetDate()', "'"+date+"'") % (warunek, mag, kar, cecha))
    
        table = []
        table2 = []
    
        suma = 0.0
        il = 0.0
    
        for pos in db.fetchall():
            pos2 = list(pos)
            pos2[1] = pos2[1].isoformat()[:10]
            pos2[7] = float(pos2[7])
            table.append(pos2)
            
            suma += float(pos2[7])
            if suma >= ilosc:
                if suma-ilosc > 0.001:
                    table[-1][7] =  "%.2f z %.2f" % (table[-1][7] - (suma - ilosc), table[-1][7] )
                break
    
    i = 0
    while i < len(table):
        if i < len(table)-1 and table[i][7] < 0 and table[i][7]*-1 == table[i+1][7]:
            i+=1
        else:
            table2.append(table[i])
        i+=1
            
    
    user_dict = {"date": date, "mag": mag, "symkar": kar, "cecha": cecha, "ilosc": ilosc, 'table': table2 }
    
    #c=RequestContext(request,user_dict)
    return render_to_response('raporty/edit_wiek.html', user_dict, request = request)
    




@dict_to_json

def gen(request):
    
    id = request.POST.get('id', '0')
    date_rap = request.POST.get('date_rap', datetime.datetime.now().isoformat()[:19].replace('T', ' '))
    date_gen = request.POST.get('date_gen',datetime.datetime.now().isoformat()[:19].replace('T', ' '))
    
    request.META['HTTP_USER_AGENT']='direct'
    
    for rap in models.Raporty.objects.filter(okres=id):
        print("Raport:", rap.name)
        request.POST = request.POST.copy()
        request.POST['report_type'] = rap.name
    
        if rap.typ=='pdf':
            request.POST['pdf'] = '1'
            request.POST['odf'] = None
            request.POST['xlsx'] = None
        elif rap.typ=='odf':
            request.POST['pdf'] = None
            request.POST['odf'] = '1'
            request.POST['xlsx'] = None
        elif rap.typ=='xlsx':
            request.POST['pdf'] = None
            request.POST['odf'] = None
            request.POST['xlsx'] = '1'
        elif rap.typ=='mail' or rap.typ=='html':
            request.POST['pdf'] = None
            request.POST['odf'] = None
            request.POST['xlsx'] = None
        else:
            request.POST['pdf'] = '1'
            request.POST['odf'] = None
    
        y  = int(date_rap[:4])
        m = int(date_rap[5:7])
        m-=1
        if m==0:
            m=12
            y-=1
        d = calendar.monthrange(y, m)[1]
    
        date_end = '%04d-%02d-%02d' % (y, m, d)
        request.POST['date_end'] = date_end
        if rap.narast:
            date_start =  '%04d-%02d-%02d' % (y,1,1)
        else:
            date_start = '%04d-%02d-%02d' % (y,m,1)
        request.POST['date_start'] = date_start
    
        date_start2 = date_start.replace('-','')
        date_end2 = date_end.replace('-','')
    
        request.POST['date_gen'] = date_gen
    
        typ = 0
    
        if 'select' in rap.mail:
            typ = 1
            sel = rap.mail
            if 'mysql' in sel:
                cursor = connection.cursor()
                cursor.execute(sel.replace('{{data_od}}', date_start2).replace('{{data_do}}', date_end2).replace('[[data_od]]', date_start2).replace('[[data_do]]', date_end2))
                parameters=cursor.fetchall()
            elif 'http' in sel and '://' in sel:
                r = requests.get(sel.replace('{{data_od}}', date_start2).replace('{{data_do}}', date_end2).replace('[[data_od]]', date_start2).replace('[[data_do]]', date_end2))
                p = r.text
                parser = SimpleTabParserBase()
                parser.feed(p)
                parameters = parser.tables[0][1:]
            else:
                with settings.DB as db:
                    db.execute(sel.replace('{{data_od}}', date_start2).replace('{{data_do}}', date_end2).replace('[[data_od]]', date_start2).replace('[[data_do]]', date_end2))
                    parameters=db.fetchall()
        else:
            parameters = ( ('', rap.mail), )
    
        for p in parameters:
            request.POST['param'] = p[0]
            mail_to = [p for p in  p[1].split(';') if p]
    
            x = view_simplereport(request)
            #try:
            if True:
                x.render()
                if len(mail_to)>0:
                    if rap.typ=='mail':
                        mail = EmailMultiAlternatives(rap.description, MAIL_CONTENT, to=mail_to)
                        mail.attach_alternative(x.content.decode('utf-8'), "text/html")
                        mail.send()
                    else:
                        mail = EmailMessage(rap.description, MAIL_CONTENT, to=mail_to)
                        if rap.typ=='html':
                            mail.attach(rap.name + "_"+date_rap.replace('-','').replace(' ','')+".pdf", x.content, "text/html")
                        elif rap.typ=='odf':
                            mail.attach(rap.name + "_"+date_rap.replace('-','').replace(' ','')+".ods", x.content, "application/vnd.oasis.opendocument.spreadsheet")
                        elif rap.typ=='xlsx':
                            mail.attach(rap.name + "_"+date_rap.replace('-','').replace(' ','')+".xlsx", x.content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        else:
                            mail.attach(rap.name + "_"+date_rap.replace('-','').replace(' ','')+".pdf", x.content, "application/pdf")
                        mail.send()
            #except:
            #    print("Unexpected error:", sys.exc_info()[0])
    
    return { 'id': id,  'date_rap': date_rap, 'date_gen': date_gen }
    
    




@dict_to_json

def gen2(request):
    
    date_rap = request.POST.get('date_rap', datetime.datetime.now().isoformat()[:19].replace('T', ' '))
    y  = int(date_rap[:4])
    m = int(date_rap[5:7])
    m-=1
    if m==0:
        m=12
        y-=1
    d = calendar.monthrange(y, m)[1]
    request.META['HTTP_USER_AGENT']='direct'
    
    request.POST = request.POST.copy()
    
    request.POST['mag'] = '%'
    request.POST['pdf'] = None
    request.POST['odf'] = '1'
    request.POST['rodzaj_handlowy'] = "o3"
    request.POST['typ'] = '1'
    request.POST['data'] = '%04d-%02d-%02d' % (y, m, d)
    request.POST['pd_typ'] = '%'
    request.POST['przelicz'] = True
    request.POST['mag_typ'] = "o1"
    request.POST['okresy'] = '30;90;180;364;547;729'
    x = view_wiekowanieform(request)
    x.render()
    mail_to = ['patrycja.kolodziejczyk@polbruk.pl', 'slawomir.cholaj@polbruk.pl',]
    mail = EmailMessage("raport wiekowania", MAIL_CONTENT, to=mail_to)
    mail.attach("wiekowanie.ods", x.content, "application/vnd.oasis.opendocument.spreadsheet")
    mail.send()
    
    return { 'date_rap': date_rap, }
    
    






def kwerenda(request, name):
    
    sel1 = "select * from polbruk_tech.dbo.w_polbruk_vv_ip_logins where client_net_address = '%s' "
    objs = models.Kwerendy.objects.filter(name=name)
    response = HttpResponse()
    if len(objs)==1:
        loginname = None
        with settings.DB as db:
            db.execute(sel1 % request.META['REMOTE_ADDR'])
            rows = list(db.fetchall())
            if len(rows)==1:
                sel2 = objs[0].select.replace('{{loginname}}', rows[0][2])
                db.execute(sel2)
                rows2 = db.iterall()
                response.write("<html><body><table border='1'>\n")
                columns = objs[0].columns
                if columns:
                    rowstr = "<tr>"
                    for pos in columns.split(';'):
                        if pos:
                            rowstr += "<td>"+str(pos)+"</td>"
                    rowstr += "</tr>\n"
                    response.write(rowstr)
                for rec in rows2:
                    rowstr = "<tr>"
                    for pos in rec:
                        rowstr += "<td>"+str(pos)+"</td>"
                    rowstr += "</tr>\n"
                    response.write(rowstr)
                response.write("</table></body><html>")
    return response
    
    






def rep_gen(request, rep_id):
    
    reports = CommonGroup.objects.filter(id=rep_id)
    if len(reports)>0:
        report = reports[0]
        ret = gen_report(report.title, destination="5. download")
        if type(ret) in (tuple, list):
            content = ret[1]
            content_type = ret[2]
            content_disposition = ret[2]['Content-Disposition']
            content_type = ret[2]['Content-Type']        
            response = HttpResponse(content, content_type=content_type)
            response['Content-Disposition'] = content_disposition.replace('formsimplereport_','')
            return response        
        else:
            return HttpResponse("Error")
    return HttpResponse("Report doesn't exists")
    


 
