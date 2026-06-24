"""
Spidey AI — Main Entry Point (With Voice Input!)
Now you can SPEAK to Spidey! 🎤
"""
from spidey.brain.chat import SpideyBrain
from spidey.config import settings, APP_NAME, APP_VERSION, LOGS_DIR
from spidey.logger import log_startup, log_shutdown
import os


# Try to import voice
try:
    from spidey.voice.voice_input import VoiceInput
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
    print("   Voice:    voice | v | voice5 | voice10 | voiceauto | mictest")
    print("   Other:    stats | logs")
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
            if input(f"⚠️ Delete [{conv_id}]? (y/n): ").strip().lower() in ["y", "yes"]:
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
    print(f"\n🔍 Found {len(results)} summaries:\n")
    for r in results:
        print(f"   📝 {r['content'][:60]}...")
    print()


def show_providers(brain):
    all_p = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()
    print("\n" + "=" * 55)
    print("   🤖 PROVIDERS")
    print("=" * 55)
    for key, config in all_p.items():
        status = "✅" if key == current else ("🟢" if key in available else "🔴")
        free = "FREE" if config["free"] else "PAID"
        print(f"   {status} {key} — {config['name']} ({free})")
    print("=" * 55 + "\n")


def switch_provider(brain):
    show_providers(brain)
    choice = input("🔢 Provider: ").strip().lower()
    if brain.switch_provider(choice):
        info = brain.get_provider_info()
        print(f"\n✅ Switched to {info['name']}!\n")
    else:
        print("\n❌ Could not switch.\n")


def remember_something(brain):
    key = input("   📝 Key: ").strip()
    if not key:
        return
    value = input(f"   📝 Value: ").strip()
    if not value:
        return
    category = input("   📁 Category (general/personal/coding/work): ").strip() or "general"
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
    print(f"\n   🧠 Found {len(results)} memories:\n")
    for r in results:
        print(f"      • {r['content']}")
    print()


def show_memories(brain):
    memories = brain.get_all_memories()
    if not memories:
        print("\n📭 No memories.\n")
        return
    print("\n" + "=" * 55)
    print("   🧠 MEMORIES")
    print("=" * 55)
    for key, info in memories.items():
        print(f"   • {key}: {info['value']} ({info['category']})")
    print("=" * 55 + "\n")


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
    print("\n" + "=" * 55)
    print("   📝 NOTES")
    print("=" * 55)
    for note in notes:
        star = "⭐" if note["is_important"] else "  "
        print(f"   {star} [{note['id']}] {note['title']}")
        print(f"      {note['content'][:50]}")
    print("=" * 55 + "\n")


def find_note(brain):
    query = input("   🔍 Search notes: ").strip()
    if not query:
        return
    results = brain.search_notes(query)
    if not results:
        print(f"\n   ❌ No notes found.\n")
        return
    print(f"\n   📝 Found {len(results)} notes:\n")
    for r in results:
        print(f"      • {r['content'][:60]}...")
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
    print("\n" + "=" * 55)
    print("   📊 SPIDEY STATS")
    print("=" * 55)
    print(f"   💬 Conversations: {stats['total_conversations']}")
    print(f"   📨 Messages: {stats['total_messages']}")
    print(f"      👤 User: {stats['user_messages']}")
    print(f"      🕷️ AI: {stats['ai_messages']}")
    print(f"   🔢 Tokens: {stats['total_tokens']}")
    print(f"   📝 Notes: {stats['total_notes']}")
    print(f"   🧠 Memories: {stats['total_preferences']}")
    print(f"   🔍 Vectors: {stats.get('vector_messages', 0)}")
    print("=" * 55 + "\n")


def show_logs():
    if not os.path.exists(LOGS_DIR):
        print("\n📭 No logs.\n")
        return
    files = sorted(os.listdir(LOGS_DIR), reverse=True)
    print("\n📋 Logs:")
    for f in files[:5]:
        size = round(os.path.getsize(os.path.join(LOGS_DIR, f)) / 1024, 1)
        print(f"   📄 {f} ({size} KB)")
    print()


