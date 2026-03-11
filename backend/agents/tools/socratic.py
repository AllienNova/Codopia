"""
SocraticQuestionTool
====================

Generates age-appropriate Socratic questions to guide students
toward understanding rather than giving them answers directly.

This tool works in conjunction with PauseForInputTool:
    1. The Tutor Agent uses SocraticQuestionTool to generate a good question
    2. Then uses PauseForInputTool to actually ask the student

The tool provides question templates organized by:
    - Tier (age group)
    - Concept being taught
    - Bloom's taxonomy level (Remember → Create)
"""

from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


# Socratic question templates organized by Bloom's taxonomy level
QUESTION_TEMPLATES = {
    "remember": {
        "magic_workshop": [
            "Can you remember what the {concept} block does?",
            "What happened last time we used {concept}?",
            "Which color block is for {concept}?",
        ],
        "innovation_lab": [
            "What does the {concept} keyword do in Python?",
            "Can you remember the syntax for {concept}?",
            "What type of data does {concept} work with?",
        ],
        "professional_studio": [
            "What is the time complexity of {concept}?",
            "How does {concept} differ from {related_concept}?",
            "What are the key properties of {concept}?",
        ],
    },
    "understand": {
        "magic_workshop": [
            "Why do you think the wizard moved that way?",
            "What would happen if we took away the {concept} block?",
            "Can you explain what {concept} does in your own words?",
        ],
        "innovation_lab": [
            "Why does the code need {concept} here?",
            "What would happen if we changed {concept} to something else?",
            "Can you explain what this line does: `{code_snippet}`?",
        ],
        "professional_studio": [
            "Why is {concept} the right choice here instead of {related_concept}?",
            "What problem does {concept} solve in this context?",
            "How would you explain {concept} to a younger student?",
        ],
    },
    "apply": {
        "magic_workshop": [
            "Can you use the {concept} block to make the wizard dance?",
            "How would you use {concept} to solve this puzzle?",
            "What blocks would you need to make {goal}?",
        ],
        "innovation_lab": [
            "How would you use {concept} to build {goal}?",
            "Can you write code that uses {concept} to {goal}?",
            "What would you change in this code to make it {goal}?",
        ],
        "professional_studio": [
            "Implement a solution using {concept} that handles {goal}.",
            "How would you refactor this code to use {concept}?",
            "Write a function that applies {concept} to solve {goal}.",
        ],
    },
    "analyze": {
        "magic_workshop": [
            "Why did the wizard go the wrong way? What block caused it?",
            "Which part of your spell is making the star disappear?",
            "What's different between your spell and the example?",
        ],
        "innovation_lab": [
            "Why is this code producing the wrong output?",
            "What's causing the bug on line {line_number}?",
            "Which part of the code runs first, and why does that matter?",
        ],
        "professional_studio": [
            "What are the trade-offs between these two approaches?",
            "Where is the performance bottleneck in this code?",
            "What edge cases could break this implementation?",
        ],
    },
    "evaluate": {
        "magic_workshop": [
            "Is there a shorter way to make the wizard do the same thing?",
            "Which spell do you think works better? Why?",
            "Did your spell do what you expected?",
        ],
        "innovation_lab": [
            "Is this the most efficient way to solve this problem?",
            "What are the pros and cons of your approach?",
            "How would you rate your code on a scale of 1-5? Why?",
        ],
        "professional_studio": [
            "How would this code perform with 1 million users?",
            "What security concerns does this implementation have?",
            "How maintainable is this code? What would you improve?",
        ],
    },
    "create": {
        "magic_workshop": [
            "Can you invent a new spell that combines {concept} and {related_concept}?",
            "What would YOU like the wizard to do? Let's build it!",
            "Can you create a story using the blocks you learned?",
        ],
        "innovation_lab": [
            "Can you design your own version of this program?",
            "What feature would you add to make this app better?",
            "Build something new using {concept} — surprise me!",
        ],
        "professional_studio": [
            "Design a system architecture for {goal}.",
            "Create a library that implements {concept} with a clean API.",
            "Build a project that combines {concept} with {related_concept}.",
        ],
    },
}


class SocraticQuestionSchema(BaseModel):
    """Input schema for SocraticQuestionTool."""
    concept: str = Field(
        description="The coding concept being taught (e.g., 'loops', 'variables', 'functions')."
    )
    tier: str = Field(
        default="innovation_lab",
        description="Student tier: 'magic_workshop', 'innovation_lab', or 'professional_studio'."
    )
    bloom_level: str = Field(
        default="understand",
        description="Bloom's taxonomy level: 'remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'."
    )
    related_concept: Optional[str] = Field(
        default=None,
        description="A related concept for comparison questions."
    )
    code_snippet: Optional[str] = Field(
        default=None,
        description="A code snippet to reference in the question."
    )
    goal: Optional[str] = Field(
        default=None,
        description="The learning goal or project objective."
    )


class SocraticQuestionTool(BaseTool):
    """
    Generate age-appropriate Socratic questions to guide student learning.
    
    Uses Bloom's taxonomy to create questions at the right difficulty level,
    adapted for each tier's age group and vocabulary.
    """
    name: str = "generate_question"
    description: str = (
        "Generate a Socratic question to guide the student toward understanding "
        "a concept. Returns a well-crafted question appropriate for the student's "
        "age and learning level. Use this before ask_student to prepare a good question."
    )
    args_schema: Type[BaseModel] = SocraticQuestionSchema

    def _run(
        self,
        concept: str,
        tier: str = "innovation_lab",
        bloom_level: str = "understand",
        related_concept: Optional[str] = None,
        code_snippet: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> str:
        """Generate a Socratic question based on the parameters."""
        # Get templates for this tier and bloom level
        templates = QUESTION_TEMPLATES.get(bloom_level, {}).get(tier, [])
        if not templates:
            templates = QUESTION_TEMPLATES.get("understand", {}).get(tier, [
                "What do you think about {concept}?"
            ])

        # Pick the best template based on available context
        best_template = templates[0]
        for template in templates:
            if code_snippet and "{code_snippet}" in template:
                best_template = template
                break
            if goal and "{goal}" in template:
                best_template = template
                break
            if related_concept and "{related_concept}" in template:
                best_template = template
                break

        # Fill in the template
        question = best_template.format(
            concept=concept,
            related_concept=related_concept or "other approaches",
            code_snippet=code_snippet or "",
            goal=goal or "something cool",
            line_number="?",
        )

        # Add tier-appropriate framing
        if tier == "magic_workshop":
            framing = f"Professor Sparkle asks: {question}"
        elif tier == "innovation_lab":
            framing = f"Think about this: {question}"
        else:
            framing = f"Consider this: {question}"

        return framing
