# ---------- Example 1 — Test configuration system ---------------

# Central test configuration — one place to rule them all
config = {
    "env":      "staging",
    "base_url": "https://staging.myapp.com",
    "browser":  "chromium",
    "timeout":  5000,
    "headless": True,
    "retries":  2,
    "screenshot_on_fail": True,
    "credentials": {
        "valid":   {"username": "tomsmith", "password": "SuperSecretPassword!"},
        "invalid": {"username": "wronguser", "password": "wrongpass"}
    }
}

#Build URLs from config
login_url = f"{config['base_url']}/login"
dashboard_url = f"{config['base_url']}/dashboard"
api_url = f"{config['base_url']}/api/v1"

#Access nested credentials
valid_user = config["credentials"]["valid"]
invalid_user = config["credentials"]["invalid"]

#Print full config - loop over top-level keys
print(f"{'='*35}")
print(f" Test Configuration")
print(f"{'='*35}")

for key, value in config.items():
    if key != "credentials":
        print(f" {key:22}: {value}")

print(f"{'='*35}")
print(f" Login URL   : {login_url}")
print(f" Valid user  : {valid_user['username']}")
print(f" Invalid user: {invalid_user['username']}")