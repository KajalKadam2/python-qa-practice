
#API response field checker 

# Simulating a JSON response from reqres.in/api/users/2
first_name = "Janet"
last_name = "Weaver"
email = "janel.weaver@reqres.in"
avatar_url = "https://reqres.in/img/faces/2-image.jpg"

# Build full name from parts
full_name = f"{first_name} {last_name}"
print(f"Full name: {full_name}")

# Validate email format (basic checks)
has_at = "@" in email
has_dot = "." in email.split("@")[-1]
not_empty = len(email.strip()) > 0
looks_valid = has_at and has_dot and not_empty

print(f"Email: {email}")
print(f" Has @: {has_at}")
print(f" Has dot: {has_dot}")
print(f" Not empty: {not_empty}")
print(f" Looks valid: {looks_valid}")

# Validate avatar URL
print(f"\nAvatar URL checks:")
print(f" Is HTTPS: {avatar_url.startswith('https')}")
print(f" Is image: {avatar_url.endswith(('.jpg','.png','.webp'))}")
print(f" Has user ID: {'2' in avatar_url}")

# Domain extraction from email
domain = email.split("@")[1]
print(f"\nEmail domain: {domain}")
print(f"Domain is reqres.in: {domain == 'reqres.in'}")
