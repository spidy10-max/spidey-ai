"""
Spidey AI — Voice Input System
Complete pipeline: Mic → Record → Transcribe → Text
"""
from spidey.voice.recorder import AudioRecorder
from spidey.voice.transcriber import Transcriber
from spidey.logger import app_logger, log_event, log_error
import os


class VoiceInput:
    """
    Complete voice input system

    Records audio from mic and converts to text
    Three recording modes:
    1. Fixed duration (e.g., 5 seconds)
    2. Press Enter to stop
    3. Auto-stop on silence
    """

    def __init__(self, whisper_model="base"):
        """
        Initialize voice input

        Args:
            whisper_model: tiny, base, small, medium
        """
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber(model_size=whisper_model)
        self.last_audio_path = None
        self.last_transcription = None

        if self.transcriber.is_available():
            app_logger.info("VoiceInput ready")
        else:
            app_logger.warning("VoiceInput: Whisper not available")

    def listen_fixed(self, duration=5, language=None):
        """
        Listen for fixed duration

        Args:
            duration: Seconds to record
            language: 'en', 'ur', etc. or None for auto

        Returns:
            Transcribed text or None
        """
        # Record
        filepath = self.recorder.record_fixed(duration=duration)
        if not filepath:
            return None

        # Transcribe
        text = self._transcribe_and_cleanup(filepath, language)
        return text

    def listen_until_enter(self, language=None):
        """
        Listen until user presses Enter

        Args:
            language: Language code or None

        Returns:
            Transcribed text or None
        """
        filepath = self.recorder.record_until_enter()
        if not filepath:
            return None

        text = self._transcribe_and_cleanup(filepath, language)
        return text

    def listen_auto(self, max_duration=30, silence_seconds=2.0, language=None):
        """
        Listen and auto-stop on silence

        Args:
            max_duration: Max recording time
            silence_seconds: Silence before auto-stop
            language: Language code or None

        Returns:
            Transcribed text or None
        """
        filepath = self.recorder.record_with_silence_detection(
            max_duration=max_duration,
            silence_threshold=0.01,
            silence_duration=silence_seconds
        )
        if not filepath:
            return None

        text = self._transcribe_and_cleanup(filepath, language)
        return text

    def listen(self, mode="fixed", duration=5, language=None):
        """
        Universal listen method

        Args:
            mode: 'fixed', 'enter', 'auto'
            duration: For fixed mode
            language: Language code or None

        Returns:
            Transcribed text or None
        """
        if mode == "fixed":
            return self.listen_fixed(duration=duration, language=language)
        elif mode == "enter":
            return self.listen_until_enter(language=language)
        elif mode == "auto":
            return self.listen_auto(language=language)
        else:
            print(f"   ❌ Unknown mode: {mode}")
            return None

    def _transcribe_and_cleanup(self, filepath, language=None):
        """
        Transcribe audio file and cleanup

        Args:
            filepath: Path to audio file
            language: Language code

        Returns:
            Transcribed text or None
        """
        if not filepath or not os.path.exists(filepath):
            return None

        self.last_audio_path = filepath

        # Transcribe
        result = self.transcriber.transcribe(filepath, language=language)
        self.last_transcription = result

        # Cleanup audio file
        try:
            os.remove(filepath)
        except Exception:
            pass

        if result["success"] and result["text"]:
            text = result["text"].strip()
            if text:
                log_event("Voice input", f"[{result['language']}] {text[:50]}")
                print(f"   📝 You said: \"{text}\"")
                print(f"   🌍 Language: {result['language']}")
                return text

        print("   ❌ Could not understand audio.")
        return None

    def test_mic(self):
        """Test microphone"""
        return self.recorder.test_microphone()

    def list_mics(self):
        """List microphones"""
        return self.recorder.list_microphones()

    def is_available(self):
        """Check if voice input is ready"""
        return self.transcriber.is_available()

    def get_last_result(self):
        """Get last transcription result"""
        return self.last_transcription