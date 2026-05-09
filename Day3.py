
#Modifying lists — add, remove, change

results = ["PASS", "PASS", "FAIL"]
print(f"Start: {results}")

# Add more results as tests finish
results.append("PASS")
results.append("FAIL")
print(f"Added: {results}")

# Count failures
fail_count = results.count("FAIL")
pass_count = results.count("PASS")
print(f"Passed: {pass_count} | Failed: {fail_count}")

# Fix a wrong result — replace by index
results[2] = "PASS"
print(f"Fixed: {results}")


# Remove a specific value
results.remove("FAIL") 
print(f"Removed: {results}")

# Pop the last result off
last = results.pop()
print(f"Popped: {last} | remaining: {results}")

print('=' *60) # blank line separator



#------------ Slicing — grabbing a portion of a list ----------------------------------------------

tests = ["login", "register", "checkout", "payment", "logout"]
#          0          1           2           3          4

print(tests[0:2]) # ['login', 'register']
print(tests[1:4])  # ['register', 'checkout', 'payment']

print(tests[:3]) # first 3:  ['login', 'register', 'checkout']
print(tests[3:]) # from 3 on: ['payment', 'logout']
print(tests[:]) # entire list (a copy)

print(tests[-2:])  # last 2: ['payment', 'logout']
print(tests[-3:]) # last 3: ['checkout', 'payment', 'logout']

all_user_ids = [1,2,3,4,5,6,7,8,9,10]
sample = all_user_ids[:5]
print(f"Testing sample: {sample}")


print('=' *60) # blank line separator

#----------- Looping over a list ---------------------------------------------------------

# Pattern 1: basic — item only
browsers = ["chrome", "firefox", "webkit"]
for browser in browsers:
    print(f"Running tests on: {browser}")

print() # blank line separator

# Pattern 2: enumerate — index AND item together
for i, browser in enumerate(browsers):
    print(f"Browser {i+1} of {len(browsers)}: {browser}")

print() # blank line separator

# Pattern 3: with a condition inside the loop
invalid_emails = ["noatsign", "@nodomain", "", "a@b", "ok@test.com"]
for email in invalid_emails:
    if "@" in email and "." in email:
        print(f" PASS: {email} looks valid")
    else:
        print(f" FAIL: {email!r} is invalid")

print() # blank line separator

# Pattern 4: building a new list inside a loop
urls   = ["https://app.com", "http://old.com", "https://api.com"]
secure = []
for url in urls:
    if url.startswith("https"):
        secure.append(url)
print(f"Secure URLs: {secure}")

print('=' *60) # blank line separator
print('=' *60) # blank line separator

# ------------ List comprehension — compact list building ----------------------------

#Full loop

# results = []
# for r in ["PASS","FAIL", "PASS"]:
#    results.append(r.lower())

#Same thing - 1 line (list comprehension)
results = [r.lower() for r in ["PASS","FAIL", "PASS"]] # Read as: "r.lower(), for each r in this list"

print('=' *60) # blank line separator

# ---------------- Example ------------------

# 1. Build all test URLs from a list
base = "https://staging.myapp.com"
paths = ["/login", "/dashboard", "/profile", "/logout"]
urls = [f"{base}{path}" for path in paths]
print(urls)

#2. Filter - keep only FAIL results
all_results = ["PASS", "FAIL", "PASS", "FAIL", "PASS"]
failures = [r for r in all_results if r == "FAIL"]
print(f"Failures: {failures}")
print(f"Count: {len(failures)}")

# 3. Transform - uppercase all browser names
browsers = ["chromium", "firefox", "webkit"]
upper = [b.upper() for b in browsers]
print(upper)

# 4. Filter + Transform together
response_times = [120, 3500, 89, 4100, 250]
slow = [t for t in response_times if t > 2000]
print(f"Slow responses (>2s): {slow}")


print('=' *60) # blank line separator
print('=' *60) # blank line separator

#------------------ Example 1 — Invalid email test data runner ------------------------------

# All the invalid emails your login form should reject
invalid_emails = [
    "noatsign",
    "@nodomain.com",
    "",
    "spaces in@email.com",
    "double@@at.com",
    "toolong" * 50 + "@x.com",
]

print(f"Testing {len(invalid_emails)} invalid email inputs\n")

for i, email in enumerate(invalid_emails, start=1):
    display = repr(email[:30])
    print(f"Test {i}: filling email -> {display}")
    print(f" expecting error message to appear")

print(f"\nAll {len(invalid_emails)} invalid inputs tested.")

print('=' *60) # blank line separator

# ------------------ Example 2 — Test result tracker -------------------------------------------

# Simulated test suite — each tuple is (test_name, result)
test_suite = [
    ("test_login_valid",       "PASS"),
    ("test_login_invalid",     "PASS"),
    ("test_login_empty",       "FAIL"),
    ("test_dashboard_loads",   "PASS"),
    ("test_profile_update",    "FAIL"),
    ("test_logout",            "PASS"),
]
passed = []
failed = []

for test_name, result in test_suite:
    if result == "PASS":
        passed.append(test_name)
    else:
        failed.append(test_name)

# Summary
total = len(test_suite)
n_passed = len(passed)
n_failed = len(failed)
rate = round(n_passed / total * 100, 1)

print(f"{'='*30}")
print(f" Results: {n_passed}/{total} passed ({rate}%)")
print(f"{'='*30}")

if failed:
    print(f"\nFailed tests ({n_failed}):")
    for name in failed:
        print(f" x {name}")

print(f"\nPassed tests ({n_passed}):")
for name in passed:
    print(f" v {name}")



print('=' *60) # blank line separator

# --------------- Example 3 — API response list checker -----------------------------
# Simulating: data = response.json()["data"]  from reqres.in
api_users = [
    {"id": 1, "email": "george.bluth@reqres.in",    "active": True},
    {"id": 2, "email": "janet.weaver@reqres.in",   "active": True},
    {"id": 3, "email": "emma.wong",               "active": False},  # bad email
    {"id": 4, "email": "eve.holt@reqres.in",      "active": True},
    {"id": 5, "email": "",                       "active": True},  # empty!
]
print(f"Checking {len(api_users)} users from API response\n")

issues = []
valid_emails = []

for user in api_users:
    uid = user["id"]
    email = user["email"]
    valid = "@" in email and "." in email and len(email) > 0

    if valid:
        valid_emails.append(email)
        print(f" v Users {uid}:   {email}")
    else:
        issues.append(f"User {uid} has invalid email:  {repr(email)}")
        print(f" x Users {uid}:  {repr(email)} - INVALID")

print(f"\n--- Summary ---")
print(f"Valid:  {len(valid_emails)}/{len(api_users)}")
print(f"Issues: {len(issues)}")

for issue in issues:
    print(f"   -> {issue}")

# Final assertion — what a real test would do
assert len(issues) == 0, f"{len(issues)} users failed email validation"