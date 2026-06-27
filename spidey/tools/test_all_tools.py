"""
Spidey Tools — Complete Test Suite
Tests ALL internet tools with success & error cases
Day 42 — Final testing & error handling
"""

import time
import sys
from datetime import datetime


class ToolTester:
    """Complete test suite for all Spidey tools"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.total_time = 0

    def run_test(self, test_name, test_func):
        """Run a single test and record result"""
        print(f"\n  🧪 {test_name}...", end=" ")
        start = time.time()

        try:
            result = test_func()
            elapsed = time.time() - start
            self.total_time += elapsed

            if result and "⚠️" not in str(result)[:5]:
                self.passed += 1
                print(f"✅ PASS ({elapsed:.1f}s)")
                self.results.append(("PASS", test_name, elapsed))
                return result
            elif "⚠️" in str(result)[:5]:
                self.failed += 1
                print(f"⚠️ WARNING ({elapsed:.1f}s)")
                print(f"     {str(result)[:100]}")
                self.results.append(("WARN", test_name, elapsed))
                return result
            else:
                self.failed += 1
                print(f"❌ FAIL — Empty result")
                self.results.append(("FAIL", test_name, elapsed))
                return None

        except Exception as e:
            elapsed = time.time() - start
            self.total_time += elapsed
            self.failed += 1
            print(f"❌ ERROR ({elapsed:.1f}s)")
            print(f"     {str(e)[:100]}")
            self.results.append(("ERROR", test_name, elapsed))
            return None

    def skip_test(self, test_name, reason):
        """Skip a test"""
        print(f"\n  ⏭️ {test_name}... SKIPPED — {reason}")
        self.skipped += 1
        self.results.append(("SKIP", test_name, 0))

    def print_summary(self):
        """Print final test summary"""
        total = self.passed + self.failed + self.skipped
        print("\n")
        print("=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"  ✅ Passed:  {self.passed}")
        print(f"  ❌ Failed:  {self.failed}")
        print(f"  ⏭️ Skipped: {self.skipped}")
        print(f"  📦 Total:   {total}")
        print(f"  ⏱️ Time:    {self.total_time:.1f}s")
        print("=" * 60)

        if self.failed == 0:
            print("  🎉 ALL TESTS PASSED! Spidey tools are ready!")
        else:
            print(f"  ⚠️ {self.failed} test(s) need attention")

        print("=" * 60)


def test_weather_tool(tester):
    """Test Weather Tool"""
    print("\n" + "=" * 60)
    print("🌤️ WEATHER TOOL TESTS")
    print("=" * 60)

    try:
        from spidey.tools.weather_tool import WeatherTool
        tool = WeatherTool()
    except ImportError as e:
        tester.skip_test("Weather Tool Import", str(e))
        return

    if not tool.is_available():
        tester.skip_test("Weather Tool", "OPENWEATHER_API_KEY not set")
        return

    # Test 1: Valid city
    result = tester.run_test(
        "Current weather — Karachi",
        lambda: tool.get_current_weather("Karachi")
    )
    if result:
        print(f"     Preview: {result[:80].replace(chr(10), ' ')}...")

    # Test 2: Another city
    tester.run_test(
        "Current weather — London",
        lambda: tool.get_current_weather("London")
    )

    # Test 3: Fahrenheit
    tester.run_test(
        "Weather in Fahrenheit — New York",
        lambda: tool.get_current_weather("New York", units="imperial")
    )

    # Test 4: Forecast
    tester.run_test(
        "3-day forecast — Lahore",
        lambda: tool.get_forecast("Lahore", days=3)
    )

    # Test 5: Invalid city
    result = tester.run_test(
        "Invalid city (should handle gracefully)",
        lambda: tool.get_current_weather("xyzabc123")
    )
    # This should return error message, not crash
    if result and "not found" in result.lower():
        print("     ✅ Error handled correctly!")

    # Test 6: Empty city
    tester.run_test(
        "Empty city name",
        lambda: tool.get_current_weather("")
    )

    # Test 7: Multi-city
    tester.run_test(
        "Multi-city weather",
        lambda: tool.get_multi_city_weather(["Karachi", "Islamabad"])
    )


def test_news_tool(tester):
    """Test News Tool"""
    print("\n" + "=" * 60)
    print("📰 NEWS TOOL TESTS")
    print("=" * 60)

    try:
        from spidey.tools.news_tool import NewsTool
        tool = NewsTool()
    except ImportError as e:
        tester.skip_test("News Tool Import", str(e))
        return

    # Test 1: Top headlines
    result = tester.run_test(
        "Top headlines — US",
        lambda: tool.get_top_headlines(country="us", count=3)
    )
    if result:
        print(f"     Preview: {result[:80].replace(chr(10), ' ')}...")

    # Test 2: Pakistan news
    tester.run_test(
        "Top headlines — Pakistan",
        lambda: tool.get_top_headlines(country="pk", count=3)
    )

    # Test 3: Category news
    tester.run_test(
        "Technology news",
        lambda: tool.get_category_news("technology", count=3)
    )

    # Test 4: Sports news
    tester.run_test(
        "Sports news",
        lambda: tool.get_category_news("sports", count=3)
    )

    # Test 5: Invalid category
    tester.run_test(
        "Invalid category (should handle)",
        lambda: tool.get_category_news("fakecategory", count=3)
    )

    # Test 6: RSS backup
    tester.run_test(
        "RSS feed — World news",
        lambda: tool.get_rss_news("world", count=3)
    )

    # Test 7: RSS tech
    tester.run_test(
        "RSS feed — Technology",
        lambda: tool.get_rss_news("technology", count=3)
    )

    # Test 8: Search news (if API key available)
    if tool.api_key:
        tester.run_test(
            "Search news — AI",
            lambda: tool.search_news("artificial intelligence", count=3)
        )
    else:
        tester.skip_test("Search news", "No API key")

    # Test 9: Available options
    tester.run_test(
        "Available categories",
        lambda: ", ".join(tool.get_available_categories())
    )


def test_search_tool(tester):
    """Test Search Tool"""
    print("\n" + "=" * 60)
    print("🔍 SEARCH TOOL TESTS")
    print("=" * 60)

    try:
        from spidey.tools.search_tool import SearchTool
        tool = SearchTool()
    except ImportError as e:
        tester.skip_test("Search Tool Import", str(e))
        return

    # Test 1: Basic search
    result = tester.run_test(
        "Text search — Python programming",
        lambda: tool.search("Python programming", count=3)
    )
    if result:
        print(f"     Preview: {result[:80].replace(chr(10), ' ')}...")

    # Test 2: Quick answer
    tester.run_test(
        "Quick answer — What is Python",
        lambda: tool.search_quick("What is Python programming language")
    )

    # Test 3: News search
    tester.run_test(
        "News search — AI 2025",
        lambda: tool.search_news("artificial intelligence 2025", count=3)
    )

    # Test 4: Video search
    tester.run_test(
        "Video search — Python tutorial",
        lambda: tool.search_videos("Python tutorial for beginners", count=3)
    )

    # Test 5: Image search
    tester.run_test(
        "Image search — AI robot",
        lambda: tool.search_images("AI robot", count=3)
    )

    # Test 6: Empty query
    tester.run_test(
        "Empty search query",
        lambda: tool.search("", count=3)
    )

    # Test 7: Page summary
    tester.run_test(
        "Page summary — Wikipedia",
        lambda: tool.get_page_summary(
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            max_chars=300
        )
    )

    # Test 8: Regional search
    tester.run_test(
        "Regional search — Pakistan",
        lambda: tool.search("best universities", count=3, region="pk-en")
    )


def test_wiki_tool(tester):
    """Test Wikipedia Tool"""
    print("\n" + "=" * 60)
    print("📚 WIKIPEDIA TOOL TESTS")
    print("=" * 60)

    try:
        from spidey.tools.wiki_tool import WikiTool
        tool = WikiTool()
    except ImportError as e:
        tester.skip_test("Wiki Tool Import", str(e))
        return

    # Test 1: Summary
    result = tester.run_test(
        "Summary — Python",
        lambda: tool.get_summary("Python (programming language)", sentences=3)
    )
    if result:
        print(f"     Preview: {result[:80].replace(chr(10), ' ')}...")

    # Test 2: Summary — Pakistan
    tester.run_test(
        "Summary — Pakistan",
        lambda: tool.get_summary("Pakistan", sentences=3)
    )

    # Test 3: Quick fact
    tester.run_test(
        "Quick fact — Earth",
        lambda: tool.quick_fact("Earth")
    )

    # Test 4: Search
    tester.run_test(
        "Search — Artificial Intelligence",
        lambda: tool.search("Artificial Intelligence", count=5)
    )

    # Test 5: Sections
    tester.run_test(
        "Sections — Machine Learning",
        lambda: tool.get_sections("Machine learning")
    )

    # Test 6: Related topics
    tester.run_test(
        "Related topics — Python",
        lambda: tool.get_related("Python (programming language)", count=5)
    )

    # Test 7: Invalid topic
    result = tester.run_test(
        "Invalid topic (should handle)",
        lambda: tool.get_summary("xyzabc123456fakepage")
    )
    if result and ("not found" in result.lower() or "did you mean" in result.lower()):
        print("     ✅ Error handled correctly!")

    # Test 8: Urdu summary
    tester.run_test(
        "Urdu summary — Pakistan",
        lambda: tool.get_urdu_summary("پاکستان", sentences=3)
    )

    # Test 9: Full article (truncated)
    tester.run_test(
        "Full article — AI (500 chars)",
        lambda: tool.get_full_article("Artificial intelligence", max_chars=500)
    )

    # Test 10: Quick facts batch
    tester.run_test(
        "Batch facts — Planets",
        lambda: "\n".join([
            tool.quick_fact(t) for t in ["Earth", "Mars", "Jupiter"]
        ])
    )


def test_tool_connector(tester):
    """Test Tool Connector — Intent Detection"""
    print("\n" + "=" * 60)
    print("🔧 TOOL CONNECTOR TESTS")
    print("=" * 60)

    try:
        from spidey.tools.tool_connector import ToolConnector
        connector = ToolConnector()
    except ImportError as e:
        tester.skip_test("Tool Connector Import", str(e))
        return

    # Test: Tools loaded
    tester.run_test(
        "All tools loaded",
        lambda: connector._list_tools()
    )

    # Weather intent tests
    weather_tests = [
        "Karachi ka weather kya hai?",
        "What is the temperature in London?",
        "Lahore mein barish hogi?",
        "/weather Dubai",
    ]

    for msg in weather_tests:
        tester.run_test(
            f"Weather intent: '{msg[:35]}...'",
            lambda m=msg: connector.process_command(m)
        )

    # News intent tests
    news_tests = [
        "Latest news dikhao",
        "Tech news show karo",
        "/news sports",
    ]

    for msg in news_tests:
        tester.run_test(
            f"News intent: '{msg[:35]}...'",
            lambda m=msg: connector.process_command(m)
        )

    # Wiki intent tests
    wiki_tests = [
        "Python kya hota hai?",
        "Who is Elon Musk?",
        "/wiki Pakistan",
    ]

    for msg in wiki_tests:
        tester.run_test(
            f"Wiki intent: '{msg[:35]}...'",
            lambda m=msg: connector.process_command(m)
        )

    # Search intent tests
    search_tests = [
        "Search best laptops 2025",
        "/search Python frameworks",
    ]

    for msg in search_tests:
        tester.run_test(
            f"Search intent: '{msg[:35]}...'",
            lambda m=msg: connector.process_command(m)
        )

    # NO tool should match — should return None
    no_tool_tests = [
        "Hello how are you?",
        "Tell me a joke",
        "Mera naam kya hai?",
        "Good morning",
    ]

    for msg in no_tool_tests:
        result = connector.process_command(msg)
        if result is None:
            tester.passed += 1
            print(f"\n  🧪 No tool for: '{msg}'... ✅ PASS (correctly None)")
            tester.results.append(("PASS", f"No tool: '{msg}'", 0))
        else:
            tester.failed += 1
            print(f"\n  🧪 No tool for: '{msg}'... ❌ FAIL (tool fired incorrectly)")
            tester.results.append(("FAIL", f"No tool: '{msg}'", 0))

    # Direct commands
    tester.run_test(
        "Direct: /tools",
        lambda: connector.process_command("/tools")
    )

    tester.run_test(
        "Direct: /fact Earth",
        lambda: connector.process_command("/fact Earth")
    )

    # Toggle test
    tester.run_test(
        "Toggle tools off/on",
        lambda: (connector.toggle(), connector.toggle())[1]
    )


def test_error_handling(tester):
    """Test error handling across all tools"""
    print("\n" + "=" * 60)
    print("🛡️ ERROR HANDLING TESTS")
    print("=" * 60)

    # Weather — invalid city
    try:
        from spidey.tools.weather_tool import WeatherTool
        tool = WeatherTool()
        if tool.is_available():
            result = tester.run_test(
                "Weather — Invalid city",
                lambda: tool.get_current_weather("zzzfakecity999")
            )
            if result and ("not found" in result.lower() or "⚠️" in result):
                print("     ✅ Graceful error!")

            result = tester.run_test(
                "Weather — Special characters",
                lambda: tool.get_current_weather("@#$%^&*()")
            )
            if result and "⚠️" in result:
                print("     ✅ Graceful error!")
    except Exception:
        pass

    # Wiki — invalid topic
    try:
        from spidey.tools.wiki_tool import WikiTool
        tool = WikiTool()
        result = tester.run_test(
            "Wiki — Invalid topic",
            lambda: tool.get_summary("zzzzfaketopic99999")
        )
        if result and ("not found" in result.lower() or "⚠️" in result):
            print("     ✅ Graceful error!")
    except Exception:
        pass

    # Search — empty query
    try:
        from spidey.tools.search_tool import SearchTool
        tool = SearchTool()
        tester.run_test(
            "Search — Very long query",
            lambda: tool.search("a " * 500, count=2)
        )
    except Exception:
        pass

    # News — invalid category
    try:
        from spidey.tools.news_tool import NewsTool
        tool = NewsTool()
        result = tester.run_test(
            "News — Invalid category",
            lambda: tool.get_category_news("fakecategory123")
        )
        if result and "⚠️" in result:
            print("     ✅ Graceful error!")

        # Invalid RSS topic
        result = tester.run_test(
            "News — Invalid RSS topic",
            lambda: tool.get_rss_news("faketopic123")
        )
        if result and "⚠️" in result:
            print("     ✅ Graceful error!")
    except Exception:
        pass


# ========================================
# Main Runner
# ========================================
if __name__ == "__main__":
    print("🕷️" + "=" * 58)
    print("   SPIDEY AI — COMPLETE TOOL TEST SUITE")
    print("   Day 42 — Testing All Internet Tools")
    print("   " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🕷️" + "=" * 58)

    tester = ToolTester()

    # Ask user what to test
    print("\n📋 What do you want to test?")
    print("  1. All tools (full test)")
    print("  2. Weather only")
    print("  3. News only")
    print("  4. Search only")
    print("  5. Wiki only")
    print("  6. Tool Connector only")
    print("  7. Error handling only")
    print("  0. Quick test (1 test per tool)")

    choice = input("\n  Enter choice (0-7) [default=1]: ").strip()

    if not choice or choice == "1":
        # Full test
        test_weather_tool(tester)
        test_news_tool(tester)
        test_search_tool(tester)
        test_wiki_tool(tester)
        test_tool_connector(tester)
        test_error_handling(tester)

    elif choice == "2":
        test_weather_tool(tester)

    elif choice == "3":
        test_news_tool(tester)

    elif choice == "4":
        test_search_tool(tester)

    elif choice == "5":
        test_wiki_tool(tester)

    elif choice == "6":
        test_tool_connector(tester)

    elif choice == "7":
        test_error_handling(tester)

    elif choice == "0":
        # Quick test — 1 test per tool
        print("\n⚡ QUICK TEST MODE\n")

        try:
            from spidey.tools.weather_tool import WeatherTool
            tool = WeatherTool()
            if tool.is_available():
                tester.run_test("Quick Weather", lambda: tool.get_current_weather("Karachi"))
        except Exception:
            tester.skip_test("Quick Weather", "Import failed")

        try:
            from spidey.tools.news_tool import NewsTool
            tool = NewsTool()
            tester.run_test("Quick News", lambda: tool.get_rss_news("world", count=2))
        except Exception:
            tester.skip_test("Quick News", "Import failed")

        try:
            from spidey.tools.search_tool import SearchTool
            tool = SearchTool()
            tester.run_test("Quick Search", lambda: tool.search("Python", count=2))
        except Exception:
            tester.skip_test("Quick Search", "Import failed")

        try:
            from spidey.tools.wiki_tool import WikiTool
            tool = WikiTool()
            tester.run_test("Quick Wiki", lambda: tool.quick_fact("Earth"))
        except Exception:
            tester.skip_test("Quick Wiki", "Import failed")

        try:
            from spidey.tools.tool_connector import ToolConnector
            c = ToolConnector()
            tester.run_test("Quick Connector", lambda: c.process_command("/tools"))
        except Exception:
            tester.skip_test("Quick Connector", "Import failed")

    # Print summary
    tester.print_summary()