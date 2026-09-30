"""Path Resolution Utilities
Provides secure path resolution and validation for Pytigon commands.
"""

import os
from pathlib import Path


def _resolved(path: Path) -> Path | None:
    """Return the fully resolved form of *path*, or None if it cannot be read.

    Args:
        path: Path to resolve.

    Returns:
        The resolved path, or None when resolution fails.

    """
    try:
        return path.resolve()
    except OSError:
        return None


class PathResolver:

    """Secure path resolution and validation for Pytigon commands.

    Prevents path traversal attacks and ensures paths are within
    allowed directories.
    """

    def __init__(self, base_path: str | None = None):
        """Initialize PathResolver.

        Args:
            base_path: Base directory for path resolution. Defaults to current working directory.

        """
        self.base_path = Path(base_path or os.getcwd()).resolve()

    def resolve(self, path: str, must_exist: bool = False) -> Path:
        """Resolve a path relative to base_path.

        Args:
            path: Path to resolve (can be absolute or relative)
            must_exist: If True, raises error if path doesn't exist

        Returns:
            Resolved Path object

        Raises:
            PathError: If path is invalid or doesn't exist when must_exist=True

        """
        from ..errors import PathError

        try:
            # Convert to Path object
            path_obj = Path(path)

            # If absolute, validate it's within allowed directories
            if path_obj.is_absolute():
                resolved = path_obj.resolve()
                # Check if path is within base_path or system directories
                if not self._is_allowed_path(resolved):
                    msg = f"Access denied: Path '{path}' is outside allowed directories"
                    raise PathError(
                        msg, code=50,
                    )
            else:
                # Relative path - resolve against base_path
                resolved = (self.base_path / path_obj).resolve()

            # Check existence if required
            if must_exist and not resolved.exists():
                msg = f"Path does not exist: {resolved}"
                raise PathError(msg, code=51)

            return resolved

        except (ValueError, OSError) as e:
            msg = f"Invalid path: {path} - {e}"
            raise PathError(msg, code=52)

    def _allowed_roots(self) -> list[Path]:
        """Return the directories a path may resolve into.

        Deliberately generous: Pytigon runs programs out of its own data
        directory, from the interpreter's virtual environment, and from scripts
        next to a project. Blocking those made ``ptig python``, ``ptig run``
        and build scripts fail on a normal installation, while not protecting
        anything - anyone who can invoke a command here can already read the
        files.

        Args:
            None.

        Returns:
            list: Directories to check, most specific first.

        """
        roots = [self.base_path]

        # Pytigon's own data area: the prj/ tree, per-project prjlib/bin,
        # downloaded programs under DATA_PATH.
        data_root = os.environ.get("PYTIGON_DATA") or os.environ.get("PYTIGON_ROOT_PATH")
        if data_root:
            roots.append(Path(data_root))
        try:
            from pytigon_lib.schtools.main_paths import get_main_paths

            roots.append(Path(get_main_paths()["DATA_PATH"]))
        except Exception:
            # Not fatal: the env var above covers the usual case, and the
            # interpreter/home roots below already allow a project's own tree.
            pass

        # The interpreter and its virtual environment. PYTIGON_USERBASE is the
        # *user base* directory, not the environment, so the venv had to be
        # added separately - otherwise the ptig interpreter was rejected.
        import sys

        roots.append(Path(sys.prefix))
        roots.append(Path(os.path.dirname(os.path.abspath(sys.executable))))
        userbase = os.environ.get("PYTHONUSERBASE")
        if userbase:
            roots.append(Path(userbase))

        # A venv normally lives under $HOME, and /home was not in the old
        # hard-coded list, so a default installation could not run its own
        # interpreter from anywhere but its working directory.
        roots.append(Path.home())

        # System directories.
        roots.extend([Path("/usr"), Path("/bin"), Path("/sbin"), Path("/opt")])
        if os.name == "nt":  # Windows
            roots.extend(
                [
                    Path(os.environ.get("ProgramFiles", "C:\\Program Files")),
                    Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")),
                ]
            )

        unique: list[Path] = []
        for root in roots:
            # Both forms are kept: on a usrmerge system /bin is a symlink to
            # /usr/bin, so a caller may pass either spelling and a purely
            # textual relative_to() against the resolved root would miss it.
            for candidate in (root, _resolved(root)):
                if candidate is not None and candidate not in unique:
                    unique.append(candidate)
        return unique

    def _is_allowed_path(self, path: Path) -> bool:
        """Check if a path is within allowed directories.

        Args:
            path: Path to check

        Returns:
            True if path is allowed, False otherwise

        """
        for allowed_dir in self._allowed_roots():
            try:
                path.relative_to(allowed_dir)
                return True
            except ValueError:
                continue
        return False

    def validate_executable(self, executable: str) -> Path:
        """Validate and resolve an executable path.

        Args:
            executable: Executable name or path

        Returns:
            Resolved Path to executable

        Raises:
            PathError: If executable is not found or not allowed

        """
        from ..errors import PathError

        # If it's just a name (no path separators), search in PATH
        if os.sep not in executable and (os.name != "nt" or "/" not in executable):
            import shutil

            exe_path = shutil.which(executable)
            if exe_path is None:
                msg = f"Executable not found: {executable}"
                raise PathError(msg, code=53)
            return Path(exe_path).resolve()

        # Otherwise, resolve as a path
        return self.resolve(executable, must_exist=True)

    def safe_join(self, *paths: str) -> Path:
        """Safely join multiple path components.

        Args:
            *paths: Path components to join

        Returns:
            Joined and resolved Path

        Raises:
            PathError: If resulting path is invalid

        """
        from ..errors import PathError

        try:
            joined = Path(*paths)
            return self.resolve(str(joined))
        except (ValueError, TypeError) as e:
            msg = f"Invalid path join: {e}"
            raise PathError(msg, code=54)
