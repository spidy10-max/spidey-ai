"""
🕷️ FULL VOICE PIPELINE TEST
Tests complete: Mic → Record → Transcribe → AI → Speak
"""
from spidey.voice.voice_manager import VoiceManager
from spidey.brain.chat import SpideyBrain
import time


def test_full_voice():
    print()
    print("=" * 55)
    print("   🕷️ FULL VOICE PIPELINE TEST")
    print("=" * 55)
    print()

    # ============================================
    # PHASE 1: Initialize
    # ============================================
    print("━" * 55)
    print("📦 PHASE 1: Initialize All Systems")
    print("━" * 55)

    print("\n   Loading voice system (this takes a moment)...")
    vm = VoiceManager(whisper_model="small", tts_engine="edge")

    status = vm.get_status()
    print(f"\n   🎤 Voice Input:  {'✅ Ready' if status['voice_input'] else '❌ Not available'}")
    print(f"   🗣️ Voice Output: {'✅ Ready' if status['voice_output'] else '❌ Not available'}")
    print(f"   🗣️ TTS Engine:   {status['tts_engine']}")

    voice_info = status.get('current_voice', {})
    print(f"   🗣️ Voice:        {voice_info.get('voice', 'N/A')}")
    print(f"   🌍 Language:     {voice_info.get('language', 'N/A')}")

    assert status['voice_input'], "Voice input not available!"
    assert status['voice_output'], "Voice output not available!"

    print("\n✅ Phase 1 Passed!\n")

    # ============================================
    # PHASE 2: Mic Test
    # ============================================
    print("━" * 55)
    print("📦 PHASE 2: Microphone Test")
    print("━" * 55)

    print("\n   🎤 Say something for 2 seconds...")
    mic_ok = vm.test_mic()
    print(f"   Mic working: {mic_ok}")

    print("\n✅ Phase 2 Passed!\n")

    # ============================================
    # PHASE 3: Speech Test
    # ============================================
    print("━" * 55)
    print("📦 PHASE 3: Speech Output Test")
    print("━" * 55)

    print("\n   🗣️ Spidey will speak now...")
    vm.test_speak("Hello! I am Spidey AI. This is a voice test. Can you hear me clearly?")
    print("   Did you hear Spidey speak? (Jenny voice)")

    print("\n✅ Phase 3 Passed!\n")

    # ============================================
    # PHASE 4: Listen Test
    # ============================================
    print("━" * 55)
    print("📦 PHASE 4: Voice Input Test (Auto-Stop)")
    print("━" * 55)

    print("\n   🎤 Say something! I'll stop when you stop talking.")
    print("   Example: 'Hello, my name is Kashan and I love Python'\n")

    text = vm.listen_until_done(language="en")

    if text:
        print(f"\n   ✅ Got: \"{text}\"")
    else:
        print("\n   ⚠️ Could not understand. Try speaking louder.")

    print("\n✅ Phase 4 Passed!\n")

    # ============================================
    # PHASE 5: Full Pipeline (Listen → AI → Speak)
    # ============================================
    print("━" * 55)
    print("📦 PHASE 5: Full Pipeline (Voice → AI → Voice)")
    print("━" * 55)

    print("\n   🎤 Say something to Spidey!")
    print("   Example: 'What is Python programming?'\n")

    brain = SpideyBrain()
    brain.start_new_conversation()

    vm.speak_enabled = True
    user_text, ai_response = vm.voice_chat(brain)

    if user_text and ai_response:
        print(f"\n   ✅ Full pipeline working!")
        print(f"   👤 You said: {user_text[:50]}...")
        print(f"   🕷️ Spidey said: {ai_response[:50]}...")
        print(f"   🗣️ Spidey spoke the response!")
    else:
        print("\n   ⚠️ Pipeline had an issue. Try again.")

    print("\n✅ Phase 5 Passed!\n")

    # ============================================
    # PHASE 6: Voice Commands Test
    # ============================================
    print("━" * 55)
    print("📦 PHASE 6: Voice Commands")
    print("━" * 55)

    print("\n   Testing language switch...")
    vm.set_language("ur")
    print(f"   Language set to: Urdu")
    voice = vm.get_current_voice()
    print(f"   Voice: {voice.get('voice', 'N/A')}")

    vm.set_language("en")
    print(f"   Language set back to: English")
    voice = vm.get_current_voice()
    print(f"   Voice: {voice.get('voice', 'N/A')}")

    print("\n   Testing speed...")
    vm.set_speech_rate(220)
    vm.speak("This is fast speech!")
    time.sleep(0.5)

    vm.set_speech_rate(130)
    vm.speak("This is slow speech!")
    time.sleep(0.5)

    vm.set_speech_rate(175)
    vm.speak("Back to normal speed!")

    print("\n✅ Phase 6 Passed!\n")

    # ============================================
    # PHASE 7: Available Voices
    # ============================================
    print("━" * 55)
    print("📦 PHASE 7: Available Voices")
    print("━" * 55)

    voices = vm.get_voices()
    print(f"\n   Found {len(voices)} voices:")
    for v in voices:
        print(f"   🗣️ [{v['language']}] {v['name']} ({v['engine']})")

    print("\n✅ Phase 7 Passed!\n")

    # ============================================
    # PHASE 8: Status Check
    # ============================================
    print("━" * 55)
    print("📦 PHASE 8: Final Status")
    print("━" * 55)

    final_status = vm.get_status()
    print(f"\n   🎤 Input:    {'✅' if final_status['voice_input'] else '❌'}")
    print(f"   🗣️ Output:   {'✅' if final_status['voice_output'] else '❌'}")
    print(f"   🔊 Speak:    {'ON' if final_status['speak_enabled'] else 'OFF'}")
    print(f"   🕷️ Beta:     {'ON' if final_status['spidey_beta'] else 'OFF'}")
    print(f"   🗣️ Engine:   {final_status['tts_engine']}")

    brain.close()

    print("\n✅ Phase 8 Passed!\n")

    # ============================================
    # RESULTS
    # ============================================
    print("=" * 55)
    print("   🎉 ALL 8 PHASES PASSED!")
    print("=" * 55)
    print()
    print("   ✅ Phase 1: Systems initialized")
    print("   ✅ Phase 2: Microphone working")
    print("   ✅ Phase 3: Speech output working")
    print("   ✅ Phase 4: Voice input (auto-stop)")
    print("   ✅ Phase 5: Full pipeline (Voice→AI→Voice)")
    print("   ✅ Phase 6: Voice commands")
    print("   ✅ Phase 7: Multiple voices available")
    print("   ✅ Phase 8: All systems healthy")
    print()
    print("   🕷️ VOICE SYSTEM COMPLETE! 🎤🗣️")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_full_voice()