"""WebView browser plugin for Pytigon using wx.html2 backend.

Provides an embedded web browser control (HTML2) based on wx.html2.WebView,
with support for local request interception, script message handling, and
navigation controls.
"""

import base64
import json
import os

from django.conf import settings

from pytigon.pytigon_request import request


def init_plugin_web_view(
    app, mainframe, desktop, mgr, menubar, toolbar, accel, base_web_browser
):
    """Initialize the wx.html2 WebView-based browser plugin.

    Args:
        app: The wx application instance.
        mainframe: Main application frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
        base_web_browser: Base browser mixin class providing shared functionality.

    Returns:
        None
    """
    import wx.html2

    import pytigon_gui.guictrl.ctrl
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    from pytigon_lib.schindent.indent_tools import norm_html

    # Workaround for DMA-BUF renderer issues on Linux
    os.environ.setdefault("WEBKIT_DISABLE_DMABUF_RENDERER", "1")

    class BaseBrowser(SchBaseCtrl, base_web_browser):
        """wx.html2.WebView-based embedded browser with local request handling."""

        logged = False

        def Init(self, parent, **kwds):
            """Initialize the browser control.

            Args:
                parent: Parent window.
                **kwds: Keyword arguments for control configuration.
            """
            kwds["style"] = wx.TRANSPARENT_WINDOW | wx.WANTS_CHARS
            SchBaseCtrl.__init__(self, parent, kwds)
            base_web_browser.__init__(self)

            self.loaded = True
            self.next_in_new_win = False
            self.page_loaded = False

            self.redirect_to_html = [None, None]
            self.redirect_to_local = True
            self.last_status_txt = ""
            if hasattr(self.GetParent(), "any_parent_command"):
                self.GetParent().any_parent_command("set_handle_info", "browser", self)

            self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)
            self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_web_view_loaded, self)
            self.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, self.on_new_window, self)
            self.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, self.on_title_changed, self)
            self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigating, self)
            self.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.on_error, self)
            self.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.on_received)
            self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

            self.edit = False

            if hasattr(self.GetParent(), "any_parent_command"):
                self.GetParent().any_parent_command("show_info")
            self.after_init()

        def on_destroy(self, event):
            """Handle window destruction - mark browser as unloaded."""
            self.loaded = False
            event.Skip()

        def on_navigating(self, event):
            """Handle navigation events - intercept local commands.

            Args:
                event: The navigation event.
            """
            url = event.GetURL()
            if url.startswith("http://127.0.0.2/?:"):
                event.Veto()
                self.run_command_from_js(url[21:])
            else:
                if self.next_in_new_win and wx.GetKeyState(wx.WXK_CONTROL):
                    self.next_in_new_win = False
                    event.Veto()
                    self.new_win(event.GetURL())
                else:
                    self.next_in_new_win = False
                    self.page_loaded = False
                    event.Skip()

        def on_received(self, event):
            """Handle script messages received from JavaScript.

            Processes AJAX requests from the web page, forwarding them
            to the local request handler and returning results as base64.

            Args:
                event: The script message event containing JSON data.
            """
            try:
                msg = json.loads(event.GetString())
            except (json.JSONDecodeError, ValueError):
                return

            if "action" in msg:
                try:
                    if msg["action"] == "get":
                        ret = request(msg["url"], None, user_agent="webviewembeded")
                    else:
                        ret = request(
                            msg["url"], msg.get("params"), user_agent="webviewembeded"
                        )
                    content = base64.b64encode(ret.ptr()).decode("utf-8")
                    script = f"window.callback_from_python({msg['callback_id']}, '{content}')"
                    self.RunScriptAsync(script)
                except Exception:
                    pass

        def on_error(self, event):
            """Handle web view navigation errors.

            Args:
                event: The error event.
            """
            message = f"{event.GetURL()}\n{event.GetString()}"
            self.show_error("WebView error", message)
            event.Skip()

        def on_web_view_loaded(self, event):
            """Handle page load completion.

            Args:
                event: The load completion event.
            """
            self.page_loaded = True

            ev = wx.CommandEvent()
            try:
                ev.SetString(event.GetURL().decode("utf-8"))
            except (AttributeError, UnicodeDecodeError):
                ev.SetString(event.GetURL())
            self.on_address_changed(ev)
            self.on_load_end(ev)
            event.Skip()
            self.SetFocus()

        def on_web_view_error(self, event):
            """Handle web view errors (logging only)."""
            print("on_web_view_error:", event.GetURL())
            event.Skip()

        def on_new_window(self, event):
            """Handle requests to open new browser windows.

            Args:
                event: The new window event.
            """
            url = event.GetURL()
            if url.startswith("http://127.0.0.2/?:"):
                event.Veto()
                if url != "http://127.0.0.2/?:":
                    self.run_command_from_js(url[19:])
            else:
                self.new_win(event.GetURL())
                event.Skip()

        def progress_change(self, progress, max_progress):
            """Update loading progress indicator.

            Args:
                progress: Current progress value.
                max_progress: Maximum progress value.

            Returns:
                Result from progress_changed callback.
            """
            if max_progress == 0:
                max_progress = 100
            progress2 = int(progress * 100 / max_progress) if progress >= 0 else 100
            return self.progress_changed(progress2)

        def load_url(self, url, cookies=None):
            """Load a URL in the browser.

            Args:
                url: The URL to load.
                cookies: Optional cookies (unused in wx backend).
            """
            self.LoadURL(url)

        def load_str(self, data, base=None):
            """Load HTML string content into the browser.

            Args:
                data: HTML string to load.
                base: Optional base URL (unused in wx backend).
            """
            self.LoadURL("about:blank")
            if wx.Platform == "__WXMSW__":
                path = os.path.join(settings.TEMP_PATH, "index.html")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(data)
                url = "file:///" + path.replace("\\", "/")
                self.LoadURL(url)
            else:
                self.SetPage(data, "http://127.0.0.5")

        def on_back(self, event):
            self.GoBack()

        def on_forward(self, event):
            self.GoForward()

        def on_stop(self, event):
            self.Stop()

        def on_refresh(self, event):
            self.Reload()

        def execute_javascript(self, script):
            """Execute JavaScript in the browser context.

            Args:
                script: JavaScript code to execute.
            """
            self.RunScript(script)

        def on_source(self, event):
            """Open page source in an editor tab."""
            okno = self.GetParent().new_main_page(
                "^standard/editor/editor.html",
                self.GetParent().GetTab().title + " - page source",
                None,
            )
            okno.body["EDITOR"].SetValue(norm_html(self.GetPageSource()))
            okno.body["EDITOR"].GotoPos(0)

        def on_edit(self, event):
            """Toggle content editable mode."""
            self.edit = not self.edit
            self.SetEditable(self.edit)

        def can_go_back(self):
            return self.CanGoBack()

        def can_go_forward(self):
            return self.CanGoForward()

        def clear_history(self):
            self.ClearHistory()

    def Html2(parent, **kwds):
        """Create a new HTML2 browser control (factory function).

        Constructs a wx.html2.WebView, dynamically mixes in BaseBrowser
        behavior, and configures script message handling.

        Args:
            parent: Parent window.
            **kwds: Configuration keywords (name, size, url, backend, etc.).

        Returns:
            Configured WebView-based browser control.
        """
        kwds2 = {}
        kwds2["name"] = kwds["name"]
        kwds2["size"] = kwds["size"]
        kwds2["style"] = wx.BORDER_NONE
        if "backend" in kwds:
            kwds2["backend"] = kwds["backend"]

        if "url" in kwds:
            kwds2["url"] = kwds["url"]
        wb = wx.html2.WebView.New(parent, **kwds2)
        wb.__class__ = type("BrowserCtrl", (wb.__class__, BaseBrowser), {})
        wb.AddScriptMessageHandler("wx_msg")
        wb.EnableAccessToDevTools(enable=True)
        wb.Init(parent, **kwds)

        return wb

    pytigon_gui.guictrl.ctrl.HTML2 = Html2
