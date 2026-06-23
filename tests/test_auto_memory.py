"""
Test Auto Memory Detection
"""
from spidey.memory.memory import SpideyMemory
from spidey.memory.auto_memory import AutoMemory


def test_auto_memory():
    print("Testing Auto Memory Detection...\n")

    memory = SpideyMemory()
    auto = AutoMemory(memory)

    # Test 1: Detect name
    print("--- Test 1: Detect Name ---")
    facts = auto.detect_and_save("My name is Kashan")
    print(f"  Detected: {facts}")
    assert len(facts) > 0
    assert facts[0]["key"] == "name"
    assert facts[0]["value"] == "Kashan"
    print("✅ Test 1 Passed!\n")

    # Test 2: Detect city
    print("--- Test 2: Detect City ---")
    facts = auto.detect_and_save("I live in Kotaddu")
    print(f"  Detected: {facts}")
    assert len(facts) > 0
    assert facts[0]["key"] == "city"
    assert facts[0]["value"] == "Kotaddu"
    print("✅ Test 2 Passed!\n")

    # Test 3: Detect age
    print("--- Test 3: Detect Age ---")
    facts = auto.detect_and_save("I'm 17 years old")
    print(f"  Detected: {facts}")
    assert len(facts) > 0
    assert facts[0]["key"] == "age"
    assert facts[0]["value"] == "17"
    print("✅ Test 3 Passed!\n")

    # Test 4: Detect favorite language
    print("--- Test 4: Detect Language ---")
    facts = auto.detect_and_save("I love Python programming")
    print(f"  Detected: {facts}")
    assert len(facts) > 0
    assert facts[0]["key"] == "favorite_language"
    print("✅ Test 4 Passed!\n")

    # Test 5: Detect occupation
    print("--- Test 5: Detect Occupation ---")
    facts = auto.detect_and_save("I am a software student")
    print(f"  Detected: {facts}")
    assert len(facts) > 0
    print("✅ Test 5 Passed!\n")

    # Test 6: No detection on normal message
    print("--- Test 6: No Detection ---")
    facts = auto.detect_and_save("What is the weather today?")
    print(f"  Detected: {facts}")
    assert len(facts) == 0
    print("✅ Test 6 Passed!\n")

    # Test 7: Verify memories saved
    print("--- Test 7: Verify Saved Memories ---")
    name = memory.recall("name")
    city = memory.recall("city")
    age = memory.recall("age")
    print(f"  Name: {name}")
    print(f"  City: {city}")
    print(f"  Age: {age}")
    assert name == "Kashan"
    assert city == "Kotaddu"
    assert age == "17"
    print("✅ Test 7 Passed!\n")

    # Test 8: Detected count
    print("--- Test 8: Detection Stats ---")
    count = auto.get_detected_count()
    facts = auto.get_detected_facts()
    print(f"  Detected this session: {count}")
    print(f"  Facts: {facts}")
    assert count >= 4
    print("✅ Test 8 Passed!\n")

    # Test 9: Duplicate detection skip
    print("--- Test 9: Duplicate Skip ---")
    facts = auto.detect_and_save("My name is Kashan")
    print(f"  Detected (should be empty): {facts}")
    assert len(facts) == 0
    print("✅ Test 9 Passed!\n")

    # Test 10: Reset session
    print("--- Test 10: Reset Session ---")
    auto.reset_session()
    count = auto.get_detected_count()
    print(f"  After reset: {count}")
    assert count == 0
    print("✅ Test 10 Passed!\n")

    # Test 11: Detect after reset
    print("--- Test 11: Detect After Reset ---")
    facts = auto.detect_and_save("Call me Ali")
    print(f"  Detected: {facts}")
    assert len(facts) > 0
    print("✅ Test 11 Passed!\n")

    # Test 12: Exclude common words
    print("--- Test 12: Exclude Common Words ---")
    auto.reset_session()
    facts = auto.detect_and_save("What is the weather today?")
    print(f"  Detected (should be empty): {facts}")
    assert len(facts) == 0
    print("✅ Test 12 Passed!\n")

    memory.close()
    print("🎉 All auto memory tests passed!")


if __name__ == "__main__":
    test_auto_memory()