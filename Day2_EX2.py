#Error message validator 

# Simulating text scraped from a web page
scraped_text = "  \n  Your username is invalid!  \n  "

# Step 1: clean it
clean = scraped_text.strip()
print(f"After clean: '{clean}'")

# Step 2: normalise case
normalised = clean.lower()
print(f"Normalised: '{normalised}'")

# Step 3: assert — does it contain expected text?
expected = "invalid"
print(f"Contains '{expected}': {expected in normalised}")

# Real assertion pattern — one chained line
assert "invalid" in scraped_text.strip().lower(), \
    f"Expected error message to contain 'invalid', got: '{clean}'"
print("Assertion passed")

# Now test an exact match
expected_exact = "Your username is invalid!"
print(f"Exact match: {clean == expected_exact}")
