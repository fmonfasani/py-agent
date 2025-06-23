"""Context management for session persistence"""

from typing import Any, Dict, Optional


class ContextManager:
    """Manages session context and memory across requests"""

    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}

    def get_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get context for a session"""
        return self.contexts.get(session_id)

    def set_context(self, session_id: str, context: Dict[str, Any]) -> None:
        """Set context for a session"""
        self.contexts[session_id] = context

    def clear_context(self, session_id: Optional[str] = None) -> None:
        """Clear context for a session or all sessions"""
        if session_id:
            self.contexts.pop(session_id, None)
        else:
            self.contexts.clear()

    def update_context(self, session_id: str, updates: Dict[str, Any]) -> None:
        """Update context with new information"""
        if session_id not in self.contexts:
            self.contexts[session_id] = {}
        self.contexts[session_id].update(updates)
