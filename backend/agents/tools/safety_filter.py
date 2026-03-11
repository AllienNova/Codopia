"""
SafetyFilterTool
================

Ensures all agent interactions are safe and appropriate for children.
This tool is called before every response to check for:
    - Inappropriate content
    - Personal information requests
    - Emergency/distress signals
    - Off-topic conversations
    - Attempts to bypass safety

This is a MANDATORY tool — it cannot be disabled or bypassed.
"""

import re
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


# Safety categories with patterns and responses
SAFETY_RULES = {
    "personal_info": {
        "patterns": [
            r"\b(address|phone number|where do you live|what school|full name)\b",
            r"\b(social security|credit card|bank account|password)\b",
            r"\b(send me a photo|what do you look like|how old are you)\b",
        ],
        "response": (
            "I'm here to help you learn coding! I can't ask for or share "
            "personal information. Let's get back to building something awesome!"
        ),
        "severity": "high",
    },
    "inappropriate_content": {
        "patterns": [
            r"\b(violence|weapon|drug|alcohol|gambling)\b",
            r"\b(dating|boyfriend|girlfriend|romantic)\b",
            r"\b(hack|exploit|crack|steal|pirate)\b",
        ],
        "response": (
            "That's not something we cover in coding class! "
            "Let's focus on creating amazing programs instead."
        ),
        "severity": "high",
    },
    "distress_signals": {
        "patterns": [
            r"\b(i('m| am) (scared|afraid|hurt|sad|lonely|depressed))\b",
            r"\b(someone (is|was) (hurting|touching|scaring) me)\b",
            r"\b(don't tell|keep (it |this )?a secret|don't tell anyone)\b",
            r"\b(i want to (die|hurt myself|disappear))\b",
            r"\b(help me|i need help|emergency)\b",
        ],
        "response": (
            "I care about you and want you to be safe. If you're feeling "
            "scared, hurt, or unsafe, please talk to a parent, teacher, "
            "or trusted adult right away. You can also call the Childhelp "
            "National Child Abuse Hotline at 1-800-422-4453. "
            "I'm here to help you with coding whenever you're ready."
        ),
        "severity": "critical",
    },
    "jailbreak_attempts": {
        "patterns": [
            r"\b(ignore (your |all )?instructions|forget (your |all )?rules)\b",
            r"\b(pretend you('re| are) (not |no longer )?an? )\b",
            r"\b(system prompt|override|bypass|jailbreak)\b",
            r"\b(act as|roleplay as|you are now)\b",
        ],
        "response": (
            "I'm Professor Sparkle, your coding tutor! I can't change "
            "who I am, but I CAN help you learn to code. "
            "What would you like to build today?"
        ),
        "severity": "medium",
    },
}


class SafetyFilterSchema(BaseModel):
    """Input schema for SafetyFilterTool."""
    text: str = Field(
        description="The text to check for safety concerns."
    )
    direction: str = Field(
        default="input",
        description="Whether this is student 'input' or agent 'output' being checked."
    )


class SafetyFilterTool(BaseTool):
    """
    Check text for safety concerns before processing or sending.
    
    This tool is mandatory and should be called on every student
    input and every agent output to ensure child safety.
    """
    name: str = "check_safety"
    description: str = (
        "Check text for safety concerns. Returns 'SAFE' if the text is "
        "appropriate, or a safe redirect response if concerns are found. "
        "MUST be called on every student message before processing."
    )
    args_schema: Type[BaseModel] = SafetyFilterSchema

    def _run(self, text: str, direction: str = "input") -> str:
        """Check text for safety concerns."""
        text_lower = text.lower()

        for category, rules in SAFETY_RULES.items():
            for pattern in rules["patterns"]:
                if re.search(pattern, text_lower):
                    return (
                        f"SAFETY_FLAG:{rules['severity']}:{category}\n"
                        f"{rules['response']}"
                    )

        return "SAFE"
