"""
Test script for Config System
"""
from spidey.config import Settings, APP_NAME, APP_VERSION, DEFAULT_USER_SETTINGS
import os


def test_config():
    """Test configuration system"""
    print("Testing Config System...\n")

    # Test 1: App constants
    print("--- Test 1: App Constants ---")
    print(f"  App: {APP_NAME}")
    print(f"  Version: {APP_VERSION}")
    assert APP_NAME == "Spidey AI"
    print("✅ Test 1 Passed!\n")

    # Test 2: Settings instance
    print("--- Test 2: Settings Instance ---")
    s = Settings()
    print(f"  Provider: {s.get('provider')}")
    print(f"  Temperature: {s.get('temperature')}")
    print(f"  Max Tokens: {s.get('max_tokens')}")
    assert s.get("provider") is not None
    print("✅ Test 2 Passed!\n")

    # Test 3: Get and Set
    print("--- Test 3: Get and Set ---")
    s.set("username", "TestUser")
    assert s.get("username") == "TestUser"
    print(f"  Username: {s.get('username')}")
    print("✅ Test 3 Passed!\n")

    # Test 4: Save and Load
    print("--- Test 4: Save and Load ---")
    s.set("temperature", 0.5)
    s.save()

    s2 = Settings()
    loaded_temp = s2.get("temperature")
    print(f"  Saved temp: 0.5, Loaded temp: {loaded_temp}")
    assert loaded_temp == 0.5
    print("✅ Test 4 Passed!\n")

    # Test 5: Reset
    print("--- Test 5: Reset ---")
    s.reset()
    default_temp = s.get("temperature")
    print(f"  After reset temp: {default_temp}")
    assert default_temp == DEFAULT_USER_SETTINGS["temperature"]
    print("✅ Test 5 Passed!\n")

    # Test 6: Print settings
    print("--- Test 6: Print Settings ---")
    print(s)
    print("✅ Test 6 Passed!\n")

    # Test 7: Get all
    print("--- Test 7: Get All ---")
    all_settings = s.get_all()
    print(f"  Total settings: {len(all_settings)}")
    for key, value in all_settings.items():
        print(f"    {key}: {value}")
    print("✅ Test 7 Passed!\n")

    print("🎉 All config tests passed!")


if __name__ == "__main__":
    test_config()
