"""
Spidey AI — Voice Manager (FAST + Ctrl+C Safe!)
"""
from spidey.voice.voice_input import VoiceInput
from spidey.voice.voice_output import VoiceOutput
from spidey.logger import app_logger, log_event, log_error
import time


class VoiceManager:

    def __init__(self, whisper_model="base", tts_engine="edge"):
        self.voice_enabled = False
        self.speak_enabled = False
        self.listen_mode = "auto"
        self.listen_duration = 5
        self.spidey_beta = False

        self.voice_input = None
        try:
            self.voice_input = VoiceInput(whisper_model=whisper_model)
            if not self.voice_input.is_available():
                self.voice_input = None
        except Exception as e:
            log_error(str(e), "VoiceManager - input")
            self.voice_input = None

        self.voice_output = None
        try:
            self.voice_output = VoiceOutput(engine=tts_engine)
            if not self.voice_output.is_available():
                self.voice_output = None
        except Exception as e:
            log_error(str(e), "VoiceManager - output")
            self.voice_output = None

        app_logger.info("VoiceManager initialized")

    def listen(self, mode=None, duration=None, language="en"):
        if not self.voice_input or not self.voice_input.is_available():
            print("   ❌ Voice not available!")
            return None
        use_mode = mode or self.listen_mode
        use_duration = duration or self.listen_duration
        for attempt in range(2):
            text = self.voice_input.listen(mode=use_mode, duration=use_duration, language=language)
            if text and len(text.strip()) > 1:
                garbage = ["you", "the", "a", "an", "um", "uh", "hmm", "thank you", "thanks"]
                if text.strip().lower() not in garbage:
                    return text
            if attempt == 0:
                print("   🔄 Didn't catch that...")
                time.sleep(0.3)
        print("   ❌ Could not understand.")
        return None

    def listen_until_done(self, language="en"):
        if not self.voice_input or not self.voice_input.is_available():
            return None
        for attempt in range(2):
            text = self.voice_input.listen(mode="auto", duration=60, language=language)
            if text and len(text.strip()) > 1:
                garbage = ["you", "the", "a", "an", "um", "uh", "hmm", "thank you", "thanks"]
                if text.strip().lower() not in garbage:
                    return text
            if attempt == 0:
                print("   🔄 Didn't catch that...")
                time.sleep(0.3)
        print("   ❌ Could not understand.")
        return None

    def speak(self, text):
        if not text or not text.strip() or not self.voice_output:
            return False
        try:
            return self.voice_output.speak(text)
        except Exception as e:
            log_error(str(e), "speak")
            return False

    def speak_fast(self, text):
        if not text or not text.strip() or not self.voice_output:
            return False
        try:
            return self.voice_output.speak_fast(text)
        except Exception as e:
            log_error(str(e), "speak_fast")
            return False

    def voice_chat(self, brain, mode=None, duration=None):
        user_text = self.listen_until_done()
        if not user_text:
            return None, None
        print()
        print("🕷️ Spidey: ", end="", flush=True)
        ai_response = brain.chat(user_text)
        print(ai_response)
        print()
        if self.speak_enabled and ai_response:
            self.speak(ai_response)
        return user_text, ai_response

    def _handle_voice_command(self, text):
        lower = text.lower().strip()
        stop_words = ["stop", "exit", "quit", "bye", "close", "band karo", "ruko", "bas", "end", "band"]
        if any(w in lower for w in stop_words):
            return True, False
        if "urdu" in lower or "speak urdu" in lower:
            self.set_language("ur")
            self.speak_fast("Urdu voice activated!")
            return True, True
        if "english" in lower or "speak english" in lower:
            self.set_language("en")
            self.speak_fast("English voice activated!")
            return True, True
        if "hindi" in lower or "speak hindi" in lower:
            self.set_language("hi")
            self.speak_fast("Hindi voice activated!")
            return True, True
        if "speak faster" in lower or "tez bolo" in lower:
            self.set_speech_rate(250)
            self.speak_fast("Speaking faster!")
            return True, True
        if "speak slower" in lower or "dhire bolo" in lower:
            self.set_speech_rate(150)
            self.speak_fast("Speaking slower!")
            return True, True
        if "normal speed" in lower:
            self.set_speech_rate(200)
            self.speak_fast("Normal speed!")
            return True, True
        return False, True

    def spidey_beta_loop(self, brain):
        self.spidey_beta = True
        self.speak_enabled = True
        print()
        print("=" * 55)
        print("   🕷️ SPIDEY BETA MODE (FAST!)")
        print("=" * 55)
        print("   🎤 Talk as long as you want!")
        print("   🗣️ INSTANT speech response!")
        print("   ⌨️ Ctrl+C = Cancel current")
        print("   🗣️ 'stop' = Exit beta")
        print("=" * 55)
        print()
        try:
            self.speak_fast("Spidey Beta on! Go ahead!")
        except KeyboardInterrupt:
            print("\n   ⚠️ Cancelled!\n")
        round_num = 0
        while self.spidey_beta:
            round_num += 1
            print(f"\n   🎤 Round {round_num} — Speak!", flush=True)
            user_text = None
            try:
                user_text = self.listen_until_done(language="en")
            except KeyboardInterrupt:
                print("\n   ⚠️ Cancelled!\n")
                continue
            if not user_text:
                print("   😴 Silence...")
                time.sleep(0.3)
                continue
            try:
                is_cmd, cont = self._handle_voice_command(user_text)
                if is_cmd:
                    if not cont:
                        try:
                            self.speak_fast("Beta off!")
                        except KeyboardInterrupt:
                            pass
                        print("\n   ❌ Spidey Beta OFF\n")
                        self.spidey_beta = False
                        break
                    continue
            except KeyboardInterrupt:
                print("\n   ⚠️ Cancelled!\n")
                continue
            print(f"\n   👤 You: {user_text}")
            ai_response = None
            try:
                print()
                print("   🕷️ Spidey: ", end="", flush=True)
                ai_response = brain.chat(user_text)
                print(ai_response)
                print()
            except KeyboardInterrupt:
                print("\n   ⚠️ AI cancelled!\n")
                continue
            if ai_response:
                try:
                    self.speak_fast(ai_response)
                except KeyboardInterrupt:
                    print("\n   ⚠️ Speech cancelled!\n")
                    if self.voice_output and hasattr(self.voice_output, 'stop'):
                        try:
                            self.voice_output.stop()
                        except Exception:
                            pass
                    continue
            time.sleep(0.2)
        self.spidey_beta = False

    def toggle_speak(self):
        self.speak_enabled = not self.speak_enabled
        log_event("Speak", "ON" if self.speak_enabled else "OFF")
        return self.speak_enabled

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        return self.voice_enabled

    def set_listen_mode(self, mode):
        if mode in ["fixed", "enter", "auto"]:
            self.listen_mode = mode
            return True
        return False

    def set_listen_duration(self, seconds):
        if 1 <= seconds <= 60:
            self.listen_duration = seconds
            return True
        return False

    def switch_tts_engine(self, engine):
        if self.voice_output:
            return self.voice_output.switch_engine(engine)
        return False

    def set_edge_voice(self, voice_id):
        if self.voice_output:
            self.voice_output.set_edge_voice(voice_id)

    def set_language(self, lang):
        if self.voice_output:
            return self.voice_output.set_language(lang)
        return False

    def set_speech_rate(self, rate):
        if self.voice_output:
            self.voice_output.set_rate(rate)

    def test_mic(self):
        if self.voice_input:
            return self.voice_input.test_mic()
        return False

    def test_speak(self, text="Hello! I am Spidey AI!"):
        if self.voice_output and self.voice_output.is_available():
            self.voice_output.speak(text)
            return True
        return False

    def get_voices(self):
        if self.voice_output:
            return self.voice_output.get_voices()
        return []

    def get_mics(self):
        if self.voice_input:
            return self.voice_input.list_mics()
        return []

    def get_current_voice(self):
        if self.voice_output:
            return self.voice_output.get_current_voice()
        return {}

    def get_status(self):
        return {
            "voice_input": self.voice_input is not None and self.voice_input.is_available(),
            "voice_output": self.voice_output is not None and self.voice_output.is_available(),
            "voice_enabled": self.voice_enabled,
            "speak_enabled": self.speak_enabled,
            "spidey_beta": self.spidey_beta,
            "listen_mode": self.listen_mode,
            "listen_duration": self.listen_duration,
            "tts_engine": self.voice_output.get_engine_name() if self.voice_output else "none",
            "current_voice": self.get_current_voice()
        }

    def is_input_available(self):
        return self.voice_input is not None and self.voice_input.is_available()

    def is_output_available(self):
        return self.voice_output is not None and self.voice_output.is_available()