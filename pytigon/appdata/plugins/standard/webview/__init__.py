"""WebView browser plugin for Pytigon.

Provides the COMPONENT factory and HTML2 browser control for
embedded web browsing. Uses the wx.html2 WebView backend by default.
"""

import wx
from .basebrowser import BaseWebBrowser


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Initialize the web browser plugin.

    Registers the COMPONENT control factory and the HTML2 browser
    control using the wx.html2 WebView backend.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    import pytigon_gui.guictrl.ctrl
    from base64 import b64encode

    def Component(parent, **kwds):
        """Create a web component control.

        Fetches the web widget HTML from the server and renders it
        as a base64-encoded data URL in a new HTML2 browser instance.

        Args:
            parent: Parent window.
            **kwds: Configuration keywords.

        Returns:
            Configured HTML2 browser control.
        """
        http = wx.GetApp().get_http(parent)
        response = http.get(
            parent,
            "/schsys/widget_web?browser_type=1",
            user_agent="webviewembeded",
        )
        buf = response.str()
        url = "data:text/html;base64," + b64encode(buf.encode("utf-8")).decode("utf-8")
        obj = pytigon_gui.guictrl.ctrl.HTML2(parent, **kwds)
        obj.load_url(url)
        return obj

    pytigon_gui.guictrl.ctrl.COMPONENT = Component

    from .wxwebview import init_plugin_web_view

    return init_plugin_web_view(
        app,
        mainframe,
        desktop,
        mgr,
        menubar,
        toolbar,
        accel,
        BaseWebBrowser,
    )
