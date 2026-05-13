# Example 3 — Config loader with validation files + JSON + custom errors

import json
from typing import Any, Dict

class ConfigError(Exception):
    """ Raise when configuration is missing or invalid """
    pass

def load_config(filepath: str) -> Dict[str, Any]:
    """Load and validate test config from a JSON file.

    Raises ConfigError for any problem found.
    Returns validated config dict on success.
    """

    # Step 1 - load the file
    try:
        with open(filepath, "r") as f:
            config = json.load(f)

    except FileNotFoundError:
        raise ConfigError(f" Config file not found: '{filepath}")
    
    except json.JSONDecodeError as e:
        raise ConfigError(f" Invalid JSON in '{filepath}': {e}")
    
    # Step 2 - check required keys
    required = ["base_url", "env", "browser", "timeout"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ConfigError(f" Missing required keys: {missing}")
    
    # Step 3 - validate types
    if not isinstance(config["timeout"], int):
        raise ConfigError(f" 'timeout' mist be int, got {type(config['timeout']).__name__}")
    if not config["base_url"].startswith("http"):
        raise ConfigError(f" 'base_url' must start with http: {config['base_url']}")
    
    return config

# Test with different scenarios
scenarios = [
    ("test_data.json",   "real file (from page 4)"),
    ("missing.json",     "missing file"),
]

for filepath, label in scenarios:
    print(f" Loading: {label}")
    try:
        cfg = load_config(filepath)
        print(f" ✓ Loaded: env={cfg.get('env')} browser={cfg.get('browser')}")
    except ConfigError as e:
        print(f" ✗ ConfigError: {e}")
    print()