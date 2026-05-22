import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage


def get_login_data():
    return [
        ("invalid@gmail.com", "wrong@123", "invalid"),
        ("dhamodartest36@gmail.com", "Dhamodar@236", "valid")
    ]


@pytest.mark.parametrize("username,password,case_type", get_login_data())
def test_login_flow(username, password, case_type, driver):

    home = HomePage(driver)
    login = LoginPage(driver)

    home.navigate_to_login()

    login.login(username, password)

    if case_type == "invalid":
        assert login.is_error_message_displayed()
        print("❌ Invalid login verified")

        login.clear_username()
        login.clear_password()

    else:
        print("✅ Valid login success")