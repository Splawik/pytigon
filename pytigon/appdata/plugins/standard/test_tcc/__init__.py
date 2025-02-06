from . import schtest
import wx

def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    print("tcc plugin - start testing")
    print(schtest.silnia(10))
    print(schtest.passed("test2"))
    schtest.message("end!")
    print("tcc plugin - end testing")

    functions = { 'silnia': schtest.silnia, 'passed': schtest.passed, 'message': schtest.message, }
    app.extern_data['schtest'] = functions

    print("tcc plugin - start testing2")
    context = wx.GetApp().extern_data['schtest']
    print(context['silnia'](10))
    print(context['passed']("test2"))
    context['message']("end!")
    print("tcc plugin - end testing2")
