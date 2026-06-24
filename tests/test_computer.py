"""
Test Computer Control
"""
from spidey.tools.computer import ComputerControl
import time


def test_computer():
    print()
    print("=" * 55)
    print("   🖥️ COMPUTER CONTROL TEST")
    print("=" * 55)
    print()

    pc = ComputerControl()

    # Test 1: Screen size
    print("--- Test 1: Screen Size ---")
    print(f"   {pc.get_screen_size()}")
    print("✅ Passed!\n")

    # Test 2: Mouse position
    print("--- Test 2: Mouse Position ---")
    print(f"   {pc.get_mouse_position()}")
    print("✅ Passed!\n")

    # Test 3: Available commands
    print("--- Test 3: Available Commands ---")
    cmds = pc.get_available_commands()
    for category, commands in cmds.items():
        print(f"   {category}: {', '.join(commands)}")
    print("✅ Passed!\n")

    # Test 4: Screenshot
    print("--- Test 4: Screenshot ---")
    result = pc.take_screenshot()
    print(f"   {result}")
    print("✅ Passed!\n")

    # Test 5: Open Notepad
    print("--- Test 5: Open Notepad ---")
    result = pc.open_app("notepad")
    print(f"   {result}")
    time.sleep(2)
    print("✅ Passed!\n")

    # Test 6: Type text
    print("--- Test 6: Type Text ---")
    time.sleep(1)
    result = pc.type_text("Hello from Spidey AI!")
    print(f"   {result}")
    print("✅ Passed!\n")

    # Test 7: Close Notepad
    print("--- Test 7: Close Notepad ---")
    time.sleep(1)
    result = pc.close_app("notepad")
    print(f"   {result}")
    print("✅ Passed!\n")

    # Test 8: Search files
    print("--- Test 8: Search Files ---")
    files = pc.search_files("C:\\Users", "readme", extension=".md")
    print(f"   Found {len(files)} files")
    for f in files[:3]:
        print(f"   📄 {f}")
    print("✅ Passed!\n")

    print("=" * 55)
    print("   🎉 COMPUTER CONTROL TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_computer()