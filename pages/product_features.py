import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductFeaturesPage(BasePage):

    product_features_title  = (By.XPATH, "//android.view.View[@content-desc='Product Features']")
    manuals_bulletins_title = (AppiumBy.ACCESSIBILITY_ID, "Manual & Bulletins")
    back_button             = (AppiumBy.ACCESSIBILITY_ID, "Back")
    training_manuals_title  = (AppiumBy.ACCESSIBILITY_ID, "Training Manual")
    product_overview_title  = (AppiumBy.ACCESSIBILITY_ID, "Product Overview")
    ethernet_title          = (AppiumBy.ACCESSIBILITY_ID, "Ethernet Port")
    kitchen_appliances_title= (AppiumBy.ACCESSIBILITY_ID, "Kitchen Appliances")
    close_button            = (AppiumBy.ACCESSIBILITY_ID, "Close")
    outside_popup           = (AppiumBy.ACCESSIBILITY_ID, "Scrim")

    # ---------- Validations ----------

    def __init__(self, driver):
        super().__init__(driver)


    def is_product_features_screen_loaded(self):
        """Validate Product Features screen is displayed."""
        assert self.is_element_present(self.product_features_title, timeout=15), \
            "❌ Product Features screen not loaded"

    def is_manuals_bulletins_displayed(self):
        """Validate Manual & Bulletins is present and click it."""
        assert self.is_element_present(self.manuals_bulletins_title, timeout=10), \
            "❌ 'Manual & Bulletins' not found on Product Features screen"
        self.click(self.manuals_bulletins_title)

    def click_back_button(self):
        assert self.is_element_present(self.back_button, timeout=10), \
            "❌ Back button not found"
        self.click(self.back_button)

    def is_training_manuals_displayed(self):
        """Validate Training Manual is present and click it."""
        assert self.is_element_present(self.training_manuals_title, timeout=10), \
            "❌ 'Training Manual' not found on Product Features screen"
        self.click(self.training_manuals_title)

    def clik_back_button(self):
        self.click_back_button()

    def is_product_overview_displayed(self):
        """Validate Product Overview is present and click it."""
        assert self.is_element_present(self.product_overview_title, timeout=10), \
            "❌ 'Product Overview' not found on Product Features screen"
        self.click(self.product_overview_title)

    def clk_back_button(self):
        self.click_back_button()

    def is_ethernet_port_displayed(self):
        """Validate Ethernet Port is present and click it."""
        assert self.is_element_present(self.ethernet_title, timeout=10), \
            "❌ 'Ethernet Port' not found on Product Features screen"
        self.click(self.ethernet_title)

    def is_kitchen_appliances_displayed(self):
        """Validate Kitchen Appliances is present and click it."""
        assert self.is_element_present(self.kitchen_appliances_title, timeout=10), \
            "❌ 'Kitchen Appliances' not found inside Ethernet Port section"
        self.click(self.kitchen_appliances_title)

    def is_close_button(self):
        """Validate Close button is present and click it."""
        assert self.is_element_present(self.close_button, timeout=10), \
            "❌ Close button not found on popup"
        self.click(self.close_button)

    def is_outside_popup(self):
        """Validate Scrim (outside popup area) is present and tap it."""
        assert self.is_element_present(self.outside_popup, timeout=10), \
            "❌ Scrim element not found — cannot dismiss popup by tapping outside"
        self.click(self.outside_popup)

