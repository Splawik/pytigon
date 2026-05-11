"""
Safe Subprocess Execution
Provides secure subprocess execution with input validation and sanitization.
"""

import os
import sys
import subprocess
import shlex
from typing import List, Optional, Tuple, Union
from pathlib import Path


class SafeSubprocess:
    """
    Secure subprocess execution with input validation.
    
    Prevents command injection and ensures safe execution of external commands.
    """
    
    # Allowed executables (can be extended via configuration)
    ALLOWED_EXECUTABLES = {
        'python', 'python3', 'pip', 'pip3',
        'manage.py', 'daphne', 'waitress',
        'nim', 'nimble', 'zig',
    }
    
    # Dangerous shell metacharacters
    DANGEROUS_CHARS = set(';&|`$(){}[]<>!#~')
    
    def __init__(self, allowed_executables: Optional[set] = None):
        """
        Initialize SafeSubprocess.
        
        Args:
            allowed_executables: Set of allowed executable names. Defaults to ALLOWED_EXECUTABLES.
        """
        self.allowed_executables = allowed_executables or self.ALLOWED_EXECUTABLES.copy()
    
    def validate_command(self, command: List[str]) -> List[str]:
        """
        Validate and sanitize command arguments.
        
        Args:
            command: List of command arguments
            
        Returns:
            Validated and sanitized command list
            
        Raises:
            SecurityError: If command contains dangerous characters or invalid executable
        """
        from ..errors import SecurityError
        
        if not command:
            raise SecurityError("Empty command", code=20)
        
        # Validate executable
        executable = command[0]
        if not self._is_executable_allowed(executable):
            raise SecurityError(
                f"Executable not allowed: {executable}",
                code=21
            )
        
        # Validate each argument
        sanitized = []
        for i, arg in enumerate(command):
            if not isinstance(arg, str):
                raise SecurityError(
                    f"Argument {i} must be a string, got {type(arg).__name__}",
                    code=22
                )
            
            # Check for dangerous characters
            if self._contains_dangerous_chars(arg):
                raise SecurityError(
                    f"Argument {i} contains dangerous characters: {arg}",
                    code=23
                )
            
            sanitized.append(arg)
        
        return sanitized
    
    def _is_executable_allowed(self, executable: str) -> bool:
        """
        Check if an executable is allowed.
        
        Args:
            executable: Executable name or path
            
        Returns:
            True if executable is allowed, False otherwise
        """
        # Extract just the executable name if it's a path
        exe_name = Path(executable).name
        
        # Check against allowed list
        if exe_name in self.allowed_executables:
            return True
        
        # Allow Python interpreter
        if executable in (sys.executable, 'python', 'python3'):
            return True
        
        # Allow get_executable() result
        try:
            from pytigon_lib.schtools.tools import get_executable
            if executable == get_executable():
                return True
        except ImportError:
            pass
        
        return False
    
    def _contains_dangerous_chars(self, arg: str) -> bool:
        """
        Check if an argument contains dangerous shell characters.
        
        Args:
            arg: Argument to check
            
        Returns:
            True if argument contains dangerous characters, False otherwise
        """
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
        self,
        command: List[str],
        cwd: Optional[str] = None,
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
            result = self.run(command, cwd=cwd, check=False)
            return result.returncode
        except Exception:
            return 1
