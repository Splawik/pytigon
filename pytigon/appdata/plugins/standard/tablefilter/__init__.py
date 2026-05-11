"""Table filter plugin for Pytigon.

Adds keyboard shortcuts to grid/table controls for filtering:
- Ctrl+F: Open filter panel
- Numpad +/=: Add filter
- Numpad -/-: Add subtract filter
"""

import wx


def _find_ancestor_with_method(win, method_name):
    """Find the nearest ancestor that has the given method.

    Args:
        win: Starting window.
        method_name: Method name to search for.

    Returns:
        The ancestor window with the method, or None.
    """
    while win is not None and not hasattr(win, method_name):
        win = win.GetParent()
    return win


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Install filter keyboard shortcuts on table grid controls.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    import pytigon_gui.guictrl.grid.grid

    old_on_key_down = pytigon_gui.guictrl.grid.grid.SchTableGrid.on_key_down

    def on_key_down(self, event):
        """Enhanced key handler with filter shortcuts.

        Args:
            event: Key event.
        """
        key = event.KeyCode
        if key in (ord("F"), ord("f")) and event.ControlDown():
            win = _find_ancestor_with_method(self.GetParent(), "new_child_page")
            if win:
                win.new_child_page(
                    "^standard/tablefilter/tablefilter.html", title="Filter"
                )
        elif key in (wx.WXK_NUMPAD_ADD, 61):
            win = _find_ancestor_with_method(self.GetParent(), "new_child_page")
            if win:
                win.new_child_page("^standard/tablefilter/addfilter.html", title="Add")
        elif key in (wx.WXK_NUMPAD_SUBTRACT, ord("-")):
            win = _find_ancestor_with_method(self.GetParent(), "new_child_page")
            if win:
                p = win.new_child_page(
                    "^standard/tablefilter/addfilter.html", title="Add"
                )
                p.body.StyleSubtract()
        else:
            if old_on_key_down:
                old_on_key_down(self, event)

    pytigon_gui.guictrl.grid.grid.SchTableGrid.on_key_down = on_key_down
