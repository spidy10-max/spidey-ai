"""
Test YouTube Search
"""
from spidey.tools.internet.youtube import YouTubeTool
from spidey.tools.tool_connector import ToolConnector


def test_youtube():
    print()
    print("=" * 55)
    print("   🎬 YOUTUBE TOOL TEST")
    print("=" * 55)
    print()

    yt = YouTubeTool()

    # Test 1: Search
    print("--- Test 1: YouTube Search ---")
    if yt.is_available():
        result = yt.search("Python tutorial for beginners", max_results=3)
        print(result)
    else:
        print("   ⚠️ Not available")
    print("\n✅ Test 1 Done!\n")

    # Test 2: Get URL
    print("--- Test 2: Get Video URL ---")
    if yt.is_available():
        url = yt.get_video_url("Python tutorial")
        print(f"   URL: {url}")
    print("\n✅ Test 2 Done!\n")

    # Test 3: NLP Detection
    print("--- Test 3: Command Detection ---")
    tc = ToolConnector()

    tests = [
        "youtube Python tutorial",
        "yt coding tips",
        "play music on youtube",
        "find videos about AI",
        "search youtube for gaming",
    ]

    for text in tests:
        result = tc.process_command(text)
        status = "✅" if result else "❌"
        print(f"   {status} '{text}'")
        if result:
            first = result.split("\n")[0]
            print(f"      → {first[:60]}...")

    print("\n✅ Test 3 Done!\n")

    # Test 4: No False Positives
    print("--- Test 4: No False Positives ---")
    safe = [
        "what is python",
        "my name is kashan",
        "hello how are you",
    ]
    for text in safe:
        result = tc.process_command(text)
        status = "✅" if not result else "❌ FALSE POSITIVE!"
        print(f"   {status} '{text}'")

    print("\n✅ Test 4 Done!\n")

    print("=" * 55)
    print("   🎉 YOUTUBE TEST COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_youtube()