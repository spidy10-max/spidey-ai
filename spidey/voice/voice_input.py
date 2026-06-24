"""
Spidey AI — Voice Input System
Accurate speech recognition with language setting
"""
from spidey.voice.recorder import AudioRecorder
from spidey.voice.transcriber import Transcriber
from spidey.logger import app_logger, log_event, log_error
import os


class VoiceInput:
    """Voice input with language support"""

    def __init__(self, whisper_model="small"):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber(model_size=whisper_model)
        self.last_audio_path = None
        self.last_transcription = None

        if self.transcriber.is_available():
            app_logger.info("VoiceInput ready")
        else:
            app_logger.warning("VoiceInput: Whisper not available")

    def listen_fixed(self, duration=5, language=None):
        filepath = self.recorder.record_fixed(duration=duration)
        if not filepath:
            return None
        return self._transcribe_and_cleanup(filepath, language)

    def listen_until_enter(self, language=None):
        filepath = self.recorder.record_until_enter()
        if not filepath:
            return None
        return self._transcribe_and_cleanup(filepath, language)

    def listen_auto(self, max_duration=30, silence_seconds=2.0, language=None):
        filepath = self.recorder.record_with_silence_detection(
            max_duration=max_duration,
            silence_threshold=0.01,
            silence_duration=silence_seconds
        )
        if not filepath:
            return None
        return self._transcribe_and_cleanup(filepath, language)

    def listen(self, mode="fixed", duration=5, language=None):
        if mode == "fixed":
            return self.listen_fixed(duration=duration, language=language)
        elif mode == "enter":
            return self.listen_until_enter(language=language)
        elif mode == "auto":
            return self.listen_auto(language=language)
        else:
            return None

    def _transcribe_and_cleanup(self, filepath, language=None):
        if not filepath or not os.path.exists(filepath):
            return None

        self.last_audio_path = filepath

        result = self.transcriber.transcribe(filepath, language=language)
        self.last_transcription = result

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
        return self.recorder.test_microphone()

    def list_mics(self):
        return self.recorder.list_microphones()

    def is_available(self):
        return self.transcriber.is_available()

    def get_last_result(self):
        return self.last_transcription