"""
Test script for ChromaDB Vector Store
"""
from spidey.memory.vector_store import VectorStore
import shutil
import os


def test_vector_store():
    """Test vector store operations"""
    print("Testing ChromaDB Vector Store...\n")

    test_dir = "data/test_chroma"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    vs = VectorStore(persist_dir=test_dir)

    # Test 1: Add chat messages
    print("--- Test 1: Add Chat Messages ---")
    vs.add_chat_message("msg_1", "I love Python programming", {"role": "user", "conv_id": "conv_1"})
    vs.add_chat_message("msg_2", "Python is great for AI and machine learning", {"role": "assistant", "conv_id": "conv_1"})
    vs.add_chat_message("msg_3", "I went to the gym today and did cardio", {"role": "user", "conv_id": "conv_2"})
    vs.add_chat_message("msg_4", "Exercise is important for health", {"role": "assistant", "conv_id": "conv_2"})
    vs.add_chat_message("msg_5", "Can you help me with JavaScript code?", {"role": "user", "conv_id": "conv_3"})
    vs.add_chat_message("msg_6", "What is the weather like in Karachi?", {"role": "user", "conv_id": "conv_4"})
    print("  Added 6 chat messages")
    print("✅ Test 1 Passed!\n")

    # Test 2: Semantic search - coding
    print("--- Test 2: Search 'coding' ---")
    results = vs.search_chats("coding", n_results=3)
    print(f"  Found {len(results)} results:")
    for r in results:
        print(f"    📝 {r['content'][:50]}...")
        print(f"       Distance: {round(r['distance'], 3)}")
    assert len(results) > 0
    print("✅ Test 2 Passed!\n")

    # Test 3: Semantic search - fitness
    print("--- Test 3: Search 'fitness' ---")
    results = vs.search_chats("fitness and workout", n_results=3)
    print(f"  Found {len(results)} results:")
    for r in results:
        print(f"    📝 {r['content'][:50]}...")
        print(f"       Distance: {round(r['distance'], 3)}")
    assert len(results) > 0
    print("✅ Test 3 Passed!\n")

    # Test 4: Semantic search - weather
    print("--- Test 4: Search 'climate' ---")
    results = vs.search_chats("climate and temperature", n_results=3)
    print(f"  Found {len(results)} results:")
    for r in results:
        print(f"    📝 {r['content'][:50]}...")
        print(f"       Distance: {round(r['distance'], 3)}")
    print("✅ Test 4 Passed!\n")

    # Test 5: Summaries
    print("--- Test 5: Conversation Summaries ---")
    vs.add_summary("conv_1", "Discussion about Python programming and AI", {"topic": "coding"})
    vs.add_summary("conv_2", "Talk about gym workout and health fitness", {"topic": "health"})
    vs.add_summary("conv_3", "Help with JavaScript coding", {"topic": "coding"})

    results = vs.search_summaries("programming languages", n_results=2)
    print(f"  Found {len(results)} summaries:")
    for r in results:
        print(f"    📝 {r['content'][:50]}...")
    assert len(results) > 0
    print("✅ Test 5 Passed!\n")

    # Test 6: Notes
    print("--- Test 6: Notes ---")
    vs.add_note("note_1", "Learn Django framework for web development", {"category": "study"})
    vs.add_note("note_2", "Buy protein powder and vitamins from store", {"category": "shopping"})
    vs.add_note("note_3", "Complete Spidey AI project by end of month", {"category": "project"})

    results = vs.search_notes("web development frameworks", n_results=2)
    print(f"  Found {len(results)} notes:")
    for r in results:
        print(f"    📝 {r['content'][:50]}...")
    assert len(results) > 0
    print("✅ Test 6 Passed!\n")

    # Test 7: User memories
    print("--- Test 7: User Memories ---")
    vs.add_memory("name", "Kashan", {"category": "personal"})
    vs.add_memory("favorite_language", "Python", {"category": "coding"})
    vs.add_memory("city", "Karachi", {"category": "personal"})
    vs.add_memory("hobby", "gym and fitness", {"category": "personal"})

    results = vs.search_memories("what programming does the user like", n_results=2)
    print(f"  Found {len(results)} memories:")
    for r in results:
        print(f"    🧠 {r['content']}")
    assert len(results) > 0
    print("✅ Test 7 Passed!\n")

    # Test 8: Stats
    print("--- Test 8: Stats ---")
    stats = vs.get_stats()
    print(f"  Chat messages: {stats['chat_messages']}")
    print(f"  Summaries: {stats['summaries']}")
    print(f"  Notes: {stats['notes']}")
    print(f"  Memories: {stats['memories']}")
    assert stats["chat_messages"] == 6
    assert stats["summaries"] == 3
    print("✅ Test 8 Passed!\n")

    # Test 9: Delete memory
    print("--- Test 9: Delete Memory ---")
    vs.delete_memory("city")
    results = vs.search_memories("Karachi", n_results=1)
    print(f"  Results after delete: {len(results)}")
    print("✅ Test 9 Passed!\n")

    # Cleanup
    print("--- Cleaning up ---")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    print("✅ Cleanup done!\n")

    print("🎉 All vector store tests passed!")


if __name__ == "__main__":
    test_vector_store()