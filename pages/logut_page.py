from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class logut_page(BasePage):

    settings_btn    = (By.XPATH, "//android.widget.ImageView[2]")
    yes_logout_btn  = (By.XPATH, "//android.widget.Button[@content-desc='Yes']")
    home_page_btn   = (By.XPATH, "//android.widget.Button[@content-desc='Service Tech']")

    # Field App
    LOGOUT_ACC_ID = "Logout - Connected to Field"
    # Prod App
    # LOGOUT_ACC_ID = "Logout"

    # ---------- Validations ----------

    def is_settings_button_present(self):
        """Validate Settings button is accessible."""
        assert self.is_element_present(self.settings_btn, timeout=10), \
            "❌ Settings button not found — cannot proceed with logout"

    def is_logout_confirmed(self):
        """Validate that logout was successful by checking home screen."""
        assert self.is_element_present(self.home_page_btn, timeout=15), \
            "❌ Logout failed — 'Service Tech' home button not found after logout"

    # ---------- Actions ----------

    def click_settings(self):
        self.is_settings_button_present()
        self.click(self.settings_btn)

    def click_logout(self):
        logout_element = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{self.LOGOUT_ACC_ID}"))'
        )
        assert logout_element is not None, \
            f"❌ Logout option '{self.LOGOUT_ACC_ID}' not found in settings"
        logout_element.click()

    def click_yes_logout(self):
        assert self.is_element_present(self.yes_logout_btn, timeout=10), \
            "❌ Logout confirmation dialog ('Yes' button) did not appear"
        self.click(self.yes_logout_btn)
        self.is_logout_confirmed()