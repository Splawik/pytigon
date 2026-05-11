"""
Pytest tests for pytigon.commands.errors module (exceptions and error handler).
"""

import pytest
import logging
from pytigon.commands.errors.exceptions import (
    PytigonError,
    ConfigurationError,
    SecurityError,
    CommandError,
    SubprocessError,
    PathError,
    ValidationError,
    ResourceError,
)
from pytigon.commands.errors.handler import ErrorHandler


# ---------------------------------------------------------------------------
# PytigonError base class tests
# ---------------------------------------------------------------------------


class TestPytigonError:
    def test_creation_with_message_only(self):
        err = PytigonError("Something went wrong")
        assert err.message == "Something went wrong"
        assert err.code == 0
        assert err.details == {}

    def test_creation_with_code(self):
        err = PytigonError("Config error", code=10)
        assert err.message == "Config error"
        assert err.code == 10

    def test_creation_with_details(self):
        err = PytigonError("Error", code=5, key="value", path="/test")
        assert err.details == {"key": "value", "path": "/test"}

    def test_str_representation_with_code(self):
        err = PytigonError("Test error", code=42)
        assert str(err) == "[Error 42] Test error"

    def test_str_representation_without_code(self):
        err = PytigonError("Test error")
        assert str(err) == "Test error"

    def test_to_dict(self):
        err = PytigonError("Test", code=10, extra="data")
        d = err.to_dict()
        assert d["type"] == "PytigonError"
        assert d["message"] == "Test"
        assert d["code"] == 10
        assert d["details"] == {"extra": "data"}


# ---------------------------------------------------------------------------
# Specific exception types tests
# ---------------------------------------------------------------------------


class TestConfigurationError:
    def test_is_pytigon_error(self):
        err = ConfigurationError("Missing config")
        assert isinstance(err, PytigonError)
        assert isinstance(err, ConfigurationError)

    def test_default_code(self):
        err = ConfigurationError("test")
        assert err.code == 0  # No default code set


class TestSecurityError:
    def test_is_pytigon_error(self):
        err = SecurityError("Invalid input", code=20)
        assert isinstance(err, PytigonError)
        assert isinstance(err, SecurityError)
        assert err.code == 20


class TestCommandError:
    def test_is_pytigon_error(self):
        err = CommandError("Unknown command", code=30)
        assert isinstance(err, PytigonError)
        assert isinstance(err, CommandError)


class TestSubprocessError:
    def test_has_returncode(self):
        err = SubprocessError("Failed", code=40, returncode=1)
        assert err.returncode == 1
        assert err.code == 40

    def test_to_dict_includes_returncode(self):
        err = SubprocessError("Failed", code=40, returncode=2)
        d = err.to_dict()
        assert d["returncode"] == 2
        assert d["code"] == 40


class TestPathError:
    def test_is_pytigon_error(self):
        err = PathError("Path not found", code=51)
        assert isinstance(err, PytigonError)
        assert isinstance(err, PathError)


class TestValidationError:
    def test_is_pytigon_error(self):
        err = ValidationError("Invalid argument", code=61)
        assert isinstance(err, PytigonError)
        assert isinstance(err, ValidationError)


class TestResourceError:
    def test_is_pytigon_error(self):
        err = ResourceError("Resource not found", code=70)
        assert isinstance(err, PytigonError)
        assert isinstance(err, ResourceError)


# ---------------------------------------------------------------------------
# ErrorHandler tests
# ---------------------------------------------------------------------------


class TestErrorHandler:
    def test_initialization_default(self):
        handler = ErrorHandler()
        assert handler.debug is False
        assert isinstance(handler.logger, logging.Logger)

    def test_initialization_debug_mode(self):
        handler = ErrorHandler(debug=True)
        assert handler.debug is True

    def test_initialization_custom_logger(self):
        logger = logging.getLogger("test_handler")
        handler = ErrorHandler(logger=logger)
        assert handler.logger is logger

    def test_handle_pytigon_error(self):
        handler = ErrorHandler()
        err = CommandError("Unknown command", code=30)
        exit_code = handler.handle(err)
        assert exit_code == 30

    def test_handle_generic_exception(self):
        handler = ErrorHandler()
        err = ValueError("Something is wrong")
        exit_code = handler.handle(err)
        assert exit_code == 1

    def test_handle_keyboard_interrupt(self):
        handler = ErrorHandler()
        exit_code = handler.handle(KeyboardInterrupt())
        assert exit_code == 130

    def test_handle_system_exit(self):
        handler = ErrorHandler()
        exit_code = handler.handle(SystemExit())
        assert exit_code == 0

    def test_get_exit_code_from_mapping(self):
        handler = ErrorHandler()
        assert handler._get_exit_code(SecurityError("test"), "SecurityError") == 20
        assert handler._get_exit_code(CommandError("test"), "CommandError") == 30
        assert handler._get_exit_code(PathError("test"), "PathError") == 50

    def test_get_exit_code_from_error_code_attribute(self):
        handler = ErrorHandler()
        err = ConfigurationError("test", code=11)
        assert handler._get_exit_code(err, "ConfigurationError") == 11

    def test_format_error_pytigon(self):
        handler = ErrorHandler()
        err = SecurityError("Dangerous input", code=23)
        formatted = handler.format_error(err)
        assert "[Error 23] Dangerous input" in formatted

    def test_format_error_generic(self):
        handler = ErrorHandler()
        err = ValueError("Something")
        formatted = handler.format_error(err)
        assert "ValueError: Something" in formatted

    def test_get_error_details(self):
        handler = ErrorHandler()
        err = CommandError("Test", code=31, detail="extra")
        details = handler.get_error_details(err)
        assert details["type"] == "CommandError"
        assert details["message"] == "[Error 31] Test"
        assert details["code"] == 31
        assert details["details"] == {"detail": "extra"}

    def test_get_error_details_generic(self):
        handler = ErrorHandler()
        err = RuntimeError("Test runtime")
        details = handler.get_error_details(err)
        assert details["type"] == "RuntimeError"
        assert details["message"] == "Test runtime"
        assert "code" not in details

    def test_error_context_manager(self):
        handler = ErrorHandler()
        try:
            with handler.error_context({"command": "test"}):
                raise CommandError("Test error", code=30)
        except SystemExit as e:
            assert e.code == 30
        else:
            pytest.fail("Expected SystemExit")

    def test_error_context_manager_no_error(self):
        handler = ErrorHandler()
        with handler.error_context({"command": "test"}):
            pass  # Should not raise
