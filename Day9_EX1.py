# Example 1 — Safe API response parser 

from typing import Any, Dict, List, Tuple

def parse_api_user(response: Dict[str, Any]) -> Tuple[bool, Dict, List[str]]:
     """Safely parse a user from an API response dict.

    Returns:
        (success, user_data, errors)
    """
     errors = {}
     user = {}
     
     # Try to get nested data.email
     try:
        user["email"] = response["data"]["email"]
     except KeyError as e:
        errors["email"] = f"Missing key: {e}"

    # Try to get id as integer
     try:
         user["id"] = int(response["data"]["id"])
     except (KeyError, TypeError, ValueError) as e:
         errors["id"] = f"{type(e).__name__}: {e}"
    
    # Try to get first_name - not critical, default to empty
     try:
         user["first_name"] = response["data"]["first_name"].strip()
     except (KeyError, AttributeError):
         user["first_name"] = "" # default - not an error
    
     success = len(errors) == 0
     return success, user, list(errors.values())

# Test with various responses
responses = [
    {"data": {"id": 2, "email": "janet@reqres.in", "first_name": "Janet"}},
    {"data": {"id": "not_int", "email": "eve@reqres.in"}},
    {"data": {"first_name": "Emma"}},   # missing id and email
    {},                                    # empty response
]

for i, resp in enumerate(responses, 1):
    ok, user, errs = parse_api_user(resp)
    status = " ✓ PASS" if ok else " ✗ FAIL"
    print(f" Response {i}: {status}")
    if user: print(f" User: {user}")
    if errs: print(f" Errors: {errs}")