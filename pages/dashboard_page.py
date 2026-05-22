from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class DashboardPage(BasePage):

    tutorial_skip_btn   = (By.XPATH, "//android.widget.Button[@content-desc='TUTORIAL SKIP']")
    done_btn            = (By.XPATH, "//android.widget.Button[@content-desc='Done']")
    allow_btn           = (By.XPATH, "//android.widget.Button[@resource-id='com.android.permissioncontroller:id/permission_allow_button']")
    location_access_btn = (By.XPATH, "//android.widget.Button[@resource-id='com.android.permissioncontroller:id/permission_allow_foreground_only_button']")
    bluetooth_close_btn = (By.XPATH, '//android.widget.Button[@content-desc="Close"]')
    settings_btn        = (By.XPATH, "//android.widget.ImageView[1]")
    smarthq_label       = (AppiumBy.ACCESSIBILITY_ID,"SMARTHQ SERVICE")

    # ---------- Validation Methods ----------

    def is_dashboard_loaded(self):
        """Validate dashboard is visible by checking SMARTHQ SERVICE label."""
        assert self.is_element_present(self.smarthq_label, timeout=20), \
            "❌ Dashboard not loaded — 'SMARTHQ SERVICE' label not found"

    def is_settings_button_present(self):
        """Validate Settings icon is present on dashboard."""
        assert self.is_element_present(self.settings_btn, timeout=10), \
            "❌ Settings button not found on dashboard"

    # ---------- Action Methods ----------

    def click_tutorial_skip(self):
        self.click(self.tutorial_skip_btn)

    def click_done(self):
        self.click(self.done_btn)

    def click_allow(self):
        self.click(self.allow_btn)

    def click_location_access(self):
        self.click(self.location_access_btn)

    def click_bluetooth_close(self):
        self.click(self.bluetooth_close_btn)

    def handle_post_login_dialogs(self):
        """
        Safely handle all post-login popups/dialogs.
        Each action is wrapped in try/except — dialogs may or may not appear.
        """
        for action in [
            self.click_tutorial_skip,
            self.click_done,
            self.click_allow,
            self.click_location_access,
            self.click_bluetooth_close,
        ]:
            try:
                action()
            except Exception:
                pass

        self.is_dashboard_loaded()
        self.is_settings_button_present()