from pages.dashboard_page import DashboardPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login_rejects_invalid_credentials(driver):
    home = HomePage(driver)
    login = LoginPage(driver)

    home.navigate_to_login()
    login.login("invalid@gmail.com", "wrong@123")
    assert login.is_error_message_displayed()
    print("❌ Invalid login verified")

    login.clear_username()
    login.clear_password()


def test_login_accepts_valid_credentials(logged_in_driver):
    dashboard = DashboardPage(logged_in_driver)
    dashboard.is_dashboard_loaded()
    print("✅ Valid login reached the dashboard")