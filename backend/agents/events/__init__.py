"""
Codopia Agent Event System
==========================

Inspired by agentic-framework's rich event system.
Events are emitted during agent runs and streamed to the frontend
via Socket.IO so kids can see what the AI is "thinking."

Event Types:
    AgentThinking   — The agent is reasoning about the problem
    ToolCall        — The agent is using a tool (code execution, simulation, etc.)
    ToolResult      — A tool returned a result
    PauseForInput   — The agent is asking the student a question
    StudentResponse — The student answered a question
    ChatOutput      — Final text/voice output to the student
    TurnEnd         — The agent finished processing
    ErrorEvent      — Something went wrong (with kid-friendly message)
"""

import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional, Dict, List


class EventType(str, Enum):
    """All possible event types in the Codopia agent system."""
    AGENT_THINKING = "agent_thinking"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    PAUSE_FOR_INPUT = "pause_for_input"
    STUDENT_RESPONSE = "student_response"
    CHAT_OUTPUT = "chat_output"
    CODE_OUTPUT = "code_output"
    SIMULATION_UPDATE = "simulation_update"
    TURN_END = "turn_end"
    ERROR = "error"


@dataclass
class AgentEvent:
    """Base event emitted by the agent system."""
    event_type: EventType
    agent_name: str
    data: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)
    tier: Optional[str] = None  # "magic_workshop", "innovation_lab", "professional_studio"
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize event for Socket.IO transmission."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "agent_name": self.agent_name,
            "data": self.data,
            "timestamp": self.timestamp,
            "tier": self.tier,
            "session_id": self.session_id,
        }


class EventBus:
    """
    Central event bus for the agent system.
    
    Collects events during an agent run and provides them to the
    Flask/Socket.IO layer for real-time streaming to the frontend.
    """

    def __init__(self):
        self._events: List[AgentEvent] = []
        self._listeners: List[callable] = []
        self._pending_input: Optional[AgentEvent] = None
        self._student_response: Optional[str] = None

    def emit(self, event: AgentEvent):
        """Emit an event to all listeners."""
        self._events.append(event)
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass  # Don't let a bad listener crash the agent

    def on_event(self, listener: callable):
        """Register a listener for all events."""
        self._listeners.append(listener)

    def pause_for_input(self, event: AgentEvent):
        """
        Set a pending input request. The agent loop should check this
        and wait for a student response before continuing.
        """
        self._pending_input = event
        self.emit(event)

    def submit_student_response(self, response: str):
        """Submit the student's response to a PauseForInput event."""
        self._student_response = response
        self._pending_input = None

    @property
    def has_pending_input(self) -> bool:
        return self._pending_input is not None

    @property
    def student_response(self) -> Optional[str]:
        resp = self._student_response
        self._student_response = None
        return resp

    def get_events(self, since: float = 0) -> List[Dict[str, Any]]:
        """Get all events since a given timestamp."""
        return [e.to_dict() for e in self._events if e.timestamp > since]

    def clear(self):
        """Clear all events (for new conversation turn)."""
        self._events.clear()
        self._pending_input = None
        self._student_response = None
