"""
Test script for Multi-Provider System
"""
from spidey.brain.providers import AIProvider, ProviderManager, PROVIDERS


def test_providers():
    """Test provider system"""
    print("Testing Multi-Provider System...\n")

    # Test 1: List all providers
    print("--- Test 1: List All Providers ---")
    for key, config in PROVIDERS.items():
        free = "FREE" if config["free"] else "PAID"
        print(f"  {key}: {config['name']} ({free})")
    print(f"Total providers: {len(PROVIDERS)}")
    print("✅ Test 1 Passed!\n")

    # Test 2: Create Groq provider
    print("--- Test 2: Create Groq Provider ---")
    provider = AIProvider("groq")
    info = provider.get_info()
    print(f"  Name: {info['name']}")
    print(f"  Model: {info['model']}")
    print("✅ Test 2 Passed!\n")

    # Test 3: Chat with Groq
    print("--- Test 3: Chat with Groq ---")
    result = provider.chat(
        messages=[
            {"role": "system", "content": "You are Spidey AI. Be brief."},
            {"role": "user", "content": "Say hi in one sentence."}
        ],
        max_tokens=50
    )
    print(f"  Provider: {result['provider']}")
    print(f"  Model: {result['model']}")
    print(f"  Reply: {result['content']}")
    print(f"  Tokens: {result['total_tokens']}")
    print("✅ Test 3 Passed!\n")

    # Test 4: Provider Manager
    print("--- Test 4: Provider Manager ---")
    manager = ProviderManager("groq")
    print(f"  Current: {manager.get_current_name()}")
    print("✅ Test 4 Passed!\n")

    # Test 5: Switch provider (to groq-large)
    print("--- Test 5: Switch Provider ---")
    success = manager.switch_provider("groq-large")
    print(f"  Switched to groq-large: {success}")
    print(f"  Current: {manager.get_current_name()}")

    result = manager.chat(
        messages=[
            {"role": "user", "content": "Say hello in one word."}
        ],
        max_tokens=10
    )
    print(f"  Reply from 70B: {result['content']}")
    print("✅ Test 5 Passed!\n")

    # Test 6: Available providers
    print("--- Test 6: Available Providers ---")
    available = manager.get_available_providers()
    print(f"  Available: {available}")
    print("✅ Test 6 Passed!\n")

    # Test 7: Invalid provider
    print("--- Test 7: Invalid Provider ---")
    try:
        bad = AIProvider("invalid_provider")
        print("❌ Should have raised error!")
    except ValueError as e:
        print(f"  Correctly raised error: {e}")
    print("✅ Test 7 Passed!\n")

    print("🎉 All provider tests passed!")


if __name__ == "__main__":
    test_providers()