def handle_voice_input(voice, mode="fixed", duration=5):
    """Handle voice input and return text"""
    if not voice or not voice.is_available():
        print("\n   ❌ Voice not available!\n")
        return None

    text = voice.listen(mode=mode, duration=duration)
    return text


def main():
    print_banner()

    brain = SpideyBrain()
    conv_id = brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    # Initialize voice
    voice = None
    if VOICE_AVAILABLE:
        try:
            voice = VoiceInput(whisper_model="base")
            if voice.is_available():
                print("   🎤 Voice input: READY")
            else:
                print("   🎤 Voice input: NOT AVAILABLE")
                voice = None
        except Exception as e:
            print(f"   🎤 Voice error: {e}")
            voice = None

    log_startup(info['name'], settings.get_all())

    print(f"\n🕷️ Spidey: Hey {username}! How can I help?")
    print(f"   🤖 {info['name']}")

    memories = brain.get_all_memories()
    if memories:
        print(f"   🧠 I remember {len(memories)} things about you!")

    print(f"   💡 Type 'voice' or 'v' to speak!")
    print()

    while True:
        try:
            provider = brain.get_provider_name()
            username = settings.get("username", "User")
            user_input = input(f"👤 {username} [{provider}]: ").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            # === QUIT ===
            if cmd in ["quit", "exit", "bye", "q"]:
                count = brain.get_history_count()
                log_shutdown(count)
                print(f"\n🕷️ Spidey: Bye {username}! ({count} msgs saved) 🕸️\n")
                brain.close()
                break

            # === VOICE COMMANDS ===
            if cmd in ["voice", "v"]:
                text = handle_voice_input(voice, mode="fixed", duration=5)
                if text:
                    print()
                    print("🕷️ Spidey: ", end="")
                    response = brain.chat(text)
                    print(response)
                    print()
                continue

            if cmd == "voice5":
                text = handle_voice_input(voice, mode="fixed", duration=5)
                if text:
                    print()
                    print("🕷️ Spidey: ", end="")
                    response = brain.chat(text)
                    print(response)
                    print()
                continue

            if cmd == "voice10":
                text = handle_voice_input(voice, mode="fixed", duration=10)
                if text:
                    print()
                    print("🕷️ Spidey: ", end="")
                    response = brain.chat(text)
                    print(response)
                    print()
                continue

            if cmd == "voiceauto":
                text = handle_voice_input(voice, mode="auto")
                if text:
                    print()
                    print("🕷️ Spidey: ", end="")
                    response = brain.chat(text)
                    print(response)
                    print()
                continue

            if cmd == "mictest":
                if voice:
                    voice.test_mic()
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
                        v = float(input("   Value (0.0-2.0): "))
                        if 0.0 <= v <= 2.0:
                            settings.set("temperature", v)
                            brain.update_settings()
                            print(f"   ✅ Temperature: {v}\n")
                    except ValueError:
                        print("   ❌ Enter a number\n")
                elif choice == "max_tokens":
                    try:
                        v = int(input("   Value (100-4096): "))
                        if 100 <= v <= 4096:
                            settings.set("max_tokens", v)
                            brain.update_settings()
                            print(f"   ✅ Max tokens: {v}\n")
                    except ValueError:
                        print("   ❌ Enter a number\n")
                elif choice == "username":
                    v = input("   Name: ").strip()
                    if v:
                        settings.set("username", v)
                        brain.memory.update_user(username=v)
                        print(f"   ✅ Name: {v}\n")
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
                    v = float(input("   🌡️ Temperature (0.0-2.0): "))
                    if 0.0 <= v <= 2.0:
                        settings.set("temperature", v)
                        brain.update_settings()
                        print(f"   ✅ Temperature: {v}\n")
                except ValueError:
                    print("   ❌ Enter a number\n")
                continue
            if cmd == "name":
                v = input("   📝 Name: ").strip()
                if v:
                    settings.set("username", v)
                    print(f"   ✅ Name: {v}\n")
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
                show_logs()
                continue

            # === AI CHAT ===
            print()
            print("🕷️ Spidey: ", end="")
            response = brain.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            log_shutdown(brain.get_history_count())
            print("\n\n🕷️ Spidey: Bye! 🕸️\n")
            brain.close()
            break


if __name__ == "__main__":
    main()