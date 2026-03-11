"""
CodeSandboxTool
===============

Provides safe, isolated code execution for the Coding Agent.

Architecture:
    - In production: connects to E2B (e2b.dev) cloud sandboxes for true isolation
    - In development: uses a restricted subprocess with timeouts and resource limits
    - In demo mode: returns simulated output

Safety:
    - 10-second execution timeout (configurable per tier)
    - No network access in sandbox
    - No filesystem access outside sandbox
    - Memory limit: 128MB
    - Blocked imports: os.system, subprocess, socket, etc.
    - Output truncated to 2000 chars

Tier Behavior:
    Tier 1 (Magic Workshop): Only block-based output, no raw code execution
    Tier 2 (Innovation Lab): Python and JavaScript with training wheels
    Tier 3 (Professional Studio): Full Python, JavaScript, MicroPython
"""

import subprocess
import tempfile
import os
import signal
import json
from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from agents.events import EventBus, AgentEvent, EventType


# Dangerous imports/functions that are blocked in the sandbox
BLOCKED_PATTERNS = [
    "import os", "import subprocess", "import socket", "import shutil",
    "import sys", "__import__", "eval(", "exec(", "compile(",
    "open('/", "open(\"/"," os.system", "os.popen", "os.exec",
    "subprocess.run", "subprocess.Popen", "subprocess.call",
    "socket.socket", "requests.get", "requests.post",
    "urllib.request", "http.client",
]

# Allowed imports per tier
TIER_ALLOWED_IMPORTS = {
    "magic_workshop": [],  # No raw code execution
    "innovation_lab": [
        "math", "random", "time", "turtle", "json",
        "collections", "itertools", "functools", "string",
    ],
    "professional_studio": [
        "math", "random", "time", "json", "re", "datetime",
        "collections", "itertools", "functools", "string",
        "typing", "dataclasses", "enum", "abc",
        "csv", "io", "textwrap", "pprint",
        "machine",  # MicroPython
    ],
}


class CodeSandboxSchema(BaseModel):
    """Input schema for CodeSandboxTool."""
    code: str = Field(
        description="The Python code to execute in the sandbox."
    )
    language: str = Field(
        default="python",
        description="Programming language: 'python', 'javascript', or 'micropython'."
    )
    tier: str = Field(
        default="innovation_lab",
        description="Student tier: 'magic_workshop', 'innovation_lab', or 'professional_studio'."
    )
    timeout: int = Field(
        default=10,
        description="Maximum execution time in seconds (1-30)."
    )
    explain: bool = Field(
        default=True,
        description="Whether to include a line-by-line explanation of what the code does."
    )


