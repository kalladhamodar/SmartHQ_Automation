from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, value):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def is_element_present(self, locator, timeout=10):
        """Returns True if element is present within timeout, else False."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def is_element_visible(self, locator, timeout=10):
        """Returns True if element is visible within timeout, else False."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def get_element_text(self, locator, timeout=10):
        """Returns text/content-desc of an element."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text or element.get_attribute("content-desc") or ""
        except Exception:
            return ""

    def get_current_package(self):
        """Returns currently active app package."""
        return self.driver.current_package