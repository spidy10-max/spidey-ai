"""
Spidey AI — Main Entry Point (Updated with Database Memory)
Now with remember/recall, notes, search, and stats!
"""
from spidey.brain.chat import SpideyBrain
from spidey.config import settings, APP_NAME, APP_VERSION, LOGS_DIR
from spidey.logger import log_startup, log_shutdown, log_event
import os


def print_banner():
    """Spidey AI welcome banner"""
    print()
    print("=" * 55)
    print(f"   🕷️  {APP_NAME} v{APP_VERSION}  🕷️")
    print("=" * 55)
    print("   Your friendly neighborhood AI!")
    print()
    print("   Chat:     quit | reset | count")
    print("   History:  history | load | delete | search")
    print("   Provider: provider | switch | models")
    print("   Settings: settings | set | tokens | temp | name")
    print("   Memory:   remember | recall | memories | forget")
    print("   Notes:    note | notes | delnote")
    print("   Other:    stats | logs")
    print("=" * 55)
    print()


def show_history(brain):
    """Show all conversations"""
    conversations = brain.get_all_conversations()
    if not conversations:
        print("\n📭 No saved conversations.\n")
        return

    print("\n" + "=" * 55)
    print("   📂 SAVED CONVERSATIONS")
    print("=" * 55)

    for i, conv in enumerate(conversations, 1):
        print(f"\n   {i}. [{conv['conv_id']}]")
        print(f"      📅 {conv['created_at'][:19]}")
        print(f"      💬 {conv['message_count']} messages")
        print(f"      📝 {conv['title']}")
        print(f"      🤖 {conv['provider']}")

    print("\n" + "=" * 55)
    print()


def load_conversation(brain):
    """Load past conversation"""
    show_history(brain)
    conversations = brain.get_all_conversations()
    if not conversations:
        return

    conv_input = input("🔢 Number to load: ").strip()
    try:
        index = int(conv_input) - 1
        if 0 <= index < len(conversations):
            conv_id = conversations[index]["conv_id"]
            if brain.load_conversation(conv_id):
                count = brain.get_history_count()
                print(f"\n✅ Loaded [{conv_id}] — {count} messages!")
                print("🕷️ Spidey: I remember our chat! Let's continue.\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Enter a number.\n")


def delete_conversation(brain):
    """Delete conversation"""
    show_history(brain)
    conversations = brain.get_all_conversations()
    if not conversations:
        return

    conv_input = input("🔢 Number to delete: ").strip()
    try:
        index = int(conv_input) - 1
        if 0 <= index < len(conversations):
            conv_id = conversations[index]["conv_id"]
            confirm = input(f"⚠️ Delete [{conv_id}]? (yes/no): ").strip()
            if confirm.lower() in ["yes", "y"]:
                if brain.delete_conversation(conv_id):
                    print(f"\n🗑️ Deleted!\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Enter a number.\n")


def search_chats(brain):
    """Search across all messages"""
    query = input("🔍 Search: ").strip()
    if not query:
        return

    results = brain.search_chats(query)
    if not results:
        print(f"\n📭 No messages found for '{query}'.\n")
        return

    print(f"\n🔍 Found {len(results)} messages:\n")
    for msg in results[:10]:
        role_icon = "👤" if msg["role"] == "user" else "🕷️"
        content = msg["content"][:60]
        conv_title = msg.get("conv_title", "Unknown")
        print(f"   {role_icon} {content}...")
        print(f"      📂 {conv_title} | 📅 {msg['created_at'][:19]}")
        print()


def show_providers(brain):
    """Show all providers"""
    all_providers = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()

    print("\n" + "=" * 55)
    print("   🤖 AI PROVIDERS")
    print("=" * 55)

    for i, (key, config) in enumerate(all_providers.items(), 1):
        if key == current:
            status = "✅ ACTIVE"
        elif key in available:
            status = "🟢 Ready"
        else:
            status = "🔴 No key"

        free_tag = "FREE" if config["free"] else "PAID"
        print(f"\n   {i}. {key} — {config['name']}")
        print(f"      {status} | {free_tag}")

    print("\n" + "=" * 55)
    print()


