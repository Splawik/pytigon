"""Base views for Pytigon applications.

Provides core views for:
- Authentication (login, logout, change password)
- Table operations (DbTable-based grid views)
- Dialogs (date, list, tree, tab)
- Plugin and template serving
- Service worker and favicon
- Protected media serving
- Search functionality
"""

import datetime
import logging
import os
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
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string

from pytigon_lib.schdjangoext.tools import import_model
from pytigon_lib.schtable.dbtable import DbTable
from pytigon_lib.schtools import schjson
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schviews import actions
from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schviews.viewtools import dict_to_json
from pytigon_lib.schtools.tools import bencode, bdecode

logger = logging.getLogger(__name__)

APP = None


def change_password(request):
    """Handle password change requests.

    Args:
        request: Django HTTP request. POST must contain:
            - current_password
            - new_password
            - confirm_password

    Returns:
        HttpResponseRedirect: Redirects to logout on success, home on failure.
    """
    old_password = request.POST.get("current_password", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", ".")

    if new_password != confirm_password:
        messages.add_message(request, messages.ERROR, "Bad confirmed password")
        return HttpResponseRedirect(make_href("/"))

    user = authenticate(username=request.user, password=old_password)
    if user is not None and user.is_active:
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(make_href("/schsys/do_logout/"))

    messages.add_message(request, messages.ERROR, "Bad old password")
    return HttpResponseRedirect(make_href("/"))


def dstatic(request, script_name):
    """Serve dynamic JavaScript content.

    Args:
        request: Django HTTP request.
        sc (str): Script code.

    Returns:
        HttpResponse: JavaScript code.
    """
    sc = render_to_string(f"js/{script_name}.html", context={}, request=request)
    return HttpResponse(sc, content_type="application/javascript")


def ok(request):
    """Handle successful form submission redirect.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponse: Result from actions.ok().
    """
    logger.debug("OK view called for user: %s", request.user)
    return actions.ok(request)


# Mapping from Django message levels to Bootstrap CSS classes
MSG_MAP = {
    messages.DEBUG: "",
    messages.INFO: "text-bg-info",
    messages.SUCCESS: "",
    messages.WARNING: "text-bg-warning",
    messages.ERROR: "text-bg-danger",
}


def get_messages(request):
    """Retrieve and render accumulated messages.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponse: Rendered messages template or empty response.
    """
    tab = []
    for message in messages.get_messages(request):
        tab.append(
            {
                "level": message.level,
                "message": message.message,
                "extra_tags": message.extra_tags,
                "class": MSG_MAP.get(message.level, ""),
            }
        )

    if tab:
        return render_to_response(
            "schsys/messages.html",
            context={"messages": tab},
            request=request,
        )
    return HttpResponse("")


# def tbl(request, app, tab, value=None, template_name=None):
#     """Render a database table view using DbTable.

#     Args:
#         request: Django HTTP request.
#         app: Application name.
#         tab: Table name.
#         value: Optional value parameter.
#         template_name: Optional template name.

#     Returns:
#         HttpResponse: The rendered table output.
#     """
#     if request.POST:
#         p = request.POST.copy()
#         d = {}
#         for key, val in list(p.items()):
#             if key == "csrfmiddlewaretoken":
#                 d[str(key)] = val
#             else:
#                 d[str(key)] = schjson.loads(val)
#     else:
#         d = {}

#     if value and value != "":
#         d["value"] = bdecode(value.encode("ascii"))

#     dbtab = DbTable(app, tab)
#     retstr = dbtab.command(d)
#     return HttpResponse(retstr)


def datedialog(request, action):
    """Handle date dialog actions (size, dialog, test).

    Args:
        request: Django HTTP request.
        action: One of 'size', 'dialog', or 'test'.

    Returns:
        HttpResponse: JSON-encoded size, HTML dialog, or test result.
    """
    if request.POST or request.GET:
        p = request.POST.copy() if request.POST else request.GET.copy()
        value = bdecode(p["value"].encode("ascii"))
    else:
        value = ""

    if action == "size":
        return HttpResponse(schjson.dumps((280, 200)))

    if action == "dialog":
        if isinstance(value, int):
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            value = d
        c = {"value": value}
        return render_to_response("schsys/date.html", context=c, request=request)

    if action == "test":
        if isinstance(value, int):
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            return HttpResponse(schjson.dumps((1, d.isoformat(), (d,))))
        else:
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            return HttpResponse(schjson.dumps((1, value, (value,))))

    return HttpResponse("")


def listdialog(request, action):
    """Handle list dialog actions (size, dialog, test).

    Args:
        request: Django HTTP request.
        action: One of 'size', 'dialog', or 'test'.

    Returns:
        HttpResponse: JSON-encoded size, HTML dialog, or test result.
    """
    if request.POST or request.GET:
        p = request.POST.copy() if request.POST else request.GET.copy()
        value = bdecode(p["value"])
        if value is None:
            value = ""
    else:
        value = ""

    if action == "size":
        return HttpResponse(schjson.dumps((250, 300)))

    if action == "dialog":
        c = {"value": value}
        return render_to_response("schsys/list.html", context=c, request=request)

    if action == "test":
        return HttpResponse(schjson.dumps((2, None, (None,))))

    return HttpResponse("")


def treedialog(request, app, tab, id, action):
    """Handle tree dialog actions (size, dialog, test).

    Args:
        request: Django HTTP request.
        app: Application name.
        tab: Table name.
        id: Object ID.
        action: One of 'size', 'dialog', or 'test'.

    Returns:
        HttpResponse: JSON-encoded size, HTML dialog, or test result.
    """
    if request.POST or request.GET:
        p = request.POST.copy() if request.POST else request.GET.copy()
        value = bdecode(p["value"].encode("ascii"))
        if value is None:
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
            try:
                obj = model.objects.get(id=id)
            except model.DoesNotExist:
                obj = None
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
    """Handle tab dialog actions (size, dialog, test).

    Args:
        request: Django HTTP request.
        app: Application name.
        tab: Table name.
        id: Object ID.
        action: One of 'size', 'dialog', or 'test'.

    Returns:
        HttpResponse: JSON-encoded size, HTML dialog, or test result.
    """
    if request.POST or request.GET:
        p = request.POST.copy() if request.POST else request.GET.copy()
        value = bdecode(p["value"].encode("ascii"))
        if value is None:
            value = ""
    else:
        value = ""

    if action == "size":
        return HttpResponse(schjson.dumps((450, 400)))

    if action == "dialog":
        model = import_model(app, tab)
        obj = None
        if int(id) >= 0:
            try:
                obj = model.objects.get(id=id)
            except model.DoesNotExist:
                obj = None
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
    """Render a plugin template within the application context.

    Args:
        request: Django HTTP request.
        template_name: Name of the template to render.

    Returns:
        HttpResponse: Rendered template.
    """
    global APP
    if not APP:
        try:
            import wx

            APP = wx.GetApp()
        except ModuleNotFoundError:
            APP = None

    c = {"app": APP} if APP else {}
    for key, value in request.POST.items():
        if key not in ("settings", "request", "user", "csrf_token", "app"):
            c[key] = value
    return render_to_response(template_name, context=c, request=request)


def plugins(request, app, plugin_name):
    """Serve a plugin ZIP file from static or project directories.

    Args:
        request: Django HTTP request.
        app: Application name.
        plugin_name: Name of the plugin.

    Returns:
        HttpResponse: ZIP file content.

    Raises:
        Http404: If the plugin file is not found.
    """
    # Try static root first, then project plugins directory
    candidates = [
        os.path.join(settings.STATIC_ROOT, app, plugin_name + ".zip"),
        os.path.join(settings.ROOT_PATH, "prj", app, "plugins", plugin_name + ".zip"),
    ]

    for candidate in candidates:
        try:
            with open(candidate, "rb") as f:
                s = f.read()
            return HttpResponse(s, content_type="application/zip")
        except OSError:
            continue

    raise Http404(f"Plugin '{plugin_name}' not found for app '{app}'")


@cache_page(60 * 60 * 24 * 30)
def favicon(request):
    """Redirect to the static favicon.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponseRedirect: Redirect to /static/favicon.ico.
    """
    return HttpResponseRedirect(make_href("/static/favicon.ico"))


@cache_page(60 * 60 * 24 * 30)
def sw(request):
    """Serve the service worker JavaScript file.

    Combines a project-specific SW with the standard Pytigon SW.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponse: Service worker JavaScript content.
    """
    _static_root = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]

    static_root1 = os.path.join(_static_root, settings.PRJ_NAME)
    static_root2 = os.path.join(
        settings.PRJ_PATH, settings.PRJ_NAME, "static", settings.PRJ_NAME
    )

    buf = ""
    for static_root in (static_root1, static_root2):
        sw_path = os.path.join(static_root, "sw.js")
        if os.path.exists(sw_path):
            with open(sw_path) as sw_file:
                buf = sw_file.read()
            break

    standard_sw_path = os.path.join(_static_root, "pytigon_js", "sw.js")
    buf2 = ""
    if os.path.exists(standard_sw_path):
        with open(standard_sw_path) as sw_file:
            buf2 = sw_file.read()
            buf2 = buf2.replace("//++//", buf)

    return HttpResponse(
        buf2.encode("utf-8"),
        content_type="application/javascript; charset=utf-8",
    )


