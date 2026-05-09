# -------- Build a test session auditor----------------------------------

''' Part 1 — Basic counts
Count passed, failed, pass rate %. Use .count() and ternary for overall status.

Part 2 — Response time analysis
From response_times_ms: find fastest, slowest, average (use sum() and len()). Count how many are over 2000ms (slow). 
Use conditions to classify the overall performance: "FAST" if average under 800, "ACCEPTABLE" if under 1500, else "SLOW".

Part 3 — Error audit
Loop over errors. For each error: check if it contains "Timeout" — label as "TIMEOUT". 
Check if it contains "500" — label as "SERVER ERROR". Otherwise label as "TEST FAILURE". Print each with its label.

Part 4 — Environment safety check
Check: URL starts with "https", env is not "prod", browser is in supported list ["chromium","firefox","webkit"]. 
Use guard clauses — return a warning message for each failure. Print all warnings or "Environment OK" if none.

Part 5 — Full audit report
Print a formatted report using everything computed above. Overall status: PASS only if pass_rate >= 80 AND no slow responses AND env is safe.'''

# ================================================================================================================================================

session = {
  "env": "staging",
  "browser": "chromium",
  "base_url": "https://staging.myapp.com",
  "total_tests": 12,
  "response_times_ms": [320, 840, 1200, 450, 3500, 290, 780, 4100, 520, 670, 390, 1850],
  "results": ["PASS","PASS","FAIL","PASS","FAIL","PASS","PASS","FAIL","PASS","PASS","PASS","PASS"],
  "errors": ["Timeout on checkout", "Button not found", "API 500 on payment"]
}

# --- Part 1: basic counts ---------------------------------------------------------
results = session["results"]
passed = results.count("PASS")
failed = results.count("FAIL")
total = len(results)
pass_rate = round(passed / total * 100, 1)
suite_status = "PASS" if pass_rate >= 80 else "FAIL"

print("Part 1 - Test Counts")
print(f" Passed    : {passed}/{total}")
print(f" Failed    : {failed}/{total}")
print(f" Pass rate : {pass_rate}%")
print(f" Status    : {suite_status}")

# ---- Part 2: Response time analysis ----------------------
times     = session["response_times_ms"]
fastest    = min(times)
slowest    = max(times)
average    = round(sum(times) / len(times), 1)
slow_count = len([t for t in times if t > 2000])

if average < 8000:
    perf_label = "FAST"
elif average < 1500:
    perf_label = "ACCEPTABLE"
else:
    perf_label = "SLOW"

print("\nPart 2 - Response times")
print(f" Fastest : {fastest}ms")
print(f" Slowest : {slowest}ms")
print(f" Average : {average}ms")
print(f" Over 2s : {slow_count} tests")
print(f" Perf    : {perf_label}")

# --- Part 3: error audit -----------------------------------------
print("\nPart 3 - Error audit")
for error in session["errors"]:
    error_lower = error.lower()
    if "timeout" in error_lower:
        label = "TIMEOUT"
    elif "500" in error_lower:
        label = "SERVER ERROR"
    else:
        label = "TEST FAILURE"
    print(f" [{label}] {error}")

# --- Part 4: Environment safety check ----------------------------------------------
print("\nPart 4 - Environment check")
supported_browsers = ["chromium", "firefox", "webkit"]
warnings = []

if not session["base_url"].startswith("https"):
    warnings.append(f"URL not secure: {session['base_url']}")
if session["env"] == "prod":
    warnings.append("Running against PRODUCTION - dangerous!")
if session["browser"] not in supported_browsers:
    warnings.append(f"Unsupported browser: {session['browser']}")

if warnings:
    for w in warnings:
        print(f" ⚠ {w}")
else:
    print(" Environment OK")

env_safe = not warnings

#--- Part 5: Full audit report ----------------------------------------------
overall = "PASS" if (pass_rate >= 80 and slow_count == 0 and env_safe) else "FAIL"

print(f"\n{'='*40}")
print(f" SESSION AUDIT REPORT")
print(f" Environment : {session['env']} ({session['browser']})")
print(f" Tests       : {passed}/{total} passed ({pass_rate}%)")
print(f" Performance : avg {average}ms - {perf_label}")
print(f" Slow Tests  : {slow_count}")
print(f" Errors      : {len(session['errors'])}")
print(f" Env safe    : {env_safe}")
print(f"\n{'='*40}")
print(f" OVERALL     : {overall}")
print(f"\n{'='*40}")