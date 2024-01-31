#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import keyword

import wx
import wx.stc as stc



if wx.Platform == '__WXMSW__':
    faces = {
        'times': 'Times New Roman',
        'mono': 'Courier New',
        'helv': 'Arial',
        'other': 'Comic Sans MS',
        'size': 10,
        'size2': 8,
        }
elif wx.Platform == '__WXMAC__':
    faces = {
        'times': 'Times New Roman',
        'mono': 'Courier New',
        'helv': 'Arial',
        'other': 'Comic Sans MS',
        'size': 12,
        'size2': 10,
        }
else:
    faces = {
        'times': 'DejaVu Sans Mono',
        'mono': 'DejaVu Sans Mono',
        'helv': 'DejaVu Sans Mono',
        'other': 'DejaVu Sans Mono',
        'size': 9,
        'size2': 7,
        }


class CodeEditor(stc.StyledTextCtrl):
    def __init__(self, *args, **kwds):
        stc.StyledTextCtrl.__init__(self, *args, **kwds)
        #self.SetKeys(True)
        self.SetCodePage(65001)
        #self.SetCodePage(0)
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetProperty('fold', '1')
        self.SetProperty('tab.timmy.whinge.level', '1')
        self.SetViewWhiteSpace(False)
        self.SetEdgeColumn(78)
        self.SetMargins(2, 2)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, 'white', '#808080')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, 'white', '#808080')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, 'white', '#808080')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, 'white', '#808080')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, 'white', '#808080')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, 'white', '#808080')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, 'white', '#808080')
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.Bind(stc.EVT_STC_UPDATEUI, self.on_update_ui)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.on_margin_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'face:%(helv)s,size:%(size)d' % faces)
        self.StyleClearAll()
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'face:%(helv)s,size:%(size)d' % faces)
        col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        colstr = col.GetAsString(wx.C2S_HTML_SYNTAX)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, 'fore:#000000,back:%s' % colstr)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, 'face:%(other)s' % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, 'fore:#000000,back:#DDDDFF,bold')
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, 'fore:#000000,back:#FFCCCC,bold')
        self.StyleSetSpec(stc.STC_P_DEFAULT, 'fore:#000000,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, 'fore:#007F00,face:%(other)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_NUMBER, 'fore:#007F7F,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_STRING, 'fore:#7F007F,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_CHARACTER, 'fore:#7F007F,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_WORD, 'fore:#00007F,bold,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_TRIPLE, 'fore:#7F0000,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, 'fore:#7F0000,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_CLASSNAME, 'fore:#0000FF,bold,underline,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_DEFNAME, 'fore:#007F7F,bold,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_OPERATOR, 'bold,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, 'fore:#000000,face:%(helv)s,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, 'fore:#7F7F7F,size:%(size)d' % faces)
        self.StyleSetSpec(stc.STC_P_STRINGEOL,
                          'GetCurrentPosfore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d' % faces)
        self.SetCaretForeground('#D00000')
        self.SetCaretWidth(2)
        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        b1 = wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_MENU, (16, 16))
        b2 = wx.ArtProvider.GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_MENU, (16, 16))
        self.RegisterImage(1, b1)
        self.RegisterImage(2, b2)

        self._last_flag = None
        self._last_text = None

    def set_ext(self, ext):
        if ext in EditorObjectMap:
            self.set_language(EditorObjectMap[ext])

    def set_language(self, language):
        try:
            self.langObj = eval(language + '_EditorObject()')
        except:
            self.langObj = None
        if self.langObj:
            self.langObj.set_up_editor(self)
        else:
            try:
                lexer = eval('stc.STC_LEX_' + language)
            except:
                lexer = stc.STC_LEX_AUTOMATIC
            self.SetLexer(lexer)

    def on_key_pressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        if key == 70 and event.ControlDown():
            pass
        elif key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            if event.ShiftDown():
                if hasattr(self.GetParent(), 'on_info_cmd'):
                    self.GetParent().on_info_cmd(self, pos)
            else:
                if hasattr(self.GetParent(), 'on_auto_comp_cmd'):
                    self.GetParent().on_auto_comp_cmd(self, pos)
        elif key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN:
            if self.AutoCompActive():
                event.Skip()
            else:
                self._enter_key()
        elif key == wx.WXK_ESCAPE:
            wx.GetApp().GetTopWindow().OnCloseTab(event)
        elif key == wx.WXK_F3:
            self.on_find_next(event)
        else:
            event.Skip()

    def _enter_key(self):
        (line, space_len) = self.GetCurLine()
        pos = self.GetCurrentPos()
        col = self.GetColumn(pos)
        indent = self.GetLineIndentation(self.GetCurrentLine())
        if space_len > indent:
            space_len = indent
        if line[:col].rstrip()[-1:] == ':':
            space_len += 4
        txt = '\n' + ' ' * space_len
        self.InsertText(pos, txt)
        pos += len(txt)
        self.SetCurrentPos(pos)
        self.SetSelection(pos, pos)

    def on_update_ui(self, evt):
        brace_at_caret = -1
        brace_opposite = -1
        char_before = None
        caret_pos = self.GetCurrentPos()
        if caret_pos > 0:
            char_before = self.GetCharAt(caret_pos - 1)
            style_before = self.GetStyleAt(caret_pos - 1)
        if char_before and chr(char_before) in '[]{}()' and style_before == stc.STC_P_OPERATOR:
            brace_at_caret = caret_pos - 1
        if brace_at_caret < 0:
            char_after = self.GetCharAt(caret_pos)
            style_after = self.GetStyleAt(caret_pos)
            if char_after and chr(char_after) in '[]{}()' and style_after == stc.STC_P_OPERATOR:
                brace_at_caret = caret_pos
        if brace_at_caret >= 0:
            brace_opposite = self.BraceMatch(brace_at_caret)
        if brace_at_caret != -1 and brace_opposite == -1:
            self.BraceBadLight(brace_at_caret)
        else:
            self.BraceHighlight(brace_at_caret, brace_opposite)

    def on_margin_click(self, evt):
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                line_clicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(line_clicked, True)
                        self.Expand(line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(line_clicked):
                            self.SetFoldExpanded(line_clicked, False)
                            self.Expand(line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(line_clicked, True)
                            self.Expand(line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(line_clicked)

    def fold_all(self):
        line_count = self.GetLineCount()
        expanding = True
        for line_num in range(line_count):
            if self.GetFoldLevel(line_num) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(line_num)
                break
        line_num = 0
        while line_num < line_count:
            level = self.GetFoldLevel(line_num)
            if level & stc.STC_FOLDLEVELHEADERFLAG and level\
                 & stc.STC_FOLDLEVELNUMBERMASK == stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(line_num, True)
                    line_num = self.Expand(line_num, True)
                    line_num = line_num - 1
                else:
                    last_child = self.GetLastChild(line_num, -1)
                    self.SetFoldExpanded(line_num, False)
                    if last_child > line_num:
                        self.HideLines(line_num + 1, last_child)
            line_num = line_num + 1

    def expand(self, line, do_expand, force=False, vis_levels=0, level=-1):
        last_child = self.GetLastChild(line, level)
        line = line + 1
        while line <= last_child:
            if force:
                if vis_levels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if do_expand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if vis_levels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, do_expand, force, vis_levels - 1)
                else:
                    if do_expand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, vis_levels - 1)
                    else:
                        line = self.Expand(line, False, force, vis_levels - 1)
            else:
                line = line + 1
        return line

    def preprocess(self, txt):
        if type(txt)==str:
            return txt.replace('\t', ' ' * 4)
        else:
            return txt.replace(b'\t', b' ' * 4)

    def on_find_next(self, event):
        if self._last_text:
            sel = self.GetSelectionEnd()
            if sel >=0:
                self.SetSelectionStart(sel)
            self.SearchAnchor()
            return self.SearchNext(self._last_flag, self._last_text)

    def FindText(self, minPos, maxPos, flags, text):
        self._last_flag = flags
        self._last_text = text
        return stc.StyledTextCtrl.FindText(self, minPos, maxPos, flags, text)

    def SearchNext(self, flags, text):
        self._last_flag = flags
        self._last_text = text
        ret =  stc.StyledTextCtrl.SearchNext(self, flags, text)
        self.EnsureCaretVisible()
        return ret


    def AutoCompGetMaxHeight(self):
        return 16

class PYTHON_EditorObject(object):
    def set_up_editor(self, editor):
        editor.SetLexer(stc.STC_LEX_PYTHON)
        editor.SetKeyWords(0, ' '.join(keyword.kwlist))
        editor.SetProperty('fold', '1')
        editor.SetProperty('tab.timmy.whinge.level', '1')
        editor.SetMargins(2, 2)
        editor.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        editor.SetMarginWidth(1, 40)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


htmlKeywords = \
    'a abbr acronym address applet area b base basefont bdo big blockquote body br button caption center cite code ' \
    'col colgroup dd del dfn dir div dl dt em fieldset font form frame frameset h1 h2 h3 h4 h5 h6 head hr html i ' \
    'iframe img input ins isindex kbd label legend li link map menu meta noframes noscript object ol optgroup ' \
    'option p param pre q s samp script select small span strike strong style sub sup table tbody td textarea tfoot ' \
    'th thead title tr tt u ul var xml xmlns abbr accept-charset accept accesskey action align alink alt archive ' \
    'axis background bgcolor border cellpadding cellspacing char charoff charset checked cite class classid clear ' \
    'codebase codetype color cols colspan compact content coords data datafld dataformatas datapagesize datasrc ' \
    'datetime declare defer dir disabled enctype event face for frame frameborder headers height href hreflang ' \
    'hspace http-equiv id ismap label lang language leftmargin link longdesc marginwidth marginheight maxlength ' \
    'media method multiple name nohref noresize noshade nowrap object onblur onchange onclick ondblclick onfocus ' \
    'onkeydown onkeypress onkeyup onload onmousedown onmousemove onmouseover onmouseout onmouseup onreset onselect ' \
    'onsubmit onunload profile prompt readonly rel rev rows rowspan rules scheme scope selected shape size span src ' \
    'standby start style summary tabindex target text title topmargin type usemap valign value valuetype version ' \
    'vlink vspace width text password checkbox radio submit reset file hidden image public !doctype'

djangoKeywords = '%% if else for'


class HTML_LIKE_PYTHON_EditorObject(PYTHON_EditorObject):
    def set_up_editor(self, editor):
        PYTHON_EditorObject.set_up_editor(self, editor)
        editor.SetKeyWords(0, htmlKeywords)
        editor.SetKeyWords(1, djangoKeywords)
        editor.SetKeyWords(2, 'body_start')
        editor.SetKeyWords(3, 'extrahead')
        editor.SetKeyWords(4, 'extrastyle')
        editor.SetLexer(stc.STC_LEX_LUA)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


class HTML_EditorObject(object):

    def set_up_editor(self, editor):
        editor.SetKeyWords(0, htmlKeywords)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


class WIKI_EditorObject(object):

    def set_up_editor(self, editor):
        editor.SetLexer(stc.STC_LEX_MARKDOWN)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


EditorObjectMap = {
    'py': 'PYTHON',
    'html': 'HTML',
    'ihtml': 'HTML_LIKE_PYTHON',
    'phtml': 'PYTHON',
    'wiki': 'WIKI',
    }
