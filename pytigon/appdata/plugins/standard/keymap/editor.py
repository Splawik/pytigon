import wx
from pytigon_lib.schtools.tools import extend_fun_to

def init_control(ctrl):
    if 'keymap' in ctrl.param and ctrl.param['keymap'] == 'standard':
        @extend_fun_to(ctrl)
        def __ext_init__(self):
            aTable = [
                (wx.ACCEL_ALT, ord('J'), self.on_down),
                (wx.ACCEL_ALT, ord('K'), self.on_up),
                (wx.ACCEL_ALT, ord('H'), self.on_left),
                (wx.ACCEL_ALT, ord('L'), self.on_right),

                (wx.ACCEL_ALT, ord('N'), self.on_home),
                (wx.ACCEL_ALT, ord(';'), self.on_end),

                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('L'), self.on_next_word),
                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('H'), self.on_prev_word),

                (wx.ACCEL_CTRL, ord('K'), self.on_top),
                (wx.ACCEL_CTRL, ord('J'), self.on_bottom),

                (wx.ACCEL_ALT, ord('I'), self.on_start_sel),
                (wx.ACCEL_ALT, ord('C'), self.on_copy),
                (wx.ACCEL_ALT, ord('P'), self.on_paste),
                (wx.ACCEL_ALT, ord('X'), self.on_delete),
                (wx.ACCEL_ALT, ord('Z'), self.on_undo),

                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('J'), self.on_page_down),
                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('K'), self.on_page_up),

                (wx.ACCEL_ALT, wx.WXK_RETURN, self.on_line_next),
            ]
            self.GetParent().set_acc_key_tab(self, aTable)
            self.start_sel = None

        @extend_fun_to(ctrl)
        def on_start_sel(self, event):
            if self.start_sel:
                self.start_sel = None
                pos =  self.GetCurrentPos()
                self.SetSelection(pos,pos)
            else:
                self.start_sel =  self.GetCurrentPos()

        @extend_fun_to(ctrl)
        def on_copy(self, event):
            if self.start_sel != None:
                pos = self.GetCurrentPos()
                self.Copy()
                self.SetSelection(pos, pos)
                self.start_sel = None
            else:
                self.Copy()

        @extend_fun_to(ctrl)
        def on_paste(self, event):
            self.Paste()
            self.start_sel = None

        @extend_fun_to(ctrl)
        def _cmd(self, cmd1, cmd2):
            if self.start_sel != None:
                cmd2()
            else:
                cmd1()
            self.EnsureCaretVisible()

        @extend_fun_to(ctrl)
        def on_down(self, event):
            self._cmd(self.LineDown, self.LineDownExtend)

        @extend_fun_to(ctrl)
        def on_up(self, event):
            self._cmd(self.LineUp, self.LineUpExtend)

        @extend_fun_to(ctrl)
        def on_page_down(self, event):
            self._cmd(self.PageDown, self.PageDownExtend)

        @extend_fun_to(ctrl)
        def on_page_up(self, event):
            self._cmd(self.PageUp, self.PageUpExtend)

        @extend_fun_to(ctrl)
        def on_home(self, event):
            self._cmd(self.VCHome, self.VCHomeExtend)

        @extend_fun_to(ctrl)
        def on_end(self, event):
            self._cmd(self.LineEnd, self.LineEndExtend)

        @extend_fun_to(ctrl)
        def on_left(self, event):
            self._cmd(self.CharLeft, self.CharLeftExtend)

        @extend_fun_to(ctrl)
        def on_right(self, event):
            self._cmd(self.CharRight, self.CharRightExtend)

        @extend_fun_to(ctrl)
        def on_next_word(self, event):
            self._cmd(self.WordRight, self.WordRightExtend)

        @extend_fun_to(ctrl)
        def on_prev_word(self, event):
            self._cmd(self.WordLeft, self.WordLeftExtend)

        @extend_fun_to(ctrl)
        def on_top(self, event):
            self._cmd(self.DocumentStart, self.DocumentStartExtend)

        @extend_fun_to(ctrl)
        def on_bottom(self, event):
            self._cmd(self.DocumentEnd, self.DocumentEndExtend)

        @extend_fun_to(ctrl)
        def on_delete(self, event):
            start,end = self.GetSelection()
            if start==end:
                pos = self.GetCurrentPos()+1
                self.SetCurrentPos(pos)
                self.SetSelection(pos, pos)
                self.DeleteBack()
                self.EnsureCaretVisible()
            else:
                self.DeleteBack()
            self.start_sel = None

        @extend_fun_to(ctrl)
        def on_undo(self, event):
            self.Redo()

        @extend_fun_to(ctrl)
        def on_line_next(self, event):
            self.LineEnd()
            self._enter_key()
