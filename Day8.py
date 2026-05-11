# ---- *args — accept any number of positional arguments -------

# Without *args - limited to fixed number of time
def log_steps_bad(step1, step2, step3):
    pass

# With *args - any number of steps
def log_steps(*args):
    """Log any number of steps"""
    print(f"Running {len(args)} steps")
    for i, step in enumerate(args, 1):
        print(f" Step{i}: {step}")

log_steps("Open browser")
print()
log_steps("Open browser", "Go to login", "Fill username", "Click submit")
print()

# Mix regular args with *args - regular args come FIRST
def check_urls(env, *urls):
    """Check multiple URLs in a given environment """
    print(f"Checking {len(urls)} URLs on {env}")
    for url in urls:
        print(f" -> {url}")

check_urls("staging", "/login", "/dashboard", "/checkout")
print()

# Unpack a list into *args with * operator
pages = ["/login", "/profile", "/logout"]
check_urls("prod", *pages)



# -------- **kwargs — accept any number of keyword arguments  -----------------------
def configure_test(**kwargs):
    """Accept any configuration option"""
    print(f"Test configuration ({len(kwargs)} options:)")
    for key, value in kwargs.items():
        print(f" {key} = {value}")

configure_test(browser="chromium", headless=True)
print()
configure_test(browser="firefox", timeout=8000, slow_mo=500, video=True)
print()

# Mix regular + *args + **kwargs together
def run_suite(suite_name, *test_ids, **options):
    """Run a named suite with specific tests and options"""
    print(f"Suite: {suite_name}")
    print(f"Tests: {list(test_ids)}")
    print(f"Options: {options}")

run_suite("smoke", "TC01", "TC01", "TC03", browser="Chromium", retries=2)
print()

#Unpack a dict into **kwargs with the ** operator
my_options = {"browser":"webkit", "headless": False, "timeout": 3000}
configure_test(**my_options)


# -------- Type hints — self-documenting functions  ---------------------------------------------------
# Without type hints - 
def validate_email(email, strict):
    pass

# With type hints -
def validate_email(email: str, strict: bool = False) -> bool:
    """Return True if email looks valid"""
    if not email.strip():
        return False
    if "@" not in email:
        return False
    if strict and "." not in email.split("@")[-1]:
        return False
    return True

print(validate_email("tom@test.com")) #True
print(validate_email("notanemail")) # False
print(validate_email("tom@test", strict=True)) #False - strict needs dot in domain

print()

# Common type hints for QA automation
from typing import Optional, List, Dict, Tuple

def run_test(
        test_name: str,
        browser: str = "chromium",
        retries: int = 3,
        tags: Optional[List[str]] = None  #None - safe default
) -> Tuple[bool, str]:
    """Run a test. Returns(passed, message)"""
    tags = tags or []
    return True, f"Passed on {browser} with tags {tags}"

ok, msg = run_test("test_login", tags=["smoke", "P1"])
print(ok, msg)