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

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

"""Module contains base views for pytigon applications"""

import os
import datetime
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
)

from pytigon_lib.schdjangoext.tools import import_model
from pytigon_lib.schtable.dbtable import DbTable
from pytigon_lib.schtools import schjson
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schviews import actions
from pytigon_lib.schdjangoext.tools import make_href

from pytigon_lib.schviews.viewtools import dict_to_json

from pytigon_lib.schtools.tools import bencode, bdecode


APP = None

# _RET_OK = """
# <head>
#    <meta name="TARGET" content="_parent_refr" />
#    <meta name="RETURN" content="$$RETURN_REFRESH_PARENT" />
# </head>
# <body>OK</body>
# """

# _RET_OK_HTML = """
# <head>
#    <meta name="RETURN" content="$$RETURN_REFRESH_PARENT" />
#    <script>ret_ok(%s,"%s");</script>
# </head>
# <body></body>
# """

# _RET_OK_SHTML = """
# <head>
#    <meta name="RETURN" content="$$RETURN_OK" />
#    <meta name="target" content="code" />
# </head>
# <body>
#    <script language=python>
# page = self.get_parent_page().get_parent_page()
# if page:
#    page.signal('return_row', id=%s, title="%s")
#    </script>
# </body>
# """

MESSAGE_LIST = {"null": "", "error": "Program error", "warning": "Program warning"}


