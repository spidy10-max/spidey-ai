"""
Spidey AI — Speech-to-Text Transcriber
Handles torch/whisper blocked by Windows
"""
import os
from spidey.logger import app_logger, log_event, log_error

WHISPER_AVAILABLE = False
WHISPER_TYPE = None

try:
    import whisper
    WHISPER_AVAILABLE = True
    WHISPER_TYPE = "openai"
except (ImportError, OSError) as e:
    app_logger.warning(f"Whisper not available: {e}")
    try:
        from faster_whisper import WhisperModel
        WHISPER_AVAILABLE = True
        WHISPER_TYPE = "faster"
    except (ImportError, OSError):
        WHISPER_AVAILABLE = False
        WHISPER_TYPE = None


class Transcriber:
    """Speech to text — handles blocked torch gracefully"""

    def __init__(self, model_size="small"):
        self.model_size = model_size
        self.model = None
        self.use_faster = False

        if not WHISPER_AVAILABLE:
            app_logger.warning("Whisper not available (torch blocked by Windows policy)")
            print("   ⚠️ Voice input disabled (Windows blocked torch)")
            print("   💡 Voice output (TTS) still works!")
            return

        try:
            if WHISPER_TYPE == "openai":
                import whisper
                print(f"   📥 Loading Whisper '{model_size}'...")
                self.model = whisper.load_model(model_size)
                print(f"   ✅ Whisper loaded!")
                app_logger.info(f"Whisper loaded: {model_size}")

            elif WHISPER_TYPE == "faster":
                from faster_whisper import WhisperModel
                print(f"   📥 Loading Faster-Whisper '{model_size}'...")
                self.model = WhisperModel(model_size, compute_type="int8")
                self.use_faster = True
                print(f"   ✅ Faster-Whisper loaded!")

        except (OSError, Exception) as e:
            log_error(str(e), "Transcriber.__init__")
            print(f"   ⚠️ Whisper failed: {e}")
            self.model = None

    def transcribe(self, audio_path, language=None):
        if not self.model:
            return {"text": "", "language": "unknown", "success": False}

        if not os.path.exists(audio_path):
            return {"text": "", "language": "unknown", "success": False}

        try:
            print("   🔄 Transcribing...")

            if self.use_faster:
                segments, info = self.model.transcribe(audio_path, language=language, beam_size=5)
                text = " ".join([seg.text for seg in segments]).strip()
                detected_lang = info.language
            else:
                options = {}
                if language:
                    options["language"] = language
                result = self.model.transcribe(audio_path, **options)
                text = result["text"].strip()
                detected_lang = result.get("language", "unknown")

            log_event("Transcription", f"Language: {detected_lang}")
            return {"text": text, "language": detected_lang, "success": True}

        except Exception as e:
            log_error(str(e), "Transcriber.transcribe")
            return {"text": "", "language": "unknown", "success": False}

    def is_available(self):
        return self.model is not None