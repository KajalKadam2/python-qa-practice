#EXAMPLE 1 

env = "staging"
protocol = "https"
domain = "myapp.com"

base_url = f"{protocol}://{env}.{domain}"
login_url = f"{base_url}/login"
dashboard_url = f"{base_url}/dashboard"
profile_url = f"{base_url}/profile"
api_url = f"{base_url}/api/v1"

print(f"Base: {base_url}")
print(f"Login: {login_url}")
print(f"Dashboard: {dashboard_url}")
print(f"Profile: {profile_url}")
print(f"API: {api_url}")


env = "Prod"

base_url = f"{protocol}://{env}.{domain}"
login_url = f"{base_url}/login"
print(f"\nSwitched to PROD: {login_url}")


reset_password_url = "path:/reset-password"
admin_url = "path:/admin/users"
api_users_url = "path:/api/v1/users"

print(f"--- Test Environment: {env} ---")
print(f"Login URL: {login_url}")