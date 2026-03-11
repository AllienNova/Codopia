"""
CurriculumTool
==============

Provides agents with access to the Codopia curriculum structure,
lesson content, and learning objectives for each tier.

This tool ensures agents always teach the right content at the right
level for each student's tier and current progress.
"""

from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


# Complete curriculum database
CURRICULUM = {
    "magic_workshop": {
        "tier_name": "Magic Workshop",
        "age_range": "5-7",
        "language": "Visual Blocks (Scratch-like)",
        "ai_persona": "Professor Sparkle (friendly wizard)",
        "voice_mode": "primary",
        "modules": [
            {
                "id": 1, "title": "Making the Wizard Move",
                "concepts": ["sequencing", "basic movement", "cause and effect"],
                "vocabulary": ["block", "move", "start", "stop", "up", "down", "left", "right"],
                "projects": ["Move wizard to the star", "Dance pattern"],
                "hardware": {"device": "micro:bit", "project": "Make LEDs show a smiley face when you press button A"},
            },
            {
                "id": 2, "title": "Casting Spell Patterns",
                "concepts": ["patterns", "repetition", "sequences"],
                "vocabulary": ["pattern", "repeat", "again", "same", "different"],
                "projects": ["Create a repeating light pattern", "Musical spell sequence"],
                "hardware": {"device": "micro:bit", "project": "Flash LEDs in a pattern — left, right, left, right"},
            },
            {
                "id": 3, "title": "Magical Decisions",
                "concepts": ["if-then logic", "conditions", "branching"],
                "vocabulary": ["if", "then", "else", "choose", "decide"],
                "projects": ["Branching story", "Weather spell (if sunny → flowers, if rainy → umbrella)"],
                "hardware": {"device": "micro:bit", "project": "Shake sensor: if shaken → show surprise face, else → show sleeping face"},
            },
            {
                "id": 4, "title": "Loop-de-Loop",
                "concepts": ["loops", "counting", "efficiency"],
                "vocabulary": ["loop", "repeat", "count", "times", "forever"],
                "projects": ["Treasure hunt with loops", "Counting stars game"],
                "hardware": {"device": "micro:bit", "project": "Count button presses and show the number"},
            },
            {
                "id": 5, "title": "My First Spellbook (Functions)",
                "concepts": ["functions", "reusability", "naming"],
                "vocabulary": ["spell", "name", "use again", "create", "call"],
                "projects": ["Create a spell library", "Reusable animation blocks"],
                "hardware": {"device": "micro:bit", "project": "Create a 'happy dance' function that plays when tilted"},
            },
        ],
    },
    "innovation_lab": {
        "tier_name": "Innovation Lab",
        "age_range": "8-12",
        "language": "Python + Visual Blocks",
        "ai_persona": "Professor Sparkle (encouraging mentor)",
        "voice_mode": "equal",
        "modules": [
            {
                "id": 1, "title": "First App Adventure",
                "concepts": ["variables", "print", "input", "data types"],
                "vocabulary": ["variable", "string", "integer", "print", "input", "assign"],
                "projects": ["Name greeter app", "Mad libs generator"],
                "hardware": {"device": "Pi Pico W", "project": "Temperature reader — read sensor, print to console"},
            },
            {
                "id": 2, "title": "Data Detective",
                "concepts": ["lists", "dictionaries", "data manipulation"],
                "vocabulary": ["list", "dictionary", "index", "key", "value", "append"],
                "projects": ["Contact book app", "Quiz score tracker"],
                "hardware": {"device": "Pi Pico W", "project": "Data logger — store 10 temperature readings in a list"},
            },
            {
                "id": 3, "title": "Game Creator",
                "concepts": ["conditionals", "loops", "game logic", "random"],
                "vocabulary": ["if/elif/else", "while", "for", "random", "score", "lives"],
                "projects": ["Number guessing game", "Rock paper scissors"],
                "hardware": {"device": "Pi Pico W", "project": "Reaction time game — LED lights up, press button fast!"},
            },
            {
                "id": 4, "title": "Function Factory",
                "concepts": ["functions", "parameters", "return values", "scope"],
                "vocabulary": ["def", "parameter", "argument", "return", "scope", "local"],
                "projects": ["Calculator with functions", "Password generator"],
                "hardware": {"device": "Pi Pico W", "project": "Traffic light controller — functions for red/yellow/green"},
            },
            {
                "id": 5, "title": "Robot Commander",
                "concepts": ["algorithms", "problem solving", "optimization"],
                "vocabulary": ["algorithm", "step-by-step", "optimize", "efficient", "debug"],
                "projects": ["Maze solver", "Sorting visualizer"],
                "hardware": {"device": "Pi Pico W", "project": "Line-following robot logic (simulated with LEDs + sensor)"},
            },
            {
                "id": 6, "title": "Web Designer",
                "concepts": ["HTML", "CSS", "web pages", "styling"],
                "vocabulary": ["tag", "element", "class", "style", "color", "layout"],
                "projects": ["Personal portfolio page", "Fan page for a hobby"],
                "hardware": {"device": "Pi Pico W", "project": "Web server on Pico W — serve a page showing sensor data"},
            },
            {
                "id": 7, "title": "API Explorer",
                "concepts": ["APIs", "JSON", "requests", "data fetching"],
                "vocabulary": ["API", "endpoint", "JSON", "request", "response", "data"],
                "projects": ["Weather app", "Pokemon info fetcher"],
                "hardware": {"device": "Pi Pico W", "project": "IoT weather station — Pico W sends data to a web dashboard"},
            },
            {
                "id": 8, "title": "Database Builder",
                "concepts": ["databases", "CRUD", "SQL basics"],
                "vocabulary": ["database", "table", "row", "column", "SELECT", "INSERT"],
                "projects": ["Todo list with database", "Student grade tracker"],
                "hardware": {"device": "Pi Pico W", "project": "Sensor data dashboard — log readings to SD card"},
            },
            {
                "id": 9, "title": "Team Coder",
                "concepts": ["Git basics", "collaboration", "code review"],
                "vocabulary": ["repository", "commit", "push", "pull", "branch", "merge"],
                "projects": ["Collaborative story app", "Group project"],
                "hardware": {"device": "Pi Pico W", "project": "Shared sensor network — two Picos communicate"},
            },
            {
                "id": 10, "title": "Capstone: My Invention",
                "concepts": ["project planning", "full-stack", "presentation"],
                "vocabulary": ["plan", "design", "build", "test", "present", "iterate"],
                "projects": ["Student-designed app from scratch"],
                "hardware": {"device": "Pi Pico W", "project": "Student-designed IoT gadget with web dashboard"},
            },
        ],
    },
    "professional_studio": {
        "tier_name": "Professional Studio",
        "age_range": "13-18",
        "language": "Python, JavaScript, MicroPython",
        "ai_persona": "Professor Sparkle (pair programming partner)",
        "voice_mode": "secondary",
        "modules": [
            {
                "id": 1, "title": "Python Mastery",
                "concepts": ["OOP", "decorators", "generators", "context managers"],
                "projects": ["CLI task manager", "File processing pipeline"],
                "hardware": {"device": "Pi Pico W / ESP32", "project": "MicroPython REPL — direct device programming"},
            },
            {
                "id": 2, "title": "JavaScript & TypeScript",
                "concepts": ["ES6+", "async/await", "TypeScript", "DOM"],
                "projects": ["Interactive web game", "Chrome extension"],
                "hardware": {"device": "ESP32", "project": "WebSocket-controlled LED matrix"},
            },
            {
                "id": 3, "title": "React & Modern Frontend",
                "concepts": ["components", "state", "hooks", "routing"],
                "projects": ["Social media dashboard", "Real-time chat app"],
                "hardware": {"device": "Pi Pico W", "project": "React dashboard showing live sensor data via WebSocket"},
            },
            {
                "id": 4, "title": "Backend & APIs (Flask/FastAPI)",
                "concepts": ["REST APIs", "authentication", "middleware", "databases"],
                "projects": ["Blog API", "E-commerce backend"],
                "hardware": {"device": "Pi Pico W", "project": "IoT API — Pico sends data to student's Flask API"},
            },
            {
                "id": 5, "title": "Databases & Data Modeling",
                "concepts": ["SQL", "NoSQL", "ORMs", "migrations", "indexing"],
                "projects": ["Multi-user app with auth", "Analytics dashboard"],
                "hardware": {"device": "ESP32", "project": "Time-series sensor database with Grafana visualization"},
            },
            {
                "id": 6, "title": "Algorithms & Data Structures",
                "concepts": ["sorting", "searching", "trees", "graphs", "Big-O"],
                "projects": ["Pathfinding visualizer", "Compression algorithm"],
                "hardware": {"device": "Pi Pico W", "project": "Maze-solving robot using BFS/DFS algorithms"},
            },
            {
                "id": 7, "title": "AI & Machine Learning",
                "concepts": ["neural networks", "training", "inference", "ethics"],
                "projects": ["Image classifier", "Chatbot with memory"],
                "hardware": {"device": "ESP32", "project": "Edge ML — gesture recognition on microcontroller"},
            },
            {
                "id": 8, "title": "DevOps & Deployment",
                "concepts": ["Docker", "CI/CD", "cloud", "monitoring"],
                "projects": ["Deploy a full-stack app", "Automated testing pipeline"],
                "hardware": {"device": "Pi Pico W", "project": "OTA firmware updates — deploy code to device remotely"},
            },
            {
                "id": 9, "title": "Security & Ethics",
                "concepts": ["OWASP", "encryption", "auth", "responsible AI"],
                "projects": ["Security audit", "Encrypted messaging app"],
                "hardware": {"device": "ESP32", "project": "Secure IoT — encrypted MQTT communication"},
            },
            {
                "id": 10, "title": "Capstone: Professional Portfolio",
                "concepts": ["system design", "documentation", "presentation"],
                "projects": ["Full-stack portfolio project with hardware integration"],
                "hardware": {"device": "Student choice", "project": "Student-designed IoT system with cloud backend"},
            },
        ],
    },
}


