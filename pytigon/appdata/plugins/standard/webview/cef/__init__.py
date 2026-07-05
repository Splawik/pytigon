"""CEF (Chromium Embedded Framework) browser plugin for Pytigon.

Provides the HTML2 browser control using CEF as the rendering backend.
This is an alternative to the wx.html2 WebView backend.
"""

import wx

from pytigon_gui.guilib.tools import get_colour

CEF_INITIATED = False
TIMER = None


def init_plugin_cef(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    base_web_browser,
):
    """Initialize the CEF-based browser plugin.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
        base_web_browser: Base browser mixin class.

    Returns:
        The cef_shutdown function for cleanup on application exit.
    """
    import pytigon_gui.guictrl.ctrl
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    from pytigon_lib.schindent.indent_tools import norm_html

    from .cefcontrol import CEFControl, cef_shutdown

    class Html2(CEFControl, SchBaseCtrl, base_web_browser):
        """CEF-based embedded browser control."""

        logged = False

        def __init__(self, parent, **kwds):
            """Initialize the CEF browser control.

            Args:
                parent: Parent window.
                **kwds: Configuration keywords (supports 'component' flag).
            """
            wx.GetApp().web_ctrl = self
            self.component = kwds.pop("component", False)
            SchBaseCtrl.__init__(self, parent, kwds)
            kwds["style"] = kwds.get("style", 0) | wx.WANTS_CHARS

            CEFControl.__init__(self, parent, **kwds)

            href = self.href

            base_web_browser.__init__(self)
            if hasattr(self.GetParent(), "any_parent_command"):
                self.GetParent().any_parent_command("set_handle_info", "browser", self)
                self.GetParent().any_parent_command("show_info")

            self.edit = False

            if href is not None:
                self.go(href)

            self.after_init()

        def html_from_str(self, str_body):
            """Wrap HTML body content with the static file prefix.

            Args:
                str_body: HTML body content.

            Returns:
                Complete HTML document string.
            """
            color = get_colour(wx.SYS_COLOUR_3DFACE)
            return (
                (
                    "<!DOCTYPE html><html><head>"
                    f'<base href="{self._static_prefix()}" target="_blank">'
                    f"</head><body bgcolor='{color}'>"
                )
                + str_body
                + "</body></html>"
            )

        def get_shtml_window(self):
            """Get the parent SHTML window.

            Returns:
                Parent window.
            """
            return self.GetParent()

        def _static_prefix(self):
            """Get the file:// URL prefix for static resources.

            Returns:
                File URL prefix string.
            """
            rp = wx.GetApp().root_path
            prefix = "file://" if rp[0] == "/" else "file:///"
            return prefix + rp.replace("\\", "/") + "/"

        def load_str(self, data, base=None):
            """Load an HTML string into the browser.

            Args:
                data: HTML string to load.
                base: Optional base URL for relative links.
            """
            if self.browser:
                if base:
                    self.browser.GetMainFrame().LoadUrl(
                        "data:text/html, "
                        + data.replace("<head>", f'<head><base href="{base}/">')
                    )
                else:
                    self.browser.GetMainFrame().LoadUrl("data:text/html, " + data)
            else:
                wx.CallLater(100, self.load_str, data, base)

        def on_back(self, event):
            if self.browser:
                self.browser.GoBack()

        def on_forward(self, event):
            if self.browser:
                self.browser.GoForward()

        def on_stop(self, event):
            if self.browser:
                self.browser.StopLoad()

        def on_refresh(self, event):
            if self.browser:
                self.browser.Reload()

        def can_go_back(self):
            return self.browser and self.browser.CanGoBack()

        def can_go_forward(self):
            return self.browser and self.browser.CanGoForward()

        def execute_javascript(self, script):
            """Execute JavaScript in the browser.

            Args:
                script: JavaScript code to execute.
            """
            frame = self.browser.GetMainFrame()
            frame.ExecuteJavascript(script)

        def on_source(self, event):
            """Open page source in an editor tab."""
            okno = self.GetParent().new_main_page(
                "^standard/editor/editor.html",
                self.GetParent().GetTab().title + " - page source",
                None,
            )
            okno.body["EDITOR"].SetValue(norm_html(self.browser.GetPageSource()))
            okno.body["EDITOR"].GotoPos(0)

        def on_edit(self, event):
            """Toggle content editable mode."""
            self.edit = not self.edit
            self.browser.SetEditable(self.edit)

    pytigon_gui.guictrl.ctrl.HTML2 = Html2

    return cef_shutdown
