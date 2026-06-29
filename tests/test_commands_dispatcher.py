"""Pytest tests for CommandDispatcher and related command infrastructure.
"""

import pytest

from pytigon.commands.dispatcher import CommandDispatcher
from pytigon.commands.handlers import (
    DefaultCommandHandler,
    InitCommandHandler,
    ManageCommandHandler,
    PythonCommandHandler,
    RunCommandHandler,
    RunServerCommandHandler,
    ToolCommandHandler,
)
from pytigon.commands.registry import CommandRegistry

# ---------------------------------------------------------------------------
# CommandRegistry tests
# ---------------------------------------------------------------------------


class TestCommandRegistry:
    def test_initialization(self):
        """Test CommandRegistry initializes with empty handler lists."""
        registry = CommandRegistry()
        assert len(registry) == 0
        assert registry.get_all_handlers() == []
        assert registry.get_command_names() == []

    def test_register_handler(self):
        """Test registering a single handler."""
        registry = CommandRegistry()
        handler = ManageCommandHandler()
        registry.register(handler)
        assert len(registry) == 1
        assert handler in registry
        assert "manage" in registry.get_command_names()

    def test_register_multiple_handlers(self):
        """Test registering multiple handlers."""
        registry = CommandRegistry()
        handlers = [
            ManageCommandHandler(),
            RunCommandHandler(),
            RunServerCommandHandler(),
        ]
        for h in handlers:
            registry.register(h)
        assert len(registry) == 3
        assert "manage" in registry.get_command_names()
        assert "run" in registry.get_command_names()
        assert "runserver" in registry.get_command_names()

    def test_register_invalid_type_raises_error(self):
        """Test registering a non-handler raises TypeError."""
        registry = CommandRegistry()
        with pytest.raises(TypeError, match="must be an instance of CommandHandler"):
            registry.register("not_a_handler")

    def test_find_handler_returns_correct_handler(self):
        """Test find_handler returns the correct handler based on argv."""
        registry = CommandRegistry()
        manage = ManageCommandHandler()
        run = RunCommandHandler()
        registry.register(manage)
        registry.register(run)

        found = registry.find_handler(["pytigon", "manage_test"])
        assert found is manage

        found = registry.find_handler(["pytigon", "run_test"])
        assert found is run

    def test_find_handler_returns_none_for_unknown_command(self):
        """Test find_handler returns None for unknown commands."""
        registry = CommandRegistry()
        registry.register(ManageCommandHandler())
        found = registry.find_handler(["pytigon", "unknown_cmd"])
        assert found is None

    def test_get_handler_by_name(self):
        """Test get_handler returns handler by command name."""
        registry = CommandRegistry()
        handler = ManageCommandHandler()
        registry.register(handler)
        assert registry.get_handler("manage") is handler
        assert registry.get_handler("nonexistent") is None

    def test_unregister_handler(self):
        """Test unregistering a handler."""
        registry = CommandRegistry()
        handler = ManageCommandHandler()
        registry.register(handler)
        assert len(registry) == 1
        registry.unregister(handler)
        assert len(registry) == 0
        assert handler not in registry
        assert "manage" not in registry.get_command_names()

    def test_unregister_nonexistent_handler(self):
        """Test unregistering a handler not in registry does nothing."""
        registry = CommandRegistry()
        handler = ManageCommandHandler()
        registry.register(handler)
        other = RunCommandHandler()
        registry.unregister(other)  # Should not raise
        assert len(registry) == 1

    def test_clear_removes_all_handlers(self):
        """Test clear removes all registered handlers."""
        registry = CommandRegistry()
        registry.register(ManageCommandHandler())
        registry.register(RunCommandHandler())
        registry.clear()
        assert len(registry) == 0
        assert registry.get_all_handlers() == []
        assert registry.get_command_names() == []

    def test_get_command_names_returns_copy(self):
        """Test get_command_names returns a list copy."""
        registry = CommandRegistry()
        registry.register(ManageCommandHandler())
        names = registry.get_command_names()
        assert names == ["manage"]


# ---------------------------------------------------------------------------
# CommandDispatcher tests
# ---------------------------------------------------------------------------


