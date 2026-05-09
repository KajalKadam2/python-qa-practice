print("Hello QA")

#hello
'''hellooooooo'''


number1 = 10
number2 = 20

sum = number1 + number2
print("The sum is: ", sum)
#print("The product is: ", product)


#Test environment configuration

'''EXAMPLE 1'''

base_url = "https://staging.myapp.com"
browser = 'chromium'
timeout = 5000
headless = True
retry_max = 3

print(base_url)
print(browser)
print(timeout)
print(headless)
print(retry_max)

print(type(base_url))
print(type(timeout))
print(type(headless))


'''EXAMPLE 2'''
#Test User Credentials

username = "wronguser" # Changed the value
password = "SuperSecretPassword"
user_role = "admin"
expected_message = "You logged into secured area"

error_message = "Your username is invalid"
page_title = "The Internet"
login_url = "https://the-internet.herokuapp.com/login"

#print(username)
#print(password)
#print(user_role)
#print(expected_message)

print(error_message)
print(page_title)
print(login_url)

print(type(error_message))
print(type(page_title))
print(type(login_url))


'''EXAMPLE 3'''
# HTTP status codes you'll assert in API tests

status_ok = 200
status_created = 201
status_no_content = 204
status_not_found = 404
status_server_err = 500

print(status_ok)
print(status_not_found)

# Integers can do maths
timeout_seconds = 5000
timeout_minutes = timeout_seconds / 60000
print(timeout_minutes)

# Compare integers
actual_status = 200
print(actual_status == status_ok)
print(actual_status == status_not_found)

#Mini challenge
actual_response_time = 1250
max_allowed_time = 2000

print(actual_status < max_allowed_time)




'''Example 4'''
# Boolean flags in test configuration

headless_mode = True
slow_motion = False
take_screenshot = True
record_video = False
is_logged_in = False

print(headless_mode)
print(is_logged_in)
print(type(headless_mode))

# Booleans come from comparisons too
status = 200
test_passed = (status == 200)
test_failed = (status == 404)

print(test_passed)
print(test_failed)


# not flips a boolean
print(not test_passed)
print(not is_logged_in)



'''Example 5 - print() with labels '''
# Method 1: comma-separated (simplest)

url = "https://staging.myapp.com"
status = 200
passed = True

print("URL: ", url)
print("Status: ", status)
print("Passed: ", passed)

# Method 2: f-string 
print(f"Testing URL: {url}")
print(f"Response status: {status}")
print(f"Test passed: {passed}")

# Method 3: string concatenation with +
# Note: + only works between strings
# print("Status: " + status)  ← this CRASHES
print("Status:" + str(status))