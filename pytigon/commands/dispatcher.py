"""
Command Dispatcher
Routes commands to appropriate handlers.
"""

import sys
from typing import List, Optional, Dict, Any

from .registry import CommandRegistry
from .errors import CommandError, ErrorHandler
from .handlers import CommandHandler


class CommandDispatcher:
    """
    Command dispatcher that routes commands to appropriate handlers.
    
    Uses the CommandRegistry to find the appropriate handler for each command.
    Provides centralized error handling and logging.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize CommandDispatcher.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.registry = CommandRegistry()
        self.error_handler = ErrorHandler(debug=self.config.get('debug', False))
        
        # Register default handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self) -> None:
        """Register default command handlers."""
        from .handlers import (
            ManageCommandHandler,
            RunCommandHandler,
            RunServerCommandHandler,
            PythonCommandHandler,
            PipCommandHandler,
            InitCommandHandler,
            ToolCommandHandler,
            DefaultCommandHandler,
        )
        
        # Register handlers in priority order
        self.registry.register(ManageCommandHandler(self.config))
        self.registry.register(RunCommandHandler(self.config))
        self.registry.register(RunServerCommandHandler(self.config))
        self.registry.register(PythonCommandHandler(self.config))
        self.registry.register(PipCommandHandler(self.config))
        self.registry.register(InitCommandHandler(self.config))
        self.registry.register(ToolCommandHandler(self.config))
        self.registry.register(DefaultCommandHandler(self.config))
    
    def dispatch(self, argv: List[str], **kwargs) -> int:
        """
        Dispatch a command to the appropriate handler.
        
        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            # Find appropriate handler
            handler = self.registry.find_handler(argv)
            
            if handler is None:
                raise CommandError(
                    f"No handler found for command: {argv[1] if len(argv) > 1 else 'unknown'}",
                    code=30
                )
            
            # Execute the handler
            return handler.execute(argv, **kwargs)
            
        except CommandError as e:
            # Handle command-specific errors
            return self.error_handler.handle(e, {'argv': argv})
        except Exception as e:
            # Handle unexpected errors
            return self.error_handler.handle(e, {'argv': argv})
    
    def dispatch_with_context(self, argv: List[str], context: Optional[Dict[str, Any]] = None) -> int:
        """
        Dispatch a command with error context.
        
        Args:
            argv: Command arguments
            context: Additional context for error handling
            
        Returns:
            Exit code
        """
        with self.error_handler.error_context(context or {'argv': argv}):
            return self.dispatch(argv)
    
    def get_available_commands(self) -> List[str]:
        """
        Get list of available commands.
        
        Returns:
            List of command names
        """
        return self.registry.get_command_names()
    
    def get_handler_for_command(self, command: str) -> Optional[CommandHandler]:
        """
        Get handler for a specific command.
        
        Args:
            command: Command name
            
        Returns:
            CommandHandler instance or None
        """
        return self.registry.get_handler(command)
