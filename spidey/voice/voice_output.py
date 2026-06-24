"""
Spidey AI — Voice Output (Wake Word Interruptible!)
Says "Spidey" → Stops speaking → Listens to you
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
    """Text-to-Speech with background play support"""

    def __init__(self, engine="edge"):
        self.engine_name = "edge" if EDGE_TTS_AVAILABLE else "system"
        self.pyttsx3_engine = None
        self.rate = 175
        self.volume = 1.0
        self.voice_id = None
        self.edge_voice = "en-US-JennyNeural"
        self.language = "en"
        self._current_process = None

        if self.engine_name == "edge":
            app_logger.info(f"Edge TTS — Voice: {self.edge_voice}")

        if PYTTSX3_AVAILABLE:
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', self.rate)
                self.pyttsx3_engine.setProperty('volume', self.volume)
            except Exception:
                pass

    def speak(self, text):
        """Speak FULL text — blocking (waits till done)"""
        if not text or not text.strip():
            return False

        clean_text = self._clean_for_speech(text)
        if not clean_text or len(clean_text.strip()) < 2:
            return False

        for attempt in range(2):
            try:
                if self.engine_name == "edge" and EDGE_TTS_AVAILABLE:
                    if self._speak_edge(clean_text):
                        return True
                elif self.pyttsx3_engine:
                    if self._speak_pyttsx3(clean_text):
                        return True
            except Exception as e:
                log_error(str(e), f"speak attempt {attempt+1}")
            time.sleep(0.3)

        return self._fallback_speak(clean_text)

    def speak_background(self, text):
        """
        Start speaking in BACKGROUND — returns immediately!
        Audio plays while you can do other things.
        Use is_speaking() to check if still playing.
        Use stop() to kill audio.
        """
        if not text or not text.strip():
            return False

        clean_text = self._clean_for_speech(text)
        if not clean_text or len(clean_text.strip()) < 2:
            return False

        try:
            if self.engine_name == "edge" and EDGE_TTS_AVAILABLE:
                return self._speak_edge_background(clean_text)
            elif self.pyttsx3_engine:
                # pyttsx3 doesn't support background well, use blocking
                self._speak_pyttsx3(clean_text)
                return True
        except Exception as e:
            log_error(str(e), "speak_background")

        return False

    def _speak_edge_background(self, text):
        """Generate audio and play in background"""
        try:
            temp_file = os.path.join(AUDIO_DIR, f"tts_{int(time.time() * 1000)}.mp3")

            # Generate audio file
            try:
                asyncio.run(self._edge_generate(text, temp_file))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._edge_generate(text, temp_file))
                loop.close()

            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 100:
                # Start playing in BACKGROUND (non-blocking!)
                self._current_process = subprocess.Popen(
                    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_file]
                )
                # Store temp file path for cleanup
                self._current_temp_file = temp_file
                return True

            return False
        except Exception as e:
            log_error(str(e), "_speak_edge_background")
            return False

    def is_speaking(self):
        """Check if audio is still playing"""
        if self._current_process:
            return self._current_process.poll() is None
        return False

    def stop(self):
        """Stop current speech IMMEDIATELY"""
        if self._current_process:
            try:
                self._current_process.kill()
                self._current_process.wait(timeout=2)
            except Exception:
                pass
            self._current_process = None

        # Cleanup temp file
        if hasattr(self, '_current_temp_file') and self._current_temp_file:
            time.sleep(0.3)
            try:
                if os.path.exists(self._current_temp_file):
                    os.remove(self._current_temp_file)
            except Exception:
                pass
            self._current_temp_file = None

        # Stop pyttsx3
        if self.pyttsx3_engine:
            try:
                self.pyttsx3_engine.stop()
            except Exception:
                pass

    def wait_until_done(self):
        """Wait until speech finishes, then cleanup"""
        if self._current_process:
            try:
                self._current_process.wait(timeout=120)
            except subprocess.TimeoutExpired:
                self._current_process.kill()
            except Exception:
                pass
            self._current_process = None

        # Cleanup temp file
        if hasattr(self, '_current_temp_file') and self._current_temp_file:
            time.sleep(0.3)
            try:
                if os.path.exists(self._current_temp_file):
                    os.remove(self._current_temp_file)
            except Exception:
                pass
            self._current_temp_file = None

    def _fallback_speak(self, text):
        try:
            if self.engine_name == "edge" and self.pyttsx3_engine:
                return self._speak_pyttsx3(text)
            elif self.engine_name == "system" and EDGE_TTS_AVAILABLE:
                return self._speak_edge(text)
        except Exception:
            pass
        return False

    def _speak_pyttsx3(self, text):
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
            except Exception:
                return False
        except Exception:
            return False

    def _speak_edge(self, text):
        """Blocking edge speech"""
        try:
            temp_file = os.path.join(AUDIO_DIR, f"tts_{int(time.time() * 1000)}.mp3")

            try:
                asyncio.run(self._edge_generate(text, temp_file))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._edge_generate(text, temp_file))
                loop.close()

            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 100:
                self._current_process = subprocess.Popen(
                    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_file]
                )
                self._current_temp_file = temp_file
                self.wait_until_done()
                return True
            return False
        except Exception as e:
            log_error(str(e), "_speak_edge")
            return False

    async def _edge_generate(self, text, output_file):
        communicate = edge_tts.Communicate(text, self.edge_voice)
        await communicate.save(output_file)

    def _clean_for_speech(self, text):
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
        if engine == "edge" and EDGE_TTS_AVAILABLE:
            self.engine_name = "edge"
            return True
        elif engine == "system" and PYTTSX3_AVAILABLE:
            self.engine_name = "system"
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
        if self.engine_name == "edge":
            return EDGE_TTS_AVAILABLE
        return self.pyttsx3_engine is not None