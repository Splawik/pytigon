"""Console plugin for Pytigon.

Provides a basic CONSOLE panel with an HTML output area and
text input field.
"""

import wx
import wx.html


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register the Console control in the global control registry.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    class Console(wx.Panel):
        """Simple console panel with HTML display and text input."""

        def __init__(self, parent, **kwds):
            """Initialize the console panel.

            Args:
                parent: Parent window.
                **kwds: Configuration keywords (supports 'name').
            """
            name = kwds.pop("name", "CONSOLE")
            SchBaseCtrl.__init__(self, parent, kwds)
            wx.Panel.__init__(self, parent, name=name)
            html = wx.html.HtmlWindow(self)
            html.SetPage("Hello world " * 6)
            text = wx.TextCtrl(self)
            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(html, 1, wx.EXPAND)
            box.Add(text, 0, wx.EXPAND)
            self.SetSizer(box)
            box.Fit(self)

    pytigon_gui.guictrl.ctrl.CONSOLE = Console
