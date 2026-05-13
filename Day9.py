# Exception types ------ Intentionally trigger and catch each type

# KeyError
try:
    data = {"id":1}
    email= data["email"]
except KeyError as e:
    print(f"KeyError: missing key {e}") # KeyError: missing key 'email'

# TypeError
try:
    result = "Status: " + 200
except TypeError as e:
    print(f"TypeError: {e}") # TypeError: can only concatenate str (not "int") to str

# ValueError
try:
    port = int("not_a_number")
except ValueError as e:
    print(f"ValueError: {e}") # ValueError: invalid literal for int() with base 10: 'not_a_number'

# IndexError
try:
    result = ["PASS", "FAIL"]
    third = result[5]
except IndexError as e:
    print(f"IndexError: {e}") # IndexError: list index out of range

# AttributeError
try:
    text = None
    clean = text.strip()
except AttributeError as e:
    print(f"AttributeError: {e}") # AttributeError: 'NoneType' object has no attribute 'strip'
    

print("="*50)

# ==========================================================================================================


# else and finally 

# else - runs ONLY on success
from typing import Optional

def parse_user_id(value: str) -> Optional[int]: #int | None
    """Parse a string to user ID. Returns None as failure."""
    try:
        user_id = int(value)
    except ValueError:
        print(f" Cannot parse '{value}' as integer")
        return None
    else:
        print(f" Parsed successfully: {user_id}") # ONLY runs on success
        return user_id
    
for val in ["2", "abc", "99", ""]:
    result = parse_user_id(val)
    print(f"  -> result : {result}\n")

print()

# finally - ALWAYS runs, use for cleanup
def run_with_cleanup(test_name: str, should_fail: bool = False):
    """Simulate a test with guaranteed cleanup. """
    print(f"[{test_name}] Setting up test data...")

    try:
        if should_fail:
            raise AssertionError("Element not found")
        print(f"[{test_name}] Test actions completed")
    
    except AssertionError as e:
        print(f"[{test_name}] FAIL: {e}")
    
    finally:
        # This ALWAYS runs - cleanup test data
        print(f"[{test_name}] Cleanup: deleting test data...")

run_with_cleanup("test_login", should_fail=False)
print()
run_with_cleanup("test_checkout", should_fail=True)

print("="*50)

# ==========================================================================================================

# raise — deliberately triggering exceptions 

# raise with a build-in exception type
def set_timeout(ms: int) ->int:
    """ Set test timeout. Must be between 1000 and 30000ms. """
    if not isinstance(ms, int):
        raise TypeError(f"Timeout must be int, got {type(ms).__name__}")
    if ms < 1000:
        raise ValueError(f"Timeout too low: {ms}ms (minimum 1000ms)")
    if ms > 300000:
        raise ValueError(f"Timeout too high: {ms}ms (maximum 30000ms)")
    return ms

# Test valid and invalid values
for val in [5000, 500, 50000, "5000"]:
    try:
        result = set_timeout(val)
        print(f"  ✓ timeout set to {result}ms")
    except (TypeError, ValueError) as e:
        print(f"  ✗ {type(e).__name__}: {e}")

print()

# Custom exception class - 
class TestConfigError(Exception):
    """ Raised when test configuration is invalid """
    pass

class TestDataError(Exception):
    """ Raised when test data is missing or malformed """
    pass

def load_test_user(users: list, role: str) -> dict:
    """ Find a user by role. Raise TestDataError if not found """
    for user in users:
        if user.get("role") == role:
            return user
    raise TestDataError(f"No user found with role '{role}' in test data")

users = [
    {"username": "tomsmith", "role": "admin"},
    {"username": "janesmith", "role": "viewer"}
]

try:
    user = load_test_user(users, "editor")
except TestDataError as e:
    print(f"TestDataError: {e}")


print("="*50)

# ==========================================================================================================

# Reading files and JSON — loading test data 

import json
from typing import Any, Dict, Optional

def load_test_data(filepath: str) -> Optional[Dict[str, Any]]:
    """ Load test data from JSON file .
    Returns the data dict, or None or any error """

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f" ✓ Loaded: {filepath}")
        return data
    
    except FileNotFoundError:
        print(f" ✗ File not found: {filepath}")
    except json.JSONDecodeError as e:
        print(f" ✗ Invalid JSON in {filepath}: {e}")
    except PermissionError:
        print(f" ✗ No permission to read: {filepath}")
    return None

# Local read file
data = load_test_data("test_data.json")
if data:
    print(f"Users: {len(data['users'])}")
    print(f"Base URL: {data['base_url']}")

print()

# Try a missing file - 
bad = load_test_data("missing.json")
print(f"Result: {bad}") # None

print()

# Writing JSON - save test results to file
def save_results(results: list, filepath: str) -> bool:
    """ Save test results to JSON. Returns True on success """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f" ✓ Results saved to {filepath}")
        return True
    except Exception as e:
        print(f" ✗ Failed to save: {e}")
        return False

save_results([{"id":"TC01", "status":"PASS"}], "results.json")