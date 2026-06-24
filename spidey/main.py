"""
Spidey AI — Main (Jarvis Mode!)
"""
from spidey.brain.chat import SpideyBrain
from spidey.config import settings, APP_NAME, APP_VERSION, LOGS_DIR
from spidey.logger import log_startup, log_shutdown
import os

try:
    from spidey.voice.voice_manager import VoiceManager
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


def print_banner():
    print()
    print("=" * 55)
    print(f"   🕷️  {APP_NAME} v{APP_VERSION}  🕷️")
    print("=" * 55)
    print("   Chat:     quit | reset | count")
    print("   History:  history | load | delete")
    print("   Search:   search | smart | findsummary")
    print("   Provider: provider | switch | models")
    print("   Settings: settings | set | tokens | temp | name")
    print("   Memory:   remember | recall | smartrecall | memories | forget")
    print("   Notes:    note | notes | findnote | delnote")
    print("   Voice:    v | voice5 | voice10 | voiceauto")
    print("   Speech:   speak | speakmode | tts | voices | saytest")
    print("   Language: urdu | english | hindi | setvoice")
    print("   🤖 JARVIS: jarvis")
    print("   Other:    stats | logs | mictest | voicestatus")
    print("=" * 55)
    print()


def show_history(brain):
    conversations = brain.get_all_conversations()
    if not conversations:
        print("\n📭 No conversations.\n")
        return
    print("\n" + "=" * 55)
    print("   📂 CONVERSATIONS")
    print("=" * 55)
    for i, conv in enumerate(conversations, 1):
        print(f"\n   {i}. [{conv['conv_id']}]")
        print(f"      📅 {conv['created_at'][:19]}")
        print(f"      💬 {conv['message_count']} msgs | 📝 {conv['title']}")
    print("\n" + "=" * 55 + "\n")


def load_conversation(brain):
    show_history(brain)
    conversations = brain.get_all_conversations()
    if not conversations:
        return
    try:
        index = int(input("🔢 Number: ").strip()) - 1
        if 0 <= index < len(conversations):
            if brain.load_conversation(conversations[index]["conv_id"]):
                print(f"\n✅ Loaded!\n")
    except (ValueError, IndexError):
        print("\n❌ Invalid.\n")


def delete_conversation(brain):
    show_history(brain)
    conversations = brain.get_all_conversations()
    if not conversations:
        return
    try:
        index = int(input("🔢 Number: ").strip()) - 1
        if 0 <= index < len(conversations):
            if input("⚠️ Delete? (y/n): ").strip().lower() in ["y", "yes"]:
                if brain.delete_conversation(conversations[index]["conv_id"]):
                    print(f"\n🗑️ Deleted!\n")
    except (ValueError, IndexError):
        print("\n❌ Invalid.\n")


def show_providers(brain):
    all_p = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()
    print("\n" + "=" * 55)
    for key, config in all_p.items():
        status = "✅" if key == current else ("🟢" if key in available else "🔴")
        print(f"   {status} {key} — {config['name']}")
    print("=" * 55 + "\n")


def show_voices(vm):
    voices = vm.get_voices()
    current_v = vm.get_current_voice().get("voice", "")
    print("\n   🗣️ VOICES:")
    for i, v in enumerate(voices, 1):
        active = " ← ACTIVE" if v["id"] == current_v else ""
        print(f"   {i}. [{v['language']}] {v['name']} ({v['engine']}){active}")
    print()


def show_voice_status(vm):
    status = vm.get_status()
    print("\n" + "=" * 55)
    print("   🎤 VOICE STATUS")
    print("=" * 55)
    print(f"   🎤 Input:  {'✅' if status['voice_input'] else '❌'}")
    print(f"   🗣️ Output: {'✅' if status['voice_output'] else '❌'}")
    print(f"   🔊 Speak:  {'ON 🟢' if status['speak_enabled'] else 'OFF 🔴'}")
    print(f"   🤖 Jarvis: {'ON 🟢' if status['jarvis_mode'] else 'OFF 🔴'}")
    print(f"   🎤 Mode:   {status['listen_mode']}")
    print(f"   ⏱️ Duration: {status['listen_duration']}s")
    print(f"   🗣️ Engine: {status['tts_engine']}")
    v = status.get('current_voice', {})
    print(f"   🗣️ Voice:  {v.get('voice', 'N/A')}")
    print(f"   🌍 Lang:   {v.get('language', 'N/A')}")
    print("=" * 55 + "\n")


