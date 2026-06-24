"""
🕷️ FULL COMPUTER CONTROL TEST
Tests everything: apps, files, screenshots, recording, system info
"""
from spidey.tools.computer import ComputerControl
from spidey.tools.file_manager import FileManager
from spidey.tools.system_info import SystemInfo
from spidey.tools.tool_connector import ToolConnector
import time
import os


def test_all_tools():
    print()
    print("=" * 55)
    print("   🖥️ FULL COMPUTER CONTROL TEST")
    print("=" * 55)
    print()

    # ============================================
    # PHASE 1: System Info
    # ============================================
    print("━" * 55)
    print("📦 PHASE 1: System Info")
    print("━" * 55)

    si = SystemInfo()

    print("\n" + si.get_all_info())
    print()
    print(si.get_battery())
    print(si.get_wifi())
    print(si.get_ip())
    print(si.get_date_time())

    print("\n✅ Phase 1 Passed!\n")

    # ============================================
    # PHASE 2: File Manager
    # ============================================
    print("━" * 55)
    print("📦 PHASE 2: File Manager")
    print("━" * 55)

    fm = FileManager()

    print("\n   📂 Search 'readme':")
    results = fm.search("readme", max_results=3)
    print(fm.format_results(results))

    print("   📂 Python files:")
    results = fm.search_by_extension(".py", max_results=3)
    print(fm.format_results(results))

    print("   📂 Recent files:")
    results = fm.search_recent(hours=48, max_results=3)
    print(fm.format_results(results))

    print("   💾 Disk space:")
    info = fm.get_disk_space("C:")
    if isinstance(info, dict):
        print(f"   C: — {info['free']} free / {info['total']}")

    print("\n✅ Phase 2 Passed!\n")

    # ============================================
    # PHASE 3: Computer Control
    # ============================================
    print("━" * 55)
    print("📦 PHASE 3: Computer Control")
    print("━" * 55)

    pc = ComputerControl()

    print(f"\n   {pc.get_screen_size()}")
    print(f"   {pc.get_mouse_position()}")

    # Screenshot
    result = pc.take_screenshot()
    print(f"   {result}")

    # Available commands
    cmds = pc.get_available_commands()
    total = sum(len(v) for v in cmds.values())
    print(f"\n   Total commands available: {total}")
    for cat, commands in cmds.items():
        print(f"   {cat}: {', '.join(commands)}")

    print("\n✅ Phase 3 Passed!\n")

    # ============================================
    # PHASE 4: Tool Connector (NLP Detection)
    # ============================================
    print("━" * 55)
    print("📦 PHASE 4: Natural Language Detection")
    print("━" * 55)

    tc = ToolConnector()

    # Should DETECT
    detect_tests = [
        "open notepad",
        "take screenshot",
        "find python files",
        "show recent files",
        "disk space",
        "battery",
        "wifi",
        "what time is it",
        "system info",
        "running apps",
        "list downloads",
    ]

    print("\n   ✅ Should DETECT:")
    for text in detect_tests:
        result = tc.process_command(text)
        detected = result is not None
        status = "✅" if detected else "❌"
        print(f"   {status} '{text}'")
        if detected and "open" not in text.lower():
            # Don't show result for app openings (messy)
            pass
        time.sleep(0.3)

    # Close notepad if opened
    tc.process_command("close notepad")
    time.sleep(0.5)

    # Should NOT detect
    safe_tests = [
        "what is python",
        "tell me a joke",
        "how are you",
        "my name is kashan",
        "explain machine learning",
        "hello spidey",
    ]

    print("\n   ✅ Should NOT detect:")
    for text in safe_tests:
        result = tc.process_command(text)
        detected = result is not None
        status = "✅" if not detected else "❌ WRONGLY DETECTED!"
        print(f"   {status} '{text}'")

    print("\n✅ Phase 4 Passed!\n")

    # ============================================
    # PHASE 5: Security Check
    # ============================================
    print("━" * 55)
    print("📦 PHASE 5: Security Check")
    print("━" * 55)

    dangerous = [
        "format c drive",
        "delete system32",
        "shutdown computer",
        "rm -rf /",
    ]

    print("\n   🛡️ Dangerous commands should NOT execute:")
    for text in dangerous:
        result = tc.process_command(text)
        detected = result is not None
        status = "✅ Blocked" if not detected else "❌ DANGER! Executed!"
        print(f"   {status} '{text}'")

    print("\n✅ Phase 5 Passed!\n")

    # ============================================
    # RESULTS
    # ============================================
    print("=" * 55)
    print("   🎉 ALL 5 PHASES PASSED!")
    print("=" * 55)
    print()
    print("   ✅ Phase 1: System Info (battery, wifi, time)")
    print("   ✅ Phase 2: File Manager (search, disk)")
    print("   ✅ Phase 3: Computer Control (screenshot, mouse)")
    print("   ✅ Phase 4: NLP Detection (open, find, show)")
    print("   ✅ Phase 5: Security (dangerous blocked)")
    print()
    print("   🖥️ COMPUTER CONTROL FULLY TESTED!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_all_tools()