# 

import requests

HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

# --- Make a GET request -----------------------
response = requests.get("https://reqres.in/api/users/2", headers=HEADERS)

# ---- Status code -----------------------------
print(f"Status code    : {response.status_code}") #200
print(f"OK ?           : {response.ok}") # True if 2xx

# ---- Headers ---------------------------------
print(f"\nContent-Type : {response.headers['Content-Type']}") 

# ---- Body as JSON ------------------------
body = response.json() # converts JSON string to python dict
print(f"\nFull body : {body}")

# ----Navigate the nested dict -------------------
data = body["data"]
print(f"\nUser ID  : {data['id']}")
print(f"First Name : {data['first_name']}")
print(f"Last name  : {data['last_name']}")
print(f"Email      : {data['email']}")
print(f"Avatar URL : {data['avatar']}")

# ---- Response time ------------------------------
print(f"\nResponse time : {response.elapsed.total_seconds():.3f}s")