def main():
    print_banner()

    brain = SpideyBrain()
    brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    # Initialize voice
    vm = None
    if VOICE_AVAILABLE:
        try:
            vm = VoiceManager(whisper_model="base", tts_engine="edge")
            print(f"   🎤 Input:  {'✅' if vm.is_input_available() else '❌'}")
            print(f"   🗣️ Output: {'✅' if vm.is_output_available() else '❌'}")
            print(f"   🗣️ Voice:  Jenny (US Female)")
        except Exception as e:
            print(f"   🎤 Voice error: {e}")
            vm = None

    log_startup(info['name'], settings.get_all())

    print(f"\n🕷️ Spidey: Hey {username}!")
    print(f"   🤖 {info['name']}")

    memories = brain.get_all_memories()
    if memories:
        print(f"   🧠 I remember {len(memories)} things!")

    print(f"   💡 Type 'jarvis' for hands-free voice mode!")
    print()

    while True:
        try:
            provider = brain.get_provider_name()
            username = settings.get("username", "User")
            speak_icon = "🔊" if (vm and vm.speak_enabled) else ""
            user_input = input(f"👤 {username} [{provider}]{speak_icon}: ").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            # === QUIT ===
            if cmd in ["quit", "exit", "bye", "q"]:
                count = brain.get_history_count()
                log_shutdown(count)
                farewell = f"Bye {username}! {count} messages saved!"
                print(f"\n🕷️ Spidey: {farewell} 🕸️")
                if vm and vm.speak_enabled:
                    vm.speak(farewell)
                brain.close()
                break

            # === 🤖 JARVIS MODE ===
            if cmd == "jarvis":
                if vm and vm.is_input_available() and vm.is_output_available():
                    vm.jarvis_loop(brain)
                else:
                    print("\n   ❌ Voice not available for Jarvis mode!\n")
                continue

            # === VOICE INPUT ===
            if cmd in ["v", "voice"]:
                if vm:
                    vm.voice_chat(brain, mode="fixed", duration=5)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "voice5":
                if vm:
                    vm.voice_chat(brain, mode="fixed", duration=5)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "voice10":
                if vm:
                    vm.voice_chat(brain, mode="fixed", duration=10)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "voiceauto":
                if vm:
                    vm.voice_chat(brain, mode="auto")
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            # === SPEECH ===
            if cmd == "speakmode":
                if vm:
                    enabled = vm.toggle_speak()
                    status = "ON 🟢" if enabled else "OFF 🔴"
                    print(f"\n   🔊 Speak mode: {status}")
                    if enabled:
                        vm.speak("Speak mode on! I will speak all responses!")
                    print()
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "speak":
                if vm:
                    text = input("   🗣️ Text: ").strip()
                    if text:
                        vm.speak(text)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "saytest":
                if vm:
                    vm.test_speak("Hello! I am Spidey AI, your personal Jarvis!")
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "tts":
                if vm:
                    print("\n   1. system (offline)")
                    print("   2. edge (online, better)")
                    c = input("   Choose (system/edge): ").strip().lower()
                    if vm.switch_tts_engine(c):
                        print(f"\n   ✅ Switched to {c}!\n")
                continue

            if cmd == "voices":
                if vm:
                    show_voices(vm)
                continue

            if cmd == "voicestatus":
                if vm:
                    show_voice_status(vm)
                continue

            if cmd == "mictest":
                if vm:
                    vm.test_mic()
                continue

            # === LANGUAGE ===
            if cmd == "urdu":
                if vm:
                    vm.set_language("ur")
                    print("\n   ✅ Urdu voice!")
                    vm.speak("السلام علیکم! میں سپائیڈی اے آئی ہوں!")
                    print()
                continue

            if cmd == "english":
                if vm:
                    vm.set_language("en")
                    print("\n   ✅ English voice!")
                    vm.speak("Hello! Back to English!")
                    print()
                continue

            if cmd == "hindi":
                if vm:
                    vm.set_language("hi")
                    print("\n   ✅ Hindi voice!")
                    vm.speak("नमस्ते! मैं स्पाइडी हूँ!")
                    print()
                continue

            if cmd == "setvoice":
                if vm:
                    voices = vm.get_voices()
                    current_v = vm.get_current_voice().get("voice", "")
                    print("\n   🗣️ Voices:")
                    for i, v in enumerate(voices, 1):
                        active = " ← ACTIVE" if v["id"] == current_v else ""
                        print(f"   {i}. [{v['language']}] {v['name']}{active}")
                    try:
                        c = int(input("\n   🔢 Number: ").strip()) - 1
                        if 0 <= c < len(voices):
                            vm.voice_output.set_voice(voices[c]["id"])
                            print(f"\n   ✅ Voice: {voices[c]['name']}")
                            vm.speak(f"Hello! I am now {voices[c]['name']}!")
                            print()
                    except (ValueError, IndexError):
                        print("   ❌ Invalid\n")
                continue

            # === CHAT ===
            if cmd == "reset":
                brain.reset()
                print("\n🕷️ Fresh start! 🔄\n")
                continue
            if cmd == "count":
                print(f"\n📊 Messages: {brain.get_history_count()}\n")
                continue

            # === HISTORY ===
            if cmd == "history":
                show_history(brain)
                continue
            if cmd == "load":
                load_conversation(brain)
                continue
            if cmd == "delete":
                delete_conversation(brain)
                continue

            # === SEARCH ===
            if cmd == "search":
                q = input("🔍 Search: ").strip()
                if q:
                    results = brain.search_chats(q)
                    if results:
                        for m in results[:5]:
                            print(f"   {'👤' if m['role']=='user' else '🕷️'} {m['content'][:60]}...")
                    else:
                        print("   📭 Nothing found.")
                    print()
                continue
            if cmd == "smart":
                q = input("🔍 Smart: ").strip()
                if q:
                    results = brain.semantic_search(q)
                    if results:
                        for r in results[:5]:
                            print(f"   📝 {r['content'][:60]}...")
                    else:
                        print("   📭 Nothing found.")
                    print()
                continue

            # === PROVIDERS ===
            if cmd == "provider":
                i = brain.get_provider_info()
                print(f"\n🤖 {i['name']}\n")
                continue
            if cmd == "switch":
                show_providers(brain)
                c = input("🔢 Provider: ").strip().lower()
                if brain.switch_provider(c):
                    print(f"\n✅ Switched!\n")
                continue
            if cmd == "models":
                show_providers(brain)
                continue

            # === SETTINGS ===
            if cmd == "settings":
                print(settings)
                continue
            if cmd == "tokens":
                cur = settings.get("show_tokens", False)
                settings.set("show_tokens", not cur)
                brain.update_settings()
                print(f"\n📊 Tokens: {'ON' if not cur else 'OFF'}\n")
                continue
            if cmd == "temp":
                try:
                    v = float(input("   🌡️ (0.0-2.0): "))
                    if 0.0 <= v <= 2.0:
                        settings.set("temperature", v)
                        brain.update_settings()
                        print(f"   ✅ Temp: {v}\n")
                except ValueError:
                    pass
                continue
            if cmd == "name":
                v = input("   📝 Name: ").strip()
                if v:
                    settings.set("username", v)
                    print(f"   ✅ Name: {v}\n")
                continue

            # === MEMORY ===
            if cmd == "remember":
                k = input("   📝 Key: ").strip()
                v = input("   📝 Value: ").strip() if k else ""
                c = input("   📁 Category: ").strip() or "general" if v else ""
                if k and v:
                    brain.remember(k, v, c)
                    print(f"\n   ✅ {k} = {v}\n")
                continue
            if cmd == "recall":
                k = input("   🧠 Key: ").strip()
                if k:
                    v = brain.recall(k)
                    print(f"\n   🧠 {k} = {v}\n" if v else f"\n   ❌ Unknown\n")
                continue
            if cmd == "smartrecall":
                q = input("   🧠 Query: ").strip()
                if q:
                    for r in brain.smart_recall(q):
                        print(f"      • {r['content']}")
                    print()
                continue
            if cmd == "memories":
                m = brain.get_all_memories()
                if m:
                    for k, i in m.items():
                        print(f"   • {k}: {i['value']}")
                else:
                    print("   📭 No memories.")
                print()
                continue
            if cmd == "forget":
                k = input("   🗑️ Key: ").strip()
                if k and brain.forget(k):
                    print(f"   ✅ Forgot: {k}\n")
                continue

            # === NOTES ===
            if cmd == "note":
                t = input("   📝 Title: ").strip()
                c = input("   📝 Content: ").strip() if t else ""
                if t and c:
                    brain.add_note(t, c)
                    print("   ✅ Added!\n")
                continue
            if cmd == "notes":
                for n in brain.get_notes():
                    star = "⭐" if n["is_important"] else "  "
                    print(f"   {star}[{n['id']}] {n['title']}: {n['content'][:40]}")
                print()
                continue

            # === STATS ===
            if cmd == "stats":
                s = brain.get_stats()
                print(f"\n   💬 {s['total_conversations']} convs | 📨 {s['total_messages']} msgs | 🧠 {s['total_preferences']} memories\n")
                continue
            if cmd == "logs":
                if os.path.exists(LOGS_DIR):
                    for f in sorted(os.listdir(LOGS_DIR), reverse=True)[:5]:
                        print(f"   📄 {f}")
                print()
                continue

            # === AI CHAT ===
            print()
            print("🕷️ Spidey: ", end="", flush=True)
            response = brain.chat(user_input)
            print(response)
            print()

            # ALWAYS speak if speak mode ON
            if vm and vm.speak_enabled and response:
                vm.speak(response)

        except KeyboardInterrupt:
            log_shutdown(brain.get_history_count())
            print("\n\n🕷️ Bye! 🕸️\n")
            brain.close()
            break


if __name__ == "__main__":
    main()