"""
Pytest tests for pytigon.commands.utils module (PathResolver and SafeSubprocess).
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path

from pytigon.commands.utils.paths import PathResolver
from pytigon.commands.utils.subprocess import SafeSubprocess
from pytigon.commands.errors.exceptions import PathError, SecurityError


# ---------------------------------------------------------------------------
# PathResolver tests
# ---------------------------------------------------------------------------


class TestPathResolver:
    def test_initialization_default_base_path(self):
        resolver = PathResolver()
        assert resolver.base_path == Path(os.getcwd()).resolve()

    def test_initialization_custom_base_path(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        assert resolver.base_path == tmp_path.resolve()

    def test_resolve_relative_path(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        (tmp_path / "test_file.txt").touch()
        resolved = resolver.resolve("test_file.txt")
        assert resolved == (tmp_path / "test_file.txt").resolve()

    def test_resolve_relative_path_must_exist(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        (tmp_path / "existing.txt").touch()
        resolved = resolver.resolve("existing.txt", must_exist=True)
        assert resolved.exists()

    def test_resolve_relative_path_must_exist_raises_error(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        with pytest.raises(PathError, match="Path does not exist"):
            resolver.resolve("nonexistent.txt", must_exist=True)

    def test_resolve_absolute_path_within_base(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        (tmp_path / "file.txt").touch()
        abs_path = str(tmp_path / "file.txt")
        resolved = resolver.resolve(abs_path)
        assert resolved == (tmp_path / "file.txt").resolve()

    def test_resolve_absolute_path_outside_base_raises_error(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        with pytest.raises(PathError, match="Access denied"):
            resolver.resolve("/etc/passwd")

    def test_is_allowed_path_within_base(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        assert resolver._is_allowed_path(tmp_path / "subdir") is True

    def test_is_allowed_path_outside_base(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        assert resolver._is_allowed_path(Path("/root/secret")) is False

    def test_is_allowed_path_system_directories(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        # /usr/bin should be allowed as a system directory
        assert resolver._is_allowed_path(Path("/usr/bin")) is True
        assert resolver._is_allowed_path(Path("/bin")) is True

    def test_validate_executable_by_name(self):
        resolver = PathResolver()
        # python should be found in PATH
        result = resolver.validate_executable("python3")
        assert result is not None
        assert result.name.startswith("python")

    def test_validate_executable_not_found(self):
        resolver = PathResolver()
        with pytest.raises(PathError, match="Executable not found"):
            resolver.validate_executable("nonexistent_executable_xyz")

    def test_validate_executable_by_path(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        exe_path = tmp_path / "my_exe"
        exe_path.touch()
        exe_path.chmod(0o755)
        result = resolver.validate_executable(str(exe_path))
        assert result == exe_path.resolve()

    def test_safe_join(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        result = resolver.safe_join(str(tmp_path), "subdir", "file.txt")
        assert result == (tmp_path / "subdir" / "file.txt").resolve()

    def test_safe_join_with_absolute_paths(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        result = resolver.safe_join(str(tmp_path), "a", "b")
        assert result == (tmp_path / "a" / "b").resolve()

    def test_resolve_invalid_path_raises_error(self, tmp_path):
        resolver = PathResolver(base_path=str(tmp_path))
        # Path with null bytes is invalid
        with pytest.raises(PathError):
            resolver.resolve("\0invalid")


# ---------------------------------------------------------------------------
# SafeSubprocess tests
# ---------------------------------------------------------------------------


class TestSafeSubprocess:
    def test_initialization_default_allowed(self):
        sp = SafeSubprocess()
        assert "python" in sp.allowed_executables
        assert "python3" in sp.allowed_executables
        assert "pip" in sp.allowed_executables

    def test_initialization_custom_allowed(self):
        custom = {"my_tool", "my_script"}
        sp = SafeSubprocess(allowed_executables=custom)
        assert sp.allowed_executables == custom

    def test_validate_command_valid(self):
        sp = SafeSubprocess()
        result = sp.validate_command(["python3", "--version"])
        assert result == ["python3", "--version"]

    def test_validate_command_empty_raises_error(self):
        sp = SafeSubprocess()
        with pytest.raises(SecurityError, match="Empty command"):
            sp.validate_command([])

    def test_validate_command_disallowed_executable(self):
        sp = SafeSubprocess()
        with pytest.raises(SecurityError, match="Executable not allowed"):
            sp.validate_command(["rm", "-rf", "/"])

    def test_validate_command_dangerous_chars(self):
        sp = SafeSubprocess()
        with pytest.raises(SecurityError, match="dangerous characters"):
            sp.validate_command(["python3", "; ls"])

    def test_validate_command_non_string_argument(self):
        sp = SafeSubprocess()
        with pytest.raises(SecurityError, match="must be a string"):
            sp.validate_command(["python3", 123])

    def test_is_executable_allowed_python(self):
        sp = SafeSubprocess()
        assert sp._is_executable_allowed("python3") is True
        assert sp._is_executable_allowed("python") is True
        assert sp._is_executable_allowed(sys.executable) is True

    def test_is_executable_allowed_pip(self):
        sp = SafeSubprocess()
        assert sp._is_executable_allowed("pip") is True
        assert sp._is_executable_allowed("pip3") is True

    def test_is_executable_allowed_disallowed(self):
        sp = SafeSubprocess()
        assert sp._is_executable_allowed("rm") is False
        assert sp._is_executable_allowed("bash") is False

    def test_contains_dangerous_chars(self):
        sp = SafeSubprocess()
        assert sp._contains_dangerous_chars("safe_arg") is False
        assert sp._contains_dangerous_chars("arg; ls") is True
        assert sp._contains_dangerous_chars("arg|cat") is True
        assert sp._contains_dangerous_chars("$(whoami)") is True
        assert sp._contains_dangerous_chars("`whoami`") is True

    def test_run_simple_with_valid_command(self):
        sp = SafeSubprocess()
        exit_code = sp.run_simple(["python3", "--version"])
        assert exit_code == 0

    def test_run_simple_with_invalid_command(self):
        sp = SafeSubprocess()
        exit_code = sp.run_simple(["python3", "--nonexistent-flag-xyz"])
        assert exit_code != 0

    def test_run_with_capture_output(self, tmp_path):
        sp = SafeSubprocess()
        # Create a script file to avoid dangerous characters in arguments
        script = tmp_path / "test_script.py"
        script.write_text("import sys\nsys.stdout.write('hello')\n")
        result = sp.run(
            ["python3", str(script)],
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0
        assert b"hello" in result.stdout

    def test_dangerous_chars_set(self):
        sp = SafeSubprocess()
        assert ";" in sp.DANGEROUS_CHARS
        assert "|" in sp.DANGEROUS_CHARS
        assert "$" in sp.DANGEROUS_CHARS
        assert "`" in sp.DANGEROUS_CHARS
