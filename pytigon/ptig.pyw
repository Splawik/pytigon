import wx
import subprocess
import threading
import sys
import os

from wx.lib.embeddedimage import PyEmbeddedImage

_ = wx.GetTranslation


pytigon_ico = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABHNCSVQICAgIfAhkiAAAANBJ"
    b"REFUaIHtmM0JAjEQhXdlz54924RNLNiBxdmBYBM24dmzDay3IGEHdLIz4YP3HQPJ5PEek59h"
    b"EKKJMaHGErBm2fcuYPFU8AKm1GrXl3/u5bA6jHcAL8ATIX9XMWLQEi28A3gBTV3oeJvdc5/n"
    b"e0vpAt4BCeiNBPSm7kIRV99Q8A7gBZgH2fLYr46Pp/f2u7DuSD+AdwAvIPdFZuP+XMA7gBdQ"
    b"W1cOstQupAiB+bsLWdH6popZ6Pcl3gEJ6I0E9MY8yAJrbAreAbwAIYQQAs0HU2sVyiQU3wUA"
    b"AAAASUVORK5CYII="
)


# Agreed keyword the main app prints when its main window is ready
SUCCESS_KEYWORD = "The Pytigon application has been launched"

# Keywords used to detect error lines in the main app's output
ERROR_KEYWORDS = ("Error", "Traceback", "Exception", "Failed", "FAILED")


