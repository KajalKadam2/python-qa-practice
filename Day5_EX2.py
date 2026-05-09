# Example 2 — API response classifier

def assess_api_response(status, body, response_ms):
    """Assess an API response - classify and Return assessment dict. """

    #Classify the status code
    if 200 <= status < 300:
        category = "success"
    elif status == 401:
        category = "auth_error"
    elif status == 404:
        category = "not_found"
    elif 400 <= status < 500:
        category = "client_error"
    elif 500 <= status < 600:
        category = "server_error"
    else:
        category = "unknown"

    # Assess body
    has_data = bool(body) and body is not None
    has_error = isinstance(body, dict) and "error" in body
    body_ok = has_data and not has_error

    # Performance classification
    perf = ("fast" if response_ms < 500 else 
            "ok" if response_ms < 1500 else 
            "slow" if response_ms < 3000 else 
            "timeout")
    
    overall = "PASS" if category == "success" and body_ok else "FAIL"

    return {
        "status"  :   status,
        "category": category,
        "body_ok" :  body_ok,
        "perf"    : perf,
        "overall" : overall
    }

responses = [
    (200, {"id": 1, "email": "a@b.com"}, 320),
    (404, {"error": "not found"},        110),
    (200, {} ,                           280),
    (500, {"error": "server crashed"},  4500)
]

for status, body, ms in responses:
    r = assess_api_response(status, body, ms)
    print(f" {r['overall']:4} | {r['status']} {r['category']:14} | body:{r['body_ok']} | {r['perf']}")