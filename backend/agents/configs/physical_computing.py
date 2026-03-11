"""
Physical Computing Project Modules
===================================

Tier-specific physical computing projects that integrate with the
Codopia curriculum. Each project is designed as a learning experience
where the AI guides, not generates.

Structure:
    Each project has:
    - Scaffolded code (with strategic blanks for students to fill)
    - Learning objectives mapped to Bloom's taxonomy
    - Wokwi simulator configuration
    - Step-by-step guided challenges
    - Extension activities for fast learners
"""


# ─────────────────────────────────────────────────────────────────────
# TIER 1: MAGIC WORKSHOP (Ages 5-7) — BBC micro:bit
# ─────────────────────────────────────────────────────────────────────

TIER1_PROJECTS = [
    {
        "id": "t1_p1",
        "title": "Smiley Face Spell",
        "module_link": 1,
        "description": "Make the micro:bit show a happy face when you press button A!",
        "device": "micro:bit",
        "difficulty": "beginner",
        "estimated_time": "15 min",
        "learning_objectives": [
            "Understand that buttons are inputs",
            "Understand that LEDs are outputs",
            "Connect cause (button) to effect (display)",
        ],
        "scaffolded_code": """# Professor Sparkle's Smiley Spell!
# Can you fill in the blanks to make the micro:bit smile?

from microbit import *

while True:
    if button_a.is_pressed():
        display.show(Image.___)  # What face should we show? HAPPY!
    else:
        display.show(Image.___)  # What about when no button? ASLEEP!
""",
        "solution": {
            "blank_1": "HAPPY",
            "blank_2": "ASLEEP",
        },
        "sparkle_hints": [
            "The micro:bit has built-in pictures! Try HAPPY, SAD, HEART, or ASLEEP.",
            "Button A is on the LEFT side of the micro:bit.",
            "Image.HAPPY shows a smiley face with 25 tiny LEDs!",
        ],
        "challenges": [
            "Can you make it show a HEART when button B is pressed?",
            "What happens if you press BOTH buttons at the same time?",
            "Can you make your OWN face using display.set_pixel()?",
        ],
    },
    {
        "id": "t1_p2",
        "title": "Shake the Magic Wand",
        "module_link": 3,
        "description": "Shake the micro:bit like a magic wand to cast random spells!",
        "device": "micro:bit",
        "difficulty": "beginner",
        "estimated_time": "20 min",
        "learning_objectives": [
            "Understand sensors (accelerometer)",
            "Understand randomness",
            "Connect physical action to digital response",
        ],
        "scaffolded_code": """# Shake the Magic Wand!
# Shake the micro:bit to cast a random spell!

from microbit import *
import random

spells = [Image.HEART, Image.DIAMOND, Image.STAR, Image.BUTTERFLY]

while True:
    if accelerometer.was_shaken():
        # Pick a random spell from our list
        magic = random.___(spells)  # What function picks randomly?
        display.show(___)           # Show the magic spell!
        sleep(2000)                 # Wait 2 seconds
        display.clear()
""",
        "solution": {
            "blank_1": "choice",
            "blank_2": "magic",
        },
        "sparkle_hints": [
            "random.choice() picks one random thing from a list — like reaching into a hat!",
            "We stored our random pick in a variable called 'magic'.",
            "sleep(2000) means wait 2000 milliseconds, which is 2 seconds!",
        ],
        "challenges": [
            "Add more spells to the list! Try Image.GHOST or Image.SKULL.",
            "Can you make it play a sound when you shake it?",
            "What if different shakes cast different spells?",
        ],
    },
    {
        "id": "t1_p3",
        "title": "Counting Stars",
        "module_link": 4,
        "description": "Press the button to count stars! How high can you go?",
        "device": "micro:bit",
        "difficulty": "intermediate",
        "estimated_time": "20 min",
        "learning_objectives": [
            "Understand variables (counting)",
            "Understand loops",
            "Understand incrementing a counter",
        ],
        "scaffolded_code": """# Counting Stars!
# Press button A to count up, button B to reset!

from microbit import *

stars = ___  # What number do we start counting from?

while True:
    if button_a.is_pressed():
        stars = stars + ___  # How much do we add each time?
        display.scroll(str(stars))
        sleep(500)
    
    if button_b.is_pressed():
        stars = ___  # Reset back to the beginning!
        display.show(Image.HAPPY)
        sleep(500)
""",
        "solution": {
            "blank_1": "0",
            "blank_2": "1",
            "blank_3": "0",
        },
        "sparkle_hints": [
            "We start counting from 0, just like a brand new counter!",
            "Each press adds 1 star to our collection.",
            "To reset, we put the counter back to 0.",
        ],
        "challenges": [
            "Can you count by 2s instead of 1s?",
            "What if button A adds and button B subtracts?",
            "Can you make it show a star image when you reach 10?",
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────
# TIER 2: INNOVATION LAB (Ages 8-12) — Raspberry Pi Pico W
# ─────────────────────────────────────────────────────────────────────

TIER2_PROJECTS = [
    {
        "id": "t2_p1",
        "title": "Temperature Reporter",
        "module_link": 1,
        "description": "Read the Pico's built-in temperature sensor and display readings!",
        "device": "pi-pico-w",
        "difficulty": "beginner",
        "estimated_time": "25 min",
        "learning_objectives": [
            "Read analog sensor data",
            "Convert raw values to meaningful units",
            "Use print() for output",
            "Understand variables and data types",
        ],
        "scaffolded_code": """# Temperature Reporter
# Read the Pico's built-in temperature sensor!

from machine import ADC
import time

# The built-in temp sensor is on ADC channel ___
sensor = ADC(___)  # Which channel? (Hint: it's 4)

def read_temperature():
    raw = sensor.read_u16()
    voltage = raw * ___ / 65535  # What's the Pico's voltage? (3.3V)
    temp_c = 27 - (voltage - 0.706) / 0.001721
    return round(temp_c, 1)

# Read temperature every 2 seconds
while True:
    temperature = read_temperature()
    print(f"Temperature: {___}°C")  # What variable holds our reading?
    time.sleep(2)
""",
        "solution": {
            "blank_1": "4",
            "blank_2": "3.3",
            "blank_3": "temperature",
        },
        "sparkle_hints": [
            "The Pico has a built-in temperature sensor on ADC channel 4.",
            "The Pico runs on 3.3 volts, so we multiply by 3.3.",
            "We stored the reading in a variable called 'temperature'.",
        ],
        "challenges": [
            "Add Fahrenheit conversion: F = C * 9/5 + 32",
            "Store 10 readings in a list and calculate the average",
            "Add a warning message if temperature goes above 30°C",
        ],
    },
    {
        "id": "t2_p2",
        "title": "Traffic Light Controller",
        "module_link": 4,
        "description": "Build a working traffic light with functions for each phase!",
        "device": "pi-pico-w",
        "difficulty": "intermediate",
        "estimated_time": "30 min",
        "learning_objectives": [
            "Define and call functions",
            "Use parameters and return values",
            "Understand sequential logic",
            "Control multiple outputs",
        ],
        "scaffolded_code": """# Traffic Light Controller
# Use functions to control each traffic light phase!

from machine import Pin
import time

red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

def all_off():
    \"\"\"Turn off all lights.\"\"\"
    red.value(0)
    yellow.value(0)
    green.value(0)

def go_phase(duration):
    \"\"\"Green light — cars can go!\"\"\"
    all_off()
    ___.value(1)  # Which light means GO?
    time.sleep(duration)

def caution_phase(duration):
    \"\"\"Yellow light — slow down!\"\"\"
    all_off()
    ___.value(1)  # Which light means CAUTION?
    time.sleep(duration)

def stop_phase(duration):
    \"\"\"Red light — stop!\"\"\"
    all_off()
    ___.value(1)  # Which light means STOP?
    time.sleep(duration)

# Run the traffic light forever
while True:
    go_phase(___)       # How many seconds for green?
    caution_phase(___)  # How many seconds for yellow?
    stop_phase(___)     # How many seconds for red?
""",
        "solution": {
            "blank_1": "green",
            "blank_2": "yellow",
            "blank_3": "red",
            "blank_4": "3",
            "blank_5": "1",
            "blank_6": "3",
        },
        "sparkle_hints": [
            "Green means GO, yellow means CAUTION, red means STOP!",
            "Each function controls one phase of the traffic light.",
            "Real traffic lights: green ~30s, yellow ~3s, red ~30s. For testing, use shorter times!",
        ],
        "challenges": [
            "Add a pedestrian crossing button that interrupts the cycle",
            "Make the yellow light blink 3 times before turning red",
            "Add a countdown display showing seconds until the next change",
        ],
    },
    {
        "id": "t2_p3",
        "title": "Reaction Time Game",
        "module_link": 3,
        "description": "Build a reaction speed tester — how fast can you press the button?",
        "device": "pi-pico-w",
        "difficulty": "intermediate",
        "estimated_time": "35 min",
        "learning_objectives": [
            "Use random for unpredictability",
            "Measure time precisely",
            "Use lists to store data",
            "Calculate averages",
        ],
        "scaffolded_code": """# Reaction Time Game!
# Press the button as fast as you can when the LED lights up!

from machine import Pin
import time
import random

led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)

def play_round():
    led.value(0)
    print("Get ready...")
    
    # Wait a random time so you can't cheat!
    wait_time = random.uniform(___, ___)  # Random between ? and ? seconds
    time.sleep(wait_time)
    
    # LED ON — GO!
    led.value(1)
    start = time.ticks_ms()
    
    # Wait for button press
    while button.value() == ___:  # What value when NOT pressed? (1)
        pass
    
    # Calculate reaction time
    reaction = time.ticks_diff(time.ticks_ms(), start)
    led.value(0)
    return reaction

# Play 3 rounds and track scores
scores = ___  # What data structure stores multiple values?
for i in range(3):
    print(f"Round {i + 1}!")
    ms = play_round()
    print(f"Reaction: {ms}ms")
    scores.append(ms)
    time.sleep(1)

average = sum(scores) / len(scores)
print(f"Average: {average:.0f}ms")
""",
        "solution": {
            "blank_1": "1",
            "blank_2": "5",
            "blank_3": "1",
            "blank_4": "[]",
        },
        "sparkle_hints": [
            "random.uniform(1, 5) gives a random decimal between 1 and 5 seconds.",
            "With PULL_UP, the button reads 1 when NOT pressed, 0 when pressed.",
            "An empty list [] is perfect for collecting scores!",
        ],
        "challenges": [
            "Add difficulty levels: easy (1-3s wait), hard (0.5-5s wait)",
            "Display a rating: <200ms = 'Lightning!', <400ms = 'Great!', etc.",
            "Add a high score tracker that persists between games",
        ],
    },
    {
        "id": "t2_p4",
        "title": "IoT Weather Station",
        "module_link": 7,
        "description": "Build a weather station that sends data to a web dashboard!",
        "device": "pi-pico-w",
        "difficulty": "advanced",
        "estimated_time": "45 min",
        "learning_objectives": [
            "Connect to WiFi",
            "Send HTTP requests",
            "Work with JSON data",
            "Understand IoT concepts",
        ],
        "scaffolded_code": """# IoT Weather Station
# Read sensors and send data to a web dashboard!

import network
import urequests
import json
from machine import ADC, Pin
import time

# WiFi setup
wlan = network.WLAN(network.___)  # Station or Access Point? (STA_IF)
wlan.active(True)
wlan.connect("YourWiFi", "YourPassword")

# Wait for connection
while not wlan.isconnected():
    print("Connecting...")
    time.sleep(1)
print(f"Connected! IP: {wlan.ifconfig()[0]}")

# Temperature sensor
temp_sensor = ADC(4)

def read_temp():
    raw = temp_sensor.read_u16()
    voltage = raw * 3.3 / 65535
    return round(27 - (voltage - 0.706) / 0.001721, 1)

# Send data every 30 seconds
while True:
    temp = read_temp()
    
    # Build the data payload
    data = {
        "temperature": ___,  # What variable holds our reading?
        "unit": "celsius",
        "device": "pico_w"
    }
    
    # Convert to JSON and send
    payload = json.___(data)  # What function converts dict to JSON string?
    print(f"Sending: {payload}")
    
    # In production, this would POST to your API
    # response = urequests.post("https://your-api.com/data", data=payload)
    
    time.sleep(30)
""",
        "solution": {
            "blank_1": "STA_IF",
            "blank_2": "temp",
            "blank_3": "dumps",
        },
        "sparkle_hints": [
            "STA_IF means Station Interface — the Pico connects TO a WiFi network.",
            "We stored the temperature reading in the variable 'temp'.",
            "json.dumps() converts a Python dictionary into a JSON string for sending.",
        ],
        "challenges": [
            "Add a light sensor (LDR) to measure brightness",
            "Create a simple web server ON the Pico that shows the data",
            "Add data logging to a file on the Pico's filesystem",
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────
# TIER 3: PROFESSIONAL STUDIO (Ages 13-18) — Pi Pico W / ESP32
# ─────────────────────────────────────────────────────────────────────

TIER3_PROJECTS = [
    {
        "id": "t3_p1",
        "title": "MQTT Smart Home Controller",
        "module_link": 4,
        "description": "Build a smart home system using MQTT protocol for real-time device control.",
        "device": "pi-pico-w",
        "difficulty": "advanced",
        "estimated_time": "60 min",
        "learning_objectives": [
            "Understand pub/sub messaging patterns",
            "Implement MQTT client on microcontroller",
            "Design a topic hierarchy",
            "Handle asynchronous events",
        ],
        "scaffolded_code": """# MQTT Smart Home Controller
# Control devices using publish/subscribe messaging!

import network
import time
from umqtt.simple import MQTTClient
from machine import Pin

# Hardware
led_room = Pin(15, Pin.OUT)
led_porch = Pin(14, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)

# MQTT Configuration
BROKER = "test.mosquitto.org"
CLIENT_ID = "codopia_pico_001"
TOPIC_PREFIX = "codopia/home"

# Topic hierarchy design:
# codopia/home/room/light    → control room light
# codopia/home/porch/light   → control porch light
# codopia/home/status        → device status updates

def on_message(topic, msg):
    \"\"\"Handle incoming MQTT messages.\"\"\"
    topic_str = topic.decode()
    msg_str = msg.decode()
    print(f"Received: {topic_str} → {msg_str}")
    
    if topic_str == f"{TOPIC_PREFIX}/room/light":
        led_room.value(___ if msg_str == "on" else ___)  # What values for on/off?
    elif topic_str == f"{TOPIC_PREFIX}/porch/light":
        led_porch.value(1 if msg_str == "___" else 0)  # What string means turn on?

# Connect to WiFi (simplified)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# wlan.connect("SSID", "PASSWORD")

# Connect to MQTT broker
client = MQTTClient(CLIENT_ID, ___)  # What's our broker address?
client.set_callback(on_message)
client.connect()

# Subscribe to control topics
client.subscribe(f"{TOPIC_PREFIX}/+/light")  # + is a single-level wildcard

print("Smart Home Controller ready!")
print(f"Subscribed to: {TOPIC_PREFIX}/+/light")

# Main loop
while True:
    client.check_msg()  # Check for new messages
    
    # Publish button state
    if button.value() == 0:
        client.publish(
            f"{TOPIC_PREFIX}/status",
            '{"button": "pressed", "timestamp": ' + str(time.time()) + '}'
        )
        time.sleep(0.5)  # Debounce
    
    time.sleep(0.1)
""",
        "solution": {
            "blank_1": "1",
            "blank_2": "0",
            "blank_3": "on",
            "blank_4": "BROKER",
        },
        "sparkle_hints": [
            "In digital logic, 1 means ON and 0 means OFF.",
            "The message 'on' turns the light on, anything else turns it off.",
            "BROKER holds our server address — test.mosquitto.org is a free public broker.",
        ],
        "challenges": [
            "Add QoS levels — what happens if a message is lost?",
            "Implement a Last Will and Testament (LWT) for disconnect detection",
            "Build a React dashboard that subscribes to the same MQTT topics",
            "Add TLS encryption for secure communication",
        ],
    },
    {
        "id": "t3_p2",
        "title": "Edge ML: Gesture Recognition",
        "module_link": 7,
        "description": "Train a tiny ML model to recognize hand gestures using the accelerometer.",
        "device": "pi-pico-w",
        "difficulty": "expert",
        "estimated_time": "90 min",
        "learning_objectives": [
            "Understand machine learning basics",
            "Collect and label training data",
            "Deploy a model to a microcontroller",
            "Evaluate model accuracy",
        ],
        "scaffolded_code": """# Edge ML: Gesture Recognition
# Train the Pico to recognize hand gestures!

from machine import Pin, I2C
import time
import json

# Simulated accelerometer data (in production, use MPU6050)
# Each gesture is a sequence of [x, y, z] readings

class GestureRecognizer:
    def __init__(self):
        self.gestures = {}  # name → list of training samples
        self.is_trained = False
    
    def record_gesture(self, name, duration=2):
        \"\"\"Record a gesture for training.\"\"\"
        print(f"Recording '{name}' in 3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1... GO!")
        
        samples = []
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
            # In production: read real accelerometer
            # x, y, z = accelerometer.read()
            import random
            x = random.uniform(-2, 2)
            y = random.uniform(-2, 2)
            z = random.uniform(-2, 2)
            samples.append([round(x,2), round(y,2), round(z,2)])
            time.sleep(0.05)
        
        if name not in self.gestures:
            self.gestures[___] = []  # What key do we use?
        self.gestures[name].append(samples)
        print(f"Recorded {len(samples)} samples for '{name}'")
    
    def train(self):
        \"\"\"Train the model using collected data.\"\"\"
        if len(self.gestures) < ___:  # Minimum gestures needed?
            print("Need at least 2 different gestures to train!")
            return False
        
        # Simple DTW-based classifier (production would use TFLite)
        self.is_trained = True
        gesture_names = list(self.gestures.keys())
        print(f"Model trained on {len(gesture_names)} gestures: {gesture_names}")
        return True
    
    def predict(self, samples):
        \"\"\"Predict which gesture the samples represent.\"\"\"
        if not self.___:  # What flag tells us if training is done?
            print("Model not trained yet!")
            return None
        
        # Simplified prediction (compare average magnitudes)
        best_match = None
        best_score = float('inf')
        
        for name, training_data in self.gestures.items():
            for training_sample in training_data:
                score = self._compare(samples, training_sample)
                if score < best_score:
                    best_score = score
                    best_match = name
        
        confidence = max(0, 100 - best_score * 10)
        return {"gesture": best_match, "confidence": round(confidence, 1)}
    
    def _compare(self, a, b):
        \"\"\"Simple distance metric between two gesture recordings.\"\"\"
        min_len = min(len(a), len(b))
        total = 0
        for i in range(min_len):
            for j in range(3):  # x, y, z
                total += (a[i][j] - b[i][j]) ** 2
        return total / min_len

# Usage
recognizer = GestureRecognizer()

# Training phase
print("=== TRAINING PHASE ===")
print("Let's teach the Pico to recognize gestures!")
recognizer.record_gesture("wave", duration=2)
recognizer.record_gesture("shake", duration=2)
recognizer.train()

# Prediction phase
print("\\n=== PREDICTION PHASE ===")
print("Now perform a gesture!")
""",
        "solution": {
            "blank_1": "name",
            "blank_2": "2",
            "blank_3": "is_trained",
        },
        "sparkle_hints": [
            "We use the gesture 'name' as the dictionary key to store its samples.",
            "You need at least 2 different gestures to have something to classify between.",
            "The 'is_trained' flag tells us whether the model has been trained.",
        ],
        "challenges": [
            "Implement Dynamic Time Warping (DTW) for better gesture matching",
            "Export the model as a TFLite file for faster inference",
            "Add a confusion matrix to evaluate model accuracy",
            "Build a web interface that shows real-time gesture predictions",
        ],
    },
    {
        "id": "t3_p3",
        "title": "OTA Firmware Updater",
        "module_link": 8,
        "description": "Build an Over-The-Air update system to deploy code to devices remotely.",
        "device": "pi-pico-w",
        "difficulty": "expert",
        "estimated_time": "75 min",
        "learning_objectives": [
            "Understand OTA update architecture",
            "Implement version checking",
            "Handle file downloads safely",
            "Implement rollback on failure",
        ],
        "scaffolded_code": """# OTA Firmware Updater
# Update your Pico's code over WiFi — like a real IoT device!

import network
import urequests
import json
import os
import machine
import time

CURRENT_VERSION = "1.0.0"
UPDATE_SERVER = "https://your-api.com/firmware"

class OTAUpdater:
    def __init__(self, server_url, current_version):
        self.server = server_url
        self.version = current_version
    
    def check_for_update(self):
        \"\"\"Check if a newer version is available.\"\"\"
        try:
            response = urequests.get(f"{self.server}/latest")
            data = response.json()
            latest = data.get("version", self.version)
            
            if self._version_compare(latest, self.version) > 0:
                return {
                    "available": ___,  # Is an update available? (True/False)
                    "current": self.version,
                    "latest": latest,
                    "url": data.get("download_url"),
                    "changelog": data.get("changelog", "No changelog"),
                }
            return {"available": False, "current": self.version}
        except Exception as e:
            print(f"Update check failed: {e}")
            return {"available": False, "error": str(e)}
    
    def _version_compare(self, v1, v2):
        \"\"\"Compare semantic version strings.\"\"\"
        parts1 = [int(x) for x in v1.split("___")]  # What separates version parts?
        parts2 = [int(x) for x in v2.split(".")]
        
        for a, b in zip(parts1, parts2):
            if a > b: return 1
            if a < b: return -1
        return 0
    
    def download_and_apply(self, url):
        \"\"\"Download new firmware and apply it.\"\"\"
        print("Downloading update...")
        
        # Step 1: Backup current main.py
        try:
            os.rename("main.py", "main.py.___")  # What extension for backups?
            print("Backup created: main.py.bak")
        except:
            print("No existing main.py to backup")
        
        # Step 2: Download new version
        try:
            response = urequests.get(url)
            new_code = response.text
            
            with open("main.py", "w") as f:
                f.write(new_code)
            print("New firmware written!")
            
            # Step 3: Verify (basic check)
            if len(new_code) < 10:
                raise ValueError("Downloaded file too small — likely corrupted")
            
            print("Update successful! Rebooting...")
            time.sleep(2)
            machine.reset()
            
        except Exception as e:
            print(f"Update failed: {e}")
            self._rollback()
    
    def _rollback(self):
        \"\"\"Restore the backup if update fails.\"\"\"
        print("Rolling back to previous version...")
        try:
            os.rename("main.py.bak", "main.py")
            print("Rollback successful!")
        except:
            print("CRITICAL: Rollback failed! Manual intervention needed.")

# Usage
updater = OTAUpdater(UPDATE_SERVER, CURRENT_VERSION)
print(f"Current firmware: v{CURRENT_VERSION}")

update_info = updater.check_for_update()
if update_info["available"]:
    print(f"Update available: v{update_info['latest']}")
    print(f"Changelog: {update_info['changelog']}")
    # updater.download_and_apply(update_info["url"])
else:
    print("Firmware is up to date!")
""",
        "solution": {
            "blank_1": "True",
            "blank_2": ".",
            "blank_3": "bak",
        },
        "sparkle_hints": [
            "True (capital T) is a Python boolean — the update IS available.",
            "Semantic versioning uses dots: major.minor.patch (e.g., 1.2.3).",
            ".bak is the standard extension for backup files.",
        ],
        "challenges": [
            "Add SHA-256 checksum verification for downloaded files",
            "Implement a staged rollout (update 10% of devices first)",
            "Add a web dashboard showing all devices and their firmware versions",
            "Implement encrypted firmware packages for security",
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────
# Combined Project Registry
# ─────────────────────────────────────────────────────────────────────

ALL_PROJECTS = {
    "magic_workshop": TIER1_PROJECTS,
    "innovation_lab": TIER2_PROJECTS,
    "professional_studio": TIER3_PROJECTS,
}


def get_projects_for_tier(tier: str) -> list:
    """Get all physical computing projects for a tier."""
    return ALL_PROJECTS.get(tier, [])


def get_project_by_id(project_id: str) -> dict:
    """Get a specific project by its ID."""
    for tier_projects in ALL_PROJECTS.values():
        for project in tier_projects:
            if project["id"] == project_id:
                return project
    return None


def get_project_for_module(tier: str, module_id: int) -> dict:
    """Get the physical computing project linked to a curriculum module."""
    projects = ALL_PROJECTS.get(tier, [])
    for project in projects:
        if project.get("module_link") == module_id:
            return project
    return None
