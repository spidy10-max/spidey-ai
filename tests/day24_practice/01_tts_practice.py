"""
Practice: Text-to-Speech
Try different voices and settings
"""
from spidey.voice.voice_output import VoiceOutput
import time


def main():
    print()
    print("=" * 55)
    print("   🗣️ TTS PRACTICE")
    print("=" * 55)
    print()

    tts = VoiceOutput(engine="system")

    if not tts.is_available():
        print("❌ TTS not available!")
        return

    while True:
        print("\n   Options:")
        print("   1. Speak custom text")
        print("   2. Try fast speed")
        print("   3. Try slow speed")
        print("   4. Normal speed")
        print("   5. List voices")
        print("   6. Switch to Edge TTS")
        print("   7. Switch to System TTS")
        print("   8. Try Urdu (Edge TTS)")
        print("   9. Quit")

        choice = input("\n   Choose (1-9): ").strip()

        if choice == "1":
            text = input("   📝 Text to speak: ").strip()
            if text:
                print("   🗣️ Speaking...")
                tts.speak(text)

        elif choice == "2":
            tts.set_rate(280)
            tts.speak("I am speaking very fast now! Can you keep up?")

        elif choice == "3":
            tts.set_rate(100)
            tts.speak("I am speaking very slowly now.")

        elif choice == "4":
            tts.set_rate(175)
            tts.speak("Back to normal speed.")

        elif choice == "5":
            voices = tts.get_voices()
            for v in voices:
                print(f"   🗣️ [{v['engine']}] {v['name']}")
                print(f"      ID: {v['id']}")

        elif choice == "6":
            if tts.switch_engine("edge"):
                print("   ✅ Switched to Edge TTS!")
                tts.speak("Hello! I am using Microsoft Edge TTS now. I sound more natural!")
            else:
                print("   ❌ Edge TTS not available!")

        elif choice == "7":
            if tts.switch_engine("system"):
                print("   ✅ Switched to System TTS!")
                tts.speak("Hello! Back to system voice.")
            else:
                print("   ❌ System TTS not available!")

        elif choice == "8":
            try:
                edge = VoiceOutput(engine="edge")
                if edge.is_available():
                    import asyncio
                    import edge_tts as et

                    temp_file = "data/audio/urdu_test.mp3"
                    async def speak_urdu():
                        communicate = et.Communicate(
                            "السلام علیکم! میں سپائیڈی اے آئی ہوں۔",
                            "ur-PK-AsadNeural"
                        )
                        await communicate.save(temp_file)

                    asyncio.run(speak_urdu())

                    import pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                    import os
                    os.remove(temp_file)
                    print("   ✅ Urdu speech done!")
                else:
                    print("   ❌ Edge TTS not available!")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        elif choice == "9":
            print("\n   👋 Bye!\n")
            break

        else:
            print("   ❌ Invalid choice")


if __name__ == "__main__":
    main()