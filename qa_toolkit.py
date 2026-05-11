# ---- Config ---------------------
CONFIG = {
    "envs": {
        "staging": "https://staging.myapp.com",
        "prod": "https://myapp.com",
        "dev": "http://localhost:3000"
    },
    "supported_browsers": ["chromium", "firefox", "webkit"],
    "slow_threshold_ms": 2000,
    "pass_rate_threshold": 80
}

# ------ build_url() -------------------
def build_url(env, path="/"):
    """Build a full URL for the given environment and path.
    Returns (url, error) — error is None if valid."""

    #Guard: env must exist in config
    if env not in CONFIG["envs"]:
        valid = list(CONFIG["envs"].keys())
        return None, f"Unknown env '{env}'. Valid: {valid}"
    
    #Guard: path must start with /
    if not path.startswith("/"):
        return None, f"Path must start with '/': got '{path}'"
    
    base = CONFIG["envs"][env]
    url = f"{base}{path}"
    return url, None

#Quick test
"""url, err = build_url("staging", "/login")
print(f"URL: {url}")

url, err = build_url("unknown", "/login")
print(f"Error: {err}")"""

# ---- validate user() --------------------
def validate_user(user):
    """Validate a test user dict. Returns list of error strings.
    Empty list means valid."""
    errors = []

    # Guard: must be dict
    if not isinstance(user, dict):
        return ["user must be dict"]
    
    # Required fields
    for field in ["username", "password", "role"]:
        if field not in user:
            errors.append(f"missing filed: '{field}'")
    
    # Only validate values if fields exist
    if "username" in user:
        if not user["username"].strip():
            errors.append("username is empty")
        elif len(user["username"]) < 3:
            errors.append(f"username too short ({len(user['username'])} chars)")
    
    if "password" in user:
        if not user["password"]:
            errors.append("password is empty")
        elif len(user["password"]) < 8:
            errors.append(f"password too short ({len(user['password'])} chars)")
    
    if "role" in user:
        valid_roles = ["admin", "editor", "viewer"]
        if user["role"] not in valid_roles:
            errors.append(f"invalid role '{user['role']}' - must be {valid_roles}")
    
    return errors

# Quick test
"""good = {"username": "tomsmith", "password": "SuperSecret!", "role": "admin"}
bad  = {"username": "ab",       "password": "short",       "role": "superuser"}

print(validate_user(good)) #[]
print(validate_user(bad)) # ['username too short...', 'password too short...', 'invalid role...']"""

# ---- classify_response() ------------------------------
def classify_response(status, body=None, ms=0):
    """Classify an API response. Returns a result dict."""

    # Status category
    if 200 <= status < 300:    category = "success"
    elif status == 401:        category = "unauthorized"
    elif status == 403 :       category = "forbidden"
    elif status == 404 :       category = "not_found"
    elif 400 <= status < 500 : category = "client_error"
    elif 500 <= status < 600 : category = "server_error"
    else:                      category = "unknown"

    # Body assessment
    has_body = body is not None and bool(body)
    has_error = isinstance(body, dict) and "error" in body

    # Performance
    slow_ms = CONFIG["slow_threshold_ms"]
    perf = "fast" if ms < 500 else "ok" if ms < slow_ms else "slow"

    # Overall verdict
    passed = category == "success" and has_body and not has_error

    return {
        "status" :  status,
        "category": category,
        "has_body": has_body,
        "perf":     perf,
        "passed":   passed,
        "verdict":  "PASS" if passed else "FAIL"
    }

# Quick test
"""r = classify_response(200, {"id": 1, "email": "a@b.com"}, 320)
print(f"200 with body: {r['verdict']} ({r['perf']})") #PASS {fast}

r= classify_response(200, {}, 150)
print(f"200 empty body: {r['verdict']}") #FAIL """


# ---- run_test_suite() -----------------------
import random

def run_test_suite(test_cases, browsers, seed=42):
    """Run all test cases across all browsers.
    Returns list of result dicts."""
    random.seed(seed)

    # Validate browsers first
    invalid = [b for b in browsers if b not in CONFIG["supported_browsers"]]
    if invalid:
        print(f" Warning: unsupported browsers will be skipped: {invalid}")
        browsers = [b for b in browsers if b in CONFIG["supported_browsers"]]
    
    results = []

    for browser in browsers:
        for tc in test_cases:
            # Skip P3 tests
            if tc.get("priority") == "P3":
                continue

            # Simulate: higher pass rate for P1 tests
            rate   = 0.85 if tc.get("priority") == "P1" else 0.7
            status = "PASS" if random.random() < rate else "FAIL"
            ms     = random.randint(150, 3500)

            results.append({
                "browser":     browser,
                "test_id":     tc["id"],
                "test_name":   tc["name"],
                "priority":    tc.get("priority", "P2"),
                "retries":     tc.get("retrier", 2),
                "status":      status,
                "duration_ms": ms
            })
    return results

