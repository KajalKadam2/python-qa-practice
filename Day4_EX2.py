# ---------- QA Example 2 — API response field validator ------------

# Simulating: data = requests.get(url).json()["data"]
api_data = {
    "id":         2,
    "email":      "janet.weaver@reqres.in",
    "first_name": "Janet",
    "last_name":  "Weaver",
    "avatar":     "https://reqres.in/img/faces/2-image.jpg"
}

#Define what fields MUST exist in the response
required_fields = ["id", "email", "first_name", "last_name", "avatar"]

#Check all required fields are present
missing = [f for f in required_fields if f not in api_data]
if missing:
    print(f"FAIL: Missing fields: {missing}")
else:
    print(f"PASS: All required fields present")

#Validate field values
checks = {
    "id is integer"       :      isinstance(api_data["id"], int),
    "id is positive"      :     api_data["id"] > 0,
    "email has @   "      :     "@" in api_data["email"],
    "first_name not empty": len(api_data["first_name"]) > 0,
    "avatar is https"     : api_data["avatar"].startswith("https"),
    "avatar is image"     : api_data["avatar"].endswith((".jpg", ".png", ".webp"))
}

print("\nField validation: ")
all_ok = True
for check_name, result in checks.items():
    icon = "✓" if result else "x"
    print(f" {icon} {check_name}")
    if not result:
        all_ok = False
print(f"\nOverall : {'PASS' if all_ok else 'FAIL'}")