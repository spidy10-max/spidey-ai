"""
Spidey AI — Main Entry Point (Full Voice Support!)
Type OR Speak to Spidey — Spidey types AND speaks back!
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
    print("   Other:    stats | logs | mictest")
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
            conv_id = conversations[index]["conv_id"]
            if brain.load_conversation(conv_id):
                print(f"\n✅ Loaded [{conv_id}]!\n")
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
            conv_id = conversations[index]["conv_id"]
            if input(f"⚠️ Delete? (y/n): ").strip().lower() in ["y", "yes"]:
                if brain.delete_conversation(conv_id):
                    print(f"\n🗑️ Deleted!\n")
    except (ValueError, IndexError):
        print("\n❌ Invalid.\n")


def semantic_search(brain):
    query = input("🔍 Smart search: ").strip()
    if not query:
        return
    results = brain.semantic_search(query, n_results=5)
    if not results:
        print(f"\n📭 Nothing found.\n")
        return
    print(f"\n🔍 Found {len(results)} results:\n")
    for r in results:
        role = r.get("metadata", {}).get("role", "?")
        icon = "👤" if role == "user" else "🕷️"
        print(f"   {icon} {r['content'][:60]}...")
    print()


def search_exact(brain):
    query = input("🔍 Search: ").strip()
    if not query:
        return
    results = brain.search_chats(query)
    if not results:
        print(f"\n📭 Nothing found.\n")
        return
    print(f"\n🔍 Found {len(results)} results:\n")
    for msg in results[:10]:
        icon = "👤" if msg["role"] == "user" else "🕷️"
        print(f"   {icon} {msg['content'][:60]}...")
    print()


def search_summaries(brain):
    query = input("🔍 Search summaries: ").strip()
    if not query:
        return
    results = brain.search_summaries(query)
    if not results:
        print(f"\n📭 No summaries.\n")
        return
    for r in results:
        print(f"   📝 {r['content'][:60]}...")
    print()


def show_providers(brain):
    all_p = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()
    print("\n" + "=" * 55)
    for key, config in all_p.items():
        status = "✅" if key == current else ("🟢" if key in available else "🔴")
        free = "FREE" if config["free"] else "PAID"
        print(f"   {status} {key} — {config['name']} ({free})")
    print("=" * 55 + "\n")


def switch_provider(brain):
    show_providers(brain)
    choice = input("🔢 Provider: ").strip().lower()
    if brain.switch_provider(choice):
        print(f"\n✅ Switched!\n")
    else:
        print("\n❌ Could not switch.\n")


def remember_something(brain):
    key = input("   📝 Key: ").strip()
    if not key:
        return
    value = input(f"   📝 Value: ").strip()
    if not value:
        return
    category = input("   📁 Category: ").strip() or "general"
    if brain.remember(key, value, category):
        print(f"\n   ✅ Remembered: {key} = {value}\n")


def recall_something(brain):
    key = input("   🧠 Key: ").strip()
    if not key:
        return
    value = brain.recall(key)
    if value:
        print(f"\n   🧠 {key} = {value}\n")
    else:
        print(f"\n   ❌ Don't remember '{key}'\n")


def smart_recall(brain):
    query = input("   🧠 Smart recall: ").strip()
    if not query:
        return
    results = brain.smart_recall(query)
    if not results:
        print(f"\n   ❌ No memories found.\n")
        return
    for r in results:
        print(f"      • {r['content']}")
    print()


def show_memories(brain):
    memories = brain.get_all_memories()
    if not memories:
        print("\n📭 No memories.\n")
        return
    print("\n   🧠 MEMORIES:")
    for key, info in memories.items():
        print(f"   • {key}: {info['value']} ({info['category']})")
    print()


def forget_something(brain):
    show_memories(brain)
    key = input("   🗑️ Key: ").strip()
    if key and brain.forget(key):
        print(f"\n   ✅ Forgot: {key}\n")


def add_note(brain):
    title = input("   📝 Title: ").strip()
    if not title:
        return
    content = input("   📝 Content: ").strip()
    if not content:
        return
    category = input("   📁 Category: ").strip() or "general"
    important = input("   ⭐ Important? (y/n): ").strip().lower() in ["y", "yes"]
    if brain.add_note(title, content, category, important):
        print(f"\n   ✅ Note added!\n")


def show_notes(brain):
    notes = brain.get_notes()
    if not notes:
        print("\n📭 No notes.\n")
        return
    for note in notes:
        star = "⭐" if note["is_important"] else "  "
        print(f"   {star} [{note['id']}] {note['title']}: {note['content'][:40]}")
    print()


def find_note(brain):
    query = input("   🔍 Search: ").strip()
    if not query:
        return
    results = brain.search_notes(query)
    if results:
        for r in results:
            print(f"      • {r['content'][:60]}...")
    else:
        print("   ❌ Nothing found.")
    print()


def delete_note(brain):
    show_notes(brain)
    try:
        note_id = int(input("   🗑️ Note ID: ").strip())
        if brain.delete_note(note_id):
            print(f"\n   ✅ Deleted!\n")
    except ValueError:
        print("\n   ❌ Enter a number.\n")


def show_stats(brain):
    stats = brain.get_stats()
    print(f"\n   📊 STATS:")
    print(f"   💬 Conversations: {stats['total_conversations']}")
    print(f"   📨 Messages: {stats['total_messages']}")
    print(f"   🔢 Tokens: {stats['total_tokens']}")
    print(f"   📝 Notes: {stats['total_notes']}")
    print(f"   🧠 Memories: {stats['total_preferences']}")
    print()


def show_voice_status(vm):
    """Show voice system status"""
    status = vm.get_status()
    print("\n" + "=" * 55)
    print("   🎤 VOICE STATUS")
    print("=" * 55)
    print(f"   🎤 Input:  {'✅ Ready' if status['voice_input'] else '❌ Not available'}")
    print(f"   🗣️ Output: {'✅ Ready' if status['voice_output'] else '❌ Not available'}")
    print(f"   🔊 Speak mode: {'ON 🟢' if status['speak_enabled'] else 'OFF 🔴'}")
    print(f"   🎤 Listen mode: {status['listen_mode']}")
    print(f"   ⏱️ Duration: {status['listen_duration']}s")
    print(f"   🗣️ TTS Engine: {status['tts_engine']}")
    print("=" * 55 + "\n")


def show_voices(vm):
    """Show available voices"""
    voices = vm.get_voices()
    if not voices:
        print("\n   ❌ No voices available.\n")
        return
    print("\n   🗣️ AVAILABLE VOICES:")
    for v in voices:
        print(f"   [{v['engine']}] {v['name']}")
        print(f"      ID: {v['id']}")
    print()


def switch_tts(vm):
    """Switch TTS engine"""
    print("\n   TTS Engines:")
    print("   1. system — Offline (pyttsx3)")
    print("   2. edge   — Online, better quality (Microsoft)")
    choice = input("\n   Choose (system/edge): ").strip().lower()
    if vm.switch_tts_engine(choice):
        print(f"\n   ✅ Switched to {choice}!\n")
    else:
        print(f"\n   ❌ Could not switch.\n")


def main():
    print_banner()

    brain = SpideyBrain()
    conv_id = brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    # Initialize voice
    vm = None
    if VOICE_AVAILABLE:
        try:
            vm = VoiceManager(whisper_model="base", tts_engine="system")
            input_ok = vm.is_input_available()
            output_ok = vm.is_output_available()
            print(f"   🎤 Voice input:  {'✅ Ready' if input_ok else '❌ Not available'}")
            print(f"   🗣️ Voice output: {'✅ Ready' if output_ok else '❌ Not available'}")
        except Exception as e:
            print(f"   🎤 Voice error: {e}")
            vm = None
    else:
        print("   🎤 Voice: Not installed")

    log_startup(info['name'], settings.get_all())

    print(f"\n🕷️ Spidey: Hey {username}! How can I help?")
    print(f"   🤖 {info['name']}")

    memories = brain.get_all_memories()
    if memories:
        print(f"   🧠 I remember {len(memories)} things about you!")

    print(f"   💡 Type 'v' to speak | 'speakmode' for auto-speak")
    print()

    while True:
        try:
            provider = brain.get_provider_name()
            username = settings.get("username", "User")

            # Voice mode indicator
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
                print()
                brain.close()
                break

            # === VOICE INPUT COMMANDS ===
            if cmd in ["v", "voice"]:
                if vm:
                    user_text, ai_response = vm.voice_chat(brain, mode="fixed", duration=5)
                    if ai_response and vm.speak_enabled:
                        pass  # already spoken in voice_chat
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

            # === SPEECH OUTPUT COMMANDS ===
            if cmd == "speakmode":
                if vm:
                    enabled = vm.toggle_speak()
                    status = "ON 🟢" if enabled else "OFF 🔴"
                    print(f"\n   🔊 Speak mode: {status}")
                    if enabled:
                        print("   Spidey will now SPEAK all responses!")
                        vm.speak("Speak mode activated! I will now speak all my responses!")
                    else:
                        print("   Spidey will only type responses.")
                    print()
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "speak":
                if vm:
                    text = input("   🗣️ Text to speak: ").strip()
                    if text:
                        vm.speak(text)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "saytest":
                if vm:
                    print("   🗣️ Testing speech...")
                    vm.test_speak("Hello! I am Spidey AI, your friendly neighborhood assistant!")
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "tts":
                if vm:
                    switch_tts(vm)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "voices":
                if vm:
                    show_voices(vm)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "voicestatus":
                if vm:
                    show_voice_status(vm)
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            if cmd == "mictest":
                if vm:
                    vm.test_mic()
                else:
                    print("\n   ❌ Voice not available!\n")
                continue

            # === CHAT ===
            if cmd == "reset":
                brain.reset()
                print("\n🕷️ Spidey: Fresh start! 🔄\n")
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
                search_exact(brain)
                continue
            if cmd == "smart":
                semantic_search(brain)
                continue
            if cmd == "findsummary":
                search_summaries(brain)
                continue

            # === PROVIDERS ===
            if cmd == "provider":
                info = brain.get_provider_info()
                print(f"\n🤖 {info['name']} | {info['model']}\n")
                continue
            if cmd == "switch":
                switch_provider(brain)
                continue
            if cmd == "models":
                show_providers(brain)
                continue

            # === SETTINGS ===
            if cmd == "settings":
                print(settings)
                continue
            if cmd == "set":
                print("\n⚙️ temperature | max_tokens | username | show_tokens")
                choice = input("   Setting: ").strip().lower()
                if choice == "temperature":
                    try:
                        val = float(input("   Value (0.0-2.0): "))
                        if 0.0 <= val <= 2.0:
                            settings.set("temperature", val)
                            brain.update_settings()
                            print(f"   ✅ Temperature: {val}\n")
                    except ValueError:
                        print("   ❌ Enter a number\n")
                elif choice == "max_tokens":
                    try:
                        val = int(input("   Value (100-4096): "))
                        if 100 <= val <= 4096:
                            settings.set("max_tokens", val)
                            brain.update_settings()
                            print(f"   ✅ Max tokens: {val}\n")
                    except ValueError:
                        print("   ❌ Enter a number\n")
                elif choice == "username":
                    val = input("   Name: ").strip()
                    if val:
                        settings.set("username", val)
                        brain.memory.update_user(username=val)
                        print(f"   ✅ Name: {val}\n")
                elif choice == "show_tokens":
                    cur = settings.get("show_tokens", False)
                    settings.set("show_tokens", not cur)
                    brain.update_settings()
                    print(f"   ✅ Tokens: {'ON' if not cur else 'OFF'}\n")
                continue
            if cmd == "tokens":
                cur = settings.get("show_tokens", False)
                settings.set("show_tokens", not cur)
                brain.update_settings()
                print(f"\n📊 Tokens: {'ON' if not cur else 'OFF'}\n")
                continue
            if cmd == "temp":
                try:
                    val = float(input("   🌡️ Temperature (0.0-2.0): "))
                    if 0.0 <= val <= 2.0:
                        settings.set("temperature", val)
                        brain.update_settings()
                        print(f"   ✅ Temperature: {val}\n")
                except ValueError:
                    print("   ❌ Enter a number\n")
                continue
            if cmd == "name":
                val = input("   📝 Name: ").strip()
                if val:
                    settings.set("username", val)
                    print(f"   ✅ Name: {val}\n")
                continue

            # === MEMORY ===
            if cmd == "remember":
                remember_something(brain)
                continue
            if cmd == "recall":
                recall_something(brain)
                continue
            if cmd == "smartrecall":
                smart_recall(brain)
                continue
            if cmd == "memories":
                show_memories(brain)
                continue
            if cmd == "forget":
                forget_something(brain)
                continue

            # === NOTES ===
            if cmd == "note":
                add_note(brain)
                continue
            if cmd == "notes":
                show_notes(brain)
                continue
            if cmd == "findnote":
                find_note(brain)
                continue
            if cmd == "delnote":
                delete_note(brain)
                continue

            # === STATS & LOGS ===
            if cmd == "stats":
                show_stats(brain)
                continue
            if cmd == "logs":
                if os.path.exists(LOGS_DIR):
                    files = sorted(os.listdir(LOGS_DIR), reverse=True)
                    for f in files[:5]:
                        size = round(os.path.getsize(os.path.join(LOGS_DIR, f)) / 1024, 1)
                        print(f"   📄 {f} ({size} KB)")
                else:
                    print("   📭 No logs.")
                print()
                continue

            # === AI CHAT ===
            print()
            print("🕷️ Spidey: ", end="", flush=True)
            response = brain.chat(user_input)
            print(response)
            print()

            # Speak response if speak mode is ON
            if vm and vm.speak_enabled:
                vm.speak(response)

        except KeyboardInterrupt:
            log_shutdown(brain.get_history_count())
            print("\n\n🕷️ Spidey: Bye! 🕸️\n")
            brain.close()
            break


if __name__ == "__main__":
    main()