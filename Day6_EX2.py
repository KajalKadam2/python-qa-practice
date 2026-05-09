# Test matrix runner nested + zip + all/any

browsers  = ["chromium", "firefox"]
envs      = ["staging", "prod"]
pages     = ["/login", "/dashboard"]

# Result matrix - dict of dicts
matrix = {}

import random
random.seed()

for env in envs:
    matrix[env] = {}
    for browser in browsers:
        matrix[env][browser] = {}
        for page in pages:
            # Simulate: prod has more failures
            rate = 0.7 if env == "prod" else 0.9
            result = "PASS" if random.random() < rate else "FAIL"
            matrix[env][browser][page] = result

# Print matrix report
print(f"{'='*50}")
print(f" Test Matrix Report")
print(f"{'='*50}")

all_results = []
for env, browsers_data in matrix.items():
    print(f"\n Environment: {env.upper()}")
    for browser, pages_data in browsers_data.items():
        env_results = list(pages_data.values())
        all_results.extend(env_results)
        status = "✓ all pass" if all(r == "PASS" for r in env_results) else "✗ has failures"
        print(f" {browser:10}: {status}")
        for page, result in pages_data.items():
            icon = "✓" if result == "PASS" else "✗"
            print(f" {icon} {page} - {result}")

print(f"{'='*50}")
total = len(all_results)
passed = all_results.count("PASS")
print(f" Total: {passed}/{total} passed")
print(f" Any failures: {any(r == 'FAIL' for r in all_results)}")