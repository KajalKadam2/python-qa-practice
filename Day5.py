# Conditions


status = 200
response_time = 843
email = "test@example.com"
element = None
retry_count = 2

print(status == 200)
print(status != 404)
print(response_time > 2000)
print(response_time < 2000)
print("@" in email)
print("error" not in email)
print(element is None)
print(element is not None)
print(retry_count <= 3)

print('='*38)

# ----------- and / or / not — combining conditions --------------------------------------------

#AND - both conditions must be True

url = "https://staging.myapp.com"
status = 200

is_valid = url.startswith("https") and status == 200
print(f"URL is secure AND status OK: {is_valid}")

#OR - at least one must be True
browser = "firefox"
is_supported = browser == "chromium" or browser == "firefox" or browser == "webkit"
print(f"Browser supported: {is_supported}")

# OR - use 'in' with a list instead
is_supported1 = browser in ["chromium", "firefox", "webkit"]
print(f"Browser supported (cleaner): {is_supported1}")

# NOT - flips the result
is_logged_in = False
print(f"Needs login: {not is_logged_in}")

# Combining all three - real validation logic
email = "user@test.com"
password_len = 10
role = "admin"

can_access_admin = (
    "@" in email and password_len >= 8 and role == "admin" and not is_logged_in
)
print(f"Can access admin: {can_access_admin}")


print('='*38)

# -----------------------------------------------------------------------------------------------

# Beginners
errors = []
if len(errors) > 0:
    print("Has error")
else:
    print("No errors")

# Professional way
if errors:
    print("Has errors")
else:
    print("No errors")

# All the patterns you'll use

test_name = "test_login"
result = None
failures = []
passed = ["test_a", "test_b"]

if test_name:
    print(f"Running: {test_name}")

if result is None:
    print("No result yet!")

if not failures:
    print("All test passed!")

if passed:
    print(f"{len(passed)} tests passed")


print('='*38)

# ---------- if / elif / else — branching logic -------------------------------------------------

# Pattern 1 - Status code classifier --------

# Classify any HTTP status code
def classify_status(code):
    if 200 <= code < 300:
        return "SUCCESS"
    elif 300 <= code < 400:
        return "REDIRECT"
    elif 400 <= code < 500:
        return "CLIENT ERROR"
    elif 500 <= code < 600:
        return "SERVER ERROR"
    else:
        return "UNKNOWN"
    
for code in [200, 201, 301, 400, 404, 500, 503]:
    print(f" {code} → {classify_status(code)}")

print('='*38)

# Pattern 2 — guard clauses (exit early) -----------

# WITHOUT guard clauses — deeply nested, hard to read

def validate_user_bad(user):
    if user is not None:
        if user.get("username"):
            if user.get("email") and "@" in user["email"]:
                return "VALID"

# WITH guard clauses — exit early, flat and readable
def validate_user(user):
    if user is None:
        return "FAIL: user is None"
    if not user.get("username"):
        return "FAIL: missing username"
    if not user.get("email") or "@" not in user["email"]:
        return "FAIL: invalid email"
    return "VALID"            # ------ reached only if all checks pass

print(validate_user(None))
print(validate_user({"email": "test@x.com"}))
print(validate_user({"username": "tom", "email" : "notvalid"}))
print(validate_user({"username": "tom", "email" : "tom@test.com"}))

print('='*38)


# ----------- Ternary expression — one-line if/else ----------------------------------------------------------

#Full if/else - 4 lines

'''
if condition:
    result = "value_if_true"
else:
    result = "value_if_false"

# Ternary — 1 line, same result

result = "value_if_true" if condition else "value_if_false" ----------  Read: "give me X if condition, otherwise Y"    
'''

#Test result labelling
status = 200
label = "PASS" if status == 200 else "FAIL"
print(f"Status {status}: {label}")

#Environment display
env = "staging"
is_prod = env == "prod"
safety = "⚠ PRODUCTION" if is_prod else "safe"
print(f"Environment: {env} ({safety})")

#Response time severity
response_ms = 1850
speed = "SLOW" if response_ms > 2000 else "ACCEPTABLE" if response_ms > 1000 else "FAST"
print(f"Response {response_ms}ms: {speed}")

#Active/Inactive display
users = [
    {"name": "George", "active": True},
    {"name": "Emma", "active": False},
    {"name": "Janet", "active": True}
]
for u in users:
    icon = "✓" if u["active"] else "✗"
    print(f" {icon} {u['name']}")