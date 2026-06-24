"""
Spidey AI — Voice Manager (Simple & Reliable!)
No wake word — just Listen → AI → Speak → Repeat!
All control through voice commands!
"""
from spidey.voice.voice_input import VoiceInput
from spidey.voice.voice_output import VoiceOutput
from spidey.logger import app_logger, log_event, log_error
import time


class VoiceManager:
    """Simple voice system — everything by voice!"""

    def __init__(self, whisper_model="small", tts_engine="edge"):
        self.voice_enabled = False
        self.speak_enabled = False
        self.listen_mode = "fixed"
        self.listen_duration = 5
        self.spidey_beta = False

        # Voice Input
        self.voice_input = None
        try:
            self.voice_input = VoiceInput(whisper_model=whisper_model)
            if not self.voice_input.is_available():
                self.voice_input = None
        except Exception as e:
            log_error(str(e), "VoiceManager - input")
            self.voice_input = None

        # Voice Output (Jenny English default)
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
        """Listen with retry"""
        if not self.voice_input or not self.voice_input.is_available():
            print("   ❌ Voice not available!")
            return None

        use_mode = mode or self.listen_mode
        use_duration = duration or self.listen_duration

        for attempt in range(2):
            text = self.voice_input.listen(
                mode=use_mode, duration=use_duration, language=language
            )
            if text and len(text.strip()) > 1:
                garbage = ["you", "the", "a", "an", "um", "uh", "hmm",
                           "thank you", "thanks"]
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
        """Single voice turn"""
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

    def _handle_voice_command(self, text):
        """
        Check if user gave a voice command
        Returns: (is_command, should_continue)
        """
        lower = text.lower().strip()

        # Stop commands
        stop_words = ["stop", "exit", "quit", "bye", "close",
                       "band karo", "ruko", "bas", "end", "band"]
        if any(w in lower for w in stop_words):
            return True, False

        # Language commands
        if "urdu" in lower or "speak urdu" in lower or "urdu mein" in lower:
            self.set_language("ur")
            self.speak("Urdu voice activated!")
            print("   ✅ Urdu voice ON!")
            return True, True

        if "english" in lower or "speak english" in lower or "english mein" in lower:
            self.set_language("en")
            self.speak("English voice activated!")
            print("   ✅ English voice ON!")
            return True, True

        if "hindi" in lower or "speak hindi" in lower or "hindi mein" in lower:
            self.set_language("hi")
            self.speak("Hindi voice activated!")
            print("   ✅ Hindi voice ON!")
            return True, True

        # Volume commands
        if "speak faster" in lower or "fast" in lower or "tez bolo" in lower:
            self.set_speech_rate(220)
            self.speak("Speaking faster now!")
            return True, True

        if "speak slower" in lower or "slow" in lower or "dhire bolo" in lower:
            self.set_speech_rate(130)
            self.speak("Speaking slower now!")
            return True, True

        if "normal speed" in lower or "normal" in lower:
            self.set_speech_rate(175)
            self.speak("Normal speed!")
            return True, True

        return False, True

    def spidey_beta_loop(self, brain):
        """
        🕷️ SPIDEY BETA MODE

        Simple Flow:
        1. Spidey says "Listening!"
        2. Records 7 seconds
        3. Transcribes your speech
        4. Checks for voice commands (language/stop/speed)
        5. If normal message → AI responds → speaks
        6. Repeats!

        Voice Commands (just SAY these):
        - "speak urdu" → switches to Urdu
        - "speak english" → switches to English
        - "speak hindi" → switches to Hindi
        - "speak faster" → faster speech
        - "speak slower" → slower speech
        - "stop" → exits Spidey Beta

        No typing needed — ALL by voice!
        """
        self.spidey_beta = True
        self.speak_enabled = True

        print()
        print("=" * 55)
        print("   🕷️ SPIDEY BETA MODE!")
        print("=" * 55)
        print("   🎤 I'll keep listening to you!")
        print("   🗣️ I'll speak all responses!")
        print("   ⏱️ Speak within 7 seconds each time")
        print()
        print("   🎯 VOICE COMMANDS (just say these!):")
        print("   • 'speak urdu'    → Urdu voice")
        print("   • 'speak english' → English voice")
        print("   • 'speak hindi'   → Hindi voice")
        print("   • 'speak faster'  → Fast speech")
        print("   • 'speak slower'  → Slow speech")
        print("   • 'stop'          → Exit")
        print("=" * 55)
        print()

        self.speak("Spidey Beta mode on! I'm listening. Go ahead!")

        round_num = 0

        while self.spidey_beta:
            try:
                round_num += 1
                print(f"\n   🎤 Round {round_num} — Speak now! (7 sec)", flush=True)

                # Listen
                user_text = self.listen(
                    mode="fixed", duration=7, language="en"
                )

                # Nothing heard
                if not user_text:
                    print("   😴 Silence... Speak or say 'stop' to end.")
                    time.sleep(1)
                    continue

                # Check voice commands
                is_command, should_continue = self._handle_voice_command(user_text)

                if is_command:
                    if not should_continue:
                        self.speak("Spidey Beta off! See you!")
                        print("\n   ❌ Spidey Beta OFF\n")
                        self.spidey_beta = False
                        break
                    continue

                # Normal message — send to AI
                print(f"\n   👤 You: {user_text}")

                print()
                print("   🕷️ Spidey: ", end="", flush=True)
                ai_response = brain.chat(user_text)
                print(ai_response)
                print()

                # Speak full response
                self.speak(ai_response)

                # Small pause
                time.sleep(0.5)

            except KeyboardInterrupt:
                self.speak("Bye!")
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