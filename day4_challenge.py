# --------- Day 4 challenge — write it all from scratch ----------

api_users = [
  {"id":1,"email":"george.bluth@reqres.in","first_name":"George","last_name":"Bluth","active":True},
  {"id":2,"email":"janet.weaver@reqres.in","first_name":"Janet","last_name":"Weaver","active":True},
  {"id":3,"email":"emma.wong","first_name":"Emma","last_name":"Wong","active":False},
  {"id":4,"email":"","first_name":"Eve","last_name":"Holt","active":True},
  {"id":5,"email":"charles.morris@reqres.in","first_name":"","last_name":"Morris","active":True},
]
required_fields = ["id","email","first_name","last_name","active"]

# Part 1 — Field presence check
print("Part 1 — Required field presence")
print("─" * 38)

for user in api_users:
    missing = [f for f in required_fields if f not in user]
    status  = "PASS" if not missing else f"FAIL — missing: {missing}"
    print(f"  User {user['id']}: {status}")


# Part 2 — Value validation
print("\nPart 2 — Value validation")
print("─" * 38)
all_failures = []

for user in api_users:
    uid = user["id"]
    failures = []

    if "@" not in user["email"]:
        failures.append(f"email invalid ({repr(user['email'])})")
    if not user["first_name"].strip():
        failures.append("first_name is empty")
    if user["id"] <= 0:
        failures.append("id must be > 0")

    if failures:
        all_failures.extend(failures)
        print(f" User {uid} FAIL: ")
        for f in failures:
            print(f" ✗ {f}")
    else:
        print(f" User {uid} ✓ PASS")

# Part 3 — Extract and analyse
print("\nPart 3 — Extracted data")
print("─" * 38)

all_emails   = [u["email"] for u in api_users]
all_ids      = [u["id"] for u in api_users]
active_users = [u for u in api_users if u["active"]]

print(f" All IDs      : {all_ids}")
print(f" All emails   : {all_emails}")
print(f" Active users : {[u['first_name'] for u in active_users]}")

# Part 4 — Safe access with .get()
print("\nPart 4 — Safe field access")
print("─" * 38)

for user in api_users:
    phone = user.get("phone", "N/A")
    print(f" User {user['id']} phone: {phone}")


# Part 5 — Summary report
print("\nPart 5 - Summary report")
total          = len(api_users)
active_count   = len([u for u in api_users if u["active"]])
inactive_count = total - active_count
bad_emails     = len([u for u in api_users if "@" not in u["email"]])
empty_names    = len([u for u in api_users if not u["first_name"].strip()])
overall        = "PASS" if not all_failures else f"FAIL ({len(all_failures)} issues)"

print(f"{'='*38}")
print(f" Total users      : {total}")
print(f" Active           : {active_count}")
print(f" Inactive         : {inactive_count}")
print(f" Inactive emails  : {bad_emails}")
print(f" Empty first_name : {empty_names}")

print(f"{'-'*38}")
print(f" Overall          : {overall}")
print(f"{'='*38}")