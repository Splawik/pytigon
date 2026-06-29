"""Basic tests for command dispatcher.
"""

import os
import sys

# Add pytigon to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytigon.commands import CommandDispatcher
from pytigon.commands.handlers import (
    ManageCommandHandler,
    RunCommandHandler,
    RunServerCommandHandler,
)


def test_dispatcher_creation():
    """Test that dispatcher can be created."""
    dispatcher = CommandDispatcher()
    assert dispatcher is not None
    print("✓ Dispatcher creation test passed")


def test_handler_registration():
    """Test that handlers are registered."""
    dispatcher = CommandDispatcher()
    handlers = dispatcher.registry.get_all_handlers()
    assert len(handlers) > 0
    print(f"✓ Handler registration test passed ({len(handlers)} handlers registered)")


def test_manage_handler():
    """Test manage command handler."""
    handler = ManageCommandHandler()
    assert handler.can_handle(["pytigon", "manage_test"])
    assert not handler.can_handle(["pytigon", "run_test"])
    print("✓ Manage handler test passed")


def test_run_handler():
    """Test run command handler."""
    handler = RunCommandHandler()
    assert handler.can_handle(["pytigon", "run_test"])
    assert not handler.can_handle(["pytigon", "manage_test"])
    print("✓ Run handler test passed")


def test_runserver_handler():
    """Test runserver command handler."""
    handler = RunServerCommandHandler()
    assert handler.can_handle(["pytigon", "runserver_test"])
    assert not handler.can_handle(["pytigon", "manage_test"])
    print("✓ RunServer handler test passed")


def test_dispatcher_dispatch():
    """Test dispatcher dispatch."""
    dispatcher = CommandDispatcher()
    # Test with help command (should not fail)
    exit_code = dispatcher.dispatch(["pytigon", "--help"])
    assert exit_code == 0
    print("✓ Dispatcher dispatch test passed")


if __name__ == "__main__":
    print("Running command dispatcher tests...")
    print()

    try:
        test_dispatcher_creation()
        test_handler_registration()
        test_manage_handler()
        test_run_handler()
        test_runserver_handler()
        test_dispatcher_dispatch()

        print()
        print("All tests passed! ✓")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
