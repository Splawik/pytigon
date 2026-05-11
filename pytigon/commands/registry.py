"""
Command Registry
Manages command handler registration and lookup.
"""

from typing import List, Optional, Dict

from .handlers import CommandHandler


class CommandRegistry:
    """
    Registry for command handlers.
    
    Manages registration and lookup of command handlers.
    Handlers are checked in registration order.
    """
    
    def __init__(self):
        """Initialize CommandRegistry."""
        self._handlers: List[CommandHandler] = []
        self._handler_map: Dict[str, CommandHandler] = {}
    
    def register(self, handler: CommandHandler) -> None:
        """
        Register a command handler.
        
        Args:
            handler: CommandHandler instance to register
        """
        if not isinstance(handler, CommandHandler):
            raise TypeError(f"Handler must be an instance of CommandHandler, got {type(handler).__name__}")
        
        self._handlers.append(handler)
        
        # Also register by command name if available
        command_name = self._get_handler_command_name(handler)
        if command_name:
            self._handler_map[command_name] = handler
    
    def _get_handler_command_name(self, handler: CommandHandler) -> Optional[str]:
        """
        Get command name from handler class.
        
        Args:
            handler: CommandHandler instance
            
        Returns:
            Command name or None
        """
        # Extract command name from class name
        class_name = handler.__class__.__name__
        if class_name.endswith('CommandHandler'):
            return class_name[:-14].lower()  # Remove 'CommandHandler' suffix
        return None
    
    def find_handler(self, argv: List[str]) -> Optional[CommandHandler]:
        """
        Find appropriate handler for command arguments.
        
        Args:
            argv: Command arguments
            
        Returns:
            CommandHandler instance or None if no handler found
        """
        for handler in self._handlers:
            if handler.can_handle(argv):
                return handler
        return None
    
    def get_handler(self, command: str) -> Optional[CommandHandler]:
        """
        Get handler by command name.
        
        Args:
            command: Command name
            
        Returns:
            CommandHandler instance or None
        """
        return self._handler_map.get(command)
    
    def get_command_names(self) -> List[str]:
        """
        Get list of registered command names.
        
        Returns:
            List of command names
        """
        return list(self._handler_map.keys())
    
    def get_all_handlers(self) -> List[CommandHandler]:
        """
        Get all registered handlers.
        
        Returns:
            List of CommandHandler instances
        """
        return self._handlers.copy()
    
    def unregister(self, handler: CommandHandler) -> None:
        """
        Unregister a command handler.
        
        Args:
            handler: CommandHandler instance to unregister
        """
        if handler in self._handlers:
            self._handlers.remove(handler)
            
            # Remove from handler map
            command_name = self._get_handler_command_name(handler)
            if command_name and command_name in self._handler_map:
                del self._handler_map[command_name]
    
    def clear(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()
        self._handler_map.clear()
    
    def __len__(self) -> int:
        """Return number of registered handlers."""
        return len(self._handlers)
    
    def __contains__(self, handler: CommandHandler) -> bool:
        """Check if handler is registered."""
        return handler in self._handlers
