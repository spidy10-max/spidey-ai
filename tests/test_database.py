"""
Test script for SQLite Database System
Tests all CRUD operations
"""
from spidey.memory.database import Database
import os


def test_database():
    """Test all database operations"""
    print("Testing SQLite Database System...\n")

    # Use test database
    test_db = "data/test_spidey.db"

    # Clean up old test db
    if os.path.exists(test_db):
        os.remove(test_db)

    db = Database(db_path=test_db)

    # Test 1: Tables created
    print("--- Test 1: Tables Created ---")
    cursor = db.connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"  Tables: {tables}")
    assert "users" in tables
    assert "conversations" in tables
    assert "messages" in tables
    assert "user_preferences" in tables
    assert "notes" in tables
    print("✅ Test 1 Passed!\n")

    # Test 2: Default user
    print("--- Test 2: Default User ---")
    user = db.get_user(1)
    print(f"  User: {user}")
    assert user is not None
    assert user["username"] == "User"
    print("✅ Test 2 Passed!\n")

    # Test 3: Update user
    print("--- Test 3: Update User ---")
    db.update_user(1, username="Kashan")
    user = db.get_user(1)
    print(f"  Updated: {user['username']}")
    assert user["username"] == "Kashan"
    print("✅ Test 3 Passed!\n")

    # Test 4: Create conversation
    print("--- Test 4: Create Conversation ---")
    conv_id = db.create_conversation("test_001", title="Test Chat")
    print(f"  Created: {conv_id}")
    assert conv_id == "test_001"
    print("✅ Test 4 Passed!\n")

    # Test 5: Add messages
    print("--- Test 5: Add Messages ---")
    db.add_message("test_001", "user", "Hello Spidey!", tokens_used=10)
    db.add_message("test_001", "assistant", "Hey there! How can I help?", tokens_used=15)
    db.add_message("test_001", "user", "What is Python?", tokens_used=8)
    db.add_message("test_001", "assistant", "Python is a programming language!", tokens_used=20)
    count = db.get_message_count("test_001")
    print(f"  Messages added: {count}")
    assert count == 4
    print("✅ Test 5 Passed!\n")

    # Test 6: Get messages
    print("--- Test 6: Get Messages ---")
    messages = db.get_messages("test_001")
    for msg in messages:
        print(f"  {msg['role']}: {msg['content'][:40]}")
    assert len(messages) == 4
    print("✅ Test 6 Passed!\n")

    # Test 7: Get messages for API
    print("--- Test 7: Messages for API ---")
    api_msgs = db.get_messages_for_api("test_001")
    print(f"  API format: {len(api_msgs)} messages")
    for msg in api_msgs:
        print(f"  {msg['role']}: {msg['content'][:40]}")
    assert len(api_msgs) == 4
    assert "role" in api_msgs[0]
    assert "content" in api_msgs[0]
    print("✅ Test 7 Passed!\n")

    # Test 8: Search messages
    print("--- Test 8: Search Messages ---")
    results = db.search_messages("Python")
    print(f"  Found {len(results)} messages about 'Python'")
    assert len(results) >= 1
    print("✅ Test 8 Passed!\n")

    # Test 9: Preferences
    print("--- Test 9: Preferences ---")
    db.set_preference("favorite_color", "blue", category="personal")
    db.set_preference("language", "Python", category="coding")
    db.set_preference("city", "Karachi", category="personal")

    color = db.get_preference("favorite_color")
    print(f"  Favorite color: {color}")
    assert color == "blue"

    all_prefs = db.get_all_preferences()
    print(f"  Total preferences: {len(all_prefs)}")
    for key, info in all_prefs.items():
        print(f"    {key}: {info['value']} ({info['category']})")
    assert len(all_prefs) == 3
    print("✅ Test 9 Passed!\n")

    # Test 10: Notes
    print("--- Test 10: Notes ---")
    db.add_note("Learn Python", "Study OOP and decorators", category="study")
    db.add_note("Buy groceries", "Milk, eggs, bread", category="personal")
    db.add_note("Project idea", "Build AI assistant", category="coding", is_important=1)

    all_notes = db.get_notes()
    print(f"  Total notes: {len(all_notes)}")
    for note in all_notes:
        star = "⭐" if note["is_important"] else "  "
        print(f"  {star} {note['title']}: {note['content'][:30]}")

    important = db.get_notes(important_only=True)
    print(f"  Important notes: {len(important)}")
    assert len(important) == 1
    print("✅ Test 10 Passed!\n")

    # Test 11: Search notes
    print("--- Test 11: Search Notes ---")
    results = db.search_notes("Python")
    print(f"  Found {len(results)} notes about 'Python'")
    assert len(results) >= 1
    print("✅ Test 11 Passed!\n")

    # Test 12: Get all conversations
    print("--- Test 12: All Conversations ---")
    db.create_conversation("test_002", title="Another Chat")
    db.add_message("test_002", "user", "Hello again!")
    convs = db.get_all_conversations()
    print(f"  Total conversations: {len(convs)}")
    for conv in convs:
        print(f"    [{conv['conv_id']}] {conv['title']} — {conv['message_count']} msgs")
    assert len(convs) >= 2
    print("✅ Test 12 Passed!\n")

    # Test 13: Search conversations
    print("--- Test 13: Search Conversations ---")
    results = db.search_conversations("Hello")
    print(f"  Found {len(results)} conversations")
    assert len(results) >= 1
    print("✅ Test 13 Passed!\n")

    # Test 14: Statistics
    print("--- Test 14: Statistics ---")
    stats = db.get_stats()
    print(f"  Conversations: {stats['total_conversations']}")
    print(f"  Messages: {stats['total_messages']}")
    print(f"  User msgs: {stats['user_messages']}")
    print(f"  AI msgs: {stats['ai_messages']}")
    print(f"  Tokens: {stats['total_tokens']}")
    print(f"  Notes: {stats['total_notes']}")
    print(f"  Preferences: {stats['total_preferences']}")
    print("✅ Test 14 Passed!\n")

    # Test 15: Delete operations
    print("--- Test 15: Delete Operations ---")
    db.delete_preference("favorite_color")
    color = db.get_preference("favorite_color")
    print(f"  After delete preference: {color}")
    assert color is None

    db.delete_note(1)
    notes = db.get_notes()
    print(f"  Notes after delete: {len(notes)}")

    db.delete_conversation("test_002")
    conv = db.get_conversation("test_002")
    print(f"  After delete conversation: {conv}")
    assert conv is None
    print("✅ Test 15 Passed!\n")

    # Cleanup
    db.close()
    if os.path.exists(test_db):
        os.remove(test_db)
    print("--- Cleanup done ---\n")

    print("🎉 All database tests passed!")


if __name__ == "__main__":
    test_database()
