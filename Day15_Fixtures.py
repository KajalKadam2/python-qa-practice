# Fixtures

import pytest

# Runs before EVERY test - default
@pytest.fixture(scope="function")
def function_fixture():
    print("\n function_fixture: setting up")
    yield
    print("\n function_fixture: tearing down")

# Runs once per FILE - faster
@pytest.fixture(scope="module")
def module_fixture():
    print("\n module_fixture: setting up ONCE")
    yield {"token": "abc123"}
    print("\n module_fixture: tearing down ONCE")

# Runs once for ALL tests in the whole session
@pytest.fixture(scope="session")
def session_fixture():
    print("\n session_fixture: setting up ONE TIME")
    yield {"base_url": "https://the-internet.herokuapp.com"}
    print("\n session_fixture: done")

def test_a(function_fixture, module_fixture, session_fixture):
    print(f"\n test_a: token={module_fixture['token']}")

def test_b(function_fixture, module_fixture, session_fixture):
    print(f"\n test_b: url={session_fixture['base_url']}")