# retry_failures() ---------------------------------
def retry_failures(results, verbose=True):
    """Retry failed tests up to their retry count.
    Mutates results in place. Returns count of recovered tests."""
    recovered = 0

    for result in results:
        if result["status"] != "FAIL":
            continue

        attempt = 0
        max_r = result["retries"]

        if verbose:
            print(f" Retrying [{result['test_id']}] on {result['browser']}...")
        
        while attempt < max_r and result["status"] == "FAIL":
            attempt += 1
            if random.random() > 0.4:
                result["status"] = "PASS"
                result["recovered"] = True
                recovered += 1
                if verbose:
                    print(f" ✓ Recovered on try {attempt}")
                elif verbose:
                    print(f" ✗ Retry {attempt}/{max_r} failed")
    return recovered

# ---- generate_report() -----------------------------------------------------
def generate_report(results, config=None):
    """Generate a full session report from results list."""
    if not results:
        return "No results to report."
    
    config = config or {}
    env    = config.get("env", "unknown")

    # Aggregate counts
    total     = len(results)
    passed    = sum(1 for r in results if r["status"] == "PASS")
    failed    = total - passed
    recovered = sum(1 for r in results if r.get("recovered"))
    pass_rate = round(passed / total*100, 1)

    # Performance analysis
    durations  = [r["duration_ms"] for r in results if "duration_ms" in r]
    avg_ms     = round(sum(durations) / len(durations)) if durations else 0
    slow_count = sum(1 for ms in durations if ms > CONFIG["slow_threshold_ms"])

    # Priority analysis
    p1_results = [r for r in results if r["priority"] == "P1"]
    all_p1_passed = all(r["status"] == "PASS" for r in p1_results) if p1_results else True

    # Failed test names
    failures = [f"[{r['test_id']}] {r['test_name']} on {r['browser']}"
                for r in results if r["status"] == "FAIL"]
    
    # Overall gate
    threshold = CONFIG["pass_rate_threshold"]
    overall   = "PASS" if pass_rate >= threshold and all_p1_passed else "FAIL"

    # Build the report
    lines = [
        f"{'='*45}",
        f" QA SESSION REPORT",
        f" Environment  : {env}",
        f"{'='*45}",
        f" Total runs   : {total}",
        f" Passed       : {passed} ({pass_rate}%)",
        f" Failed       : {failed}",
        f" Recovered    : {recovered}",
        f" Avg duration : {avg_ms}ms",
        f" Slow tests   : {slow_count}",
        f" All P1 pass  : {all_p1_passed}",
        f"{'='*45}",
        f" OVERALL      : {overall}",
        f"{'='*45}"
    ]
    if failures:
        lines.append(f"\n Failures ({len(failures)}):")
        for f in failures:
            lines.append(f" ✗ {f}")
    
    return "\n".join(lines)

# ------ Main demo -------------------------------------------------
if __name__ == "__main__":

    # Test data
    TEST_USERS = [
        {"username": "tomsmith", "password": "SuperSecretPassword!", "role": "admin"},
        {"username": "ab",        "password": "short",                "role": "superuser"},
    ]

    TEST_CASES = [
        {"id":"TC01", "name":"valid_login",    "priority":"P1", "retries":3},
        {"id":"TC02", "name":"invalid_login",  "priority":"P1", "retries":2},
        {"id":"TC03", "name":"checkout_flow",  "priority":"P1", "retries":3},
        {"id":"TC04", "name":"profile_update", "priority":"P2", "retries":2},
        {"id":"TC05", "name":"logout",         "priority":"P3", "retries":1},
    ]

    BROWSERS = ["chromium", "firefox"]

    # 1. Validate URLs
    print(" ---- URL Validation ----------------------")
    for env, path in [("staging", "/login"), ("prod", "login"), ("unknown", "/x")]:
        url, err = build_url(env, path)
        if err: print(f" ✗ Error: {err}")
        else: print(f" ✓ {url}")

    # 2. Validate users
    print("\n---- User validation -------------------")
    for user in TEST_USERS:
        errs = validate_user(user)
        status = "✓ valid" if not errs else f"✗ {len(errs)} errors"
        print(f" {user['username']:12} : {status}")
        for e in errs:
            print(f"     → {e}")

    # 3. Run suite
    print("\n---- Running test suite -----------------")
    results = run_test_suite(TEST_CASES, BROWSERS)
    passed_first = sum(1 for r in results if r["status"] == "PASS")
    print(f" {len(results)} runs, {passed_first} passed initially")

    # 4. Retry failures
    print("\n---- Retrying failures -----------------")
    recovered = retry_failures(results)
    print(f" Recovered: {recovered} tests")

    # 5. Generate report
    print("\n" + generate_report(results, {"env": "staging"}))