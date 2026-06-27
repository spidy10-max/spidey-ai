"""
Spidey Tools — Error Handler
Centralized error handling for all tools
Day 42
"""

import time
import requests
from functools import wraps


class ToolError(Exception):
    """Base error for tool failures"""
    def __init__(self, tool_name, message, suggestion=""):
        self.tool_name = tool_name
        self.message = message
        self.suggestion = suggestion
        super().__init__(f"[{tool_name}] {message}")


def safe_request(func):
    """
    Decorator: Wraps any function that makes HTTP requests.
    Handles common network errors gracefully.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. Internet slow hai ya server down hai."

        except requests.exceptions.ConnectionError:
            return "⚠️ No internet connection. WiFi/data check karo."

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "Unknown"

            error_messages = {
                400: "⚠️ Bad request — check your input.",
                401: "⚠️ Invalid API key. .env file check karo.",
                403: "⚠️ Access denied. API key permissions check karo.",
                404: "⚠️ Not found. Check spelling or try different query.",
                429: "⚠️ Rate limit reached. Thodi der baad try karo.",
                500: "⚠️ Server error. Try again later.",
                502: "⚠️ Server down. Try again later.",
                503: "⚠️ Service unavailable. Try again later."
            }

            return error_messages.get(
                status,
                f"⚠️ HTTP Error {status}: {str(e)}"
            )

        except requests.exceptions.RequestException as e:
            return f"⚠️ Network error: {str(e)}"

        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"

    return wrapper


def retry(max_attempts=3, delay=1):
    """
    Decorator: Retry a function multiple times before giving up.
    
    Usage:
        @retry(max_attempts=3, delay=1)
        def fetch_data():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts:
                        time.sleep(delay)

            return f"⚠️ Failed after {max_attempts} attempts: {str(last_error)}"

        return wrapper
    return decorator


def validate_input(value, name, min_len=1, max_len=200):
    """
    Validate user input before sending to API.
    
    Args:
        value: Input value to validate
        name: Name of the field (for error messages)
        min_len: Minimum length
        max_len: Maximum length
    
    Returns:
        (True, cleaned_value) or (False, error_message)
    """
    if not value or not str(value).strip():
        return False, f"⚠️ {name} is empty. Please provide a value."

    cleaned = str(value).strip()

    if len(cleaned) < min_len:
        return False, f"⚠️ {name} is too short. Minimum {min_len} characters."

    if len(cleaned) > max_len:
        return False, f"⚠️ {name} is too long. Maximum {max_len} characters."

    # Remove dangerous characters
    dangerous = ["<script>", "javascript:", "DROP TABLE", "DELETE FROM"]
    for d in dangerous:
        if d.lower() in cleaned.lower():
            return False, f"⚠️ Invalid input detected in {name}."

    return True, cleaned


# ========================================
# Test
# ========================================
if __name__ == "__main__":
    print("🛡️ Error Handler — Testing\n")

    # Test validate_input
    tests = [
        ("Karachi", "city"),
        ("", "city"),
        ("a", "city"),
        ("x" * 300, "city"),
        ("<script>alert('hack')</script>", "city"),
        ("Normal query", "search"),
    ]

    for value, name in tests:
        valid, result = validate_input(value, name)
        status = "✅" if valid else "❌"
        print(f"  {status} validate('{value[:30]}...', '{name}') → {result[:50]}")