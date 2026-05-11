# Example 2 — Multi-browser test runner *args + **kwargs together

import random
from typing import List, Tuple
random.seed(42)

def run_tests(*test_ids: str, **options) -> List[Tuple[str, str, str]]:
     """Run any number of tests with any options.

    Args:
        *test_ids: any number of test ID strings
        **options: browser, retries, verbose (all optional)

    Returns:
        list of (test_id, browser, status) tuples
    """
     
     browser = options.get("browser", "chromium")
     retries = options.get("retries", 1)
     verbose = options.get("verbose", True)

     if not test_ids:
          print("No test IDs provided - nothing to run")
          return []
     
     results = []

     for tid in test_ids:
          attempt = 0
          status = "FAIL"

          while attempt < retries and status == "FAIL":
               attempt += 1
               status = "PASS" if random.random() > 0.3 else "FAIL"

          results.append((tid, browser, status))

          if verbose:
               icon = "✓" if status == "PASS" else "✗"
               print(f" {icon} [{browser}] {tid} - {status}")
        
     return results

# Call with just test IDs - uses all defaults
print("--- Default run ---")
r1 = run_tests("TC01", "TC02", "TC03")

# Call with options
print("\n--- Firefox with retries---")
r2 = run_tests("TC01", "TC02", "TC03", browser="firefox", retries=3)

# Unpack a list of IDs using *
print("\n--- Unpacked list---")
all_tests = ["TC01", "TC02", "TC03", "TC04"]
r3 = run_tests(*all_tests, browser="webkit", verbose=False)

# Summary
passed = sum(1 for _, _, s in r3 if s == "PASS")
print(f"Silent run: {passed}/P{len(r3)} passed")
          