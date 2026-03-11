"""
PauseForInputTool
=================

The most important tool in the Codopia agent system.

Inspired by agentic-framework's PauseForInputResult pattern, this tool
allows an agent to PAUSE execution and ask the student a question.
The agent waits for the student's response before continuing.

This is the mechanism that turns the AI from a "code generator" into a
"teacher." Instead of giving the answer, the agent asks:
    "What do you think will happen if we change this variable?"

Usage by agents:
    The Tutor Agent uses this to ask Socratic questions.
    The Coding Agent uses this to ask "What should go in the blank?"
    The Hardware Agent uses this to ask "Which pin should the sensor connect to?"

Integration:
    When this tool is called, the EventBus emits a PAUSE_FOR_INPUT event.
    The Flask/Socket.IO layer sends this to the frontend.
    The frontend shows the question and collects the student's answer.
    The answer is submitted back via the EventBus.
    The agent receives the answer and continues execution.
"""

import json
import time
from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from agents.events import EventBus, AgentEvent, EventType


class PauseForInputSchema(BaseModel):
    """Input schema for PauseForInputTool."""
    question: str = Field(
        description="The question to ask the student. Must be age-appropriate and encouraging."
    )
    hint: Optional[str] = Field(
        default=None,
        description="An optional hint to help the student if they get stuck."
    )
    question_type: str = Field(
        default="open",
        description="Type of question: 'open' for free text, 'multiple_choice' for options, 'fill_blank' for code completion."
    )
    choices: Optional[str] = Field(
        default=None,
        description="For multiple_choice questions, a JSON array of choices. e.g. '[\"A) print\", \"B) input\", \"C) return\"]'"
    )
    code_context: Optional[str] = Field(
        default=None,
        description="Code snippet with a blank (___) that the student needs to fill in."
    )
    encouragement: str = Field(
        default="Take your time, you've got this!",
        description="An encouraging message to show alongside the question."
    )


class PauseForInputTool(BaseTool):
    """
    Pause agent execution and ask the student a question.
    
    This tool is the core of Codopia's pedagogy-first approach.
    Instead of giving answers, the AI asks questions and waits
    for the student to think and respond.
    """
    name: str = "ask_student"
    description: str = (
        "Pause and ask the student a question. Use this instead of giving "
        "direct answers. Ask Socratic questions, fill-in-the-blank code "
        "challenges, or multiple choice questions. The student's answer "
        "will be returned so you can provide feedback."
    )
    args_schema: Type[BaseModel] = PauseForInputSchema
    event_bus: Optional[EventBus] = None
    live_mode: bool = False  # Set to True when a real frontend is connected

    class Config:
        arbitrary_types_allowed = True

    def _run(
        self,
        question: str,
        hint: Optional[str] = None,
        question_type: str = "open",
        choices: Optional[str] = None,
        code_context: Optional[str] = None,
        encouragement: str = "Take your time, you've got this!",
    ) -> str:
        """
        Emit a PAUSE_FOR_INPUT event and wait for the student's response.
        
        In live mode (frontend connected), this blocks until the student responds.
        In demo/test mode, it emits the event but returns a simulated response
        so the agent can continue demonstrating its behavior.
        """
        # Parse choices if provided
        parsed_choices = None
        if choices:
            try:
                parsed_choices = json.loads(choices)
            except json.JSONDecodeError:
                parsed_choices = [c.strip() for c in choices.split(",")]

        # Build the event data
        event_data = {
            "question": question,
            "hint": hint,
            "question_type": question_type,
            "choices": parsed_choices,
            "code_context": code_context,
            "encouragement": encouragement,
        }

        # Emit the pause event (always, so the frontend can display it)
        if self.event_bus:
            event = AgentEvent(
                event_type=EventType.PAUSE_FOR_INPUT,
                agent_name="tutor",
                data=event_data,
            )
            self.event_bus.emit(event)  # Always emit for logging

        # In live mode with a connected frontend, block and wait
        if self.live_mode and self.event_bus:
            self.event_bus.pause_for_input(event)

            # Wait for student response (with timeout)
            timeout = 300  # 5 minutes max wait
            start = time.time()
            while self.event_bus.has_pending_input:
                if time.time() - start > timeout:
                    return "The student didn't respond in time. Let's move on and come back to this later."
                time.sleep(0.5)

            # Get the student's response
            response = self.event_bus.student_response
            if response:
                self.event_bus.emit(AgentEvent(
                    event_type=EventType.STUDENT_RESPONSE,
                    agent_name="student",
                    data={"response": response, "question": question},
                ))
                return f"The student answered: {response}"
            else:
                return "The student skipped this question. Let's try a different approach."
        else:
            # Demo/test mode — return simulated response so agent can continue
            simulated = "I think it might be something that repeats?"
            if question_type == "multiple_choice" and parsed_choices:
                simulated = parsed_choices[0] if parsed_choices else "A"
            elif question_type == "fill_blank":
                simulated = "print"
            return (
                f"[Question posed to student: '{question}'] "
                f"Student responded: '{simulated}'"
            )
