"""Keymap plugin for Pytigon.

Provides Vi-style alternative key bindings for editor and grid controls.
"""

from .editor import init_control as init_control_edit
from .grid import init_control as init_control_grid


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register keymap handlers for text editor and grid controls.

    Installs alternative keyboard navigation bindings on
    styled text and table controls.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    app.register_ctrl_process_fun("ctrlstyledtext", init_control_edit)
    app.register_ctrl_process_fun("ctrlgrid", init_control_grid)
    app.register_ctrl_process_fun("ctrltable", init_control_grid)
