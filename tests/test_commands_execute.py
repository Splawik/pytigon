"""Execution-path tests for pytigon CLI command handlers.

Covers the ``execute`` methods of the handlers (which were previously almost
untested) using a mocked ``run_subprocess``/``SafeSubprocess.run`` so no real
subprocesses are spawned, plus the error paths of ``SafeSubprocess``.
"""

import subprocess

import pytest

from pytigon.commands.errors.exceptions import SecurityError, SubprocessError
from pytigon.commands.handlers import (
    ManageCommandHandler,
    PipCommandHandler,
    PythonCommandHandler,
)
from pytigon.commands.utils.subprocess import SafeSubprocess


class _ExitCode(int):
    """Wrapper so mocks can return an int-like return code."""

    pass


# ---------------------------------------------------------------------------
# PythonCommandHandler execution
# ---------------------------------------------------------------------------


class TestPythonCommandHandlerExecute:
    def test_handle_python_simple_builds_command(self, monkeypatch):
        handler = PythonCommandHandler()
        captured = {}

        def fake_run_subprocess(command, cwd=None):
            captured["command"] = command
            return 0

        monkeypatch.setattr(handler, "run_subprocess", fake_run_subprocess)
        monkeypatch.setattr(handler, "get_executable", lambda: "/usr/bin/python3")

        exit_code = handler.execute(["ptig", "python", "-c", "print(1)"])
        assert exit_code == 0
        assert captured["command"][0] == "/usr/bin/python3"
        assert captured["command"][1] == "-c"
        assert captured["command"][2] == "print(1)"

    def test_handle_python_app_sets_pythonpath(self, monkeypatch):
        handler = PythonCommandHandler()
        captured = {}

        def fake_run_subprocess(command, cwd=None):
            captured["command"] = command
            return 0

        monkeypatch.setattr(handler, "run_subprocess", fake_run_subprocess)
        monkeypatch.setattr(handler, "get_executable", lambda: "/usr/bin/python3")
        monkeypatch.setattr(handler, "setup_paths", lambda app: {"DATA_PATH": "/tmp/data"})

        exit_code = handler.execute(["ptig", "python_myapp", "-V"])
        assert exit_code == 0
        assert captured["command"][0] == "/usr/bin/python3"

    def test_handle_script_file(self, monkeypatch, tmp_path):
        handler = PythonCommandHandler()
        captured = {}

        script = tmp_path / "myscript.py"
        script.write_text("print('hi')\n")

        def fake_run_subprocess(command, cwd=None):
            captured["command"] = command
            return 0

        monkeypatch.setattr(handler, "run_subprocess", fake_run_subprocess)
        monkeypatch.setattr(handler, "get_executable", lambda: "/usr/bin/python3")

        exit_code = handler.execute(["ptig", str(script)])
        assert exit_code == 0
        # argv[1] (the script) must remain part of the command
        assert captured["command"][1] == str(script)


# ---------------------------------------------------------------------------
# ManageCommandHandler execution
# ---------------------------------------------------------------------------


class TestManageCommandHandlerExecute:
    def test_manage_simple(self, monkeypatch):
        handler = ManageCommandHandler()
        captured = {}

        def fake_run_subprocess(command, cwd=None):
            captured["command"] = command
            return 0

        monkeypatch.setattr(handler, "run_subprocess", fake_run_subprocess)
        monkeypatch.setattr(handler, "get_executable", lambda: "/usr/bin/python3")

        exit_code = handler.execute(["ptig", "manage", "check"])
        assert exit_code == 0
        assert captured["command"][1] == "manage.py"
        assert captured["command"][2] == "check"

    def test_manage_app(self, monkeypatch, tmp_path):
        handler = ManageCommandHandler()
        captured = {}
        start = tmp_path / "start"
        start.mkdir()

        monkeypatch.chdir(start)

        def fake_run_subprocess(command, cwd=None):
            captured["command"] = command
            return 0

        monkeypatch.setattr(handler, "run_subprocess", fake_run_subprocess)
        monkeypatch.setattr(handler, "get_executable", lambda: "/usr/bin/python3")
        monkeypatch.setattr(
            handler,
            "_prepare_project",
            lambda app: ("myapp", str(tmp_path), {"DATA_PATH": str(tmp_path)}),
        )

        exit_code = handler.execute(["ptig", "manage_myapp", "migrate"])
        assert exit_code == 0
        assert captured["command"][1] == "manage.py"

    def test_execute_error_returns_nonzero(self, monkeypatch):
        handler = ManageCommandHandler()

        def boom(argv, **kw):
            raise RuntimeError("boom")

        monkeypatch.setattr(handler, "execute", boom)
        with pytest.raises(RuntimeError):
            handler.execute(["ptig", "manage"])


