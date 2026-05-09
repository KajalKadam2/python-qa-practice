
#DAY 2

#single quote
url = 'https://staging.myapp.com'

#Double quote
message = "You logged into secure area"

#Triple quotes
test_description = '''This test verifies that a valid user
can log in and see the dashboard.'''

print(url)
print(message)
print(test_description)


password = "SuperSecretPassword"
print(len(password))

min_length = 8
print(len(password) >= min_length)

'''--------------------------------------------------------------------------------------'''

#Without f-string
env = "staging"
path = "/login"
url = "https://" + env + ".myapp.com" + path
print(url)

#With f-string ----------------------------------- clean
url = f"https://{env}.myapp.com{path}"
print(url)


# Any variable type works inside braces ----------------
test_num = 8
passed = True
print(f"Test {test_num} Result: {passed}")


# Expressions work inside braces too --------------------
total = 42
fails = 4
print(f"Pass rate: {total - fails}/{total}")
print(f"Percentage: {round((total-fails)/total*100, 1)}%")


#---------------------------------------------------------------------------------------
username = "tomsmith"
env = "staging"
browser = "chrome"
status = 200

# Print what your test is about to do — before the action
print(f"[Test] Logging in as '{username}' on {env} using {browser}")

# Print what happened — after the action
print(f"[Result] API responded with status: {status}")
print(f"[Pass] Expected 200, got {status} - {'Pass' if status == 200 else 'Fail'}")


#String methods — built-in tools on every string ----------------------------------------

message = " Your username is Invalid! "

clean = message.strip() # Clean it first
print(clean)

print(clean.lower()) # Lowercase for safe comparison

print("invalid" in clean.lower()) #case-insensitive check
print("success" in clean.lower())


url = "https://staging.myapp.com/login"
print(url.startswith("https"))
print(url.endswith("/login"))
print(url.replace("staging", "prod"))

# Split a URL into parts
parts = url.split("/")
print(parts)

