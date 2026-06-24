"""
🎤 Spidey Voice Module

Contains:
- recorder.py      — Record audio from microphone
- transcriber.py   — Convert speech to text (Whisper)
- voice_input.py   — Complete voice input pipeline
- voice_output.py  — Text-to-speech output (Edge TTS)
- voice_manager.py — Full voice conversation manager

Voice Commands (in Spidey Beta):
- "speak urdu"    → Switch to Urdu
- "speak english" → Switch to English
- "speak hindi"   → Switch to Hindi
- "speak faster"  → Faster speech
- "speak slower"  → Slower speech
- "stop"          → Exit Spidey Beta
"""

from spidey.voice.voice_manager import VoiceManager

__all__ = ["VoiceManager"]