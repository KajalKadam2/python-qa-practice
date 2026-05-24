# 

import pytest
from pages.login_page import LoginPage


def test_valid_login(login_page_pom: LoginPage):
    (login_page_pom
     .login("tomsmith", "SuperSecretPassword!")
     .expect_success())
    
def test_wrong_username(login_page_pom: LoginPage):
    (login_page_pom
     .login("wronguser", "wrongpass")
     .expect_error("Your username is invalid")
     .expect_on_login_page())

def test_wrong_password(login_page_pom: LoginPage):
    (login_page_pom
     .login("tomsmith", "wrongpass")
     .expect_error("Your password is invalid")
     .expect_on_login_page())

def test_empty_fields(login_page_pom: LoginPage):
    (login_page_pom
     .login("", "")
     .expect_error("Your username is invalid"))

# POM + parametrize together ---------------------------------
@pytest.mark.parametrize("username, password, error", [
    ("wronguser", "pass", "Your username is invalid"),
    ("tomsmith", "wrong", "Your password is invalid"),
    ("", "", "Your username is invalid"),
], ids=["bad_user", "bad_pass", "empty"])

def test_invalid_logins_parametrized(login_page_pom: LoginPage, username, password, error):
    (login_page_pom
     .login(username, password)
     .expect_error(error))