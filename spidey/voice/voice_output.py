"""
Spidey AI — Voice Output (Text-to-Speech)
Makes Spidey SPEAK!
"""
import os
import asyncio
import subprocess
import re
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


AUDIO_DIR = os.path.join(DATA_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

PYTTSX3_AVAILABLE = False
EDGE_TTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    pass

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    pass


class VoiceOutput:
    """Text-to-Speech system for Spidey AI"""

    def __init__(self, engine="system"):
        self.engine_name = engine
        self.pyttsx3_engine = None
        self.rate = 175
        self.volume = 1.0
        self.voice_id = None
        self.edge_voice = "en-US-GuyNeural"

        if engine == "system" and PYTTSX3_AVAILABLE:
            self._init_pyttsx3()
        elif engine == "edge" and EDGE_TTS_AVAILABLE:
            self.engine_name = "edge"
            app_logger.info("Edge TTS initialized")
        elif PYTTSX3_AVAILABLE:
            self._init_pyttsx3()
        elif EDGE_TTS_AVAILABLE:
            self.engine_name = "edge"
            app_logger.info("Fallback to Edge TTS")
        else:
            app_logger.error("No TTS engine available!")

    def _init_pyttsx3(self):
        """Initialize pyttsx3"""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_engine.setProperty('rate', self.rate)
            self.pyttsx3_engine.setProperty('volume', self.volume)

            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if "english" in voice.name.lower() or "en" in voice.id.lower():
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        self.voice_id = voice.id
                        break

            self.engine_name = "system"
            app_logger.info("pyttsx3 TTS initialized")

        except Exception as e:
            log_error(str(e), "VoiceOutput._init_pyttsx3")
            self.pyttsx3_engine = None

    def speak(self, text):
        """Speak the given text"""
        if not text or not text.strip():
            return

        clean_text = self._clean_for_speech(text)

        try:
            if self.engine_name == "system" and self.pyttsx3_engine:
                self._speak_pyttsx3(clean_text)

            elif self.engine_name == "edge" and EDGE_TTS_AVAILABLE:
                self._speak_edge(clean_text)

            else:
                print("   ❌ No TTS engine available!")

        except Exception as e:
            log_error(str(e), "VoiceOutput.speak")
            print(f"   ❌ Speech error: {e}")

    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3"""
        try:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
        except Exception as e:
            log_error(str(e), "VoiceOutput._speak_pyttsx3")

    def _speak_edge(self, text):
        """Speak using edge-tts"""
        try:
            temp_file = os.path.join(AUDIO_DIR, "tts_output.mp3")

            asyncio.run(self._edge_generate(text, temp_file))

            if os.path.exists(temp_file):
                self._play_audio(temp_file)
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

        except Exception as e:
            log_error(str(e), "VoiceOutput._speak_edge")

    async def _edge_generate(self, text, output_file):
        """Generate speech with edge-tts"""
        try:
            communicate = edge_tts.Communicate(text, self.edge_voice)
            await communicate.save(output_file)
        except Exception as e:
            log_error(str(e), "VoiceOutput._edge_generate")

    def _play_audio(self, filepath):
        """Play audio file using ffplay"""
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filepath],
                check=True
            )
        except FileNotFoundError:
            # ffplay not found, try start command
            try:
                os.startfile(filepath)
                import time
                time.sleep(3)
            except Exception as e:
                log_error(str(e), "VoiceOutput._play_audio")
        except Exception as e:
            log_error(str(e), "VoiceOutput._play_audio")

    def _clean_for_speech(self, text):
        """Clean text for better speech"""
        text = re.sub(r'[🕷️🎤📝✅❌🔍💬🧠📊⭐🗑️📂📄🤖💡⚙️🌡️📏🔢📨👤🕸️📋🔄⚠️🔧💻🌐📅🎉🏆🔥💪💰🆓🔑📁🛠️🎮]', '', text)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'`+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def set_rate(self, rate):
        """Set speech speed"""
        self.rate = rate
        if self.pyttsx3_engine:
            self.pyttsx3_engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """Set volume"""
        self.volume = volume
        if self.pyttsx3_engine:
            self.pyttsx3_engine.setProperty('volume', volume)

    def set_edge_voice(self, voice_id):
        """Set edge voice"""
        self.edge_voice = voice_id

    def get_voices(self):
        """Get available voices"""
        voices = []

        if self.engine_name == "system" and self.pyttsx3_engine:
            system_voices = self.pyttsx3_engine.getProperty('voices')
            for v in system_voices:
                voices.append({
                    "id": v.id,
                    "name": v.name,
                    "engine": "system"
                })

        if EDGE_TTS_AVAILABLE:
            edge_voices = [
                {"id": "en-US-GuyNeural", "name": "Guy (US Male)", "engine": "edge"},
                {"id": "en-US-JennyNeural", "name": "Jenny (US Female)", "engine": "edge"},
                {"id": "en-US-AriaNeural", "name": "Aria (US Female)", "engine": "edge"},
                {"id": "en-GB-RyanNeural", "name": "Ryan (UK Male)", "engine": "edge"},
                {"id": "en-GB-SoniaNeural", "name": "Sonia (UK Female)", "engine": "edge"},
                {"id": "ur-PK-AsadNeural", "name": "Asad (Urdu Male)", "engine": "edge"},
                {"id": "ur-PK-UzmaNeural", "name": "Uzma (Urdu Female)", "engine": "edge"},
            ]
            voices.extend(edge_voices)

        return voices

    def set_voice(self, voice_id):
        """Set voice by ID"""
        self.voice_id = voice_id
        if self.pyttsx3_engine:
            try:
                self.pyttsx3_engine.setProperty('voice', voice_id)
            except Exception:
                pass

    def switch_engine(self, engine):
        """Switch TTS engine"""
        if engine == "system" and PYTTSX3_AVAILABLE:
            self._init_pyttsx3()
            return True
        elif engine == "edge" and EDGE_TTS_AVAILABLE:
            self.engine_name = "edge"
            return True
        return False

    def get_engine_name(self):
        """Get current engine"""
        return self.engine_name

    def is_available(self):
        """Check if TTS is available"""
        if self.engine_name == "system":
            return self.pyttsx3_engine is not None
        elif self.engine_name == "edge":
            return EDGE_TTS_AVAILABLE
        return False