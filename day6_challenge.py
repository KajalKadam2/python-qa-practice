# Build a complete test suite simulator


''' Part 1 — Run the suite
Nested loop: browsers × test_cases. For each combination, simulate running with random.random() > 0.3 as the pass condition. 
Store results as a list of dicts: {"browser","test_id","test_name","status"}.

Part 2 — Retry failures
Loop over your results. For each FAIL, retry up to the test's retries count using a while loop. Use random.random() > 0.5 as retry success. 
Update the status if retry succeeds. Print each retry attempt.

Part 3 — Skip P3 tests
Loop over test_cases. Use continue to skip any test with priority "P3". Print "Skipped: {name}" for those, and "Would run: {name}" for others.

Part 4 — Find first P1 failure
Use for/else to find the first P1 test that failed. Print it or print "All P1 tests passed" using the else clause.

Part 5 — Summary
Use all() and any(). Print: total runs, passed, failed, whether all P1 tests passed, whether any test failed across both browsers.'''

# --------------------------------------------------------------------------------------------------------------------------------------------------------

import random
random.seed(99)

test_cases = [
  {"id":"TC01","name":"valid_login","priority":"P1","retries":3},
  {"id":"TC02","name":"invalid_login","priority":"P1","retries":2},
  {"id":"TC03","name":"empty_fields","priority":"P2","retries":1},
  {"id":"TC04","name":"checkout_flow","priority":"P1","retries":3},
  {"id":"TC05","name":"profile_update","priority":"P2","retries":2},
  {"id":"TC06","name":"logout","priority":"P3","retries":1},
]
browsers = ["chromium", "firefox"]

# ---- Part 1 : Run the suite
print("Part 1 - Running test suite\n")
run_results = []

for browser in browsers:
    print(f" Browser: {browser.upper()}")
    for tc in test_cases:
        status = "PASS" if random.random() > 0.3 else "FAIL"
        run_results.append({
            "browser":  browser,
            "test_id":  tc["id"],
            "test_name":tc["name"],
            "priority": tc["priority"],
            "retries":  tc["retries"],
            "status":   status
        })
        icon = "✓" if status == "PASS" else "✗"
        print(f" {icon} [{tc['id']}] {tc['name']:18} - {status}")

# ---- Part 2: Retry failures ---------
print("\nPart 2 - Retrying failures\n")
for result in run_results:
    if result["status"] != "FAIL":
        continue       #skip passing tests
    
    attempt = 0
    max_r = result["retries"]
    print(f" Retrying [{result['test_id']}] {result['test_name']} on {result['browser']}")

    while attempt < max_r and result["status"] == "FAIL":
        attempt += 1
        retry_pass = random.random() > 0.5
        if retry_pass:
            result["status"] = "PASS"
            print(f" ✓ Retry {attempt}/{max_r} - RECOVERED")
        else:
            print(f" ✗ Retry {attempt}/{max_r} - still failing")

    if result["status"] == "FAIL":
        print(f" → Gave up after {max_r} retries")

# ---- Part 3: Skip P3 tests
print("\nPart 3 - Priority filter\n")
for tc in test_cases:
    if tc["priority"] == "P3":
        print(f" Skipped : {tc['name']} ({tc['priority']})")
        continue
    print(f" Would run: {tc['name']} ({tc['priority']})")

# --- Part 4: Find first P1 failure -----------
print("\nPart 4 - First P1 failure\n")
p1_results = [r for r in run_results if r["priority"] == "P1"]

for result in p1_results:
    if result["status"] == "FAIL":
        print(f" First P1 failure: [{result['test_id']}] {result['test_name']} on {result['browser']}")
        break
    else:
        print(" All P1 tests passed !")

# --- Part 5: Summary -------
print("\nPart 5 - Final summary\n")
total_runs = len(run_results)
total_passed = sum(1 for r in run_results if r["status"] == "PASS")
total_failed = total_runs - total_passed

all_p1_passed = all(
    r["status"] == "PASS"
    for r in run_results
    if r["priority"] == "P1"
)
any_failed = any(r["status"] == "FAIL" for r in run_results)

print(f"{'='*40}")
print(f" SUITE RESULTS (after retries)")
print(f"{'='*40}")
print(f" Total runs    : {total_runs}")
print(f" Passed        : {total_passed}")
print(f" Failed        : {total_failed}")
print(f" All P1 passed : {all_p1_passed}")
print(f" Any failures  : {any_failed}")
print(f"{'='*40}")