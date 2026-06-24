"""
Spidey AI — Voice Manager (Jarvis Mode!)
Continuous voice conversation like Tony Stark's Jarvis
"""
from spidey.voice.voice_input import VoiceInput
from spidey.voice.voice_output import VoiceOutput
from spidey.logger import app_logger, log_event, log_error
import time


class VoiceManager:
    """Jarvis-like voice system"""

    def __init__(self, whisper_model="base", tts_engine="edge"):
        self.voice_enabled = False
        self.speak_enabled = False
        self.listen_mode = "fixed"
        self.listen_duration = 5
        self.jarvis_mode = False

        # Voice Input
        self.voice_input = None
        try:
            self.voice_input = VoiceInput(whisper_model=whisper_model)
            if not self.voice_input.is_available():
                self.voice_input = None
        except Exception as e:
            log_error(str(e), "VoiceManager - input")
            self.voice_input = None

        # Voice Output (default = edge + Jenny)
        self.voice_output = None
        try:
            self.voice_output = VoiceOutput(engine=tts_engine)
            if not self.voice_output.is_available():
                self.voice_output = None
        except Exception as e:
            log_error(str(e), "VoiceManager - output")
            self.voice_output = None

        app_logger.info("VoiceManager initialized")

    def listen(self, mode=None, duration=None):
        """Listen for voice input"""
        if not self.voice_input or not self.voice_input.is_available():
            print("   ❌ Voice input not available!")
            return None

        use_mode = mode or self.listen_mode
        use_duration = duration or self.listen_duration

        # Try up to 2 times if failed
        for attempt in range(2):
            text = self.voice_input.listen(mode=use_mode, duration=use_duration)
            if text and len(text.strip()) > 1:
                return text
            if attempt == 0:
                print("   🔄 Didn't catch that. Try again...")
                time.sleep(0.5)

        print("   ❌ Could not understand. Please try again.")
        return None

    def speak(self, text):
        """Speak — ALWAYS tries, with retry"""
        if not text or not text.strip():
            return False

        if not self.voice_output:
            return False

        # Try to speak, retry once if failed
        for attempt in range(2):
            try:
                result = self.voice_output.speak(text)
                if result:
                    return True
            except Exception as e:
                log_error(str(e), f"VoiceManager.speak attempt {attempt+1}")

            if attempt == 0:
                time.sleep(0.5)

        return False

    def voice_chat(self, brain, mode=None, duration=None):
        """
        Voice conversation turn:
        Listen → AI → Speak (Jarvis style)
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

        # ALWAYS speak response
        if self.speak_enabled and ai_response:
            self.speak(ai_response)

        return user_text, ai_response

    def jarvis_loop(self, brain):
        """
        🤖 JARVIS MODE — Continuous voice conversation!

        Like Tony Stark's Jarvis:
        - Continuously listens
        - Responds with voice
        - Never stops until you say "stop" or "exit"
        """
        self.jarvis_mode = True
        self.speak_enabled = True

        print()
        print("=" * 55)
        print("   🤖 JARVIS MODE ACTIVATED!")
        print("=" * 55)
        print("   🎤 I'm listening continuously...")
        print("   🗣️ I'll speak all responses!")
        print("   ❌ Say 'stop', 'exit', or 'quit' to end")
        print("=" * 55)
        print()

        self.speak("Jarvis mode activated! I'm listening. Talk to me anytime!")

        while self.jarvis_mode:
            try:
                print("\n   🎤 Listening...", flush=True)

                # Listen with auto-stop on silence
                user_text = self.listen(mode="auto", duration=None)

                if not user_text:
                    continue

                # Check for stop commands
                lower_text = user_text.lower().strip()
                if any(word in lower_text for word in ["stop", "exit", "quit", "bye", "band karo", "ruko"]):
                    self.speak("Jarvis mode deactivated. Going back to text mode!")
                    print("\n   ❌ Jarvis mode OFF\n")
                    self.jarvis_mode = False
                    break

                # Send to AI
                print(f"\n   👤 You: {user_text}")
                print()
                print("   🕷️ Spidey: ", end="", flush=True)
                ai_response = brain.chat(user_text)
                print(ai_response)
                print()

                # Speak response
                self.speak(ai_response)

                # Small pause before next listen
                time.sleep(0.5)

            except KeyboardInterrupt:
                self.speak("Jarvis mode deactivated!")
                print("\n   ❌ Jarvis mode OFF\n")
                self.jarvis_mode = False
                break

            except Exception as e:
                log_error(str(e), "VoiceManager.jarvis_loop")
                print(f"   ❌ Error: {e}")
                time.sleep(1)

    def toggle_speak(self):
        self.speak_enabled = not self.speak_enabled
        log_event("Speak mode", "ON" if self.speak_enabled else "OFF")
        return self.speak_enabled

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        log_event("Voice mode", "ON" if self.voice_enabled else "OFF")
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
        print("   ❌ Voice input not available!")
        return False

    def test_speak(self, text="Hello! I am Spidey AI, your personal assistant!"):
        if self.voice_output and self.voice_output.is_available():
            self.voice_output.speak(text)
            return True
        print("   ❌ Voice output not available!")
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
            "jarvis_mode": self.jarvis_mode,
            "listen_mode": self.listen_mode,
            "listen_duration": self.listen_duration,
            "tts_engine": self.voice_output.get_engine_name() if self.voice_output else "none",
            "current_voice": self.get_current_voice()
        }

    def is_input_available(self):
        return self.voice_input is not None and self.voice_input.is_available()

    def is_output_available(self):
        return self.voice_output is not None and self.voice_output.is_available()