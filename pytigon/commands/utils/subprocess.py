"""Safe Subprocess Execution
Provides secure subprocess execution with input validation and sanitization.
"""

import os
import shlex
import shutil
import signal
import subprocess
import sys

from ..errors import SecurityError, SubprocessError


class SafeSubprocess:
    """Secure subprocess execution with input validation.

    Validates that arguments contain no shell injection characters.
    Executables are allowed if they resolve to a real file within:
    - System PATH directories
    - The Python virtual environment
    - The PYTIGON_DATA/prg directory (user-compiled programs)
    - The Python interpreter itself
    """

    # Characters rejected in command arguments.
    #
    # subprocess.run() is always invoked with an argv list (never a shell), so
    # shell metacharacters like () {} [] <> ~ are harmless there — and must stay
    # allowed, e.g. `ptig python -c "print('hello')"`. NUL and other control
    # characters are always rejected (NUL cannot even be passed via argv).
    # The remaining shell markers (; & | $ ` ! #) are kept as a conservative
    # defense-in-depth set in case an argument is ever re-joined into a shell
    # command by another handler.
    DANGEROUS_CHARS = set(";&|`$!#") | {chr(c) for c in range(32)}

    def __init__(self):
        pass

    def validate_command(self, command: list[str]) -> list[str]:
        from ..errors import SecurityError

        if not command:
            raise SecurityError("Empty command", code=20)

        executable = command[0]
        if not self._is_executable_allowed(executable):
            msg = f"Executable not allowed: {executable}"
            raise SecurityError(msg, code=21)

        sanitized = []
        for i, arg in enumerate(command):
            if not isinstance(arg, str):
                msg = f"Argument {i} must be a string, got {type(arg).__name__}"
                raise SecurityError(
                    msg,
                    code=22,
                )
            if self._contains_dangerous_chars(arg):
                msg = f"Argument {i} contains dangerous characters: {arg}"
                raise SecurityError(msg, code=23)
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

        venv = os.environ.get("PYTHONUSERBASE")
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

    @staticmethod
    def _decode_output(data) -> str:
        """Decode bytes/str subprocess output, tolerating encoding errors."""
        if data is None:
            return ""
        if isinstance(data, bytes):
            return data.decode("utf-8", errors="replace").rstrip("\n")
        return str(data).rstrip("\n")

    def _format_failure(
        self,
        command: list[str],
        cwd: str | None,
        result: subprocess.CompletedProcess | None,
        capture_output: bool,
    ) -> str:
        """Build a detailed, multi-line message describing a failed subprocess.

        Args:
            command: The validated command that was run
            cwd: Working directory of the subprocess (if any)
            result: CompletedProcess of the failed run, or None if it never
                started (e.g. OSError)
            capture_output: Whether stdout/stderr were captured

        Returns:
            Human readable multi-line error description.

        """
        lines = [
            "Subprocess command failed",
            "------------------------",
            f"  Command:    {shlex.join(command)}",
        ]
        if cwd:
            lines.append(f"  Working in: {cwd}")

        if result is not None:
            returncode = result.returncode
            if returncode < 0:
                signum = -returncode
                try:
                    signame = signal.Signals(signum).name
                except (ValueError, OSError):
                    signame = f"signal {signum}"
                lines.append(f"  Exit code:  {returncode} ({signame})")
            else:
                lines.append(f"  Exit code:  {returncode}")

            if capture_output:
                for name in ("stdout", "stderr"):
                    text = self._decode_output(getattr(result, name))
                    if not text:
                        continue
                    lines.append("")
                    lines.append(f"  --- {name} ---")
                    lines.extend(f"  {line}" if line else "" for line in text.split("\n"))
            else:
                lines.append("")
                lines.append(
                    "  Note: stdout/stderr were not captured "
                    "(capture_output=True) so they are not shown here."
                )
        else:
            lines.append("  Exit code:  (process did not start)")

        return "\n".join(lines)

    def run(
        self,
        command: list[str],
        cwd: str | None = None,
        env: dict | None = None,
        capture_output: bool = False,
        timeout: int | None = None,
        check: bool = True,
        validate: bool = True,
    ) -> subprocess.CompletedProcess:
        """Safely execute a subprocess command.

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
        from ..errors import SubprocessError

        # Validate command
        if validate:
            validated_command = self.validate_command(command)
        else:
            validated_command = list(command)

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
                msg = self._format_failure(
                    validated_command,
                    str(cwd_path) if cwd_path else None,
                    result,
                    capture_output,
                )
                raise SubprocessError(
                    msg,
                    code=40,
                    returncode=result.returncode,
                )

            return result

        except subprocess.TimeoutExpired:
            details = self._format_failure(
                validated_command,
                str(cwd_path) if cwd_path else None,
                None,
                capture_output,
            )
            msg = f"Command timed out after {timeout} seconds.\n{details}"
            raise SubprocessError(
                msg,
                code=41,
            )
        except OSError as err:
            details = self._format_failure(
                validated_command,
                str(cwd_path) if cwd_path else None,
                None,
                capture_output,
            )
            msg = f"Failed to execute command: {err}\n{details}"
            raise SubprocessError(msg, code=42)

    def run_simple(
        self,
        command: list[str],
        cwd: str | None = None,
        capture_output=False,
        validate: bool = True,
    ) -> int:
        """Simple subprocess execution that returns exit code.

        Args:
            command: List of command arguments
            cwd: Working directory for the subprocess

        Returns:
            Exit code of the subprocess

        """
        try:
            result = self.run(
                command,
                cwd=cwd,
                check=True,
                capture_output=capture_output,
                validate=validate,
            )
            return result.returncode
        except (SecurityError, SubprocessError, OSError) as e:
            # Never fail silently: report the reason so callers get diagnostics.
            print(f"Error: {e}", file=sys.stderr)
            return 1
