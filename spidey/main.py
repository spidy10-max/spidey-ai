"""
Spidey AI — Main Entry Point (Updated with Provider Switching)
Now you can switch AI brains on the fly!
"""
from spidey.brain.chat import SpideyBrain


def print_banner():
    """Spidey AI ka welcome banner"""
    print()
    print("=" * 55)
    print("   🕷️  SPIDEY AI ASSISTANT  🕷️")
    print("=" * 55)
    print("   Your friendly neighborhood AI!")
    print()
    print("   Commands:")
    print("   • Type your message and press Enter")
    print("   • 'quit'     — Exit the app")
    print("   • 'reset'    — Start new conversation")
    print("   • 'count'    — See message count")
    print("   • 'history'  — See past conversations")
    print("   • 'load'     — Load a past conversation")
    print("   • 'delete'   — Delete a conversation")
    print("   • 'provider' — See current AI provider")
    print("   • 'switch'   — Switch AI provider")
    print("   • 'models'   — List all available providers")
    print("=" * 55)
    print()


def show_providers(brain):
    """Show all available AI providers"""
    all_providers = brain.list_providers()
    available = brain.get_available_providers()
    current = brain.get_provider_name()

    print("\n" + "=" * 55)
    print("   🤖 AVAILABLE AI PROVIDERS")
    print("=" * 55)

    for i, (key, config) in enumerate(all_providers.items(), 1):
        # Status indicator
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
        print(f"      Info: {config['description']}")
        print(f"      Status: {status} | {free_tag}")

    print("\n" + "=" * 55)
    print()


def switch_provider(brain):
    """Switch to a different AI provider"""
    show_providers(brain)

    all_providers = brain.list_providers()
    provider_keys = list(all_providers.keys())

    print("   Available keys:", ", ".join(provider_keys))
    choice = input("\n🔢 Enter provider name to switch: ").strip().lower()

    if choice in provider_keys:
        if brain.switch_provider(choice):
            info = brain.get_provider_info()
            print(f"\n✅ Switched to {info['name']}!")
            print(f"   Model: {info['model']}")
            print(f"   {info['description']}\n")
        else:
            print("\n❌ Could not switch. Check your API key.\n")
    else:
        print(f"\n❌ Unknown provider: {choice}")
        print(f"   Available: {', '.join(provider_keys)}\n")


def show_history(brain):
    """Show all saved conversations"""
    conversations = brain.get_all_conversations()

    if not conversations:
        print("\n📭 No saved conversations yet.\n")
        return

    print("\n" + "=" * 55)
    print("   📂 SAVED CONVERSATIONS")
    print("=" * 55)

    for i, conv in enumerate(conversations, 1):
        print(f"\n   {i}. [{conv['id']}]")
        print(f"      📅 Date: {conv['created_at'][:19]}")
        print(f"      💬 Messages: {conv['message_count']}")
        print(f"      📝 Preview: {conv['preview']}")

    print("\n" + "=" * 55)
    print()


def load_conversation(brain):
    """Load a past conversation"""
    show_history(brain)

    conversations = brain.get_all_conversations()
    if not conversations:
        return

    conv_input = input("🔢 Enter conversation number to load: ").strip()

    try:
        index = int(conv_input) - 1
        if 0 <= index < len(conversations):
            conv_id = conversations[index]["id"]
            if brain.load_conversation(conv_id):
                count = brain.get_history_count()
                print(f"\n✅ Loaded conversation [{conv_id}] with {count} messages!")
                print("🕷️ Spidey: I remember our chat! Let's continue.\n")
            else:
                print("\n❌ Could not load conversation.\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Please enter a valid number.\n")


def delete_conversation(brain):
    """Delete a past conversation"""
    show_history(brain)

    conversations = brain.get_all_conversations()
    if not conversations:
        return

    conv_input = input("🔢 Enter conversation number to delete: ").strip()

    try:
        index = int(conv_input) - 1
        if 0 <= index < len(conversations):
            conv_id = conversations[index]["id"]
            confirm = input(f"⚠️ Delete [{conv_id}]? (yes/no): ").strip()
            if confirm.lower() in ["yes", "y"]:
                if brain.delete_conversation(conv_id):
                    print(f"\n🗑️ Conversation [{conv_id}] deleted!\n")
                else:
                    print("\n❌ Could not delete.\n")
            else:
                print("\n❌ Cancelled.\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Please enter a valid number.\n")


def main():
    """Main chat loop"""
    print_banner()

    # Spidey brain initialize karo
    brain = SpideyBrain(provider="groq")

    # Nayi conversation shuru karo
    conv_id = brain.start_new_conversation()

    # Current provider info
    info = brain.get_provider_info()

    print(f"🕷️ Spidey: Hey there! I'm Spidey AI. How can I help you today?")
    print(f"   🤖 Brain: {info['name']} | Model: {info['model']}")
    print(f"   💬 Conversation: {conv_id}")
    print()

    # Chat loop
    while True:
        try:
            # Show current provider in prompt
            provider = brain.get_provider_name()
            user_input = input(f"👤 You [{provider}]: ").strip()

            if not user_input:
                continue

            # Commands
            if user_input.lower() in ["quit", "exit", "bye", "q"]:
                count = brain.get_history_count()
                print(f"\n🕷️ Spidey: See you later! Chat saved ({count} messages)! 🕸️\n")
                break

            if user_input.lower() == "reset":
                brain.reset()
                print("\n🕷️ Spidey: New conversation started! 🔄\n")
                continue

            if user_input.lower() == "count":
                count = brain.get_history_count()
                print(f"\n📊 Messages: {count}\n")
                continue

            if user_input.lower() == "history":
                show_history(brain)
                continue

            if user_input.lower() == "load":
                load_conversation(brain)
                continue

            if user_input.lower() == "delete":
                delete_conversation(brain)
                continue

            if user_input.lower() == "provider":
                info = brain.get_provider_info()
                print(f"\n🤖 Current Provider: {info['name']}")
                print(f"   Model: {info['model']}")
                print(f"   {info['description']}\n")
                continue

            if user_input.lower() == "switch":
                switch_provider(brain)
                continue

            if user_input.lower() == "models":
                show_providers(brain)
                continue

            # AI se jawab lo
            print()
            print("🕷️ Spidey: ", end="")
            response = brain.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\n🕷️ Spidey: Chat saved! See you next time! 🕸️\n")
            break


if __name__ == "__main__":
    main()
