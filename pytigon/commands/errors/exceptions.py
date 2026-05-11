"""
Structured Exception Hierarchy
Provides specific exception types for different error scenarios.
"""


class PytigonError(Exception):
    """
    Base exception for all Pytigon errors.

    Attributes:
        message: Error message
        code: Numeric error code for programmatic handling
        details: Additional error details
    """

    def __init__(self, message: str, code: int = 0, **details):
        """
        Initialize PytigonError.

        Args:
            message: Error message
            code: Numeric error code
            **details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.code:
            return f"[Error {self.code}] {self.message}"
        return self.message

    def to_dict(self) -> dict:
        """Convert error to dictionary representation."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }


class ConfigurationError(PytigonError):
    """
    Configuration-related errors.

    Error codes:
        10: Missing configuration
        11: Invalid configuration value
        12: Configuration file not found
        13: Configuration parse error
    """

    pass


class SecurityError(PytigonError):
    """
    Security-related errors.

    Error codes:
        20: Command injection attempt
        21: Invalid executable
        22: Invalid argument type
        23: Dangerous characters in input
        24: Path traversal attempt
        25: Access denied
    """

    pass


class CommandError(PytigonError):
    """
    Command execution errors.

    Error codes:
        30: Unknown command
        31: Invalid command arguments
        32: Command execution failed
        33: Command timeout
    """

    pass


class SubprocessError(PytigonError):
    """
    Subprocess execution errors.

    Error codes:
        40: Subprocess failed (non-zero exit)
        41: Subprocess timeout
        42: Subprocess execution error
        43: Subprocess not found
    """

    def __init__(self, message: str, code: int = 40, returncode: int = 0, **details):
        """
        Initialize SubprocessError.

        Args:
            message: Error message
            code: Numeric error code
            returncode: Subprocess return code
            **details: Additional error details
        """
        super().__init__(message, code, **details)
        self.returncode = returncode

    def to_dict(self) -> dict:
        """Convert error to dictionary representation."""
        result = super().to_dict()
        result["returncode"] = self.returncode
        return result


class PathError(PytigonError):
    """
    Path-related errors.

    Error codes:
        50: Path access denied
        51: Path does not exist
        52: Invalid path
        53: Executable not found
        54: Invalid path join
    """

    pass


class ValidationError(PytigonError):
    """
    Input validation errors.

    Error codes:
        60: Missing required argument
        61: Invalid argument value
        62: Argument type mismatch
        63: Argument out of range
    """

    pass


class ResourceError(PytigonError):
    """
    Resource-related errors.

    Error codes:
        70: Resource not found
        71: Resource already exists
        72: Resource busy
        73: Resource exhausted
    """

    pass