def switch_provider(brain):
    """Switch provider"""
    show_providers(brain)
    provider_keys = list(brain.list_providers().keys())
    print("   Available:", ", ".join(provider_keys))
    choice = input("\n🔢 Provider name: ").strip().lower()

    if choice in provider_keys:
        if brain.switch_provider(choice):
            info = brain.get_provider_info()
            print(f"\n✅ Switched to {info['name']}!\n")
        else:
            print("\n❌ Could not switch.\n")
    else:
        print(f"\n❌ Unknown: {choice}\n")


def show_settings():
    """Show settings"""
    print(settings)


def change_setting(brain):
    """Change a setting"""
    print("\n⚙️  Settings: temperature | max_tokens | username | show_tokens | theme")
    choice = input("   Setting: ").strip().lower()

    if choice == "temperature":
        try:
            value = float(input("   Value (0.0-2.0): "))
            if 0.0 <= value <= 2.0:
                settings.set("temperature", value)
                brain.update_settings()
                print(f"   ✅ Temperature: {value}\n")
        except ValueError:
            print("   ❌ Enter a number\n")

    elif choice == "max_tokens":
        try:
            value = int(input("   Value (100-4096): "))
            if 100 <= value <= 4096:
                settings.set("max_tokens", value)
                brain.update_settings()
                print(f"   ✅ Max tokens: {value}\n")
        except ValueError:
            print("   ❌ Enter a number\n")

    elif choice == "username":
        value = input("   Name: ").strip()
        if value:
            settings.set("username", value)
            brain.memory.update_user(username=value)
            print(f"   ✅ Name: {value}\n")

    elif choice == "show_tokens":
        current = settings.get("show_tokens", False)
        settings.set("show_tokens", not current)
        brain.update_settings()
        print(f"   ✅ Tokens: {'ON' if not current else 'OFF'}\n")

    elif choice == "theme":
        value = input("   Theme (dark/light): ").strip().lower()
        if value in ["dark", "light"]:
            settings.set("theme", value)
            print(f"   ✅ Theme: {value}\n")

    else:
        print(f"   ❌ Unknown: {choice}\n")


def remember_something(brain):
    """Remember a fact about user"""
    key = input("   📝 What to remember (e.g., favorite_color): ").strip()
    if not key:
        return
    value = input(f"   📝 Value for '{key}': ").strip()
    if not value:
        return

    categories = "general, personal, coding, work, hobby"
    category = input(f"   📁 Category ({categories}): ").strip() or "general"

    if brain.remember(key, value, category):
        print(f"\n   ✅ Remembered: {key} = {value} ({category})\n")
    else:
        print("\n   ❌ Could not save.\n")


def recall_something(brain):
    """Recall a specific memory"""
    key = input("   🧠 What to recall: ").strip()
    if not key:
        return

    value = brain.recall(key)
    if value:
        print(f"\n   🧠 {key} = {value}\n")
    else:
        print(f"\n   ❌ I don't remember '{key}'\n")


def show_memories(brain):
    """Show all memories"""
    memories = brain.get_all_memories()
    if not memories:
        print("\n📭 No memories saved yet.\n")
        return

    print("\n" + "=" * 55)
    print("   🧠 SPIDEY'S MEMORIES")
    print("=" * 55)

    current_category = ""
    for key, info in memories.items():
        if info["category"] != current_category:
            current_category = info["category"]
            print(f"\n   📁 {current_category.upper()}")

        print(f"      • {key}: {info['value']}")

    print("\n" + "=" * 55)
    print()


def forget_something(brain):
    """Forget a memory"""
    show_memories(brain)
    key = input("   🗑️ What to forget: ").strip()
    if key:
        if brain.forget(key):
            print(f"\n   ✅ Forgot: {key}\n")
        else:
            print(f"\n   ❌ Could not forget '{key}'\n")


def add_note(brain):
    """Add a new note"""
    title = input("   📝 Note title: ").strip()
    if not title:
        return
    content = input("   📝 Note content: ").strip()
    if not content:
        return
    category = input("   📁 Category (general/study/work/personal): ").strip() or "general"
    important = input("   ⭐ Important? (yes/no): ").strip().lower() in ["yes", "y"]

    if brain.add_note(title, content, category, important):
        star = " ⭐" if important else ""
        print(f"\n   ✅ Note added: {title}{star}\n")


