# Example 3 — Assertion helper library type hints + defaults + returns

from typing import Any, Optional

def assert_equals(
        actual: Any,
        expected: Any,
        message: str = ""
) -> None:
    """Assert actual == expected with a clear failure message."""
    label = f"-{message}" if message else ""
    assert actual == expected, (
        f"AssertionError{label}\n"
        f" Expected : {expected}\n"
        f" Actual   : {actual!r}"
    )

def assert_contains(
        text: str,
        keyword: str,
        case_sensitive: bool = False,
        message: str = ""
) -> None:
    """Assert keyword is found in text."""
    haystack = text if case_sensitive else text.lower()
    needle = keyword if case_sensitive else keyword.lower()
    label = f" - {message}" if message else ""
    assert needle in haystack, (
        f"AssertionError{label}\n"
        f" '{keyword}' not found in '{text}'"
    )

def assert_status(
        actual: int,
        expected: int = 200,
        message: Optional[str] = None
) -> None:
    """Assert HTTP status code with default of 200."""
    msg = message or f"Expected status {expected}"
    assert actual == expected, f"{msg} - got {actual}"

# Use the helpers
print("Running assertions...\n")

# These should all pass
assert_equals(200, 200, "API status")
print(" ✓ assert_equals passed")

assert_contains("You logged into a secure area!", "secure area")
print(" ✓ assert_contains passed")

assert_status(201, 201)
print(" ✓ assert_status passed")

# This should fail - catch it
try:
    assert_equals(404, 200, "login redirect")
except AssertionError as e:
    print(f"\n ✗ Caught failure: \n {e}")