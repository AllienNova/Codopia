"""
Codopia Multi-Agent System
==========================

A hybrid CrewAI + agentic-framework-inspired multi-agent system for
age-appropriate coding education (ages 5-18).

Architecture:
    Orchestrator Agent → routes to specialist agents based on intent + tier
    Tutor Agent        → Socratic teaching, curriculum delivery, pedagogy
    Coding Agent       → Code execution, debugging, pair programming
    Hardware Agent     → Physical computing, simulation, device flashing

Key Design Principles:
    1. AI teaches, it doesn't do — Socratic method, scaffolded learning
    2. Voice-first for young kids, text-first for teens
    3. Progressive disclosure — complexity revealed gradually by tier
    4. Human-in-the-loop — PauseForInput pattern for pedagogy
    5. Event streaming — real-time agent activity visible to frontend
"""

__version__ = "0.1.0"
