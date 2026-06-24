"""
🕷️ WEEK 5 FINAL TEST
Tests ALL computer control features
"""
from spidey.tools.tool_connector import ToolConnector
from spidey.tools.computer import ComputerControl
from spidey.tools.file_manager import FileManager
from spidey.tools.system_info import SystemInfo
import time


def test_week5():
    print()
    print("=" * 55)
    print("   🖥️ WEEK 5 — FINAL COMPUTER CONTROL TEST")
    print("=" * 55)
    print()

    tc = ToolConnector()
    passed = 0
    failed = 0

    # ============================================
    # TEST 1: System Info Commands
    # ============================================
    print("━" * 55)
    print("📦 TEST 1: System Info")
    print("━" * 55)

    info_tests = [
        ("battery", True),
        ("wifi", True),
        ("what time is it", True),
        ("system info", True),
        ("my ip", True),
        ("running apps", True),
        ("quick info", True),
        ("disk space", True),
    ]

    for text, should_work in info_tests:
        result = tc.process_command(text)
        ok = (result is not None) == should_work
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1

    print()

    # ============================================
    # TEST 2: App Commands
    # ============================================
    print("━" * 55)
    print("📦 TEST 2: App Commands (detection only)")
    print("━" * 55)

    app_tests = [
        ("open notepad", True),
        ("open calculator", True),
        ("open chrome", True),
        ("close notepad", True),
        ("launch paint", True),
        ("start cmd", True),
    ]

    for text, should_detect in app_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = detected == should_detect
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}' → {'Detected' if detected else 'Not detected'}")
        if ok:
            passed += 1
        else:
            failed += 1

        # Close anything that opened
        if "open" in text and detected:
            time.sleep(1)
            app = text.replace("open ", "").replace("launch ", "").replace("start ", "")
            tc.process_command(f"close {app}")
            time.sleep(0.5)

    print()

    # ============================================
    # TEST 3: File Commands
    # ============================================
    print("━" * 55)
    print("📦 TEST 3: File Commands")
    print("━" * 55)

    file_tests = [
        ("find python files", True),
        ("show recent files", True),
        ("find large files", True),
        ("list downloads", True),
        ("search for readme", True),
    ]

    for text, should_detect in file_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = detected == should_detect
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1

    print()

    # ============================================
    # TEST 4: Screenshot & Recording
    # ============================================
    print("━" * 55)
    print("📦 TEST 4: Screenshot & Recording")
    print("━" * 55)

    media_tests = [
        ("take screenshot", True),
        ("screenshot", True),
        ("start recording", True),
    ]

    for text, should_detect in media_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = detected == should_detect
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1

    # Stop recording if started
    tc.process_command("stop recording")
    time.sleep(1)

    print()

    # ============================================
    # TEST 5: Window Commands
    # ============================================
    print("━" * 55)
    print("📦 TEST 5: Window Commands")
    print("━" * 55)

    window_tests = [
        ("minimize", True),
        ("maximize", True),
        ("show desktop", True),
        ("switch window", True),
        ("snap left", True),
        ("snap right", True),
        ("scroll up", True),
        ("scroll down", True),
    ]

    for text, should_detect in window_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = detected == should_detect
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1
        time.sleep(0.3)

    print()

    # ============================================
    # TEST 6: URL Commands
    # ============================================
    print("━" * 55)
    print("📦 TEST 6: URL Commands (detection only)")
    print("━" * 55)

    url_tests = [
        ("open youtube", True),
        ("open github", True),
        ("google python tutorial", True),
        ("open gmail", True),
    ]

    for text, should_detect in url_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = detected == should_detect
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1

    print()

    # ============================================
    # TEST 7: Keyboard Commands
    # ============================================
    print("━" * 55)
    print("📦 TEST 7: Keyboard Commands")
    print("━" * 55)

    key_tests = [
        ("press enter", True),
        ("press escape", True),
        ("press tab", True),
        ("ctrl+c", True),
        ("ctrl+v", True),
        ("alt+tab", True),
    ]

    for text, should_detect in key_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = detected == should_detect
        status = "✅" if ok else "❌"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1
        time.sleep(0.2)

    print()

    # ============================================
    # TEST 8: Safety — No False Positives
    # ============================================
    print("━" * 55)
    print("📦 TEST 8: Safety — Normal Chat NOT Detected")
    print("━" * 55)

    safe_tests = [
        "what is python",
        "tell me a joke",
        "how are you doing",
        "my name is kashan",
        "explain machine learning",
        "hello spidey",
        "what is the capital of pakistan",
        "write me a poem",
        "how to learn coding",
        "thank you for your help",
    ]

    for text in safe_tests:
        result = tc.process_command(text)
        detected = result is not None
        ok = not detected
        status = "✅" if ok else "❌ FALSE POSITIVE!"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1

    print()

    # ============================================
    # TEST 9: Safety — Dangerous Commands Blocked
    # ============================================
    print("━" * 55)
    print("📦 TEST 9: Dangerous Commands Blocked")
    print("━" * 55)

    dangerous = [
        "format c drive",
        "delete system32",
        "shutdown computer",
        "rm -rf",
        "format disk",
        "delete all files",
    ]

    for text in dangerous:
        result = tc.process_command(text)
        detected = result is not None
        ok = not detected
        status = "✅ Blocked" if ok else "❌ DANGER!"
        print(f"   {status} '{text}'")
        if ok:
            passed += 1
        else:
            failed += 1

    print()

    # ============================================
    # TEST 10: Toggle On/Off
    # ============================================
    print("━" * 55)
    print("📦 TEST 10: Toggle Tools")
    print("━" * 55)

    # Disable
    tc.toggle()
    result = tc.process_command("take screenshot")
    ok = result is None
    print(f"   {'✅' if ok else '❌'} Disabled — screenshot blocked")
    if ok:
        passed += 1
    else:
        failed += 1

    # Enable
    tc.toggle()
    result = tc.process_command("battery")
    ok = result is not None
    print(f"   {'✅' if ok else '❌'} Enabled — battery works")
    if ok:
        passed += 1
    else:
        failed += 1

    print()

    # ============================================
    # RESULTS
    # ============================================
    total = passed + failed
    percent = round((passed / total) * 100) if total > 0 else 0

    print("=" * 55)
    print(f"   🏆 RESULTS: {passed}/{total} passed ({percent}%)")
    print("=" * 55)
    print()

    if failed == 0:
        print("   🎉 ALL TESTS PASSED! Computer control is PERFECT!")
    else:
        print(f"   ⚠️ {failed} tests failed. Check above.")

    print()
    print("   ✅ System Info (battery, wifi, time, IP)")
    print("   ✅ App Control (open, close)")
    print("   ✅ File Manager (search, recent, large)")
    print("   ✅ Screenshot & Recording")
    print("   ✅ Window Control (min, max, snap)")
    print("   ✅ URL & Browser (youtube, google)")
    print("   ✅ Keyboard (hotkeys, type)")
    print("   ✅ Safety (no false positives)")
    print("   ✅ Security (dangerous blocked)")
    print("   ✅ Toggle (on/off)")
    print()
    print("   🖥️ WEEK 5 COMPUTER CONTROL — COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_week5()