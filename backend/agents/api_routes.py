"""
Codopia Agent API Routes
========================

Flask Blueprint providing REST API and Socket.IO endpoints for the
multi-agent system. This is the integration layer between the
frontend and the CrewAI agent system.

REST Endpoints:
    POST /api/agents/chat          — Send a message and get a response
    POST /api/agents/respond       — Submit student response to PauseForInput
    GET  /api/agents/health        — System health check
    GET  /api/agents/curriculum/<tier>              — Get tier curriculum overview
    GET  /api/agents/curriculum/<tier>/<module_id>  — Get module details
    GET  /api/agents/hardware/<tier>                — List hardware projects
    GET  /api/agents/hardware/<tier>/<template>     — Get hardware project details
    GET  /api/agents/sessions/<session_id>/history  — Get conversation history
    DELETE /api/agents/sessions/<session_id>        — Clear session

Socket.IO Events (emitted to frontend):
    agent_thinking      — Agent is processing
    tool_call           — Agent is using a tool
    tool_result         — Tool returned a result
    pause_for_input     — Agent is asking the student a question
    chat_output         — Final response text
    code_output         — Code execution result
    simulation_update   — Wokwi simulator state change
    turn_end            — Agent finished processing
    error               — Something went wrong
"""

import uuid
import time
from flask import Blueprint, request, jsonify
from flask_socketio import emit

from agents.events import EventBus, AgentEvent, EventType


# Blueprint definition
agent_bp = Blueprint("agents", __name__, url_prefix="/api/agents")

# Global agent system instance (initialized in init_agent_system)
_agent_system = None
_event_bus = None


def init_agent_system(socketio=None):
    """
    Initialize the agent system and connect it to Socket.IO.
    
    Called from main.py during app startup.
    """
    global _agent_system, _event_bus

    _event_bus = EventBus()

    # Connect event bus to Socket.IO for real-time streaming
    if socketio:
        def socket_listener(event: AgentEvent):
            """Forward agent events to the frontend via Socket.IO."""
            try:
                room = event.session_id or "broadcast"
                socketio.emit(
                    event.event_type.value,
                    event.to_dict(),
                    room=room,
                    namespace="/agents",
                )
            except Exception as e:
                print(f"[Agent EventBus] Socket.IO emit error: {e}")

        _event_bus.on_event(socket_listener)

    # Import and create the agent system
    from agents.crew import CodopiaAgentSystem
    _agent_system = CodopiaAgentSystem(event_bus=_event_bus)

    print("[Codopia Agents] Multi-agent system initialized")
    print(f"[Codopia Agents] Agents: orchestrator, tutor, coding_agent, hardware_agent")
    print(f"[Codopia Agents] Tools: 6 (pause_for_input, code_sandbox, socratic, curriculum, safety_filter, wokwi)")
    print(f"[Codopia Agents] Socket.IO: {'connected' if socketio else 'not connected'}")

    return _agent_system


def get_agent_system():
    """Get the global agent system instance."""
    if _agent_system is None:
        raise RuntimeError(
            "Agent system not initialized. Call init_agent_system() first."
        )
    return _agent_system


# ─────────────────────────────────────────────────────────────────────
# REST API Endpoints
# ─────────────────────────────────────────────────────────────────────

@agent_bp.route("/chat", methods=["POST"])
def chat():
    """
    Send a message to the agent system and get a response.
    
    Request body:
        {
            "message": "How do I make an LED blink?",
            "session_id": "optional-session-id",
            "tier": "innovation_lab",
            "student_name": "Alex"
        }
    
    Response:
        {
            "response": "Great question! Let's learn about LEDs...",
            "intent": "HARDWARE",
            "agent": "hardware",
            "events": [...],
            "execution_time": 2.3,
            "session_id": "abc123"
        }
    """
    try:
        system = get_agent_system()
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        message = data["message"]
        session_id = data.get("session_id", str(uuid.uuid4())[:12])
        tier = data.get("tier", "innovation_lab")
        student_name = data.get("student_name", "Student")

        # Validate tier
        valid_tiers = ["magic_workshop", "innovation_lab", "professional_studio"]
        if tier not in valid_tiers:
            return jsonify({
                "error": f"Invalid tier: {tier}. Must be one of: {valid_tiers}"
            }), 400

        # Process through the agent system
        result = system.process_message_sync(
            message=message,
            session_id=session_id,
            tier=tier,
            student_name=student_name,
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "response": (
                "Oops! Professor Sparkle had a hiccup. "
                "Could you try saying that again?"
            ),
        }), 500