@dict_to_json
def app_time_stamp(request, **argv):
    """Return the application build timestamp.

    Args:
        request: Django HTTP request.

    Returns:
        dict: Contains 'TIME' with the build timestamp.
    """
    if settings.GEN_TIME:
        return {"TIME": settings.GEN_TIME}

    gmt = datetime.time.gmtime()
    gmt_str = f"{gmt[0]:04d}.{gmt[1]:02d}.{gmt[2]:02d} {gmt[3]:02d}:{gmt[4]:02d}:{gmt[5]:02d}"
    return {"TIME": gmt_str}


def search(request, **argv):
    """Handle search requests by redirecting to the search path.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponseRedirect: Redirect to search results.
        Http404: If SEARCH_PATH is not configured.
    """
    q = request.POST.get("q", "")
    q2 = bencode(q)

    if hasattr(settings, "SEARCH_PATH"):
        return HttpResponseRedirect(
            make_href((settings.SEARCH_PATH % q2) + "?fragment=page")
        )

    raise Http404("Search not configured")


def redirect_site_media_protected(request):
    """Redirect protected media requests to the internal media path.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponseRedirect or HttpResponse with X-Accel-Redirect header.
    """
    url = request.path.replace("site_media_protected", "media_protected")

    if settings.DEBUG:
        return HttpResponseRedirect(url)

    response = HttpResponse()
    response["X-Accel-Redirect"] = url
    response["Content-Type"] = ""
    return response


