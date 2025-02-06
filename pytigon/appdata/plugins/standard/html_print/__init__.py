import wx


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl
    from .printframework import HtmlPreviewCanvas, get_printout

    class Htmlprint(HtmlPreviewCanvas, SchBaseCtrl):
        def __init__(self, parent, *args, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            HtmlPreviewCanvas.__init__(self, parent, **kwds)

    pytigon_gui.guictrl.ctrl.HTMLPRINT = Htmlprint
    wx.GetApp().get_printout = get_printout
