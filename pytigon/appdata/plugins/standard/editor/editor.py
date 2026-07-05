"""Code editor with syntax highlighting for multiple languages.

Provides the CodeEditor widget based on wx.stc.StyledTextCtrl with
support for Python, HTML, Django templates, and Markdown/Wiki syntax.

Also includes language-specific editor configuration objects
(EditorObject classes) and the EditorObjectMap for file extension
to language mapping.
"""

import keyword

import wx
import wx.stc as stc

# Platform-specific font configuration
if wx.Platform == "__WXMSW__":
    faces = {
        "times": "Times New Roman",
        "mono": "Courier New",
        "helv": "Arial",
        "other": "Comic Sans MS",
        "size": 10,
        "size2": 8,
    }
elif wx.Platform == "__WXMAC__":
    faces = {
        "times": "Times New Roman",
        "mono": "Courier New",
        "helv": "Arial",
        "other": "Comic Sans MS",
        "size": 12,
        "size2": 10,
    }
else:
    faces = {
        "times": "DejaVu Sans Mono",
        "mono": "DejaVu Sans Mono",
        "helv": "DejaVu Sans Mono",
        "other": "DejaVu Sans Mono",
        "size": 9,
        "size2": 7,
    }


class CodeEditor(stc.StyledTextCtrl):
    """Syntax-highlighting code editor based on Scintilla/StyledTextCtrl.

    Features:
    - Python syntax highlighting by default
    - Code folding with margin markers
    - Brace matching and highlighting
    - Auto-indentation on Enter
    - Tab-to-spaces conversion
    - Find text with persistence
    - Extensible language support via EditorObject classes
    """

    def __init__(self, *args, **kwds):
        """Initialize the code editor with default Python styling.

        Args:
            *args: Positional arguments for StyledTextCtrl.
            **kwds: Keyword arguments for StyledTextCtrl.
        """
        stc.StyledTextCtrl.__init__(self, *args, **kwds)
        self.SetCodePage(65001)
        self.CmdKeyAssign(ord("B"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord("N"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetViewWhiteSpace(False)
        self.SetEdgeColumn(78)
        self.SetMargins(2, 2)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080"
        )
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080"
        )
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080"
        )
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080"
        )
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080"
        )
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDEROPENMID,
            stc.STC_MARK_BOXMINUSCONNECTED,
            "white",
            "#808080",
        )
        self.MarkerDefine(
            stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080"
        )
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.Bind(stc.EVT_STC_UPDATEUI, self.on_update_ui)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.on_margin_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, f"face:{faces['helv']},size:{faces['size']}")
        self.StyleClearAll()
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, f"face:{faces['helv']},size:{faces['size']}")
        col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        colstr = col.GetAsString(wx.C2S_HTML_SYNTAX)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, f"fore:#000000,back:{colstr}")
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, f"face:{faces['other']}")
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#000000,back:#DDDDFF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FFCCCC,bold")
        self.StyleSetSpec(
            stc.STC_P_DEFAULT, f"fore:#000000,face:{faces['helv']},size:{faces['size']}"
        )
        self.StyleSetSpec(
            stc.STC_P_COMMENTLINE, f"fore:#007F00,face:{faces['other']},size:{faces['size']}"
        )
        self.StyleSetSpec(stc.STC_P_NUMBER, f"fore:#007F7F,size:{faces['size']}")
        self.StyleSetSpec(
            stc.STC_P_STRING, f"fore:#7F007F,face:{faces['helv']},size:{faces['size']}"
        )
        self.StyleSetSpec(
            stc.STC_P_CHARACTER, f"fore:#7F007F,face:{faces['helv']},size:{faces['size']}"
        )
        self.StyleSetSpec(stc.STC_P_WORD, f"fore:#00007F,bold,size:{faces['size']}")
        self.StyleSetSpec(stc.STC_P_TRIPLE, f"fore:#7F0000,size:{faces['size']}")
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, f"fore:#7F0000,size:{faces['size']}")
        self.StyleSetSpec(
            stc.STC_P_CLASSNAME, f"fore:#0000FF,bold,underline,size:{faces['size']}"
        )
        self.StyleSetSpec(stc.STC_P_DEFNAME, f"fore:#007F7F,bold,size:{faces['size']}")
        self.StyleSetSpec(stc.STC_P_OPERATOR, f"bold,size:{faces['size']}")
        self.StyleSetSpec(
            stc.STC_P_IDENTIFIER, f"fore:#000000,face:{faces['helv']},size:{faces['size']}"
        )
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, f"fore:#7F7F7F,size:{faces['size']}")
        self.StyleSetSpec(
            stc.STC_P_STRINGEOL,
            f"GetCurrentPosfore:#000000,face:{faces['mono']},back:#E0C0E0,eol,size:{faces['size']}"
        )
        self.SetCaretForeground("#D00000")
        self.SetCaretWidth(2)
        self.SetSelBackground(
            True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        )
        self.SetSelForeground(
            True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        )
        b1 = wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_MENU, (16, 16))
        b2 = wx.ArtProvider.GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_MENU, (16, 16))
        self.RegisterImage(1, b1)
        self.RegisterImage(2, b2)

        self._last_flag = None
        self._last_text = None

    def set_ext(self, ext):
        """Set syntax highlighting based on file extension.

        Args:
            ext: File extension (e.g. 'py', 'html', 'ihtml').
        """
        if ext in EditorObjectMap:
            self.set_language(EditorObjectMap[ext])

    def set_language(self, language):
        """Configure syntax highlighting for a specific language.

        First tries to find a matching EditorObject class, then falls
        back to setting a Scintilla lexer directly.

        Args:
            language: Language name (e.g. 'PYTHON', 'HTML').
        """
        try:
            self.langObj = eval(language + "_EditorObject()")
        except (NameError, SyntaxError):
            self.langObj = None
        if self.langObj:
            self.langObj.set_up_editor(self)
        else:
            try:
                lexer = eval("stc.STC_LEX_" + language)
            except (NameError, AttributeError):
                lexer = stc.STC_LEX_AUTOMATIC
            self.SetLexer(lexer)

    def on_key_pressed(self, event):
        """Handle key press events for the editor.

        - Ctrl+F: Handled externally (passed through)
        - Ctrl+Space: Trigger autocomplete or info
        - Enter: Auto-indent new line
        - Escape: Close current tab
        - F3: Find next

        Args:
            event: Key event.
        """
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        if key == 70 and event.ControlDown():
            pass
        elif key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            if event.ShiftDown():
                if hasattr(self.GetParent(), "on_info_cmd"):
                    self.GetParent().on_info_cmd(self, pos)
            else:
                if hasattr(self.GetParent(), "on_auto_comp_cmd"):
                    self.GetParent().on_auto_comp_cmd(self, pos)
        elif key in (wx.WXK_NUMPAD_ENTER, wx.WXK_RETURN):
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
        """Handle Enter key - insert new line with smart indentation.

        Maintains current indentation level and adds extra indent
        after lines ending with ':'.
        """
        (line, space_len) = self.GetCurLine()
        pos = self.GetCurrentPos()
        col = self.GetColumn(pos)
        indent = self.GetLineIndentation(self.GetCurrentLine())
        if space_len > indent:
            space_len = indent
        if line[:col].rstrip()[-1:] == ":":
            space_len += 4
        txt = "\n" + " " * space_len
        self.InsertText(pos, txt)
        pos += len(txt)
        self.SetCurrentPos(pos)
        self.SetSelection(pos, pos)

    def on_update_ui(self, evt):
        """Handle UI update - perform brace matching and highlighting.

        Args:
            evt: StyledTextCtrl update UI event.
        """
        brace_at_caret = -1
        brace_opposite = -1
        char_before = None
        caret_pos = self.GetCurrentPos()
        if caret_pos > 0:
            char_before = self.GetCharAt(caret_pos - 1)
            style_before = self.GetStyleAt(caret_pos - 1)
        if (
            char_before
            and chr(char_before) in "[]{}()"
            and style_before == stc.STC_P_OPERATOR
        ):
            brace_at_caret = caret_pos - 1
        if brace_at_caret < 0:
            char_after = self.GetCharAt(caret_pos)
            style_after = self.GetStyleAt(caret_pos)
            if (
                char_after
                and chr(char_after) in "[]{}()"
                and style_after == stc.STC_P_OPERATOR
            ):
                brace_at_caret = caret_pos
        if brace_at_caret >= 0:
            brace_opposite = self.BraceMatch(brace_at_caret)
        if brace_at_caret != -1 and brace_opposite == -1:
            self.BraceBadLight(brace_at_caret)
        else:
            self.BraceHighlight(brace_at_caret, brace_opposite)

    def on_margin_click(self, evt):
        """Handle click on the folding margin.

        - Shift+Ctrl+Click: Fold/unfold all
        - Shift+Click: Expand one level
        - Ctrl+Click: Collapse one level
        - Click: Toggle fold

        Args:
            evt: Margin click event.
        """
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                line_clicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(line_clicked, True)
                        self._expand(line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(line_clicked):
                            self.SetFoldExpanded(line_clicked, False)
                            self._expand(line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(line_clicked, True)
                            self._expand(line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(line_clicked)

    def fold_all(self):
        """Toggle folding of all top-level blocks."""
        line_count = self.GetLineCount()
        expanding = True
        for line_num in range(line_count):
            if self.GetFoldLevel(line_num) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(line_num)
                break
        line_num = 0
        while line_num < line_count:
            level = self.GetFoldLevel(line_num)
            if (
                level & stc.STC_FOLDLEVELHEADERFLAG
                and level & stc.STC_FOLDLEVELNUMBERMASK == stc.STC_FOLDLEVELBASE
            ):
                if expanding:
                    self.SetFoldExpanded(line_num, True)
                    line_num = self._expand(line_num, True)
                    line_num = line_num - 1
                else:
                    last_child = self.GetLastChild(line_num, -1)
                    self.SetFoldExpanded(line_num, False)
                    if last_child > line_num:
                        self.HideLines(line_num + 1, last_child)
            line_num = line_num + 1

    def _expand(self, line, do_expand, force=False, vis_levels=0, level=-1):
        """Recursively expand or collapse code folding from a given line.

        Note: Named with underscore prefix to avoid conflicting with
        the base class Expand method.

        Args:
            line: Starting line number.
            do_expand: True to expand, False to collapse.
            force: If True, override current fold state.
            vis_levels: Number of visible levels (for force mode).
            level: Fold level (-1 to auto-detect).

        Returns:
            Next line number after processing.
        """
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
                    line = self._expand(line, do_expand, force, vis_levels - 1)
                else:
                    if do_expand and self.GetFoldExpanded(line):
                        line = self._expand(line, True, force, vis_levels - 1)
                    else:
                        line = self._expand(line, False, force, vis_levels - 1)
            else:
                line = line + 1
        return line

    def preprocess(self, txt):
        """Preprocess text before insertion - convert tabs to spaces.

        Args:
            txt: Input text (str or bytes).

        Returns:
            Text with tabs replaced by 4 spaces.
        """
        if isinstance(txt, str):
            return txt.replace("\t", " " * 4)
        return txt.replace(b"\t", b" " * 4)

    def on_find_next(self, event):
        """Find next occurrence of the last searched text.

        Args:
            event: Key event (F3).

        Returns:
            Search result position or -1 if not found.
        """
        if self._last_text:
            sel = self.GetSelectionEnd()
            if sel >= 0:
                self.SetSelectionStart(sel)
            self.SearchAnchor()
            return self.SearchNext(self._last_flag, self._last_text)
        return -1

    def FindText(self, minPos, maxPos, flags, text):
        """Find text within a range, storing search parameters.

        Args:
            minPos: Minimum position to search from.
            maxPos: Maximum position to search to.
            flags: Search flags.
            text: Text to find.

        Returns:
            Position of found text or -1.
        """
        self._last_flag = flags
        self._last_text = text
        return stc.StyledTextCtrl.FindText(self, minPos, maxPos, flags, text)

    def SearchNext(self, flags, text):
        """Find next occurrence from current position.

        Args:
            flags: Search flags.
            text: Text to find.

        Returns:
            Position of found text or -1.
        """
        self._last_flag = flags
        self._last_text = text
        ret = stc.StyledTextCtrl.SearchNext(self, flags, text)
        self.EnsureCaretVisible()
        return ret

    def AutoCompGetMaxHeight(self):
        """Get maximum height for autocomplete list.

        Returns:
            Maximum number of items (16).
        """
        return 16


class PYTHON_EditorObject:
    """Editor configuration for Python files.

    Sets up Python lexer with keyword highlighting, line numbers,
    and proper indentation settings.
    """

    def set_up_editor(self, editor):
        """Configure the editor for Python syntax.

        Args:
            editor: The CodeEditor instance to configure.
        """
        editor.SetLexer(stc.STC_LEX_PYTHON)
        editor.SetKeyWords(0, " ".join(keyword.kwlist))
        editor.SetProperty("fold", "1")
        editor.SetProperty("tab.timmy.whinge.level", "1")
        editor.SetMargins(2, 2)
        editor.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        editor.SetMarginWidth(1, 40)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


# HTML keywords for syntax highlighting
htmlKeywords = (
    "a abbr acronym address applet area b base basefont bdo big blockquote body br "
    "button caption center cite code col colgroup dd del dfn dir div dl dt em "
    "fieldset font form frame frameset h1 h2 h3 h4 h5 h6 head hr html i iframe img "
    "input ins isindex kbd label legend li link map menu meta noframes noscript "
    "object ol optgroup option p param pre q s samp script select small span strike "
    "strong style sub sup table tbody td textarea tfoot th thead title tr tt u ul "
    "var xml xmlns abbr accept-charset accept accesskey action align alink alt "
    "archive axis background bgcolor border cellpadding cellspacing char charoff "
    "charset checked cite class classid clear codebase codetype color cols colspan "
    "compact content coords data datafld dataformatas datapagesize datasrc datetime "
    "declare defer dir disabled enctype event face for frame frameborder headers "
    "height href hreflang hspace http-equiv id ismap label lang language leftmargin "
    "link longdesc marginwidth marginheight maxlength media method multiple name "
    "nohref noresize noshade nowrap object onblur onchange onclick ondblclick "
    "onfocus onkeydown onkeypress onkeyup onload onmousedown onmousemove onmouseover "
    "onmouseout onmouseup onreset onselect onsubmit onunload profile prompt readonly "
    "rel rev rows rowspan rules scheme scope selected shape size span src standby "
    "start style summary tabindex target text title topmargin type usemap valign "
    "value valuetype version vlink vspace width text password checkbox radio submit "
    "reset file hidden image public !doctype"
)

# Django template keywords
djangoKeywords = "%% if else for"


class HTML_LIKE_PYTHON_EditorObject(PYTHON_EditorObject):
    """Editor configuration for Django template files (.ihtml).

    Extends Python editor settings with HTML and Django template
    keyword highlighting using the Lua lexer (which supports
    custom keyword sets).
    """

    def set_up_editor(self, editor):
        """Configure the editor for Django/HTML template syntax.

        Args:
            editor: The CodeEditor instance to configure.
        """
        PYTHON_EditorObject.set_up_editor(self, editor)
        editor.SetKeyWords(0, htmlKeywords)
        editor.SetKeyWords(1, djangoKeywords)
        editor.SetKeyWords(2, "body_start")
        editor.SetKeyWords(3, "extrahead")
        editor.SetKeyWords(4, "extrastyle")
        editor.SetLexer(stc.STC_LEX_LUA)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


class HTML_EditorObject:
    """Editor configuration for HTML files."""

    def set_up_editor(self, editor):
        """Configure the editor for HTML syntax.

        Args:
            editor: The CodeEditor instance to configure.
        """
        editor.SetKeyWords(0, htmlKeywords)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


class WIKI_EditorObject:
    """Editor configuration for Wiki/Markdown files."""

    def set_up_editor(self, editor):
        """Configure the editor for Markdown syntax.

        Args:
            editor: The CodeEditor instance to configure.
        """
        editor.SetLexer(stc.STC_LEX_MARKDOWN)
        editor.SetIndent(4)
        editor.SetIndentationGuides(True)
        editor.SetBackSpaceUnIndents(True)
        editor.SetTabIndents(True)
        editor.SetTabWidth(4)
        editor.SetUseTabs(False)


# Mapping from file extension to EditorObject class name prefix
EditorObjectMap = {
    "py": "PYTHON",
    "html": "HTML",
    "ihtml": "HTML_LIKE_PYTHON",
    "phtml": "PYTHON",
    "wiki": "WIKI",
}
