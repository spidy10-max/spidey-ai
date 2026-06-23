"""
Spidey AI — Main Entry Point (Updated with Settings)
Now with full settings management!
"""
from spidey.brain.chat import SpideyBrain
from spidey.config import settings, APP_NAME, APP_VERSION


def print_banner():
    """Spidey AI ka welcome banner"""
    print()
    print("=" * 55)
    print(f"   🕷️  {APP_NAME} v{APP_VERSION}  🕷️")
    print("=" * 55)
    print("   Your friendly neighborhood AI!")
    print()
    print("   Chat Commands:")
    print("   • 'quit'      — Exit the app")
    print("   • 'reset'     — New conversation")
    print("   • 'count'     — Message count")
    print()
    print("   History Commands:")
    print("   • 'history'   — Past conversations")
    print("   • 'load'      — Load conversation")
    print("   • 'delete'    — Delete conversation")
    print()
    print("   Provider Commands:")
    print("   • 'provider'  — Current AI provider")
    print("   • 'switch'    — Switch AI provider")
    print("   • 'models'    — List all providers")
    print()
    print("   Settings Commands:")
    print("   • 'settings'  — View all settings")
    print("   • 'set'       — Change a setting")
    print("   • 'tokens'    — Toggle token display")
    print("   • 'temp'      — Change temperature")
    print("   • 'name'      — Set your name")
    print("=" * 55)
    print()


def show_settings():
    """Display current settings"""
    print(settings)


def change_setting(brain):
    """Change a specific setting"""
    print("\n⚙️  Changeable Settings:")
    print("   1. temperature  — AI creativity (0.0 - 2.0)")
    print("   2. max_tokens   — Max response length (100 - 4096)")
    print("   3. username     — Your name")
    print("   4. show_tokens  — Show token usage (true/false)")
    print("   5. theme        — dark / light")
    print()

    choice = input("   Enter setting name: ").strip().lower()

    if choice == "temperature":
        try:
            value = float(input("   New temperature (0.0 - 2.0): "))
            if 0.0 <= value <= 2.0:
                settings.set("temperature", value)
                brain.update_settings()
                print(f"   ✅ Temperature set to {value}\n")
            else:
                print("   ❌ Must be between 0.0 and 2.0\n")
        except ValueError:
            print("   ❌ Enter a valid number\n")

    elif choice == "max_tokens":
        try:
            value = int(input("   New max tokens (100 - 4096): "))
            if 100 <= value <= 4096:
                settings.set("max_tokens", value)
                brain.update_settings()
                print(f"   ✅ Max tokens set to {value}\n")
            else:
                print("   ❌ Must be between 100 and 4096\n")
        except ValueError:
            print("   ❌ Enter a valid number\n")

    elif choice == "username":
        value = input("   Your name: ").strip()
        if value:
            settings.set("username", value)
            print(f"   ✅ Name set to {value}\n")
        else:
            print("   ❌ Name cannot be empty\n")

    elif choice == "show_tokens":
        current = settings.get("show_tokens", False)
        new_value = not current
        settings.set("show_tokens", new_value)
        brain.update_settings()
        status = "ON" if new_value else "OFF"
        print(f"   ✅ Token display: {status}\n")

    elif choice == "theme":
        value = input("   Theme (dark/light): ").strip().lower()
        if value in ["dark", "light"]:
            settings.set("theme", value)
            print(f"   ✅ Theme set to {value}\n")
        else:
            print("   ❌ Choose 'dark' or 'light'\n")

    else:
        print(f"   ❌ Unknown setting: {choice}\n")


def show_providers(brain):
    """Show all available AI providers"""
    all_providers = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()

    print("\n" + "=" * 55)
    print("   🤖 AVAILABLE AI PROVIDERS")
    print("=" * 55)

    for i, (key, config) in enumerate(all_providers.items(), 1):
        if key == current:
            status = "✅ ACTIVE"
        elif key in available:
            status = "🟢 Ready"
        else:
            status = "🔴 No API key"

        free_tag = "FREE" if config["free"] else "PAID"

        print(f"\n   {i}. {key}")
        print(f"      Name: {config['name']}")
        print(f"      Model: {config['model']}")
        print(f"      Status: {status} | {free_tag}")

    print("\n" + "=" * 55)
    print()


def switch_provider(brain):
    """Switch AI provider"""
    show_providers(brain)

    all_providers = brain.list_providers()
    provider_keys = list(all_providers.keys())

    print("   Available:", ", ".join(provider_keys))
    choice = input("\n🔢 Enter provider name: ").strip().lower()

    if choice in provider_keys:
        if brain.switch_provider(choice):
            info = brain.get_provider_info()
            print(f"\n✅ Switched to {info['name']}!")
            print(f"   Model: {info['model']}\n")
        else:
            print("\n❌ Could not switch. Check API key.\n")
    else:
        print(f"\n❌ Unknown: {choice}\n")


