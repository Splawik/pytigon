"""Interactive find plugin for Pytigon.

Overrides the STYLEDTEXT on_key_pressed handler to add keyboard
shortcuts for find (Ctrl+F), go-to (Ctrl+G), and replace (Ctrl+H)
panels.
"""


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Install keyboard shortcuts for search panels in styled text controls.

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

    old_on_key_pressed = pytigon_gui.guictrl.ctrl.STYLEDTEXT.on_key_pressed

    def on_key_pressed(self, event):
        """Enhanced key handler with search shortcuts.

        Args:
            event: Key event.
        """
        key = event.GetKeyCode()
        if key == 70 and event.ControlDown():
            self.GetParent().new_child_page(
                "^standard/ifind/ifindpanel.html", title="Find"
            )
        elif key == 71 and event.ControlDown():
            self.GetParent().new_child_page(
                "^standard/ifind/gotopanel.html", title="Go"
            )
        elif key == 72 and event.ControlDown():
            self.GetParent().new_child_page(
                "^standard/ifind/ireplacepanel.html", title="Replace"
            )
        else:
            if old_on_key_pressed:
                old_on_key_pressed(self, event)

    pytigon_gui.guictrl.ctrl.STYLEDTEXT.on_key_pressed = on_key_pressed
