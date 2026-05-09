# Retry engine (while + break + counter) ----------------------

import random
random.seed()

def retry(action_name, max_attempts=3, success_rate=0.6):
    """Retry an action upto max_attempts times ."""
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        print(f" [{action_name}] Attempt {attempt}/{max_attempts}")

        # Simulate action success/failure
        succeeded = random.random() < success_rate

        if succeeded:
            print(f" ✓ Succeeded on attempt {attempt}")
        if attempt < max_attempts:
            print(f" ✗ Failed - waiting before retry...")

    print(f" ✗ GAVE UP after {max_attempts} attempts")
    return False

# Run several actions through retry engine
actions = [
    ("click_submit",    3, 0.7),
    ("wait_for_modal",  5, 0.4),
    ("verify_toast",    2, 0.9),
]

passed = []
failed = []

for name, attempts, rate in actions:
    print(f"\nRunning: {name}")
    ok = retry(name, attempts, rate)
    (passed if ok else failed).append(name)

print(f"\n --- Retry Summary")
print(f"Succeeded: {passed}")
print(f"Failed   : {failed}")