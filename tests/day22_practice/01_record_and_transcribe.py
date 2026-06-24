"""
Practice: Record audio and transcribe
"""
from spidey.voice.recorder import AudioRecorder
from spidey.voice.transcriber import Transcriber
import os


def main():
    print()
    print("=" * 55)
    print("   🎤 RECORD & TRANSCRIBE PRACTICE")
    print("=" * 55)
    print()

    recorder = AudioRecorder()
    transcriber = Transcriber(model_size="base")

    if not transcriber.is_available():
        print("❌ Whisper not available!")
        return

    while True:
        print("\n   Options:")
        print("   1. Record 5 seconds")
        print("   2. Record 10 seconds")
        print("   3. Record until Enter")
        print("   4. Test microphone")
        print("   5. List microphones")
        print("   6. Quit")

        choice = input("\n   Choose (1-6): ").strip()

        if choice == "1":
            filepath = recorder.record_fixed(duration=5)
        elif choice == "2":
            filepath = recorder.record_fixed(duration=10)
        elif choice == "3":
            filepath = recorder.record_until_enter()
        elif choice == "4":
            recorder.test_microphone()
            continue
        elif choice == "5":
            mics = recorder.list_microphones()
            for mic in mics:
                print(f"   🎤 [{mic['id']}] {mic['name']}")
            continue
        elif choice == "6":
            print("\n   👋 Bye!\n")
            break
        else:
            print("   ❌ Invalid choice")
            continue

        if filepath:
            print("\n   🔄 Transcribing with Whisper...")
            result = transcriber.transcribe(filepath)

            print(f"\n   📝 You said: \"{result['text']}\"")
            print(f"   🌍 Language: {result['language']}")

            os.remove(filepath)


if __name__ == "__main__":
    main()