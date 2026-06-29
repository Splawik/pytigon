"""Keymap plugin for grid/table controls.

Provides Vi-style alternative key bindings for grid navigation
and editing operations.
"""

import wx
from pytigon_lib.schtools.tools import extend_fun_to


def init_control(ctrl_param):
    """Install alternative key bindings on a grid/table control.

    Args:
        ctrl_param: The grid or table control to enhance.
    """

    @extend_fun_to(ctrl_param)
    def __ext_init__(self):
        """Initialize key bindings - called during control initialization."""
        ctrl = ctrl_param.grid if ctrl_param.tag == "ctrltable" else ctrl_param

        @extend_fun_to(ctrl)
        def __ext_init__(self):
            """Inner initialization: register key bindings on the grid."""
            self.grid_aTable = [
                (wx.ACCEL_ALT, ord("J"), self.on_down),
                (wx.ACCEL_ALT, ord("K"), self.on_up),
                (wx.ACCEL_ALT, ord("H"), self.on_left),
                (wx.ACCEL_ALT, ord("L"), self.on_right),
                (wx.ACCEL_ALT, ord("N"), self.on_home),
                (wx.ACCEL_ALT, ord(";"), self.on_end),
                (wx.ACCEL_CTRL, ord("K"), self.on_top),
                (wx.ACCEL_CTRL, ord("J"), self.on_bottom),
                (wx.ACCEL_ALT, ord("X"), self.on_delete),
                (wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("J"), self.on_page_down),
                (wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord("K"), self.on_page_up),
            ]
            ctrl_param.GetParent().set_acc_key_tab(ctrl_param, self.grid_aTable)

        @extend_fun_to(ctrl)
        def on_down(self, event):
            """Move cursor down one row (Alt+J)."""
            row = self.GetGridCursorRow()
            if row + 1 < self.GetTable().GetNumberRows():
                self.MoveCursorDown(False)

        @extend_fun_to(ctrl)
        def on_up(self, event):
            """Move cursor up one row (Alt+K)."""
            if self.GetGridCursorRow() > 0:
                self.MoveCursorUp(False)

        @extend_fun_to(ctrl)
        def on_page_down(self, event):
            """Move cursor down one page (Alt+Shift+J)."""
            self.MovePageDown()

        @extend_fun_to(ctrl)
        def on_page_up(self, event):
            """Move cursor up one page (Alt+Shift+K)."""
            self.MovePageUp()

        @extend_fun_to(ctrl)
        def on_home(self, event):
            """Move cursor to first column (Alt+N)."""
            self.SetGridCursor(self.GetGridCursorRow(), 0)

        @extend_fun_to(ctrl)
        def on_end(self, event):
            """Move cursor to last column (Alt+;)."""
            self.SetGridCursor(
                self.GetGridCursorRow(),
                self.GetTable().GetNumberCols() - 1,
            )

        @extend_fun_to(ctrl)
        def on_left(self, event):
            """Move cursor left one column (Alt+H)."""
            if self.GetGridCursorCol() > 0:
                self.MoveCursorLeft(False)

        @extend_fun_to(ctrl)
        def on_right(self, event):
            """Move cursor right one column (Alt+L)."""
            if self.GetGridCursorCol() + 1 < self.GetTable().GetNumberCols():
                self.MoveCursorRight(False)

        @extend_fun_to(ctrl)
        def on_top(self, event):
            """Move cursor to first row (Ctrl+K)."""
            self.goto_first_row()

        @extend_fun_to(ctrl)
        def on_bottom(self, event):
            """Move cursor to last row (Ctrl+J)."""
            self.goto_last_row()

        @extend_fun_to(ctrl)
        def on_delete(self, event):
            """Delete current row (Alt+X) if not in readonly mode."""
            if self.typ in (self.VIEW, self.GET_ID):
                if not self.readonly:
                    self.action("delete")
                event.Skip()

        # Trigger inner initialization
        ctrl.__ext_init__()