def change_password(request):
    """Change password view

    Args:
        request - django request
    """
    old_password = request.POST.get("current_password", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", ".")
    if new_password == confirm_password:
        user = authenticate(username=request.user, password=old_password)
        if user is not None and user.is_active:
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect(make_href("/schsys/do_logout/"))
        else:
            messages.add_message(request, messages.ERROR, "Bad old password")
            return HttpResponseRedirect(make_href("/"))
    else:
        messages.add_message(request, messages.ERROR, "Bad confirmed password")
        return HttpResponseRedirect(make_href("/"))


def ok(request):
    """If form is OK redirect to this view

    Args:
        request - django request
    """

    print("--------------------------------------------------------------")
    print(request.user)
    print("--------------------------------------------------------------")

    return actions.ok(request)


# def ret_ok(request, id, title):
#    """If form is OK redirect to this view
#
#    Args:
#        request - django request
#        id
#        title
#    """
#    return actions.new_row_ok(request, id, title)


#    if request.META["HTTP_USER_AGENT"].lower().startswith("py"):
#        return HttpResponse(_RET_OK_SHTML % (id, title))
#    else:
#        return HttpResponse(_RET_OK_HTML % (id, title))


def message(request, titleid, messageid, id):
    """View to show messages

    Args:
        titleid - title id
        messageid - message id
        id - id
    """
    global MESSAGE_LIST
    title = MESSAGE_LIST[titleid]
    if id != "0":
        message = MESSAGE_LIST[messageid] % id
    else:
        message = MESSAGE_LIST[messageid]
    c = {"title": title.decode("utf-8"), "message": message.decode("utf-8")}
    return render_to_response("schsys/message.html", context=c, request=request)


def tbl(request, app, tab, value=None, template_name=None):
    """View to show table

    Args:
        app - application name
        tab - table name
        value
        template_name - template name
    """
    if request.POST:
        p = request.POST.copy()
        d = {}
        for key, val in list(p.items()):
            if key == "csrfmiddlewaretoken":
                d[str(key)] = val
            else:
                d[str(key)] = schjson.loads(val)
    else:
        d = {}
    if value and value != "":
        d["value"] = bdecode(value.encode("ascii"))
    dbtab = DbTable(app, tab)
    retstr = dbtab.command(d)
    return HttpResponse(retstr)


def datedialog(request, action):
    """View to show date dialog

    Args:
        action - 'size', 'dialog' or 'test'
    """
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = bdecode(p["value"].encode("ascii"))
    else:
        value = ""
    if action == "size":
        return HttpResponse(schjson.dumps((280, 200)))
    if action == "dialog":
        if value.__class__ == int:
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            value = d
        c = {"value": value}
        return render_to_response("schsys/date.html", context=c, request=request)
    if action == "test":
        if value.__class__ == int:
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            return HttpResponse(schjson.dumps((1, d.isoformat(), (d,))))
        else:
            if type(value) == bytes:
                value = value.decode("utf-8")
            return HttpResponse(schjson.dumps((1, value, (value,))))
        return HttpResponse("")
    return HttpResponse("")


def listdialog(request, action):
    """View to show list with options

    Args:
        action - 'size', 'dialog' or 'test'
    """
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = bdecode(p["value"])
        if value is None:
            value = ""
    else:
        value = ""

    if action == "size":
        return HttpResponse(schjson.dumps((250, 300)))
    if action == "dialog":
        c = {"value": value}
        ret = render_to_response("schsys/list.html", context=c, request=request)
        return ret
    if action == "test":
        return HttpResponse(schjson.dumps((2, None, (None,))))
    return HttpResponse("")


def treedialog(request, app, tab, id, action):
    """View to show tree based on table

    Args:
        app - application name
        tab - table name
        id
        action - 'size', 'dialog' or 'test'
    """
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = bdecode(p["value"].encode("ascii"))
        if value == None:
            value = ""
    else:
        value = ""
    if action == "size":
        return HttpResponse(schjson.dumps((450, 400)))
    if action == "dialog":
        model = import_model(app, tab)
        obj = None
        parent_pk = -1
        if int(id) >= 0:
            obj = model.objects.get(id=id)
            if obj and obj.parent:
                id2 = obj.parent.id
                if id2 and id2 > 0:
                    parent_pk = id2
        c = {
            "value": value,
            "app": app,
            "tab": tab,
            "pk": id,
            "parent_pk": parent_pk,
            "model": model,
            "object": obj,
        }
        return render_to_response(
            "schsys/get_from_tree.html", context=c, request=request
        )
    if action == "test":
        return HttpResponse(schjson.dumps((2, None, (None,))))
    return HttpResponse("")


def tabdialog(request, app, tab, id, action):
    """View to show tab dialog

    Args:
        request - dialog request
        app - application name
        tab - table name
        id
        action - 'size', 'dialog' or 'test'
    """
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = bdecode(p["value"].encode("ascii"))
        if value == None:
            value = ""
    else:
        value = ""
    if action == "size":
        return HttpResponse(schjson.dumps((450, 400)))
    if action == "dialog":
        model = import_model(app, tab)
        obj = None
        if int(id) >= 0:
            obj = model.objects.get(id=id)
        c = {
            "value": value,
            "app": app,
            "tab": tab,
            "id": id,
            "model": model,
            "obj": obj,
        }
        return render_to_response(
            "schsys/get_from_tab.html", context=c, request=request
        )
    if action == "test":
        return HttpResponse(schjson.dumps((2, None, (None,))))
    return HttpResponse("")


def plugin_template(request, template_name):
    """Render plugin template

    Args:
        request - django request
        template_name - template name
    """
    global APP
    if not APP:
        import wx

        APP = wx.GetApp()
    c = {"app": APP}
    for key, value in request.POST.items():
        c[key] = value
    return render_to_response(template_name, context=c, request=request)


def plugins(request, app, plugin_name):
    f = None
    try:
        f = open(settings.STATIC_ROOT + "/" + app + "/" + plugin_name + ".zip", "rb")
    except:
        try:
            f = open(
                settings.ROOT_PATH + "/prj/" + app + "/plugins/" + plugin_name + ".zip",
                "rb",
            )
        except:
            raise Http404
    s = f.read()
    f.close()
    return HttpResponse(s, mimetype="application/zip")


def favicon(request):
    return HttpResponseRedirect(make_href("/static/favicon.ico"))


def sw(request):
    if settings.STATIC_ROOT:
        _static_root = settings.STATIC_ROOT
    else:
        _static_root = settings.STATICFILES_DIRS[0]
    static_root1 = os.path.join(_static_root, settings.PRJ_NAME)
    static_root2 = os.path.join(
        settings.PRJ_PATH, settings.PRJ_NAME, "static", settings.PRJ_NAME
    )

    for static_root in (static_root1, static_root2):
        sw_path = os.path.join(static_root, "sw.js")
        buf = ""
        if os.path.exists(sw_path):
            with open(sw_path, "rt") as sw:
                buf = sw.read()
            break
    standard_sw_path = os.path.join(_static_root, "pytigon_js", "sw.js")
    buf2 = ""
    if os.path.exists(standard_sw_path):
        with open(standard_sw_path, "rt") as sw:
            buf2 = sw.read()
            buf2 = buf2.replace("//++//", buf)
    return HttpResponse(
        buf2.encode("utf-8"), content_type="application/javascript; charset=utf-8"
    )


@dict_to_json
def app_time_stamp(request, **argv):
    if settings.GEN_TIME:
        return {"TIME": settings.GEN_TIME}
    else:
        gmt = datetime.time.gmtime()
        gmt_str = "%04d.%02d.%02d %02d:%02d:%02d" % (
            gmt[0],
            gmt[1],
            gmt[2],
            gmt[3],
            gmt[4],
            gmt[5],
        )
        return {"TIME": gmt_str}


def search(request, **argv):
    q = request.POST.get("q", "")
    q2 = bencode(q)
    if hasattr(settings, "SEARCH_PATH"):
        return HttpResponseRedirect(
            make_href((settings.SEARCH_PATH % q2) + "?fragment=page")
        )
    else:
        return Http404()


def redirect_site_media_protected(request):
    url = request.path.replace("site_media_protected", "media_protected")
    if settings.DEBUG:
        return HttpResponseRedirect(url)
    else:
        url = request.path.replace("site_media_protected", "media_protected")
        response = HttpResponse()
        response["X-Accel-Redirect"] = url
        response["Content-Type"] = ""
        return response


def site_media_protected(request, *argi, **argv):
    if hasattr(settings, "PROTECTED_MEDIA_PERMISSIONS"):
        x = request.path.split("site_media_protected/")
        if len(x) >= 2:
            path = x[1]
            for row in settings.PROTECTED_MEDIA_PERMISSIONS:
                result = re.match(row[0], path)
                if result:
                    if row[1] == "is_authenticated":
                        if request.user.is_authenticated:
                            return redirect_site_media_protected(request)
                    elif row[1] == "username":
                        if ("{%s}" % request.username) in path:
                            return redirect_site_media_protected(request)
                    elif row[1] == "email":
                        if ("{%s}" % request.email) in path:
                            return redirect_site_media_protected(request)
                    else:
                        if request.user.has_perm(row[1]):
                            return redirect_site_media_protected(request)

            return HttpResponseForbidden()
    else:
        if request.user.is_authenticated:
            return redirect_site_media_protected(request)
        else:
            return HttpResponseForbidden()


def change_profile_variant(request, variant_name):
    request.user.profile.set_active_variant(variant_name)
    return HttpResponseRedirect(make_href("/"))
