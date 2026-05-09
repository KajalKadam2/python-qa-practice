#What is a dictionary

# Creating a dict — curly braces, key: value pairs
test_user = {
    "username": "tomsmith",
    "password": "SuperSecretPassw0rd",
    "role"    : "admin",
    "active"  : True,
    "login_attempts": 0
}

#Access values by key
print(test_user["username"])
print(test_user["role"])
print(test_user["active"])

#f-string with dict values
print(f"Logging in as: {test_user['username']}")
print(f"Role: {test_user['role']} | Active: {test_user['active']}")

#Check how many keys it has
print(len(test_user))

#Check if a key exists
print("email" in test_user)
print("role" in test_user)

print('='*28)

# --------- Reading dict values safely — .get()  --------------------------

#Simulating an API response - some fields may be missing

api_response = {
    "id":    2,
    "email": "janet.weaver@reqres.in",
    "first_name": "Janet"
    # "phone" is missing — not all APIs return all fields
}

#Direct access - crashes if key missing
print(api_response["email"])
#print(api_response["phone"]) ----- keyError: 'phone' - crash

#.get() - safe, returns None by default
print(api_response.get("email"))
print(api_response.get("phone")) #----- no crash

# .get() with default value
print(api_response.get("phone", "not provided"))
print(api_response.get("id", 0))


print('='*28)

# --------- Modifying dicts + looping over them - .items()  --------------------------

# Start with a basic config
config = {
    "env":     "staging",
    "browser": "chromium",
    "timeout": 5000
}
print(f"Original: {config}")

#Add a new key
config["headless"] = True
config["retries"] = 3
print(f"After add: {config}")

#Update an existing key
config["timeout"] = 8000
config["env"] = "prod"
print(f"After update: {config}")

#Remove key
removed = config.pop("retries")
print(f"Removed 'retries' (value was {removed}) : {config}")

#Check if a key exists before using it
if "headless" in config:
    print(f"Headless mode: {config['headless']}")

#Loop over ALL key-value pairs
print("\n--- Config Dump ---")
for key, value in config.items():
    print(f" {key:10} : {value}")

print('='*28)


#------------------ Nested dicts — dicts inside dicts ------------------------------------------
# Simulating reqres.in/api/users/2 response
response = {
    "data": {
        "id":         2,
        "email":      "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name":  "Weaver",
        "avatar":     "https://reqres.in/img/faces/2-image.jpg"
    },
    "support": {
        "url":  "https://contentcaddy.io?utm_source=reqres",
        "text": "Tired of writing endless social media content?"
    }
}

#Access nested fields - chain the brackets
user_id = response["data"]["id"]
email   = response["data"]["email"]
first   = response["data"]["first_name"]
last    = response["data"]["last_name"]

print(f"ID    :   {user_id}")
print(f"Email : {email}")
print(f"Name  : {first}{last}")

#safe nested access with .get()
phone = response["data"].get("phone", "not in response")
print(f"Phone : {phone}")

#Assert nested fields - what a real API test does
assert response["data"]["id"] == 2, "User ID should be 2"
assert "@" in response["data"]["email"], "Email should contain @"
assert response["data"]["first_name"] == "Janet", "First name mismatch"
print("All assertions passed!")


print('='*28)


# ------- List of dicts — the most common API pattern --------------------------------------------

# Simulating reqres.in/api/users  — list of user dicts
users = [
    {"id": 1, "email": "george.bluth@reqres.in",  "first_name": "George", "active": True},
    {"id": 2, "email": "janet.weaver@reqres.in",  "first_name": "Janet",  "active": True},
    {"id": 3, "email": "emma.wong@reqres.in",    "first_name": "Emma",   "active": False},
    {"id": 4, "email": "eve.holt@reqres.in",     "first_name": "Eve",    "active": True},
]

#Loop over list, access dict fields for each user
print("All users:")
for user in users:
    status = "ACTIVE" if user["active"] else "INACTIVE"
    print(f" [{status}] ID {user['id']}: {user['first_name']} - {user['email']}")

#Filter only active users
active_users = [u for u in users if u["active"]]
print(f"\nActive users: {len(active_users)}/{len(users)}")

#Extract just the emails into a list
all_emails = [u["email"] for u in users]
print(f"Emails: {all_emails}")

#Find a specific user by ID
target_id = 3
found = None
for user in users:
    if user["id"] == target_id:
        found = user
        break
print(f"\nUser {target_id}: {found['first_name'] if found else 'not found'}")