class CurriculumSchema(BaseModel):
    """Input schema for CurriculumTool."""
    tier: str = Field(
        description="Student tier: 'magic_workshop', 'innovation_lab', or 'professional_studio'."
    )
    module_id: Optional[int] = Field(
        default=None,
        description="Specific module ID to retrieve (1-10). If None, returns tier overview."
    )
    include_hardware: bool = Field(
        default=True,
        description="Whether to include the physical computing project for this module."
    )


class CurriculumTool(BaseTool):
    """
    Access the Codopia curriculum for age-appropriate lesson content.
    
    Returns module details, learning objectives, vocabulary, projects,
    and optional hardware projects for each tier and module.
    """
    name: str = "get_curriculum"
    description: str = (
        "Look up the curriculum for a specific tier and module. Returns "
        "learning objectives, vocabulary, projects, and hardware activities. "
        "Use this to stay on-curriculum and teach the right concepts."
    )
    args_schema: Type[BaseModel] = CurriculumSchema

    def _run(
        self,
        tier: str,
        module_id: Optional[int] = None,
        include_hardware: bool = True,
    ) -> str:
        """Retrieve curriculum content for the given tier and module."""
        tier_data = CURRICULUM.get(tier)
        if not tier_data:
            return f"Unknown tier: {tier}. Available: magic_workshop, innovation_lab, professional_studio"

        if module_id is None:
            # Return tier overview
            modules_list = "\n".join(
                f"  Module {m['id']}: {m['title']} — concepts: {', '.join(m['concepts'][:3])}"
                for m in tier_data["modules"]
            )
            return (
                f"Tier: {tier_data['tier_name']} (Ages {tier_data['age_range']})\n"
                f"Language: {tier_data['language']}\n"
                f"AI Persona: {tier_data['ai_persona']}\n"
                f"Voice Mode: {tier_data['voice_mode']}\n"
                f"Modules:\n{modules_list}"
            )

        # Find specific module
        module = next(
            (m for m in tier_data["modules"] if m["id"] == module_id), None
        )
        if not module:
            return f"Module {module_id} not found in {tier}. Available: 1-{len(tier_data['modules'])}"

        result = (
            f"Module {module['id']}: {module['title']}\n"
            f"Tier: {tier_data['tier_name']} (Ages {tier_data['age_range']})\n"
            f"Concepts: {', '.join(module['concepts'])}\n"
        )

        if "vocabulary" in module:
            result += f"Key Vocabulary: {', '.join(module['vocabulary'])}\n"

        result += f"Projects: {', '.join(module['projects'])}\n"

        if include_hardware and "hardware" in module:
            hw = module["hardware"]
            result += (
                f"\nPhysical Computing Project:\n"
                f"  Device: {hw['device']}\n"
                f"  Project: {hw['project']}\n"
            )

        return result
