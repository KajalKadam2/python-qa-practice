# Example 3 — Form field validator 

def validate_form_data(username, password, email, role):
    """Validate test form before filling into browser"""

    errors = []

    # Username checks
    if not username or not username.strip():
        errors.append("username is empty")
    elif len(username) < 3:
        errors.append(f"username is too short: {len(username)} chars (min 3)")
    elif " " in username:
        errors.append("username must not contain spaces")
    
    # Password checks
    if not password:
        errors.append("password is empty")
    elif len(password) < 8:
        errors.append(f"password too short: {len(password)} chars (min 8)")
    
    # Email checks
    if not email:
        errors.append("email is empty")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errors.append(f"email format invalid: {email}")
    
    # Role check
    if role not in ["admin", "Editor", "viewer"]:
        errors.append(f"invalid role: {role!r}")

    return errors    # empty = valid

# TEST CASES

test_input = [
    ("tomsmith", "SuperSecretPassword!", "tom@test.com", "admin"),
    ("ab",       "short",                 "notanemail",   "superuser"),
    ("tom smith","ValidPass1!",           "tom@test.com", "viewer"),
    ("",         "",                      "",             "admin"),
]
for i, (u, p, e, r) in enumerate(test_input, 1):
    errs = validate_form_data(u, p, e, r)
    status = "VALID" if not errs else f"INVALID ({len(errs)} errors)"
    print(f"Input {i}: {status}")
    for err in errs:
        print(f" ✗ {err}")