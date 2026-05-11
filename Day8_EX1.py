# Example 1 — Flexible test config builder - **kwargs in action

from typing import Dict, Any

def build_config(**kwargs: Any) -> Dict[str, Any]:
    """Build a test session config from keyword arguments.
    Unknown keys are accepted and stored as-is."""

    # Sensible defaults
    config = {
        "env": "staging",
        "browser": "chromium",
        "headless": True,
        "timeout": 5000,
        "retries": 2,
        "slow_mo": 0
    }

    # Override defaults with provided values
    config.update(kwargs)

    # Validate known keys
    valid_browsers = ["chromium", "firefox", "webkit"]
    valid_envs = ["dev", "staging", "prod"]

    errors = []
    if config["browser"] not in valid_browsers:
        errors.append(f"Invalid browser '{config['browser']}' - use {valid_browsers}")
    if config["env"] not in valid_envs:
        errors.append(f"Invalid env '{config['env']}' - use {valid_envs}")
    if config["timeout"] < 1000:
        errors.append(f"Timeout too low: {config['timeout']}ms (min 1000)")
    
    if errors:
        raise ValueError("\n".join(errors))
    
    return config

# Various ways to call it
c1 = build_config()
print("Defaults: ", c1)

c2 = build_config(browser="firefox", headless=False, slow_mo=500)
print("Custom: ", c2)

c3 = build_config(env="prod", browser="webkit", retries=5, video=True)
print("Prod: ", c3)

# Invalid - raises ValueError
try:
    build_config(browser="edge", timeout=500)
except ValueError as e:
    print(f"\nConfig error:\n{e}")