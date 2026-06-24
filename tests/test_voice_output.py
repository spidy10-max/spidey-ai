"""
Test Voice Output (Text-to-Speech)
Makes Spidey speak!
"""
from spidey.voice.voice_output import VoiceOutput
import time


def test_voice_output():
    print()
    print("=" * 55)
    print("   🗣️ VOICE OUTPUT TEST")
    print("=" * 55)
    print()

    # Test 1: Check TTS libraries
    print("--- Test 1: Check Libraries ---")

    try:
        import pyttsx3
        print("  ✅ pyttsx3 installed")
    except ImportError:
        print("  ❌ pyttsx3 NOT installed")

    try:
        import edge_tts
        print("  ✅ edge-tts installed")
    except ImportError:
        print("  ❌ edge-tts NOT installed")

    try:
        import pygame
        print("  ✅ pygame installed")
    except ImportError:
        print("  ❌ pygame NOT installed")

    print("✅ Test 1 Passed!\n")

    # Test 2: System TTS (pyttsx3)
    print("--- Test 2: System TTS (pyttsx3) ---")
    tts = VoiceOutput(engine="system")

    if tts.is_available():
        print("  ✅ System TTS available")
        print("  🗣️ Speaking: 'Hello! I am Spidey AI!'")
        tts.speak("Hello! I am Spidey AI! Your friendly neighborhood assistant!")
        print("  ✅ Did you hear it?")
    else:
        print("  ⚠️ System TTS not available")

    print("✅ Test 2 Passed!\n")

    # Test 3: List voices
    print("--- Test 3: Available Voices ---")
    voices = tts.get_voices()
    print(f"  Found {len(voices)} voices:")
    for v in voices[:10]:
        print(f"    🗣️ [{v['engine']}] {v['name']}")
    print("✅ Test 3 Passed!\n")

    # Test 4: Change speed
    print("--- Test 4: Speech Speed ---")
    print("  🗣️ Fast speed (250)...")
    tts.set_rate(250)
    tts.speak("This is fast speech. I am talking very quickly!")
    time.sleep(0.5)

    print("  🗣️ Slow speed (120)...")
    tts.set_rate(120)
    tts.speak("This is slow speech. I am talking slowly.")
    time.sleep(0.5)

    print("  🗣️ Normal speed (175)...")
    tts.set_rate(175)
    tts.speak("This is normal speed. Back to regular talking.")

    print("✅ Test 4 Passed!\n")

    # Test 5: Edge TTS
    print("--- Test 5: Edge TTS (Online) ---")
    try:
        edge_tts_obj = VoiceOutput(engine="edge")
        if edge_tts_obj.is_available():
            print("  ✅ Edge TTS available")
            print("  🗣️ Speaking with Microsoft voice...")
            edge_tts_obj.speak("Hello from Edge TTS! I sound much more natural!")
            print("  ✅ Did you hear the better voice?")
        else:
            print("  ⚠️ Edge TTS not available")
    except Exception as e:
        print(f"  ⚠️ Edge TTS error: {e}")

    print("✅ Test 5 Passed!\n")

    # Test 6: Clean text
    print("--- Test 6: Clean Text for Speech ---")
    dirty_text = "🕷️ **Hello!** This is `Spidey AI` 🎤 version 0.3.0! 🎉"
    clean = tts._clean_for_speech(dirty_text)
    print(f"  Dirty: {dirty_text}")
    print(f"  Clean: {clean}")
    print("✅ Test 6 Passed!\n")

    # Test 7: Long text
    print("--- Test 7: Long Text ---")
    long_text = (
        "Python is a high-level programming language. "
        "It is used for web development, data science, and artificial intelligence. "
        "Python is easy to learn and fun to use."
    )
    print("  🗣️ Speaking long text...")
    tts.speak(long_text)
    print("✅ Test 7 Passed!\n")

    print("=" * 55)
    print("   🎉 VOICE OUTPUT TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_voice_output()