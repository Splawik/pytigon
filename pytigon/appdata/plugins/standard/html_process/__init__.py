import wx


def replace_colors(win, html):
    c_caption = \
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION).GetAsString(wx.C2S_HTML_SYNTAX)
    c_text = \
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT).GetAsString(wx.C2S_HTML_SYNTAX)
    return html.replace('#E9E0E2', c_caption).replace('#090002', c_text)


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from pytigon_gui.guiframe.form import install_pre_process_lib
    install_pre_process_lib(replace_colors)


