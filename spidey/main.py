"""
Spidey AI — Main Entry Point
Terminal mein interactive chatbot
"""
from spidey.brain.chat import SpideyBrain


def print_banner():
    """Spidey AI ka welcome banner"""
    print()
    print("=" * 50)
    print("   🕷️  SPIDEY AI ASSISTANT  🕷️")
    print("=" * 50)
    print("   Your friendly neighborhood AI!")
    print()
    print("   Commands:")
    print("   • Type your message and press Enter")
    print("   • Type 'quit' to exit")
    print("   • Type 'reset' to start new conversation")
    print("   • Type 'count' to see message count")
    print("=" * 50)
    print()


def main():
    """Main chat loop"""
    # Banner dikhao
    print_banner()

    # Spidey brain initialize karo
    brain = SpideyBrain()

    print("🕷️ Spidey: Hey there! I'm Spidey AI. How can I help you today?")
    print()

    # Chat loop — jab tak user quit na kare
    while True:
        try:
            # User se input lo
            user_input = input("👤 You: ").strip()

            # Empty input skip karo
            if not user_input:
                continue

            # Quit command
            if user_input.lower() in ["quit", "exit", "bye", "q"]:
                print()
                print("🕷️ Spidey: See you later! Stay amazing! 🕸️")
                print()
                break

            # Reset command
            if user_input.lower() == "reset":
                brain.reset()
                print()
                print("🕷️ Spidey: Conversation reset! Let's start fresh! 🔄")
                print()
                continue

            # Count command
            if user_input.lower() == "count":
                count = brain.get_history_count()
                print(f"\n📊 Messages so far: {count}\n")
                continue

            # AI se jawab lo
            print()
            print("🕷️ Spidey: ", end="")
            response = brain.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\n🕷️ Spidey: Caught ya! See you next time! 🕸️\n")
            break


if __name__ == "__main__":
    main()
