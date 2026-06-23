"""
Spidey AI — Main Entry Point (Updated with History Features)
Terminal mein interactive chatbot with save/load!
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
    print("   • Type 'quit' to exit")
    print("   • Type 'reset' to start new conversation")
    print("   • Type 'count' to see message count")
    print("   • Type 'history' to see past conversations")
    print("   • Type 'load' to load a past conversation")
    print("   • Type 'delete' to delete a conversation")
    print("=" * 55)
    print()


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
            confirm = input(f"⚠️ Delete conversation [{conv_id}]? (yes/no): ").strip()
            if confirm.lower() in ["yes", "y"]:
                if brain.delete_conversation(conv_id):
                    print(f"\n🗑️ Conversation [{conv_id}] deleted!\n")
                else:
                    print("\n❌ Could not delete conversation.\n")
            else:
                print("\n❌ Cancelled.\n")
        else:
            print("\n❌ Invalid number.\n")
    except ValueError:
        print("\n❌ Please enter a valid number.\n")


def main():
    """Main chat loop"""
    # Banner dikhao
    print_banner()

    # Spidey brain initialize karo
    brain = SpideyBrain()

    # Nayi conversation shuru karo
    conv_id = brain.start_new_conversation()

    print("🕷️ Spidey: Hey there! I'm Spidey AI. How can I help you today?")
    print(f"   (Conversation ID: {conv_id})")
    print()

    # Chat loop
    while True:
        try:
            user_input = input("👤 You: ").strip()

            # Empty input skip karo
            if not user_input:
                continue

            # Quit command
            if user_input.lower() in ["quit", "exit", "bye", "q"]:
                count = brain.get_history_count()
                print()
                print(f"🕷️ Spidey: See you later! Chat saved with {count} messages! 🕸️")
                print()
                break

            # Reset command
            if user_input.lower() == "reset":
                brain.reset()
                print()
                print("🕷️ Spidey: New conversation started! Let's go! 🔄")
                print()
                continue

            # Count command
            if user_input.lower() == "count":
                count = brain.get_history_count()
                print(f"\n📊 Messages in this conversation: {count}\n")
                continue

            # History command
            if user_input.lower() == "history":
                show_history(brain)
                continue

            # Load command
            if user_input.lower() == "load":
                load_conversation(brain)
                continue

            # Delete command
            if user_input.lower() == "delete":
                delete_conversation(brain)
                continue

            # AI se jawab lo
            print()
            print("🕷️ Spidey: ", end="")
            response = brain.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\n🕷️ Spidey: Caught ya! Chat saved! See you next time! 🕸️\n")
            break


if __name__ == "__main__":
    main()
