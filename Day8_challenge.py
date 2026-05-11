# Day 8 challenge — write it all from scratch


""" Build a QA test reporter
Write these 4 functions from scratch — no looking back:

Function 1 — log_result(test_id, status, *details, **meta)
Accepts a test ID, a status (PASS/FAIL), any number of detail strings (*args), and any metadata as keyword args.
Prints a formatted log line. Example output:
[PASS] TC01 | Details: step1 passed, element found | browser=chromium env=staging

Function 2 — build_report(title, *results, **options)
Accepts a report title, any number of result dicts (each with "id", "status"), and options like show_passed=True, 
max_failures=10. Returns a formatted report string. Uses all() and any() for the summary.

Function 3 — assert_response(status, body, expected_status=200, required_fields=None)
Uses None as safe default for required_fields. Validates status code and checks all required 
fields exist in body dict. Returns (bool, list_of_errors) tuple. Type hint everything.

Function 4 — retry(func, *args, max_attempts=3, **kwargs)
Accepts any function, its args and kwargs, and a max_attempts count. Calls func(*args, **kwargs) 
up to max_attempts times. Returns the result on success or None after all failures. 
This is an advanced pattern — a function that wraps another function."""


 # =====================================================================================================================================

from typing import Any, Callable, Dict, List, Optional, Tuple
import random
random.seed(42)

# ----- Function 1: log_result -----------------------------------
def log_result(
        test_id: str,
        status: str,
        *details: str,
        **meta: Any
) -> None:
    """Log a test result with optional strings and metadata"""
    detail_str = ", ".join(details) if details else "no details"
    meta_str = " ".join(f"{k}={v}" for k, v in meta.items())
    line = f"[{status}] {test_id} | Details: {detail_str}"
    if meta_str:
        line += f" | {meta_str}"
    print(line)

# --- Function 2: build_report --------------------------------------
def build_report(
        title: str,
        *results: Dict[str, str],
        show_passed: bool = True,
        max_failure: int = 10
) -> str:
    """Build a formatted report string from any number of result dicts."""
    if not results:
        return f" Report '{title}': no result provided"
    
    total = len(results)
    passed = sum(1 for r in results if r.get("status" == "PASS"))
    failed = total - passed
    all_ok = all(r.get("status") == "PASS" for r in results)
    any_fail = any(r.get("status") == "FAIL" for r in results)
    overall = "PASS" if all_ok else "FAIL"

    lines = [
         f"{'='*45}",
        f"  {title}",
        f"{'='*45}",
        f"  Total   : {total}",
        f"  Passed  : {passed}",
        f"  Failed  : {failed}",
        f"  All pass: {all_ok}  |  Any fail: {any_fail}",
        f"{'─'*45}",
        f"  OVERALL : {overall}",
        f"{'='*45}",
    ]

    failures = [r for r in results if r.get("status") == "FAIL"]
    if failures:
        lines.append(f"\n Failures (showing max {max_failure}): ")
        for r in failures[:max_failure]:
            lines.append(f"  ✗ {r.get('id', '?')} - {r.get('name', 'unknown')}")
    
    if show_passed:
        passed_list = [r for r in results if r.get("status") == "PASS"]
        if passed_list:
            lines.append(f"\n Passed: ")
            for r in passed_list:
                lines.append(f"  ✓ {r.get('id', '?')} - {r.get('name', 'unknown')}")

    return "\n".join(lines)

# --- Function 3: assert_response ----------------------------------------------------------
def assert_response(
        status: int,
        body: Dict[str, Any],
        expected_status: int = 200,
        required_fields: Optional[List[str]] = None
) -> Tuple[bool, List[str]]:
    """Validate an API response status and body fields.

    Returns:
        (passed: bool, errors: list of strings)
    """
    required_fields = required_fields or []
    errors = []

    # Status check
    if status != expected_status:
        errors.append(f" Status {status} != expected {expected_status}")
    
    # Body filed checks
    if not body:
        errors.append("Response body is empty")
    else:
        for filed in required_fields:
            if filed not in body:
                errors.append(f"Missing required filed: {filed}")
            elif body[filed] is None:
                errors.append(f"Filed '{filed}' is None")
    
    passed = len(errors) == 0
    return passed, errors

# --- Function 4: retry --------------------------------------------------------
def retry(
        func: Callable,
        *args: Any,
        max_attempts: int = 3,
        **kwargs: Any
) -> Optional[Any]:
    """Call func(*args, **kwargs) up to max_attempts times.

    Returns the result on success, None if all attempts fail.
    func is expected to return a truthy value on success.
    """

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            result = func(*args, **kwargs)
            if result:
                print(f"  ✓ Succeeded on attempt {attempt}/{max_attempts}")
                return result
            print(f"  ✗ Attempt {attempt}/{max_attempts} - returned falsy")
        except Exception as e:
            print(f"   ✗ Attempt {attempt}/{max_attempts} - error: {e}")
    print(f" Gave up after {max_attempts} attempts")
    return None


# --- Demo -------------------------------------------------------------------------
if __name__ == "__main__":

    # Function 1 - log_result
    print("--- log_result ────────────────────────")
    log_result("TC01", "PASS")
    log_result("TC02", "PASS", "login ok", "element found", browser="chromium", env="staging")
    log_result("TC03", "FAIL", "button not found", browser="firefox")

    # Function 2 - build_report
    print("\n── build_report ────────────────────────")
    test_results = [
        {"id":"TC01", "name":"valid_login",   "status":"PASS"},
        {"id":"TC02", "name":"invalid_login", "status":"PASS"},
        {"id":"TC03", "name":"checkout",      "status":"FAIL"},
        {"id":"TC04", "name":"profile",       "status":"FAIL"},
    ]
    print(build_report("Smoke Test Suite", *test_results, show_passed=False))

    # Function 3 - assert_response
    print("\n── assert_response ────────────────────────")
    ok, errs = assert_response(200, {"id":1, "email":"a@b.com"}, required_fields=["id", "email"])
    print(f" Valid response: {ok}")

    ok, errs = assert_response(404, {}, expected_status=200, required_fields=["id", "email"])
    print("Bad response: {ok} - errors: {errs}")

    # Function 4 - retry
    print("\n── retry ────────────────────────────────────")

    def flaky_check(url: str) -> str:
        """Simulates a flaky operation - succeeds ~60% of the time. """
        return "OK" if random.random() > 0.4 else ""
    
    result = retry(flaky_check, "https://staging.myapp.com", max_attempts = 5)
    print(f"Retry result: {result}")