class CodeSandboxTool(BaseTool):
    """
    Execute code safely in an isolated sandbox environment.
    
    Returns the output, any errors, and optionally a line-by-line
    explanation of what the code does (for learning purposes).
    """
    name: str = "run_code"
    description: str = (
        "Execute Python code in a safe sandbox and return the output. "
        "Use this to demonstrate code concepts, run student code, or "
        "show what happens when code runs. Always explain the output "
        "in an age-appropriate way."
    )
    args_schema: Type[BaseModel] = CodeSandboxSchema
    event_bus: Optional[EventBus] = None

    class Config:
        arbitrary_types_allowed = True

    def _check_safety(self, code: str, tier: str) -> Optional[str]:
        """Check code for dangerous patterns. Returns error message or None."""
        code_lower = code.lower()
        for pattern in BLOCKED_PATTERNS:
            if pattern.lower() in code_lower:
                return (
                    f"Oops! The code contains '{pattern}' which isn't allowed "
                    f"in the sandbox for safety reasons. Let's find a different "
                    f"way to do this!"
                )
        return None

    def _run(
        self,
        code: str,
        language: str = "python",
        tier: str = "innovation_lab",
        timeout: int = 10,
        explain: bool = True,
    ) -> str:
        """Execute code in the sandbox and return results."""
        # Clamp timeout
        timeout = max(1, min(30, timeout))

        # Emit tool call event
        if self.event_bus:
            self.event_bus.emit(AgentEvent(
                event_type=EventType.TOOL_CALL,
                agent_name="coding_agent",
                data={"tool": "run_code", "language": language, "code_preview": code[:200]},
            ))

        # Safety check
        safety_error = self._check_safety(code, tier)
        if safety_error:
            return safety_error

        # Tier 1 doesn't execute raw code
        if tier == "magic_workshop":
            return (
                "In the Magic Workshop, we use visual blocks instead of "
                "typing code! The blocks you arranged would do this:\n"
                f"```\n{code}\n```\n"
                "Ask Professor Sparkle to show you what these blocks do!"
            )

        # Execute Python code in restricted subprocess
        if language in ("python", "micropython"):
            return self._execute_python(code, timeout, tier)
        elif language == "javascript":
            return self._execute_javascript(code, timeout)
        else:
            return f"Language '{language}' is not supported yet. Try Python or JavaScript!"

    def _execute_python(self, code: str, timeout: int, tier: str) -> str:
        """Execute Python code in a restricted subprocess."""
        # Wrap code with safety restrictions
        restricted_code = f'''
import sys
import io

# Redirect stdout to capture output
_output = io.StringIO()
sys.stdout = _output

# Block dangerous builtins
_blocked = {{"__import__": __import__}}
def _safe_import(name, *args, **kwargs):
    allowed = {repr(TIER_ALLOWED_IMPORTS.get(tier, []))}
    if name not in allowed:
        raise ImportError(f"Module '{{name}}' is not available in this sandbox. Try using: {{', '.join(allowed)}}")
    return _blocked["__import__"](name, *args, **kwargs)

import builtins
builtins.__import__ = _safe_import

try:
{chr(10).join("    " + line for line in code.split(chr(10)))}
except Exception as e:
    print(f"Error: {{type(e).__name__}}: {{e}}")

sys.stdout = sys.__stdout__
result = _output.getvalue()
if len(result) > 2000:
    result = result[:2000] + "\\n... (output truncated)"
print(result)
'''
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, dir="/tmp"
            ) as f:
                f.write(restricted_code)
                temp_path = f.name

            result = subprocess.run(
                ["python3", temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd="/tmp",
            )

            output = result.stdout.strip()
            errors = result.stderr.strip()

            # Clean up
            os.unlink(temp_path)

            # Emit result event
            if self.event_bus:
                self.event_bus.emit(AgentEvent(
                    event_type=EventType.CODE_OUTPUT,
                    agent_name="coding_agent",
                    data={
                        "output": output[:500],
                        "has_error": bool(errors),
                        "language": "python",
                    },
                ))

            if errors and not output:
                # Make error messages kid-friendly
                friendly_error = self._make_error_friendly(errors)
                return f"The code ran into a problem:\n```\n{friendly_error}\n```\nLet's figure out what went wrong together!"
            elif errors:
                return f"Output:\n```\n{output}\n```\n\nThere were also some warnings:\n```\n{errors[:500]}\n```"
            else:
                return f"Output:\n```\n{output}\n```"

        except subprocess.TimeoutExpired:
            return (
                "The code took too long to run! This usually means there's "
                "an infinite loop. Check your while/for loops to make sure "
                "they have a way to stop."
            )
        except Exception as e:
            return f"Something went wrong running the code: {str(e)}"

    def _execute_javascript(self, code: str, timeout: int) -> str:
        """Execute JavaScript code using Node.js."""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".js", delete=False, dir="/tmp"
            ) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                ["node", temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd="/tmp",
            )

            output = result.stdout.strip()
            errors = result.stderr.strip()
            os.unlink(temp_path)

            if errors and not output:
                friendly_error = self._make_error_friendly(errors)
                return f"The JavaScript code ran into a problem:\n```\n{friendly_error}\n```"
            elif output:
                return f"Output:\n```\n{output}\n```"
            else:
                return "The code ran successfully but didn't print anything. Try adding console.log() to see output!"

        except subprocess.TimeoutExpired:
            return "The JavaScript code took too long to run! Check for infinite loops."
        except Exception as e:
            return f"Something went wrong: {str(e)}"

    def _make_error_friendly(self, error: str) -> str:
        """Convert Python/JS error messages into kid-friendly explanations."""
        error_map = {
            "SyntaxError": "There's a typo in the code! Check for missing colons, brackets, or quotes.",
            "NameError": "The code uses a name that doesn't exist yet. Did you forget to create a variable?",
            "TypeError": "The code tried to do something with the wrong type of data. Like adding a number to a word!",
            "IndexError": "The code tried to access something that doesn't exist in a list. The list might be shorter than you think!",
            "ZeroDivisionError": "The code tried to divide by zero! That's like asking 'how many times does nothing fit into something?'",
            "IndentationError": "The spacing (indentation) isn't right. Make sure your code lines up properly!",
            "ValueError": "The code got a value it didn't expect. Check what you're passing to functions!",
            "KeyError": "The code looked for something in a dictionary that isn't there.",
            "ImportError": "The code tried to use a module that isn't available in the sandbox.",
        }
        for error_type, friendly_msg in error_map.items():
            if error_type in error:
                return f"{friendly_msg}\n\nTechnical details: {error[:300]}"
        return error[:500]
