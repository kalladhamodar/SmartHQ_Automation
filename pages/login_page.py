from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (By.XPATH, "//android.widget.EditText[@resource-id='username']")
    PASSWORD = (By.XPATH, "//android.widget.EditText[@resource-id='password']")
    SIGN_IN_BTN = (By.XPATH, "//android.widget.Button[@resource-id='signin_btn']")
    ERROR_MSG = (By.XPATH, "//android.widget.TextView[@resource-id='error_message']")

    def login(self, username, password):
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.SIGN_IN_BTN)

    def is_username_field_present(self):
        return self.is_element_present(self.USERNAME)

    def is_password_field_present(self):
        return self.is_element_present(self.PASSWORD)

    def is_signin_button_present(self):
        return self.is_element_present(self.SIGN_IN_BTN)

    def is_error_message_displayed(self):
        return self.is_element_present(self.ERROR_MSG, timeout=10)

    def get_error_message_text(self):
        return self.get_element_text(self.ERROR_MSG)

    def clear_username(self):
        self.find_element(self.USERNAME).clear()

    def clear_password(self):
        self.find_element(self.PASSWORD).clear()
