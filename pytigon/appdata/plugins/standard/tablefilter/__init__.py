import wx

def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import pytigon_gui.guictrl.grid.grid
    old_on_key_down = pytigon_gui.guictrl.grid.grid.SchTableGrid.on_key_down

    def on_key_down(self, event):
        if (event.KeyCode == ord('F') or event.KeyCode == ord('f')) and event.ControlDown():
            win = self.GetParent()
            while not hasattr(win, 'new_child_page'):
                win = win.GetParent()
            win.new_child_page('^standard/tablefilter/tablefilter.html', title='Filter')
        elif event.KeyCode == wx.WXK_NUMPAD_ADD or event.KeyCode == 61:
            win = self.GetParent()
            while not hasattr(win, 'new_child_page'):
                win = win.GetParent()
            win.new_child_page('^standard/tablefilter/addfilter.html', title='Add'
                             )
        elif event.KeyCode == wx.WXK_NUMPAD_SUBTRACT or event.KeyCode == ord('-'):
            win = self.GetParent()
            while not hasattr(win, 'new_child_page'):
                win = win.GetParent()
            p = win.new_child_page('^standard/tablefilter/addfilter.html', title='Add')
            p.body.StyleSubtract()
        else:
            if old_on_key_down:
                old_on_key_down(self, event)

    pytigon_gui.guictrl.grid.grid.SchTableGrid.on_key_down = on_key_down
