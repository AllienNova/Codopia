"""
Codopia Voice Bridge
====================

Provides multimodal voice + text interaction for the agent system.

Architecture:
    Frontend (Browser):
        - Web Speech API (SpeechRecognition) for speech-to-text
        - Web Speech API (SpeechSynthesis) for text-to-speech
        - MediaRecorder API for audio capture (Gemini Live fallback)
    
    Backend (Flask):
        - Gemini Live API for real-time voice conversation (advanced)
        - Google TTS API for high-quality speech synthesis (fallback)
        - Audio processing and streaming via Socket.IO
    
Tier Behavior:
    Tier 1 (Magic Workshop, ages 5-7):
        - Voice is PRIMARY input/output
        - Big microphone button, always visible
        - Professor Sparkle speaks every response
        - Simple vocabulary, short sentences
        - Speech rate: slow (0.8x)
    
    Tier 2 (Innovation Lab, ages 8-12):
        - Voice and text are EQUAL
        - Toggle between voice and text mode
        - Professor Sparkle speaks on request or for key explanations
        - Normal vocabulary
        - Speech rate: normal (1.0x)
    
    Tier 3 (Professional Studio, ages 13-18):
        - Text is PRIMARY
        - Voice available for architecture discussions
        - Professor Sparkle speaks only when requested
        - Technical vocabulary
        - Speech rate: normal-fast (1.1x)

Integration:
    The voice bridge works alongside the agent system:
    1. Student speaks → Web Speech API transcribes → text sent to agent
    2. Agent responds with text → Voice bridge synthesizes → student hears
    3. For Gemini Live: bidirectional audio stream for natural conversation
"""

import json
import base64
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VoiceConfig:
    """Voice configuration per tier."""
    tier: str
    voice_mode: str          # "primary", "equal", "secondary"
    speech_rate: float       # 0.5 - 2.0
    pitch: float             # 0.5 - 2.0
    voice_name: str          # Web Speech API voice name
    auto_speak: bool         # Automatically speak all responses
    max_response_length: int # Max chars to speak (truncate for long responses)
    wake_word: str           # Optional wake word for hands-free


# Pre-configured voice settings per tier
VOICE_CONFIGS = {
    "magic_workshop": VoiceConfig(
        tier="magic_workshop",
        voice_mode="primary",
        speech_rate=0.85,
        pitch=1.15,
        voice_name="Google UK English Female",
        auto_speak=True,
        max_response_length=300,
        wake_word="hey sparkle",
    ),
    "innovation_lab": VoiceConfig(
        tier="innovation_lab",
        voice_mode="equal",
        speech_rate=1.0,
        pitch=1.05,
        voice_name="Google UK English Female",
        auto_speak=False,
        max_response_length=500,
        wake_word="hey sparkle",
    ),
    "professional_studio": VoiceConfig(
        tier="professional_studio",
        voice_mode="secondary",
        speech_rate=1.05,
        pitch=1.0,
        voice_name="Google UK English Female",
        auto_speak=False,
        max_response_length=800,
        wake_word="sparkle",
    ),
}