class TestCommandDispatcher:
    def test_dispatcher_creation(self):
        """Test that dispatcher can be created with default config."""
        dispatcher = CommandDispatcher()
        assert dispatcher is not None
        assert len(dispatcher.registry) > 0

    def test_dispatcher_creation_with_config(self):
        """Test dispatcher creation with custom config."""
        dispatcher = CommandDispatcher(config={"debug": True})
        assert dispatcher.config["debug"] is True

    def test_handler_registration(self):
        """Test that default handlers are registered on creation."""
        dispatcher = CommandDispatcher()
        handlers = dispatcher.registry.get_all_handlers()
        assert len(handlers) >= 7
        assert "manage" in dispatcher.registry.get_command_names()
        assert "run" in dispatcher.registry.get_command_names()
        assert "runserver" in dispatcher.registry.get_command_names()
        assert "python" in dispatcher.registry.get_command_names()
        assert "init" in dispatcher.registry.get_command_names()
        assert "tool" in dispatcher.registry.get_command_names()
        assert "default" in dispatcher.registry.get_command_names()

    def test_dispatch_help_command(self):
        """Test dispatcher handles help command without error."""
        dispatcher = CommandDispatcher()
        exit_code = dispatcher.dispatch(["pytigon", "--help"])
        assert exit_code == 0

    def test_dispatch_unknown_command(self):
        """Test dispatcher falls back to DefaultCommandHandler for any command.

        DefaultCommandHandler is designed as a catch-all fallback,
        so it handles any command not caught by previous handlers.
        The fallback may try to start GUI which calls sys.exit.
        """
        dispatcher = CommandDispatcher()
        try:
            exit_code = dispatcher.dispatch(["pytigon", "nonexistent_command_xyz"])
            assert isinstance(exit_code, int)
        except SystemExit as e:
            # pytigon_gui calls sys.exit(0) on import
            # This is expected behavior when GUI is available
            assert e.code == 0

    def test_get_available_commands(self):
        """Test get_available_commands returns command names."""
        dispatcher = CommandDispatcher()
        commands = dispatcher.get_available_commands()
        assert isinstance(commands, list)
        assert "manage" in commands

    def test_get_handler_for_command(self):
        """Test get_handler_for_command returns correct handler."""
        dispatcher = CommandDispatcher()
        handler = dispatcher.get_handler_for_command("manage")
        assert handler is not None
        assert isinstance(handler, ManageCommandHandler)
        assert dispatcher.get_handler_for_command("nonexistent") is None

    def test_dispatch_with_context(self):
        """Test dispatch_with_context works correctly."""
        dispatcher = CommandDispatcher()
        exit_code = dispatcher.dispatch_with_context(
            ["pytigon", "--help"], context={"source": "test"},
        )
        assert exit_code == 0


# ---------------------------------------------------------------------------
# Specific handler tests
# ---------------------------------------------------------------------------


class TestManageCommandHandler:
    def test_can_handle_manage_commands(self):
        handler = ManageCommandHandler()
        assert handler.can_handle(["pytigon", "manage_test"])
        assert handler.can_handle(["pytigon", "manage_myapp"])

    def test_rejects_non_manage_commands(self):
        handler = ManageCommandHandler()
        assert not handler.can_handle(["pytigon", "run_test"])
        assert not handler.can_handle(["pytigon", "runserver_test"])

    def test_get_app_name(self):
        handler = ManageCommandHandler()
        assert handler.get_app_name(["pytigon", "manage_myapp"]) == "myapp"
        assert handler.get_app_name(["pytigon", "manage"]) is None


class TestRunCommandHandler:
    def test_can_handle_run_commands(self):
        handler = RunCommandHandler()
        assert handler.can_handle(["pytigon", "run_test"])
        assert handler.can_handle(["pytigon", "run_myapp"])

    def test_rejects_non_run_commands(self):
        handler = RunCommandHandler()
        assert not handler.can_handle(["pytigon", "manage_test"])
        assert not handler.can_handle(["pytigon", "python_test"])

    def test_get_app_name(self):
        handler = RunCommandHandler()
        assert handler.get_app_name(["pytigon", "run_myapp"]) == "myapp"
        assert handler.get_app_name(["pytigon", "run"]) is None


class TestRunServerCommandHandler:
    def test_can_handle_runserver_commands(self):
        handler = RunServerCommandHandler()
        assert handler.can_handle(["pytigon", "runserver_test"])
        assert handler.can_handle(["pytigon", "runserver_myapp"])

    def test_rejects_non_runserver_commands(self):
        handler = RunServerCommandHandler()
        assert not handler.can_handle(["pytigon", "manage_test"])
        assert not handler.can_handle(["pytigon", "run_test"])


class TestPythonCommandHandler:
    def test_can_handle_python_commands(self):
        handler = PythonCommandHandler()
        assert handler.can_handle(["pytigon", "python_script"])
        assert handler.can_handle(["pytigon", "python_myapp"])

    def test_rejects_non_python_commands(self):
        handler = PythonCommandHandler()
        assert not handler.can_handle(["pytigon", "manage_test"])


class TestInitCommandHandler:
    def test_can_handle_init_commands(self):
        handler = InitCommandHandler()
        assert handler.can_handle(["pytigon", "init_newapp"])
        assert handler.can_handle(["pytigon", "init_project"])

    def test_rejects_non_init_commands(self):
        handler = InitCommandHandler()
        assert not handler.can_handle(["pytigon", "manage_test"])


class TestToolCommandHandler:
    def test_can_handle_tool_commands(self):
        handler = ToolCommandHandler()
        assert handler.can_handle(["pytigon", "nim"])
        assert handler.can_handle(["pytigon", "nimble"])
        assert handler.can_handle(["pytigon", "@mytool"])
        assert handler.can_handle(["pytigon", "-y"])

    def test_rejects_non_tool_commands(self):
        handler = ToolCommandHandler()
        assert not handler.can_handle(["pytigon", "manage_test"])
        assert not handler.can_handle(["pytigon", "python_script"])


class TestDefaultCommandHandler:
    def test_can_handle_any_command(self):
        """DefaultCommandHandler is the fallback and handles everything."""
        handler = DefaultCommandHandler()
        assert handler.can_handle(["pytigon", "any_random_command"])
        assert handler.can_handle(["pytigon", "something_else"])
        assert handler.can_handle([])
        assert handler.can_handle(["pytigon"])
