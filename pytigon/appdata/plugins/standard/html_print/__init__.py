"""HTML print plugin for Pytigon.

Provides the HTMLPRINT control - an HTML print preview widget
that integrates HtmlPreviewCanvas with SchBaseCtrl.
"""

import wx


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register the HTML print control and printout factory.

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
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl

    from .printframework import HtmlPreviewCanvas, get_printout

    class Htmlprint(HtmlPreviewCanvas, SchBaseCtrl):
        """HTML print preview control combining canvas and base control."""

        def __init__(self, parent, *args, **kwds):
            """Initialize the HTML print control.

            Args:
                parent: Parent window.
                *args: Positional arguments.
                **kwds: Keyword arguments.
            """
            SchBaseCtrl.__init__(self, parent, kwds)
            HtmlPreviewCanvas.__init__(self, parent, **kwds)

    pytigon_gui.guictrl.ctrl.HTMLPRINT = Htmlprint
    wx.GetApp().get_printout = get_printout
