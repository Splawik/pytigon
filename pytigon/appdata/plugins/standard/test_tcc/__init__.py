"""Test plugin for TCC (Tiny C Compiler) integration.

Demonstrates calling C functions from Python via CFFI.
Registers test functions in the application's external data.
"""

from . import schtest
import wx


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register CFFI test functions in application external data.

    Provides silnia (factorial), passed, and message functions
    implemented in C via the TCC compiler.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    functions = {
        "silnia": schtest.silnia,
        "passed": schtest.passed,
        "message": schtest.message,
    }
    app.extern_data["schtest"] = functions
