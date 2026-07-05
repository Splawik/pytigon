"""Autocomplete control plugin with server-side dynamic choices.

Provides an autocomplete text control (AUTOCOMPLETE) that fetches
completion suggestions from the server in real-time as the user types.
"""

import wx

import pytigon_gui.guictrl.ctrl
from autocomplete import TextCtrlAutoComplete
from pytigon_gui.guictrl.ctrl import SchBaseCtrl
from pytigon_lib.schtools import schjson


class DbDict:
    """Dictionary-like object that fetches autocomplete choices from server.

    Acts as a dynamic data source for the autocomplete control.
    Each call to filter() queries the server and updates the choice list.

    Attributes:
        href: Server endpoint URL for fetching choices.
        tab: Current list of (value,) tuples for autocomplete display.
    """

    def __init__(self, href):
        """Initialize with the server endpoint URL.

        Args:
            href: URL path for autocomplete queries.
        """
        self.href = href
        self.tab = [""]

    def filter(self, parent, f):
        """Query the server for matching choices.

        Args:
            parent: Parent window used to obtain the HTTP client.
            f: Filter string to send to the server.
        """
        http = wx.GetApp().get_http(parent)
        response = http.get(self, str(self.href), {"query": f.encode("utf-8")})
        s = response.str()
        try:
            self.tab = schjson.loads(s)
        except Exception:
            self.tab = []
        self.tab = [(pos["value"],) for pos in self.tab]

    def __iter__(self):
        """Iterate over all choices."""
        yield from self.tab

    def __getitem__(self, idx):
        """Get a choice by index.

        Args:
            idx: Index of the choice.

        Returns:
            The choice tuple or None if out of range.
        """
        if idx < len(self.tab):
            return self.tab[idx]
        return None

    def __len__(self):
        """Return the number of choices."""
        return len(self.tab)

    def __contains__(self, x):
        """Check if a choice is in the list."""
        return x in self.tab


class Autocomplete(TextCtrlAutoComplete, SchBaseCtrl):
    """Text control with server-powered autocomplete suggestions.

    Combines TextCtrlAutoComplete with SchBaseCtrl to provide an
    autocomplete input field whose suggestions are fetched dynamically
    from the server based on user input.
    """

    def __init__(self, parent, **kwds):
        """Initialize the autocomplete control.

        Args:
            parent: Parent window.
            **kwds: Configuration keywords (style, data, etc.).
        """
        SchBaseCtrl.__init__(self, parent, kwds)
        self.dynamic_choices = DbDict(self.src)
        kwds["style"] = kwds.get("style", 0) | wx.TE_MULTILINE | wx.TE_PROCESS_ENTER
        kwds["choices"] = self.dynamic_choices
        TextCtrlAutoComplete.__init__(self, parent, colNames=("label", "value"), **kwds)
        self.SetEntryCallback(self.set_dynamic_choices)
        self.SetMatchFunction(self.match)
        if "data" in self.param:
            self.SetValue(self.param["data"].encode("utf-8"))

    def SetValue(self, value):
        """Set the control value, handling both str and bytes.

        Args:
            value: String or bytes value to set.
        """
        if isinstance(value, str):
            return TextCtrlAutoComplete.SetValue(self, value.decode("utf-8"))
        return TextCtrlAutoComplete.SetValue(self, value)

    def on_key_down(self, event):
        """Handle key down events - allow left/right arrows to pass through.

        Args:
            event: Key event.
        """
        if event.GetKeyCode() in (wx.WXK_LEFT, wx.WXK_RIGHT):
            event.Skip()
        else:
            super().onKeyDown(event)

    def match(self, text, choice):
        """Check if a choice matches the typed text.

        Performs case-insensitive prefix matching, also checking
        against URL-stripped versions (removing 'http://' and 'www.').

        Args:
            text: The user-typed text.
            choice: A candidate choice string.

        Returns:
            True if the choice matches the text.
        """
        t = text.lower()
        c = choice.lower()
        if c.startswith(t):
            return True
        if c.startswith("http://"):
            c = c[7:]
        if c.startswith(t):
            return True
        if c.startswith("www."):
            c = c[4:]
        return c.startswith(t)

    def set_dynamic_choices(self):
        """Fetch and update autocomplete choices based on current input."""
        ctrl = self
        text = ctrl.GetValue().lower()
        self.dynamic_choices.filter(self.GetParent(), text)
        if len(self.dynamic_choices) > 1:
            ctrl.SetMultipleChoices(self.dynamic_choices)
        elif len(self.dynamic_choices) > 0:
            ctrl.SetChoices(self.dynamic_choices[0])

    def _set_value_from_selected(self):
        """Set the text value from the currently selected dropdown item.

        Returns:
            Result from the parent class method.
        """
        return TextCtrlAutoComplete._setValueFromSelected(self)

    def _set_value_from_selected2(self):
        """Alternative method to set value from selected dropdown item."""
        sel = self.dropdownlistbox.GetFirstSelected()
        if sel > -1:
            col = self._colFetch if self._colFetch != -1 else self._colSearch
            itemtext = self.dropdownlistbox.GetItem(sel, col).GetText()
            self.SetValue(itemtext)


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register the Autocomplete control in the global control registry.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    pytigon_gui.guictrl.ctrl.AUTOCOMPLETE = Autocomplete
