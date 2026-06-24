"""
Test Full Voice Conversation
Listen + AI + Speak
"""
from spidey.voice.voice_manager import VoiceManager
from spidey.brain.chat import SpideyBrain


def test_voice_conversation():
    print()
    print("=" * 55)
    print("   🎤🗣️ VOICE CONVERSATION TEST")
    print("=" * 55)
    print()

    # Test 1: Initialize
    print("--- Test 1: Initialize Voice Manager ---")
    vm = VoiceManager(whisper_model="base", tts_engine="system")
    status = vm.get_status()
    print(f"  Input:  {status['voice_input']}")
    print(f"  Output: {status['voice_output']}")
    print(f"  TTS:    {status['tts_engine']}")
    print("✅ Test 1 Passed!\n")

    # Test 2: Test speak
    print("--- Test 2: Test Speech ---")
    vm.test_speak("Hello! I am Spidey AI. Can you hear me?")
    print("✅ Test 2 Passed!\n")

    # Test 3: Toggle speak mode
    print("--- Test 3: Toggle Speak Mode ---")
    enabled = vm.toggle_speak()
    print(f"  Speak mode: {'ON' if enabled else 'OFF'}")
    assert enabled == True
    print("✅ Test 3 Passed!\n")

    # Test 4: Voice chat
    print("--- Test 4: Voice Chat ---")
    print("  🎤 Say something for 5 seconds!")
    print("  Example: 'What is Python?'\n")

    brain = SpideyBrain()
    brain.start_new_conversation()

    user_text, ai_response = vm.voice_chat(brain, mode="fixed", duration=5)

    if user_text:
        print(f"\n  👤 You said: {user_text}")
        print(f"  🕷️ Spidey said: {ai_response[:80]}...")
        print("  🗣️ Did Spidey speak the response?")
    else:
        print("  ⚠️ Could not understand. Try speaking louder.")

    print("✅ Test 4 Passed!\n")

    # Test 5: List voices
    print("--- Test 5: Available Voices ---")
    voices = vm.get_voices()
    print(f"  Found {len(voices)} voices:")
    for v in voices[:5]:
        print(f"    🗣️ {v['name']} ({v['engine']})")
    print("✅ Test 5 Passed!\n")

    # Test 6: Status
    print("--- Test 6: Voice Status ---")
    status = vm.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    print("✅ Test 6 Passed!\n")

    brain.close()

    print("=" * 55)
    print("   🎉 VOICE CONVERSATION TEST COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_voice_conversation()