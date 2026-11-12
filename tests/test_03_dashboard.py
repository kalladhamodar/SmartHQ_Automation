import pytest
from pages.dashboard_page import DashboardPage


@pytest.mark.order(4)
class Testdashboard:

    def test_dashboard_loads(self, logged_in_driver):
        """Verify dashboard loads with SMARTHQ SERVICE label after login."""
        dashboard = DashboardPage(logged_in_driver)
        dashboard.is_dashboard_loaded()
        print("✅ Dashboard loaded with SMARTHQ SERVICE label")

    def test_dashboard_settings_present(self, logged_in_driver):
        """Verify Settings button is present on dashboard."""
        dashboard = DashboardPage(logged_in_driver)
        dashboard.is_settings_button_present()
        print("✅ Settings button found on dashboard")

    def test_dashboard_handle_dialogs(self, dashboard_driver):
        """Verify the login fixture handles dialogs and leaves the dashboard ready."""
        dashboard = DashboardPage(dashboard_driver)
        dashboard.is_dashboard_loaded()
        dashboard.is_settings_button_present()
        print("✅ Dashboard is ready after post-login dialogs")