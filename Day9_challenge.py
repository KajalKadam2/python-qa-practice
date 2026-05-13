""" Build a resilient test data manager
Write these 4 functions — no looking back:

Function 1 — safe_get(data, *keys, default=None)
Safely navigate nested dicts using any number of keys. safe_get(resp, "data", "email") 
returns resp["data"]["email"] without crashing if any key is missing. Returns default on any failure. 
Uses *args and try/except KeyError.

Function 2 — load_users(filepath)
Load a JSON file, extract the "users" list, validate each user has username, password, and role. 
Raise a custom TestDataError with a clear message if anything is wrong. 
Return the validated list on success.

Function 3 — safe_assert(condition, message, on_fail="log")
A soft assertion wrapper. If on_fail="raise" — raise AssertionError. 
If on_fail="log" — print the failure but do not crash. Returns True if passed, False if failed. 
Use try/except AssertionError.

Function 4 — run_with_teardown(test_fn, setup_fn=None, teardown_fn=None)
Runs setup_fn() if provided, then test_fn(), then teardown_fn() in a finally block. 
Catches all exceptions from test_fn, prints them, and returns (passed: bool, error: str | None). 
Teardown always runs."""


# ==========================================================================================================
import json
from typing import Any, Callable, Dict, List, Tuple, Optional

# custom exception
class TestDataError(Exception):
    """ Raise when test data is missing or malformed """
    pass

# Function 1: safe_get -----------------------------------------------------
def safe_get(data: Dict, *keys: str, default: Any = None) -> Any:
    """Navigate nested dicts safely using any number of keys.

    safe_get(resp, "data", "email") → resp["data"]["email"]
    Returns default if any key is missing or data is not a dict.
    """
    current = data
    for key in keys:
        try:
            current = current[key]
        except (KeyError, TypeError):
            return default
    return current

# Function 2: load_user --------------------------------------------------------------
def load_users(filepath: str) -> List[Dict]:
     """Load and validate users from a JSON file.

    Raises TestDataError with a clear message on any problem.
    Returns validated list of user dicts on success.
    """
     # Load teh file
     try:
         with open(filepath, "r", encoding="utf-8") as f:
             data = json.load(f)
     except FileNotFoundError:
         raise TestDataError(f"File not found: '{filepath}'")
     except json.JSONDecodeError as e:
         raise TestDataError(f"Invalid JSON in '{filepath}': {e}")
     
     # Check users key exists
     if "users" not in data:
         raise TestDataError(f" '{filepath}' has no 'users' key")
     
     users = data["users"]

     if not isinstance(users, list) or len(users) == 0:
         raise TestDataError(f" 'users' must be a non-empty list ")
     
     # Validate each user
     required = ["username", "password", "role"]
     for i, user in enumerate(users):
         missing = [f for f in required if f not in user]
         if missing:
             raise TestDataError(f"User at index {i} missing fields: {missing}")
         
     return users
     

# Function 3 - safe_assert -------------------------------------------------------
def safe_assert(
        condition: bool,
        message: str,
        on_fail: str = "log"
) -> bool:
    """Soft assertion wrapper.

    on_fail='raise' → raises AssertionError on failure
    on_fail='log'   → prints failure, does not crash
    Returns True if passed, False if failed.
    """

    try:
        assert condition, message
        print(f" ✓ PASS: {message}")
        return True
    except AssertionError:
        if on_fail == "raise":
            raise
        print(f" ✗ FAIL: {message}")
        return False


# Function 4: run_with_teardown ---------------------------------------
def run_with_teardown(
        test_fn: Callable,
        setup_fn: Optional[Callable] = None,
        teardown_fn: Optional[Callable] = None
) -> Tuple[bool, Optional[str]]:
    
    """Run test_fn with optional setup and guaranteed teardown.

    Returns (passed: bool, error: str | None).
    teardown_fn always runs — even if test_fn crashes.
    """

    # Setup
    if setup_fn is not None:
        try:
            setup_fn()
        except Exception as e:
            print(f" ✗ setup failed: {e}")
            return False, f"Setup error: {e}"
    
    passed = False
    error = None

    try:
        test_fn()
        passed = True
        print(f" ✓ Test passed")

    except AssertionError as e:
        error = f"AssertionError: {e}"
        print(f" ✗ Test failed: {e}")

    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        print(f" ✗ Unexpected error: {e}")
    
    finally:
        if teardown_fn is not None:
            try:
                teardown_fn()
            except Exception as e:
                print(f" ⚠ Teardown error: {e}")

    return passed, error

# Demo -----------------------------------------------------------
if __name__ == "__main__":

    # Function 1 - safe_get
    print("── safe_get ─────────────────────────────")
    resp = {"data": {"id":2, "email": "janet@reqres.in"}}

    print(safe_get(resp, "data", "email"))
    print(safe_get(resp, "data", "phone"))
    print(safe_get(resp, "data", "phone", default="N/A"))
    print(safe_get(resp, "missing", "deep", "key"))
    print(safe_get(None, "data"))

    # Function 2 - load_users
    print("\n── load_users ───────────────────────────")
    for path in ["test_data.json", "missing.json"]:
        try:
            users = load_users(path)
            print(f" ✓ Loaded {len(users)} users from {path}")
        except TestDataError as e:
            print(f" ✗ TestDataError: {e}")
    
    # Function 3 - safe_assert
    print("\n── safe_assert ──────────────────────────")
    safe_assert(200 == 200, "Status is 200")
    safe_assert(200 == 200, "Status is 200", on_fail="log")
    try:
        safe_assert(False, "This must be true", on_fail="raise")
    except AssertionError as e:
        print(f" Caught raise: {e}")
    
    # Function 4 - run_with_teardown
    print("\n── run_with_teardown ────────────────────")

    def my_setup(): print(" → Setup: creating test user")
    def my_teardown(): print(" → Teardown: deleting test user")
    def passing_test(): assert True
    def failing_test(): assert False, "Button not found"
    def crashing_test(): raise KeyError("email")

    for label, fn in [("passing", passing_test), ("failing", failing_test), ("crashing", crashing_test)]:
        print(f"\n [{label} test]")
        ok, err = run_with_teardown(fn, my_setup, my_teardown)
        print(f" Result: passed={ok} error={err}")