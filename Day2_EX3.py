
#URL security validator 

# URLs returned after various actions in the app
urls = [
    "https://staging.myapp.com/dashboard",
    "http://staging.myapp.com/login",      # insecure!
    "https://staging.myapp.com/profile",
    "https://evil.com/phishing",            # wrong domain!
    "https://staging.myapp.com/logout",
]

print("------ URL Security check -------")

for url in urls:
    is_https = url.startswith("https")
    is_domain = "myapp.com" in url
    is_safe = is_https and is_domain

    status = "Pass" if is_safe else "Fail"
    print(f"[{status}] {url}")
    if not is_https:
        print(f" ^Not HTTPS!")
    if not is_domain:
        print(f" ^Wrong domain!")
