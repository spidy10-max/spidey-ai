"""
Test Semantic Search Integration
"""
from spidey.memory.memory import SpideyMemory


def test_semantic():
    print("Testing Semantic Search Integration...\n")

    memory = SpideyMemory()

    # Test 1: Start and save messages
    print("--- Test 1: Save Messages ---")
    memory.start_conversation(provider="groq")
    memory.save_message("user", "I love Python programming and coding")
    memory.save_message("assistant", "Python is great for AI!")
    memory.save_message("user", "I went to the gym today")
    memory.save_message("assistant", "Exercise is good for health!")
    memory.save_message("user", "What is the weather in Karachi?")
    memory.save_message("assistant", "Karachi is usually warm and humid")
    print("  6 messages saved to SQLite + ChromaDB")
    print("✅ Test 1 Passed!\n")

    # Test 2: Semantic search - coding
    print("--- Test 2: Smart Search 'coding' ---")
    results = memory.semantic_search("coding tutorials")
    print(f"  Found {len(results)} results:")
    for r in results[:3]:
        print(f"    📝 {r['content'][:50]}...")
    assert len(results) > 0
    print("✅ Test 2 Passed!\n")

    # Test 3: Semantic search - fitness
    print("--- Test 3: Smart Search 'fitness' ---")
    results = memory.semantic_search("fitness workout")
    print(f"  Found {len(results)} results:")
    for r in results[:3]:
        print(f"    📝 {r['content'][:50]}...")
    assert len(results) > 0
    print("✅ Test 3 Passed!\n")

    # Test 4: Remember with vectors
    print("--- Test 4: Smart Remember ---")
    memory.remember("name", "Kashan", "personal")
    memory.remember("language", "Python", "coding")
    memory.remember("hobby", "gym and fitness", "personal")

    results = memory.smart_recall("what does user like to code in")
    print(f"  Found {len(results)} memories:")
    for r in results:
        print(f"    🧠 {r['content']}")
    assert len(results) > 0
    print("✅ Test 4 Passed!\n")

    # Test 5: Summary
    print("--- Test 5: Save Summary ---")
    memory.save_summary()
    results = memory.search_summaries("programming")
    print(f"  Found {len(results)} summaries")
    print("✅ Test 5 Passed!\n")

    # Test 6: Stats
    print("--- Test 6: Combined Stats ---")
    stats = memory.get_stats()
    print(f"  SQL Messages: {stats['total_messages']}")
    print(f"  Vector Messages: {stats.get('vector_messages', 0)}")
    print(f"  Memories: {stats['total_preferences']}")
    print("✅ Test 6 Passed!\n")

    memory.close()
    print("🎉 All semantic tests passed!")


if __name__ == "__main__":
    test_semantic()