from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.login_page import LoginPage


class HomePage(BasePage):

    SERVICE_TECH_BTN = (By.XPATH, "//android.widget.Button[@content-desc='Service Tech']")
    SIGN_IN_HERE = (By.XPATH, "//android.view.View[@content-desc=' sign in here']")

    def is_service_tech_button_present(self):
        return self.is_element_present(self.SERVICE_TECH_BTN)

    def is_sign_in_here_present(self):
        return self.is_element_present(self.SIGN_IN_HERE)

    def click_service_tech(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.SERVICE_TECH_BTN)
        )
        self.click(self.SERVICE_TECH_BTN)

    def click_sign_in_here(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.SIGN_IN_HERE)
        )
        self.click(self.SIGN_IN_HERE)

        # wait for login page
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(LoginPage.USERNAME)
        )

    def navigate_to_login(self):
        if self.is_service_tech_button_present():
            self.click_service_tech()
        else:
            self.driver.close_app()
            self.driver.launch_app()
            self.click_service_tech()