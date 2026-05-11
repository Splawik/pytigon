"""Base web browser class providing shared functionality for all browser backends.

This module defines the BaseWebBrowser mixin class that implements common
web browser features: navigation (back/forward/stop/refresh), bookmarking,
local request interception, JavaScript command routing, and PDF handling.
"""

from tempfile import NamedTemporaryFile
from base64 import decodebytes, b64encode, b64decode
import urllib.parse
import os

import wx

from pytigon_gui.guilib.tools import get_colour
from pytigon_gui.guilib.events import *
from pytigon_lib.schtools.tools import split2

# JavaScript snippet to display PDF via PDF.js in the browser
JAVASCRIPT_CODE = (
    "var pdf_ptr=base64toBlob(\"%s\", 'application/pdf');"
    " PDFView.open(URL.createObjectURL(pdf_ptr), 0);"
)


class BaseWebBrowser(object):
    """Base mixin class for embedded web browsers.

    Provides shared navigation, status tracking, local request handling,
    and JavaScript command routing. Must be mixed with a concrete browser
    control (e.g. wx.html2.WebView or CEF) and SchBaseCtrl.

    Loading state constants:
        LOAD_CONNECT     - connection being established
        LOAD_START       - page loading started
        LOAD_FINISH_OK   - page loaded successfully
        LOAD_FINISH_FAILED - page load failed
    """

    LOAD_CONNECT = 0
    LOAD_START = 1
    LOAD_FINISH_OK = 2
    LOAD_FINISH_FAILED = 3

    def __init__(self):
        self.progress = -1
        self.href = ""
        self.status = {
            "stat": -1,
            "progress": -1,
            "txt": None,
            "address": None,
        }
        aTable = [
            (wx.ACCEL_ALT, ord("J"), self.on_key_j),
            (wx.ACCEL_ALT, ord("K"), self.on_key_k),
            (wx.ACCEL_CTRL, ord("N"), self.on_key_n),
            (wx.ACCEL_CTRL, ord("L"), self.on_key_l),
        ]
        self.set_acc_key_tab(aTable)
        self.last_status_txt = ""
        self.pdf = None

        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_goback, id=ID_WEB_BACK)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_goforward, id=ID_WEB_FORWARD)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_stop, id=ID_WEB_STOP)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_refresh, id=ID_WEB_REFRESH)
        self.Bind(
            wx.EVT_UPDATE_UI, self.on_check_can_addbookmark, id=ID_WEB_ADDBOOKMARK
        )
        self.Bind(wx.EVT_MENU, self._on_back, id=ID_WEB_BACK)
        self.Bind(wx.EVT_MENU, self._on_forward, id=ID_WEB_FORWARD)
        self.Bind(wx.EVT_MENU, self._on_stop, id=ID_WEB_STOP)
        self.Bind(wx.EVT_MENU, self._on_refresh, id=ID_WEB_REFRESH)
        self.Bind(wx.EVT_MENU, self._on_addbookmark, id=ID_WEB_ADDBOOKMARK)

    def _is_page_active(self):
        """Check if the parent page is the currently active tab.

        Returns:
            True if the parent page is active, False otherwise.
        """
        parent_form = self.get_parent_form()
        if parent_form is None:
            return False
        parent_page = parent_form.get_parent_page()
        if parent_page is None:
            return False
        return parent_page.is_active()

    def on_check_can_goforward(self, event):
        if self._is_page_active():
            event.Enable(self.can_go_forward())
        else:
            event.Skip()

    def on_check_can_goback(self, event):
        if self._is_page_active():
            event.Enable(self.can_go_back())
        else:
            event.Skip()

    def on_check_can_stop(self, event):
        if self._is_page_active():
            event.Enable(self.can_stop())
        else:
            event.Skip()

    def on_check_can_refresh(self, event):
        if self._is_page_active():
            event.Enable(self.can_refresh())
        else:
            event.Skip()

    def on_check_can_addbookmark(self, event):
        if self._is_page_active():
            event.Enable(self.can_addbookmark())
        else:
            event.Skip()

    def _on_back(self, event):
        if self._is_page_active():
            self.on_back(None)
        else:
            event.Skip()

    def _on_forward(self, event):
        if self._is_page_active():
            self.on_forward(None)
        else:
            event.Skip()

    def _on_stop(self, event):
        if self._is_page_active():
            self.on_stop(None)
        else:
            event.Skip()

    def _on_refresh(self, event):
        if self._is_page_active():
            self.on_refresh(None)
        else:
            event.Skip()

    def _on_addbookmark(self, event):
        if self._is_page_active():
            self.on_addbookmark(None)
        else:
            event.Skip()

    def after_init(self):
        """Post-initialization: load initial data if tdata is present.

        This method is called after the concrete browser control has been
        fully initialized. It decodes any preloaded data and renders it.
        """
        if self.tdata:
            try:
                # Try to decode as base64-encoded string
                data = decodebytes(self.tdata[0][0].data.encode("utf-8")).decode(
                    "utf-8"
                )
            except Exception:
                # Fallback: assume data is already decoded
                try:
                    data = self.tdata[0][0].data
                    if isinstance(data, bytes):
                        data = data.decode("utf-8")
                except Exception:
                    data = ""
            self.load_str(self.html_from_str(data))

    def html_from_str(self, str_body):
        """Wrap HTML body content in a minimal HTML document.

        Args:
            str_body: The HTML body content.

        Returns:
            Complete HTML document string with system background color.
        """
        color = get_colour(wx.SYS_COLOUR_3DFACE)
        return (
            (
                "<!DOCTYPE html><html><head>"
                '<base href="static://" target="_blank">'
                "</head><body bgcolor='%s'>" % color
            )
            + str_body
            + "</body></html>"
        )

    def on_key_j(self, event):
        """Scroll down by 50px."""
        self.execute_javascript("window.scrollBy(0,50);")

    def on_key_k(self, event):
        """Scroll up by 50px."""
        self.execute_javascript("window.scrollBy(0,-50);")

    def on_key_n(self, event):
        """Open a new browser window."""
        wx.PostEvent(
            wx.GetApp().GetTopWindow(),
            wx.CommandEvent(wx.EVT_MENU.typeId, id=ID_WEB_NEW_WINDOW),
        )

    def on_key_l(self, event):
        """Open the 'Go to URL' panel."""
        self.get_parent_form().GetParent().body.new_child_page(
            "^standard/webview/gotopanel.html", title="Go"
        )

    def accept_page(self, page):
        """Handle page acceptance - redirect PDFs to PDF viewer.

        Args:
            page: Page identifier string.

        Returns:
            False if the page was handled (PDF), True if loading should proceed.
        """
        self.status["address"] = page
        if "pdf_info" in page:
            http = wx.GetApp().get_http(self)
            response = http.get(self, str(page), user_agent="webkit")
            p = response.ptr()
            f = NamedTemporaryFile(delete=False)
            try:
                f.write(p)
                name = f.name
            finally:
                f.close()
            okno = (
                wx.GetApp()
                .GetTopWindow()
                .new_main_page("^standard/pdfviewer/pdfviewer.html", page, None)
            )
            okno.body["PDFVIEWER"].LoadFile(name, True)
            return False
        return True

    def status_text(self, txt):
        """Set informational status text.

        Args:
            txt: Status message string.
        """
        if txt:
            self.status["txt"] = "INFO:" + txt
        else:
            self.status["txt"] = ""

    def status_text_error(self, txt):
        """Set error status text.

        Args:
            txt: Error message string.
        """
        self.status["txt"] = "ERROR:" + txt

    def set_status(self, status, url):
        """Update browser status based on loading state.

        Args:
            status: One of LOAD_CONNECT, LOAD_START, LOAD_FINISH_OK,
                    LOAD_FINISH_FAILED.
            url: The URL being loaded.
        """
        if status == self.LOAD_CONNECT:
            if url and url != "None":
                self.status_text("Contacting " + url)
            else:
                self.status_text("Contacting ...")
        elif status == self.LOAD_START:
            if url and url != "None":
                self.status_text("Loading " + url)
        elif status == self.LOAD_FINISH_OK:
            self.status_text("")
            self.href = url
        elif status == self.LOAD_FINISH_FAILED:
            self.status_text_error("Error loading page: " + url)

    def progress_changed(self, progress):
        """Update loading progress indicator.

        Args:
            progress: Progress percentage (0-100).
        """
        self.progress = progress
        if progress < 100:
            self.status["progress"] = progress
            self.status["txt"] = "Loading: %d%%" % progress
        else:
            self.status["progress"] = -1

    def new_win0(self):
        """Open a new empty browser window.

        Returns:
            The new browser control.
        """
        okno = (
            wx.GetApp()
            .GetTopWindow()
            .new_main_page("^standard/webview/widget_web.html", "")
        )
        return okno.body.WEB

    def new_win(self, bstr_url):
        """Open a URL in a new browser window.

        Args:
            bstr_url: URL to open.

        Returns:
            True on success.
        """
        okno = (
            wx.GetApp()
            .GetTopWindow()
            .new_main_page("^standard/webview/widget_web.html", bstr_url)
        )
        okno.body.WEB.go(bstr_url)
        return True

    def new_child(self, bstr_url):
        """Open a URL in a new child page.

        Args:
            bstr_url: URL to open, may contain bestwidth/bestheight parameters.

        Returns:
            True on success.
        """
        okno = self.get_parent_form().any_parent_command(
            "new_child_page", "^standard/webview/widget_web.html"
        )
        dx, dy = 800, 600
        if "bestwidth" in bstr_url or "bestheight" in bstr_url:
            url_get = bstr_url.split("?")
            if len(url_get) > 1:
                for param in url_get[1].split("&"):
                    parts = param.split("=")
                    if len(parts) == 2:
                        if parts[0] == "bestwidth":
                            dx = int(parts[1])
                        elif parts[0] == "bestheight":
                            dy = int(parts[1])
        okno.body.SetBestSize((dx, dy))
        okno.body.WEB.Go(bstr_url)
        return True

    def set_title(self, title):
        """Set the browser tab title.

        Args:
            title: Title string (truncated to 30 chars if longer).
        """
        if title:
            title2 = title if len(title) < 32 else title[:30] + "..."
        else:
            title2 = "Empty page"
        if hasattr(self.get_parent_form(), "any_parent_command"):
            self.get_parent_form().any_parent_command(
                "change_notebook_page_title", title2
            )

    def get_status(self):
        """Get the current browser status dictionary.

        Returns:
            Status dict with keys: stat, progress, txt, address.
        """
        return self.status

    def go(self, href):
        """Navigate to the given URL or search query.

        Handles various URL formats:
        - Full URLs with scheme
        - URLs without scheme (prepends http://)
        - Search queries with spaces (uses Google search)
        - Local 127.0.0.2 URLs (loads via local request)

        Args:
            href: URL or search query string.
        """
        href2 = href.strip()
        is_search = False
        if " " in href2:
            is_search = True
        if "localhost" not in href2 and "." not in href2:
            is_search = True

        if not is_search:
            url = href
            if "://" in url:
                if "127.0.0.2" in url:
                    s = self._local_request(url + "&only_content=1")
                    self.load_str(s)
                else:
                    self.load_url(url)
            else:
                if "." in url:
                    self.load_url("http://" + url)
                else:
                    self.load_url("https://www.google.pl/search?q=" + url)

            if hasattr(self.get_parent_form(), "go_event"):
                self.get_parent_form().go_event(url)
        elif href2:
            q = urllib.parse.quote(href2)
            self.load_url("https://www.google.pl/search?q=" + q)

    def on_key_pressed(self, event):
        """Handle key press events. Override in subclass."""
        event.Skip()

    def on_status_message(self, event):
        """Handle status bar message updates from the browser.

        Args:
            event: Event containing the status message string.
        """
        self.status_text(event.GetString())

    def on_address_changed(self, event):
        """Handle URL address bar changes. Override in subclass."""
        pass

    def on_load_start(self, event):
        """Handle page load start event.

        Args:
            event: Event containing the URL being loaded.
        """
        self.set_status(self.LOAD_START, event.GetString())

    def on_load_end(self, event):
        """Handle page load completion. Triggers PDF rendering if needed.

        Args:
            event: Event containing the loaded URL.
        """
        self.set_status(self.LOAD_FINISH_OK, event.GetString())
        if hasattr(self.get_parent_form(), "loaded_event"):
            self.get_parent_form().loaded_event()

        if self.pdf:
            try:
                if self.pdf.startswith("file://"):
                    if wx.Platform == "__WXMSW__":
                        path = self.pdf.replace("file:///", "")
                    else:
                        path = self.pdf.replace("file://", "")
                    with open(path, "rb") as f:
                        buf = b64encode(f.read()).decode("utf-8")
                    cmd = JAVASCRIPT_CODE % buf
                    self.execute_javascript(cmd)
                else:
                    cmd = 'PDFView.open("%s", 0);' % self.pdf
                    self.execute_javascript(cmd)
            except Exception:
                pass
            finally:
                self.pdf = None

    def on_load_error(self, event):
        """Handle page load error.

        Args:
            event: Event containing the failed URL.
        """
        self.set_status(self.LOAD_FINISH_FAILED, event.GetString())

    def on_title_changed(self, event):
        """Handle page title change. Intercepts command titles starting with ':'.

        Args:
            event: Event containing the new title string.
        """
        event.Skip()
        title = event.GetString()
        if title.startswith(":") and title != ":":
            self.run_command_from_js(title[1:])
        else:
            self.set_title(title)

    def on_progress(self, event):
        """Handle loading progress events. Override in subclass."""
        pass

    def on_add_bookmark(self, event):
        """Handle add bookmark request. Override in subclass."""
        if hasattr(self.get_parent_form(), "addbookmark_event"):
            self.get_parent_form().addbookmark_event()

    def get_parent_form(self):
        """Get the parent form. Override in subclass.

        Returns:
            Parent form object or None.
        """
        return None

    def load_url(self, url, cookies=None):
        """Load a URL. Override in subclass."""
        pass

    def load_str(self, data, base=None):
        """Load HTML string. Override in subclass."""
        pass

    def on_back(self, event):
        """Navigate back. Override in subclass."""
        pass

    def on_forward(self, event):
        """Navigate forward. Override in subclass."""
        pass

    def on_stop(self, event):
        """Stop loading. Override in subclass."""
        pass

    def on_refresh(self, event):
        """Refresh page. Override in subclass."""
        pass

    def can_go_back(self):
        """Check if back navigation is available. Override in subclass."""
        return False

    def can_go_forward(self):
        """Check if forward navigation is available. Override in subclass."""
        return False

    def can_stop(self):
        """Check if loading can be stopped.

        Returns:
            True if a page is currently loading.
        """
        return self.progress < 100

    def can_refresh(self):
        """Check if page can be refreshed.

        Returns:
            Always True for base implementation.
        """
        return True

    def can_addbookmark(self):
        """Check if current page can be bookmarked.

        Returns:
            Always True for base implementation.
        """
        return True

    def execute_javascript(self, script):
        """Execute JavaScript. Override in subclass."""
        pass

    def on_source(self, event):
        """View page source. Override in subclass."""
        pass

    def on_edit(self, event):
        """Toggle edit mode. Override in subclass."""
        pass

    def value_to_elem(self, selector, s):
        """Set the HTML content of a DOM element.

        Args:
            selector: jQuery selector for the target element.
            s: Bytes content to inject.
        """
        if isinstance(s, bytes):
            s = s.decode("utf-8")
        buf = urllib.parse.quote(s, safe="~@#$&()*!+=:;,.?/'")
        cmd = '$("%s").html(decodeURI("%s"));' % (selector, buf)
        self.execute_javascript(cmd)

    def value_to_var(self, var, s):
        """Set a JavaScript variable value.

        Args:
            var: JavaScript variable name.
            s: Bytes content to assign.
        """
        if isinstance(s, bytes):
            s = s.decode("utf-8")
        buf = urllib.parse.quote(s, safe="~@#$&()*!+=:;,.?/'")
        cmd = '%s = decodeURI("%s");' % (var, buf)
        self.execute_javascript(cmd)

    def run_command_from_js(self, cmd):
        """Route a command received from JavaScript to the appropriate handler.

        Supported commands:
            - href_to_elem: Load URL content into a DOM element
            - href_to_var: Load URL content into a JS variable
            - run_js: Execute arbitrary JavaScript
            - python: Execute Python code
            - ajax_get: Perform AJAX GET via local request
            - ajax_post: Perform AJAX POST via local request
            - action: Trigger an action

        Args:
            cmd: Command string with parameters separated by '??'.
        """
        l = split2(cmd, "??")
        if l[0] == "href_to_elem":
            x = split2(l[1], "??")
            s = self._local_request(x[0])
            self.value_to_elem(x[1], s)
        elif l[0] == "href_to_var":
            if "?" in l[1]:
                x = l[1].split("?")
                href, parm = x[0], x[1]
            else:
                href, parm = l[1], None
            s = self._local_request(href, parm)
            self.value_to_var(l[2], s)
        elif l[0] == "run_js":
            self.execute_javascript(l[1])
        elif l[0] == "python":
            self.GetParent().exec_code(l[1])
        elif l[0] == "ajax_get":
            if l[1].startswith("static:/"):
                x = os.path.join(l[1].replace("static:/", wx.GetApp().root_path))
                try:
                    with open(x, "rt") as f:
                        txt = b64encode(f.read().encode("utf-8")).decode("utf-8")
                except Exception:
                    txt = ""
            else:
                txt = b64encode(self._local_request(l[1])).decode("utf-8")
            fun_id = l[1].split("?")[0]
            if "//127.0.0.2" in fun_id:
                fun_id = fun_id.split("//127.0.0.2")[1]
            cmd = """window.ajax_get_response_fun['%s'](window.atob("%s"));""" % (
                fun_id,
                txt,
            )
            self.execute_javascript(cmd)
        elif l[0] == "ajax_post":
            x = split2(l[1], "??")
            parm = b64decode(x[1].encode("utf-8")).decode("utf-8")
            s = self._local_request(x[0], parm)
            txt = b64encode(s).decode("utf-8")
            fun_id = x[0].split("?")[0]
            if "//127.0.0.2" in fun_id:
                fun_id = fun_id.split("//127.0.0.2")[1]
            cmd = (
                """window.ajax_get_response_fun['%s']("""
                """decodeURIComponent(escape(window.atob("%s"))));""" % (fun_id, txt)
            )
            self.execute_javascript(cmd)

    def clear_history(self):
        """Clear the browser navigation history. Override in subclass."""
        pass

    def _local_request(self, uri, parm=None):
        """Make a local HTTP request through the application's HTTP client.

        Args:
            uri: Request URI.
            parm: Optional request parameters.

        Returns:
            Response bytes from the local request.
        """
        http = wx.GetApp().get_http(self)
        response = http.get(self, uri, user_agent="embeded", parm=parm)
        return response.ptr()

    def _get_http_file(self, uri):
        """Resolve a local HTTP URI to content or file path.

        Handles various 127.0.0.2 URI schemes:
        - /data URIs with base64 encoded content
        - /fonts/ URIs for font files
        - /file/ URIs for direct file access
        - /static URIs for static files
        - /site_media/ URIs for media files
        - Command URIs starting with /?:

        Args:
            uri: The full URI to resolve.

        Returns:
            Tuple of (content_bytes, file_path) where one is None.
        """
        if not uri.startswith("http://127.0.0.2"):
            return (None, None)

        if uri.startswith("http://127.0.0.2/data") and "?" in uri:
            data = split2(uri, "?")
            s = b64decode(data[1].encode("utf-8"))
            return (s, None)
        elif uri.startswith("http://127.0.0.2/fonts/"):
            if uri.startswith("http://127.0.0.2/fonts/fontawesome"):
                uri2 = uri.replace(
                    "127.0.0.2/fonts/",
                    "127.0.0.2/static/fonts/fork-awesome/fonts/",
                )
            else:
                uri2 = uri.replace(
                    "127.0.0.2/fonts/",
                    "127.0.0.2/static/themes/bootstrap-material-design/fonts/",
                )
        elif uri.startswith("http://127.0.0.2/file/"):
            return (None, uri.replace("http://127.0.0.2/file/", ""))
        else:
            uri2 = uri

        if "/images/ui" in uri2:
            uri2 = (
                "/static/themes/bootstrap/images/ui"
                + uri2.split("/images/ui")[1].split("#")[0]
            )

        if uri.startswith("http://127.0.0.2/static") and "?" not in uri:
            path = uri.replace("http://127.0.0.2", "")
            return (None, path)
        elif "/site_media/" in uri and "?" not in uri:
            path = wx.GetApp().cwd + uri.replace("http://127.0.0.2", "").replace(
                "site_media", "media"
            )
            return (None, path)
        elif uri.startswith("http://127.0.0.2/?:"):
            self.run_command_from_js(uri.replace("http://127.0.0.2/?:", ""))
            return ("", None)
        else:
            s = self._local_request(uri2)
            return (s, None)

    def show_error(self, title, description):
        """Display an error message. Override in subclass.

        Args:
            title: Error title.
            description: Error description text.
        """
        pass
        print("ERROR: ", title)
        print(description)

    def WebBack(self):
        return self.on_back(None)

    def WebForward(self):
        return self.on_forward(None)

    def CanWebBack(self):
        return self.can_go_back()

    def CanWebForward(self):
        return self.can_go_forward()
