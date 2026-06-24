"""
Spidey AI — Main (Spidey Beta Mode!)
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
    print("   🕷️ SPIDEY: spidey beta (full voice mode!)")
    print("   🎤 Voice:   v | voice5 | voice10 | voiceauto")
    print("   🗣️ Speech:  speakmode | saytest | setvoice")
    print("   🌍 Lang:    urdu | english | hindi")
    print("   💬 Chat:    quit | reset | count")
    print("   📂 History: history | load | delete")
    print("   🔍 Search:  search | smart")
    print("   🤖 AI:      provider | switch | models")
    print("   🧠 Memory:  remember | recall | memories | forget")
    print("   📝 Notes:   note | notes")
    print("   📊 Other:   stats | voicestatus | mictest")
    print("=" * 55)
    print()


def show_history(brain):
    conversations = brain.get_all_conversations()
    if not conversations:
        print("\n📭 No conversations.\n")
        return
    for i, conv in enumerate(conversations, 1):
        print(f"   {i}. [{conv['conv_id']}] {conv['title'][:30]} ({conv['message_count']} msgs)")
    print()


def show_providers(brain):
    all_p = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()
    for key, config in all_p.items():
        status = "✅" if key == current else ("🟢" if key in available else "🔴")
        print(f"   {status} {key} — {config['name']}")
    print()


def main():
    print_banner()

    brain = SpideyBrain()
    brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    # Voice init
    vm = None
    if VOICE_AVAILABLE:
        try:
            print("   ⏳ Loading voice system (small model for accuracy)...")
            vm = VoiceManager(whisper_model="small", tts_engine="edge")
            print(f"   🎤 Mic:   {'✅' if vm.is_input_available() else '❌'}")
            print(f"   🗣️ Voice: {'✅' if vm.is_output_available() else '❌'}")
            print(f"   🗣️ Voice: Jenny (US Female)")
        except Exception as e:
            print(f"   🎤 Error: {e}")
            vm = None

    log_startup(info['name'], settings.get_all())

    print(f"\n🕷️ Spidey: Hey {username}!")
    print(f"   🤖 {info['name']}")

    memories = brain.get_all_memories()
    if memories:
        print(f"   🧠 {len(memories)} memories!")

    print(f"\n   💡 'spidey beta' = Full voice mode!")
    print(f"   💡 'v' = One voice message")
    print(f"   💡 'speakmode' = Auto-speak all replies\n")

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
                print(f"\n🕷️ Bye {username}! ({count} msgs saved) 🕸️")
                if vm and vm.speak_enabled:
                    vm.speak(f"Bye {username}!")
                brain.close()
                break

            # === 🕷️ SPIDEY BETA MODE ===
            if cmd in ["spidey beta", "spideybeta", "beta"]:
                if vm and vm.is_input_available() and vm.is_output_available():
                    vm.spidey_beta_loop(brain)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            # === VOICE ===
            if cmd in ["v", "voice"]:
                if vm:
                    vm.voice_chat(brain, mode="fixed", duration=7)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "voice5":
                if vm:
                    vm.voice_chat(brain, mode="fixed", duration=5)
                continue

            if cmd == "voice10":
                if vm:
                    vm.voice_chat(brain, mode="fixed", duration=10)
                continue

            if cmd == "voiceauto":
                if vm:
                    vm.voice_chat(brain, mode="auto")
                continue

            # === SPEECH ===
            if cmd == "speakmode":
                if vm:
                    on = vm.toggle_speak()
                    print(f"\n   🔊 Speak: {'ON 🟢' if on else 'OFF 🔴'}")
                    if on:
                        vm.speak("Speak mode on! I will speak all responses!")
                    print()
                continue

            if cmd == "saytest":
                if vm:
                    vm.test_speak()
                continue

            if cmd == "speak":
                if vm:
                    t = input("   🗣️ Text: ").strip()
                    if t:
                        vm.speak(t)
                continue

            # === LANGUAGE ===
            if cmd == "urdu":
                if vm:
                    vm.set_language("ur")
                    print("   ✅ Urdu voice!")
                    vm.speak("Urdu voice activated!")
                continue

            if cmd == "english":
                if vm:
                    vm.set_language("en")
                    print("   ✅ English voice!")
                    vm.speak("Hello! English voice activated!")
                continue

            if cmd == "hindi":
                if vm:
                    vm.set_language("hi")
                    print("   ✅ Hindi voice!")
                    vm.speak("Hindi voice activated!")
                continue

            if cmd == "setvoice":
                if vm:
                    voices = vm.get_voices()
                    cv = vm.get_current_voice().get("voice", "")
                    for i, v in enumerate(voices, 1):
                        a = " ←" if v["id"] == cv else ""
                        print(f"   {i}. [{v['language']}] {v['name']}{a}")
                    try:
                        c = int(input("\n   🔢 Number: ").strip()) - 1
                        if 0 <= c < len(voices):
                            vm.voice_output.set_voice(voices[c]["id"])
                            print(f"   ✅ {voices[c]['name']}")
                            vm.speak(f"Hello! I am now {voices[c]['name']}!")
                    except (ValueError, IndexError):
                        print("   ❌ Invalid")
                continue

            if cmd == "voicestatus":
                if vm:
                    s = vm.get_status()
                    print(f"\n   🎤 Input:  {'✅' if s['voice_input'] else '❌'}")
                    print(f"   🗣️ Output: {'✅' if s['voice_output'] else '❌'}")
                    print(f"   🔊 Speak:  {'ON' if s['speak_enabled'] else 'OFF'}")
                    print(f"   🕷️ Beta:   {'ON' if s['spidey_beta'] else 'OFF'}")
                    v = s.get('current_voice', {})
                    print(f"   🗣️ Voice:  {v.get('voice', 'N/A')}")
                    print(f"   🌍 Lang:   {v.get('language', 'N/A')}")
                    print()
                continue

            if cmd == "mictest":
                if vm:
                    vm.test_mic()
                continue

            # === CHAT ===
            if cmd == "reset":
                brain.reset()
                print("\n🕷️ Fresh start!\n")
                continue
            if cmd == "count":
                print(f"\n📊 {brain.get_history_count()} messages\n")
                continue

            # === HISTORY ===
            if cmd == "history":
                show_history(brain)
                continue
            if cmd == "load":
                show_history(brain)
                convs = brain.get_all_conversations()
                if convs:
                    try:
                        i = int(input("🔢 Number: ").strip()) - 1
                        if 0 <= i < len(convs):
                            brain.load_conversation(convs[i]["conv_id"])
                            print("✅ Loaded!\n")
                    except (ValueError, IndexError):
                        pass
                continue
            if cmd == "delete":
                show_history(brain)
                convs = brain.get_all_conversations()
                if convs:
                    try:
                        i = int(input("🔢 Number: ").strip()) - 1
                        if 0 <= i < len(convs):
                            if input("⚠️ Delete? (y/n): ").strip().lower() in ["y", "yes"]:
                                brain.delete_conversation(convs[i]["conv_id"])
                                print("🗑️ Deleted!\n")
                    except (ValueError, IndexError):
                        pass
                continue

            # === SEARCH ===
            if cmd == "search":
                q = input("🔍 Search: ").strip()
                if q:
                    for m in (brain.search_chats(q) or [])[:5]:
                        print(f"   {'👤' if m['role']=='user' else '🕷️'} {m['content'][:60]}...")
                print()
                continue
            if cmd == "smart":
                q = input("🔍 Smart: ").strip()
                if q:
                    for r in (brain.semantic_search(q) or [])[:5]:
                        print(f"   📝 {r['content'][:60]}...")
                print()
                continue

            # === PROVIDERS ===
            if cmd == "provider":
                print(f"\n🤖 {brain.get_provider_info()['name']}\n")
                continue
            if cmd == "switch":
                show_providers(brain)
                c = input("🔢 Provider: ").strip().lower()
                if brain.switch_provider(c):
                    print("✅ Switched!\n")
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
                        print(f"   ✅ {v}\n")
                except ValueError:
                    pass
                continue
            if cmd == "name":
                v = input("   📝 Name: ").strip()
                if v:
                    settings.set("username", v)
                    print(f"   ✅ {v}\n")
                continue

            # === MEMORY ===
            if cmd == "remember":
                k = input("   📝 Key: ").strip()
                v = input("   📝 Value: ").strip() if k else ""
                if k and v:
                    brain.remember(k, v, input("   📁 Category: ").strip() or "general")
                    print(f"   ✅ {k} = {v}\n")
                continue
            if cmd == "recall":
                k = input("   🧠 Key: ").strip()
                if k:
                    v = brain.recall(k)
                    print(f"   🧠 {k} = {v}\n" if v else "   ❌ Unknown\n")
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
                    print("   📭 Empty")
                print()
                continue
            if cmd == "forget":
                k = input("   🗑️ Key: ").strip()
                if k and brain.forget(k):
                    print(f"   ✅ Forgot!\n")
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
                    print(f"   {star}[{n['id']}] {n['title']}")
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

            if vm and vm.speak_enabled and response:
                vm.speak(response)

        except KeyboardInterrupt:
            log_shutdown(brain.get_history_count())
            print("\n\n🕷️ Bye!\n")
            brain.close()
            break


if __name__ == "__main__":
    main()