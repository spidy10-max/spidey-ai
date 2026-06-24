"""
Spidey AI — Voice Manager
Manages complete voice conversation:
Voice Input (mic → text) + Voice Output (text → speech)
"""
from spidey.voice.voice_input import VoiceInput
from spidey.voice.voice_output import VoiceOutput
from spidey.logger import app_logger, log_event, log_error


class VoiceManager:
    """
    Complete voice system manager

    Handles:
    - Voice input (listen → transcribe)
    - Voice output (speak response)
    - Voice mode toggle
    - TTS engine switching
    """

    def __init__(self, whisper_model="base", tts_engine="system"):
        """
        Initialize voice manager

        Args:
            whisper_model: tiny, base, small
            tts_engine: 'system' or 'edge'
        """
        self.voice_enabled = False
        self.speak_enabled = False
        self.listen_mode = "fixed"  # fixed, enter, auto
        self.listen_duration = 5

        # Voice Input
        self.voice_input = None
        try:
            self.voice_input = VoiceInput(whisper_model=whisper_model)
            if self.voice_input.is_available():
                app_logger.info("Voice input ready")
            else:
                app_logger.warning("Voice input not available")
                self.voice_input = None
        except Exception as e:
            log_error(str(e), "VoiceManager - voice input")
            self.voice_input = None

        # Voice Output
        self.voice_output = None
        try:
            self.voice_output = VoiceOutput(engine=tts_engine)
            if self.voice_output.is_available():
                app_logger.info("Voice output ready")
            else:
                app_logger.warning("Voice output not available")
                self.voice_output = None
        except Exception as e:
            log_error(str(e), "VoiceManager - voice output")
            self.voice_output = None

        app_logger.info("VoiceManager initialized")

    def listen(self, mode=None, duration=None):
        """
        Listen for voice input

        Args:
            mode: 'fixed', 'enter', 'auto' (None = use default)
            duration: Seconds for fixed mode

        Returns:
            Transcribed text or None
        """
        if not self.voice_input or not self.voice_input.is_available():
            print("   ❌ Voice input not available!")
            return None

        use_mode = mode or self.listen_mode
        use_duration = duration or self.listen_duration

        return self.voice_input.listen(
            mode=use_mode,
            duration=use_duration
        )

    def speak(self, text):
        """
        Speak text aloud

        Args:
            text: Text to speak
        """
        if not self.voice_output or not self.voice_output.is_available():
            return

        if not text or not text.strip():
            return

        try:
            self.voice_output.speak(text)
        except Exception as e:
            log_error(str(e), "VoiceManager.speak")

    def voice_chat(self, brain, mode=None, duration=None):
        """
        Complete voice conversation turn:
        Listen → Transcribe → Send to AI → Speak response

        Args:
            brain: SpideyBrain instance
            mode: Listen mode
            duration: Listen duration

        Returns:
            Tuple of (user_text, ai_response) or (None, None)
        """
        # Listen
        user_text = self.listen(mode=mode, duration=duration)
        if not user_text:
            return None, None

        # Send to AI
        print()
        print("🕷️ Spidey: ", end="", flush=True)
        ai_response = brain.chat(user_text)
        print(ai_response)
        print()

        # Speak response
        if self.speak_enabled:
            self.speak(ai_response)

        return user_text, ai_response

    def toggle_speak(self):
        """Toggle speak mode on/off"""
        self.speak_enabled = not self.speak_enabled
        status = "ON" if self.speak_enabled else "OFF"
        log_event("Speak mode", status)
        return self.speak_enabled

    def toggle_voice(self):
        """Toggle full voice mode on/off"""
        self.voice_enabled = not self.voice_enabled
        status = "ON" if self.voice_enabled else "OFF"
        log_event("Voice mode", status)
        return self.voice_enabled

    def set_listen_mode(self, mode):
        """Set default listen mode"""
        if mode in ["fixed", "enter", "auto"]:
            self.listen_mode = mode
            return True
        return False

    def set_listen_duration(self, seconds):
        """Set default listen duration"""
        if 1 <= seconds <= 60:
            self.listen_duration = seconds
            return True
        return False

    def switch_tts_engine(self, engine):
        """Switch TTS engine"""
        if self.voice_output:
            return self.voice_output.switch_engine(engine)
        return False

    def set_edge_voice(self, voice_id):
        """Set edge voice"""
        if self.voice_output:
            self.voice_output.set_edge_voice(voice_id)

    def set_speech_rate(self, rate):
        """Set speech speed"""
        if self.voice_output:
            self.voice_output.set_rate(rate)

    def test_mic(self):
        """Test microphone"""
        if self.voice_input:
            return self.voice_input.test_mic()
        print("   ❌ Voice input not available!")
        return False

    def test_speak(self, text="Hello! I am Spidey AI!"):
        """Test speech output"""
        if self.voice_output and self.voice_output.is_available():
            self.voice_output.speak(text)
            return True
        print("   ❌ Voice output not available!")
        return False

    def get_voices(self):
        """Get available voices"""
        if self.voice_output:
            return self.voice_output.get_voices()
        return []

    def get_mics(self):
        """Get available microphones"""
        if self.voice_input:
            return self.voice_input.list_mics()
        return []

    def get_status(self):
        """Get voice system status"""
        return {
            "voice_input": self.voice_input is not None and self.voice_input.is_available(),
            "voice_output": self.voice_output is not None and self.voice_output.is_available(),
            "voice_enabled": self.voice_enabled,
            "speak_enabled": self.speak_enabled,
            "listen_mode": self.listen_mode,
            "listen_duration": self.listen_duration,
            "tts_engine": self.voice_output.get_engine_name() if self.voice_output else "none"
        }

    def is_input_available(self):
        """Check voice input"""
        return self.voice_input is not None and self.voice_input.is_available()

    def is_output_available(self):
        """Check voice output"""
        return self.voice_output is not None and self.voice_output.is_available()