def show_history(brain):
    """Show saved conversations"""
    conversations = brain.get_all_conversations()

    if not conversations:
        print("\n📭 No saved conversations yet.\n")
        return

    print("\n" + "=" * 55)
    print("   📂 SAVED CONVERSATIONS")
    print("=" * 55)

    for i, conv in enumerate(conversations, 1):
        print(f"\n   {i}. [{conv['id']}]")
        print(f"      📅 {conv['created_at'][:19]}")
        print(f"      💬 {conv['message_count']} messages")
        print(f"      📝 {conv['preview']}")

    print("\n" + "=" * 55)
    print()


def load_conversation(brain):
    """Load a past conversation"""
    show_history(brain)
    conversations = brain.get_all_conversations()
    if not conversations:
        return

    conv_input = input("🔢 Enter number to load: ").strip()
    try:
        index = int(conv_input) - 1
        if 0 <= index < len(conversations):
            conv_id = conversations[index]["id"]
            if brain.load_conversation(conv_id):
                count = brain.get_history_count()
                print(f"\n✅ Loaded [{conv_id}] with {count} messages!\n")
            else:
                print("\n❌ Could not load.\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Enter a valid number.\n")


def delete_conversation(brain):
    """Delete a conversation"""
    show_history(brain)
    conversations = brain.get_all_conversations()
    if not conversations:
        return

    conv_input = input("🔢 Enter number to delete: ").strip()
    try:
        index = int(conv_input) - 1
        if 0 <= index < len(conversations):
            conv_id = conversations[index]["id"]
            confirm = input(f"⚠️ Delete [{conv_id}]? (yes/no): ").strip()
            if confirm.lower() in ["yes", "y"]:
                if brain.delete_conversation(conv_id):
                    print(f"\n🗑️ Deleted [{conv_id}]!\n")
            else:
                print("\n❌ Cancelled.\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Enter a valid number.\n")


def main():
    """Main chat loop"""
    print_banner()

    brain = SpideyBrain()

    conv_id = brain.start_new_conversation()
    info = brain.get_provider_info()
    username = settings.get("username", "User")

    print(f"🕷️ Spidey: Hey {username}! I'm Spidey AI. How can I help?")
    print(f"   🤖 Brain: {info['name']}")
    print(f"   🌡️ Temp: {settings.get('temperature')} | 📏 Max: {settings.get('max_tokens')}")
    print()

    while True:
        try:
            provider = brain.get_provider_name()
            username = settings.get("username", "User")
            user_input = input(f"👤 {username} [{provider}]: ").strip()

            if not user_input:
                continue

            # === QUIT ===
            if user_input.lower() in ["quit", "exit", "bye", "q"]:
                count = brain.get_history_count()
                print(f"\n🕷️ Spidey: Bye {username}! Chat saved ({count} msgs)! 🕸️\n")
                break

            # === CHAT COMMANDS ===
            if user_input.lower() == "reset":
                brain.reset()
                print("\n🕷️ Spidey: Fresh start! 🔄\n")
                continue

            if user_input.lower() == "count":
                print(f"\n📊 Messages: {brain.get_history_count()}\n")
                continue

            # === HISTORY COMMANDS ===
            if user_input.lower() == "history":
                show_history(brain)
                continue

            if user_input.lower() == "load":
                load_conversation(brain)
                continue

            if user_input.lower() == "delete":
                delete_conversation(brain)
                continue

            # === PROVIDER COMMANDS ===
            if user_input.lower() == "provider":
                info = brain.get_provider_info()
                print(f"\n🤖 {info['name']} | {info['model']}\n")
                continue

            if user_input.lower() == "switch":
                switch_provider(brain)
                continue

            if user_input.lower() == "models":
                show_providers(brain)
                continue

            # === SETTINGS COMMANDS ===
            if user_input.lower() == "settings":
                show_settings()
                continue

            if user_input.lower() == "set":
                change_setting(brain)
                continue

            if user_input.lower() == "tokens":
                current = settings.get("show_tokens", False)
                settings.set("show_tokens", not current)
                brain.update_settings()
                status = "ON" if not current else "OFF"
                print(f"\n📊 Token display: {status}\n")
                continue

            if user_input.lower() == "temp":
                try:
                    value = float(input("   🌡️ New temperature (0.0-2.0): "))
                    if 0.0 <= value <= 2.0:
                        settings.set("temperature", value)
                        brain.update_settings()
                        print(f"   ✅ Temperature: {value}\n")
                    else:
                        print("   ❌ Must be 0.0 - 2.0\n")
                except ValueError:
                    print("   ❌ Enter a number\n")
                continue

            if user_input.lower() == "name":
                new_name = input("   📝 Your name: ").strip()
                if new_name:
                    settings.set("username", new_name)
                    print(f"   ✅ Name: {new_name}\n")
                continue

            # === AI CHAT ===
            print()
            print("🕷️ Spidey: ", end="")
            response = brain.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\n🕷️ Spidey: Chat saved! Bye! 🕸️\n")
            break


if __name__ == "__main__":
    main()
