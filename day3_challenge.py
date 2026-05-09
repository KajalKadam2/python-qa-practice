
# DAY 3 Challenge

browsers = ["chromium", "firefox", "webkit"]
test_pages = ["/login", "/dashboard", "/profile", "/checkout"]
env = "staging"
base_url = f"https://{env}.myapp.com"

#Part 1 — build full URLs with list comprehension ─
full_urls = [f"{base_url}{page}" for page in test_pages]
print("URLto test:")
for url in full_urls:
    print(f" {url}")


#Part 2 — Simulate test runs
print(f"\n--- Test Runs ---")
results = []

for i, browser in enumerate(browsers, start=1):
    print(f"\nBrowser {i}/{len(browsers)}: {browser.upper()}")
    for url in full_urls:
        print(f" [{browser}] Testing: {url}")
        results.append("PASS")


#Part 3 — Collect results
total_runs = len(results)
n_passed   = results.count("PASS")
n_failed   = results.count("FAIL")


#Part 4 — Analyse
first_three = results[:3]
last_three = results[-3:]
has_failed = "FAIL" in results

print(f"\n --- Analysis ---")
print(f"First 3 results : {first_three}")
print(f"Last 3 results  : {last_three}")
print(f"Any failures    : {has_failed}")

# ── Part 5: final summary ───────────────────────────
status = "ALL PASSED" if n_failed == 0 else f"{n_failed} FAILED"

print(f"\n{'='*28}")
print(f"Cross-browser Test Summary")
print(f"{'='*28}")
print(f"Browsers Tested : {len(browsers)}")
print(f"Pages Tested    : {len(test_pages)}")
print(f"Total runs.     : {total_runs}")
print(f"Passed          : {n_passed}")
print(f"Failed          : {n_failed}")
print(f"Status          : {status}")