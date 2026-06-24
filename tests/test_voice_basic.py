"""
Test Voice Recording and Transcription
"""
import os


def test_voice():
    print()
    print("=" * 55)
    print("   🎤 VOICE SYSTEM TEST")
    print("=" * 55)
    print()

    # Test 1: Check libraries
    print("--- Test 1: Check Libraries ---")

    try:
        import sounddevice as sd
        print("  ✅ sounddevice installed")
    except ImportError:
        print("  ❌ sounddevice NOT installed")
        return

    try:
        import soundfile as sf
        print("  ✅ soundfile installed")
    except ImportError:
        print("  ❌ soundfile NOT installed")
        return

    try:
        import numpy as np
        print("  ✅ numpy installed")
    except ImportError:
        print("  ❌ numpy NOT installed")
        return

    whisper_ok = False
    try:
        import whisper
        print("  ✅ openai-whisper installed")
        whisper_ok = True
    except ImportError:
        try:
            from faster_whisper import WhisperModel
            print("  ✅ faster-whisper installed")
            whisper_ok = True
        except ImportError:
            print("  ❌ No whisper installed!")

    print("✅ Test 1 Passed!\n")

    # Test 2: List microphones
    print("--- Test 2: Available Microphones ---")
    from spidey.voice.recorder import AudioRecorder

    recorder = AudioRecorder()
    mics = recorder.list_microphones()

    if mics:
        print(f"  Found {len(mics)} microphones:")
        for mic in mics:
            print(f"    🎤 [{mic['id']}] {mic['name']}")
    else:
        print("  ❌ No microphones found!")
        return

    print("✅ Test 2 Passed!\n")

    # Test 3: Microphone test
    print("--- Test 3: Microphone Test ---")
    print("  🎤 Say something for 2 seconds...")
    mic_ok = recorder.test_microphone(duration=2)
    if mic_ok:
        print("✅ Test 3 Passed!\n")
    else:
        print("⚠️ Test 3 Warning: Low volume\n")

    # Test 4: Record 3 seconds
    print("--- Test 4: Record 3 Seconds ---")
    print("  🎤 Speak something for 3 seconds...")
    filepath = recorder.record_fixed(duration=3)

    if filepath and os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  📄 File: {filepath}")
        print(f"  📊 Size: {round(size/1024, 1)} KB")
        print("✅ Test 4 Passed!\n")
    else:
        print("❌ Test 4 Failed!\n")
        return

    # Test 5: Transcribe
    if whisper_ok and filepath:
        print("--- Test 5: Transcription ---")
        from spidey.voice.transcriber import Transcriber

        transcriber = Transcriber(model_size="base")

        if transcriber.is_available():
            result = transcriber.transcribe(filepath)
            print(f"  📝 Text: {result['text']}")
            print(f"  🌍 Language: {result['language']}")
            print(f"  ✅ Success: {result['success']}")

            if result["success"]:
                print("✅ Test 5 Passed!\n")
            else:
                print("⚠️ Test 5 Warning\n")
        else:
            print("  ⚠️ Whisper model not loaded\n")

    # Cleanup
    if filepath and os.path.exists(filepath):
        os.remove(filepath)
        print("🧹 Cleaned up")

    print()
    print("=" * 55)
    print("   🎉 VOICE TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_voice()