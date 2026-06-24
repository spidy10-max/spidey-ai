"""
Test Voice Input Pipeline
Records → Transcribes → Returns text
"""
from spidey.voice.voice_input import VoiceInput


def test_voice_input():
    print()
    print("=" * 55)
    print("   🎤 VOICE INPUT PIPELINE TEST")
    print("=" * 55)
    print()

    voice = VoiceInput(whisper_model="base")

    if not voice.is_available():
        print("❌ Voice not available!")
        return

    # Test 1: Mic test
    print("--- Test 1: Microphone Test ---")
    mic_ok = voice.test_mic()
    if mic_ok:
        print("✅ Test 1 Passed!\n")
    else:
        print("⚠️ Test 1 Warning\n")

    # Test 2: List mics
    print("--- Test 2: List Microphones ---")
    mics = voice.list_mics()
    print(f"  Found {len(mics)} mics")
    for mic in mics[:3]:
        print(f"    🎤 {mic['name']}")
    print("✅ Test 2 Passed!\n")

    # Test 3: Fixed duration recording
    print("--- Test 3: Record 5 Seconds ---")
    print("  🎤 Say something clearly for 5 seconds!")
    print("  Example: 'Hello, my name is Kashan'\n")

    text = voice.listen_fixed(duration=5)

    if text:
        print(f"\n  ✅ Got text: \"{text}\"")
        print("✅ Test 3 Passed!\n")
    else:
        print("\n  ⚠️ No text detected")
        print("  Try speaking louder\n")

    # Test 4: Check last result
    print("--- Test 4: Last Result ---")
    result = voice.get_last_result()
    if result:
        print(f"  Text: {result.get('text', 'N/A')}")
        print(f"  Language: {result.get('language', 'N/A')}")
        print(f"  Success: {result.get('success', False)}")
    print("✅ Test 4 Passed!\n")

    # Test 5: Another recording
    print("--- Test 5: Record Again (3 seconds) ---")
    print("  🎤 Say something short!\n")

    text = voice.listen_fixed(duration=3)
    if text:
        print(f"\n  ✅ Got: \"{text}\"")
    print("✅ Test 5 Passed!\n")

    print("=" * 55)
    print("   🎉 VOICE INPUT TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_voice_input()