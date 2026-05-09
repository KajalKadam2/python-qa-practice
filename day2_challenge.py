
#The challenge — QA login test string validator

env = "staging"
username = "tomsmith"
current_url = " https://staging.myapp.com/secure "
page_title = " Secure Area "
flash_message = "\n You logged into a secure area! \n"
response_time_ms = 843

# Build a login_url using f-string: https://staging.myapp.com/login
login_url = f"https://{env}.myapp.com/login"
print(f"Login URL: {login_url}")

#Clean current url
clean_url = current_url.strip()
print(f"Current URL: {clean_url}")

#Clean page_title
clean_title = page_title.strip()
print(f"Page title: {clean_title}")

#Flash message contains "secure area"
flash_clean = flash_message.strip().lower()
flash_ok = "secure area" in flash_clean
print(f"Flash OK: {flash_ok}")

#URL starts with https
url_secure = clean_url.startswith("https")
print(f"URL secure {url_secure}")

#URL ends with /secure
on_secure_page = clean_url.endswith("/secure")
print(f"On /secure : {on_secure_page}")

#response time under 2000ms
fast_enough = response_time_ms < 2000
print(f"Fast enough: {fast_enough}")

#overall result + summary
all_passed = url_secure and on_secure_page and flash_ok and fast_enough
overall = "PASS" if all_passed else "FAIL"

print(f"{'=' *25}")
print(f"=== Login Test Result ===")
print(f"{'=' *25}")
print(f"Environment : {env}")
print(f"User        : {username}")
print(f"URL secure  : {url_secure}")
print(f"On /secure  : {on_secure_page}")
print(f"Flash OK    : {flash_ok}")
print(f"Fast enough : {fast_enough}")
print(f"{'-' *25}")
print(f"Overall     : {overall}")