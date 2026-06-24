"""
Spidey AI — Voice Output (Jarvis-like reliable speech)
Default: Jenny (US Female) — Edge TTS
"""
import os
import asyncio
import subprocess
import re
import time
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
    """Text-to-Speech — Jarvis-like reliable speech"""

    def __init__(self, engine="edge"):
        """Default engine = edge for better quality"""
        self.engine_name = "edge" if EDGE_TTS_AVAILABLE else "system"
        self.pyttsx3_engine = None
        self.rate = 175
        self.volume = 1.0
        self.voice_id = None
        # DEFAULT VOICE = Jenny (US Female)
        self.edge_voice = "en-US-JennyNeural"
        self.language = "en"

        if self.engine_name == "edge" and EDGE_TTS_AVAILABLE:
            app_logger.info(f"Edge TTS initialized — Voice: {self.edge_voice}")
        elif PYTTSX3_AVAILABLE:
            self._init_pyttsx3()
        else:
            app_logger.error("No TTS engine available!")

        # Also init pyttsx3 as backup
        if PYTTSX3_AVAILABLE and not self.pyttsx3_engine:
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', self.rate)
                self.pyttsx3_engine.setProperty('volume', self.volume)
            except Exception:
                pass

    def _init_pyttsx3(self):
        """Initialize pyttsx3"""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_engine.setProperty('rate', self.rate)
            self.pyttsx3_engine.setProperty('volume', self.volume)

            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if "zira" in voice.name.lower():
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        self.voice_id = voice.id
                        break

            self.engine_name = "system"
            app_logger.info("pyttsx3 TTS initialized")
        except Exception as e:
            log_error(str(e), "VoiceOutput._init_pyttsx3")
            self.pyttsx3_engine = None

    def speak(self, text):
        """
        ALWAYS speak — tries edge first, then pyttsx3 as backup
        Returns True if spoken successfully
        """
        if not text or not text.strip():
            return False

        clean_text = self._clean_for_speech(text)
        if not clean_text or len(clean_text.strip()) < 2:
            return False

        # Try primary engine
        success = False

        try:
            if self.engine_name == "edge" and EDGE_TTS_AVAILABLE:
                success = self._speak_edge(clean_text)
            elif self.pyttsx3_engine:
                success = self._speak_pyttsx3(clean_text)
        except Exception as e:
            log_error(str(e), "VoiceOutput.speak primary")

        # Fallback if primary failed
        if not success:
            success = self._fallback_speak(clean_text)

        return success

    def _fallback_speak(self, text):
        """Try alternate engine"""
        try:
            if self.engine_name == "edge" and self.pyttsx3_engine:
                return self._speak_pyttsx3(text)
            elif self.engine_name == "system" and EDGE_TTS_AVAILABLE:
                return self._speak_edge(text)
        except Exception as e:
            log_error(str(e), "VoiceOutput._fallback_speak")
        return False

    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3"""
        try:
            if not self.pyttsx3_engine:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', self.rate)
                self.pyttsx3_engine.setProperty('volume', self.volume)

            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
            return True

        except RuntimeError:
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', self.rate)
                self.pyttsx3_engine.setProperty('volume', self.volume)
                self.pyttsx3_engine.say(text)
                self.pyttsx3_engine.runAndWait()
                return True
            except Exception as e:
                log_error(str(e), "VoiceOutput._speak_pyttsx3 retry")
                return False
        except Exception as e:
            log_error(str(e), "VoiceOutput._speak_pyttsx3")
            return False

    def _speak_edge(self, text):
        """Speak using edge-tts"""
        try:
            temp_file = os.path.join(AUDIO_DIR, f"tts_{int(time.time())}.mp3")

            # Generate speech
            try:
                asyncio.run(self._edge_generate(text, temp_file))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._edge_generate(text, temp_file))
                loop.close()

            # Play
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 100:
                self._play_audio(temp_file)
                time.sleep(0.3)
                try:
                    os.remove(temp_file)
                except Exception:
                    pass
                return True
            else:
                log_error("Edge TTS file empty or not created", "_speak_edge")
                return False

        except Exception as e:
            log_error(str(e), "VoiceOutput._speak_edge")
            return False

    async def _edge_generate(self, text, output_file):
        """Generate speech with edge-tts"""
        communicate = edge_tts.Communicate(text, self.edge_voice)
        await communicate.save(output_file)

    def _play_audio(self, filepath):
        """Play audio using ffplay"""
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filepath],
                timeout=120
            )
        except FileNotFoundError:
            try:
                os.startfile(filepath)
                time.sleep(5)
            except Exception as e:
                log_error(str(e), "_play_audio startfile")
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            log_error(str(e), "_play_audio")

    def _clean_for_speech(self, text):
        """Clean text for speech"""
        text = re.sub(r'[🕷️🎤📝✅❌🔍💬🧠📊⭐🗑️📂📄🤖💡⚙️🌡️📏🔢📨👤🕸️📋🔄⚠️🔧💻🌐📅🎉🏆🔥💪💰🆓🔑📁🛠️🎮🟢🔴🔊👋]', '', text)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'`+', '', text)
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def set_rate(self, rate):
        self.rate = rate
        if self.pyttsx3_engine:
            self.pyttsx3_engine.setProperty('rate', rate)

    def set_volume(self, volume):
        self.volume = volume
        if self.pyttsx3_engine:
            self.pyttsx3_engine.setProperty('volume', volume)

    def set_edge_voice(self, voice_id):
        self.edge_voice = voice_id
        if "ur-PK" in voice_id:
            self.language = "ur"
        elif "hi-IN" in voice_id:
            self.language = "hi"
        else:
            self.language = "en"

    def set_language(self, lang):
        self.language = lang
        voice_map = {
            "en": "en-US-JennyNeural",
            "en-male": "en-US-GuyNeural",
            "en-uk": "en-GB-RyanNeural",
            "ur": "ur-PK-AsadNeural",
            "ur-female": "ur-PK-UzmaNeural",
            "hi": "hi-IN-MadhurNeural",
            "hi-female": "hi-IN-SwaraNeural",
            "ar": "ar-SA-HamedNeural",
        }
        if lang in voice_map:
            self.edge_voice = voice_map[lang]
            self.engine_name = "edge"
            return True
        return False

    def get_voices(self):
        voices = []
        if self.pyttsx3_engine:
            for v in self.pyttsx3_engine.getProperty('voices'):
                voices.append({"id": v.id, "name": v.name, "engine": "system", "language": "en"})
        if EDGE_TTS_AVAILABLE:
            voices.extend([
                {"id": "en-US-JennyNeural", "name": "Jenny (US Female) ⭐DEFAULT", "engine": "edge", "language": "en"},
                {"id": "en-US-GuyNeural", "name": "Guy (US Male)", "engine": "edge", "language": "en"},
                {"id": "en-US-AriaNeural", "name": "Aria (US Female)", "engine": "edge", "language": "en"},
                {"id": "en-GB-RyanNeural", "name": "Ryan (UK Male)", "engine": "edge", "language": "en"},
                {"id": "en-GB-SoniaNeural", "name": "Sonia (UK Female)", "engine": "edge", "language": "en"},
                {"id": "ur-PK-AsadNeural", "name": "Asad (Urdu Male)", "engine": "edge", "language": "ur"},
                {"id": "ur-PK-UzmaNeural", "name": "Uzma (Urdu Female)", "engine": "edge", "language": "ur"},
                {"id": "hi-IN-MadhurNeural", "name": "Madhur (Hindi Male)", "engine": "edge", "language": "hi"},
                {"id": "hi-IN-SwaraNeural", "name": "Swara (Hindi Female)", "engine": "edge", "language": "hi"},
            ])
        return voices

    def set_voice(self, voice_id):
        self.voice_id = voice_id
        if "Neural" in voice_id:
            self.edge_voice = voice_id
            self.engine_name = "edge"
        elif self.pyttsx3_engine:
            try:
                self.pyttsx3_engine.setProperty('voice', voice_id)
            except Exception:
                pass

    def switch_engine(self, engine):
        if engine == "system" and PYTTSX3_AVAILABLE:
            self._init_pyttsx3()
            return True
        elif engine == "edge" and EDGE_TTS_AVAILABLE:
            self.engine_name = "edge"
            return True
        return False

    def get_engine_name(self):
        return self.engine_name

    def get_current_voice(self):
        return {
            "engine": self.engine_name,
            "voice": self.edge_voice if self.engine_name == "edge" else self.voice_id,
            "language": self.language,
            "rate": self.rate
        }

    def is_available(self):
        if self.engine_name == "system":
            return self.pyttsx3_engine is not None
        elif self.engine_name == "edge":
            return EDGE_TTS_AVAILABLE
        return False