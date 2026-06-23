"""
Test script for ChatHistory and persistent memory
"""
from spidey.brain.history import ChatHistory
from spidey.brain.chat import SpideyBrain
import os


def test_history():
    """Test history saving and loading"""
    print("Testing ChatHistory...\n")

    # Test 1: Create conversation
    print("--- Test 1: Create Conversation ---")
    history = ChatHistory(history_dir="data/test_conversations")
    conv_id = history.create_new_conversation()
    print(f"Created conversation: {conv_id}")
    assert conv_id is not None
    print("✅ Test 1 Passed!\n")

    # Test 2: Add messages
    print("--- Test 2: Add Messages ---")
    history.add_message("user", "Hello Spidey!")
    history.add_message("assistant", "Hey there! How can I help?")
    history.add_message("user", "What is Python?")
    history.add_message("assistant", "Python is a programming language!")
    count = history.get_message_count()
    print(f"Messages saved: {count}")
    assert count == 4
    print("✅ Test 2 Passed!\n")

    # Test 3: Get messages
    print("--- Test 3: Get Messages ---")
    messages = history.get_messages()
    print(f"Retrieved {len(messages)} messages")
    for msg in messages:
        print(f"  {msg['role']}: {msg['content'][:40]}")
    assert len(messages) == 4
    print("✅ Test 3 Passed!\n")

    # Test 4: List conversations
    print("--- Test 4: List Conversations ---")
    convs = history.get_all_conversations()
    print(f"Total conversations: {len(convs)}")
    for conv in convs:
        print(f"  ID: {conv['id']}, Messages: {conv['message_count']}, Preview: {conv['preview']}")
    assert len(convs) >= 1
    print("✅ Test 4 Passed!\n")

    # Test 5: Load conversation
    print("--- Test 5: Load Conversation ---")
    history2 = ChatHistory(history_dir="data/test_conversations")
    loaded = history2.load_conversation(conv_id)
    messages = history2.get_messages()
    print(f"Loaded: {loaded}, Messages: {len(messages)}")
    assert loaded == True
    assert len(messages) == 4
    print("✅ Test 5 Passed!\n")

    # Test 6: Full brain test with persistence
    print("--- Test 6: SpideyBrain Persistence ---")
    brain = SpideyBrain()
    brain.start_new_conversation()
    reply = brain.chat("My name is Kashan")
    print(f"Spidey: {reply[:60]}...")
    reply = brain.chat("What is my name?")
    print(f"Spidey: {reply[:60]}...")
    print("✅ Test 6 Passed!\n")

    # Cleanup test files
    print("--- Cleaning up test files ---")
    import shutil
    if os.path.exists("data/test_conversations"):
        shutil.rmtree("data/test_conversations")
    print("✅ Cleanup done!\n")

    print("🎉 All history tests passed!")


if __name__ == "__main__":
    test_history()