class VoiceBridge:
    """
    Manages voice interaction between the frontend and agent system.
    
    This class provides:
    1. Voice configuration per tier
    2. Text-to-speech preparation (frontend handles actual synthesis)
    3. Speech-to-text post-processing (cleanup, punctuation)
    4. Gemini Live API session management (for advanced voice)
    5. Audio streaming coordination via Socket.IO
    """

    def __init__(self):
        self._active_sessions: Dict[str, Dict] = {}

    def get_voice_config(self, tier: str) -> Dict[str, Any]:
        """Get voice configuration for a tier (sent to frontend)."""
        config = VOICE_CONFIGS.get(tier, VOICE_CONFIGS["innovation_lab"])
        return {
            "tier": config.tier,
            "voice_mode": config.voice_mode,
            "speech_rate": config.speech_rate,
            "pitch": config.pitch,
            "voice_name": config.voice_name,
            "auto_speak": config.auto_speak,
            "max_response_length": config.max_response_length,
            "wake_word": config.wake_word,
            "supported_languages": ["en-US", "en-GB", "es-ES", "fr-FR"],
            "features": {
                "speech_to_text": True,
                "text_to_speech": True,
                "wake_word_detection": config.voice_mode == "primary",
                "continuous_listening": config.voice_mode == "primary",
                "gemini_live": False,  # Requires API key configuration
            },
        }

    def prepare_speech_output(
        self,
        text: str,
        tier: str,
        is_question: bool = False,
    ) -> Dict[str, Any]:
        """
        Prepare text for speech synthesis on the frontend.
        
        Cleans up the text, adjusts for the tier, and returns
        speech parameters for the Web Speech API.
        """
        config = VOICE_CONFIGS.get(tier, VOICE_CONFIGS["innovation_lab"])

        # Clean text for speech
        clean_text = self._clean_for_speech(text, tier)

        # Truncate if too long
        if len(clean_text) > config.max_response_length:
            # Find a natural break point
            truncated = clean_text[:config.max_response_length]
            last_period = truncated.rfind(".")
            last_question = truncated.rfind("?")
            last_exclaim = truncated.rfind("!")
            break_point = max(last_period, last_question, last_exclaim)
            if break_point > config.max_response_length * 0.5:
                clean_text = truncated[:break_point + 1]
            else:
                clean_text = truncated + "..."

        # Adjust speech rate for questions (slightly slower)
        rate = config.speech_rate
        if is_question:
            rate *= 0.95

        return {
            "text": clean_text,
            "rate": rate,
            "pitch": config.pitch,
            "voice": config.voice_name,
            "auto_speak": config.auto_speak or is_question,
            "is_question": is_question,
        }

    def process_speech_input(self, transcript: str, tier: str) -> str:
        """
        Post-process speech-to-text transcript before sending to agent.
        
        Cleans up common speech recognition errors, adds punctuation,
        and normalizes for the agent system.
        """
        if not transcript:
            return ""

        text = transcript.strip()

        # Common speech-to-text corrections for kids
        corrections = {
            "um ": "",
            "uh ": "",
            "like ": "",
            "you know ": "",
            "i wanna": "I want to",
            "gonna": "going to",
            "wanna": "want to",
            "gotta": "got to",
            "lemme": "let me",
            "gimme": "give me",
            "dunno": "don't know",
            "kinda": "kind of",
            "sorta": "sort of",
        }

        text_lower = text.lower()
        for wrong, right in corrections.items():
            text_lower = text_lower.replace(wrong, right)

        # Capitalize first letter
        if text_lower:
            text = text_lower[0].upper() + text_lower[1:]

        # Add period if no ending punctuation
        if text and text[-1] not in ".?!":
            # Detect if it's a question
            question_starters = [
                "what", "how", "why", "when", "where", "who", "which",
                "can", "could", "would", "should", "is", "are", "do", "does",
            ]
            first_word = text.split()[0].lower() if text.split() else ""
            if first_word in question_starters:
                text += "?"
            else:
                text += "."

        return text

    def _clean_for_speech(self, text: str, tier: str) -> str:
        """Clean text for natural speech synthesis."""
        import re

        # Remove markdown formatting
        text = re.sub(r"```[\s\S]*?```", " (see the code on screen) ", text)
        text = re.sub(r"`([^`]+)`", r"\1", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        text = re.sub(r"#{1,6}\s+", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

        # Remove technical artifacts
        text = re.sub(r"SAFETY_FLAG:\w+:\w+", "", text)
        text = re.sub(r"\[DEMO MODE\]", "", text)

        # Clean up whitespace
        text = re.sub(r"\n+", ". ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        # Tier-specific adjustments
        if tier == "magic_workshop":
            # Simplify for young kids
            text = text.replace("function", "spell recipe")
            text = text.replace("variable", "magic box")
            text = text.replace("loop", "repeat charm")
            text = text.replace("debug", "find the gremlin")
            text = text.replace("error", "oopsie")
            text = text.replace("execute", "cast")
            text = text.replace("parameter", "ingredient")

        return text

    def create_gemini_live_config(self, tier: str) -> Dict[str, Any]:
        """
        Create configuration for a Gemini Live API session.
        
        This enables real-time bidirectional voice conversation
        with Professor Sparkle using Google's Gemini Live API.
        """
        config = VOICE_CONFIGS.get(tier, VOICE_CONFIGS["innovation_lab"])

        # System instruction based on tier
        system_instructions = {
            "magic_workshop": (
                "You are Professor Sparkle, a magical coding wizard talking to a "
                "child aged 5-7. Speak simply, warmly, and with excitement. "
                "Use magical words like 'spell', 'wizard', 'magic'. "
                "Keep sentences very short. Ask lots of questions. "
                "Celebrate everything they say."
            ),
            "innovation_lab": (
                "You are Professor Sparkle, a coding mentor talking to a child "
                "aged 8-12. Be encouraging and curious. Use real-world analogies. "
                "Ask Socratic questions. Never give complete answers — guide them "
                "to discover the answer themselves."
            ),
            "professional_studio": (
                "You are Professor Sparkle, a senior developer mentor talking to "
                "a teen aged 13-18. Be professional but approachable. Discuss "
                "trade-offs and design decisions. Push them to think critically. "
                "Reference real industry practices."
            ),
        }

        return {
            "model": "gemini-2.0-flash-exp",
            "generation_config": {
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {
                            "voice_name": "Aoede",  # Warm, friendly voice
                        }
                    }
                },
            },
            "system_instruction": system_instructions.get(
                tier, system_instructions["innovation_lab"]
            ),
            "tools": [
                {"google_search": {}},  # Allow searching for coding references
            ],
        }


def register_voice_routes(agent_bp, socketio=None):
    """Register voice-related routes on the agent blueprint."""
    voice_bridge = VoiceBridge()

    @agent_bp.route("/voice/config/<tier>", methods=["GET"])
    def voice_config(tier):
        """Get voice configuration for a tier."""
        config = voice_bridge.get_voice_config(tier)
        return json.dumps(config), 200, {"Content-Type": "application/json"}

    @agent_bp.route("/voice/prepare-speech", methods=["POST"])
    def prepare_speech():
        """Prepare text for speech synthesis."""
        data = json.loads(request.data) if request.data else {}
        text = data.get("text", "")
        tier = data.get("tier", "innovation_lab")
        is_question = data.get("is_question", False)

        result = voice_bridge.prepare_speech_output(text, tier, is_question)
        return json.dumps(result), 200, {"Content-Type": "application/json"}

    @agent_bp.route("/voice/process-transcript", methods=["POST"])
    def process_transcript():
        """Post-process a speech-to-text transcript."""
        data = json.loads(request.data) if request.data else {}
        transcript = data.get("transcript", "")
        tier = data.get("tier", "innovation_lab")

        cleaned = voice_bridge.process_speech_input(transcript, tier)
        return json.dumps({"cleaned_text": cleaned}), 200, {"Content-Type": "application/json"}

    @agent_bp.route("/voice/gemini-config/<tier>", methods=["GET"])
    def gemini_config(tier):
        """Get Gemini Live API configuration for a tier."""
        config = voice_bridge.create_gemini_live_config(tier)
        return json.dumps(config), 200, {"Content-Type": "application/json"}

    # Socket.IO voice events
    if socketio:
        @socketio.on("voice_start", namespace="/agents")
        def handle_voice_start(data):
            """Student started speaking."""
            session_id = data.get("session_id")
            emit("voice_status", {"status": "listening", "session_id": session_id})

        @socketio.on("voice_transcript", namespace="/agents")
        def handle_voice_transcript(data):
            """Received a speech-to-text transcript from the frontend."""
            transcript = data.get("transcript", "")
            tier = data.get("tier", "innovation_lab")
            cleaned = voice_bridge.process_speech_input(transcript, tier)
            emit("voice_cleaned", {"original": transcript, "cleaned": cleaned})

        @socketio.on("voice_end", namespace="/agents")
        def handle_voice_end(data):
            """Student stopped speaking."""
            emit("voice_status", {"status": "processing"})

    print("[Codopia Voice] Voice bridge routes registered")
    return voice_bridge
