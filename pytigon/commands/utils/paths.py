"""
Path Resolution Utilities
Provides secure path resolution and validation for Pytigon commands.
"""

import os
import sys
from typing import Optional, Tuple
from pathlib import Path


class PathResolver:
    """
    Secure path resolution and validation.
    
    Prevents path traversal attacks and ensures paths are within
    allowed directories.
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize PathResolver.
        
        Args:
            base_path: Base directory for path resolution. Defaults to current working directory.
        """
        self.base_path = Path(base_path or os.getcwd()).resolve()
    
    def resolve(self, path: str, must_exist: bool = False) -> Path:
        """
        Resolve a path relative to base_path.
        
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
                    raise PathError(
                        f"Access denied: Path '{path}' is outside allowed directories",
                        code=50
                    )
            else:
                # Relative path - resolve against base_path
                resolved = (self.base_path / path_obj).resolve()
            
            # Check existence if required
            if must_exist and not resolved.exists():
                raise PathError(
                    f"Path does not exist: {resolved}",
                    code=51
                )
            
            return resolved
            
        except (ValueError, OSError) as e:
            raise PathError(f"Invalid path: {path} - {e}", code=52)
    
    def _is_allowed_path(self, path: Path) -> bool:
        """
        Check if a path is within allowed directories.
        
        Args:
            path: Path to check
            
        Returns:
            True if path is allowed, False otherwise
        """
        # Allow paths within base_path
        try:
            path.relative_to(self.base_path)
            return True
        except ValueError:
            pass
        
        # Allow system directories (for subprocess execution)
        allowed_system_dirs = [
            Path("/usr"),
            Path("/bin"),
            Path("/sbin"),
            Path("/opt"),
        ]
        
        if os.name == "nt":  # Windows
            allowed_system_dirs.extend([
                Path(os.environ.get("ProgramFiles", "C:\\Program Files")),
                Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")),
            ])
        
        for allowed_dir in allowed_system_dirs:
            try:
                path.relative_to(allowed_dir)
                return True
            except ValueError:
                continue
        
        return False
    
    def validate_executable(self, executable: str) -> Path:
        """
        Validate and resolve an executable path.
        
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
                raise PathError(
                    f"Executable not found: {executable}",
                    code=53
                )
            return Path(exe_path).resolve()
        
        # Otherwise, resolve as a path
        return self.resolve(executable, must_exist=True)
    
    def safe_join(self, *paths: str) -> Path:
        """
        Safely join multiple path components.
        
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
            raise PathError(f"Invalid path join: {e}", code=54)
