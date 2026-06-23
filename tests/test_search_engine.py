"""
Test Smart Search Engine
"""
from spidey.memory.memory import SpideyMemory
from spidey.memory.search_engine import SearchEngine


def test_search_engine():
    print("Testing Smart Search Engine...\n")

    memory = SpideyMemory()
    search = SearchEngine(db=memory.db, vectors=memory.vectors)

    # Setup: Add test data
    print("--- Setup: Adding test data ---")
    memory.start_conversation(provider="groq")

    memory.save_message("user", "I love Python programming and building AI projects")
    memory.save_message("assistant", "Python is excellent for AI and machine learning!")
    memory.save_message("user", "Can you help me with Django web development?")
    memory.save_message("assistant", "Django is a great Python web framework!")
    memory.save_message("user", "I went to gym today and did weight training")
    memory.save_message("assistant", "Weight training builds muscle and strength!")
    memory.save_message("user", "What is the weather like in Karachi today?")
    memory.save_message("assistant", "Karachi is usually hot and humid this time of year")

    memory.remember("name", "Kashan", "personal")
    memory.remember("language", "Python", "coding")
    memory.remember("city", "Karachi", "personal")

    memory.add_note("Learn FastAPI", "Study FastAPI for building APIs", "study", important=True)
    memory.add_note("Gym Schedule", "Monday Wednesday Friday workout", "personal")

    memory.save_summary()
    print("  ✅ Test data added!\n")

    # Test 1: Smart search
    print("--- Test 1: Smart Search 'programming' ---")
    results = search.smart_search("programming")
    print(f"  Total found: {results['total_found']}")
    print(f"  Semantic: {len(results['semantic_messages'])}")
    print(f"  Exact: {len(results['exact_messages'])}")
    print(f"  Summaries: {len(results['summaries'])}")
    print(f"  Memories: {len(results['memories'])}")
    print(f"  Notes: {len(results['notes'])}")
    assert results["total_found"] > 0
    print("✅ Test 1 Passed!\n")

    # Test 2: Smart search - fitness
    print("--- Test 2: Smart Search 'fitness' ---")
    results = search.smart_search("fitness and exercise")
    print(f"  Total found: {results['total_found']}")
    if results["semantic_messages"]:
        for r in results["semantic_messages"][:3]:
            print(f"    📝 {r['content'][:50]}...")
    assert results["total_found"] > 0
    print("✅ Test 2 Passed!\n")

    # Test 3: Find related chats
    print("--- Test 3: Find Related Chats ---")
    related = search.find_related_chats("I want to learn web development")
    print(f"  Found {len(related)} related messages:")
    for r in related[:3]:
        print(f"    📝 {r['content'][:50]}...")
    assert len(related) > 0
    print("✅ Test 3 Passed!\n")

    # Test 4: Find conversations about topic
    print("--- Test 4: Find Conversations About 'coding' ---")
    result = search.find_conversations_about("coding and programming")
    print(f"  Summaries: {len(result['summaries'])}")
    print(f"  Conversations: {len(result['conversations'])}")
    print("✅ Test 4 Passed!\n")

    # Test 5: Get context for query
    print("--- Test 5: Auto Context ---")
    context = search.get_context_for_query("Tell me about Python")
    print(f"  Context length: {len(context)} chars")
    if context:
        print(f"  Preview: {context[:100]}...")
    assert len(context) > 0
    print("✅ Test 5 Passed!\n")

    # Test 6: Search stats
    print("--- Test 6: Search Stats ---")
    stats = search.get_search_stats()
    print(f"  Searchable messages: {stats['total_searchable_messages']}")
    print(f"  Summaries: {stats['total_summaries']}")
    print(f"  Memories: {stats['total_memories']}")
    print(f"  Notes: {stats['total_notes']}")
    print("✅ Test 6 Passed!\n")

    # Test 7: Smart search - weather
    print("--- Test 7: Smart Search 'weather' ---")
    results = search.smart_search("climate and weather")
    print(f"  Total found: {results['total_found']}")
    if results["semantic_messages"]:
        print(f"  Top result: {results['semantic_messages'][0]['content'][:50]}...")
    assert results["total_found"] > 0
    print("✅ Test 7 Passed!\n")

    memory.close()
    print("🎉 All search engine tests passed!")


if __name__ == "__main__":
    test_search_engine()