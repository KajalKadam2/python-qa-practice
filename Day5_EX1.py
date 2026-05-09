# Example 1 — Login test decision engine 

def evaluate_login_result(url, title, flash, response_ms):
    """ Evaluate a login attempt result - return PASS or FAIL with reason."""

    # Guard clauses - check failure first
    if not url:
        return "FAIL", "URL is empty"
    if not url.startswith("https"):
        return "FAIL", f"URL not secure: {url}"
    if not title.strip():
        return "FAIL", "Page title is empty"
    if not flash or "secure area" not in flash.strip().lower():
        return "FAIL", f"Flash message wrong: {repr(flash)}"
    if response_ms > 3000:
        return "FAIL", f"Too slow: {response_ms}"
    
    #All checks passed
    speed = "fast" if response_ms < 1000 else "acceptable"
    return "PASS", f"Login OK in {response_ms}ms ({speed})"

#Run it again multiple scenarios
scenario = [
    ("https://app.com/secure", "Secure Area", "You logged into a secure area!", 840),
    ("https://app.com/secure", "Secure Area", "You logged into a secure area!", 3500),
    ("http://app.com/secure",  "Secure Area", "You logged into a secure area!", 500),
    ("https://app.com/secure", "Secure Area", "Your username is invalid!",      300),
    ("https://app.com/secure", "Secure Area", "You logged into a secure area!", 1200),
]
print("Login test results: ")
for i, (url, title, flash, ms) in enumerate(scenario, 1):
    verdict, reason = evaluate_login_result(url, title, flash, ms)
    icon = "✓" if verdict == "PASS" else "✗"
    print(f" {icon} Scenario {i}: {verdict} - {reason}")