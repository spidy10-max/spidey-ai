"""
Test Internet Tools — Weather, Search, Wikipedia
"""
from spidey.tools.internet.weather import WeatherTool
from spidey.tools.internet.search import SearchTool
from spidey.tools.internet.wiki import WikiTool
from spidey.tools.tool_connector import ToolConnector


def test_internet():
    print()
    print("=" * 55)
    print("   🌐 INTERNET TOOLS TEST")
    print("=" * 55)
    print()

    # Test 1: Weather
    print("--- Test 1: Weather ---")
    w = WeatherTool()
    if w.is_available():
        result = w.get_weather("Kotaddu")
        print(result)
        print()
        result = w.get_weather("Karachi")
        print(result)
    else:
        print("   ⚠️ No API key. Add OPENWEATHER_API_KEY to .env")
    print("\n✅ Test 1 Done!\n")

    # Test 2: Web Search
    print("--- Test 2: Web Search ---")
    s = SearchTool()
    if s.is_available():
        result = s.search("Python programming", max_results=3)
        print(result)
    else:
        print("   ⚠️ DuckDuckGo not installed")
    print("\n✅ Test 2 Done!\n")

    # Test 3: News
    print("--- Test 3: News ---")
    if s.is_available():
        result = s.search_news("Pakistan", max_results=3)
        print(result)
    print("\n✅ Test 3 Done!\n")

    # Test 4: Wikipedia
    print("--- Test 4: Wikipedia ---")
    wiki = WikiTool()
    if wiki.is_available():
        result = wiki.get_summary("Python programming language")
        print(result)
    else:
        print("   ⚠️ Wikipedia not installed")
    print("\n✅ Test 4 Done!\n")

    # Test 5: NLP Detection
    print("--- Test 5: Command Detection ---")
    tc = ToolConnector()

    tests = [
        "weather in Kotaddu",
        "weather in Karachi",
        "search for Python tutorial",
        "news about Pakistan",
        "wikipedia Python",
        "what is machine learning",
        "latest news",
    ]

    for text in tests:
        result = tc.process_command(text)
        status = "✅" if result else "❌"
        print(f"   {status} '{text}'")
        if result:
            # Show first line only
            first_line = result.split("\n")[0]
            print(f"      → {first_line[:60]}...")

    print("\n✅ Test 5 Done!\n")

    print("=" * 55)
    print("   🎉 INTERNET TOOLS TEST COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_internet()