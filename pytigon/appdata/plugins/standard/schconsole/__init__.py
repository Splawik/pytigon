import wx
import wx.html


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    class Console(wx.Panel):
        def __init__(self, parent, **kwds):
            if 'name' in kwds:
                name = kwds['name']
                del kwds['name']
            else:
                name = 'CONSOLE'
            self.obj = SchBaseCtrl(self, parent, kwds)
            wx.Panel.__init__(self, parent, name=name)
            html = wx.html.HtmlWindow(self)
            html.SetPage('Hello world Hello world Hello world Hello world Hello world Hello world')
            text = wx.TextCtrl(self)
            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(html, 1, wx.EXPAND)
            box.Add(text, 0, wx.EXPAND)
            self.SetSizer(box)
            box.Fit(self)

    pytigon_gui.guictrl.ctrl.CONSOLE = Console