class SplashFrame(wx.Frame):
    """
    A borderless, always-on-top frame that behaves like a splash screen
    but gives us full control over clicks and process termination.
    """

    def __init__(self):
        super().__init__(
            None, title="Starting...", style=wx.FRAME_NO_TASKBAR | wx.BORDER_NONE | wx.STAY_ON_TOP
        )

        self.process = None  # subprocess.Popen handle, set by start_main_app
        self._error_shown = False  # becomes True on the first error

        # --- Color palette ---
        self.bg_color = wx.Colour(245, 247, 250)
        self.accent_color = wx.Colour(45, 105, 185)
        self.muted_color = wx.Colour(120, 128, 140)

        self.SetBackgroundColour(self.bg_color)

        # --- Layout ---
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top accent bar
        accent_bar = wx.Panel(self, size=(-1, 6))
        accent_bar.SetBackgroundColour(self.accent_color)
        main_sizer.Add(accent_bar, 0, wx.EXPAND)

        # Header: logo + title side by side
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        logo_bmp = pytigon_ico.GetBitmap()

        logo_ctrl = wx.StaticBitmap(self, bitmap=logo_bmp)
        header_sizer.Add(logo_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)

        text_sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="Pytigon")
        title_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(self.accent_color)
        text_sizer.Add(title, 0, wx.TOP | wx.BOTTOM, 4)

        # self.subtitle = wx.StaticText(self, label="Starting application, please wait...")
        self.subtitle = wx.StaticText(self, label=wx.GetTranslation("Loading : ") + sys.argv[1])
        subtitle_font = wx.Font(
            10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        self.subtitle.SetFont(subtitle_font)
        self.subtitle.SetForegroundColour(self.muted_color)
        text_sizer.Add(self.subtitle, 0, wx.BOTTOM, 4)

        header_sizer.Add(text_sizer, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        main_sizer.Add(header_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)

        self.spinner = wx.ActivityIndicator(self)
        main_sizer.Add(self.spinner, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, 20)

        # --- Error section (hidden by default) ---
        self.error_label = wx.StaticText(self, label="Startup errors:")
        self.error_label.SetFont(
            wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        )
        self.error_label.SetForegroundColour(wx.Colour(180, 45, 45))
        self.error_label.Hide()

        self.error_list = wx.ListCtrl(
            self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SIMPLE
        )
        self.error_list.InsertColumn(0, "#", width=35)
        self.error_list.InsertColumn(1, "Message", width=520)
        self.error_list.SetBackgroundColour(wx.Colour(255, 250, 250))
        self.error_list.Hide()

        main_sizer.Add(self.error_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 16)
        main_sizer.Add(self.error_list, 1, wx.EXPAND | wx.ALL, 16)

        # Placeholder that fills the "no error" state
        self.spacer = wx.Panel(self, size=(-1, 60))
        self.spacer.SetBackgroundColour(self.bg_color)
        main_sizer.Add(self.spacer, 1, wx.EXPAND)

        # --- Button bar (hidden until the first error) ---

        self.button_panel = wx.Panel(self)
        self.button_panel.SetBackgroundColour(self.bg_color)

        self.close_btn = wx.Button(self.button_panel, label="Close")  # parent = button_panel
        self.close_btn.SetBackgroundColour(self.accent_color)
        self.close_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.close_btn.Bind(wx.EVT_BUTTON, self.on_close_clicked)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.AddStretchSpacer()
        self.button_sizer.Add(self.close_btn, 0, wx.RIGHT | wx.BOTTOM, 16)
        self.button_panel.SetSizer(self.button_sizer)

        self.button_panel.Hide()
        main_sizer.Add(self.button_panel, 0, wx.EXPAND)

        self.SetSizer(main_sizer)
        self.Fit()
        self.CentreOnScreen()

        # Allow dragging the borderless window by its background
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self._drag_start = None

        self.SetClientSize(
            wx.Size(max(self.GetClientSize().GetWidth(), 360), self.GetClientSize().GetHeight())
        )

        self.spinner.Start()  # Uruchomienie animacji

    # ------------------------------------------------------------------ #
    # Dragging a borderless window
    # ------------------------------------------------------------------ #
    def _on_left_down(self, evt):
        if not self._error_shown:
            # Don't allow dragging once errors are shown (not needed, cosmetic)
            self._drag_start = evt.GetPosition()
        evt.Skip()

    def _on_motion(self, evt):
        if self._drag_start is not None and evt.LeftIsDown():
            pos = self.ClientToScreen(evt.GetPosition())
            new_pos = pos - self._drag_start
            self.Move(new_pos)
        evt.Skip()

    def _on_left_up(self, evt):
        self._drag_start = None
        evt.Skip()

    # ------------------------------------------------------------------ #
    # Public API used by the launcher thread
    # ------------------------------------------------------------------ #
    def show_error(self, message):
        """Reveal the error list + close button and append a message."""
        if not self._error_shown:
            self._error_shown = True
            self.spacer.Hide()
            self.error_label.Show()
            self.error_list.Show()
            self.button_panel.Show()
            self.subtitle.SetLabel("The application reported errors:")
            self.Layout()
            self.Fit()
            self.CentreOnScreen()
            self.spinner.Stop()

        index = self.error_list.GetItemCount()
        self.error_list.InsertItem(index, str(index + 1))
        self.error_list.SetItem(index, 1, message)
        self.error_list.EnsureVisible(index)
        self.error_list.SetItemState(index, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def on_success(self):
        """The main app started successfully — close the launcher."""
        self.Destroy()

    # ------------------------------------------------------------------ #
    # Close button: kill child process, then close the launcher
    # ------------------------------------------------------------------ #
    def on_close_clicked(self, evt):
        self._terminate_child()
        self.Destroy()

    def _terminate_child(self):
        """Terminate the child process if it's still running."""
        if self.process is None:
            return
        if self.process.poll() is None:  # still running
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.process.kill()  # force kill on Windows
                    self.process.wait(timeout=2)
            except Exception:
                pass

    def Destroy(self):
        """Ensure the child is killed whenever the launcher is destroyed."""
        self._terminate_child()
        return super().Destroy()


class LauncherApp(wx.App):
    def OnInit(self):

        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)

        if hasattr(wx, "Locale_AddCatalogLookupPathPrefix"):
            wx.Locale.AddCatalogLookupPathPrefix("/usr/share/locale")

        self.frame = SplashFrame()
        self.frame.Show()
        # Pass the frame explicitly so the thread never depends on attribute order
        threading.Thread(
            target=self._run_main_app,
            args=(self.frame,),
            daemon=True,
        ).start()
        return True

    @staticmethod
    def _run_main_app(frame):
        """Launch the main app and stream its output to the splash frame."""
        try:
            process = subprocess.Popen(
                ["ptig", *sys.argv[1:]],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout for easier handling
                text=True,
                bufsize=1,  # Line-buffered output
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
        except Exception as exc:
            wx.CallAfter(frame.show_error, f"Failed to start process: {exc}")
            return

        # Store the handle so the Close button can terminate it
        frame.process = process

        success = False
        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            if not line:
                continue

            if SUCCESS_KEYWORD in line:
                success = True
                wx.CallAfter(frame.on_success)
                break

            if any(k in line for k in ERROR_KEYWORDS):
                wx.CallAfter(frame.show_error, line)

        process.stdout.close()
        return_code = process.wait()

        if not success and return_code != 0:
            wx.CallAfter(frame.show_error, f"Process exited abnormally, exit code: {return_code}")


if __name__ == "__main__":
    app = LauncherApp()
    app.MainLoop()
