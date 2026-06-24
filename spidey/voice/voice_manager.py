"""
Spidey AI — Voice Manager (Spidey Beta Mode!)
Simple & Reliable: Speak FULL → Listen → Repeat
"""
from spidey.voice.voice_input import VoiceInput
from spidey.voice.voice_output import VoiceOutput
from spidey.logger import app_logger, log_event, log_error
import time


class VoiceManager:
    """Simple reliable voice system"""

    def __init__(self, whisper_model="small", tts_engine="edge"):
        """
        whisper_model = "small" for better accuracy!
        (base = fast but less accurate)
        (small = slower but MUCH more accurate)
        """
        self.voice_enabled = False
        self.speak_enabled = False
        self.listen_mode = "fixed"
        self.listen_duration = 5
        self.spidey_beta = False

        # Voice Input (small model for accuracy!)
        self.voice_input = None
        try:
            self.voice_input = VoiceInput(whisper_model=whisper_model)
            if not self.voice_input.is_available():
                self.voice_input = None
        except Exception as e:
            log_error(str(e), "VoiceManager - input")
            self.voice_input = None

        # Voice Output
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
        """Listen with retry — language set for better accuracy"""
        if not self.voice_input or not self.voice_input.is_available():
            print("   ❌ Voice input not available!")
            return None

        use_mode = mode or self.listen_mode
        use_duration = duration or self.listen_duration

        for attempt in range(2):
            text = self.voice_input.listen(
                mode=use_mode,
                duration=use_duration,
                language=language
            )
            if text and len(text.strip()) > 1:
                garbage = ["you", "the", "a", "an", "um", "uh", "hmm",
                           "thank you", "thanks", "bye"]
                if text.strip().lower() not in garbage:
                    return text

            if attempt == 0:
                print("   🔄 Didn't catch that. Try again...")
                time.sleep(0.5)

        print("   ❌ Could not understand. Speak clearly!")
        return None

    def speak(self, text):
        """Speak FULL response"""
        if not text or not text.strip():
            return False
        if not self.voice_output:
            return False

        for attempt in range(2):
            try:
                if self.voice_output.speak(text):
                    return True
            except Exception as e:
                log_error(str(e), f"speak attempt {attempt+1}")
            time.sleep(0.3)
        return False

    def voice_chat(self, brain, mode=None, duration=None):
        """Voice conversation: Listen → AI → Speak"""
        user_text = self.listen(mode=mode, duration=duration)
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

    def spidey_beta_loop(self, brain):
        """
        🕷️ SPIDEY BETA MODE

        Simple & Reliable Flow:
        1. Beep sound → You speak
        2. Spidey listens (7 seconds)
        3. Transcribes your speech
        4. Sends to AI
        5. Speaks FULL response
        6. Response done → Listens again
        7. Say "stop/exit/quit" to end

        No complex interrupts — just ACCURATE & RELIABLE!
        """
        self.spidey_beta = True
        self.speak_enabled = True

        print()
        print("=" * 55)
        print("   🕷️ SPIDEY BETA MODE ACTIVATED!")
        print("=" * 55)
        print("   🎤 I'll listen after every response!")
        print("   🗣️ I'll speak all my responses!")
        print("   ⏱️ You have 7 seconds to speak each time")
        print("   ❌ Say 'stop', 'exit', or 'quit' to end")
        print("=" * 55)
        print()

        self.speak("Spidey Beta mode activated! Go ahead, I'm listening!")

        while self.spidey_beta:
            try:
                print("\n   🎤 Your turn — speak now! (7 seconds)", flush=True)

                # Listen for 7 seconds with English language set
                user_text = self.listen(mode="fixed", duration=7, language="en")

                if not user_text:
                    self.speak("I didn't hear anything. Try again!")
                    continue

                # Check stop commands
                lower = user_text.lower().strip()
                stop_words = ["stop", "exit", "quit", "bye", "close",
                              "band karo", "ruko", "bas", "end"]
                if any(w in lower for w in stop_words):
                    self.speak("Spidey Beta mode deactivated! Back to text mode.")
                    print("\n   ❌ Spidey Beta OFF\n")
                    self.spidey_beta = False
                    break

                # Show what user said
                print(f"\n   👤 You: {user_text}")

                # Get AI response
                print()
                print("   🕷️ Spidey: ", end="", flush=True)
                ai_response = brain.chat(user_text)
                print(ai_response)
                print()

                # Speak FULL response
                self.speak(ai_response)

                # Done speaking → small pause → listen again
                time.sleep(0.5)

            except KeyboardInterrupt:
                self.speak("Spidey Beta off!")
                print("\n   ❌ Spidey Beta OFF\n")
                self.spidey_beta = False
                break
            except Exception as e:
                log_error(str(e), "spidey_beta_loop")
                print(f"   ❌ Error: {e}")
                time.sleep(1)

    def toggle_speak(self):
        self.speak_enabled = not self.speak_enabled
        log_event("Speak mode", "ON" if self.speak_enabled else "OFF")
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

    def test_speak(self, text="Hello! I am Spidey AI, your personal assistant!"):
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