def show_notes(brain):
    """Show all notes"""
    notes = brain.get_notes()
    if not notes:
        print("\n📭 No notes yet.\n")
        return

    print("\n" + "=" * 55)
    print("   📝 YOUR NOTES")
    print("=" * 55)

    for note in notes:
        star = "⭐ " if note["is_important"] else "   "
        print(f"\n   {star}[{note['id']}] {note['title']}")
        print(f"      {note['content'][:50]}")
        print(f"      📁 {note['category']} | 📅 {note['created_at'][:19]}")

    print("\n" + "=" * 55)
    print()


def delete_note(brain):
    """Delete a note"""
    show_notes(brain)
    try:
        note_id = int(input("   🗑️ Note ID to delete: ").strip())
        if brain.delete_note(note_id):
            print(f"\n   ✅ Note deleted!\n")
        else:
            print("\n   ❌ Could not delete.\n")
    except ValueError:
        print("\n   ❌ Enter a valid ID.\n")


def show_stats(brain):
    """Show database statistics"""
    stats = brain.get_stats()

    print("\n" + "=" * 55)
    print("   📊 SPIDEY STATS")
    print("=" * 55)
    print(f"\n   💬 Conversations: {stats['total_conversations']}")
    print(f"   📨 Total Messages: {stats['total_messages']}")
    print(f"      👤 User: {stats['user_messages']}")
    print(f"      🕷️ Spidey: {stats['ai_messages']}")
    print(f"   🔢 Total Tokens: {stats['total_tokens']}")
    print(f"   📝 Notes: {stats['total_notes']}")
    print(f"   🧠 Memories: {stats['total_preferences']}")
    print("\n" + "=" * 55)
    print()


def show_logs():
    """Show log files"""
    if not os.path.exists(LOGS_DIR):
        print("\n📭 No logs yet.\n")
        return

    print("\n" + "=" * 55)
    print("   📋 LOG FILES")
    print("=" * 55)

    files = sorted(os.listdir(LOGS_DIR), reverse=True)
    for f in files[:10]:
        filepath = os.path.join(LOGS_DIR, f)
        size = round(os.path.getsize(filepath) / 1024, 1)
        print(f"\n   📄 {f} ({size} KB)")

    print(f"\n   📁 {LOGS_DIR}")
    print("=" * 55)
    print()


def main():
    """Main chat loop"""
    print_banner()

    brain = SpideyBrain()
    conv_id = brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    log_startup(info['name'], settings.get_all())

    print(f"🕷️ Spidey: Hey {username}! I'm Spidey AI!")
    print(f"   🤖 {info['name']}")
    print(f"   🌡️ Temp: {settings.get('temperature')} | 📏 Max: {settings.get('max_tokens')}")

    # Show memory context
    memories = brain.get_all_memories()
    if memories:
        print(f"   🧠 I remember {len(memories)} things about you!")

    stats = brain.get_stats()
    if stats['total_conversations'] > 0:
        print(f"   📊 Total: {stats['total_conversations']} chats, {stats['total_messages']} messages")

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
            if cmd == "search":
                search_chats(brain)
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
                show_settings()
                continue
            if cmd == "set":
                change_setting(brain)
                continue
            if cmd == "tokens":
                current = settings.get("show_tokens", False)
                settings.set("show_tokens", not current)
                brain.update_settings()
                print(f"\n📊 Tokens: {'ON' if not current else 'OFF'}\n")
                continue
            if cmd == "temp":
                try:
                    value = float(input("   🌡️ Temperature (0.0-2.0): "))
                    if 0.0 <= value <= 2.0:
                        settings.set("temperature", value)
                        brain.update_settings()
                        print(f"   ✅ Temperature: {value}\n")
                except ValueError:
                    print("   ❌ Enter a number\n")
                continue
            if cmd == "name":
                new_name = input("   📝 Your name: ").strip()
                if new_name:
                    settings.set("username", new_name)
                    brain.memory.update_user(username=new_name)
                    print(f"   ✅ Name: {new_name}\n")
                continue

            # === MEMORY ===
            if cmd == "remember":
                remember_something(brain)
                continue
            if cmd == "recall":
                recall_something(brain)
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
            print("\n\n🕷️ Spidey: Chat saved! Bye! 🕸️\n")
            brain.close()
            break


if __name__ == "__main__":
    main()
