def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import pytigon_gui.guictrl.ctrl
    old_on_key_pressed = pytigon_gui.guictrl.ctrl.STYLEDTEXT.on_key_pressed

    def on_key_pressed(self, event):
        key = event.GetKeyCode()
        if key == 70 and event.ControlDown():
            self.GetParent().new_child_page('^standard/ifind/ifindpanel.html', title='Find')
        if key == 71 and event.ControlDown():
            self.GetParent().new_child_page('^standard/ifind/gotopanel.html', title='Go')
        if key == 72 and event.ControlDown():
            self.GetParent().new_child_page('^standard/ifind/ireplacepanel.html', title='Replace')
        else:
            if old_on_key_pressed:
                old_on_key_pressed(self, event)

    pytigon_gui.guictrl.ctrl.STYLEDTEXT.on_key_pressed = on_key_pressed


