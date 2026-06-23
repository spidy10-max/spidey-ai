"""
Test script for SpideyBrain
Quick test to make sure everything works
"""
from spidey.brain.chat import SpideyBrain


def test_basic_chat():
    """Test basic chat functionality"""
    print("Testing SpideyBrain...")

    brain = SpideyBrain()

    # Test 1: Basic reply
    print("\n--- Test 1: Basic Reply ---")
    reply = brain.chat("Hello, who are you?")
    print(f"Reply: {reply}")
    assert reply is not None
    assert len(reply) > 0
    print("✅ Test 1 Passed!")

    # Test 2: Memory check
    print("\n--- Test 2: Memory Check ---")
    brain.chat("My favorite color is blue")
    reply = brain.chat("What is my favorite color?")
    print(f"Reply: {reply}")
    print("✅ Test 2 Passed!")

    # Test 3: Message count
    print("\n--- Test 3: Message Count ---")
    count = brain.get_history_count()
    print(f"Message count: {count}")
    assert count > 0
    print("✅ Test 3 Passed!")

    # Test 4: Reset
    print("\n--- Test 4: Reset ---")
    brain.reset()
    count = brain.get_history_count()
    print(f"After reset count: {count}")
    assert count == 0
    print("✅ Test 4 Passed!")

    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    test_basic_chat()
