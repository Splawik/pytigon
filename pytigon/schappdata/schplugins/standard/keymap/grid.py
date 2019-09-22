import wx
from pytigon_lib.schtools.tools import extend_fun_to

def init_control(ctrl_param):

    @extend_fun_to(ctrl_param)
    def __ext_init__(self):
        if ctrl_param.tag == 'ctrltable':
            ctrl = ctrl_param.grid
        else:
            ctrl = ctrl_param

        @extend_fun_to(ctrl)
        def __ext_init__(self):

            self.grid_aTable = [
                (wx.ACCEL_ALT, ord('J'), self.on_down),
                (wx.ACCEL_ALT, ord('K'), self.on_up),
                (wx.ACCEL_ALT, ord('H'), self.on_left),
                (wx.ACCEL_ALT, ord('L'), self.on_right),

                (wx.ACCEL_ALT, ord('N'), self.on_home),
                (wx.ACCEL_ALT, ord(';'), self.on_end),

                (wx.ACCEL_CTRL, ord('K'), self.on_top),
                (wx.ACCEL_CTRL, ord('J'), self.on_bottom),

                (wx.ACCEL_ALT, ord('X'), self.on_delete),

                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('J'), self.on_page_down),
                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('K'), self.on_page_up),

            ]
            ctrl_param.GetParent().set_acc_key_tab(ctrl_param, self.grid_aTable)

        @extend_fun_to(ctrl)
        def on_down(self, event):
            row = self.GetGridCursorRow()
            if row+1 < self.GetTable().GetNumberRows():
                self.MoveCursorDown(False)

        @extend_fun_to(ctrl)
        def on_up(self, event):
            row = self.GetGridCursorRow()
            if row > 0:
                self.MoveCursorUp(False)

        @extend_fun_to(ctrl)
        def on_page_down(self, event):
            self.MovePageDown()

        @extend_fun_to(ctrl)
        def on_page_up(self, event):
            self.MovePageUp()

        @extend_fun_to(ctrl)
        def on_home(self, event):
            self.SetGridCursor(self.GetGridCursorRow(), 0)

        @extend_fun_to(ctrl)
        def on_end(self, event):
            self.SetGridCursor(self.GetGridCursorRow(), self.GetNumberRows() - 1)

        @extend_fun_to(ctrl)
        def on_left(self, event):
            col = self.GetGridCursorCol()
            if col > 0:
                self.MoveCursorLeft(False)

        @extend_fun_to(ctrl)
        def on_right(self, event):
            col = self.GetGridCursorCol()
            if col+1 < self.GetTable().GetNumberCols():
                self.MoveCursorRight(False)

        @extend_fun_to(ctrl)
        def on_top(self, event):
            self.goto_first_row()

        @extend_fun_to(ctrl)
        def on_bottom(self, event):
            self.goto_last_row()

        @extend_fun_to(ctrl)
        def on_delete(self, event):
            if self.typ == self.VIEW or self.typ == self.GET_ID:
                if not self.readonly:
                    self.action('delete')
                event.Skip()
                return

        ctrl.__ext_init__()
