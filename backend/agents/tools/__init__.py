"""
Codopia Agent Tool Library
==========================

Custom CrewAI tools inspired by agentic-framework's clean tool patterns.
Each tool is a self-contained class with configuration, authentication,
and error handling built in.

Tools:
    PauseForInputTool     — Ask the student a question (pedagogy-first)
    SocraticQuestionTool  — Generate Socratic questions based on context
    CodeSandboxTool       — Execute code safely in an isolated sandbox
    WokwiSimulatorTool    — Interact with Wokwi hardware simulator
    WebSerialTool         — Flash code to physical devices via Web Serial
    CurriculumTool        — Access age-appropriate curriculum and lessons
    SafetyFilterTool      — Filter content for child safety
"""

from .pause_for_input import PauseForInputTool
from .code_sandbox import CodeSandboxTool
from .socratic import SocraticQuestionTool
from .curriculum import CurriculumTool
from .safety_filter import SafetyFilterTool
from .wokwi_simulator import WokwiSimulatorTool

__all__ = [
    "PauseForInputTool",
    "CodeSandboxTool",
    "SocraticQuestionTool",
    "CurriculumTool",
    "SafetyFilterTool",
    "WokwiSimulatorTool",
]
