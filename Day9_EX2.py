# Example 2 — Resilient test runner with error capture

from typing import Callable, Dict, List
import traceback

def run_resilient_suite(tests: List[Dict]) -> List[Dict]:
    """ Run a list of test dicts. Never crashes - capture all errors """
    results = []

    for test in tests:
        name = test.get("name", "unnamed")
        action = test.get("action")
        result = {"name": name, "status": "UNKNOWN", "error": None}

        if not callable(action):
            result["status"] = "SKIP"
            result["error"] = "No action defined"
            results.append(result)
            continue

        try:
            action()
            result["status"] = "PASS"
            print(f" ✓ {name}")
        
        except AssertionError as e:
            result["status"] = "FAIL"
            result["error"] = f"Assertion: {e}"
            print(f" ✗ {name} - {e}")
        
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = f"{type(e).__name__}: {e}"
            print(f" ⚠ {name} - unexpected error: {e}")
        
        results.append(result)
    
    return results

# Define test actions as simple functions
def test_login():
    assert True, "Login should succeed"

def test_checkout():
    assert False, "Checkout button not found"

def test_api():
    data = {}
    _ = data["email"] # KeyError - unexpected crash

def test_profile():
    assert 200 == 200, "Status mismatch"

tests = [
    {"name": "test_login",    "action": test_login},
    {"name": "test_checkout", "action": test_checkout},
    {"name": "test_api",      "action": test_api},
    {"name": "test_profile",  "action": test_profile},
    {"name": "test_no_action"},   # no action key
]

print("Running suite: ")
results = run_resilient_suite(tests)

print(f"\nSummary: {sum(1 for r in results if r['status'] == 'PASS')} / {len(results)} passed")
for r in results:
    if r["error"]:
        print(f" {r['name']}: {r['error']}")