# ---------------------------------------------------------------------------
# PipCommandHandler execution
# ---------------------------------------------------------------------------


class TestPipCommandHandlerExecute:
    def test_missing_subcommand_returns_error(self, monkeypatch):
        handler = PipCommandHandler()
        monkeypatch.setattr(handler, "handle_error", lambda e, c: 1)
        exit_code = handler.execute(["ptig", "pip_myapp"])
        assert exit_code == 1

    def test_pip_install_adds_target(self, monkeypatch):
        handler = PipCommandHandler()
        captured = {}

        monkeypatch.setattr(
            handler,
            "setup_paths",
            lambda app: {"DATA_PATH": "/tmp/data"},
        )
        monkeypatch.setattr(handler, "get_executable", lambda: "/usr/bin/python3")
        monkeypatch.setattr(
            handler,
            "run_subprocess",
            lambda cmd, cwd=None: captured.setdefault("cmd", cmd) and 0,
        )

        exit_code = handler.execute(["ptig", "pip_myapp", "install", "requests"])
        assert exit_code == 0
        assert captured["cmd"][0] == "/usr/bin/python3"
        assert captured["cmd"][2] == "pip"
        assert captured["cmd"][3] == "install"
        assert "--target=/tmp/data/myapp/prjlib" in captured["cmd"]


# ---------------------------------------------------------------------------
# SafeSubprocess error paths
# ---------------------------------------------------------------------------


class TestSafeSubprocessErrors:
    def test_run_timeout_raises_subprocess_error(self, monkeypatch):
        sp = SafeSubprocess()

        def fake_run(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd=args[0], timeout=5)

        monkeypatch.setattr(subprocess, "run", fake_run)
        with pytest.raises(SubprocessError, match="timed out"):
            sp.run(["python3", "--version"], timeout=5)

    def test_run_oserror_raises_subprocess_error(self, monkeypatch):
        sp = SafeSubprocess()

        def fake_run(*args, **kwargs):
            raise OSError("no such file")

        monkeypatch.setattr(subprocess, "run", fake_run)
        with pytest.raises(SubprocessError, match="Failed to execute"):
            sp.run(["python3", "--version"])

    def test_run_simple_reports_errors(self, monkeypatch, capsys):
        """run_simple must return 1 and report the reason on stderr."""
        sp = SafeSubprocess()
        monkeypatch.setattr(sp, "run", lambda *a, **k: (_ for _ in ()).throw(SubprocessError("x")))
        assert sp.run_simple(["python3", "--version"]) == 1
        captured = capsys.readouterr()
        assert "x" in captured.err

    def test_run_simple_reports_security_error(self, capsys):
        """SecurityError (e.g. dangerous chars) must be reported, not silent."""
        sp = SafeSubprocess()
        assert sp.run_simple(["python3", "-c", "print('hello'); print(1)"]) == 1
        captured = capsys.readouterr()
        assert "dangerous characters" in captured.err

    def test_run_dash_c_via_argv(self):
        """End-to-end: -c code as argv (no shell) executes and prints."""
        sp = SafeSubprocess()
        result = sp.run(
            ["python3", "-c", "print('hello')"],
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0
        assert b"hello" in result.stdout


# ---------------------------------------------------------------------------
# Error handler exit codes
# ---------------------------------------------------------------------------


class TestErrorExitCodes:
    def test_security_error_code(self):
        from pytigon.commands.errors.handler import ErrorHandler

        handler = ErrorHandler()
        code = handler.handle(SecurityError("denied", code=20))
        assert code == 20

    def test_unknown_error_default(self):
        from pytigon.commands.errors.handler import ErrorHandler

        handler = ErrorHandler()
        code = handler.handle(RuntimeError("oops"))
        assert code == 1
