# ============================================
# PRACTICE 2: Decorators Samajhna
# ============================================

import time

# Decorator 1: Time measure karne wala
def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️  '{func.__name__}' took {end - start:.4f} seconds")
        return result
    return wrapper


# Decorator 2: Logging karne wala
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"📝 LOG: Calling function '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"✅ LOG: Function '{func.__name__}' completed")
        return result
    return wrapper


# Ab decorators use karte hain
@measure_time
@log_action
def process_message(message):
    print(f"🤖 Processing: {message}")
    time.sleep(1)  # 1 second wait (jaise AI soch raha ho)
    return f"Response to: {message}"


# Test
print("="*50)
result = process_message("Hello Spidey!")
print(f"Final Result: {result}")
print("="*50)