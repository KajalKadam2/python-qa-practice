#Day1 Challenge


app_name = "Day 1 Challenge"
test_env = "staging"
tester_name = "Kajal"
browser = "chrominum"

total_test = 42
tests_passed = 38
tests_failed = 4

all_critical_passed = True
blocking_bug_found = False

print(f"Test session: {app_name} on {test_env}")
print(f"Tester: {tester_name} | Browser: {browser}")
print(f"Results: {tests_passed}/{total_test} passed")
print(f"Critical test passed: {all_critical_passed}")
print(f"Blocking bug found: {blocking_bug_found}")

print(type(total_test))
print(type(test_env))
print(type(all_critical_passed))
