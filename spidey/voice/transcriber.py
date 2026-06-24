"""
Spidey AI — Speech-to-Text Transcriber
Uses Whisper to convert audio to text
"""
import os
from spidey.logger import app_logger, log_event, log_error

try:
    import whisper
    WHISPER_AVAILABLE = True
    WHISPER_TYPE = "openai"
except ImportError:
    try:
        from faster_whisper import WhisperModel
        WHISPER_AVAILABLE = True
        WHISPER_TYPE = "faster"
    except ImportError:
        WHISPER_AVAILABLE = False
        WHISPER_TYPE = None


class Transcriber:
    """Converts speech audio to text using Whisper"""

    def __init__(self, model_size="base"):
        """
        Initialize Whisper

        model_size: tiny, base, small, medium, large
            - tiny: Fastest (39MB)
            - base: Good balance (74MB)
            - small: Better accuracy (244MB)
        """
        self.model_size = model_size
        self.model = None
        self.use_faster = False

        if not WHISPER_AVAILABLE:
            app_logger.error("No whisper library available!")
            return

        try:
            if WHISPER_TYPE == "openai":
                import whisper
                print(f"   📥 Loading Whisper '{model_size}' model...")
                print(f"   ⏳ First time will download. Please wait...")
                self.model = whisper.load_model(model_size)
                print(f"   ✅ Whisper '{model_size}' model loaded!")
                app_logger.info(f"Whisper model loaded: {model_size}")

            elif WHISPER_TYPE == "faster":
                from faster_whisper import WhisperModel
                print(f"   📥 Loading Faster-Whisper '{model_size}' model...")
                self.model = WhisperModel(model_size, compute_type="int8")
                self.use_faster = True
                print(f"   ✅ Faster-Whisper '{model_size}' model loaded!")
                app_logger.info(f"Faster-Whisper model loaded: {model_size}")

        except Exception as e:
            log_error(str(e), "Transcriber.__init__")
            print(f"   ❌ Could not load whisper model: {e}")

    def transcribe(self, audio_path, language=None):
        """
        Transcribe audio file to text

        Args:
            audio_path: Path to .wav file
            language: 'en', 'ur', etc. or None for auto

        Returns:
            Dict with text, language, success
        """
        if not self.model:
            return {
                "text": "Error: Whisper model not loaded",
                "language": "unknown",
                "success": False
            }

        if not os.path.exists(audio_path):
            return {
                "text": f"Error: File not found: {audio_path}",
                "language": "unknown",
                "success": False
            }

        try:
            print("   🔄 Transcribing...")

            if self.use_faster:
                segments, info = self.model.transcribe(
                    audio_path,
                    language=language,
                    beam_size=5
                )
                text = " ".join([seg.text for seg in segments]).strip()
                detected_lang = info.language

            else:
                options = {}
                if language:
                    options["language"] = language

                result = self.model.transcribe(audio_path, **options)
                text = result["text"].strip()
                detected_lang = result.get("language", "unknown")

            log_event("Transcription done", f"Language: {detected_lang}")

            return {
                "text": text,
                "language": detected_lang,
                "success": True
            }

        except Exception as e:
            log_error(str(e), "Transcriber.transcribe")
            return {
                "text": f"Error: {str(e)}",
                "language": "unknown",
                "success": False
            }

    def is_available(self):
        """Check if Whisper is available"""
        return self.model is not None