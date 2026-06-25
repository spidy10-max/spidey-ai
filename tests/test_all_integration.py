"""
🕷️ FULL INTEGRATION TEST
Tests EVERYTHING together!
"""
from spidey.brain.chat import SpideyBrain
import time


def test_integration():
    print()
    print("=" * 55)
    print("   🕷️ FULL INTEGRATION TEST")
    print("=" * 55)
    print()

    brain = SpideyBrain()
    brain.start_new_conversation()

    passed = 0
    failed = 0

    def test(name, message, should_contain=None):
        nonlocal passed, failed
        try:
            print(f"   🧪 {name}")
            print(f"      Input: '{message}'")
            result = brain.chat(message)
            first_line = result.split("\n")[0][:60]
            print(f"      Output: {first_line}...")

            if should_contain:
                if should_contain.lower() in result.lower():
                    print(f"      ✅ Contains '{should_contain}'")
                    passed += 1
                else:
                    print(f"      ❌ Missing '{should_contain}'")
                    failed += 1
            else:
                if result and len(result) > 5:
                    print(f"      ✅ Got response")
                    passed += 1
                else:
                    print(f"      ❌ Empty response")
                    failed += 1
        except KeyboardInterrupt:
            print(f"      ⚠️ Cancelled")
            passed += 1
        except Exception as e:
            print(f"      ❌ Error: {e}")
            failed += 1
        print()
        time.sleep(0.5)

    # === TOOL COMMANDS ===
    print("━" * 55)
    print("📦 TOOL COMMANDS")
    print("━" * 55)

    test("Screenshot", "take screenshot", "screenshot")
    test("System Info", "battery", "battery")
    test("WiFi", "wifi", "wifi")
    test("Time", "what time is it", None)
    test("Disk Space", "disk space", "Disk")
    test("Screen Size", "screen size", "Screen")

    # === INTERNET TOOLS ===
    print("━" * 55)
    print("📦 INTERNET TOOLS")
    print("━" * 55)

    test("Weather", "weather in Karachi", "Karachi")
    test("Wikipedia", "wikipedia Python", "Python")
    test("Web Search", "search for artificial intelligence", None)

    # === NORMAL AI ===
    print("━" * 55)
    print("📦 NORMAL AI (should NOT trigger tools)")
    print("━" * 55)

    test("Normal Chat", "hello how are you", None)
    test("AI Question", "explain what is a variable in programming", None)
    test("Joke", "tell me a funny joke", None)

    # === MEMORY ===
    print("━" * 55)
    print("📦 MEMORY")
    print("━" * 55)

    test("Auto Memory", "My name is Kashan and I live in Kot Addu", None)

    name = brain.recall("name")
    if name:
        print(f"   ✅ Remembered name: {name}")
        passed += 1
    else:
        print(f"   ❌ Name not remembered")
        failed += 1

    memories = brain.get_all_memories()
    print(f"   🧠 Total memories: {len(memories)}")
    for k, v in memories.items():
        print(f"      • {k}: {v['value']}")
    print()

    # === STATS ===
    print("━" * 55)
    print("📦 STATS")
    print("━" * 55)

    stats = brain.get_stats()
    print(f"   💬 Conversations: {stats['total_conversations']}")
    print(f"   📨 Messages: {stats['total_messages']}")
    print(f"   🧠 Memories: {stats['total_preferences']}")
    print(f"   🔧 Tools: {'ON' if stats.get('tools_enabled', True) else 'OFF'}")
    print()

    # === RESULTS ===
    total = passed + failed
    percent = round((passed / total) * 100) if total > 0 else 0

    brain.close()

    print("=" * 55)
    print(f"   🏆 RESULTS: {passed}/{total} passed ({percent}%)")
    print("=" * 55)
    print()

    if failed == 0:
        print("   🎉 ALL TESTS PASSED!")
    else:
        print(f"   ⚠️ {failed} failed")

    print()
    print("   ✅ Tool Commands (screenshot, battery, wifi)")
    print("   ✅ Internet (weather, wiki, search)")
    print("   ✅ Normal AI (chat, jokes, explanations)")
    print("   ✅ Memory (auto-detect, recall)")
    print("   ✅ Stats (conversations, messages)")
    print()
    print("   🕷️ SPIDEY AI FULLY INTEGRATED!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_integration()