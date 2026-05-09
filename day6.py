# LOOPS 

# ALL range() patterns

# 1. range(stop) - 0 to stop-1
for i in range(3):
    print(f"Retry attempt {i+1}")  # 1, 2, 3
print()

# 2. range(start, stop) - start to stop-1
for i in range(1,6):
    print(f"Test case {i}") # 1,2,3,4,5
print()

# 3. range(start, stop, step)
for port in range(8080, 8090, 2):
    print(f"Checking port: {port}") #8080, 8082,...
print()

# 4. reverse range - count down
for i in range(3, 0, -1):
    print(f" Countdown: {i}") #3,2,1


print('='*40)

# ---- break and continue --------------------------------------------------------------------------------------------------
# Find first failing test — stop searching after finding it
# break — stop as soon as you find what you need

results = [
    {"name": "test_login",     "status": "PASS"},
    {"name": "test_register",  "status": "PASS"},
    {"name": "test_checkout",  "status": "FAIL"},
    {"name": "test_payment",   "status": "FAIL"},
    {"name": "test_logout",    "status": "PASS"},
]
first_failure = None
for result in results:
    if result["status"] == "FAIL":
        first_failure = result
        break 
if first_failure:
    print(f"First failure: {first_failure['name']}")
else:
    print("All tests passed!")

# Find a user by ID — stop once found
users = [{"id":1,"name":"George"},{"id":2,"name":"Janet"},{"id":3,"name":"Emma"}]
target = None
for u in users:
    if u["id"] == 2:
        target = u
        break
print(f"Found: {target['name'] if target else 'not found'}")

# ------ continue — skip invalid items, process valid ones ------
# Skip empty or invalid emails — process only valid ones

emails = ["george@reqres.in", "", "notanemail", "janet@reqres.in", None]
print("Processing valid emails: ")
for email in emails:
    if not email:
        print(f" Skipping empty/None value")
        continue 
    if "@" not in email:
        print(f" Skipping invalid: {email}")
        continue
    print(f" ✓ Processing: {email}")


print('='*40)

# ----------- for / else ------------------------------------------------------------------------------------------------

# 1. without for/else - needs a flag variable
users = [{"id":1,"name":"George"},{"id":2,"name":"Janet"}]
found = False
for u in users:
    if u["id"] == 99:
        print(f"Found: {u['name']}")
        found = True
        break
if not found:
    print("User 99 not found")
print()

# 2. WITH for/else
for u in users:
    if u["id"] == 99:
        print(f"Found: {u['name']}")
        break
else:
    print("User 99 not found")
print()

# Example - check a required element exists in a list
required_fields = ["id", "email", "first_name"]
api_response    = {"id": 1, "email": "a@b.com"}   # missing first_name!

for field in required_fields:
    if field not in api_response:
        print(f"FAIL: missing required field '{field}'")
        break
else:
    print("PASS: all required fields present")

print('='*40)

# ------ while loops --------------------------------------------------------------------------------------------------------

#Retry a flaky action - stop on success or max attempts
import random
random.seed(42) #makes random predictable for practice

max_retries = 5
attempt = 0
success = False

while attempt < max_retries and not success:
    attempt += 1
    print(f"Attempt {attempt}/{max_retries}...")

    # Simulate: succeeds ~50% of the time
    success = random.random() > 0.5

    if success:
        print(f" ✓ Succeeded on attempt {attempt}")
    else:
        print(f" ✗ Failed - retrying...")

if not success:
    print(f"FAIL: action failed after {max_retries} attempts")

# Pattern 2 - POLL until a condition is met - with timeout safety net
import time
max_wait_seconds = 5
poll_interval = 1
elapsed = 0
is_ready = False

print(f"Waiting for element to appear...")

while elapsed < max_wait_seconds and not is_ready:
    time.sleep(poll_interval) #wait before checking
    elapsed += poll_interval

    # Simulate: element appears after 3 sec
    is_ready = elapsed >= 3
    print(f" {elapsed}s - element ready: {is_ready}")

if is_ready:
    print("✓ Element found — continuing test")
else:
    print(f"✗ FAIL: element not found after {max_wait_seconds}s")

print('='*40)


# -------- zip — pairing two lists together --------------------------------------------------------------------

# Inputs and expected outputs as paired lists
inputs   = ["tomsmith", "wronguser", "",       "tomsmith"]
passwords= ["SuperSecretPassword!", "wrongpass", "pass", "wrongpass"]
expected = ["secure area", "invalid", "invalid", "invalid"]

print("Login test cases: ")
for i, (user, pw, exp) in enumerate(zip(inputs, passwords, expected), 1):
    print(f" Test {i}: user={user!r:12} expects='{exp}'")
print()

# Zip two lists to compare expected vs actual
expected_statuses = [200, 201, 404, 200]
actual_statuses   = [200, 201, 500, 200]   # 3rd is wrong!
endpoints         = ["/users", "/users", "/users/99", "/users/1"]

print("API status checks: ")
for endpoint, expected, actual in zip(endpoints, expected_statuses, actual_statuses):
    icon = "✓" if actual == expected else "✗"
    detail = "" if actual == expected else f" (expected {expected}, got {actual})"
    print(f" {icon} {endpoint}{detail}")
print()

# zip stops at the shortest list
a = [1,2,3,4,5]
b = ["a", "b", "c"]  # shorter list
print(list(zip(a,b)))

print('='*40)


# ------ Nested loops — every combination  -------------------------------------------------------
# cross-browser × cross-page matrix

browsers  = ["chromium", "firefox", "webkit"]
pages     = ["/login", "/dashboard", "/checkout"]
base_url  = "https://staging.myapp.com"

total_runs = 0
results = []

for browser in browsers:
    for page in pages:
        total_runs += 1
        url = f"{base_url}{page}"
        print(f" [{browser:10}] Testing {url}")
        results.append("PASS")

print(f"\nTotal: {total_runs} runs ({len(browsers)} browsers x {len(pages)} pages)")
print(f"All passed: {all(r == 'PASS' for r in results)}")

# all() and any() ----
statuses = [200, 200, 201, 200]
print(all(s < 300 for s in statuses)) #True - all are success

results = ["PASS", "PASS", "FAIL", "PASS"]
print(all(r == "PASS" for r in results)) # False - one FAIL

print(any(r == "FAIL" for r in results)) # True - at least one FAIL
print(any(s >= 500 for s in statuses)) # False - no server errors