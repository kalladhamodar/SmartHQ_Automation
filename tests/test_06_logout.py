import pytest
from pages.home_page import HomePage
from pages.logut_page import logut_page


@pytest.mark.order(9)
def test_logout(dashboard_driver):
    """Verify logout flow: Settings → Logout → Yes → Home screen."""
    logout = logut_page(dashboard_driver)

    # Validate Settings button and click
    logout.click_settings()
    print("✅ Settings opened")

    # Validate Logout option found via scroll and click
    logout.click_logout()
    print("✅ Logout option clicked")

    # Validate confirmation dialog and click Yes — also validates home screen appears
    logout.click_yes_logout()
    HomePage(dashboard_driver).is_home_screen_loaded()
    print("✅ Logout confirmed — returned to home screen")