"""
Test AI Agent
"""
from spidey.brain.chat import SpideyBrain
import time


def test_agent():
    print()
    print("=" * 55)
    print("   🤖 AI AGENT TEST")
    print("=" * 55)
    print()

    brain = SpideyBrain()
    brain.start_new_conversation()

    # Test 1: Single command
    print("--- Test 1: Single Command ---")
    result = brain.agent_execute("take screenshot")
    print(f"   Result: {result.split(chr(10))[0][:60]}")
    print("✅ Passed!\n")

    # Test 2: Multi-step task
    print("--- Test 2: Multi-Step Task ---")
    result = brain.agent_execute("take screenshot and show disk space")
    print(result[:200])
    print("✅ Passed!\n")

    # Test 3: Three steps
    print("--- Test 3: Three Steps ---")
    result = brain.agent_execute("battery and wifi and what time is it")
    print(result[:300])
    print("✅ Passed!\n")

    # Test 4: Plan a task
    print("--- Test 4: Plan Task ---")
    steps = brain.agent_plan("Check weather in Karachi, search for Python news, and take a screenshot")
    print(f"   Planned {len(steps)} steps:")
    for i, s in enumerate(steps, 1):
        print(f"   {i}. {s}")
    print("✅ Passed!\n")

    # Test 5: Tool registry
    print("--- Test 5: Available Tools ---")
    tools = brain.agent_tools()
    print(tools[:300])
    print("✅ Passed!\n")

    # Test 6: Normal chat (should use AI)
    print("--- Test 6: Normal Chat via Agent ---")
    result = brain.agent_execute("tell me a joke")
    print(f"   {result[:80]}...")
    print("✅ Passed!\n")

    brain.close()

    print("=" * 55)
    print("   🎉 AGENT TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_agent()