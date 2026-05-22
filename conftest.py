import time
import pytest
import allure

from appium.webdriver.appium_service import AppiumService
from allure_commons.types import AttachmentType
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from config.capabilities import get_driver
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.model_number import ModelPage
from pages.multi_model_page import MultiModelPage
from pages.dashboard_page import DashboardPage
from pages.logut_page import logut_page


# ---------- APPIUM SERVICE ----------
@pytest.fixture(scope="session")
def appium_service():
    service = AppiumService()
    service.start()
    time.sleep(5)
    yield service
    service.stop()


# ---------- DRIVER ----------
@pytest.fixture(scope="session")
def driver(appium_service):
    drv = get_driver()
    yield drv
    drv.quit()


# ---------- LOGIN (FUNCTION SCOPE - IMPORTANT) ----------
@pytest.fixture(scope="function")
def logged_in_driver(driver):
    home = HomePage(driver)
    login = LoginPage(driver)

    # Safe navigation to login screen
    try:
        home.click_service_tech()
        home.click_sign_in_here()
    except Exception:
        driver.close_app()
        driver.launch_app()
        home.click_service_tech()
        home.click_sign_in_here()

    # Validate login screen
    if not login.is_username_field_present():
        raise Exception("❌ Login page not loaded properly")

    login.is_password_field_present()
    login.is_signin_button_present()

    # Perform login
    login.login("dhamodartest36@gmail.com", "Dhamodar@236")

    return driver


# ---------- DASHBOARD (FUNCTION SCOPE) ----------
@pytest.fixture(scope="function")
def dashboard_driver(logged_in_driver):
    drv = logged_in_driver
    dashboard = DashboardPage(drv)

    actions = [
        dashboard.click_tutorial_skip,
        dashboard.click_done,
        dashboard.click_allow,
        dashboard.click_location_access,
        dashboard.click_bluetooth_close,
    ]

    for action in actions:
        try:
            action()
        except Exception as e:
            print(f"Skipped dashboard action: {e}")

    # Validate dashboard loaded
    dashboard.is_dashboard_loaded()
    dashboard.is_settings_button_present()

    return drv


# ---------- MODEL SELECTION ----------
@pytest.fixture(scope="function")
def model_selected_driver(dashboard_driver):
    drv = dashboard_driver
    model = ModelPage(drv)

    try:
        model.wait.until(
            EC.presence_of_element_located((
                AppiumBy.XPATH,
                '//android.view.View[contains(@content-desc,"SMARTHQ SERVICE")]'
            ))
        )
    except Exception:
        pass

    search_text = "GFD28"
    expected_model = "GFD28GYNFS"

    model.click_edit_btn()

    result = model.scroll_and_select_model(search_text, expected_model)
    assert result, f"❌ Model '{expected_model}' selection failed"

    model.click_done_btn()

    return drv


# ---------- MULTI MODEL ----------
@pytest.fixture(scope="function")
def multi_model_driver(dashboard_driver):
    drv = dashboard_driver
    multi = MultiModelPage(drv)

    models = [
        "GDT565HSY1SS",
        "GDT585HYY0FS",
        "GDT595HYY0FS",
        "GDT635HSR7SS",
        "GDF650SYV3FS",
        "GDF650SMV3ES",
    ]

    multi.enter_models_and_assert(models)

    return drv


# ---------- LOGOUT ----------
@pytest.fixture(scope="function")
def logout_driver(dashboard_driver):
    drv = dashboard_driver
    logout = logut_page(drv)

    try:
        logout.click_settings()
        logout.click_logout()
        logout.click_yes_logout()
    except Exception as e:
        print(f"Logout skipped due to: {e}")

    return drv


# ---------- SCREENSHOT ON FAILURE ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = None
        for key in item.funcargs:
            if "driver" in key:
                driver = item.funcargs[key]
                break

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG
            )