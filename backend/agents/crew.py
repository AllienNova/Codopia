"""
Codopia Multi-Agent Crew
========================

Defines the 4 CrewAI agents and the crew orchestration logic.

Architecture:
    1. Student message arrives via Flask/Socket.IO
    2. Orchestrator Agent classifies intent → TUTOR | CODING | HARDWARE | SAFETY
    3. The appropriate specialist agent handles the request
    4. Events stream back to the frontend in real-time
    5. PauseForInput events block until the student responds

Agent Hierarchy:
    Orchestrator (manager) → delegates to:
        ├── Tutor Agent (pedagogy, Socratic questioning)
        ├── Coding Agent (code execution, debugging)
        └── Hardware Agent (simulation, wiring, flashing)

LLM Configuration:
    Orchestrator: gemini-2.5-flash (fast, cheap routing)
    Tutor Agent: gpt-4.1-mini (strong reasoning, good with kids)
    Coding Agent: gpt-4.1-mini (code understanding)
    Hardware Agent: gpt-4.1-mini (technical accuracy)
    
    All via LiteLLM for unified API access.
"""

import os
import re
import json
import time
from typing import Optional, Dict, Any, List

from crewai import Agent, Task, Crew, Process

from backend.agents.events import EventBus, AgentEvent, EventType
from backend.agents.tools.pause_for_input import PauseForInputTool
from backend.agents.tools.code_sandbox import CodeSandboxTool
from backend.agents.tools.socratic import SocraticQuestionTool
from backend.agents.tools.curriculum import CurriculumTool
from backend.agents.tools.safety_filter import SafetyFilterTool
from backend.agents.tools.wokwi_simulator import WokwiSimulatorTool
from backend.agents.prompts import (
    ORCHESTRATOR_BACKSTORY, ORCHESTRATOR_GOAL,
    TUTOR_BACKSTORY, TUTOR_GOAL,
    CODING_AGENT_BACKSTORY, CODING_AGENT_GOAL,
    HARDWARE_AGENT_BACKSTORY, HARDWARE_AGENT_GOAL,
)


# ─────────────────────────────────────────────────────────────────────
# LLM Configuration
# ─────────────────────────────────────────────────────────────────────

# Default LLM for all agents — uses OpenAI-compatible endpoint
DEFAULT_LLM = "openai/gpt-4.1-mini"
FAST_LLM = "openai/gpt-4.1-nano"  # For orchestrator routing (fast + cheap)


