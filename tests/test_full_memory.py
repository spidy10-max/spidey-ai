"""
🕷️ FULL MEMORY SYSTEM TEST
Tests the complete memory pipeline:
SQLite + ChromaDB + AutoMemory + SearchEngine
"""
from spidey.brain.chat import SpideyBrain
from spidey.config import settings


def test_full_memory():
    print()
    print("=" * 55)
    print("   🕷️ FULL MEMORY SYSTEM TEST")
    print("=" * 55)
    print()

    brain = SpideyBrain()

    # ============================================
    # PHASE 1: Conversation + Auto Memory
    # ============================================
    print("━" * 55)
    print("📦 PHASE 1: Chat + Auto Memory Detection")
    print("━" * 55)

    conv_id = brain.start_new_conversation()
    print(f"\n  ✅ Conversation started: {conv_id}")

    # Test chat
    print("\n  💬 Sending messages...")
    reply1 = brain.chat("My name is Kashan and I live in Kotaddu")
    print(f"  🕷️ {reply1[:80]}...")

    reply2 = brain.chat("I'm 17 years old and I love Python programming")
    print(f"  🕷️ {reply2[:80]}...")

    reply3 = brain.chat("I am a software student")
    print(f"  🕷️ {reply3[:80]}...")

    reply4 = brain.chat("What is Django used for?")
    print(f"  🕷️ {reply4[:80]}...")

    # Check auto-detected
    detected = brain.get_auto_detected()
    print(f"\n  🧠 Auto-detected {len(detected)} facts:")
    for key, value in detected.items():
        print(f"     • {key} = {value}")

    assert len(detected) >= 3
    print("\n  ✅ Phase 1 Passed!\n")

    # ============================================
    # PHASE 2: Memory Recall
    # ============================================
    print("━" * 55)
    print("📦 PHASE 2: Memory Recall")
    print("━" * 55)

    name = brain.recall("name")
    city = brain.recall("city")
    age = brain.recall("age")

    print(f"\n  Name: {name}")
    print(f"  City: {city}")
    print(f"  Age: {age}")

    assert name == "Kashan"
    assert city == "Kotaddu"
    assert age == "17"

    # Manual remember
    brain.remember("favorite_food", "biryani", "personal")
    food = brain.recall("favorite_food")
    print(f"  Food: {food}")
    assert food == "biryani"

    print("\n  ✅ Phase 2 Passed!\n")

    # ============================================
    # PHASE 3: All Memories
    # ============================================
    print("━" * 55)
    print("📦 PHASE 3: All Memories")
    print("━" * 55)

    memories = brain.get_all_memories()
    print(f"\n  Total memories: {len(memories)}")
    for key, info in memories.items():
        print(f"     • {key}: {info['value']} ({info['category']})")

    assert len(memories) >= 4
    print("\n  ✅ Phase 3 Passed!\n")

    # ============================================
    # PHASE 4: Semantic Search
    # ============================================
    print("━" * 55)
    print("📦 PHASE 4: Semantic Search")
    print("━" * 55)

    # Search by meaning
    print("\n  🔍 Searching 'coding'...")
    results = brain.semantic_search("coding and programming")
    print(f"  Found {len(results)} results:")
    for r in results[:3]:
        print(f"     📝 {r['content'][:50]}...")

    assert len(results) > 0

    # Smart recall
    print("\n  🧠 Smart recall 'where does user live'...")
    results = brain.smart_recall("where does the user live")
    print(f"  Found {len(results)} memories:")
    for r in results[:3]:
        print(f"     🧠 {r['content']}")

    print("\n  ✅ Phase 4 Passed!\n")

    # ============================================
    # PHASE 5: Notes
    # ============================================
    print("━" * 55)
    print("📦 PHASE 5: Notes System")
    print("━" * 55)

    brain.add_note("Learn FastAPI", "Build REST APIs with FastAPI", "study", important=True)
    brain.add_note("Gym Schedule", "Mon Wed Fri workout", "personal")
    brain.add_note("Spidey Project", "Complete week 3 memory system", "coding", important=True)

    notes = brain.get_notes()
    print(f"\n  Total notes: {len(notes)}")
    for note in notes:
        star = "⭐" if note["is_important"] else "  "
        print(f"     {star} [{note['id']}] {note['title']}")

    assert len(notes) >= 3

    # Search notes
    print("\n  🔍 Searching notes for 'API'...")
    results = brain.search_notes("building APIs and web development")
    print(f"  Found {len(results)} notes:")
    for r in results[:3]:
        print(f"     📝 {r['content'][:50]}...")

    print("\n  ✅ Phase 5 Passed!\n")

    # ============================================
    # PHASE 6: Conversation History
    # ============================================
    print("━" * 55)
    print("📦 PHASE 6: Conversation History")
    print("━" * 55)

    count = brain.get_history_count()
    print(f"\n  Messages in current conv: {count}")
    assert count > 0

    convs = brain.get_all_conversations()
    print(f"  Total conversations: {len(convs)}")

    print("\n  ✅ Phase 6 Passed!\n")

    # ============================================
    # PHASE 7: Smart Search (Full)
    # ============================================
    print("━" * 55)
    print("📦 PHASE 7: Smart Search (Combined)")
    print("━" * 55)

    results = brain.smart_search("Python programming")
    print(f"\n  Total found: {results['total_found']}")
    print(f"  Semantic messages: {len(results['semantic_messages'])}")
    print(f"  Exact messages: {len(results['exact_messages'])}")
    print(f"  Summaries: {len(results['summaries'])}")
    print(f"  Memories: {len(results['memories'])}")
    print(f"  Notes: {len(results['notes'])}")

    assert results["total_found"] > 0

    print("\n  ✅ Phase 7 Passed!\n")

    # ============================================
    # PHASE 8: Forget
    # ============================================
    print("━" * 55)
    print("📦 PHASE 8: Forget")
    print("━" * 55)

    brain.forget("favorite_food")
    food = brain.recall("favorite_food")
    print(f"\n  Food after forget: {food}")
    assert food is None

    print("\n  ✅ Phase 8 Passed!\n")

    # ============================================
    # PHASE 9: Statistics
    # ============================================
    print("━" * 55)
    print("📦 PHASE 9: Statistics")
    print("━" * 55)

    stats = brain.get_stats()
    print(f"\n  💬 Conversations: {stats['total_conversations']}")
    print(f"  📨 Messages: {stats['total_messages']}")
    print(f"  👤 User msgs: {stats['user_messages']}")
    print(f"  🕷️ AI msgs: {stats['ai_messages']}")
    print(f"  🔢 Tokens: {stats['total_tokens']}")
    print(f"  📝 Notes: {stats['total_notes']}")
    print(f"  🧠 Memories: {stats['total_preferences']}")
    print(f"  🔍 Vector msgs: {stats.get('vector_messages', 0)}")
    print(f"  🤖 Auto-detected: {stats.get('auto_detected_this_session', 0)}")

    print("\n  ✅ Phase 9 Passed!\n")

    # ============================================
    # PHASE 10: Cleanup
    # ============================================
    print("━" * 55)
    print("📦 PHASE 10: Cleanup")
    print("━" * 55)

    brain.close()
    print("\n  ✅ Brain closed properly")

    print("\n  ✅ Phase 10 Passed!\n")

    # ============================================
    # RESULTS
    # ============================================
    print("=" * 55)
    print("   🎉 ALL 10 PHASES PASSED!")
    print("=" * 55)
    print()
    print("   ✅ Phase 1:  Chat + Auto Memory")
    print("   ✅ Phase 2:  Memory Recall")
    print("   ✅ Phase 3:  All Memories")
    print("   ✅ Phase 4:  Semantic Search")
    print("   ✅ Phase 5:  Notes System")
    print("   ✅ Phase 6:  Conversation History")
    print("   ✅ Phase 7:  Smart Search")
    print("   ✅ Phase 8:  Forget")
    print("   ✅ Phase 9:  Statistics")
    print("   ✅ Phase 10: Cleanup")
    print()
    print("   🧠 FULL MEMORY SYSTEM WORKING! 🕷️")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_full_memory()