@agent_bp.route("/respond", methods=["POST"])
def respond_to_pause():
    """
    Submit a student's response to a PauseForInput event.
    
    Request body:
        {
            "session_id": "abc123",
            "response": "I think the answer is pin 25"
        }
    """
    try:
        data = request.get_json()
        if not data or "response" not in data:
            return jsonify({"error": "Missing 'response' in request body"}), 400

        if _event_bus:
            _event_bus.submit_student_response(data["response"])
            return jsonify({"status": "response_submitted"}), 200
        else:
            return jsonify({"error": "Event bus not initialized"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/health", methods=["GET"])
def health():
    """System health check endpoint."""
    try:
        system = get_agent_system()
        return jsonify(system.get_health()), 200
    except RuntimeError:
        return jsonify({
            "status": "not_initialized",
            "message": "Agent system has not been initialized yet.",
        }), 503


@agent_bp.route("/curriculum/<tier>", methods=["GET"])
def curriculum_overview(tier):
    """Get curriculum overview for a tier."""
    try:
        system = get_agent_system()
        overview = system.get_curriculum_overview(tier)
        return jsonify({"tier": tier, "overview": overview}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/curriculum/<tier>/<int:module_id>", methods=["GET"])
def module_details(tier, module_id):
    """Get details for a specific module."""
    try:
        system = get_agent_system()
        details = system.get_module_details(tier, module_id)
        return jsonify({"tier": tier, "module_id": module_id, "details": details}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/hardware/<tier>", methods=["GET"])
def hardware_projects(tier):
    """List available hardware projects for a tier."""
    try:
        system = get_agent_system()
        projects = system.list_hardware_projects(tier)
        return jsonify({"tier": tier, "projects": projects}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/hardware/<tier>/<template_name>", methods=["GET"])
def hardware_project_details(tier, template_name):
    """Get a specific hardware project template."""
    try:
        system = get_agent_system()
        details = system.get_hardware_project(template_name, tier)
        return jsonify({
            "tier": tier,
            "template": template_name,
            "details": details,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/sessions/<session_id>/history", methods=["GET"])
def session_history(session_id):
    """Get conversation history for a session."""
    try:
        system = get_agent_system()
        history = system._conversation_history.get(session_id, [])
        return jsonify({
            "session_id": session_id,
            "history": history,
            "turn_count": len(history),
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/sessions/<session_id>", methods=["DELETE"])
def clear_session(session_id):
    """Clear a session's conversation history."""
    try:
        system = get_agent_system()
        if session_id in system._conversation_history:
            del system._conversation_history[session_id]
        if session_id in system._session_tiers:
            del system._session_tiers[session_id]
        return jsonify({"status": "cleared", "session_id": session_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────────────
# Socket.IO Event Handlers (registered in main.py)
# ─────────────────────────────────────────────────────────────────────

def register_socketio_handlers(socketio):
    """
    Register Socket.IO event handlers for the /agents namespace.
    
    Called from main.py during app startup.
    """

    @socketio.on("connect", namespace="/agents")
    def handle_connect():
        print(f"[Agent Socket.IO] Client connected")
        emit("connected", {"status": "ok", "message": "Connected to Codopia Agent System"})

    @socketio.on("disconnect", namespace="/agents")
    def handle_disconnect():
        print(f"[Agent Socket.IO] Client disconnected")

    @socketio.on("join_session", namespace="/agents")
    def handle_join_session(data):
        """Join a session room for targeted event delivery."""
        session_id = data.get("session_id")
        if session_id:
            from flask_socketio import join_room
            join_room(session_id)
            emit("session_joined", {"session_id": session_id})

    @socketio.on("student_message", namespace="/agents")
    def handle_student_message(data):
        """
        Handle a student message via Socket.IO (alternative to REST API).
        Provides real-time event streaming during processing.
        """
        try:
            system = get_agent_system()
            message = data.get("message", "")
            session_id = data.get("session_id", str(uuid.uuid4())[:12])
            tier = data.get("tier", "innovation_lab")
            student_name = data.get("student_name", "Student")

            result = system.process_message_sync(
                message=message,
                session_id=session_id,
                tier=tier,
                student_name=student_name,
            )

            emit("agent_response", result)

        except Exception as e:
            emit("error", {
                "message": str(e),
                "friendly": "Professor Sparkle had a hiccup! Try again.",
            })

    @socketio.on("student_response", namespace="/agents")
    def handle_student_response(data):
        """Handle a student's response to a PauseForInput event."""
        response = data.get("response", "")
        if _event_bus and response:
            _event_bus.submit_student_response(response)
            emit("response_received", {"status": "ok"})

    print("[Codopia Agents] Socket.IO handlers registered on /agents namespace")
