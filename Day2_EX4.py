
#Test result report formatter 

# Test session data
app_name = "ShopCart Pro"
env = "staging"
browser = "Chrome"
total = 47
passed = 43
failed = 4
duration_s = 127.5

# Calculate derived values
pass_rate = (passed/total)*100
skipped = total-passed-failed

print(f"{'=' *40}")
print(f" Test Report - {app_name}")
print(f"{'=' *40}")
print(f"Environment : {env}")
print(f"Browser     : {browser}")
print(f"Duration    : {duration_s:.1f}s")
print(f"{'-' *40}")
print(f"Total tests : {total}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")
print(f"Skipped     : {skipped}")
print(f"Pass rate   : {pass_rate:.1f}%")
print(f"{'-' *40}")
print(f" Status: {'PASSED' if failed == 0 else 'FAILED'}")