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
        """Verify all post-login dialogs are handled and dashboard is ready."""
        dashboard = DashboardPage(dashboard_driver)

        for action in [
            dashboard.click_tutorial_skip,
            dashboard.click_done,
            dashboard.click_allow,
            dashboard.click_location_access,
            dashboard.click_bluetooth_close,
        ]:
            try:
                action()
            except Exception:
                pass

        # Final validation — dashboard must be loaded
        dashboard.is_dashboard_loaded()
        dashboard.is_settings_button_present()
        print("✅ All dialogs handled. Dashboard is fully ready.")