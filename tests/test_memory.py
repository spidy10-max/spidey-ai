"""
Test script for SpideyMemory
"""
from spidey.memory.memory import SpideyMemory
import os


def test_memory():
    """Test memory system"""
    print("Testing SpideyMemory...\n")

    memory = SpideyMemory()

    # Test 1: Start conversation
    print("--- Test 1: Start Conversation ---")
    conv_id = memory.start_conversation(provider="groq")
    print(f"  Conv ID: {conv_id}")
    assert conv_id is not None
    print("✅ Test 1 Passed!\n")

    # Test 2: Save messages
    print("--- Test 2: Save Messages ---")
    memory.save_message("user", "Hello Spidey!")
    memory.save_message("assistant", "Hey there!")
    memory.save_message("user", "What is Python?")
    memory.save_message("assistant", "Python is awesome!")
    count = memory.get_message_count()
    print(f"  Messages: {count}")
    assert count == 4
    print("✅ Test 2 Passed!\n")

    # Test 3: Get messages for API
    print("--- Test 3: API Messages ---")
    msgs = memory.get_conversation_messages()
    print(f"  API messages: {len(msgs)}")
    for m in msgs:
        print(f"    {m['role']}: {m['content'][:30]}")
    assert len(msgs) == 4
    print("✅ Test 3 Passed!\n")

    # Test 4: Remember/Recall
    print("--- Test 4: Remember/Recall ---")
    memory.remember("name", "Kashan", "personal")
    memory.remember("language", "Python", "coding")
    memory.remember("city", "Karachi", "personal")

    name = memory.recall("name")
    print(f"  Name: {name}")
    assert name == "Kashan"

    all_mem = memory.get_all_memories()
    print(f"  Total memories: {len(all_mem)}")
    assert len(all_mem) == 3
    print("✅ Test 4 Passed!\n")

    # Test 5: Memory context
    print("--- Test 5: Memory Context ---")
    context = memory.get_memory_context()
    print(f"  Context:\n{context}")
    assert "Kashan" in context
    print("✅ Test 5 Passed!\n")

    # Test 6: Notes
    print("--- Test 6: Notes ---")
    memory.add_note("Test Note", "This is a test", "study", important=True)
    notes = memory.get_notes()
    print(f"  Notes: {len(notes)}")
    assert len(notes) >= 1
    print("✅ Test 6 Passed!\n")

    # Test 7: Stats
    print("--- Test 7: Stats ---")
    stats = memory.get_stats()
    print(f"  Conversations: {stats['total_conversations']}")
    print(f"  Messages: {stats['total_messages']}")
    print(f"  Notes: {stats['total_notes']}")
    print(f"  Memories: {stats['total_preferences']}")
    print("✅ Test 7 Passed!\n")

    # Test 8: Search messages
    print("--- Test 8: Search ---")
    results = memory.search_messages("Python")
    print(f"  Found {len(results)} messages about 'Python'")
    assert len(results) >= 1
    print("✅ Test 8 Passed!\n")

    # Test 9: Forget
    print("--- Test 9: Forget ---")
    memory.forget("city")
    city = memory.recall("city")
    print(f"  City after forget: {city}")
    assert city is None
    print("✅ Test 9 Passed!\n")

    memory.close()
    print("🎉 All memory tests passed!")


if __name__ == "__main__":
    test_memory()
