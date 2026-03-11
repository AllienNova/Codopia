"""
WokwiSimulatorTool
==================

Provides integration with the Wokwi hardware simulator for
physical computing education.

Architecture:
    - In production: embeds Wokwi simulator via iframe with API control
    - In development: generates simulator configuration and code
    - In demo mode: returns simulated hardware output

Wokwi Integration:
    Wokwi provides a free, browser-based simulator for:
    - Arduino (Uno, Mega, Nano)
    - ESP32 / ESP32-S2 / ESP32-C3
    - Raspberry Pi Pico / Pico W
    - STM32
    - BBC micro:bit (coming soon)

    The simulator supports:
    - LEDs, buttons, sensors, displays, motors, servos
    - WiFi simulation (ESP32, Pico W)
    - Serial monitor
    - Logic analyzer
    - Custom chips (advanced)

Tier Behavior:
    Tier 1: micro:bit simulator with visual blocks
    Tier 2: Pi Pico W simulator with MicroPython
    Tier 3: ESP32/Pico W with full MicroPython or C++
"""

import json
from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from backend.agents.events import EventBus, AgentEvent, EventType


# Pre-built project templates for each tier
PROJECT_TEMPLATES = {
    "led_blink": {
        "name": "LED Blink",
        "description": "Make an LED blink on and off",
        "tier": ["magic_workshop", "innovation_lab", "professional_studio"],
        "device": "pi-pico-w",
        "code": '''from machine import Pin
import time

led = Pin(25, Pin.OUT)  # Built-in LED on Pico

while True:
    led.value(1)   # LED ON
    time.sleep(0.5)
    led.value(0)   # LED OFF
    time.sleep(0.5)
''',
        "wiring": {
            "parts": [
                {"type": "wokwi-pi-pico-w", "id": "pico"},
            ],
            "connections": [],
        },
        "learning_points": [
            "Pin(25, Pin.OUT) sets up GPIO pin 25 as an output",
            "led.value(1) sends electricity to turn the LED on",
            "time.sleep(0.5) waits half a second",
            "The while True loop makes it repeat forever",
        ],
    },
    "traffic_light": {
        "name": "Traffic Light",
        "description": "Build a traffic light with red, yellow, and green LEDs",
        "tier": ["innovation_lab", "professional_studio"],
        "device": "pi-pico-w",
        "code": '''from machine import Pin
import time

red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

def traffic_cycle():
    """Run one complete traffic light cycle."""
    # Green phase
    green.value(1)
    red.value(0)
    yellow.value(0)
    time.sleep(3)
    
    # Yellow phase
    green.value(0)
    yellow.value(1)
    time.sleep(1)
    
    # Red phase
    yellow.value(0)
    red.value(1)
    time.sleep(3)

while True:
    traffic_cycle()
''',
        "wiring": {
            "parts": [
                {"type": "wokwi-pi-pico-w", "id": "pico"},
                {"type": "wokwi-led", "id": "red_led", "attrs": {"color": "red"}},
                {"type": "wokwi-led", "id": "yellow_led", "attrs": {"color": "yellow"}},
                {"type": "wokwi-led", "id": "green_led", "attrs": {"color": "green"}},
                {"type": "wokwi-resistor", "id": "r1", "attrs": {"resistance": "220"}},
                {"type": "wokwi-resistor", "id": "r2", "attrs": {"resistance": "220"}},
                {"type": "wokwi-resistor", "id": "r3", "attrs": {"resistance": "220"}},
            ],
            "connections": [
                ["pico:GP15", "r1:1"],
                ["r1:2", "red_led:A"],
                ["red_led:C", "pico:GND.1"],
                ["pico:GP14", "r2:1"],
                ["r2:2", "yellow_led:A"],
                ["yellow_led:C", "pico:GND.2"],
                ["pico:GP13", "r3:1"],
                ["r3:2", "green_led:A"],
                ["green_led:C", "pico:GND.3"],
            ],
        },
        "learning_points": [
            "Each LED connects to a different GPIO pin through a resistor",
            "Resistors (220 ohm) protect the LEDs from too much current",
            "Functions like traffic_cycle() organize code into reusable blocks",
            "time.sleep() controls how long each light stays on",
        ],
    },
    "temperature_sensor": {
        "name": "Temperature Sensor",
        "description": "Read temperature from a sensor and display it",
        "tier": ["innovation_lab", "professional_studio"],
        "device": "pi-pico-w",
        "code": '''from machine import Pin, ADC
import time

# Built-in temperature sensor on Pico
temp_sensor = ADC(4)

def read_temperature():
    """Read temperature from the built-in sensor."""
    raw = temp_sensor.read_u16()
    voltage = raw * 3.3 / 65535
    temperature_c = 27 - (voltage - 0.706) / 0.001721
    temperature_f = temperature_c * 9/5 + 32
    return round(temperature_c, 1), round(temperature_f, 1)

while True:
    celsius, fahrenheit = read_temperature()
    print(f"Temperature: {celsius}C / {fahrenheit}F")
    time.sleep(2)
''',
        "wiring": {
            "parts": [
                {"type": "wokwi-pi-pico-w", "id": "pico"},
            ],
            "connections": [],
        },
        "learning_points": [
            "ADC(4) accesses the Pico's built-in temperature sensor",
            "read_u16() reads a raw 16-bit value (0-65535)",
            "We convert the raw value to voltage, then to temperature",
            "The formula comes from the RP2040 datasheet",
        ],
    },
    "reaction_game": {
        "name": "Reaction Time Game",
        "description": "Test your reaction speed — press the button when the LED lights up!",
        "tier": ["innovation_lab", "professional_studio"],
        "device": "pi-pico-w",
        "code": '''from machine import Pin
import time
import random

led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)

def play_round():
    """Play one round of the reaction game."""
    # Wait a random time
    led.value(0)
    print("Get ready...")
    time.sleep(random.uniform(1, 5))
    
    # Turn on LED and start timer
    led.value(1)
    print("NOW! Press the button!")
    start_time = time.ticks_ms()
    
    # Wait for button press
    while button.value() == 1:  # Button not pressed
        pass
    
    # Calculate reaction time
    reaction_ms = time.ticks_diff(time.ticks_ms(), start_time)
    led.value(0)
    
    print(f"Your reaction time: {reaction_ms}ms")
    if reaction_ms < 200:
        print("AMAZING! Lightning fast!")
    elif reaction_ms < 400:
        print("Great reflexes!")
    elif reaction_ms < 600:
        print("Good job! Keep practicing!")
    else:
        print("Keep trying, you'll get faster!")
    
    return reaction_ms

# Play 3 rounds
scores = []
for i in range(3):
    print(f"\\n--- Round {i+1} ---")
    score = play_round()
    scores.append(score)
    time.sleep(1)

avg = sum(scores) / len(scores)
print(f"\\nAverage reaction time: {avg:.0f}ms")
''',
        "wiring": {
            "parts": [
                {"type": "wokwi-pi-pico-w", "id": "pico"},
                {"type": "wokwi-led", "id": "led1", "attrs": {"color": "green"}},
                {"type": "wokwi-resistor", "id": "r1", "attrs": {"resistance": "220"}},
                {"type": "wokwi-pushbutton", "id": "btn1"},
            ],
            "connections": [
                ["pico:GP15", "r1:1"],
                ["r1:2", "led1:A"],
                ["led1:C", "pico:GND.1"],
                ["pico:GP14", "btn1:1.l"],
                ["btn1:2.l", "pico:GND.2"],
            ],
        },
        "learning_points": [
            "random.uniform(1, 5) creates a random wait so you can't cheat",
            "time.ticks_ms() measures time in milliseconds for precision",
            "Pin.PULL_UP means the button reads 1 when NOT pressed, 0 when pressed",
            "Lists store multiple scores so we can calculate the average",
        ],
    },
}


