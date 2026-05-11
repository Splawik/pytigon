"""
Centralized Error Handler
Provides consistent error handling and logging across all commands.
"""

import sys
import logging
import traceback
from typing import Optional, Dict, Any
from contextlib import contextmanager

from .exceptions import PytigonError


class ErrorHandler:
    """
    Centralized error handler for Pytigon commands.

    Provides consistent error logging, user-friendly messages,
    and proper exit code determination.
    """

    # Exit codes for different error types
    EXIT_CODES = {
        "ConfigurationError": 10,
        "SecurityError": 20,
        "CommandError": 30,
        "SubprocessError": 40,
        "PathError": 50,
        "ValidationError": 60,
        "ResourceError": 70,
        "KeyboardInterrupt": 130,
        "SystemExit": 0,
    }

    def __init__(self, logger: Optional[logging.Logger] = None, debug: bool = False):
        """
        Initialize ErrorHandler.

        Args:
            logger: Logger instance for error logging. Defaults to root logger.
            debug: Whether to enable debug mode (shows full tracebacks)
        """
        self.logger = logger or logging.getLogger("pytigon")
        self.debug = debug

    def handle(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> int:
        """
        Handle an exception and return appropriate exit code.

        Args:
            error: Exception to handle
            context: Additional context information

        Returns:
            Exit code for the error
        """
        # Get error type name
        error_type = type(error).__name__

        # Determine exit code
        exit_code = self._get_exit_code(error, error_type)

        # Log the error
        self._log_error(error, error_type, context)

        # Print user-friendly message
        self._print_user_message(error, error_type)

        return exit_code

    def _get_exit_code(self, error: Exception, error_type: str) -> int:
        """
        Determine exit code for an error.

        Args:
            error: Exception instance
            error_type: Error type name

        Returns:
            Exit code
        """
        # Check if it's a PytigonError with a code
        if isinstance(error, PytigonError) and error.code:
            return error.code

        # Check EXIT_CODES mapping
        if error_type in self.EXIT_CODES:
            return self.EXIT_CODES[error_type]

        # Default exit code for unknown errors
        return 1

    def _log_error(
        self,
        error: Exception,
        error_type: str,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Log error with appropriate level.

        Args:
            error: Exception instance
            error_type: Error type name
            context: Additional context information
        """
        # Build log message
        log_parts = [f"{error_type}: {error}"]

        if context:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            log_parts.append(f"Context: {context_str}")

        log_message = " | ".join(log_parts)

        # Log with appropriate level
        if isinstance(error, PytigonError):
            # PytigonError instances are expected errors
            self.logger.warning(log_message)
        else:
            # Unexpected errors get error level
            self.logger.error(log_message)

        # Log full traceback in debug mode
        if self.debug:
            self.logger.debug(traceback.format_exc())

    def _print_user_message(self, error: Exception, error_type: str):
        """
        Print user-friendly error message.

        Args:
            error: Exception instance
            error_type: Error type name
        """
        # Format user-friendly message
        if isinstance(error, PytigonError):
            # Use the error's message directly
            message = str(error)
        else:
            # Generic message for unexpected errors
            message = f"An error occurred: {error}"

        # Print to stderr
        print(f"Error: {message}", file=sys.stderr)

        # Print help hint for common errors
        if error_type == "CommandError":
            print("Hint: Use --help to see available commands", file=sys.stderr)
        elif error_type == "SecurityError":
            print(
                "Hint: Check your command arguments for special characters",
                file=sys.stderr,
            )
        elif error_type == "ConfigurationError":
            print(
                "Hint: Check your configuration files and environment variables",
                file=sys.stderr,
            )

    @contextmanager
    def error_context(self, context: Optional[Dict[str, Any]] = None):
        """
        Context manager for error handling.

        Args:
            context: Additional context information

        Yields:
            None

        Example:
            with error_handler.error_context({'command': 'manage'}):
                # Code that might raise exceptions
                pass
        """
        try:
            yield
        except Exception as e:
            exit_code = self.handle(e, context)
            sys.exit(exit_code)

    def format_error(self, error: Exception) -> str:
        """
        Format error for display.

        Args:
            error: Exception instance

        Returns:
            Formatted error string
        """
        if isinstance(error, PytigonError):
            return str(error)

        error_type = type(error).__name__
        return f"{error_type}: {error}"

    def get_error_details(self, error: Exception) -> Dict[str, Any]:
        """
        Get detailed error information.

        Args:
            error: Exception instance

        Returns:
            Dictionary with error details
        """
        details = {
            "type": type(error).__name__,
            "message": str(error),
        }

        if isinstance(error, PytigonError):
            details["code"] = error.code
            details["details"] = error.details

        if self.debug:
            details["traceback"] = traceback.format_exc()

        return details
