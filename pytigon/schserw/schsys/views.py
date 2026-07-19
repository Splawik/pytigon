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
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from pytigon_lib.schdjangoext.tools import import_model, make_href
from pytigon_lib.schtools import schjson
from pytigon_lib.schtools.tools import bdecode, bencode
from pytigon_lib.schviews import actions
from pytigon_lib.schviews.viewtools import dict_to_json, render_to_response

logger = logging.getLogger(__name__)

_APP_WX = None


def _get_wx_app():
    """Return the wx.App singleton if wxPython is available, else None.

    The lookup is performed at most once per process and cached in a
    module-level variable guarded by a lock to remain thread-safe.
    """
    global _APP_WX
    if _APP_WX is None:
        try:
            import wx

            _APP_WX = wx.GetApp() or False
        except ModuleNotFoundError:
            _APP_WX = False
    return _APP_WX if _APP_WX else None


def change_password(request):
    old_password = request.POST.get("current_password", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", ".")

    if new_password != confirm_password:
        messages.add_message(request, messages.ERROR, "Bad confirmed password")
        return HttpResponseRedirect(make_href("/"))

    user = authenticate(request, username=request.user.username, password=old_password)
    if user is not None and user.is_active:
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(make_href("/schsys/do_logout/"))

    messages.add_message(request, messages.ERROR, "Bad old password")
    return HttpResponseRedirect(make_href("/"))


def dstatic(request, script_name):
    sc = render_to_string(f"js/{script_name}.html", context={}, request=request)
    return HttpResponse(sc, content_type="application/javascript")


def ok(request):
    logger.debug("OK view called for user: %s", request.user)
    return actions.ok(request)


MSG_MAP = {
    messages.DEBUG: "",
    messages.INFO: "text-bg-info",
    messages.SUCCESS: "",
    messages.WARNING: "text-bg-warning",
    messages.ERROR: "text-bg-danger",
}


def get_messages(request):
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


class _DialogView:
    """Base class for dialog views (date, list, tree, tab).

    Subclasses must define ``size_to_render``, ``action_to_render``,
    and ``template_to_render``.
    """

    size = (280, 200)
    template_name = ""
    action = ""

    def get_value(self, request):
        if request.POST or request.GET:
            p = request.POST.copy() if request.POST else request.GET.copy()
            return bdecode(p.get("value", "").encode("utf-8"))
        return ""

    def handle_size(self, request):
        return HttpResponse(schjson.dumps(self.size))

    def handle_dialog(self, request, value, *args, **kwargs):
        c = {"value": value}
        return render_to_response(self.template_name, context=c, request=request)

    def handle_test(self, request, value, *args, **kwargs):
        return HttpResponse(schjson.dumps((2, None, (None,))))

    def __call__(self, request, action, *args, **kwargs):
        value = self.get_value(request)
        if action == "size":
            return self.handle_size(request)
        if action == "dialog":
            return self.handle_dialog(request, value, *args, **kwargs)
        if action == "test":
            return self.handle_test(request, value, *args, **kwargs)
        return HttpResponse("")


class _DateDialogView(_DialogView):
    size = (280, 200)
    template_name = "schsys/date.html"

    def handle_dialog(self, request, value, *args, **kwargs):
        if isinstance(value, int):
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            value = d
        c = {"value": value}
        return render_to_response(self.template_name, context=c, request=request)

    def handle_test(self, request, value, *args, **kwargs):
        if isinstance(value, int):
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            return HttpResponse(schjson.dumps((1, d.isoformat(), (d,))))
        else:
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            return HttpResponse(schjson.dumps((1, value, (value,))))


class _ListDialogView(_DialogView):
    size = (250, 300)
    template_name = "schsys/list.html"

    def get_value(self, request):
        if request.POST or request.GET:
            p = request.POST.copy() if request.POST else request.GET.copy()
            value = bdecode(p["value"])
            if value is None:
                value = ""
            return value
        return ""


class _TreeDialogView(_DialogView):
    size = (450, 400)
    template_name = "schsys/get_from_tree.html"

    def handle_dialog(self, request, value, app, tab, id):
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
        return render_to_response(self.template_name, context=c, request=request)


class _TabDialogView(_DialogView):
    size = (450, 400)
    template_name = "schsys/get_from_tab.html"

    def handle_dialog(self, request, value, app, tab, id):
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
        return render_to_response(self.template_name, context=c, request=request)


_datedialog = _DateDialogView()
_listdialog = _ListDialogView()
_treedialog = _TreeDialogView()
_tabdialog = _TabDialogView()


def datedialog(request, action):
    return _datedialog(request, action)


def listdialog(request, action):
    return _listdialog(request, action)


def treedialog(request, app, tab, id, action):
    return _treedialog(request, action, app, tab, id)


def tabdialog(request, app, tab, id, action):
    return _tabdialog(request, action, app, tab, id)


def plugin_template(request, template_name):
    """Render a plugin template within the application context.

    Args:
        request: Django HTTP request.
        template_name: Name of the template to render.

    Returns:
        HttpResponse: Rendered template.
    """
    app = _get_wx_app()
    c = {"app": app} if app else {}
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

    gmt = time.gmtime()
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
                        if (f"{{{request.user.username}}}") in path:
                            return redirect_site_media_protected(request)
                    elif row[1] == "email":
                        if (f"{{{request.user.email}}}") in path:
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
