"""
Test Tool Connector — AI to Computer bridge
"""
from spidey.tools.tool_connector import ToolConnector
import time


def test_tool_connector():
    print()
    print("=" * 55)
    print("   🖥️ TOOL CONNECTOR TEST")
    print("=" * 55)
    print()

    tc = ToolConnector()

    # Test 1: Open app detection
    print("--- Test 1: Open App Detection ---")
    tests = [
        ("open chrome", True),
        ("open notepad", True),
        ("launch calculator", True),
        ("start paint", True),
        ("what is python", False),
        ("hello how are you", False),
    ]
    for text, should_detect in tests:
        result = tc.process_command(text)
        detected = result is not None
        status = "✅" if detected == should_detect else "❌"
        print(f"   {status} '{text}' → {'Detected' if detected else 'Not detected'}")
        if detected:
            time.sleep(1)

    print("✅ Test 1 Done!\n")

    # Test 2: Close app
    print("--- Test 2: Close App Detection ---")
    result = tc.process_command("close notepad")
    print(f"   Result: {result}")
    time.sleep(1)
    print("✅ Test 2 Done!\n")

    # Test 3: Screenshot
    print("--- Test 3: Screenshot Detection ---")
    result = tc.process_command("take a screenshot")
    print(f"   Result: {result}")
    print("✅ Test 3 Done!\n")

    # Test 4: URL detection
    print("--- Test 4: URL Detection ---")
    url_tests = [
        "open youtube",
        "open google",
        "open github",
    ]
    for text in url_tests:
        result = tc.process_command(text)
        detected = result is not None
        print(f"   {'✅' if detected else '❌'} '{text}' → {result if result else 'Not detected'}")
    print("✅ Test 4 Done!\n")

    # Test 5: No false positives
    print("--- Test 5: No False Positives ---")
    safe_texts = [
        "what is the weather",
        "tell me a joke",
        "how are you doing",
        "my name is kashan",
        "what is python programming",
    ]
    for text in safe_texts:
        result = tc.process_command(text)
        status = "✅" if result is None else "❌"
        print(f"   {status} '{text}' → {'WRONGLY detected!' if result else 'Correctly ignored'}")
    print("✅ Test 5 Done!\n")

    # Test 6: Search files
    print("--- Test 6: File Search ---")
    result = tc.process_command("search for python files")
    if result:
        print(f"   {result[:200]}...")
    else:
        print("   No files found (normal)")
    print("✅ Test 6 Done!\n")

    # Test 7: Toggle
    print("--- Test 7: Toggle ---")
    tc.toggle()
    result = tc.process_command("open notepad")
    print(f"   Disabled: {result}")
    assert result is None
    tc.toggle()
    print("   Re-enabled")
    print("✅ Test 7 Done!\n")

    print("=" * 55)
    print("   🎉 TOOL CONNECTOR TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_tool_connector()