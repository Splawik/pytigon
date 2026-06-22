"""
Safe Subprocess Execution
Provides secure subprocess execution with input validation and sanitization.
"""

import os
import shutil
import sys
import subprocess
from typing import List, Optional, Tuple, Union
from pathlib import Path


class SafeSubprocess:
    """
    Secure subprocess execution with input validation.

    Validates that arguments contain no shell injection characters.
    Executables are allowed if they resolve to a real file within:
    - System PATH directories
    - The Python virtual environment
    - The PYTIGON_DATA/prg directory (user-compiled programs)
    - The Python interpreter itself
    """

    DANGEROUS_CHARS = set(";&|`$(){}[]<>!#~")

    def __init__(self):
        pass

    def validate_command(self, command: List[str]) -> List[str]:
        from ..errors import SecurityError

        if not command:
            raise SecurityError("Empty command", code=20)

        executable = command[0]
        if not self._is_executable_allowed(executable):
            raise SecurityError(f"Executable not allowed: {executable}", code=21)

        sanitized = []
        for i, arg in enumerate(command):
            if not isinstance(arg, str):
                raise SecurityError(
                    f"Argument {i} must be a string, got {type(arg).__name__}", code=22
                )
            if self._contains_dangerous_chars(arg):
                raise SecurityError(f"Argument {i} contains dangerous characters: {arg}", code=23)
            sanitized.append(arg)

        return sanitized

    def _safe_directories(self):
        dirs = set()

        for path in os.environ.get("PATH", "").split(os.pathsep):
            real = os.path.realpath(path) if os.path.exists(path) else None
            if real:
                dirs.add(real)

        try:
            from pytigon_lib.schtools.main_paths import get_main_paths
            paths = get_main_paths()
            prg = os.path.join(paths["DATA_PATH"], "prg")
            if os.path.isdir(prg):
                dirs.add(os.path.realpath(prg))
        except Exception:
            pass

        venv = os.environ.get("VIRTUAL_ENV")
        if venv and os.path.isdir(venv):
            venv_bin = os.path.join(venv, "bin" if os.name != "nt" else "Scripts")
            if os.path.isdir(venv_bin):
                dirs.add(os.path.realpath(venv_bin))

        return dirs

    def _is_executable_allowed(self, executable: str) -> bool:
        if executable in (sys.executable, "python", "python3"):
            return True

        if os.sep in executable or "/" in executable or "\\" in executable:
            exe_path = os.path.realpath(executable)
            if not os.path.isfile(exe_path):
                return False
        else:
            exe_path = shutil.which(executable) if shutil else None
            if not exe_path:
                return False
            exe_path = os.path.realpath(exe_path)

        exe_dir = os.path.dirname(exe_path)
        return exe_dir in self._safe_directories()

    def _contains_dangerous_chars(self, arg: str) -> bool:
        return bool(self.DANGEROUS_CHARS & set(arg))

    def run(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        capture_output: bool = False,
        timeout: Optional[int] = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess:
        """
        Safely execute a subprocess command.

        Args:
            command: List of command arguments
            cwd: Working directory for the subprocess
            env: Environment variables for the subprocess
            capture_output: Whether to capture stdout/stderr
            timeout: Timeout in seconds
            check: Whether to raise exception on non-zero exit code

        Returns:
            CompletedProcess instance

        Raises:
            SecurityError: If command validation fails
            SubprocessError: If subprocess execution fails
        """
        from ..errors import SecurityError, SubprocessError

        # Validate command
        validated_command = self.validate_command(command)

        # Prepare environment
        subprocess_env = os.environ.copy()
        if env:
            subprocess_env.update(env)

        # Prepare working directory
        if cwd:
            from .paths import PathResolver

            resolver = PathResolver()
            cwd_path = resolver.resolve(cwd, must_exist=True)
        else:
            cwd_path = None

        try:
            # Execute subprocess
            result = subprocess.run(
                validated_command,
                cwd=str(cwd_path) if cwd_path else None,
                env=subprocess_env,
                capture_output=capture_output,
                timeout=timeout,
                check=False,  # We'll handle the check ourselves
            )

            # Check return code if requested
            if check and result.returncode != 0:
                raise SubprocessError(
                    f"Command failed with exit code {result.returncode}: {' '.join(validated_command)}",
                    code=40,
                    returncode=result.returncode,
                )

            return result

        except subprocess.TimeoutExpired as e:
            raise SubprocessError(
                f"Command timed out after {timeout} seconds: {' '.join(validated_command)}",
                code=41,
            )
        except OSError as e:
            raise SubprocessError(
                f"Failed to execute command: {e}",
                code=42,
            )

    def run_simple(
        self, command: List[str], cwd: Optional[str] = None, capture_output=False
    ) -> int:
        """
        Simple subprocess execution that returns exit code.

        Args:
            command: List of command arguments
            cwd: Working directory for the subprocess

        Returns:
            Exit code of the subprocess
        """
        try:
            result = self.run(command, cwd=cwd, check=True, capture_output=capture_output)
            return result.returncode
        except Exception:
            return 1
