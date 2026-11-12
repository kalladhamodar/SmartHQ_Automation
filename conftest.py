import os
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

# ---------- APP RESET ----------
#app reset fixture to ensure a clean state before each test

APP_PACKAGE = "com.smarthqpro.service.field"

@pytest.fixture(autouse=True)
def reset_app(driver):
    driver.terminate_app(APP_PACKAGE)

    driver.execute_script(
        "mobile: clearApp",
        {"appId": APP_PACKAGE}
    )

    driver.activate_app(APP_PACKAGE)
    yield

@pytest.fixture(scope="session")
def valid_credentials():
    username = os.getenv("SMARTHQ_USERNAME")
    password = os.getenv("SMARTHQ_PASSWORD")
    if not username or not password:
        pytest.fail(
            "Set SMARTHQ_USERNAME and SMARTHQ_PASSWORD before running authenticated tests."
        )
    return username, password


# ---------- LOGIN (FUNCTION SCOPE - IMPORTANT) ----------
@pytest.fixture(scope="function")
def logged_in_driver(driver, valid_credentials):
    home = HomePage(driver)
    login = LoginPage(driver)

    # Safe navigation to login screen
    try:
        home.click_service_tech()
        home.click_sign_in_here()
    except Exception:
        driver.terminate_app("com.smarthqpro.service.field")
        driver.activate_app("com.smarthqpro.service.field")
        home.click_service_tech()
        home.click_sign_in_here()

    # Validate login screen
    if not login.is_username_field_present():
        raise Exception("❌ Login page not loaded properly")

    login.is_password_field_present()
    login.is_signin_button_present()

    # Perform login
    login.login(*valid_credentials)

    dashboard = DashboardPage(driver)
    dashboard.handle_post_login_dialogs()

    return driver


# ---------- DASHBOARD (FUNCTION SCOPE) ----------
@pytest.fixture(scope="function")
def dashboard_driver(logged_in_driver):
    drv = logged_in_driver
    dashboard = DashboardPage(drv)
    dashboard.is_dashboard_loaded()
    dashboard.is_settings_button_present()

    return drv


# ---------- MODEL SELECTION ----------
@pytest.fixture(scope="function")
def model_selected_driver(dashboard_driver):
    drv = dashboard_driver
    model = ModelPage(drv)


    model.wait.until(
            EC.presence_of_element_located((
                AppiumBy.XPATH,
                '//android.view.View[contains(@content-desc,"SMARTHQ SERVICE")]'
            ))
    )


    search_text = "GFD28"
    expected_model = "GFD28GYNFS"

    model.click_edit_btn()

    result = model.scroll_and_select_model(search_text, expected_model)
    assert result, f"❌ Model '{expected_model}' selection failed"

    model.click_done_btn()
    dashboard = DashboardPage(drv)
    dashboard.is_dashboard_loaded()

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


# ---------- SCREENSHOT ON FAILURE ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call") and report.failed:

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