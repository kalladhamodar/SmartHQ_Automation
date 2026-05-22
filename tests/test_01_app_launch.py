import pytest

APP_PACKAGE = "com.smarthqpro.service.field"


@pytest.mark.order(1)
def test_app_launch(driver):
    """Verify app launches and correct package is active."""
    current_package = driver.current_package
    assert current_package == APP_PACKAGE, \
        f"❌ Wrong app launched. Expected: {APP_PACKAGE}, Got: {current_package}"
    print("✅ App Launched Successfully")