class CodopiaAgentSystem:
    """
    The main multi-agent system for Codopia.
    
    Creates and manages the CrewAI agents, handles message routing,
    and provides the interface between Flask and the agent system.
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        """Initialize the agent system with tools and agents."""
        self.event_bus = event_bus or EventBus()
        self._conversation_history: Dict[str, List[Dict]] = {}
        self._session_tiers: Dict[str, str] = {}

        # Initialize tools with shared event bus
        self.pause_tool = PauseForInputTool(event_bus=self.event_bus)
        self.code_sandbox = CodeSandboxTool(event_bus=self.event_bus)
        self.socratic_tool = SocraticQuestionTool()
        self.curriculum_tool = CurriculumTool()
        self.safety_filter = SafetyFilterTool()
        self.wokwi_tool = WokwiSimulatorTool(event_bus=self.event_bus)

        # Build agents
        self._build_agents()

    def _build_agents(self):
        """Create all CrewAI agents with their tools and prompts."""

        # ── Orchestrator Agent ──────────────────────────────────────
        self.orchestrator = Agent(
            role="Intent Classifier and Router",
            backstory=ORCHESTRATOR_BACKSTORY,
            goal=ORCHESTRATOR_GOAL,
            llm=FAST_LLM,
            verbose=False,
            allow_delegation=False,
            tools=[self.safety_filter],
        )

        # ── Tutor Agent (default tier, updated per request) ────────
        self.tutor = Agent(
            role="Socratic Coding Tutor",
            backstory=TUTOR_BACKSTORY["innovation_lab"],
            goal=TUTOR_GOAL["innovation_lab"],
            llm=DEFAULT_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            tools=[
                self.pause_tool,
                self.socratic_tool,
                self.curriculum_tool,
                self.safety_filter,
            ],
        )

        # ── Coding Agent ───────────────────────────────────────────
        self.coding_agent = Agent(
            role="Code Execution and Debugging Specialist",
            backstory=CODING_AGENT_BACKSTORY,
            goal=CODING_AGENT_GOAL,
            llm=DEFAULT_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            tools=[
                self.code_sandbox,
                self.pause_tool,
                self.safety_filter,
            ],
        )

        # ── Hardware Agent ─────────────────────────────────────────
        self.hardware_agent = Agent(
            role="Physical Computing and Hardware Specialist",
            backstory=HARDWARE_AGENT_BACKSTORY,
            goal=HARDWARE_AGENT_GOAL,
            llm=DEFAULT_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            tools=[
                self.wokwi_tool,
                self.code_sandbox,
                self.pause_tool,
                self.curriculum_tool,
                self.safety_filter,
            ],
        )

    def _update_tutor_for_tier(self, tier: str):
        """Update the Tutor Agent's backstory and goal for the current tier."""
        if tier in TUTOR_BACKSTORY:
            self.tutor.backstory = TUTOR_BACKSTORY[tier]
            self.tutor.goal = TUTOR_GOAL[tier]

    def _classify_intent(self, message: str) -> str:
        """
        Classify the student's message intent using the Orchestrator.
        
        Returns: "TUTOR", "CODING", "HARDWARE", or "SAFETY"
        """
        # First, run safety check
        safety_result = self.safety_filter._run(text=message, direction="input")
        if safety_result != "SAFE":
            return "SAFETY"

        # Use keyword-based fast classification (saves an LLM call)
        message_lower = message.lower()

        # Hardware keywords
        hardware_keywords = [
            "led", "sensor", "motor", "servo", "pico", "micro:bit", "esp32",
            "wiring", "circuit", "robot", "hardware", "flash", "simulate",
            "pin", "gpio", "breadboard", "resistor", "button press",
            "temperature sensor", "traffic light", "reaction game",
            "physical", "device", "microcontroller", "micropython",
        ]
        if any(kw in message_lower for kw in hardware_keywords):
            return "HARDWARE"

        # Coding keywords
        coding_keywords = [
            "run this", "debug", "fix my code", "error", "doesn't work",
            "write code", "code review", "execute", "compile", "syntax",
            "traceback", "exception", "bug", "output is wrong",
            "run the code", "test this", "what does this code",
        ]
        if any(kw in message_lower for kw in coding_keywords):
            return "CODING"

        # Default to TUTOR for everything else (learning, questions, etc.)
        return "TUTOR"

    def _get_conversation_context(self, session_id: str, max_turns: int = 10) -> str:
        """Get recent conversation history as context for the agent."""
        history = self._conversation_history.get(session_id, [])
        if not history:
            return "This is the start of the conversation."

        recent = history[-max_turns:]
        context_lines = []
        for turn in recent:
            role = turn.get("role", "unknown")
            content = turn.get("content", "")[:300]
            context_lines.append(f"{role}: {content}")

        return "\n".join(context_lines)

    def _add_to_history(self, session_id: str, role: str, content: str):
        """Add a message to the conversation history."""
        if session_id not in self._conversation_history:
            self._conversation_history[session_id] = []
        self._conversation_history[session_id].append({
            "role": role,
            "content": content,
            "timestamp": time.time(),
        })
        # Keep history manageable
        if len(self._conversation_history[session_id]) > 50:
            self._conversation_history[session_id] = \
                self._conversation_history[session_id][-30:]

    def process_message(
        self,
        message: str,
        session_id: str,
        tier: str = "innovation_lab",
        student_name: str = "Student",
    ) -> Dict[str, Any]:
        """
        Process a student message through the multi-agent system.
        
        This is the main entry point called by the Flask API.
        Synchronous because CrewAI's kickoff() is synchronous.
        
        Args:
            message: The student's text message
            session_id: Unique session identifier
            tier: Student's tier (magic_workshop, innovation_lab, professional_studio)
            student_name: Student's display name
            
        Returns:
            Dict with response text, events, and metadata
        """
        start_time = time.time()

        # Store tier for this session
        self._session_tiers[session_id] = tier

        # Update tutor personality for this tier
        self._update_tutor_for_tier(tier)

        # Add student message to history
        self._add_to_history(session_id, "student", message)

        # Emit thinking event
        self.event_bus.emit(AgentEvent(
            event_type=EventType.AGENT_THINKING,
            agent_name="orchestrator",
            data={"status": "Analyzing your message..."},
            tier=tier,
            session_id=session_id,
        ))

        # Step 1: Classify intent
        intent = self._classify_intent(message)

        # Step 2: Handle safety concerns immediately
        if intent == "SAFETY":
            safety_result = self.safety_filter._run(text=message, direction="input")
            # Extract the safe response (after the SAFETY_FLAG line)
            lines = safety_result.split("\n")
            safe_response = "\n".join(lines[1:]) if len(lines) > 1 else safety_result
            self._add_to_history(session_id, "professor_sparkle", safe_response)
            return {
                "response": safe_response,
                "intent": "SAFETY",
                "agent": "safety_filter",
                "events": self.event_bus.get_events(),
                "execution_time": time.time() - start_time,
            }

        # Step 3: Build context
        conversation_context = self._get_conversation_context(session_id)

        # Step 4: Route to the appropriate agent
        agent_map = {
            "TUTOR": self.tutor,
            "CODING": self.coding_agent,
            "HARDWARE": self.hardware_agent,
        }
        selected_agent = agent_map.get(intent, self.tutor)

        # Emit routing event
        self.event_bus.emit(AgentEvent(
            event_type=EventType.AGENT_THINKING,
            agent_name=intent.lower(),
            data={"status": f"Routing to {intent} agent..."},
            tier=tier,
            session_id=session_id,
        ))

        # Step 5: Create and execute the task
        task_description = (
            f"Student ({student_name}, {tier} tier) says: \"{message}\"\n\n"
            f"Conversation history:\n{conversation_context}\n\n"
            f"Instructions:\n"
            f"- Respond as Professor Sparkle appropriate for the {tier} tier\n"
            f"- Use your tools to teach, not to give answers\n"
            f"- If the student asks a question, use ask_student to turn it into a learning moment\n"
            f"- Keep your response appropriate for the age group\n"
            f"- Be encouraging and celebrate effort\n"
        )

        task = Task(
            description=task_description,
            expected_output=(
                "A helpful, age-appropriate response that teaches the student "
                "through Socratic questioning and guided discovery. Include "
                "encouragement and connect to the learning objective."
            ),
            agent=selected_agent,
        )

        crew = Crew(
            agents=[selected_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        try:
            result = crew.kickoff()
            response_text = str(result)
        except Exception as e:
            response_text = (
                "Hmm, Professor Sparkle got a bit confused there! "
                "Could you try asking that in a different way? "
                f"(Technical note: {str(e)[:100]})"
            )

        # Emit output event
        self.event_bus.emit(AgentEvent(
            event_type=EventType.CHAT_OUTPUT,
            agent_name=intent.lower(),
            data={"response": response_text[:200]},
            tier=tier,
            session_id=session_id,
        ))

        # Add response to history
        self._add_to_history(session_id, "professor_sparkle", response_text)

        # Emit turn end
        execution_time = time.time() - start_time
        self.event_bus.emit(AgentEvent(
            event_type=EventType.TURN_END,
            agent_name="orchestrator",
            data={
                "intent": intent,
                "execution_time": round(execution_time, 2),
            },
            tier=tier,
            session_id=session_id,
        ))

        return {
            "response": response_text,
            "intent": intent,
            "agent": intent.lower(),
            "events": self.event_bus.get_events(),
            "execution_time": round(execution_time, 2),
            "session_id": session_id,
            "tier": tier,
        }

    def process_message_sync(
        self,
        message: str,
        session_id: str,
        tier: str = "innovation_lab",
        student_name: str = "Student",
    ) -> Dict[str, Any]:
        """
        Alias for process_message (kept for backward compatibility).
        process_message is now synchronous since CrewAI kickoff() is sync.
        """
        return self.process_message(message, session_id, tier, student_name)

    def get_health(self) -> Dict[str, Any]:
        """Return system health status."""
        return {
            "status": "healthy",
            "agents": {
                "orchestrator": {"status": "ready", "llm": FAST_LLM},
                "tutor": {"status": "ready", "llm": DEFAULT_LLM},
                "coding_agent": {"status": "ready", "llm": DEFAULT_LLM},
                "hardware_agent": {"status": "ready", "llm": DEFAULT_LLM},
            },
            "tools": {
                "pause_for_input": "ready",
                "code_sandbox": "ready",
                "socratic_question": "ready",
                "curriculum": "ready",
                "safety_filter": "ready",
                "wokwi_simulator": "ready",
            },
            "active_sessions": len(self._conversation_history),
            "event_bus": "connected" if self.event_bus else "disconnected",
        }

    def get_curriculum_overview(self, tier: str) -> str:
        """Get curriculum overview for a tier."""
        return self.curriculum_tool._run(tier=tier)

    def get_module_details(self, tier: str, module_id: int) -> str:
        """Get details for a specific module."""
        return self.curriculum_tool._run(tier=tier, module_id=module_id)

    def list_hardware_projects(self, tier: str) -> str:
        """List available hardware projects for a tier."""
        return self.wokwi_tool._run(action="list_templates", tier=tier)

    def get_hardware_project(self, template_name: str, tier: str) -> str:
        """Get a specific hardware project template."""
        return self.wokwi_tool._run(
            action="get_template", template_name=template_name, tier=tier
        )
