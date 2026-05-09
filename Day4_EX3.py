# ------------------- Example 3 — Multi-user test data bank ---------------------

# Complete test user data bank
test_users = [
    {
        "id":            "valid_admin",
        "username":     "tomsmith",
        "password":     "SuperSecretPassword!",
        "role":         "admin",
        "expect_login": True,
        "expect_msg":   "You logged into a secure area!"
    },
     {
        "id":            "wrong_password",
        "username":     "tomsmith",
        "password":     "wrongpassword",
        "role":         None,
        "expect_login": False,
        "expect_msg":   "Your password is invalid!"
    },
    {
        "id":            "wrong_username",
        "username":     "baduser",
        "password":     "SuperSecretPassword!",
        "role":         None,
        "expect_login": False,
        "expect_msg":   "Your username is invalid!"
    },
]

#Loop and simulate running each test case
print(f"Running {len(test_users)} login tests\n")

for i, user in enumerate(test_users, 1):
    print(f"Test{i}: {user['id']}")
    print(f" Username    : {user['username']}")
    print(f" Expect login: {user['expect_login']}")
    print(f" Expect msg  : {user['expect_msg']}")

    print(f" → Would fill form and assert message\n")