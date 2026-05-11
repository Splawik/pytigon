"""HTML pre-processing plugin for Pytigon.

Provides color replacement for HTML content to match the system
color scheme (inactive caption colors).
"""

import wx


def replace_colors(win, html):
    """Replace hardcoded colors in HTML with system theme colors.

    Args:
        win: Window for context (unused).
        html: HTML string to process.

    Returns:
        HTML string with colors replaced by system theme values.
    """
    c_caption = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION).GetAsString(
        wx.C2S_HTML_SYNTAX
    )
    c_text = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT).GetAsString(
        wx.C2S_HTML_SYNTAX
    )
    return html.replace("#E9E0E2", c_caption).replace("#090002", c_text)


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Install the HTML color pre-processor.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    from pytigon_gui.guiframe.form import install_pre_process_lib

    install_pre_process_lib(replace_colors)