class WokwiSimulatorSchema(BaseModel):
    """Input schema for WokwiSimulatorTool."""
    action: str = Field(
        description="Action: 'list_templates', 'get_template', 'generate_config', or 'explain_wiring'."
    )
    template_name: Optional[str] = Field(
        default=None,
        description="Name of the project template (e.g., 'led_blink', 'traffic_light')."
    )
    tier: str = Field(
        default="innovation_lab",
        description="Student tier for filtering appropriate templates."
    )
    custom_code: Optional[str] = Field(
        default=None,
        description="Custom MicroPython code to generate a Wokwi config for."
    )


class WokwiSimulatorTool(BaseTool):
    """
    Interact with the Wokwi hardware simulator for physical computing projects.
    
    Provides project templates, wiring configurations, and code for
    simulating hardware projects in the browser.
    """
    name: str = "hardware_simulator"
    description: str = (
        "Access the Wokwi hardware simulator for physical computing projects. "
        "Can list available project templates, get a specific template with "
        "code and wiring, or generate a simulator configuration for custom code. "
        "Use this for all hardware-related teaching."
    )
    args_schema: Type[BaseModel] = WokwiSimulatorSchema
    event_bus: Optional[EventBus] = None

    class Config:
        arbitrary_types_allowed = True

    def _run(
        self,
        action: str,
        template_name: Optional[str] = None,
        tier: str = "innovation_lab",
        custom_code: Optional[str] = None,
    ) -> str:
        """Execute the requested simulator action."""
        if action == "list_templates":
            return self._list_templates(tier)
        elif action == "get_template":
            return self._get_template(template_name, tier)
        elif action == "generate_config":
            return self._generate_config(custom_code, tier)
        elif action == "explain_wiring":
            return self._explain_wiring(template_name)
        else:
            return f"Unknown action: {action}. Use: list_templates, get_template, generate_config, explain_wiring"

    def _list_templates(self, tier: str) -> str:
        """List available project templates for this tier."""
        available = []
        for name, template in PROJECT_TEMPLATES.items():
            if tier in template["tier"]:
                available.append(f"  - {name}: {template['description']}")

        if not available:
            return f"No templates available for tier: {tier}"

        return f"Available hardware projects for {tier}:\n" + "\n".join(available)

    def _get_template(self, template_name: str, tier: str) -> str:
        """Get a specific project template with code and wiring."""
        template = PROJECT_TEMPLATES.get(template_name)
        if not template:
            return f"Template '{template_name}' not found. Use list_templates to see available projects."

        if tier not in template["tier"]:
            return f"Template '{template_name}' is not available for tier {tier}."

        # Emit simulation event
        if self.event_bus:
            self.event_bus.emit(AgentEvent(
                event_type=EventType.SIMULATION_UPDATE,
                agent_name="hardware_agent",
                data={
                    "template": template_name,
                    "device": template["device"],
                    "action": "load_template",
                },
            ))

        result = (
            f"Project: {template['name']}\n"
            f"Description: {template['description']}\n"
            f"Device: {template['device']}\n\n"
            f"Code:\n```python\n{template['code']}\n```\n\n"
            f"What you'll learn:\n"
        )
        for point in template["learning_points"]:
            result += f"  - {point}\n"

        wiring_parts = template["wiring"]["parts"]
        if len(wiring_parts) > 1:
            result += f"\nParts needed:\n"
            for part in wiring_parts:
                result += f"  - {part['type'].replace('wokwi-', '')}"
                if "attrs" in part:
                    attrs = ", ".join(f"{k}={v}" for k, v in part["attrs"].items())
                    result += f" ({attrs})"
                result += "\n"

        return result

    def _generate_config(self, code: str, tier: str) -> str:
        """Generate a Wokwi diagram.json config for custom code."""
        if not code:
            return "Please provide custom MicroPython code to generate a config for."

        # Analyze code to determine needed components
        parts = [{"type": "wokwi-pi-pico-w", "id": "pico", "top": 0, "left": 0}]
        connections = []

        code_lower = code.lower()
        gpio_pins_used = set()

        # Detect LED usage
        if "pin.out" in code_lower or "led" in code_lower:
            parts.append({"type": "wokwi-led", "id": "led1", "attrs": {"color": "green"}})
            parts.append({"type": "wokwi-resistor", "id": "r1", "attrs": {"resistance": "220"}})

        # Detect button usage
        if "pin.in" in code_lower or "button" in code_lower or "pull_up" in code_lower:
            parts.append({"type": "wokwi-pushbutton", "id": "btn1"})

        # Detect temperature sensor
        if "adc(4)" in code_lower or "temperature" in code_lower:
            pass  # Built-in sensor, no external parts needed

        # Detect servo
        if "servo" in code_lower or "pwm" in code_lower:
            parts.append({"type": "wokwi-servo", "id": "servo1"})

        config = {
            "version": 1,
            "author": "Codopia",
            "editor": "wokwi",
            "parts": parts,
            "connections": connections,
        }

        return (
            f"Generated Wokwi configuration for your code:\n"
            f"```json\n{json.dumps(config, indent=2)}\n```\n\n"
            f"Parts detected: {len(parts)} components\n"
            f"To run this in Wokwi: paste the code and this config into wokwi.com"
        )

    def _explain_wiring(self, template_name: str) -> str:
        """Explain the wiring diagram for a project in kid-friendly terms."""
        template = PROJECT_TEMPLATES.get(template_name)
        if not template:
            return f"Template '{template_name}' not found."

        connections = template["wiring"]["connections"]
        if not connections:
            return (
                f"The {template['name']} project uses the Pico's built-in "
                f"components, so no extra wiring is needed! Just plug in the "
                f"Pico and you're ready to go."
            )

        explanation = f"Wiring explanation for {template['name']}:\n\n"
        for conn in connections:
            pin_a, pin_b = conn[0], conn[1]
            explanation += f"  Connect {pin_a} → {pin_b}\n"

        explanation += (
            f"\nRemember:\n"
            f"  - Always connect through a resistor to protect LEDs\n"
            f"  - GND means Ground (the negative side)\n"
            f"  - GP## means General Purpose pin number ##\n"
            f"  - A = Anode (long leg, positive), C = Cathode (short leg, negative)\n"
        )

        return explanation