def site_media_protected(request, *argi, **argv):
    """Handle protected media access with configurable permission checks.

    Supports permission types:
        - is_authenticated: User must be logged in.
        - username: Path must contain the username.
        - email: Path must contain the user's email.
        - <permission_name>: User must have the specified Django permission.

    Args:
        request: Django HTTP request.

    Returns:
        HttpResponse: The media file or a forbidden response.
    """
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
                        if (f"{{{request.username}}}") in path:
                            return redirect_site_media_protected(request)
                    elif row[1] == "email":
                        if (f"{{{request.email}}}") in path:
                            return redirect_site_media_protected(request)
                    else:
                        if request.user.has_perm(row[1]):
                            return redirect_site_media_protected(request)

            return HttpResponseForbidden()

    # Default behavior: only authenticated users can access
    if request.user.is_authenticated:
        return redirect_site_media_protected(request)

    return HttpResponseForbidden()


def change_profile_variant(request, variant_name):
    """Change the user's active profile variant.

    Args:
        request: Django HTTP request.
        variant_name: Name of the variant to activate.

    Returns:
        HttpResponseRedirect: Redirect to home.
    """
    request.user.profile.set_active_variant(variant_name)
    return HttpResponseRedirect(make_href("/"))


def start(request, start_page=False):
    """Handle the start page.

    Redirects unauthenticated users to login when allauth is enabled.

    Args:
        request: Django HTTP request.
        start_page: Whether this is a project start page.

    Returns:
        HttpResponse: Rendered index page or redirect to login.
    """
    if (
        hasattr(request, "user")
        and not request.user.is_authenticated
        and settings.SHOW_LOGIN_WIN
        and settings.ALLAUTH
    ):
        return HttpResponseRedirect(make_href("/accounts/login/"))

    return render_to_response(
        "schsys/app/index.html",
        context={"start_page": start_page},
        request=request,
    )
